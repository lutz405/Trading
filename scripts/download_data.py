"""Download recent BTC/USDT OHLCV for all configured timeframes."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from tradingai.data.provider import BinanceOHLCVProvider
from tradingai.data.storage import ParquetStorage
from tradingai.data.validation import validate_ohlcv

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30, help="Days of history to fetch")
    parser.add_argument("--symbol", default="BTC/USDT")
    args = parser.parse_args()

    with open(ROOT / "config" / "settings.yaml") as f:
        cfg = yaml.safe_load(f)

    provider = BinanceOHLCVProvider(
        symbol=args.symbol,
        timeframes=cfg["timeframes"],
        rate_limit_ms=cfg.get("rate_limit_ms", 1200),
        max_candles=cfg.get("max_candles_per_request", 1000),
    )
    storage = ParquetStorage(ROOT / cfg.get("data_dir", "data/raw"))
    for tf in cfg["timeframes"]:
        print(f"Fetching {args.symbol} {tf} ({args.days}d)...")
        df = provider.fetch_all(tf, days=args.days)
        df = validate_ohlcv(df)
        path = storage.save(df, args.symbol, tf)
        print(f"  -> {len(df)} rows saved to {path}")


if __name__ == "__main__":
    main()
