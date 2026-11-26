from __future__ import annotations

from pathlib import Path

import pandas as pd


class ParquetStorage:
    def __init__(self, base_dir: str | Path = "data/raw") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, symbol: str, timeframe: str) -> Path:
        safe = symbol.replace("/", "_")
        return self.base_dir / f"{safe}_{timeframe}.parquet"

    def save(self, df: pd.DataFrame, symbol: str, timeframe: str) -> Path:
        path = self.path_for(symbol, timeframe)
        df.to_parquet(path, index=False)
        return path

    def load(self, symbol: str, timeframe: str) -> pd.DataFrame:
        path = self.path_for(symbol, timeframe)
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path)
