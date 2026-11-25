import tempfile

import numpy as np
import pandas as pd
import pytest
import yaml

from tradingai.features.engineering import build_features
from tradingai.ml.labels import make_labels
from tradingai.ml.pipeline import run_training


def make_ohlcv(n=500, seed=9):
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


def _features(n=500, seed=9):
    df = make_ohlcv(n, seed)
    feat = build_features(df).dropna().reset_index(drop=True)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    return feat, fc


def _cfg(model_dir):
    with open("config/ml.yaml") as handle:
        cfg = yaml.safe_load(handle)
    cfg["model_dir"] = str(model_dir)
    cfg["use_gpu"] = False
    cfg["rf_params"]["n_estimators"] = 3
    cfg["xgb_params"]["n_estimators"] = 3
    return cfg


def test_label_horizon_exact():
    df = make_ohlcv(30)
    lab = make_labels(df, horizon=5)
    assert lab.iloc[-5:].isna().all()
    assert pd.notna(lab.iloc[-6])
    assert lab.iloc[-6] in {0, 1, 2}


def test_no_future_in_features():
    df = make_ohlcv(50)
    feat = build_features(df)
    # rsi at i equals rsi on prefix
    from tradingai.features.indicators import rsi

    for i in [10, 20, 40]:
        prefix = df.iloc[: i + 1]
        r = rsi(prefix["close"], 14).iloc[-1]
        assert np.isclose(r, feat["rsi_14"].iloc[i], equal_nan=True)


def test_gap_purge():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        result = run_training(feat, fc, _cfg(td))

    split = result["split"]
    assert split["purge"]["train_to_validation"] >= split["gap"]
    assert split["purge"]["validation_to_test"] >= split["gap"]
    assert split["train"]["label_end_position"] <= split["validation"]["start_position"]
    assert split["validation"]["label_end_position"] <= split["test"]["start_position"]


def test_small_dataset_raises():
    feat, fc = _features(60)
    with tempfile.TemporaryDirectory() as td, pytest.raises(ValueError, match="insufficient data"):
        run_training(feat, fc, _cfg(td))


def test_holdout_not_passed_to_train():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        result = run_training(feat, fc, _cfg(td))

    train = set(result["indices"]["train"])
    val = set(result["indices"]["val"])
    test = set(result["indices"]["test"])
    assert train.isdisjoint(val)
    assert train.isdisjoint(test)
    assert val.isdisjoint(test)
    assert max(train) < min(val)
    assert max(val) < min(test)
