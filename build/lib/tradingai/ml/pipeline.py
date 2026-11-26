from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
)

from .calibration import Calibrator
from .dataset import build_dataset
from .labels import LABEL_CLASSES
from .metrics import compute_metrics as compute_advanced


def gpu_available() -> bool:
    try:
        import xgboost as x

        info = x.build_info()
        return bool(info.get("USE_CUDA"))
    except (ImportError, AttributeError, KeyError, TypeError):
        return False


def train_rf(X_train, y_train, params: dict):
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    return model


def train_xgb(X_train, y_train, params: dict, use_gpu: bool):
    classes = np.unique(y_train)
    if not np.array_equal(classes, np.arange(len(classes))):
        raise ValueError("XGBoost requires contiguous integer classes starting at 0")
    p = dict(params)
    p.setdefault("tree_method", "hist")
    p.setdefault("device", "cuda" if use_gpu else "cpu")
    p["objective"] = "multi:softprob"
    p["num_class"] = len(classes)
    p["eval_metric"] = "mlogloss"
    model = xgb.XGBClassifier(**p)
    model.fit(X_train, y_train)
    return model


def _aligned_proba(model, X, classes: list) -> np.ndarray:
    proba = np.asarray(model.predict_proba(X), dtype=float)
    model_classes = list(model.classes_)
    if model_classes != list(classes):
        if set(model_classes) != set(classes):
            raise ValueError("model classes do not match the expected classes")
        order = [model_classes.index(c) for c in classes]
        proba = proba[:, order]
    row_sums = proba.sum(axis=1, keepdims=True)
    if (row_sums <= 0).any():
        raise ValueError("predict_proba contains non-positive rows")
    return proba / row_sums


def evaluate(model, X, y) -> dict:
    if "XGB" in type(model).__name__:
        try:
            model.set_params(device="cpu")
        except (TypeError, ValueError):
            pass
    if not hasattr(model, "classes_"):
        raise ValueError("model must expose classes_ for evaluation")
    classes = [c.item() if isinstance(c, np.generic) else c for c in list(model.classes_)]
    y = np.asarray(y)
    if len(X) != len(y):
        raise ValueError("X and y have different lengths")
    if len(y) == 0:
        raise ValueError("cannot evaluate an empty partition")
    unknown = sorted(set(y.tolist()) - set(classes))
    if unknown:
        raise ValueError(f"labels outside model classes: {unknown}")

    pred = np.asarray(model.predict(X))
    proba = np.asarray(model.predict_proba(X), dtype=float)
    if proba.shape != (len(y), len(classes)):
        raise ValueError("predict_proba shape does not match model classes")
    if not np.isfinite(proba).all():
        raise ValueError("predict_proba contains non-finite values")
    row_sums = proba.sum(axis=1, keepdims=True)
    if (row_sums <= 0).any():
        raise ValueError("predict_proba contains non-positive rows")
    # XGBoost returns float32 values that can sum to 0.99999994.  Normalising
    # here keeps sklearn's probability metrics well-defined.
    proba = proba / row_sums

    present = sorted(set(y.tolist()))
    briers = []
    for i, c in enumerate(classes):
        if c in present:
            yi = (y == c).astype(int)
            briers.append(brier_score_loss(yi, proba[:, i]))
    brier = float(sum(briers) / len(briers)) if briers else float("nan")
    metrics = {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(
            precision_score(y, pred, average="macro", zero_division=0, labels=classes)
        ),
        "recall": float(recall_score(y, pred, average="macro", zero_division=0, labels=classes)),
        "f1": float(f1_score(y, pred, average="macro", zero_division=0, labels=classes)),
        "confusion_matrix": confusion_matrix(y, pred, labels=classes).tolist(),
        "brier": brier,
        "log_loss": float(log_loss(y, proba, labels=classes)),
        "classes_present": present,
    }
    adv = compute_advanced(y, proba, labels=classes)
    metrics.update(adv)
    return metrics


class _CalibratedEnsemble:
    def __init__(self, rf, xgbm, calibrator, classes):
        self.rf = rf
        self.xgbm = xgbm
        self.calibrator = calibrator
        self.classes_ = np.asarray(classes)
        self.classes = list(self.classes_)
        if not calibrator.fitted:
            raise ValueError("calibrated ensemble requires a fitted calibrator")
        for name, model in (("rf", rf), ("xgb", xgbm)):
            if hasattr(model, "classes_") and set(model.classes_) != set(self.classes):
                raise ValueError(f"{name} classes do not match ensemble classes")

    def predict_proba(self, X):
        rf_p = _aligned_proba(self.rf, X, self.classes)
        xgb_p = _aligned_proba(self.xgbm, X, self.classes)
        ens = (rf_p + xgb_p) / 2.0
        return self.calibrator.transform(ens)

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]


