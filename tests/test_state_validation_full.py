import math
import os
import tempfile
import pytest

from tradingai.risk.risk_manager import RiskManager
from tradingai.paper.broker import PaperBroker


@pytest.mark.parametrize("field", ["capital", "peak_capital", "daily_loss", "exposure",
                                  "initial_capital", "risk_per_trade", "max_drawdown", "max_daily_loss",
                                  "max_exposure", "volatility_threshold", "uncertainty_threshold"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_rm_nan_inf(field, value):
    d, _ = _base_rm()
    d[field] = value
    with pytest.raises(ValueError):
        RiskManager.from_dict(d)


@pytest.mark.parametrize("field", ["capital", "peak_capital", "daily_loss", "exposure",
                                  "initial_capital", "risk_per_trade", "max_drawdown", "max_daily_loss",
                                  "max_exposure", "volatility_threshold", "uncertainty_threshold"])
def test_rm_bool(field):
    d, _ = _base_rm()
    d[field] = True
    with pytest.raises(ValueError):
        RiskManager.from_dict(d)


def _base_rm():
    rm = RiskManager()
    rm.register_trade_result(-50)
    rm.cooldown = 2
    return rm.to_dict(), rm


def test_rm_missing_field():
    d, _ = _base_rm()
    del d["daily_loss"]
    with pytest.raises(ValueError):
        RiskManager.from_dict(d)


def test_rm_capital_mismatch_broker():
    d, rm = _base_rm()
    b = PaperBroker(capital=10000.0)
    b.risk_state = d
    b.risk_state["capital"] = 9999.0
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "s.json")
        try:
            b.save(p)
        except ValueError:
            return
        b2 = PaperBroker.load(p)
        assert b2.risk_state is None


def test_rm_repeated_recovery():
    d, rm = _base_rm()
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


def test_accounting_example():
    b = PaperBroker(capital=10000.0, fee=0.001, slippage=0)
    b.open_position("long", 100.0, 1.0, 90.0, 110.0)
    b.close_position(0, 95.0)
    assert abs(b.trades[0]["pnl"] - (-5.195)) < 1e-9
    assert abs(b.capital - 9994.805) < 1e-9
