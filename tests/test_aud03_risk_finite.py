"""Regressions for AUD-03: RiskManager must fail closed on non-finite state."""

import pytest

from tradingai.risk import RiskManager

NAN = float("nan")
INF = float("inf")


def _approve(rm, **overrides):
    values = {
        "proba": [0.2, 0.3, 0.5],
        "volatility": 0.01,
        "price": 50000.0,
        "atr": 1000.0,
        "data_fresh": True,
        "enough_data": True,
    }
    values.update(overrides)
    return rm.approve(**values)


@pytest.mark.parametrize("value", [NAN, INF, -INF, True, "100", -1.0])
def test_update_capital_rejects_invalid_values(value):
    rm = RiskManager()
    before = (rm.capital, rm.peak_capital)
    with pytest.raises(ValueError):
        rm.update_capital(value)
    assert (rm.capital, rm.peak_capital) == before


@pytest.mark.parametrize("value", [NAN, INF, -INF, True, "100"])
def test_register_trade_result_rejects_non_finite_values(value):
    rm = RiskManager()
    before = (rm.capital, rm.peak_capital, rm.daily_loss, rm.cooldown)
    with pytest.raises(ValueError):
        rm.register_trade_result(value)
    assert (rm.capital, rm.peak_capital, rm.daily_loss, rm.cooldown) == before


def test_register_trade_result_rejects_negative_capital():
    rm = RiskManager()
    before = (rm.capital, rm.peak_capital, rm.daily_loss)
    with pytest.raises(ValueError):
        rm.register_trade_result(-10000.01)
    assert (rm.capital, rm.peak_capital, rm.daily_loss) == before


def test_register_trade_result_allows_loss_to_zero_but_approval_fails_closed():
    rm = RiskManager()
    rm.register_trade_result(-10000.0)
    assert rm.capital == 0.0
    assert rm.daily_loss == 10000.0
    ok, reason = _approve(rm)
    assert not ok
    assert reason in ("cooldown active", "max drawdown exceeded")


@pytest.mark.parametrize(
    "field,value",
    [
        ("capital", NAN),
        ("peak_capital", NAN),
        ("peak_capital", -1.0),
        ("peak_capital", 5000.0),
        ("daily_loss", NAN),
        ("daily_loss", INF),
        ("exposure", NAN),
        ("exposure", INF),
        ("exposure", -1.0),
        ("cooldown", -1),
        ("cooldown", True),
        ("max_drawdown", NAN),
        ("max_drawdown", 2.0),
        ("max_exposure", INF),
        ("uncertainty_threshold", NAN),
        ("uncertainty_threshold", 2.0),
    ],
)
def test_approve_rejects_corrupt_state(field, value):
    rm = RiskManager()
    setattr(rm, field, value)
    ok, reason = _approve(rm)
    assert not ok
    assert "invalid risk state" in reason


@pytest.mark.parametrize(
    "proba",
    [
        [0.7, 0.2, NAN],
        [0.7, 0.2, INF],
        [0.7, 0.2, -INF],
        [0.7, 0.2, -0.1],
        [0.7, 0.2, 1.1],
        [0.7, 0.2],
    ],
)
def test_approve_rejects_invalid_probabilities(proba):
    ok, reason = _approve(RiskManager(), proba=proba)
    assert not ok
    assert "invalid probabilities" in reason


def test_approve_rejects_probabilities_not_summing_to_one():
    ok, reason = _approve(RiskManager(), proba=[0.4, 0.3, 0.4])
    assert not ok
    assert "sum" in reason


def test_approve_rejects_high_uncertainty():
    ok, reason = _approve(RiskManager(), proba=[0.3, 0.3, 0.4])
    assert not ok
    assert "uncertainty" in reason


@pytest.mark.parametrize("value", [NAN, INF, -INF, -0.01])
def test_approve_rejects_invalid_volatility(value):
    ok, reason = _approve(RiskManager(), volatility=value)
    assert not ok
    assert "invalid volatility" in reason


@pytest.mark.parametrize("value", [NAN, INF, -INF, 0.0, -1.0])
def test_approve_rejects_invalid_price(value):
    ok, reason = _approve(RiskManager(), price=value)
    assert not ok
    assert "invalid price" in reason


@pytest.mark.parametrize("value", [NAN, INF, -INF, -1.0])
def test_approve_rejects_invalid_atr(value):
    ok, reason = _approve(RiskManager(), atr=value)
    assert not ok
    assert "invalid atr" in reason


def test_approve_still_accepts_valid_state():
    ok, reason = _approve(RiskManager())
    assert ok
    assert reason == "approved"


def test_from_dict_rejects_invalid_parameter_ranges():
    state = RiskManager().to_dict()
    for field, value in [
        ("risk_per_trade", -0.1),
        ("max_drawdown", 1.5),
        ("max_daily_loss", -0.1),
        ("max_exposure", -0.1),
        ("volatility_threshold", -0.1),
        ("uncertainty_threshold", 1.5),
    ]:
        bad = dict(state)
        bad[field] = value
        with pytest.raises(ValueError):
            RiskManager.from_dict(bad)


def test_constructor_rejects_non_finite_parameters():
    with pytest.raises(ValueError):
        RiskManager(initial_capital=NAN)
    with pytest.raises(ValueError):
        RiskManager(max_drawdown=INF)
    with pytest.raises(ValueError):
        RiskManager(cooldown_periods=-1)
