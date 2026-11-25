# Indicators

All indicators are causal (no future data).

- SMA(n): simple moving average over n periods.
- EMA(n): exponential moving average (span n, adjust=False).
- RSI(n=14): Wilder RSI.
- MACD(12,26,9): EMA12-EMA26, signal EMA9, histogram.
- ATR(n=14): Wilder ATR from true range.
- Bollinger(n=20,k=2): SMA ± k*std.
- ADX(n=14): Wilder ADX.
- VWAP: session (per UTC day) cumulative volume-weighted price.

Volume features: vol_mean, vol_rel, vol_pct_change, vol_zscore, vol_anomaly (|z|>3).

Feature engineering in `features/engineering.py` adds returns, lags-free causal transforms only.
Multi-timeframe alignment uses merge_asof backward against an explicit
`available_at` timestamp (higher-bar open time plus inferred bar duration), so
a higher bar is only visible from its close onward. See
`docs/market_data_conventions.md`.
