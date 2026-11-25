import numpy as np
import pandas as pd

from tradingai.features.indicators import rsi, macd, ema, sma, atr, bollinger_bands, adx, vwap


def make_ohlcv(n=60, seed=1):
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0, 1, n)
    low = close - rng.uniform(0, 1, n)
    open_ = close + rng.normal(0, 0.5, n)
    vol = rng.uniform(1, 5, n)
    ts = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame({"timestamp": ts, "open": open_, "high": high, "low": low, "close": close, "volume": vol})


def test_sma_ema():
    df = make_ohlcv()
    s = sma(df["close"], 5)
    e = ema(df["close"], 5)
    assert s.isna().sum() == 4
    assert not e.isna().all()


def test_rsi_range():
    df = make_ohlcv()
    r = rsi(df["close"], 14)
    valid = r.dropna()
    assert (valid >= 0).all() and (valid <= 100).all()


def test_macd_shapes():
    df = make_ohlcv()
    line, sig, hist = macd(df["close"])
    assert len(line) == len(df)


def test_atr_positive():
    df = make_ohlcv()
    a = atr(df, 14)
    assert (a.dropna() >= 0).all()


def test_bollinger_order():
    df = make_ohlcv()
    u, m, l = bollinger_bands(df["close"], 20, 2.0)
    valid = ~u.isna()
    assert (u[valid] >= m[valid]).all()
    assert (m[valid] >= l[valid]).all()


def test_adx_range():
    df = make_ohlcv(120)
    a = adx(df, 14)
    valid = a.dropna()
    assert (valid >= 0).all()


def test_vwap_no_future():
    df = make_ohlcv()
    v = vwap(df)
    # causal: vwap at i uses only rows <= i
    first_day = df["timestamp"].dt.date == df["timestamp"].dt.date.iloc[0]
    sub = df[first_day]
    tp = (sub["high"] + sub["low"] + sub["close"]) / 3
    manual = (tp * sub["volume"]).cumsum() / sub["volume"].cumsum()
    v_sub = vwap(df)[first_day].reset_index(drop=True)
    assert np.allclose(v_sub.values, manual.values, atol=1e-9)