def save_artifact(model, path: Path, metadata: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    (path.with_suffix(".json")).write_text(json.dumps(metadata, indent=2, default=str))


def _validate_temporal(df, X, y, horizon, gap):
    if "timestamp" not in df.columns:
        raise ValueError("missing timestamp column")
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if ts.isna().any():
        raise ValueError("invalid timestamps")
    if ts.duplicated().any():
        raise ValueError("duplicate timestamps")
    if not ts.is_monotonic_increasing:
        raise ValueError("timestamps not sorted")
    if not df.index.is_unique:
        raise ValueError("df index must be unique")
    if not X.index.equals(y.index):
        raise ValueError("index mismatch between X and y")
    if X.index.duplicated().any():
        raise ValueError("duplicate indices")
    positions = df.index.get_indexer(X.index)
    if (positions < 0).any():
        raise ValueError("X contains rows that are not in df")
    if not np.all(np.diff(positions) > 0):
        raise ValueError("X rows are not in chronological df order")
    if int(gap) < int(horizon):
        raise ValueError("gap must be greater than or equal to the label horizon")
    return positions, ts


def _validate_label_purge(
    positions,
    *,
    train_end: int,
    val_start: int,
    val_end: int,
    test_start: int,
    horizon: int,
    n_df: int,
) -> dict[str, int]:
    """Return the last dataframe close position used by each partition's labels.

    ``make_labels`` uses ``close.shift(-horizon)``, so the label attached to the
    dataframe row at position ``p`` reads the close at ``p + horizon``.  If the
    last train row is at position ``t`` and validation starts at ``v``, strict
    separation requires::

        t + horizon < v
        <=> v - t >= horizon + 1

    The same argument applies between validation and test.  This check is
    performed on actual dataframe positions, not on the configured ``gap``, so
    missing feature rows cannot silently shorten the purge.  ``gap == horizon``
    is safe when positions are contiguous because the last train row itself
    contributes one position: ``v - t == gap + 1 == horizon + 1``.
    """
    train_last_pos = int(positions[train_end - 1])
    val_start_pos = int(positions[val_start])
    val_last_pos = int(positions[val_end - 1])
    test_start_pos = int(positions[test_start])
    test_last_pos = int(positions[-1])

    train_label_end = train_last_pos + horizon
    val_label_end = val_last_pos + horizon
    test_label_end = test_last_pos + horizon

    for name, label_end in (
        ("train", train_label_end),
        ("validation", val_label_end),
        ("test", test_label_end),
    ):
        if label_end >= n_df:
            raise ValueError(f"{name} label close position {label_end} is outside the dataframe")

    if train_label_end >= val_start_pos:
        raise ValueError(
            "label leakage: train label close position "
            f"{train_label_end} is not before validation start {val_start_pos}"
        )
    if val_label_end >= test_start_pos:
        raise ValueError(
            "label leakage: validation label close position "
            f"{val_label_end} is not before test start {test_start_pos}"
        )
    return {
        "train_label_end_position": train_label_end,
        "validation_label_end_position": val_label_end,
        "test_label_end_position": test_label_end,
    }


def run_training(df, feature_cols, cfg) -> dict:
    horizon = int(cfg["horizon"])
    gap = int(cfg.get("gap", horizon))
    vol_mult = float(cfg.get("vol_mult", 0.5))
    X, y = build_dataset(df, feature_cols, horizon=horizon, vol_mult=vol_mult)
    positions, _ = _validate_temporal(df, X, y, horizon, gap)

    n = len(X)
    test_size = float(cfg.get("test_size", 0.2))
    val_size = float(cfg.get("val_size", 0.2))
    if not (0 < test_size < 1) or not (0 < val_size < 1):
        raise ValueError("test_size and val_size must be between 0 and 1")
    test_n = int(n * test_size)
    val_n = int(n * val_size)
    train_end = n - test_n - val_n - gap * 2
    if test_n <= 0 or val_n <= 0 or train_end <= 0:
        raise ValueError("insufficient data for splits")
    val_start = train_end + gap
    val_end = val_start + val_n
    test_start = val_end + gap
    if test_start >= n:
        raise ValueError("insufficient data for test split")

    if positions[val_start] - positions[train_end - 1] < gap:
        raise ValueError("insufficient gap train-val")
    if positions[test_start] - positions[val_end - 1] < gap:
        raise ValueError("insufficient gap val-test")

    train_end_pos = int(positions[train_end - 1])
    val_start_pos = int(positions[val_start])
    val_end_pos = int(positions[val_end - 1])
    test_start_pos = int(positions[test_start])
    label_ends = _validate_label_purge(
        positions,
        train_end=train_end,
        val_start=val_start,
        val_end=val_end,
        test_start=test_start,
        horizon=horizon,
        n_df=len(df),
    )

    Xtr = X.iloc[:train_end]
    ytr = y.iloc[:train_end]
    Xval = X.iloc[val_start:val_end]
    yval = y.iloc[val_start:val_end]
    Xte = X.iloc[test_start:]
    yte = y.iloc[test_start:]

    expected_classes = list(LABEL_CLASSES)
    for name, target in (("train", ytr), ("validation", yval)):
        missing = [c for c in expected_classes if c not in set(target.tolist())]
        if missing:
            raise ValueError(f"{name} partition is missing classes: {missing}")

    use_gpu = gpu_available() if cfg.get("use_gpu", True) else False
    rf_params = cfg["rf_params"]
    xgb_params = cfg["xgb_params"]
    rf = train_rf(Xtr, ytr, rf_params)
    xgbm = train_xgb(Xtr, ytr, xgb_params, use_gpu)

    val_rf = _aligned_proba(rf, Xval, expected_classes)
    val_xgb = _aligned_proba(xgbm, Xval, expected_classes)
    val_ensemble = (val_rf + val_xgb) / 2.0
    calibrator = Calibrator().fit(val_ensemble, yval, classes=expected_classes)
    if not calibrator.fitted:
        raise ValueError(f"calibration failed: {calibrator.reason}")

    calibrated_model = _CalibratedEnsemble(rf, xgbm, calibrator, expected_classes)
    rf_metrics = evaluate(rf, Xte, yte)
    xgb_metrics = evaluate(xgbm, Xte, yte)
    calibrated_metrics = evaluate(calibrated_model, Xte, yte)

    manifest = {
        "horizon": horizon,
        "gap": gap,
        "n_rows": n,
        "train": {
            "start": 0,
            "end": train_end,
            "start_position": int(positions[0]),
            "end_position": train_end_pos,
            "label_end_position": label_ends["train_label_end_position"],
        },
        "validation": {
            "start": val_start,
            "end": val_end,
            "start_position": val_start_pos,
            "end_position": val_end_pos,
            "label_end_position": label_ends["validation_label_end_position"],
        },
        "test": {
            "start": test_start,
            "end": n,
            "start_position": test_start_pos,
            "end_position": int(positions[-1]),
            "label_end_position": label_ends["test_label_end_position"],
        },
        "purge": {
            "train_to_validation": val_start_pos - train_end_pos,
            "validation_to_test": test_start_pos - val_end_pos,
            "train_label_to_validation": val_start_pos - label_ends["train_label_end_position"],
            "validation_label_to_test": test_start_pos
            - label_ends["validation_label_end_position"],
        },
    }

    meta = {
        "features": feature_cols,
        "horizon": horizon,
        "label_config": {"vol_mult": vol_mult, "classes": expected_classes},
        "gpu_used": use_gpu,
        "rf_params": rf_params,
        "xgb_params": xgb_params,
        "classes": expected_classes,
        "split": manifest,
        "created_at": datetime.now(UTC).isoformat(),
    }
    import sklearn
    import xgboost

    meta["versions"] = {"sklearn": sklearn.__version__, "xgboost": xgboost.__version__}
    model_dir = Path(cfg["model_dir"])
    save_artifact(
        rf,
        model_dir / "rf.joblib",
        {**meta, "metrics": rf_metrics, "calibration": calibrator.metadata()},
    )
    save_artifact(
        xgbm,
        model_dir / "xgb.joblib",
        {**meta, "metrics": xgb_metrics, "calibration": calibrator.metadata()},
    )
    calibrator.save(model_dir / "calibrator.json")
    return {
        "rf": rf_metrics,
        "xgb": xgb_metrics,
        "calibrated": calibrated_metrics,
        "gpu_used": use_gpu,
        "indices": {
            "train": list(Xtr.index),
            "val": list(Xval.index),
            "test": list(Xte.index),
        },
        "split": manifest,
        "calibration": calibrator.metadata(),
    }
