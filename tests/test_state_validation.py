import math
import json
import tempfile, os

from tradingai.risk.risk_manager import RiskManager
from tradingai.paper.broker import PaperBroker


def base_state():
    rm = RiskManager()
    rm.register_trade_result(-50)
    rm.cooldown = 2
    return rm.to_dict(), rm


def test_nan_rejected():
    d, _ = base_state()
    for k in ["capital", "peak_capital", "daily_loss", "exposure"]:
        dd = dict(d)
        dd[k] = float("nan")
        try:
            RiskManager.from_dict(dd)
        except ValueError:
            continue
        raise AssertionError(f"NaN accepted in {k}")


def test_inf_rejected():
    d, _ = base_state()
    for k in ["capital", "peak_capital", "daily_loss", "exposure"]:
        dd = dict(d)
        dd[k] = float("inf")
        try:
            RiskManager.from_dict(dd)
        except ValueError:
            continue
        raise AssertionError(f"inf accepted in {k}")


def test_bool_rejected():
    d, _ = base_state()
    d["capital"] = True
    try:
        RiskManager.from_dict(d)
    except ValueError:
        return
    raise AssertionError("bool accepted")


def test_missing_field():
    d, _ = base_state()
    del d["daily_loss"]
    try:
        RiskManager.from_dict(d)
    except ValueError:
        return
    raise AssertionError("missing field accepted")


def test_capital_mismatch_broker():
    d, rm = base_state()
    b = PaperBroker(capital=10000.0)
    b.risk_state = d
    b.risk_state["capital"] = 9999.0  # mismatch
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "s.json")
        try:
            b.save(p)
        except ValueError:
            return
        # if saved, load should reset
        b2 = PaperBroker.load(p)
        assert b2.risk_state is None or b2.capital == 10000.0


def test_accounting_example():
    b = PaperBroker(capital=10000.0, fee=0.001, slippage=0)
    b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    b.close_position(0, 95.0)
    assert abs(b.trades[0]["pnl"] - (-5.195)) < 1e-9
    assert abs(b.capital - 9994.805) < 1e-9
    d, rm = base_state()
    b = PaperBroker(capital=rm.capital)
    b.risk_state = d
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "s.json")
        b.save(p)
        for _ in range(3):
            b2 = PaperBroker.load(p)
            assert b2.risk_state is not None
            rm2 = RiskManager.from_dict(b2.risk_state)
            assert rm2.daily_loss == rm.daily_loss
