from __future__ import annotations

import logging
import math
from dataclasses import dataclass

from tradingai.accounting import (
    execution_price,
    gross_pnl,
    slippage_cost_amount,
    validate_number,
    validate_side,
)
from tradingai.risk.sizing import SizingInput, calculate_position_size

logger = logging.getLogger("backtesting")


@dataclass
class Trade:
    side: str
    entry_idx: int
    exit_idx: int
    entry_price: float
    exit_price: float
    qty: float
    pnl: float
    fees: float
    slippage: float
    entry_fee: float = 0.0
    exit_fee: float = 0.0
    gross_pnl: float = 0.0
    reason: str = ""


class BacktestEngine:
    def __init__(self, capital: float = 10000.0, fee: float = 0.001, slippage: float = 0.0005, risk_manager=None):
        self.initial_capital = validate_number(capital, "capital", positive=True)
        self.fee = validate_number(fee, "fee", nonnegative=True)
        self.slippage = validate_number(slippage, "slippage", nonnegative=True)
        self.risk = risk_manager
        self.reset()

    def reset(self):
        self.capital = self.initial_capital
        self.peak = self.initial_capital
        self.position = None
        self.pending = None
        self.trades: list[Trade] = []
        self.equity: list[float] = []
        self.max_dd = 0.0
        self.collateral = 0.0
        self.realized_gross_pnl = 0.0
        self.realized_net_pnl = 0.0
        self.fees_paid = 0.0
        self.slippage_cost = 0.0
        self.last_mark: float | None = None

    @property
    def cash(self) -> float:
        return self.capital

    @property
    def realized_equity(self) -> float:
        return self.initial_capital + self.realized_net_pnl

    def _long_market_value(self, mark: float) -> float:
        if self.position is None or self.position["side"] != "long":
            return 0.0
        return self.position["qty"] * mark

    def _short_liability(self, mark: float) -> float:
        if self.position is None or self.position["side"] != "short":
            return 0.0
        return self.position["qty"] * mark

    def mark_equity(self, mark_price: float) -> float:
        mark = validate_number(mark_price, "mark_price", positive=True)
        return self.capital + self.collateral + self._long_market_value(mark) - self._short_liability(mark)

    def _exit_gap(self, idx: int, open_price: float) -> bool:
        """Close at the open when the market has already crossed a level.

        A pending order fills at the bar open, but a stop or take computed from
        the previous close may already be behind the open. Exiting at the level
        in that case would fabricate a better price than the market offered.
        """
        pos = self.position
        if pos is None:
            return False
        if pos["side"] == "long":
            if open_price <= pos["stop"]:
                self._exit(idx, open_price, "stop")
                return True
            if open_price >= pos["take"]:
                self._exit(idx, open_price, "take")
                return True
        else:
            if open_price >= pos["stop"]:
                self._exit(idx, open_price, "stop")
                return True
            if open_price <= pos["take"]:
                self._exit(idx, open_price, "take")
                return True
        return False

    def _enter(self, idx, price, side, qty, stop, take):
        if price <= 0 or qty <= 0:
            return
        side = validate_side(side)
        entry = execution_price(price, side, self.slippage, opening=True)
        entry_notional = entry * qty
        entry_fee = entry_notional * self.fee
        entry_slip = slippage_cost_amount(qty, price, self.slippage)
        # Cash-collateralised shorts require the full notional plus the fee to
        # be covered by free cash at entry, exactly like a long.
        if entry_notional + entry_fee > self.capital:
            logger.warning("insufficient capital for entry")
            return
        if side == "long":
            self.capital -= entry_notional + entry_fee
        else:
            self.capital -= entry_fee
            self.collateral += entry_notional
        self.fees_paid += entry_fee
        self.slippage_cost += entry_slip
        self.position = {
            "side": side,
            "idx": idx,
            "entry": entry,
            "qty": qty,
            "stop": stop,
            "take": take,
            "fees": entry_fee,
            "collateral": entry_notional,
            "entry_slip": entry_slip,
        }

    def _exit(self, idx, price, reason):
        pos = self.position
        if pos is None:
            return
        side = pos["side"]
        qty = pos["qty"]
        entry = pos["entry"]
        exit_price = execution_price(price, side, self.slippage, opening=False)
        exit_notional = exit_price * qty
        exit_fee = exit_notional * self.fee
        exit_slip = slippage_cost_amount(qty, price, self.slippage)
        entry_slip = pos.get("entry_slip", 0.0)
        entry_fee = pos.get("fees", 0.0)
        gross = gross_pnl(side, qty, entry, exit_price)
        if side == "long":
            self.capital += exit_notional - exit_fee
        else:
            short_collateral = pos.get("collateral", qty * entry)
            self.capital += qty * entry - exit_notional - exit_fee
            self.collateral -= short_collateral
        self.realized_gross_pnl += gross
        self.realized_net_pnl += gross - entry_fee - exit_fee
        self.fees_paid += exit_fee
        self.slippage_cost += exit_slip
        trade = Trade(
            side,
            pos["idx"],
            idx,
            entry,
            exit_price,
            qty,
            gross - entry_fee - exit_fee,
            entry_fee + exit_fee,
            entry_slip + exit_slip,
            entry_fee=entry_fee,
            exit_fee=exit_fee,
            gross_pnl=gross,
            reason=reason,
        )
        self.trades.append(trade)
        self.position = None

    def run(self, df, decision_fn):
        self.reset()
        if "open" not in df.columns:
            raise ValueError("missing open column")
        n = len(df)
        for i in range(n):
            row = df.iloc[i]
            open_price = float(row["open"])
            valid_open = math.isfinite(open_price) and open_price > 0
            if not valid_open:
                logger.warning("invalid open at %d; skip pending fill", i)
            elif self.pending is not None and self.position is None:
                side, qty, stop, take = self.pending
                self._enter(i, open_price, side, qty, stop, take)
                self.pending = None

            if self.position is not None:
                gap_exit = valid_open and self._exit_gap(i, open_price)
                if not gap_exit:
                    pos = self.position
                    high = float(row["high"])
                    low = float(row["low"])
                    if (
                        not math.isfinite(high)
                        or not math.isfinite(low)
                        or high <= 0
                        or low <= 0
                        or high < low
                    ):
                        logger.warning("invalid OHLC at %d; skip stop check", i)
                    else:
                        stop_hit = False
                        take_hit = False
                        if pos["side"] == "long":
                            stop_hit = low <= pos["stop"]
                            take_hit = high >= pos["take"]
                        else:
                            stop_hit = high >= pos["stop"]
                            take_hit = low <= pos["take"]
                        # conservative: if both hit same candle, stop first
                        if stop_hit:
                            self._exit(i, pos["stop"], "stop")
                        elif take_hit:
                            self._exit(i, pos["take"], "take")

            price = float(row["close"])
            if not math.isfinite(price) or price <= 0:
                raise ValueError("invalid close price at end of run")
            equity = self.mark_equity(price)
            self.last_mark = price
            self.equity.append(equity)
            self.peak = max(self.peak, equity)
            dd = (self.peak - equity) / self.peak if self.peak > 0 else 0.0
            self.max_dd = max(self.max_dd, dd)

            if self.position is None:
                action = decision_fn(i, row, self)
                if action in ("LONG_SIMULATED", "SHORT_SIMULATED"):
                    price = float(row["close"])
                    side = "long" if action == "LONG_SIMULATED" else "short"
                    if action == "LONG_SIMULATED":
                        stop, take = price * 0.99, price * 1.02
                    else:
                        stop, take = price * 1.01, price * 0.98
                    if self.risk is not None:
                        risk_budget = self.risk.risk_per_trade
                        max_exposure = self.risk.max_exposure
                    else:
                        risk_budget = 0.01
                        max_exposure = 0.5
                    sizing = calculate_position_size(
                        SizingInput(
                            side=side,
                            price=price,
                            equity=self.mark_equity(price),
                            cash=self.capital,
                            risk_budget_ratio=risk_budget,
                            max_exposure_ratio=max_exposure,
                            fee_rate=self.fee,
                            slippage=self.slippage,
                            stop=stop,
                            open_gross_notional=0.0,
                            risk_open=0.0,
                        )
                    )
                    qty = sizing.qty
                    if not sizing.ok or qty <= 0:
                        self.pending = None
                        continue
                    self.pending = (side, qty, stop, take)

        if self.position is not None:
            last_close = float(df.iloc[-1]["close"])
            self._exit(n - 1, last_close, "end")
        if self.equity:
            self.equity[-1] = self.capital
            self.peak = max(self.peak, self.equity[-1])
            if self.peak > 0:
                self.max_dd = max(self.max_dd, (self.peak - self.equity[-1]) / self.peak)
        return self
