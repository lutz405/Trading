import pandas as pd

from tradingai.data.validation import validate_ohlcv


def make_df():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01", "2024-01-02"], utc=True),
            "open": [100.0, 101.0],
            "high": [105.0, 106.0],
            "low": [99.0, 100.0],
            "close": [102.0, 103.0],
            "volume": [10.0, 11.0],
        }
    )


def test_validate_ok():
    df = validate_ohlcv(make_df())
    assert len(df) == 2


def test_validate_drops_duplicates():
    df = make_df()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    out = validate_ohlcv(df)
    assert len(out) == 2


def test_validate_rejects_bad_high_low():
    df = make_df()
    df.loc[0, "high"] = 90.0
    try:
        validate_ohlcv(df)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
