from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import joblib
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

SCHEMA_VERSION = 2


def _as_class_list(values) -> list:
    return [v.item() if isinstance(v, np.generic) else v for v in list(values)]


@dataclass
class Calibrator:
    method: str = "none"
    reason: str = ""
    calibrators: list = field(default_factory=list)
    classes: list = field(default_factory=list)
    fitted: bool = False

    def _reset(self) -> None:
        self.method = "none"
        self.reason = ""
        self.calibrators = []
        self.classes = []
        self.fitted = False

    def fit(self, proba_val, y_val, classes=None):
        """Fit a per-class calibrator on validation data only.

        Invalid input leaves the calibrator unfitted (and resets any previous
        state) with a reason, so callers can fail explicitly instead of using a
        partially fitted object.
        """
        self._reset()
        proba_val = np.asarray(proba_val, dtype=float)
        y_val = np.asarray(y_val)
        if proba_val.ndim != 2:
            self.reason = "invalid proba shape"
            return self
        if y_val.ndim != 1:
            self.reason = "invalid label shape"
            return self
        if proba_val.shape[0] != y_val.shape[0]:
            self.reason = "proba and labels have different lengths"
            return self
        if proba_val.shape[0] == 0:
            self.reason = "no validation samples"
            return self
        if not np.isfinite(proba_val).all():
            self.reason = "non-finite proba"
            return self
        if (proba_val < 0).any() or (proba_val > 1).any():
            self.reason = "probabilities outside [0,1]"
            return self
        if not np.allclose(proba_val.sum(axis=1), 1.0, atol=1e-5):
            self.reason = "probability rows do not sum to 1"
            return self

        expected = _as_class_list(classes) if classes is not None else sorted(set(y_val.tolist()))
        if len(expected) != len(set(expected)):
            self.reason = "duplicate classes"
            return self
        if proba_val.shape[1] != len(expected):
            self.reason = "proba columns do not match classes"
            return self
        if len(expected) < 2:
            self.reason = "single class in validation"
            return self
        if len(y_val) < 30:
            self.reason = "insufficient samples"
            return self

        expected_set = set(expected)
        unknown = sorted(set(y_val.tolist()) - expected_set)
        if unknown:
            self.reason = f"labels outside expected classes: {unknown}"
            return self
        missing = [c for c in expected if c not in set(y_val.tolist())]
        if missing:
            self.reason = f"classes missing in validation: {missing}"
            return self

        method = "isotonic" if len(y_val) >= 200 else "sigmoid"
        cals = []
        try:
            for k, cls in enumerate(expected):
                y_bin = (y_val == cls).astype(int)
                if method == "isotonic":
                    ir = IsotonicRegression(out_of_bounds="clip")
                    ir.fit(proba_val[:, k], y_bin)
                    cals.append(("isotonic", ir))
                else:
                    lr = LogisticRegression(solver="lbfgs")
                    lr.fit(proba_val[:, k].reshape(-1, 1), y_bin)
                    cals.append(("sigmoid", lr))
        except (ValueError, TypeError, RuntimeError, np.linalg.LinAlgError) as exc:
            self._reset()
            self.reason = f"fit failed: {exc}"
            return self

        self.classes = expected
        self.calibrators = cals
        self.method = method
        self.fitted = True
        return self

    def transform(self, proba):
        """Apply calibration or return a validated copy when unfitted.

        Invalid shapes, non-finite values, values outside [0,1] and (for a
        fitted calibrator) rows that do not sum to one raise ``ValueError``.
        An unfitted calibrator is an explicit fallback, not a fitted state.
        """
        proba = np.asarray(proba, dtype=float)
        if proba.ndim != 2:
            raise ValueError("proba must be a 2-D array")
        if not np.isfinite(proba).all():
            raise ValueError("proba contains non-finite values")
        if (proba < 0).any() or (proba > 1).any():
            raise ValueError("proba values must be in [0,1]")
        if not self.fitted:
            return proba.copy()
        if proba.shape[1] != len(self.classes):
            raise ValueError("proba columns do not match calibrated classes")
        if len(self.calibrators) != len(self.classes):
            raise ValueError("calibrator state is inconsistent")
        if not np.allclose(proba.sum(axis=1), 1.0, atol=1e-5):
            raise ValueError("proba rows do not sum to 1")

        out = np.zeros_like(proba)
        for k, (method, cal) in enumerate(self.calibrators):
            if method == "isotonic":
                out[:, k] = cal.predict(proba[:, k])
            else:
                out[:, k] = cal.predict_proba(proba[:, k].reshape(-1, 1))[:, 1]
        row_sums = out.sum(axis=1, keepdims=True)
        if (row_sums <= 0).any():
            raise ValueError("calibrated probabilities have non-positive rows")
        return out / row_sums

    def metadata(self):
        return {
            "method": self.method,
            "fitted": self.fitted,
            "reason": self.reason,
            "classes": list(self.classes),
            "n_calibrators": len(self.calibrators),
        }

    def _payload(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "method": self.method,
            "reason": self.reason,
            "classes": list(self.classes),
            "fitted": self.fitted,
            "calibrators": self.calibrators,
        }

    def save(self, path):
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        joblib_path = p.with_suffix(".joblib")
        joblib_tmp = joblib_path.with_suffix(joblib_path.suffix + ".tmp")
        joblib.dump(self._payload(), joblib_tmp)
        digest = hashlib.sha256(joblib_tmp.read_bytes()).hexdigest()
        joblib_tmp.replace(joblib_path)

        data = {
            "schema_version": SCHEMA_VERSION,
            "method": self.method,
            "reason": self.reason,
            "classes": list(self.classes),
            "fitted": self.fitted,
            "n_calibrators": len(self.calibrators),
            "joblib_sha256": digest,
        }
        json_tmp = p.with_suffix(p.suffix + ".tmp")
        json_tmp.write_text(json.dumps(data, indent=2))
        json_tmp.replace(p)

    @classmethod
    def load(cls, path):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(str(p))
        data = json.loads(p.read_text())
        if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("incompatible calibration schema")

        cal = cls(
            method=data.get("method", "none"),
            reason=data.get("reason", ""),
            classes=_as_class_list(data.get("classes", [])),
            fitted=bool(data.get("fitted", False)),
        )
        if not cal.fitted:
            return cal

        joblib_path = p.with_suffix(".joblib")
        if not joblib_path.exists():
            raise ValueError("calibrator metadata is fitted but the .joblib file is missing")
        expected_hash = data.get("joblib_sha256")
        actual_hash = hashlib.sha256(joblib_path.read_bytes()).hexdigest()
        if expected_hash != actual_hash:
            raise ValueError("calibrator metadata and .joblib checksum do not match")

        try:
            payload = joblib.load(joblib_path)
        except Exception as exc:
            raise ValueError(f"cannot load calibrator state: {exc}") from exc
        if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("invalid calibrator joblib payload")
        if bool(payload.get("fitted")) != cal.fitted:
            raise ValueError("calibrator fitted flag mismatch")
        if _as_class_list(payload.get("classes", [])) != cal.classes:
            raise ValueError("calibrator classes mismatch")
        if payload.get("method") != cal.method:
            raise ValueError("calibrator method mismatch")
        calibrators = payload.get("calibrators")
        if not isinstance(calibrators, list) or len(calibrators) != len(cal.classes):
            raise ValueError("calibrator state is inconsistent")
        cal.calibrators = calibrators
        return cal
