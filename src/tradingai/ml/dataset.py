from __future__ import annotations

import pandas as pd


def build_dataset(
    df: pd.DataFrame,
    feature_cols: list[str],
    horizon: int = 5,
    vol_mult: float = 0.5,
) -> tuple[pd.DataFrame, pd.Series]:
    from .labels import make_labels

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"missing feature columns: {missing}")
    if not feature_cols:
        raise ValueError("feature_cols cannot be empty")

    labels = make_labels(df, horizon=horizon, vol_mult=vol_mult)
    data = df[feature_cols].copy()
    data["__label__"] = labels
    data = data.dropna()
    if data.empty:
        raise ValueError("no labeled rows with complete features")
    y = data.pop("__label__").astype(int)
    X = data
    if not X.index.equals(y.index):
        raise ValueError("feature/label index mismatch")
    return X, y


def chronological_split(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2):
    n = len(X)
    cut = int(n * (1 - test_size))
    return X.iloc[:cut], X.iloc[cut:], y.iloc[:cut], y.iloc[cut:]
