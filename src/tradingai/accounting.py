from __future__ import annotations

import math
from typing import Literal

Side = Literal["long", "short"]


def validate_number(value: object, name: str, *, positive: bool = False, nonnegative: bool = False) -> float:
    try:
        v = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    if positive and v <= 0:
        raise ValueError(f"{name} must be positive")
    if nonnegative and v < 0:
        raise ValueError(f"{name} must be nonnegative")
    return v


def validate_side(side: str) -> str:
    if side not in ("long", "short"):
        raise ValueError("side must be 'long' or 'short'")
    return side


def execution_price(reference: float, side: str, slippage: float, opening: bool) -> float:
    reference = validate_number(reference, "reference_price", positive=True)
    slippage = validate_number(slippage, "slippage", nonnegative=True)
    slip = reference * slippage
    if side == "long":
        return reference + slip if opening else reference - slip
    if side == "short":
        return reference - slip if opening else reference + slip
    raise ValueError("side must be 'long' or 'short'")


def slippage_cost_amount(qty: float, reference_price: float, slippage: float) -> float:
    qty = validate_number(qty, "qty", positive=True)
    reference_price = validate_number(reference_price, "reference_price", positive=True)
    slippage = validate_number(slippage, "slippage", nonnegative=True)
    return qty * reference_price * slippage


def entry_notional(qty: float, price: float) -> float:
    qty = validate_number(qty, "qty", positive=True)
    price = validate_number(price, "price", positive=True)
    return qty * price


def entry_fee_amount(qty: float, price: float, fee_rate: float) -> float:
    return entry_notional(qty, price) * validate_number(fee_rate, "fee", nonnegative=True)


def exit_notional(qty: float, price: float) -> float:
    return entry_notional(qty, price)


def exit_fee_amount(qty: float, price: float, fee_rate: float) -> float:
    return exit_notional(qty, price) * validate_number(fee_rate, "fee", nonnegative=True)


def gross_pnl(side: str, qty: float, entry: float, exit: float) -> float:
    side = validate_side(side)
    qty = validate_number(qty, "qty", positive=True)
    entry = validate_number(entry, "entry_price", positive=True)
    exit_ = validate_number(exit, "exit_price", positive=True)
    return qty * (exit_ - entry) if side == "long" else qty * (entry - exit_)


def unrealized_pnl(side: str, qty: float, entry: float, mark: float) -> float:
    side = validate_side(side)
    qty = validate_number(qty, "qty", positive=True)
    entry = validate_number(entry, "entry_price", positive=True)
    mark = validate_number(mark, "mark_price", positive=True)
    return qty * (mark - entry) if side == "long" else qty * (entry - mark)


def account_equity(cash: float, collateral: float, long_market_value: float, short_liability: float) -> float:
    return validate_number(cash, "cash") + validate_number(collateral, "collateral", nonnegative=True) + validate_number(
        long_market_value, "long_market_value"
    ) - validate_number(short_liability, "short_liability", nonnegative=True)
