import pandas as pd

from tradingai.data.storage import ParquetStorage


def test_storage_roundtrip(tmp_path):
    df = pd.DataFrame({"a": [1, 2]})
    st = ParquetStorage(tmp_path)
    p = st.save(df, "BTC/USDT", "1h")
    assert p.exists()
    loaded = st.load("BTC/USDT", "1h")
    assert len(loaded) == 2
