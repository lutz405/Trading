from __future__ import annotations

import numpy as np
import pandas as pd


def volume_features(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    if "volume" not in df.columns:
        raise ValueError("missing column: volume")
    out = pd.DataFrame(index=df.index)
    out["vol_mean"] = df["volume"].rolling(window=window, min_periods=window).mean()
    out["vol_rel"] = df["volume"] / out["vol_mean"].replace(0, np.nan)
    out["vol_pct_change"] = df["volume"].pct_change()
    mean = out["vol_mean"]
    std = df["volume"].rolling(window=window, min_periods=window).std(ddof=0)
    out["vol_zscore"] = (df["volume"] - mean) / std.replace(0, np.nan)
    out["vol_anomaly"] = (out["vol_zscore"].abs() > 3).astype(int)
    return out
