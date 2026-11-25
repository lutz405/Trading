from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def validate_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df = df.copy()
    df = df.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    if df["timestamp"].is_monotonic_increasing is False:
        raise ValueError("Timestamps not sorted")
    for col in ["open", "high", "low", "close", "volume"]:
        if (df[col] < 0).any():
            raise ValueError(f"Negative values in {col}")
    if ((df["high"] < df["low"]).any()):
        raise ValueError("high < low detected")
    if ((df["close"] > df["high"]).any() or (df["close"] < df["low"]).any()):
        raise ValueError("close outside [low, high]")
    return df
