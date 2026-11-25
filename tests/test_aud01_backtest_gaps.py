"""Regressions for AUD-01: gaps must not exit at already-crossed levels."""

import pandas as pd
import pytest

from tradingai.backtesting.engine import BacktestEngine


def _frame(rows):
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=len(rows), freq="h", tz="UTC"),
            "open": [r[0] for r in rows],
            "high": [r[1] for r in rows],
            "low": [r[2] for r in rows],
            "close": [r[3] for r in rows],
        }
    )


def _run(side, rows):
    def decision(i, row, engine):
        return f"{side}_SIMULATED" if i == 0 else "HOLD"

    engine = BacktestEngine(capital=1000.0, fee=0.001, slippage=0.0)
    engine.run(_frame(rows), decision)
    return engine


def _assert_gap_exit(engine, entry, exit_price, reason):
    trade = engine.trades[0]
    assert trade.entry_price == pytest.approx(entry)
    assert trade.exit_price == pytest.approx(exit_price)
    assert trade.reason == reason
    assert trade.gross_pnl == pytest.approx(0.0)
    assert trade.pnl == pytest.approx(-trade.fees)
    assert engine.capital == pytest.approx(engine.initial_capital + engine.realized_net_pnl)
    assert engine.equity[-1] == pytest.approx(engine.capital)


def test_long_gap_down_through_stop_exits_at_open():
    engine = _run("LONG", [(100.0, 101.0, 99.0, 100.0), (90.0, 95.0, 85.0, 90.0)])
    _assert_gap_exit(engine, entry=90.0, exit_price=90.0, reason="stop")


def test_long_gap_up_through_take_exits_at_open():
    engine = _run("LONG", [(100.0, 101.0, 99.0, 100.0), (120.0, 125.0, 115.0, 120.0)])
    _assert_gap_exit(engine, entry=120.0, exit_price=120.0, reason="take")


def test_short_gap_up_through_stop_exits_at_open():
    engine = _run("SHORT", [(100.0, 101.0, 99.0, 100.0), (110.0, 115.0, 105.0, 110.0)])
    _assert_gap_exit(engine, entry=110.0, exit_price=110.0, reason="stop")


def test_short_gap_down_through_take_exits_at_open():
    engine = _run("SHORT", [(100.0, 101.0, 99.0, 100.0), (90.0, 95.0, 85.0, 90.0)])
    _assert_gap_exit(engine, entry=90.0, exit_price=90.0, reason="take")


def test_existing_long_position_gap_down_exits_at_open():
    engine = _run(
        "LONG",
        [
            (100.0, 101.0, 99.0, 100.0),
            (100.0, 100.5, 99.5, 100.0),
            (90.0, 95.0, 85.0, 90.0),
        ],
    )
    trade = engine.trades[0]
    assert trade.entry_price == pytest.approx(100.0)
    assert trade.exit_price == pytest.approx(90.0)
    assert trade.reason == "stop"
    assert trade.pnl < 0


def test_existing_short_position_gap_up_exits_at_open():
    engine = _run(
        "SHORT",
        [
            (100.0, 101.0, 99.0, 100.0),
            (100.0, 100.5, 99.5, 100.0),
            (110.0, 115.0, 105.0, 110.0),
        ],
    )
    trade = engine.trades[0]
    assert trade.entry_price == pytest.approx(100.0)
    assert trade.exit_price == pytest.approx(110.0)
    assert trade.reason == "stop"
    assert trade.pnl < 0


def test_long_intrabar_both_levels_still_prefers_stop():
    engine = _run(
        "LONG",
        [
            (100.0, 101.0, 99.0, 100.0),
            (100.0, 100.5, 99.5, 100.0),
            (100.0, 105.0, 95.0, 100.0),
        ],
    )
    trade = engine.trades[0]
    assert trade.exit_price == pytest.approx(99.0)
    assert trade.reason == "stop"


def test_short_intrabar_both_levels_still_prefers_stop():
    engine = _run(
        "SHORT",
        [
            (100.0, 101.0, 99.0, 100.0),
            (100.0, 100.5, 99.5, 100.0),
            (100.0, 105.0, 95.0, 100.0),
        ],
    )
    trade = engine.trades[0]
    assert trade.exit_price == pytest.approx(101.0)
    assert trade.reason == "stop"
