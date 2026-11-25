import numpy as np
import pandas as pd
import pytest

from tradingai.ml.labels import make_labels


@pytest.mark.parametrize("bad_close", [np.nan, np.inf, -np.inf, 0.0, -1.0])
def test_make_labels_rejects_non_finite_or_non_positive_close(bad_close):
    df = pd.DataFrame({"close": [100.0, 101.0, 102.0, 103.0]})
    df.loc[1, "close"] = bad_close
    with pytest.raises(ValueError, match="finite and positive"):
        make_labels(df, horizon=1)


def test_make_labels_accepts_finite_positive_close():
    df = pd.DataFrame({"close": np.linspace(100.0, 120.0, 30)})
    labels = make_labels(df, horizon=5)
    assert labels.notna().any()
    assert set(labels.dropna().unique()).issubset({0.0, 1.0, 2.0})
