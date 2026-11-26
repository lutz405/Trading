from __future__ import annotations

import math

import numpy as np
import pandas as pd


def validate_features(df: pd.DataFrame, min_rows: int = 50) -> None:
    if df.empty:
        raise ValueError("empty dataframe")
    if len(df) < min_rows:
        raise ValueError(f"insufficient rows: {len(df)} < {min_rows}")
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if ts.isna().any():
        raise ValueError("invalid timestamps")
    if not ts.is_monotonic_increasing:
        raise ValueError("timestamps not sorted")
    if ts.duplicated().any():
        raise ValueError("duplicate timestamps")
    for col in ["open", "high", "low", "close", "volume"]:
        if df[col].isna().any():
            raise ValueError(f"NaN in {col}")
        if np.isinf(df[col]).any():
            raise ValueError(f"inf in {col}")
    if (df["high"] < df["low"]).any():
        raise ValueError("high < low")
    if (df["close"] > df["high"]).any() or (df["close"] < df["low"]).any():
        raise ValueError("close out of range")
    feat_cols = [c for c in df.columns if c not in required]
    for c in feat_cols:
        if df[c].isna().all():
            raise ValueError(f"all-NaN feature: {c}")
        if np.isinf(df[c].replace([None], 0)).any() if df[c].dtype.kind in "fc" else False:
            raise ValueError(f"inf in feature {c}")
