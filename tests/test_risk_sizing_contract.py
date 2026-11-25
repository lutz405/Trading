from __future__ import annotations

import math

import pytest

from tradingai.backtesting.engine import BacktestEngine
from tradingai.paper.broker import PaperBroker
from tradingai.risk.sizing import (
    DEFAULT_Q_MIN,
    DEFAULT_QUANTITY_STEP,
    SizingInput,
    calculate_cash_short,
    calculate_position_size,
    calculate_risk_incremental,
    floor_to_step,
)


def approx(a, b, tol=1e-9):
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def base_input(side="long", stop=90.0, equity=10000.0, cash=8000.0, price=100.0, fee_rate=0.001, slippage=0.001, risk_budget=0.01, max_exposure=0.5, open_gross_notional=0.0, risk_open=0.0, **overrides):
    kwargs = {
        "side": side,
        "price": price,
        "equity": equity,
        "cash": cash,
        "risk_budget_ratio": risk_budget,
        "max_exposure_ratio": max_exposure,
        "fee_rate": fee_rate,
        "slippage": slippage,
        "stop": stop,
        "open_gross_notional": open_gross_notional,
        "risk_open": risk_open,
        "quantity_step": DEFAULT_QUANTITY_STEP,
        "q_min": DEFAULT_Q_MIN,
    }
    kwargs.update(overrides)
    return SizingInput(**kwargs)


def test_long_sizing_math():
    inp = base_input(side="long", equity=10000.0, cash=8000.0, price=100.0, stop=90.0)
    res = calculate_position_size(inp)
    assert res.ok
    assert res.entry_exec == pytest.approx(100.1)
    assert res.stop_exec == pytest.approx(89.91)
    assert res.risk_incremental >= 0
    assert res.gross_new <= 10000.0 * 0.5 + 1e-9
    assert res.qty >= inp.q_min


def test_short_sizing_cash_rule():
    inp = base_input(side="short", equity=10000.0, cash=100.0, price=100.0, stop=120.0, fee_rate=0.001)
    res = calculate_position_size(inp)
    assert res.ok
    expected = calculate_cash_short(100.0, 99.9, 0.001)
    assert approx(res.q_cash, expected)
    assert expected > 0


def test_stop_hit_fails_closed():
    # long stop 105, entry ~100.1 -> stop_exec ~104.505; mark entry is hit.
    inp = base_input(side="long", price=100.0, stop=105.0, equity=10000.0, cash=8000.0)
    res = calculate_position_size(inp)
    assert not res.ok
    assert res.qty == 0.0


def test_no_stop_conservative_risk():
    qty = 1.5
    r = calculate_risk_incremental("short", qty, 100.1, 120.12, 0.001)
    assert approx(r, qty * (120.12 - 100.1 + 0.001 * 120.12))


def test_floor_to_step_and_q_min():
    assert floor_to_step(0.05, 0.1) == 0.0
    assert floor_to_step(0.5, 0.1) == pytest.approx(0.5)
    inp = base_input(q_min=0.2, quantity_step=0.1)
    inp.cash = 0.01
    res = calculate_position_size(inp)
    assert not res.ok


def test_invalid_inputs_rejected():
    for kwargs in ({"equity": 0.0}, {"price": 0.0}, {"quantity_step": 0.0}):
        with pytest.raises(ValueError):
            calculate_position_size(base_input(**kwargs))


def test_paper_broker_uses_sizing():
    b = PaperBroker(capital=8000.0, fee=0.001, slippage=0.001, risk_budget_ratio=0.01, max_exposure_ratio=0.5)
    assert b.open_position("long", 100.0, None, 90.0, 110.0)
    assert len(b.positions) == 1
    assert b.positions[0].qty > 0
    assert b.positions[0].qty >= b.q_min - 1e-12
    assert b.equity(100.0) > 0


def test_backtest_engine_uses_sizing():
    e = BacktestEngine(capital=8000.0, fee=0.001, slippage=0.001)
    import pandas as pd
    df = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-01-01 00:00", "2026-01-01 01:00"], utc=True),
        "open": [100.0, 100.0],
        "high": [101.4, 101.3],
        "low": [100.8, 100.7],
        "close": [100.0, 100.0],
    })
    e.run(df, lambda i, row, eng: "LONG_SIMULATED" if i == 0 else "HOLD")
    assert e.trades or e.position is not None
    if e.trades:
        assert e.trades[0].qty > 0


def _broker_state(b):
    return (b.capital, b.positions, b.trades, b.realized_gross_pnl, b.realized_net_pnl, b.fees_paid, b.slippage_cost)


def test_paper_broker_rejects_when_sizing_not_ok_even_with_qty():
    b = PaperBroker(capital=0.0, fee=0.001, slippage=0.0)
    before = _broker_state(b)
    assert not b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    assert _broker_state(b) == before


def test_paper_broker_rejects_when_stop_hit_even_with_qty():
    b = PaperBroker(capital=10000.0, fee=0.0, slippage=0.0)
    before = _broker_state(b)
    assert not b.open_position("long", 100.0, 1.0, 105.0, 110.0)
    assert _broker_state(b) == before


def test_paper_broker_accepts_explicit_qty_below_max():
    b = PaperBroker(capital=10000.0, fee=0.0, slippage=0.0)
    assert b.open_position("long", 100.0, 0.1, 90.0, 110.0)
    assert len(b.positions) == 1
    assert b.positions[0].qty > 0


def test_paper_broker_rejects_explicit_qty_above_max():
    b = PaperBroker(capital=10000.0, fee=0.0, slippage=0.0)
    assert not b.open_position("long", 100.0, 1000.0, 90.0, 110.0)


def test_paper_broker_rejections_do_not_mutate_state():
    b = PaperBroker(capital=10000.0, fee=0.001, slippage=0.001)
    before = _broker_state(b)
    assert not b.open_position("short", 100.0, 1.0, 90.0, 110.0)  # short invalid: stop < entry
    assert _broker_state(b) == before


def test_paper_broker_short_uses_sizing_constraints():
    b = PaperBroker(capital=1000.0, fee=0.0, slippage=0.0)
    assert b.open_position("short", 100.0, None, 120.0, 80.0)
    assert len(b.positions) == 1
    assert b.positions[0].side == "short"
    assert b.collateral > 0
    assert b.equity(100.0) > 0

