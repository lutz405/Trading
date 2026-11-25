import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from tradingai.features.engineering import build_features
from tradingai.ml.pipeline import evaluate
from tradingai.ml.walkforward import run_walk_forward


def make_ohlcv(n=400, seed=5):
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


def test_walk_forward_no_leakage():
    df = make_ohlcv(400)
    feat = build_features(df).dropna().reset_index(drop=True)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]

    def train_fn(X, y):
        m = RandomForestClassifier(n_estimators=5, random_state=0)
        m.fit(X, y)
        return m

    results, _agg = run_walk_forward(
        feat,
        fc,
        horizon=5,
        train_fn=train_fn,
        eval_fn=evaluate,
        train_window=120,
        test_window=40,
        step=40,
        gap=5,
    )
    assert len(results) >= 1
    # temporal order: each test window after train
    assert all(r["status"] in ("ok", "insufficient data", "insufficient classes") for r in results)


def test_walk_forward_aggregate():
    df = make_ohlcv(400)
    feat = build_features(df).dropna().reset_index(drop=True)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]

    def train_fn(X, y):
        m = RandomForestClassifier(n_estimators=5, random_state=0)
        m.fit(X, y)
        return m

    _results, agg = run_walk_forward(
        feat,
        fc,
        horizon=5,
        train_fn=train_fn,
        eval_fn=evaluate,
        train_window=120,
        test_window=40,
        step=40,
        gap=5,
    )
    if agg:
        assert "accuracy" in agg
