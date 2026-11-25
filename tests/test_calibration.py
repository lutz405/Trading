import numpy as np

from tradingai.ml.calibration import Calibrator


def test_fallback_small_sample():
    proba = np.array([[0.8, 0.2], [0.3, 0.7]])
    y = np.array([0, 1])
    cal = Calibrator()
    cal.fit(proba, y)
    assert not cal.fitted
    out = cal.transform(proba)
    np.testing.assert_allclose(out, proba)


def test_calibration_runs():
    rng = np.random.default_rng(0)
    n = 300
    proba = rng.dirichlet([2, 2], size=n)
    y = (rng.random(n) < proba[:, 1]).astype(int)
    cal = Calibrator()
    cal.fit(proba, y)
    assert cal.fitted
    out = cal.transform(proba)
    assert out.shape == proba.shape
    assert np.allclose(out.sum(axis=1), 1.0)


def test_invalid_proba():
    proba = np.array([[0.5, np.nan], [0.5, 0.5]])
    y = np.array([0, 1])
    cal = Calibrator()
    cal.fit(proba, y)
    assert not cal.fitted
    assert "non-finite" in cal.reason


def test_metadata():
    cal = Calibrator()
    assert "method" in cal.metadata()
