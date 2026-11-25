from __future__ import annotations

import json
import math
import os
import tempfile

import pytest

from tradingai.backtesting.engine import BacktestEngine
from tradingai.paper.broker import PaperBroker


def approx(a: float, b: float, tol: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def test_backtest_long_open_and_close_accounting():
    e = BacktestEngine(capital=1000.0, fee=0.0, slippage=0.0)
    e._enter(0, 100.0, "long", 2.0, 90.0, 110.0)
    assert e.capital == 800.0
    assert e.collateral == 0.0
    assert approx(e.mark_equity(100.0), 1000.0)
    e._exit(1, 110.0, "end")
    assert approx(e.capital, 1020.0)
    assert approx(e.realized_gross_pnl, 20.0)
    assert approx(e.realized_net_pnl, 20.0)
    assert approx(e.trades[0].gross_pnl, 20.0)
    assert approx(e.trades[0].pnl, 20.0)


def test_backtest_short_open_and_close_profit_and_loss():
    e = BacktestEngine(capital=1000.0, fee=0.0, slippage=0.0)
    e._enter(0, 100.0, "short", 2.0, 110.0, 90.0)
    assert e.capital == 1000.0
    assert e.collateral == 200.0
    assert approx(e.mark_equity(100.0), 1000.0)
    assert approx(e.mark_equity(90.0), 1020.0)
    e._exit(1, 90.0, "end")
    assert approx(e.capital, 1020.0)
    assert approx(e.realized_gross_pnl, 20.0)

    e2 = BacktestEngine(capital=1000.0, fee=0.0, slippage=0.0)
    e2._enter(0, 100.0, "short", 2.0, 90.0, 110.0)
    assert approx(e2.mark_equity(110.0), 980.0)
    e2._exit(1, 110.0, "end")
    assert approx(e2.capital, 980.0)
    assert approx(e2.trades[0].pnl, -20.0)


def test_backtest_final_liquidation_updates_last_equity(tmp_path=None):
    e = BacktestEngine(capital=1000.0, fee=0.001, slippage=0.0005)
    rows = []
    for i, px in enumerate([100.0, 101.0, 102.0]):
        rows.append((f"2026-01-01 {i:02d}:00", px))

    import pandas as pd

    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime([r[0] for r in rows], utc=True),
            "open": [r[1] for r in rows],
            "high": [r[1] + 0.01 for r in rows],
            "low": [r[1] - 0.01 for r in rows],
            "close": [r[1] for r in rows],
        }
    )
    e.run(df, lambda i, r, eng: "LONG_SIMULATED" if i == 0 else "HOLD")
    assert len(e.trades) == 1
    assert e.position is None
    assert approx(e.equity[-1], e.capital)
    assert e.trades[0].reason in ("end", "take")


def test_paper_long_accounting():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("long", 100.0, 2.0, 90.0, 110.0)
    assert approx(b.capital, 800.0)
    assert approx(b.collateral, 0.0)
    assert approx(b.equity(100.0), 1000.0)
    assert b.close_position(0, 110.0)
    assert approx(b.capital, 1020.0)
    assert approx(b.realized_gross_pnl, 20.0)
    assert approx(b.realized_net_pnl, 20.0)


def test_paper_short_accounting_and_collateral():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("short", 100.0, 2.0, 110.0, 90.0)
    assert approx(b.capital, 1000.0)
    assert approx(b.collateral, 200.0)
    assert approx(b.equity(100.0), 1000.0)
    assert approx(b.equity(90.0), 1020.0)
    assert b.close_position(0, 90.0)
    assert approx(b.capital, 1020.0)
    assert approx(b.collateral, 0.0)
    assert approx(b.realized_gross_pnl, 20.0)


def test_paper_multiple_short_positions_without_limit():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("short", 100.0, 1.0, 110.0, 90.0)
    assert b.open_position("short", 100.0, 1.0, 110.0, 90.0)
    assert len(b.positions) == 2
    assert approx(b.collateral, 200.0)
    assert b.close_position(0, 90.0)
    assert len(b.positions) == 1


