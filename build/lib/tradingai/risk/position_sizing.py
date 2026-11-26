from __future__ import annotations

import math


def position_size(capital: float, risk_per_trade: float, volatility: float, price: float, max_exposure: float) -> float:
    if capital <= 0 or price <= 0 or volatility <= 0:
        return 0.0
    risk_amount = capital * risk_per_trade
    per_unit_risk = price * volatility
    if per_unit_risk <= 0:
        return 0.0
    qty = risk_amount / per_unit_risk
    max_qty = (capital * max_exposure) / price
    qty = min(qty, max_qty)
    if not math.isfinite(qty) or qty < 0:
        return 0.0
    return float(qty)
