from __future__ import annotations

import numpy as np
import pandas as pd

LABEL_CLASSES = (0, 1, 2)
VOLATILITY_WINDOW = 20


def make_labels(df: pd.DataFrame, horizon: int = 5, vol_mult: float = 0.5) -> pd.Series:
    """Build 3-class labels from future returns and a volatility threshold.

    Rows without a defined volatility estimate or without a known future close
    are left as NaN.  They must not be silently assigned to the sideways class.
    """
    if not isinstance(horizon, (int, np.integer)) or int(horizon) < 1:
        raise ValueError("horizon must be a positive integer")
    horizon = int(horizon)
    if not np.isfinite(vol_mult) or vol_mult <= 0:
        raise ValueError("vol_mult must be a positive finite number")
    if "close" not in df.columns:
        raise ValueError("missing close column")
    if df.empty:
        return pd.Series(dtype=float)

    close = pd.to_numeric(df["close"], errors="coerce")
    if not np.isfinite(close).all() or (close <= 0).any():
        raise ValueError("close must be finite and positive")

    future_ret = close.shift(-horizon) / close - 1
    vol = close.pct_change().rolling(VOLATILITY_WINDOW).std()
    up_thr = vol * vol_mult
    down_thr = -vol * vol_mult

    labels = pd.Series(np.nan, index=df.index, dtype=float)
    valid = future_ret.notna() & vol.notna() & np.isfinite(vol)
    labels[valid & (future_ret > up_thr)] = 2.0  # up
    labels[valid & (future_ret < down_thr)] = 0.0  # down
    labels[valid & ~(future_ret > up_thr) & ~(future_ret < down_thr)] = 1.0  # sideways
    labels.iloc[-horizon:] = np.nan
    return labels
