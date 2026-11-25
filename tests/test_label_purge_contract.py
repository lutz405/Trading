import tempfile

import numpy as np
import pandas as pd
import pytest
import yaml

from tradingai.features.engineering import build_features
from tradingai.ml.labels import make_labels
from tradingai.ml.pipeline import _validate_label_purge, run_training


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


def test_label_purge_distance_equal_to_horizon_is_rejected():
    positions = np.arange(25)
    with pytest.raises(ValueError, match="train label close position"):
        _validate_label_purge(
            positions,
            train_end=5,
            val_start=9,
            val_end=15,
            test_start=20,
            horizon=5,
            n_df=30,
        )


def test_label_purge_minimum_safe_distance_is_horizon_plus_one():
    positions = np.arange(25)
    result = _validate_label_purge(
        positions,
        train_end=5,
        val_start=10,
        val_end=15,
        test_start=20,
        horizon=5,
        n_df=30,
    )
    assert result == {
        "train_label_end_position": 9,
        "validation_label_end_position": 19,
        "test_label_end_position": 29,
    }
    assert 10 - 4 == 6 == 5 + 1


def test_label_purge_uses_actual_sparse_positions():
    # The fifth X row is dataframe position 4 and the next X row is position 9.
    # A row-count-only check would accept this; the close of the first
    # validation row (position 9) is the close used by the last train label.
    positions = np.array([0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24])
    with pytest.raises(ValueError, match="train label close position"):
        _validate_label_purge(
            positions,
            train_end=5,
            val_start=5,
            val_end=11,
            test_start=11,
            horizon=5,
            n_df=30,
        )


def test_gap_equal_to_horizon_has_strict_label_separation():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        cfg = _cfg(td)
        horizon = int(cfg["horizon"])
        cfg["gap"] = horizon
        result = run_training(feat, fc, cfg)

    split = result["split"]
    assert split["gap"] == split["horizon"] == horizon
    for left, right in (("train", "validation"), ("validation", "test")):
        assert split[left]["label_end_position"] == split[left]["end_position"] + horizon
        assert split[left]["label_end_position"] < split[right]["start_position"]
        assert split["purge"][f"{left}_label_to_{right}"] >= 1
        # The minimum position distance that guarantees separation is
        # horizon + 1, because the last partition row itself is before the
        # next partition.
        assert split[right]["start_position"] - split[left]["end_position"] >= horizon + 1


def test_label_close_position_is_used_and_first_validation_close_is_not():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        cfg = _cfg(td)
        horizon = int(cfg["horizon"])
        cfg["gap"] = horizon
        result = run_training(feat, fc, cfg)
        vol_mult = float(cfg["vol_mult"])

    split = result["split"]
    last_train_pos = split["train"]["end_position"]
    label_end = split["train"]["label_end_position"]
    val_start = split["validation"]["start_position"]
    assert label_end == last_train_pos + horizon
    assert label_end < val_start

    labels = make_labels(feat, horizon=horizon, vol_mult=vol_mult)
    base_label = labels.iloc[last_train_pos]
    assert pd.notna(base_label)

    close_col = feat.columns.get_loc("close")
    base_close = feat["close"].to_numpy(dtype=float)

    # Force a different future return at the documented label close: this must
    # change the last train label, proving that this is the close it uses.
    changed = feat.copy()
    replacement = base_close[last_train_pos] * (0.5 if base_label == 2 else 3.0)
    changed.iloc[label_end, close_col] = replacement
    changed_labels = make_labels(changed, horizon=horizon, vol_mult=vol_mult)
    assert changed_labels.iloc[last_train_pos] != base_label

    # Changing the first validation close must not affect the last train label.
    untouched = feat.copy()
    untouched.iloc[val_start, close_col] = base_close[val_start] * 3.0
    untouched_labels = make_labels(untouched, horizon=horizon, vol_mult=vol_mult)
    assert untouched_labels.iloc[last_train_pos] == base_label


def test_gap_below_horizon_is_rejected():
    feat, fc = _features()
    with tempfile.TemporaryDirectory() as td:
        cfg = _cfg(td)
        cfg["gap"] = int(cfg["horizon"]) - 1
        with pytest.raises(ValueError, match="gap"):
            run_training(feat, fc, cfg)
