from __future__ import annotations


def atr_stops(price: float, atr: float, stop_mult: float = 1.5, tp_mult: float = 3.0):
    if price <= 0 or atr < 0 or stop_mult <= 0 or tp_mult <= 0:
        return None, None
    stop = price - atr * stop_mult
    take = price + atr * tp_mult
    if stop <= 0:
        return None, None
    return float(stop), float(take)
