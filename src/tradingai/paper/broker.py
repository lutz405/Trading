from __future__ import annotations

import json
import logging
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

from tradingai.accounting import (
    execution_price,
    gross_pnl,
    slippage_cost_amount,
    validate_number,
    validate_side,
)
from tradingai.risk.sizing import (
    DEFAULT_Q_MIN,
    DEFAULT_QUANTITY_STEP,
    SizingInput,
    calculate_position_size,
    stop_exec,
)

logger = logging.getLogger("paper")


@dataclass
class Position:
    side: str
    entry_price: float
    qty: float
    stop: float
    take: float
    entry_fee: float = 0.0
    entry_slippage: float = 0.0


@dataclass
class PaperBroker:
    capital: float = 10000.0
    fee: float = 0.001
    slippage: float = 0.0005
    positions: list[Position] = field(default_factory=list)
    trades: list[dict] = field(default_factory=list)
    schema_version: int = 2
    risk_state: dict | None = None
    initial_capital: float | None = None
    realized_gross_pnl: float = 0.0
    realized_net_pnl: float = 0.0
    fees_paid: float = 0.0
    slippage_cost: float = 0.0
    risk_budget_ratio: float = 0.1
    max_exposure_ratio: float = 0.5
    quantity_step: float = DEFAULT_QUANTITY_STEP
    q_min: float = DEFAULT_Q_MIN

    def __post_init__(self) -> None:
        if self.initial_capital is None:
            self.initial_capital = float(self.capital if self.capital is not None else 10000.0)

    @property
    def cash(self) -> float:
        return self.capital

    @property
    def collateral(self) -> float:
        return sum(p.qty * p.entry_price for p in self.positions if p.side == "short")

    @property
    def realized_equity(self) -> float:
        return (float(self.initial_capital) if self.initial_capital is not None else 0.0) + self.realized_net_pnl

    def _long_market_value(self, mark: float) -> float:
        return sum(p.qty * mark for p in self.positions if p.side == "long")

    def _short_liability(self, mark: float) -> float:
        return sum(p.qty * mark for p in self.positions if p.side == "short")

    def equity(self, mark_price: float) -> float:
        mark = validate_number(mark_price, "mark_price", positive=True)
        return self.capital + self.collateral + self._long_market_value(mark) - self._short_liability(mark)

    def _validate_position_fields(self) -> None:
        for p in self.positions:
            validate_side(p.side)
            qty = validate_number(p.qty, "position.qty", positive=True)
            entry = validate_number(p.entry_price, "position.entry_price", positive=True)
            stop = validate_number(p.stop, "position.stop", positive=True)
            take = validate_number(p.take, "position.take", positive=True)
            validate_number(p.entry_fee, "position.entry_fee", nonnegative=True)
            validate_number(p.entry_slippage, "position.entry_slippage", nonnegative=True)
            if p.side == "long" and not (stop < entry < take):
                raise ValueError("invalid long position fields")
            if p.side == "short" and not (take < entry < stop):
                raise ValueError("invalid short position fields")
            _ = qty

    def _validate_trade_fields(self) -> None:
        for t in self.trades:
            if not isinstance(t, dict):
                raise TypeError("invalid trade record")
            required = ["side", "entry", "exit", "qty", "entry_fee", "exit_fee", "gross_pnl", "pnl", "fees", "slippage"]
            if any(k not in t for k in required):
                raise ValueError("invalid trade record fields")
            side = validate_side(t["side"])
            qty = validate_number(t["qty"], "trade.qty", positive=True)
            entry = validate_number(t["entry"], "trade.entry", positive=True)
            exit_ = validate_number(t["exit"], "trade.exit", positive=True)
            entry_fee = validate_number(t["entry_fee"], "trade.entry_fee", nonnegative=True)
            exit_fee = validate_number(t["exit_fee"], "trade.exit_fee", nonnegative=True)
            gross = validate_number(t["gross_pnl"], "trade.gross_pnl")
            pnl = validate_number(t["pnl"], "trade.pnl")
            fees = validate_number(t["fees"], "trade.fees", nonnegative=True)
            slip = validate_number(t["slippage"], "trade.slippage", nonnegative=True)
            expected_gross = qty * (exit_ - entry) if side == "long" else qty * (entry - exit_)
            expected_pnl = expected_gross - entry_fee - exit_fee
            if not math.isclose(gross, expected_gross, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("trade gross_pnl mismatch")
            if not math.isclose(pnl, expected_pnl, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("trade pnl mismatch")
            if not math.isclose(fees, entry_fee + exit_fee, rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError("trade fees mismatch")
            if slip < 0:
                raise ValueError("invalid trade slippage")

    def _expected_fees_paid(self) -> float:
        return sum(t["fees"] for t in self.trades) + sum(p.entry_fee for p in self.positions)

    def _expected_slippage_cost(self) -> float:
        return sum(t["slippage"] for t in self.trades) + sum(p.entry_slippage for p in self.positions)

    def _validate_state_for_save(self) -> None:
        validate_number(self.capital, "capital")
        validate_number(self.initial_capital, "initial_capital", positive=True)
        validate_number(self.fee, "fee", nonnegative=True)
        validate_number(self.slippage, "slippage", nonnegative=True)
        validate_number(self.realized_gross_pnl, "realized_gross_pnl")
        validate_number(self.realized_net_pnl, "realized_net_pnl")
        validate_number(self.fees_paid, "fees_paid", nonnegative=True)
        validate_number(self.slippage_cost, "slippage_cost", nonnegative=True)
        if self.risk_state is not None:
            validate_number(self.risk_state["capital"], "risk_state.capital")
        self._validate_position_fields()
        self._validate_trade_fields()
        expected_gross = sum(t["gross_pnl"] for t in self.trades)
        expected_net = sum(t["pnl"] for t in self.trades)
        expected_fees = self._expected_fees_paid()
        expected_slip = self._expected_slippage_cost()
        expected_collateral = sum(p.qty * p.entry_price for p in self.positions if p.side == "short")
        if not math.isclose(self.realized_gross_pnl, expected_gross, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("realized_gross_pnl mismatch")
        if not math.isclose(self.realized_net_pnl, expected_net, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("realized_net_pnl mismatch")
        if not math.isclose(self.fees_paid, expected_fees, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("fees_paid mismatch")
        if not math.isclose(self.slippage_cost, expected_slip, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("slippage_cost mismatch")
        if not math.isclose(self.collateral, expected_collateral, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("collateral mismatch")
        if not self.positions and not math.isclose(self.capital, self.realized_equity, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("capital must equal realized_equity when no positions are open")
        if self.risk_state is not None and not math.isclose(
            float(self.risk_state["capital"]), self.realized_equity, rel_tol=1e-9, abs_tol=1e-9
        ):
            raise ValueError("risk_state.capital must equal realized_equity")

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self._validate_state_for_save()
        data = {
            "schema_version": 2,
            "initial_capital": self.initial_capital,
            "capital": self.capital,
            "fee": self.fee,
            "slippage": self.slippage,
            "positions": [asdict(x) for x in self.positions],
            "trades": self.trades,
            "realized_gross_pnl": self.realized_gross_pnl,
            "realized_net_pnl": self.realized_net_pnl,
            "fees_paid": self.fees_paid,
            "slippage_cost": self.slippage_cost,
            "collateral": self.collateral,
            "risk_state": self.risk_state,
            "risk_budget_ratio": self.risk_budget_ratio,
            "max_exposure_ratio": self.max_exposure_ratio,
            "quantity_step": self.quantity_step,
            "q_min": self.q_min,
        }
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=2, allow_nan=False))
        tmp.replace(p)

    def _risk_open(self, mark_price: float) -> float:
        risk_open = 0.0
        for p in self.positions:
            validate_side(p.side)
            qty = validate_number(p.qty, "position.qty", positive=True)
            mark = validate_number(mark_price, "mark_price", positive=True)
            if p.stop is not None and math.isfinite(p.stop) and p.stop > 0:
                stop_ = stop_exec(p.side, p.stop, self.slippage)
                adverse = max(0.0, mark - stop_) if p.side == "long" else max(0.0, stop_ - mark)
                risk_open += qty * (adverse + self.fee * stop_)
            else:
                risk_open += qty * mark * (1 + self.fee)
        return risk_open

    def open_position(self, side: str, price: float, qty: float | None, stop: float, take: float) -> bool:
        validate_number(self.fee, "fee", nonnegative=True)
        validate_number(self.slippage, "slippage", nonnegative=True)
        side = validate_side(side)
        validate_number(price, "price", positive=True)
        if qty is not None:
            qty = validate_number(qty, "qty", positive=True)
        validate_number(stop, "stop", positive=True)
        validate_number(take, "take", positive=True)
        entry = execution_price(price, side, self.slippage, opening=True)
        if side == "long" and not (stop < entry < take):
            return False
        if side == "short" and not (take < entry < stop):
            return False
        gross_open = sum(abs(p.qty * p.entry_price) for p in self.positions)
        try:
            sizing = calculate_position_size(
                SizingInput(
                    side=side,
                    price=price,
                    equity=self.equity(entry),
                    cash=self.capital,
                    risk_budget_ratio=self.risk_budget_ratio,
                    max_exposure_ratio=self.max_exposure_ratio,
                    fee_rate=self.fee,
                    slippage=self.slippage,
                    stop=stop,
                    open_gross_notional=gross_open,
                    risk_open=self._risk_open(entry),
                    quantity_step=self.quantity_step,
                    q_min=self.q_min,
                )
            )
        except (ValueError, OverflowError):
            return False
        if not sizing.ok or sizing.reason == "stop_hit":
            return False
        if qty is None:
            qty = sizing.qty
        if qty > sizing.qty:
            return False
        notional = entry * qty
        fee = notional * self.fee
        slip = slippage_cost_amount(qty, price, self.slippage)
        validate_number(entry, "entry", positive=True)
        validate_number(notional, "entry_notional", positive=True)
        validate_number(fee, "entry_fee", nonnegative=True)
        validate_number(slip, "entry_slip", nonnegative=True)
        new_capital = self.capital - (notional + fee if side == "long" else fee)
        new_fees_paid = self.fees_paid + fee
        new_slippage_cost = self.slippage_cost + slip
        validate_number(new_capital, "new_capital")
        validate_number(new_fees_paid, "new_fees_paid", nonnegative=True)
        validate_number(new_slippage_cost, "new_slippage_cost", nonnegative=True)
        # Both long entries and cash-collateralised shorts must cover the full
        # notional plus the fee with free cash.
        if notional + fee > self.capital:
            return False
        self.capital = new_capital
        self.positions.append(Position(side, entry, qty, stop, take, entry_fee=fee, entry_slippage=slip))
        self.fees_paid = new_fees_paid
        self.slippage_cost = new_slippage_cost
        return True

    def close_position(self, idx: int, price: float, reason: str = "manual") -> bool:
        validate_number(self.fee, "fee", nonnegative=True)
        validate_number(self.slippage, "slippage", nonnegative=True)
        if not isinstance(idx, int) or isinstance(idx, bool) or idx < 0 or idx >= len(self.positions):
            return False
        pos = self.positions[idx]
        entry = validate_number(pos.entry_price, "entry", positive=True)
        qty = validate_number(pos.qty, "qty", positive=True)
        side = validate_side(pos.side)
        entry_fee = validate_number(pos.entry_fee, "entry_fee", nonnegative=True)
        entry_slip = validate_number(pos.entry_slippage, "entry_slippage", nonnegative=True)
        exit_price = execution_price(price, side, self.slippage, opening=False)
        exit_notional = exit_price * qty
        exit_fee = exit_notional * self.fee
        exit_slip = slippage_cost_amount(qty, price, self.slippage)
        validate_number(exit_fee, "exit_fee", nonnegative=True)
        gross = gross_pnl(side, qty, entry, exit_price)
        pnl = gross - entry_fee - exit_fee
        new_capital = self.capital + exit_notional - exit_fee if side == "long" else self.capital + qty * entry - exit_notional - exit_fee
        new_fees_paid = self.fees_paid + exit_fee
        new_slippage_cost = self.slippage_cost + exit_slip
        new_realized_gross = self.realized_gross_pnl + gross
        new_realized_net = self.realized_net_pnl + pnl
        trade = {
            "side": side,
            "entry": entry,
            "exit": exit_price,
            "qty": qty,
            "entry_notional": entry * qty,
            "exit_notional": exit_notional,
            "gross_pnl": gross,
            "entry_fee": entry_fee,
            "exit_fee": exit_fee,
            "fees": entry_fee + exit_fee,
            "slippage": entry_slip + exit_slip,
            "pnl": pnl,
            "reason": reason,
        }
        for value, name in [
            (entry_fee, "entry_fee"),
            (entry_slip, "entry_slippage"),
            (exit_price, "exit_price"),
            (exit_notional, "exit_notional"),
            (exit_fee, "exit_fee"),
            (exit_slip, "exit_slip"),
            (trade["fees"], "trade_fees"),
            (trade["slippage"], "trade_slippage"),
            (gross, "gross_pnl"),
            (pnl, "pnl"),
            (new_capital, "new_capital"),
            (new_fees_paid, "new_fees_paid"),
            (new_slippage_cost, "new_slippage_cost"),
            (new_realized_gross, "new_realized_gross_pnl"),
            (new_realized_net, "new_realized_net_pnl"),
        ]:
            validate_number(value, name)
        new_positions = self.positions[:idx] + self.positions[idx + 1 :]
        new_trades = self.trades + [trade]
        self.positions = new_positions
        self.capital = new_capital
        self.trades = new_trades
        self.realized_gross_pnl = new_realized_gross
        self.realized_net_pnl = new_realized_net
        self.fees_paid = new_fees_paid
        self.slippage_cost = new_slippage_cost
        return True

    @classmethod
    def load(cls, path: str | Path) -> PaperBroker:
        p = Path(path)
        if not p.exists():
            return cls()
        try:
            data = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError) as e:
            raise ValueError(f"corrupt state file: {p}") from e
        if not isinstance(data, dict) or data.get("schema_version") != 2:
            raise ValueError(f"incompatible schema in state file: {p}")
        required = ["capital", "initial_capital", "realized_gross_pnl", "realized_net_pnl", "fees_paid", "slippage_cost", "collateral", "positions", "trades"]
        for key in required:
            if key not in data:
                raise ValueError(f"missing state field: {key}")
        broker = cls(
            capital=validate_number(data["capital"], "capital"),
            fee=validate_number(data["fee"], "fee", nonnegative=True),
            slippage=validate_number(data["slippage"], "slippage", nonnegative=True),
            positions=[Position(**x) for x in data.get("positions", [])],
            trades=data.get("trades", []),
            initial_capital=validate_number(data["initial_capital"], "initial_capital", positive=True),
            realized_gross_pnl=validate_number(data["realized_gross_pnl"], "realized_gross_pnl"),
            realized_net_pnl=validate_number(data["realized_net_pnl"], "realized_net_pnl"),
            fees_paid=validate_number(data["fees_paid"], "fees_paid", nonnegative=True),
            slippage_cost=validate_number(data["slippage_cost"], "slippage_cost", nonnegative=True),
            risk_state=data.get("risk_state"),
            risk_budget_ratio=validate_number(data.get("risk_budget_ratio", 0.1), "risk_budget_ratio", nonnegative=True),
            max_exposure_ratio=validate_number(data.get("max_exposure_ratio", 0.5), "max_exposure_ratio", nonnegative=True),
            quantity_step=validate_number(data.get("quantity_step", DEFAULT_QUANTITY_STEP), "quantity_step", positive=True),
            q_min=validate_number(data.get("q_min", DEFAULT_Q_MIN), "q_min", nonnegative=True),
        )
        if not isinstance(broker.positions, list) or not isinstance(broker.trades, list):
            raise TypeError("invalid positions or trades")
        if not isinstance(data["collateral"], (int, float)) or not math.isfinite(float(data["collateral"])):
            raise ValueError("invalid collateral")
        if not math.isclose(float(data["collateral"]), broker.collateral, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("collateral mismatch")
        broker._validate_position_fields()
        broker._validate_trade_fields()
        expected_gross = sum(t["gross_pnl"] for t in broker.trades)
        expected_net = sum(t["pnl"] for t in broker.trades)
        expected_fees = broker._expected_fees_paid()
        expected_slip = broker._expected_slippage_cost()
        if not math.isclose(broker.realized_gross_pnl, expected_gross, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("realized_gross_pnl mismatch")
        if not math.isclose(broker.realized_net_pnl, expected_net, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("realized_net_pnl mismatch")
        if not math.isclose(broker.fees_paid, expected_fees, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("fees_paid mismatch")
        if not math.isclose(broker.slippage_cost, expected_slip, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("slippage_cost mismatch")
        if not broker.positions and not math.isclose(broker.capital, broker.realized_equity, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("capital must equal realized_equity when no positions are open")
        if broker.risk_state is not None and not math.isclose(
            float(broker.risk_state["capital"]), broker.realized_equity, rel_tol=1e-9, abs_tol=1e-9
        ):
            raise ValueError("risk_state.capital must equal realized_equity")
        return broker

    def check_stops(self, high: float, low: float) -> None:
        if high is None or low is None:
            return
        try:
            high = float(high)
            low = float(low)
        except (TypeError, ValueError):
            return
        if not (high >= low) or high <= 0 or low <= 0:
            return
        to_close = []
        for i, pos in enumerate(self.positions):
            hit = False
            if pos.side == "long":
                if low <= pos.stop or high >= pos.take:
                    hit = True
            else:
                if high >= pos.stop or low <= pos.take:
                    hit = True
            if hit:
                to_close.append(i)
        for i in reversed(to_close):
            pos = self.positions[i]
            if pos.side == "long":
                exitp = pos.stop if low <= pos.stop else pos.take
                self.close_position(i, exitp, reason="stop" if low <= pos.stop else "take")
            else:
                exitp = pos.stop if high >= pos.stop else pos.take
                self.close_position(i, exitp, reason="stop" if high >= pos.stop else "take")
