import numpy as np
import pandas as pd

from tradingai.backtesting.engine import BacktestEngine
from tradingai.backtesting.metrics import compute_metrics


def make_df(n=20):
    rng = np.random.default_rng(1)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + 1
    low = close - 1
    open_ = close
    ts = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame({"timestamp": ts, "open": open_, "high": high, "low": low, "close": close})


def test_backtest_runs():
    df = make_df(20)
    eng = BacktestEngine(capital=1000, fee=0.001, slippage=0.0005)
    def dec(i, row, e):
        return "LONG_SIMULATED" if i % 3 == 0 else "HOLD"
    eng.run(df, dec)
    m = compute_metrics(eng)
    assert "total_trades" in m
    assert m["total_trades"] >= 0


def test_no_trades():
    df = make_df(20)
    eng = BacktestEngine(capital=1000)
    eng.run(df, lambda i, r, e: "HOLD")
    m = compute_metrics(eng)
    assert m["total_trades"] == 0
    assert m["win_rate"] == 0.0


def test_stop_loss():
    df = make_df(10)
    eng = BacktestEngine(capital=1000, fee=0, slippage=0)
    # force position then stop
    eng.position = {"side": "long", "idx": 0, "entry": 100.0, "qty": 1, "stop": 95.0, "take": 110.0, "fees": 0}
    # inject a row with low below stop by monkeypatch run not needed; check _exit
    eng._exit(1, 95.0, "stop")
    assert len(eng.trades) == 1
    assert eng.trades[0].pnl < 0
