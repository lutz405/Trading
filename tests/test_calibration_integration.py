import os
import tempfile

import numpy as np
import pytest

from tradingai.ml.calibration import Calibrator


def test_persistence_roundtrip():
    rng = np.random.default_rng(1)
    n = 300
    proba = rng.dirichlet([2, 2], size=n)
    y = (rng.random(n) < proba[:, 1]).astype(int)
    cal = Calibrator()
    cal.fit(proba, y)
    assert cal.fitted
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "cal.json")
        cal.save(p)
        cal2 = Calibrator.load(p)
        assert cal2.method == cal.method
        assert cal2.fitted == cal.fitted
        out1 = cal.transform(proba)
        out2 = cal2.transform(proba)
        np.testing.assert_allclose(out1, out2)


def test_corrupt_state():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "cal.json")
        with open(p, "w") as f:
            f.write("{bad json")
        with pytest.raises(ValueError):
            Calibrator.load(p)


def test_transform_validity():
    rng = np.random.default_rng(2)
    n = 300
    proba = rng.dirichlet([2, 2], size=n)
    y = (rng.random(n) < proba[:, 1]).astype(int)
    cal = Calibrator()
    cal.fit(proba, y)
    out = cal.transform(proba)
    assert np.isfinite(out).all()
    assert (out >= 0).all() and (out <= 1).all()
    assert np.allclose(out.sum(axis=1), 1.0)


def test_holdout_not_used():
    proba_val = np.array([[0.8, 0.2], [0.3, 0.7]] * 20)
    y_val = np.array([0, 1] * 20)
    cal = Calibrator()
    cal.fit(proba_val, y_val)
    assert cal.fitted

    holdout = np.array([[0.9, 0.1], [0.2, 0.8]] * 5)
    out = cal.transform(holdout)
    assert out.shape == holdout.shape
    assert np.isfinite(out).all()
    assert np.allclose(out.sum(axis=1), 1.0)
