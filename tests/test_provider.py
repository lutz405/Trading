from unittest.mock import patch

import pandas as pd

from tradingai.data.provider import BinanceOHLCVProvider


def test_provider_fetch_mocked():
    fake = [[1700000000000, 1.0, 2.0, 0.5, 1.5, 10.0]]
    with patch.object(BinanceOHLCVProvider, "__post_init__", lambda self: None):
        p = BinanceOHLCVProvider.__new__(BinanceOHLCVProvider)
        p.symbol = "BTC/USDT"
        p.timeframes = ["1h"]
        p.rate_limit_ms = 0
        p.max_candles = 1000
        p._exchange = type("E", (), {"fetch_ohlcv": lambda self, *a, **k: fake})()
        df = p.fetch("1h")
    assert len(df) == 1
    assert "timestamp" in df.columns
