import pandas as pd

from tradingai.dashboard.app import load_broker, candlestick_figure, equity_dataframe


def test_load_broker_empty(tmp_path):
    p = tmp_path / "s.json"
    b = load_broker(str(p))
    assert b.capital == 10000.0


def test_candlestick_figure():
    df = pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=3, freq="h", tz="UTC"),
                       "open": [1, 2, 3], "high": [2, 3, 4], "low": [0, 1, 2], "close": [1.5, 2.5, 3.5]})
    fig = candlestick_figure(df)
    assert fig is not None


def test_equity_dataframe_empty():
    b = load_broker("/tmp/nope.json")
    df = equity_dataframe(b)
    assert isinstance(df, pd.DataFrame)
