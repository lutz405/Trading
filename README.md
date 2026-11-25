# TradingAI_BTC

Quantitative BTC/USDT analysis platform. Paper trading only: no real orders,
leverage, margin or private exchange credentials. The repository contains data,
features, ML training/calibration, backtesting, paper broker, risk primitives
and a dashboard; it is a research scaffold, not a validated profitable system.
Phase 1 focuses on ML integrity and chronological data separation.

## Setup (Python 3.13)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .[dev]
```

## Run tests and checks

```bash
pytest -q
ruff check .
```

## Market data and accounting conventions

See `docs/market_data_conventions.md` for the Binance candle timestamp rule and
the cash/collateral model for paper shorts.

## Download data (est. size)

30 days x 7 timeframes. Approx rows: 1m ~43k, 5m ~8.6k, 15m ~2.9k, 30m ~1.4k, 1h ~720, 4h ~180, 1d ~30. Parquet total < 5 MB.

```bash
python scripts/download_data.py --days 30
```

Data saved to `data/raw/BTC_USDT_<tf>.parquet`.
