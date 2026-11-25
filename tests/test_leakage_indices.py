import json
import tempfile
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
import pytest
import yaml

from tradingai.features.engineering import build_features
from tradingai.ml.calibration import Calibrator
from tradingai.ml.pipeline import run_training, train_rf, train_xgb


def make_ohlcv(n=400, seed=11):
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0, 1, n)
    low = close - rng.uniform(0, 1, n)
    open_ = close + rng.normal(0, 0.5, n)
    vol = rng.uniform(1, 5, n)
    ts = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame(
        {"timestamp": ts, "open": open_, "high": high, "low": low, "close": close, "volume": vol}
    )


def _cfg(model_dir):
    with open("config/ml.yaml") as handle:
        cfg = yaml.safe_load(handle)
    cfg["model_dir"] = str(model_dir)
    cfg["use_gpu"] = False
    cfg["rf_params"]["n_estimators"] = 5
    cfg["xgb_params"]["n_estimators"] = 5
    return cfg


def _features():
    df = make_ohlcv(400)
    feat = build_features(df).dropna().reset_index(drop=True)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    return feat, fc


def _instrumented_run(feat, fc, cfg, captured):
    orig_train_rf = train_rf
    orig_train_xgb = train_xgb
    orig_cal_fit = Calibrator.fit

    def spy_train_rf(X, y, params):
        captured["train_idx"] = list(X.index)
        return orig_train_rf(X, y, params)

    def spy_train_xgb(X, y, params, use_gpu):
        captured["xgb_train_idx"] = list(X.index)
        return orig_train_xgb(X, y, params, use_gpu)

    def spy_cal_fit(self, proba_val, y_val, classes=None):
        captured["cal_n"] = len(proba_val)
        captured["cal_classes"] = list(classes) if classes is not None else None
        return orig_cal_fit(self, proba_val, y_val, classes=classes)

    with (
        patch("tradingai.ml.pipeline.train_rf", side_effect=spy_train_rf),
        patch("tradingai.ml.pipeline.train_xgb", side_effect=spy_train_xgb),
        patch.object(Calibrator, "fit", spy_cal_fit),
    ):
        res = run_training(feat, fc, cfg)
    captured["indices"] = res.get("indices", {})
    captured["split"] = res.get("split", {})
    return res, captured


def test_indices_real():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        captured = {}
        result, captured = _instrumented_run(feat, fc, _cfg(td), captured)

        assert captured["train_idx"] == captured["indices"]["train"]
        assert captured["xgb_train_idx"] == captured["indices"]["train"]
        assert captured["cal_n"] == len(captured["indices"]["val"])
        assert captured["cal_classes"] == [0, 1, 2]
        assert result["calibration"]["fitted"] is True

        train = captured["indices"]["train"]
        val = captured["indices"]["val"]
        test = captured["indices"]["test"]
        assert max(train) < min(val) < max(val) < min(test)
        assert captured["split"]["purge"]["train_to_validation"] >= 5
        assert captured["split"]["purge"]["validation_to_test"] >= 5


def test_holdout_independence_compares_learned_state():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td2:
        result1 = run_training(feat, fc, _cfg(td1))
        test_idx = result1["indices"]["test"]

        feat2 = feat.copy()
        # Mutate only holdout feature values.  Train and validation are unchanged,
        # so the learned models and calibrator must be bit-for-bit equivalent in
        # their predictions on a fixed probe grid.
        feat2.loc[test_idx, fc] = feat2.loc[test_idx, fc] + 1000.0
        result2 = run_training(feat2, fc, _cfg(td2))

        rf1 = joblib.load(f"{td1}/rf.joblib")
        rf2 = joblib.load(f"{td2}/rf.joblib")
        xgb1 = joblib.load(f"{td1}/xgb.joblib")
        xgb2 = joblib.load(f"{td2}/xgb.joblib")
        cal1 = Calibrator.load(f"{td1}/calibrator.json")
        cal2 = Calibrator.load(f"{td2}/calibrator.json")

        probe = feat.loc[result1["indices"]["train"][:20], fc]
        np.testing.assert_allclose(rf1.predict_proba(probe), rf2.predict_proba(probe), atol=1e-12)
        np.testing.assert_allclose(xgb1.predict_proba(probe), xgb2.predict_proba(probe), atol=1e-12)
        proba_probe = np.array([[0.2, 0.3, 0.5], [0.6, 0.2, 0.2], [0.1, 0.1, 0.8]])
        np.testing.assert_allclose(cal1.transform(proba_probe), cal2.transform(proba_probe))
        assert cal1.classes == cal2.classes == [0, 1, 2]
        assert result1["split"] == result2["split"]


def test_gap_smaller_than_horizon_rejected():
    feat, fc = _features()
    cfg = _cfg("models/_never_written")
    cfg["gap"] = 0
    cfg["horizon"] = 5
    with pytest.raises(ValueError, match="gap"):
        run_training(feat, fc, cfg)


def test_datetime_index_split_supported():
    df = make_ohlcv(400)
    df.index = pd.DatetimeIndex(df["timestamp"])
    feat = build_features(df).dropna()
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    with tempfile.TemporaryDirectory() as td:
        result = run_training(feat, fc, _cfg(td))
        assert result["split"]["n_rows"] > 0


def test_sparse_integer_index_split_supported():
    df = make_ohlcv(400)
    df.index = np.arange(len(df)) * 10
    feat = build_features(df).dropna()
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    with tempfile.TemporaryDirectory() as td:
        result = run_training(feat, fc, _cfg(td))
        assert result["split"]["n_rows"] > 0


def test_artifacts_include_classes_and_split_manifest():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        result = run_training(feat, fc, _cfg(td))
        with open(f"{td}/rf.json") as handle:
            metadata = json.load(handle)
        assert metadata["classes"] == [0, 1, 2]
        assert metadata["split"] == result["split"]
