from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterable

import ccxt
import pandas as pd


@dataclass
class BinanceOHLCVProvider:
    symbol: str = "BTC/USDT"
    timeframes: list[str] = field(default_factory=lambda: ["1m", "5m", "15m", "30m", "1h", "4h", "1d"])
    rate_limit_ms: int = 1200
    max_candles: int = 1000
    _exchange: ccxt.binance = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._exchange = ccxt.binance({"enableRateLimit": True, "options": {"defaultType": "spot"}})
        self._exchange.load_markets()

    def fetch(
        self, timeframe: str, since: int | None = None, limit: int | None = None
    ) -> pd.DataFrame:
        if timeframe not in self.timeframes:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        limit = limit or self.max_candles
        rows: list[list] = []
        cursor = since
        while True:
            batch = self._exchange.fetch_ohlcv(self.symbol, timeframe, since=cursor, limit=limit)
            if not batch:
                break
            rows.extend(batch)
            last_ts = batch[-1][0]
            if len(batch) < limit:
                break
            cursor = last_ts + 1
            time.sleep(self.rate_limit_ms / 1000.0)
        if not rows:
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
        df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        return df.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    def fetch_all(self, timeframe: str, days: int = 30) -> pd.DataFrame:
        since = int((pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=days)).timestamp() * 1000)
        return self.fetch(timeframe, since=since)
