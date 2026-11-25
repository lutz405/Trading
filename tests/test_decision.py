import yaml

from tradingai.risk import RiskManager
from tradingai.decision.engine import DecisionEngine


def make_engine():
    with open("config/decision.yaml") as f:
        dcfg = yaml.safe_load(f)
    with open("config/risk.yaml") as f:
        rcfg = yaml.safe_load(f)
    rm = RiskManager(**{k: rcfg[k] for k in ["initial_capital", "risk_per_trade", "max_drawdown", "max_daily_loss", "max_exposure", "volatility_threshold", "uncertainty_threshold", "cooldown_periods"]})
    return DecisionEngine(dcfg, rm)


def test_long_signal():
    eng = make_engine()
    res = eng.decide([0.1, 0.2, 0.7], {"1h": {"direction": 1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    assert res["action"] == "LONG_SIMULATED"


def test_short_signal():
    eng = make_engine()
    res = eng.decide([0.7, 0.2, 0.1], {"1h": {"direction": -1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    assert res["action"] == "SHORT_SIMULATED"


def test_hold_sideways():
    eng = make_engine()
    res = eng.decide([0.2, 0.6, 0.2], {"1h": {"direction": 0}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    assert res["action"] == "HOLD"


def test_invalid_proba():
    eng = make_engine()
    res = eng.decide([0.2, 0.2, 0.2], {"1h": {"direction": 1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    assert res["action"] == "HOLD" and "invalid" in res["reason"]


def test_stale_data():
    eng = make_engine()
    res = eng.decide([0.1, 0.2, 0.7], {"1h": {"direction": 1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": False, "enough_data": True})
    assert res["action"] == "HOLD"


def test_conflict():
    eng = make_engine()
    res = eng.decide([0.1, 0.2, 0.7], {"1h": {"direction": 1}, "4h": {"direction": -1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    assert res["action"] == "HOLD"


def test_risk_reject():
    eng = make_engine()
    eng.risk.update_capital(8000)  # drawdown > 0.15? 20% -> reject
    res = eng.decide([0.1, 0.2, 0.7], {"1h": {"direction": 1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    assert res["action"] == "HOLD" and "risk rejected" in res["reason"]


def test_explainability_fields():
    eng = make_engine()
    res = eng.decide([0.1, 0.2, 0.7], {"1h": {"direction": 1}}, {"volatility": 0.01, "price": 50000, "atr": 1000, "data_fresh": True, "enough_data": True})
    for k in ["timestamp", "model_version", "probabilities", "timeframes_used", "indicators", "risk_result", "reason", "action"]:
        assert k in res
