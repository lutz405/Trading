import tempfile

import numpy as np
import pandas as pd
import yaml

from tradingai.features.engineering import build_features
from tradingai.ml.dataset import build_dataset, chronological_split
from tradingai.ml.ensemble import ensemble_proba, predict_with_abstention
from tradingai.ml.labels import make_labels
from tradingai.ml.pipeline import run_training


def make_ohlcv(n=300, seed=3):
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


def test_labels():
    df = make_ohlcv()
    lab = make_labels(df, horizon=5)
    assert set(lab.dropna().unique()).issubset({0, 1, 2})
    assert lab.iloc[-5:].isna().all()


def test_dataset_no_leakage():
    df = make_ohlcv()
    feat = build_features(df)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    X, y = build_dataset(feat, fc, horizon=5)
    assert len(X) == len(y)
    assert not X.isna().any().any()


def test_chronological_split():
    df = make_ohlcv()
    feat = build_features(df)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    X, y = build_dataset(feat, fc, horizon=5)
    Xtr, Xte, ytr, yte = chronological_split(X, y, 0.2)
    assert len(Xtr) + len(Xte) == len(X)
    assert Xtr.index.equals(ytr.index)
    assert Xte.index.equals(yte.index)
    assert Xtr.index.max() < Xte.index.min()
    assert set(Xtr.index).isdisjoint(set(Xte.index))


def test_ensemble():
    rf = np.array([[0.2, 0.5, 0.3], [0.1, 0.2, 0.7]])
    xg = np.array([[0.3, 0.4, 0.3], [0.2, 0.3, 0.5]])
    p = ensemble_proba(rf, xg, 0.4, 0.6)
    assert np.allclose(p.sum(axis=1), 1.0)
    pred = predict_with_abstention(p, 0.6)
    assert set(pred.tolist()).issubset({-1, 0, 1, 2})


def test_training_runs():
    df = make_ohlcv(300)
    feat = build_features(df).dropna().reset_index(drop=True)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    with open("config/ml.yaml") as f:
        cfg = yaml.safe_load(f)
    cfg["use_gpu"] = False
    cfg["rf_params"]["n_estimators"] = 10
    cfg["xgb_params"]["n_estimators"] = 10
    with tempfile.TemporaryDirectory() as td:
        cfg["model_dir"] = td
        res = run_training(feat, fc, cfg)
        assert "rf" in res and "xgb" in res
        assert 0 <= res["rf"]["accuracy"] <= 1
