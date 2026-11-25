from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger("risk")


def _require_finite(value: object, name: str, *, positive: bool = False, nonnegative: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        # Keep ValueError as the single risk-validation contract, consistent
        # with from_dict(); the type itself is still rejected, never coerced.
        raise ValueError(f"{name} must be a finite number")  # noqa: TRY004
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    if positive and number <= 0:
        raise ValueError(f"{name} must be positive")
    if nonnegative and number < 0:
        raise ValueError(f"{name} must be nonnegative")
    return number


def _require_periods(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


@dataclass
class RiskManager:
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.01
    max_drawdown: float = 0.15
    max_daily_loss: float = 0.03
    max_exposure: float = 0.5
    volatility_threshold: float = 0.05
    uncertainty_threshold: float = 0.5
    cooldown_periods: int = 5

    capital: float = field(init=False)
    peak_capital: float = field(init=False)
    daily_loss: float = field(default=0.0)
    exposure: float = field(default=0.0)
    cooldown: int = field(default=0)
    current_day: object = field(default=None)

    def __post_init__(self) -> None:
        self.initial_capital = _require_finite(self.initial_capital, "initial_capital", positive=True)
        self.risk_per_trade = _require_finite(self.risk_per_trade, "risk_per_trade", nonnegative=True)
        self.max_drawdown = _require_finite(self.max_drawdown, "max_drawdown", nonnegative=True)
        self.max_daily_loss = _require_finite(self.max_daily_loss, "max_daily_loss", nonnegative=True)
        self.max_exposure = _require_finite(self.max_exposure, "max_exposure", nonnegative=True)
        self.volatility_threshold = _require_finite(self.volatility_threshold, "volatility_threshold", nonnegative=True)
        self.uncertainty_threshold = _require_finite(
            self.uncertainty_threshold, "uncertainty_threshold", nonnegative=True
        )
        self.cooldown_periods = _require_periods(self.cooldown_periods, "cooldown_periods")
        if self.max_drawdown > 1.0:
            raise ValueError("max_drawdown must be <= 1")
        if self.max_daily_loss > 1.0:
            raise ValueError("max_daily_loss must be <= 1")
        if self.uncertainty_threshold > 1.0:
            raise ValueError("uncertainty_threshold must be <= 1")
        self.capital = self.initial_capital
        self.peak_capital = self.initial_capital
        self.daily_loss = _require_finite(self.daily_loss, "daily_loss", nonnegative=True)
        self.exposure = _require_finite(self.exposure, "exposure", nonnegative=True)
        self.cooldown = _require_periods(self.cooldown, "cooldown")

    def _reject(self, reason: str) -> tuple[bool, str]:
        logger.warning("signal rejected: %s", reason)
        return False, reason

    def _state_error(self) -> str | None:
        try:
            _require_finite(self.initial_capital, "initial_capital", positive=True)
            capital = _require_finite(self.capital, "capital", nonnegative=True)
            peak = _require_finite(self.peak_capital, "peak_capital", nonnegative=True)
            _require_finite(self.daily_loss, "daily_loss", nonnegative=True)
            _require_finite(self.exposure, "exposure", nonnegative=True)
            _require_finite(self.risk_per_trade, "risk_per_trade", nonnegative=True)
            drawdown_limit = _require_finite(self.max_drawdown, "max_drawdown", nonnegative=True)
            daily_limit = _require_finite(self.max_daily_loss, "max_daily_loss", nonnegative=True)
            _require_finite(self.max_exposure, "max_exposure", nonnegative=True)
            _require_finite(self.volatility_threshold, "volatility_threshold", nonnegative=True)
            uncertainty_limit = _require_finite(
                self.uncertainty_threshold, "uncertainty_threshold", nonnegative=True
            )
            _require_periods(self.cooldown_periods, "cooldown_periods")
            _require_periods(self.cooldown, "cooldown")
        except ValueError as exc:
            return f"invalid risk state: {exc}"
        if peak < capital:
            return "invalid risk state: peak_capital below capital"
        if drawdown_limit > 1.0:
            return "invalid risk state: max_drawdown above 1"
        if daily_limit > 1.0:
            return "invalid risk state: max_daily_loss above 1"
        if uncertainty_limit > 1.0:
            return "invalid risk state: uncertainty_threshold above 1"
        return None

    def update_capital(self, new_capital: float) -> None:
        new_capital = _require_finite(new_capital, "capital", nonnegative=True)
        peak = _require_finite(self.peak_capital, "peak_capital", nonnegative=True)
        self.capital = new_capital
        self.peak_capital = max(peak, new_capital)

    def drawdown(self) -> float:
        if self.peak_capital <= 0:
            return 0.0
        return (self.peak_capital - self.capital) / self.peak_capital

    def update_time(self, ts) -> None:
        dt = ts if isinstance(ts, datetime) else datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        day = dt.date()
        if self.current_day is None or day != self.current_day:
            self.current_day = day
            self.daily_loss = 0.0

    def advance(self) -> None:
        if self.cooldown > 0:
            self.cooldown -= 1

    def approve(self, proba, volatility, price, atr, data_fresh, enough_data) -> tuple[bool, str]:
        state_error = self._state_error()
        if state_error is not None:
            return self._reject(state_error)
        if self.cooldown > 0:
            return self._reject("cooldown active")
        if not enough_data:
            return self._reject("insufficient data")
        if not data_fresh:
            return self._reject("stale data")
        if not proba or len(proba) != 3:
            return self._reject("invalid probabilities")
        proba_values: list[float] = []
        for p in proba:
            if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(float(p)):
                return self._reject("invalid probabilities")
            if p < 0 or p > 1:
                return self._reject("invalid probabilities")
            proba_values.append(float(p))
        if abs(sum(proba_values) - 1.0) > 1e-6:
            return self._reject("probabilities do not sum to 1")
        try:
            vol = _require_finite(volatility, "volatility", nonnegative=True)
        except ValueError:
            return self._reject("invalid volatility")
        try:
            _require_finite(price, "price", positive=True)
        except ValueError:
            return self._reject("invalid price")
        try:
            _require_finite(atr, "atr", nonnegative=True)
        except ValueError:
            return self._reject("invalid atr")
        if max(proba_values) < self.uncertainty_threshold:
            return self._reject("high uncertainty")
        if vol > self.volatility_threshold:
            return self._reject("volatility too high")
        if self.drawdown() > self.max_drawdown:
            return self._reject("max drawdown exceeded")
        if self.daily_loss > self.max_daily_loss * self.initial_capital:
            return self._reject("max daily loss exceeded")
        if self.exposure > self.max_exposure:
            return self._reject("max exposure exceeded")
        return True, "approved"

    def register_trade_result(self, pnl: float) -> None:
        state_error = self._state_error()
        if state_error is not None:
            raise ValueError(state_error)
        pnl = _require_finite(pnl, "pnl")
        new_capital = self.capital + pnl
        if not math.isfinite(new_capital):
            raise ValueError("pnl would make capital non-finite")
        if new_capital < 0:
            raise ValueError("pnl would make capital negative")
        new_daily_loss = self.daily_loss + (-pnl if pnl < 0 else 0.0)
        if not math.isfinite(new_daily_loss):
            raise ValueError("daily_loss must be finite")
        new_peak = max(self.peak_capital, new_capital)
        new_cooldown = self.cooldown
        drawdown = (new_peak - new_capital) / new_peak if new_peak > 0 else 0.0
        if drawdown > self.max_drawdown:
            new_cooldown = self.cooldown_periods
        self.capital = new_capital
        self.peak_capital = new_peak
        self.daily_loss = new_daily_loss
        self.cooldown = new_cooldown
        if new_cooldown > 0 and drawdown > self.max_drawdown:
            logger.warning("cooldown triggered for %d periods", new_cooldown)

    def to_dict(self) -> dict:
        return {
            "schema_version": 1,
            "initial_capital": self.initial_capital,
            "risk_per_trade": self.risk_per_trade,
            "max_drawdown": self.max_drawdown,
            "max_daily_loss": self.max_daily_loss,
            "max_exposure": self.max_exposure,
            "volatility_threshold": self.volatility_threshold,
            "uncertainty_threshold": self.uncertainty_threshold,
            "cooldown_periods": self.cooldown_periods,
            "capital": self.capital,
            "peak_capital": self.peak_capital,
            "daily_loss": self.daily_loss,
            "exposure": self.exposure,
            "cooldown": self.cooldown,
            "current_day": str(self.current_day) if self.current_day is not None else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RiskManager":
        if not isinstance(data, dict):
            raise ValueError("risk state must be a dict")
        if data.get("schema_version") != 1:
            raise ValueError("incompatible risk schema_version")
        required = ["initial_capital", "risk_per_trade", "max_drawdown", "max_daily_loss", "max_exposure",
                    "volatility_threshold", "uncertainty_threshold", "cooldown_periods", "capital", "peak_capital",
                    "daily_loss", "exposure", "cooldown"]
        for key in required:
            if key not in data:
                raise ValueError(f"missing risk field: {key}")
        num_fields = ["initial_capital", "risk_per_trade", "max_drawdown", "max_daily_loss", "max_exposure",
                      "volatility_threshold", "uncertainty_threshold", "capital", "peak_capital", "daily_loss", "exposure"]
        for key in num_fields:
            if not isinstance(data[key], (int, float)) or isinstance(data[key], bool):
                raise ValueError(f"invalid type for {key}")
            if not math.isfinite(data[key]):
                raise ValueError(f"non-finite value for {key}")
        if not isinstance(data["cooldown_periods"], int) or isinstance(data["cooldown_periods"], bool):
            raise ValueError("invalid type for cooldown_periods")
        if not isinstance(data["cooldown"], int) or isinstance(data["cooldown"], bool):
            raise ValueError("invalid type for cooldown")
        if data["initial_capital"] <= 0:
            raise ValueError("initial_capital must be > 0")
        if data["capital"] < 0 or data["peak_capital"] < data["capital"]:
            raise ValueError("invalid capital state")
        if data["daily_loss"] < 0 or data["exposure"] < 0:
            raise ValueError("negative risk accumulator")
        if data["cooldown"] < 0 or data["cooldown_periods"] < 0:
            raise ValueError("invalid cooldown")
        if data["risk_per_trade"] < 0:
            raise ValueError("risk_per_trade must be nonnegative")
        if not (0 <= data["max_drawdown"] <= 1):
            raise ValueError("max_drawdown must be in [0, 1]")
        if not (0 <= data["max_daily_loss"] <= 1):
            raise ValueError("max_daily_loss must be in [0, 1]")
        if data["max_exposure"] < 0:
            raise ValueError("max_exposure must be nonnegative")
        if data["volatility_threshold"] < 0:
            raise ValueError("volatility_threshold must be nonnegative")
        if not (0 <= data["uncertainty_threshold"] <= 1):
            raise ValueError("uncertainty_threshold must be in [0, 1]")
        rm = cls(
            initial_capital=float(data["initial_capital"]),
            risk_per_trade=float(data["risk_per_trade"]),
            max_drawdown=float(data["max_drawdown"]),
            max_daily_loss=float(data["max_daily_loss"]),
            max_exposure=float(data["max_exposure"]),
            volatility_threshold=float(data["volatility_threshold"]),
            uncertainty_threshold=float(data["uncertainty_threshold"]),
            cooldown_periods=int(data["cooldown_periods"]),
        )
        rm.capital = float(data["capital"])
        rm.peak_capital = float(data["peak_capital"])
        rm.daily_loss = float(data["daily_loss"])
        rm.exposure = float(data["exposure"])
        rm.cooldown = int(data["cooldown"])
        cd = data.get("current_day")
        if cd is not None:
            if not isinstance(cd, str) or cd.strip() == "":
                raise ValueError("invalid current_day type")
            try:
                rm.current_day = datetime.strptime(cd, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("invalid current_day format")
        else:
            rm.current_day = None
        return rm
