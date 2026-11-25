from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from tradingai.data.provider import BinanceOHLCVProvider


def is_stale(last_ts, max_age_minutes: int = 5) -> bool:
    if last_ts is None:
        return True
    now = datetime.now(UTC)
    ts = last_ts if isinstance(last_ts, datetime) else datetime.fromisoformat(str(last_ts))
    return (now - ts).total_seconds() > max_age_minutes * 60


def fetch_latest(provider: BinanceOHLCVProvider, timeframe: str, limit: int = 5) -> Any:
    return provider.fetch(timeframe, limit=limit)
