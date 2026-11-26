from __future__ import annotations

import pandas as pd


def _infer_bar_duration(timestamps: pd.Series) -> pd.Timedelta:
    """Infer the bar duration from a regular UTC timestamp series.

    Binance/CCXT timestamps are candle open times.  The duration is the
    smallest positive spacing between consecutive bars, which is robust to a
    few missing bars in the higher-timeframe history.
    """
    ts = pd.to_datetime(timestamps, utc=True, errors="coerce")
    if ts.isna().any():
        raise ValueError("higher timeframe contains invalid timestamps")
    if ts.duplicated().any():
        raise ValueError("higher timeframe contains duplicate timestamps")
    diffs = ts.sort_values().diff().dropna()
    positive = diffs[diffs > pd.Timedelta(0)]
    if positive.empty:
        raise ValueError(
            "higher timeframe needs at least two timestamps to infer duration; "
            "pass bar_duration explicitly"
        )
    return positive.min()


def align_higher_timeframe(
    base: pd.DataFrame,
    higher: pd.DataFrame,
    cols: list[str],
    suffix: str,
    bar_duration: str | pd.Timedelta | None = None,
) -> pd.DataFrame:
    """Merge higher-TF indicator columns into base using only closed bars.

    Binance/CCXT timestamps are candle open times.  A higher bar labelled ``t``
    is closed at ``t + duration``; it must not be visible to base rows before
    that instant.  We make that rule explicit with an ``available_at`` column
    and a backward merge on the base timestamp.

    An exact match at ``available_at`` is allowed: a bar that closes at 04:00
    is available to a base row stamped 04:00, but not to rows before 04:00.
    """
    if "timestamp" not in base.columns or "timestamp" not in higher.columns:
        raise ValueError("base and higher must contain a timestamp column")
    missing = [c for c in cols if c not in higher.columns]
    if missing:
        raise ValueError(f"higher timeframe missing columns: {missing}")
    if "timestamp" in cols:
        raise ValueError("timestamp cannot be used as a feature column")
    if higher.empty:
        raise ValueError("higher timeframe is empty")

    h = higher[["timestamp"] + cols].copy()
    h["timestamp"] = pd.to_datetime(h["timestamp"], utc=True, errors="coerce")
    if h["timestamp"].isna().any():
        raise ValueError("higher timeframe contains invalid timestamps")
    if h["timestamp"].duplicated().any():
        raise ValueError("higher timeframe contains duplicate timestamps")
    if bar_duration is None:
        duration = _infer_bar_duration(h["timestamp"])
    else:
        duration = pd.Timedelta(bar_duration)
        if duration <= pd.Timedelta(0):
            raise ValueError("bar_duration must be positive")
    h["available_at"] = h["timestamp"] + duration
    h = h.drop(columns=["timestamp"]).rename(columns={c: f"{c}_{suffix}" for c in cols})
    h = h.sort_values("available_at")

    b = base.copy()
    b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True, errors="coerce")
    if b["timestamp"].isna().any():
        raise ValueError("base contains invalid timestamps")
    b = b.sort_values("timestamp")
    merged = pd.merge_asof(
        b,
        h,
        left_on="timestamp",
        right_on="available_at",
        direction="backward",
        allow_exact_matches=True,
    )
    merged = merged.drop(columns=["available_at"])
    return merged.sort_values("timestamp").reset_index(drop=True)
