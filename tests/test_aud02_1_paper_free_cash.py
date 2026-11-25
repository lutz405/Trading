"""Regressions for AUD-02.1: PaperBroker must authorize against free cash."""

from __future__ import annotations

import math

import pytest

from tradingai.paper.broker import PaperBroker


def approx(a: float, b: float, tol: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def _broker(capital: float = 1000.0, fee: float = 0.0, slippage: float = 0.0) -> PaperBroker:
    return PaperBroker(
        capital=capital,
        fee=fee,
        slippage=slippage,
        risk_budget_ratio=100.0,
        max_exposure_ratio=100.0,
    )


def _free(b: PaperBroker) -> float:
    return b.capital - b.collateral


def _snapshot(b: PaperBroker):
    return (
        b.capital,
        b.collateral,
        _free(b),
        list(b.positions),
        list(b.trades),
        b.realized_gross_pnl,
        b.realized_net_pnl,
        b.fees_paid,
        b.slippage_cost,
    )


@pytest.mark.parametrize(("fee", "slippage"), [(0.0, 0.0), (0.001, 0.0005)])
def test_two_shorts_individually_funded_but_jointly_unfunded_rejects_second(fee, slippage):
    b = _broker(fee=fee, slippage=slippage)
    assert b.open_position("short", 100.0, 6.0, 120.0, 80.0)
    assert _free(b) >= 0.0
    before = _snapshot(b)

    assert not b.open_position("short", 100.0, 6.0, 120.0, 80.0)
    assert _snapshot(b) == before


@pytest.mark.parametrize(("fee", "slippage"), [(0.0, 0.0), (0.001, 0.0005)])
def test_several_shorts_whose_collateral_fits_are_accepted(fee, slippage):
    b = _broker(fee=fee, slippage=slippage)
    for _ in range(3):
        assert b.open_position("short", 100.0, 3.0, 120.0, 80.0)

    assert len(b.positions) == 3
    expected_collateral = sum(p.qty * p.entry_price for p in b.positions)
    expected_fees = sum(p.entry_fee for p in b.positions)
    assert approx(b.collateral, expected_collateral)
    assert approx(b.collateral + expected_fees + b.free_cash, b.initial_capital)
    assert b.free_cash >= 0.0


@pytest.mark.parametrize(("fee", "slippage"), [(0.0, 0.0), (0.001, 0.0005)])
def test_long_after_short_cannot_use_reserved_collateral(fee, slippage):
    b = _broker(fee=fee, slippage=slippage)
    assert b.open_position("short", 100.0, 6.0, 120.0, 80.0)
    before = _snapshot(b)

    assert not b.open_position("long", 100.0, 5.0, 90.0, 110.0)
    assert _snapshot(b) == before

    assert b.open_position("long", 100.0, 3.9, 90.0, 110.0)
    assert b.free_cash >= 0.0
    assert approx(
        b.equity(100.0),
        b.capital
        + b.collateral
        + sum(p.qty * 100.0 for p in b.positions if p.side == "long")
        - sum(p.qty * 100.0 for p in b.positions if p.side == "short"),
    )


@pytest.mark.parametrize(("fee", "slippage"), [(0.0, 0.0), (0.001, 0.0005)])
def test_short_after_long_respects_remaining_cash(fee, slippage):
    b = _broker(fee=fee, slippage=slippage)
    assert b.open_position("long", 100.0, 6.0, 90.0, 110.0)
    before = _snapshot(b)

    assert not b.open_position("short", 100.0, 5.0, 120.0, 80.0)
    assert _snapshot(b) == before

    assert b.open_position("short", 100.0, 3.9, 120.0, 80.0)
    assert b.free_cash >= 0.0
    assert approx(
        b.equity(100.0),
        b.capital
        + b.collateral
        + sum(p.qty * 100.0 for p in b.positions if p.side == "long")
        - sum(p.qty * 100.0 for p in b.positions if p.side == "short"),
    )


def test_rejection_does_not_mutate_any_state_with_fees_and_slippage():
    b = _broker(fee=0.001, slippage=0.0005)
    assert b.open_position("short", 100.0, 4.0, 120.0, 80.0)
    before = _snapshot(b)

    assert not b.open_position("long", 100.0, 6.0, 90.0, 110.0)
    assert _snapshot(b) == before


@pytest.mark.parametrize(("fee", "slippage"), [(0.0, 0.0), (0.001, 0.0005)])
def test_closing_short_releases_collateral(fee, slippage):
    b = _broker(fee=fee, slippage=slippage)
    assert b.open_position("short", 100.0, 6.0, 120.0, 80.0)
    free_before = b.free_cash

    assert b.close_position(0, 100.0)
    assert b.collateral == 0.0
    assert approx(b.free_cash, b.capital)
    assert b.free_cash > free_before
    assert b.open_position("short", 100.0, 6.0, 120.0, 80.0)


def test_consecutive_opens_and_closes_keep_accounting_identities():
    b = _broker(fee=0.001, slippage=0.0005)
    initial = b.initial_capital

    assert b.open_position("short", 100.0, 4.0, 120.0, 80.0)
    assert b.open_position("long", 100.0, 2.0, 90.0, 110.0)
    assert b.free_cash >= 0.0

    mark = 105.0
    long_mv = sum(p.qty * mark for p in b.positions if p.side == "long")
    short_liability = sum(p.qty * mark for p in b.positions if p.side == "short")
    assert approx(b.equity(mark), b.capital + b.collateral + long_mv - short_liability)
    assert approx(
        b.collateral, sum(p.qty * p.entry_price for p in b.positions if p.side == "short")
    )

    assert b.close_position(1, mark)
    assert b.free_cash >= 0.0
    remaining_short_liability = sum(p.qty * mark for p in b.positions if p.side == "short")
    assert approx(b.equity(mark), b.capital + b.collateral - remaining_short_liability)

    assert b.close_position(0, 95.0)
    assert b.positions == []
    assert approx(b.capital, initial + b.realized_net_pnl)
    assert approx(b.free_cash, b.capital)
    assert approx(b.equity(95.0), b.capital)


def test_persistence_preserves_collateral_and_free_cash(tmp_path):
    b = _broker(fee=0.001, slippage=0.0005)
    assert b.open_position("short", 100.0, 4.0, 120.0, 80.0)
    assert b.open_position("long", 100.0, 2.0, 90.0, 110.0)

    path = tmp_path / "state.json"
    b.save(path)
    restored = PaperBroker.load(path)

    assert approx(restored.capital, b.capital)
    assert approx(restored.collateral, b.collateral)
    assert approx(restored.free_cash, b.free_cash)
    assert restored.positions == b.positions
    assert approx(restored.equity(105.0), b.equity(105.0))

    assert restored.close_position(0, 95.0)
    assert restored.close_position(0, 105.0)
    assert restored.positions == []
    assert approx(restored.capital, restored.initial_capital + restored.realized_net_pnl)
    assert approx(restored.free_cash, restored.capital)


def test_exact_free_cash_boundary_with_fee_rejects_any_further_side():
    b = _broker(fee=0.001, slippage=0.0)
    assert b.open_position("short", 100.0, 9.99, 120.0, 80.0)
    entry_fee = b.positions[0].entry_fee

    assert approx(b.collateral + entry_fee + b.free_cash, b.initial_capital)
    assert b.free_cash >= 0.0
    before = _snapshot(b)

    assert not b.open_position("short", 100.0, 0.0001, 120.0, 80.0)
    assert _snapshot(b) == before
    assert not b.open_position("long", 100.0, 0.0001, 90.0, 110.0)
    assert _snapshot(b) == before


def test_free_cash_property_distinguishes_total_cash_and_reserved_collateral():
    b = _broker()
    assert approx(b.free_cash, 1000.0)

    assert b.open_position("long", 100.0, 2.0, 90.0, 110.0)
    assert approx(b.free_cash, b.capital)
    assert approx(b.free_cash, 800.0)

    assert b.open_position("short", 100.0, 3.0, 120.0, 80.0)
    assert approx(b.capital, 800.0)
    assert approx(b.collateral, 300.0)
    assert approx(b.free_cash, 500.0)
