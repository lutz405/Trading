import json
import os
import tempfile

import numpy as np
import pytest

from tradingai.ml.calibration import Calibrator


def _valid_sample(n=300, classes=(0, 1, 2), seed=0):
    rng = np.random.default_rng(seed)
    proba = rng.dirichlet(np.ones(len(classes)), size=n)
    y = np.array(classes)[rng.integers(0, len(classes), size=n)]
    return proba, y


def test_fit_rejects_probabilities_outside_unit_interval():
    proba, y = _valid_sample(40, classes=(0, 1))
    proba = proba.copy()
    proba[0] = [2.0, -1.0]
    cal = Calibrator().fit(proba, y, classes=[0, 1])

    assert not cal.fitted
    assert "outside" in cal.reason


def test_fit_rejects_mismatched_lengths():
    proba, y = _valid_sample(40, classes=(0, 1))
    cal = Calibrator().fit(proba[:-1], y, classes=[0, 1])

    assert not cal.fitted
    assert "different lengths" in cal.reason


def test_fit_rejects_missing_validation_class():
    proba, y = _valid_sample(300, classes=(0, 1, 2))
    y = np.where(y == 2, 0, y)
    cal = Calibrator().fit(proba, y, classes=[0, 1, 2])

    assert not cal.fitted
    assert "missing" in cal.reason


def test_invalid_refit_resets_previous_state():
    proba, y = _valid_sample(300, classes=(0, 1))
    cal = Calibrator().fit(proba, y, classes=[0, 1])
    assert cal.fitted

    bad = proba.copy()
    bad[0] = [2.0, -1.0]
    cal.fit(bad, y, classes=[0, 1])

    assert not cal.fitted
    assert cal.calibrators == []
    assert cal.classes == []


def test_load_without_joblib_fails():
    proba, y = _valid_sample(300, classes=(0, 1))
    cal = Calibrator().fit(proba, y, classes=[0, 1])
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "cal.json")
        cal.save(path)
        os.remove(os.path.join(td, "cal.joblib"))
        with pytest.raises(ValueError, match="joblib"):
            Calibrator.load(path)


def test_load_rejects_tampered_metadata():
    proba, y = _valid_sample(300, classes=(0, 1))
    cal = Calibrator().fit(proba, y, classes=[0, 1])
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "cal.json")
        cal.save(path)
        with open(path) as handle:
            payload = json.load(handle)
        payload["classes"] = [0, 1, 2]
        with open(path, "w") as handle:
            handle.write(json.dumps(payload))
        with pytest.raises(ValueError, match="classes mismatch"):
            Calibrator.load(path)


def test_load_rejects_tampered_joblib():
    proba, y = _valid_sample(300, classes=(0, 1))
    cal = Calibrator().fit(proba, y, classes=[0, 1])
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "cal.json")
        cal.save(path)
        joblib_path = os.path.join(td, "cal.joblib")
        with open(joblib_path, "ab") as handle:
            handle.write(b"tampered")
        with pytest.raises(ValueError, match="checksum"):
            Calibrator.load(path)


def test_fitted_transform_requires_matching_class_columns():
    proba, y = _valid_sample(300, classes=(0, 1))
    cal = Calibrator().fit(proba, y, classes=[0, 1])
    with pytest.raises(ValueError, match="columns"):
        cal.transform(np.full((3, 3), 1 / 3))
