from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import rsi, macd, ema, sma, atr, bollinger_bands, adx, vwap
from .volume import volume_features


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    close = out["close"]
    out["ret_1"] = close.pct_change()
    out["log_ret_1"] = np.log(close / close.shift(1))
    out["sma_20"] = sma(close, 20)
    out["ema_20"] = ema(close, 20)
    out["rsi_14"] = rsi(close, 14)
    macd_line, macd_sig, macd_hist = macd(close)
    out["macd"] = macd_line
    out["macd_signal"] = macd_sig
    out["macd_hist"] = macd_hist
    out["atr_14"] = atr(out, 14)
    bb_u, bb_m, bb_l = bollinger_bands(close, 20, 2.0)
    out["bb_upper"] = bb_u
    out["bb_mid"] = bb_m
    out["bb_lower"] = bb_l
    out["adx_14"] = adx(out, 14)
    out["vwap"] = vwap(out)
    vf = volume_features(out, 20)
    for c in vf.columns:
        out[c] = vf[c]
    out["high_low_range"] = out["high"] - out["low"]
    out["close_open_diff"] = out["close"] - out["open"]
    return out
