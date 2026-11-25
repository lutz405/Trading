import numpy as np
import pandas as pd
import yaml

from tradingai.features.engineering import build_features
from tradingai.ml.calibration import Calibrator
from tradingai.ml.pipeline import run_training


def make_ohlcv(n=400, seed=7):
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high = close + rng.uniform(0, 1, n)
    low = close - rng.uniform(0, 1, n)
    open_ = close + rng.normal(0, 0.5, n)
    vol = rng.uniform(1, 5, n)
    ts = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC")
    return pd.DataFrame(
        {"timestamp": ts, "open": open_, "high": high, "low": low, "close": close, "volume": vol}
    )


def test_pipeline_integration_runs(tmp_path):
    df = make_ohlcv(400)
    feat = build_features(df).dropna().reset_index(drop=True)
    fc = [
        c for c in feat.columns if c not in ["timestamp", "open", "high", "low", "close", "volume"]
    ]
    with open("config/ml.yaml") as handle:
        cfg = yaml.safe_load(handle)
    cfg["model_dir"] = str(tmp_path)
    cfg["use_gpu"] = False
    cfg["rf_params"]["n_estimators"] = 5
    cfg["xgb_params"]["n_estimators"] = 5

    res = run_training(feat, fc, cfg)

    assert "rf" in res and "xgb" in res and "calibrated" in res
    assert res["calibration"]["fitted"] is True
    assert res["calibration"]["classes"] == [0, 1, 2]
    assert res["calibrated"]["classes_present"]
    assert (tmp_path / "calibrator.json").exists()
    loaded = Calibrator.load(tmp_path / "calibrator.json")
    assert loaded.fitted
    assert loaded.classes == [0, 1, 2]
