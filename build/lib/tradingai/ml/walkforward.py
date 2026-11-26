from __future__ import annotations

import pandas as pd

from .dataset import build_dataset


def _validate_timestamps(df: pd.DataFrame) -> None:
    if "timestamp" not in df.columns:
        raise ValueError("missing timestamp column")
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if ts.isna().any():
        raise ValueError("invalid timestamps")
    if ts.duplicated().any():
        raise ValueError("duplicate timestamps")
    if not ts.is_monotonic_increasing:
        raise ValueError("timestamps not sorted")


def run_walk_forward(
    df, feature_cols, horizon, train_fn, eval_fn, train_window=200, test_window=50, step=50, gap=5
):
    _validate_timestamps(df)
    results = []
    n = len(df)
    start = 0
    while start + train_window + gap + test_window <= n:
        train_df = df.iloc[start : start + train_window].copy()
        test_df = df.iloc[
            start + train_window + gap : start + train_window + gap + test_window
        ].copy()
        Xtr, ytr = build_dataset(train_df, feature_cols, horizon=horizon)
        Xte, yte = build_dataset(test_df, feature_cols, horizon=horizon)
        if len(Xtr) == 0 or len(Xte) == 0:
            results.append({"window": len(results), "status": "insufficient data", "metrics": None})
            start += step
            continue
        if len(set(ytr.tolist())) < 2 or len(set(yte.tolist())) < 1:
            results.append(
                {"window": len(results), "status": "insufficient classes", "metrics": None}
            )
            start += step
            continue
        model = train_fn(Xtr, ytr)
        metrics = eval_fn(model, Xte, yte)
        results.append(
            {
                "window": len(results),
                "status": "ok",
                "metrics": metrics,
                "train_size": len(Xtr),
                "test_size": len(Xte),
            }
        )
        start += step
    # aggregate
    valid = [r for r in results if r["metrics"] is not None]
    agg = {}
    if valid:
        for key in ["accuracy", "precision", "recall", "f1"]:
            vals = [r["metrics"][key] for r in valid]
            agg[key] = sum(vals) / len(vals)
        agg["total_trades_windows"] = len(valid)
    return results, agg
