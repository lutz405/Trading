import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from tradingai.backtesting.engine import BacktestEngine
from tradingai.ml.pipeline import evaluate
from tradingai.paper.broker import PaperBroker


def test_backtest_accounting():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=5, freq="h", tz="UTC"),
        "open": [100.0, 101, 102, 103, 104],
        "high": [101, 102, 103, 104, 105],
        "low": [99, 100, 101, 102, 103],
        "close": [100.5, 101.5, 102.5, 103.5, 104.5],
    })
    eng = BacktestEngine(capital=1000, fee=0.001, slippage=0.0005)
    def dec(i, row, e):
        return "LONG_SIMULATED" if i == 0 else "HOLD"
    eng.run(df, dec)
    # final capital should equal initial + net pnl
    assert abs(eng.capital - (1000 + sum(t.pnl for t in eng.trades))) < 1e-6


def test_backtest_uses_open():
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=3, freq="h", tz="UTC"),
        "open": [100.0, 105.0, 106.0],
        "high": [101, 106, 107],
        "low": [99, 104, 105],
        "close": [100.5, 105.5, 106.5],
    })
    eng = BacktestEngine(capital=1000, fee=0, slippage=0)
    def dec(i, row, e):
        return "LONG_SIMULATED" if i == 0 else "HOLD"
    eng.run(df, dec)
    assert eng.trades[0].entry_price == 105.0


def test_evaluate_missing_class():
    X = pd.DataFrame({"a": [1, 2, 3, 4]})
    y = pd.Series([0, 0, 1, 1])
    model = RandomForestClassifier(n_estimators=5, random_state=0)
    model.fit(X, y)
    m = evaluate(model, X, y)
    assert "classes_present" in m
    assert m["classes_present"] == [0, 1]


def test_check_stops_invalid():
    b = PaperBroker(capital=1000, fee=0, slippage=0)
    b.open_position("long", 100, 1, 95, 110)
    b.check_stops(high=90, low=100)  # invalid (high<low)
    assert len(b.positions) == 1
    b.check_stops(high=111, low=94)
    assert len(b.positions) == 0
