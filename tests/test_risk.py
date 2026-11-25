from tradingai.risk import RiskManager, position_size, atr_stops


def test_position_size_valid():
    q = position_size(10000, 0.01, 0.02, 50000, 0.5)
    assert q > 0
    assert q <= (10000 * 0.5) / 50000


def test_position_size_invalid():
    assert position_size(0, 0.01, 0.02, 50000, 0.5) == 0.0
    assert position_size(10000, 0.01, 0, 50000, 0.5) == 0.0
    assert position_size(10000, 0.01, 0.02, 0, 0.5) == 0.0


def test_atr_stops():
    sl, tp = atr_stops(50000, 1000, 1.5, 3.0)
    assert sl == 50000 - 1500
    assert tp == 50000 + 3000
    assert atr_stops(50000, 1000, 0, 3.0) == (None, None)


def test_risk_approve_reject():
    rm = RiskManager()
    ok, _ = rm.approve([0.2, 0.3, 0.5], 0.01, 50000, 1000, True, True)
    assert ok
    ok, r = rm.approve([0.3, 0.3, 0.4], 0.01, 50000, 1000, True, True)
    assert not ok and "uncertainty" in r
    ok, r = rm.approve([0.2, 0.3, 0.5], 0.01, 50000, 1000, False, True)
    assert not ok and "stale" in r


def test_drawdown_cooldown():
    rm = RiskManager(initial_capital=10000)
    rm.update_capital(8000)
    assert rm.drawdown() > 0.15
    ok, r = rm.approve([0.1, 0.2, 0.7], 0.01, 50000, 1000, True, True)
    assert not ok
    rm2 = RiskManager()
    rm2.register_trade_result(-400)
    assert rm2.daily_loss == 400
