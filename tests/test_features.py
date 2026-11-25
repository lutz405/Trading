import numpy as np
import pandas as pd

from tradingai.features.engineering import build_features
from tradingai.features.validation import validate_features
from tradingai.features.multitimeframe import align_higher_timeframe
from tradingai.features.volume import volume_features


def make_ohlcv(n=80, seed=2):
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0, 1, n)
    low = close - rng.uniform(0, 1, n)
    open_ = close + rng.normal(0, 0.5, n)
    vol = rng.uniform(1, 5, n)
    ts = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame({"timestamp": ts, "open": open_, "high": high, "low": low, "close": close, "volume": vol})


def test_build_features():
    df = make_ohlcv()
    out = build_features(df)
    assert "rsi_14" in out.columns
    assert "vol_rel" in out.columns
    validate_features(out.dropna().reset_index(drop=True), min_rows=10)


def test_no_future_leakage():
    df = make_ohlcv()
    out = build_features(df)
    # rsi at i should equal rsi computed on prefix
    from tradingai.features.indicators import rsi
    for i in [20, 40, 60]:
        prefix = df.iloc[: i + 1]
        r = rsi(prefix["close"], 14).iloc[-1]
        assert np.isclose(r, out["rsi_14"].iloc[i], equal_nan=True)


def test_multitimeframe_align():
    base = make_ohlcv(20)
    base["timestamp"] = pd.date_range("2024-01-01", periods=20, freq="h", tz="UTC")
    higher = base.iloc[::4].copy().reset_index(drop=True)
    higher["rsi_14"] = 50.0
    merged = align_higher_timeframe(base, higher, ["rsi_14"], "4h")
    assert "rsi_14_4h" in merged.columns
    assert merged["rsi_14_4h"].isna().sum() <= 4


def test_volume_features():
    df = make_ohlcv()
    vf = volume_features(df, 10)
    assert "vol_anomaly" in vf.columns