def test_paper_identities_open_and_closed():
    b = PaperBroker(capital=1000.0, fee=0.001, slippage=0.0005)
    b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    mark = 102.0
    equity = b.equity(mark)
    long_mv = sum(p.qty * mark for p in b.positions if p.side == "long")
    assert approx(equity, b.capital + b.collateral + long_mv - sum(p.qty * mark for p in b.positions if p.side == "short"))
    assert approx(b.realized_gross_pnl, 0.0)
    assert approx(b.realized_net_pnl, 0.0)
    b.close_position(0, 110.0)
    assert approx(b.realized_gross_pnl, sum(t["gross_pnl"] for t in b.trades))
    assert approx(b.realized_net_pnl, sum(t["pnl"] for t in b.trades))


def test_paper_fees_and_slippage_registration():
    b = PaperBroker(capital=10000.0, fee=0.001, slippage=0.001)
    b.open_position("long", 100.0, 2.0, 90.0, 110.0)
    b.close_position(0, 110.0)
    t = b.trades[0]
    assert approx(t["entry_fee"], 2 * 100.1 * 0.001)
    assert approx(t["exit_fee"], 2 * 109.89 * 0.001)
    assert approx(t["fees"], t["entry_fee"] + t["exit_fee"])
    assert t["slippage"] > 0
    assert approx(b.realized_net_pnl, sum(t["pnl"] for t in b.trades))
    assert approx(b.fees_paid, sum(t["fees"] for t in b.trades))


def test_paper_persistence_v2_roundtrip():
    b = PaperBroker(capital=500.0, fee=0.001, slippage=0.0005)
    b.open_position("long", 50.0, 1.0, 45.0, 55.0)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "state.json")
        b.save(p)
        b2 = PaperBroker.load(p)
        assert approx(b2.capital, b.capital)
        assert approx(b2.initial_capital, b.initial_capital)
        assert approx(b2.realized_gross_pnl, b.realized_gross_pnl)
        assert approx(b2.fees_paid, b.fees_paid)
        assert approx(b2.slippage_cost, b.slippage_cost)
        assert approx(b2.realized_net_pnl, b.realized_net_pnl)
        assert len(b2.positions) == 1
        assert len(b2.trades) == 0


def test_paper_persistence_rejects_invalid_state():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "bad.json")
        PaperBroker().save(p)
        with open(p) as f:
            obj = json.load(f)
        obj["schema_version"] = 1
        with open(p, "w") as f:
            json.dump(obj, f)
        with open(p) as f:
            before = f.read()
        with pytest.raises((TypeError, ValueError)):
            PaperBroker.load(p)
        with open(p) as f:
            after = f.read()
        assert before == after


def test_paper_negative_capital_persistence_roundtrip():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("short", 100.0, 2.0, 110.0, 90.0)
    assert b.close_position(0, 650.0)
    assert b.capital < 0
    assert approx(b.realized_gross_pnl, -1100.0)
    assert approx(b.realized_net_pnl, -1100.0)
    assert approx(b.realized_equity, b.capital)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "state.json")
        b.save(p)
        b2 = PaperBroker.load(p)
        assert approx(b2.capital, b.capital)
        assert approx(b2.realized_gross_pnl, b.realized_gross_pnl)
        assert approx(b2.realized_net_pnl, b.realized_net_pnl)
        assert b2.positions == []


@pytest.mark.parametrize("price", [float("nan"), float("inf"), float("-inf"), 0.0, -100.0])
def test_paper_close_position_rejects_invalid_price(price):
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    pos_before = list(b.positions)
    state_before = (b.capital, b.realized_gross_pnl, b.realized_net_pnl, b.trades)
    with pytest.raises(ValueError):
        b.close_position(0, price)
    assert b.positions == pos_before
    assert (b.capital, b.realized_gross_pnl, b.realized_net_pnl, b.trades) == state_before


@pytest.mark.parametrize("slip", [float("nan"), float("inf"), float("-inf"), -0.1, -1.0])
def test_paper_close_position_rejects_invalid_entry_slippage(slip):
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    b.positions[0].entry_slippage = slip
    pos_before = list(b.positions)
    state_before = (b.capital, b.realized_gross_pnl, b.realized_net_pnl, b.trades)
    with pytest.raises(ValueError):
        b.close_position(0, 110.0)
    assert b.positions == pos_before
    assert (b.capital, b.realized_gross_pnl, b.realized_net_pnl, b.trades) == state_before


