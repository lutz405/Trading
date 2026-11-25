from __future__ import annotations

import numpy as np


def ensemble_proba(rf_proba: np.ndarray, xgb_proba: np.ndarray, w_rf: float = 0.5, w_xgb: float = 0.5) -> np.ndarray:
    w_rf = max(0.0, w_rf)
    w_xgb = max(0.0, w_xgb)
    s = w_rf + w_xgb
    if s == 0:
        w_rf, w_xgb, s = 0.5, 0.5, 1.0
    return (w_rf * rf_proba + w_xgb * xgb_proba) / s


def predict_with_abstention(proba: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    maxp = proba.max(axis=1)
    pred = proba.argmax(axis=1)
    pred = np.where(maxp >= threshold, pred, -1)
    return pred
