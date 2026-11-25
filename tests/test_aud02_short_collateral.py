"""Regressions for AUD-02: shorts require full cash collateral plus fees."""

import math

import pytest

from tradingai.backtesting.engine import BacktestEngine
from tradingai.paper.broker import PaperBroker
from tradingai.risk.sizing import SizingInput, calculate_cash_short, calculate_position_size


def _approx(a, b, tol=1e-9):
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def test_cash_short_requires_collateral_and_fee():
    qty = calculate_cash_short(1000.0, 100.0, 0.001)
    assert qty == pytest.approx(1000.0 / (100.0 * 1.001))
    assert qty * 100.0 * 1.001 <= 1000.0


def test_cash_short_zero_fee_is_finite_collateral():
    qty = calculate_cash_short(1000.0, 100.0, 0.0)
    assert math.isfinite(qty)
    assert qty == pytest.approx(10.0)


@pytest.mark.parametrize("cash", [0.0, -1.0])
def test_cash_short_nonpositive_cash_returns_zero(cash):
    assert calculate_cash_short(cash, 100.0, 0.001) == 0.0


def test_sizing_short_capped_by_cash_collateral():
    inp = SizingInput(
        side="short",
        price=100.0,
        equity=1000.0,
        cash=1000.0,
        risk_budget_ratio=10.0,
        max_exposure_ratio=2.0,
        fee_rate=0.001,
        slippage=0.0,
        stop=120.0,
    )
    res = calculate_position_size(inp)
    assert res.ok
    assert res.qty == pytest.approx(9.99)
    assert res.qty <= res.q_cash + 1e-12
    assert res.qty * res.entry_exec * (1.0 + inp.fee_rate) <= inp.cash + 1e-9


def test_paper_broker_rejects_unfunded_short():
    broker = PaperBroker(
        capital=1000.0,
        fee=0.001,
        slippage=0.0,
        risk_budget_ratio=10.0,
        max_exposure_ratio=2.0,
    )
    before = (broker.capital, list(broker.positions), list(broker.trades), broker.collateral)
    assert not broker.open_position("short", 100.0, 20.0, 120.0, 80.0)
    assert (broker.capital, broker.positions, broker.trades, broker.collateral) == before


def test_paper_broker_exact_collateral_boundary_without_fee():
    broker = PaperBroker(
        capital=1000.0,
        fee=0.0,
        slippage=0.0,
        risk_budget_ratio=10.0,
        max_exposure_ratio=2.0,
    )
    assert broker.open_position("short", 100.0, 10.0, 120.0, 80.0)
    assert broker.collateral == pytest.approx(1000.0)
    assert broker.capital == pytest.approx(1000.0)
    assert broker.equity(100.0) == pytest.approx(1000.0)

    other = PaperBroker(
        capital=1000.0,
        fee=0.0,
        slippage=0.0,
        risk_budget_ratio=10.0,
        max_exposure_ratio=2.0,
    )
    assert not other.open_position("short", 100.0, 10.01, 120.0, 80.0)
    assert other.positions == []


def test_paper_broker_covered_short_keeps_identities():
    broker = PaperBroker(
        capital=1000.0,
        fee=0.001,
        slippage=0.0,
        risk_budget_ratio=10.0,
        max_exposure_ratio=2.0,
    )
    assert not broker.open_position("short", 100.0, 10.0, 120.0, 80.0)
    assert broker.positions == []

    assert broker.open_position("short", 100.0, 9.99, 120.0, 80.0)
    assert broker.collateral == pytest.approx(999.0)
    assert broker.capital == pytest.approx(999.001)
    assert broker.equity(100.0) == pytest.approx(999.001)

    assert broker.close_position(0, 90.0)
    trade = broker.trades[0]
    assert broker.capital == pytest.approx(1000.0 + trade["pnl"])
    assert broker.realized_net_pnl == pytest.approx(sum(t["pnl"] for t in broker.trades))
    assert broker.collateral == 0.0


def test_backtest_rejects_unfunded_short():
    engine = BacktestEngine(capital=1000.0, fee=0.001, slippage=0.0)
    engine._enter(0, 100.0, "short", 20.0, 120.0, 80.0)
    assert engine.position is None
    assert engine.capital == pytest.approx(1000.0)
    assert engine.collateral == 0.0


def test_backtest_covered_short_keeps_identities():
    engine = BacktestEngine(capital=1000.0, fee=0.001, slippage=0.0)
    engine._enter(0, 100.0, "short", 9.99, 120.0, 80.0)
    assert engine.position is not None
    assert engine.collateral == pytest.approx(999.0)
    assert engine.capital == pytest.approx(999.001)
    assert engine.mark_equity(100.0) == pytest.approx(999.001)

    engine._exit(1, 90.0, "end")
    trade = engine.trades[0]
    assert engine.capital == pytest.approx(engine.initial_capital + engine.realized_net_pnl)
    assert engine.realized_net_pnl == pytest.approx(trade.pnl)
    assert engine.collateral == 0.0
    assert engine.trades[0].gross_pnl == pytest.approx(9.99 * 10.0)


def test_backtest_exact_collateral_boundary_without_fee():
    engine = BacktestEngine(capital=1000.0, fee=0.0, slippage=0.0)
    engine._enter(0, 100.0, "short", 10.0, 120.0, 80.0)
    assert engine.position is not None
    assert engine.collateral == pytest.approx(1000.0)

    other = BacktestEngine(capital=1000.0, fee=0.0, slippage=0.0)
    other._enter(0, 100.0, "short", 10.0001, 120.0, 80.0)
    assert other.position is None
    assert other.collateral == 0.0