@pytest.mark.parametrize("field", ["fee", "slippage"])
@pytest.mark.parametrize("invalid", [-0.1, float("nan"), float("inf"), float("-inf")])
def test_paper_open_position_rejects_invalid_fee_or_slippage(field, invalid):
    b = PaperBroker(capital=1000.0, fee=0.001, slippage=0.001)
    setattr(b, field, invalid)
    state_before = (b.capital, b.positions, b.trades, b.realized_gross_pnl, b.realized_net_pnl, b.fees_paid, b.slippage_cost)
    with pytest.raises(ValueError):
        b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    assert (b.capital, b.positions, b.trades, b.realized_gross_pnl, b.realized_net_pnl, b.fees_paid, b.slippage_cost) == state_before


@pytest.mark.parametrize("side", ["long", "short"])
@pytest.mark.parametrize("field", ["fee", "slippage"])
@pytest.mark.parametrize("invalid", [-0.1, float("nan"), float("inf"), float("-inf")])
def test_paper_close_position_rejects_invalid_fee_or_slippage(side, field, invalid):
    b = PaperBroker(capital=1000.0, fee=0.001, slippage=0.001)
    if side == "long":
        assert b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    else:
        assert b.open_position("short", 100.0, 1.0, 110.0, 90.0)
    setattr(b, field, invalid)
    state_before = (b.capital, b.positions, b.trades, b.realized_gross_pnl, b.realized_net_pnl, b.fees_paid, b.slippage_cost)
    with pytest.raises(ValueError):
        b.close_position(0, 110.0 if side == "long" else 90.0)
    assert (b.capital, b.positions, b.trades, b.realized_gross_pnl, b.realized_net_pnl, b.fees_paid, b.slippage_cost) == state_before


def test_paper_close_position_rejects_invalid_index():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    state_before = (b.capital, b.realized_gross_pnl, b.realized_net_pnl, b.trades)
    assert not b.close_position(99, 100.0)
    assert not b.close_position(-1, 100.0)
    assert (b.capital, b.realized_gross_pnl, b.realized_net_pnl, b.trades) == state_before


@pytest.mark.parametrize(
    "field,value",
    [
        ("fee", -0.1),
        ("fee", float("nan")),
        ("fee", float("inf")),
        ("fee", float("-inf")),
        ("slippage", -0.1),
        ("slippage", float("nan")),
        ("slippage", float("inf")),
        ("slippage", float("-inf")),
    ],
)
def test_paper_save_rejects_invalid_fee_or_slippage(field, value):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "bad.json")
        b = PaperBroker()
        setattr(b, field, value)
        with pytest.raises(ValueError):
            b.save(p)
        assert not os.path.exists(p)


def test_paper_save_load_valid_state():
    b = PaperBroker(capital=500.0, fee=0.001, slippage=0.0005)
    b.open_position("long", 100.0, 2.0, 90.0, 110.0)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "state.json")
        b.save(p)
        b2 = PaperBroker.load(p)
        assert approx(b2.capital, b.capital)
        assert approx(b2.fee, b.fee)
        assert approx(b2.slippage, b.slippage)


def test_paper_save_validates_complete_state():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    b.open_position("short", 100.0, 2.0, 110.0, 90.0)
    b.close_position(0, 90.0)
    with tempfile.TemporaryDirectory() as d:
        bad = os.path.join(d, "bad.json")
        b.realized_gross_pnl += 1.0
        with pytest.raises(ValueError):
            b.save(bad)
        assert not os.path.exists(bad)
        b.realized_gross_pnl -= 1.0
        b.capital = 9999.0
        with pytest.raises(ValueError):
            b.save(bad)
        assert not os.path.exists(bad)
        b.capital = b.realized_equity


def test_paper_short_extreme_negative_cash_allowed():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("short", 100.0, 2.0, 110.0, 90.0)
    assert b.close_position(0, 650.0)
    assert b.capital < 0
    assert b.positions == []
    assert approx(b.realized_gross_pnl, -1100.0)
