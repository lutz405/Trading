from tradingai.paper.broker import PaperBroker
import tempfile, os

def test_open_close():
    b = PaperBroker(capital=1000, fee=0, slippage=0)
    assert b.open_position("long", 100, 2, 90, 110)
    assert b.capital == 800
    b.close_position(0, 110)
    assert b.capital == 1020
    assert len(b.trades) == 1

def test_insufficient_funds():
    b = PaperBroker(capital=10, fee=0, slippage=0)
    assert not b.open_position("long", 100, 2, 90, 110)

def test_persistence():
    b = PaperBroker(capital=500, fee=0.001, slippage=0.0005)
    b.open_position("long", 50, 1, 45, 55)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "state.json")
        b.save(p)
        b2 = PaperBroker.load(p)
        assert b2.capital == b.capital
        assert len(b2.positions) == 1

def test_stops():
    b = PaperBroker(capital=1000, fee=0, slippage=0)
    b.open_position("long", 100, 1, 95, 110)
    b.check_stops(high=111, low=94)
    assert len(b.positions) == 0
    assert len(b.trades) == 1
