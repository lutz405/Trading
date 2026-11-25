# Market data conventions

## Binance/CCXT candle timestamps

The `timestamp` returned by CCXT `fetch_ohlcv()` for Binance is the **candle open
time in UTC**, not the close time. Binance's public kline payload confirms this:
the first field is the open time and the seventh field is the close time.

Verification performed on 2026-11-23 against the public Binance Spot endpoint
(`/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=1`):

```text
openTime_ms  = 1795482000000  -> 2026-11-24 01:00:00 UTC
closeTime_ms = 1795485599999  -> 2026-11-24 01:59:59.999 UTC
delta_ms     = 3,599,999
```

So a candle labelled `t` covers the half-open interval `[t, t + duration)` and
is **closed at** `t + duration`. For example:

- the 1h candle labelled `2024-01-01 04:00` covers 04:00:00–04:59:59.999 and
  closes at 05:00:00;
- the 4h candle labelled `2024-01-01 04:00` covers 04:00–07:59:59.999 and
  closes at 08:00:00.

The local parquet files follow the same convention: all 1h timestamps are on
the hour and all 4h timestamps are at 00:00, 04:00, 08:00, etc.

## Availability rule for higher timeframes

A higher-timeframe bar labelled `t` may only be used by base rows whose
timestamp is **greater than or equal to** the higher bar's close time
`t + duration`.

`features/multitimeframe.py` therefore computes an explicit `available_at`
column (`timestamp + inferred_bar_duration`) and merges backwards on the base
timestamp. An exact match is allowed at the close instant: a 4h bar closing at
04:00 is available to a base row at 04:00, but not to a base row at 03:59 or to
a base row at the 04:00 bar's own open (00:00).

This is also why the base bar itself must be treated as a closed bar. Feature
engineering uses the base bar's OHLC/close, so no decision should be taken
before that base bar closes. The backtest enters on the next bar's open, which
is consistent with using closed-bar features.

## Short accounting model (design for Phase 2, not implemented yet)

Paper trading remains spot-only: no real orders, no leverage, no margin, no
private endpoints. A simulated short must not be modelled by simply flipping
the sign of the long cash flow. The coherent model is a **fully
cash-collateralised short**:

- On opening a short of quantity `q` at price `P`:
  - require free cash of at least `q * P` (100% collateral) plus the entry fee;
  - move `q * P` from free cash to restricted collateral;
  - credit the short-sale proceeds `q * P` to free cash;
  - deduct the entry fee from free cash.
- While open, equity is:

  `free_cash + collateral - q * current_price`

  At entry this equals initial capital minus the entry fee.
- On closing at price `Px`:
  - release the collateral to free cash;
  - debit `q * Px` from free cash to buy back the asset;
  - deduct the exit fee.
- Net trade PnL is `q * (P - Px) - entry_fee - exit_fee`, and the final equity
  must equal `initial_capital + sum(net trade PnL)`.

For a long, free cash decreases by the entry notional plus fee, the position is
marked at `q * current_price`, and equity is `free_cash + market_value`. The
same identity must hold: `final_equity == initial_capital + sum(net PnL)`.

This model is documented now so the Phase 2 accounting fix is based on an
explicit ledger, not on sign inversion.
