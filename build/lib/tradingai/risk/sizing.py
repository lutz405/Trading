from __future__ import annotations

import math
from dataclasses import dataclass

from tradingai.accounting import (
    execution_price,
    validate_number,
    validate_side,
)

DEFAULT_Q_MIN = 0.00001
DEFAULT_QUANTITY_STEP = 0.0001


@dataclass
class SizingInput:
    side: str
    price: float
    equity: float
    cash: float
    risk_budget_ratio: float
    max_exposure_ratio: float
    fee_rate: float = 0.001
    slippage: float = 0.0005
    stop: float | None = None
    open_gross_notional: float = 0.0
    risk_open: float = 0.0
    quantity_step: float = DEFAULT_QUANTITY_STEP
    q_min: float = DEFAULT_Q_MIN


@dataclass
class SizingResult:
    qty: float
    ok: bool
    reason: str
    entry_exec: float
    stop_exec: float | None
    q_cash: float
    q_risk: float
    q_exposure: float
    risk_open: float
    risk_incremental: float
    gross_open: float
    gross_new: float


def _validate_input(inp: SizingInput) -> None:
    validate_side(inp.side)
    validate_number(inp.price, "price", positive=True)
    validate_number(inp.equity, "equity", positive=True)
    validate_number(inp.cash, "cash")
    validate_number(inp.risk_budget_ratio, "risk_budget_ratio", positive=True)
    validate_number(inp.max_exposure_ratio, "max_exposure_ratio", positive=True)
    validate_number(inp.fee_rate, "fee_rate", nonnegative=True)
    validate_number(inp.slippage, "slippage", nonnegative=True)
    validate_number(inp.open_gross_notional, "open_gross_notional", nonnegative=True)
    validate_number(inp.risk_open, "risk_open", nonnegative=True)
    validate_number(inp.quantity_step, "quantity_step", positive=True)
    validate_number(inp.q_min, "q_min", positive=True)
    if inp.stop is not None:
        validate_number(inp.stop, "stop", positive=True)


def stop_exec(side: str, stop_ref: float, slippage: float) -> float:
    side = validate_side(side)
    stop_ref = validate_number(stop_ref, "stop", positive=True)
    slippage = validate_number(slippage, "slippage", nonnegative=True)
    if side == "long":
        return stop_ref * (1 - slippage)
    return stop_ref * (1 + slippage)


def stop_hit(side: str, mark: float, stop_ref: float) -> bool:
    side = validate_side(side)
    mark = validate_number(mark, "mark", positive=True)
    stop_ref = validate_number(stop_ref, "stop", positive=True)
    return mark <= stop_ref if side == "long" else mark >= stop_ref


def calculate_risk_incremental(side: str, qty: float, entry_exec: float, stop_exec_: float, fee_rate: float) -> float:
    side = validate_side(side)
    qty = validate_number(qty, "qty", nonnegative=True)
    entry_exec = validate_number(entry_exec, "entry_exec", positive=True)
    stop_exec_ = validate_number(stop_exec_, "stop_exec", positive=True)
    fee_rate = validate_number(fee_rate, "fee_rate", nonnegative=True)
    adverse = max(0.0, entry_exec - stop_exec_) if side == "long" else max(0.0, stop_exec_ - entry_exec)
    return qty * (adverse + fee_rate * stop_exec_)


def calculate_cash_long(cash: float, entry_exec: float, fee_rate: float) -> float:
    cash = validate_number(cash, "cash")
    entry_exec = validate_number(entry_exec, "entry_exec", positive=True)
    fee_rate = validate_number(fee_rate, "fee_rate", nonnegative=True)
    if cash <= 0:
        return 0.0
    return cash / (entry_exec * (1 + fee_rate))


def calculate_cash_short(cash: float, entry_exec: float, fee_rate: float) -> float:
    """Maximum short quantity backed by cash collateral plus the entry fee.

    The documented contract is ``free_cash >= q * P + fee``. With
    ``fee = q * entry_exec * fee_rate`` this is ``q <= cash / (P * (1 + fee))``.
    A short is never funded by the fee alone.
    """
    cash = validate_number(cash, "cash")
    entry_exec = validate_number(entry_exec, "entry_exec", positive=True)
    fee_rate = validate_number(fee_rate, "fee_rate", nonnegative=True)
    if cash <= 0:
        return 0.0
    return cash / (entry_exec * (1.0 + fee_rate))


def floor_to_step(qty: float, step: float) -> float:
    qty = validate_number(qty, "qty", nonnegative=True)
    step = validate_number(step, "quantity_step", positive=True)
    return math.floor(qty / step) * step


def calculate_position_size(inp: SizingInput) -> SizingResult:
    _validate_input(inp)
    entry_exec = execution_price(inp.price, inp.side, inp.slippage, opening=True)
    stop_ref = inp.stop if inp.stop is not None else entry_exec
    stop_ = stop_exec(inp.side, stop_ref, inp.slippage)
    if stop_hit(inp.side, entry_exec, stop_ref):
        risk_open = 0.0
        q_risk = 0.0
        return SizingResult(0.0, False, "stop_hit", entry_exec, stop_, 0.0, 0.0, 0.0, risk_open, 0.0, inp.open_gross_notional, 0.0)
    q_cash = calculate_cash_long(inp.cash, entry_exec, inp.fee_rate) if inp.side == "long" else calculate_cash_short(inp.cash, entry_exec, inp.fee_rate)
    remaining_exposure = max(0.0, inp.equity * inp.max_exposure_ratio - inp.open_gross_notional)
    q_exposure = remaining_exposure / entry_exec if entry_exec > 0 else 0.0
    risk_limit = inp.equity * inp.risk_budget_ratio
    remaining_risk = max(0.0, risk_limit - inp.risk_open)
    # Use qty = 0 for incremental risk since qty unknown; per-unit risk from entry/stop.
    incremental_per_unit = calculate_risk_incremental(inp.side, 1.0, entry_exec, stop_, inp.fee_rate)
    q_risk = remaining_risk / incremental_per_unit if incremental_per_unit > 0 else 0.0
    q_raw = min(q_cash, q_exposure, q_risk)
    qty = floor_to_step(max(0.0, q_raw), inp.quantity_step)
    risk_incremental = calculate_risk_incremental(inp.side, qty, entry_exec, stop_, inp.fee_rate)
    gross_new = inp.open_gross_notional + qty * entry_exec
    ok = qty >= inp.q_min and math.isfinite(qty) and math.isfinite(gross_new) and math.isfinite(risk_incremental)
    reason = "ok" if ok else "below_q_min"
    return SizingResult(qty, ok, reason, entry_exec, stop_, q_cash, q_risk, q_exposure, inp.risk_open, risk_incremental, inp.open_gross_notional, gross_new)
