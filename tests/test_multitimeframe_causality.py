import numpy as np
import pandas as pd

from tradingai.features.multitimeframe import align_higher_timeframe


def test_higher_bar_not_visible_at_its_open():
    base = pd.DataFrame(
        {"timestamp": pd.date_range("2024-01-01 00:00", periods=9, freq="h", tz="UTC")}
    )
    higher = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01 00:00", "2024-01-01 04:00"], utc=True),
            "rsi_14": [10.0, 20.0],
        }
    )

    merged = align_higher_timeframe(base, higher, ["rsi_14"], "4h")

    # The 00:00 4h bar closes at 04:00.  It must not appear at 00:00, 01:00,
    # 02:00 or 03:00, and it becomes visible exactly at 04:00.
    assert merged.loc[0:3, "rsi_14_4h"].isna().all()
    assert merged.loc[4:7, "rsi_14_4h"].eq(10.0).all()
    # The 04:00 4h bar closes at 08:00.
    assert merged.loc[8, "rsi_14_4h"] == 20.0


def test_higher_bar_visibility_at_minute_boundary():
    base = pd.DataFrame(
        {"timestamp": pd.to_datetime(["2024-01-01 03:59", "2024-01-01 04:00"], utc=True)}
    )
    higher = pd.DataFrame(
        {"timestamp": pd.to_datetime(["2024-01-01 00:00"], utc=True), "rsi_14": [10.0]}
    )

    merged = align_higher_timeframe(
        base, higher, ["rsi_14"], "4h", bar_duration=pd.Timedelta(hours=4)
    )

    assert np.isnan(merged.loc[0, "rsi_14_4h"])
    assert merged.loc[1, "rsi_14_4h"] == 10.0


def test_align_rejects_duplicate_higher_timestamps():
    base = pd.DataFrame({"timestamp": pd.to_datetime(["2024-01-01 04:00"], utc=True)})
    higher = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01 00:00", "2024-01-01 00:00"], utc=True),
            "rsi_14": [10.0, 11.0],
        }
    )

    try:
        align_higher_timeframe(base, higher, ["rsi_14"], "4h")
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate higher timestamps were accepted")
