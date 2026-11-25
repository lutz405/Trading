import numpy as np
import pandas as pd
import pytest

from tradingai.ml.dataset import build_dataset
from tradingai.ml.labels import VOLATILITY_WINDOW, make_labels


def _frame(n=60, seed=0):
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"),
            "open": close,
            "high": close + 1,
            "low": close - 1,
            "close": close,
            "volume": rng.uniform(1, 5, n),
        }
    )


def test_undefined_volatility_rows_are_not_sideways():
    labels = make_labels(_frame(), horizon=5)

    assert labels.iloc[:VOLATILITY_WINDOW].isna().all()
    assert set(labels.dropna().unique()).issubset({0, 1, 2})


def test_horizon_must_be_positive():
    with pytest.raises(ValueError, match="horizon"):
        make_labels(_frame(), horizon=0)
    with pytest.raises(ValueError, match="horizon"):
        make_labels(_frame(), horizon=-1)


def test_vol_mult_must_be_positive_finite():
    with pytest.raises(ValueError, match="vol_mult"):
        make_labels(_frame(), vol_mult=0)
    with pytest.raises(ValueError, match="vol_mult"):
        make_labels(_frame(), vol_mult=np.inf)


def test_dataset_drops_only_rows_without_label_or_features():
    df = _frame()
    labels = make_labels(df, horizon=5)
    X, y = build_dataset(df, ["close"], horizon=5)
    expected = labels.dropna().index

    assert X.index.equals(y.index)
    assert X.index.equals(expected)
    assert len(X) == len(expected)
