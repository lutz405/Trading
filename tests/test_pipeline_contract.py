import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from tradingai.ml.calibration import Calibrator
from tradingai.ml.pipeline import (
    _CalibratedEnsemble,
    _validate_temporal,
    evaluate,
    run_training,
    train_xgb,
)


def _training_data(n=150, seed=0):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame(rng.normal(size=(n, 3)), columns=["a", "b", "c"])
    y = np.tile([0, 1, 2], n // 3)
    return X, y


def test_calibrated_ensemble_evaluates_when_test_misses_a_class():
    X, y = _training_data()
    rf = RandomForestClassifier(n_estimators=5, random_state=0).fit(X, y)
    xgbm = train_xgb(X, y, {"n_estimators": 5, "random_state": 0}, use_gpu=False)
    classes = [0, 1, 2]

    val_ensemble = (rf.predict_proba(X) + xgbm.predict_proba(X)) / 2.0
    cal = Calibrator().fit(val_ensemble, y, classes=classes)
    assert cal.fitted
    ensemble = _CalibratedEnsemble(rf, xgbm, cal, classes)
    assert list(ensemble.classes_) == classes

    X_test = X.iloc[:20].copy()
    y_test = np.array([0, 1] * 10)
    metrics = evaluate(ensemble, X_test, y_test)

    assert metrics["classes_present"] == [0, 1]
    assert len(metrics["confusion_matrix"]) == 3
    assert np.isfinite(metrics["log_loss"])


def test_calibrated_ensemble_evaluates_with_single_class_test_partition():
    X, y = _training_data()
    rf = RandomForestClassifier(n_estimators=5, random_state=0).fit(X, y)
    xgbm = train_xgb(X, y, {"n_estimators": 5, "random_state": 0}, use_gpu=False)
    classes = [0, 1, 2]
    val_ensemble = (rf.predict_proba(X) + xgbm.predict_proba(X)) / 2.0
    cal = Calibrator().fit(val_ensemble, y, classes=classes)
    ensemble = _CalibratedEnsemble(rf, xgbm, cal, classes)

    y_test = np.zeros(20, dtype=int)
    metrics = evaluate(ensemble, X.iloc[:20], y_test)

    assert metrics["classes_present"] == [0]
    assert len(metrics["confusion_matrix"]) == 3
    assert np.isfinite(metrics["log_loss"])
    assert np.isfinite(metrics["brier"])


def test_evaluate_requires_explicit_model_classes():
    X, y = _training_data(30)
    model = RandomForestClassifier(n_estimators=2, random_state=0).fit(X, y)
    del model.classes_

    with pytest.raises(ValueError, match="classes_"):
        evaluate(model, X, y)


def test_train_xgb_rejects_non_contiguous_labels():
    X, _ = _training_data(30)
    y = np.tile([0, 2, 3], 10)
    with pytest.raises(ValueError, match="contiguous"):
        train_xgb(X, y, {"n_estimators": 2}, use_gpu=False)


def test_run_training_fails_when_a_label_class_is_missing():
    rng = np.random.default_rng(4)
    n = 220
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"),
            "close": close,
            "a": rng.normal(size=n),
            "b": rng.normal(size=n),
        }
    )
    cfg = {
        "horizon": 5,
        "gap": 5,
        "test_size": 0.2,
        "val_size": 0.2,
        "vol_mult": 0.5,
        "use_gpu": False,
        "rf_params": {"n_estimators": 2},
        "xgb_params": {"n_estimators": 2},
    }
    with (
        tempfile.TemporaryDirectory() as td,
        patch("tradingai.ml.pipeline.LABEL_CLASSES", (0, 1, 2, 3)),
        pytest.raises(ValueError, match="missing classes"),
    ):
        cfg["model_dir"] = td
        run_training(df, ["a", "b"], cfg)


def test_temporal_validation_rejects_shuffled_rows():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=10, freq="h", tz="UTC"),
            "a": np.arange(10.0),
        }
    )
    X = df.loc[[2, 1], ["a"]]
    y = pd.Series([1, 0], index=[2, 1])
    with pytest.raises(ValueError, match="chronological"):
        _validate_temporal(df, X, y, horizon=2, gap=2)


def test_temporal_validation_rejects_duplicate_timestamps():
    df = pd.DataFrame(
        {
            "timestamp": [pd.Timestamp("2024-01-01", tz="UTC")] * 3,
            "a": np.arange(3.0),
        }
    )
    X = df[["a"]]
    y = pd.Series([0, 1, 0], index=df.index)
    with pytest.raises(ValueError, match="duplicate timestamps"):
        _validate_temporal(df, X, y, horizon=1, gap=1)
