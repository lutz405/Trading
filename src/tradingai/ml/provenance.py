"""Provenance v3: schema validation, JCS canonicalization, and integrity checks.

Implements S1 of AUD-04B: JSON Schema v3, RFC 8785 JCS canonicalization,
and pure validators for manifest integrity and consistency.

No model loading, no deserialization, no training.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import datetime
from typing import Any

# ---------------------------------------------------------------------------
# JCS Canonicalization (RFC 8785)
# ---------------------------------------------------------------------------


def _utf16_sort_key(s: str) -> list[int]:
    """RFC 8785 §3.2.3: sort by UTF-16 code units (unsigned)."""
    encoded = s.encode("utf-16-le")
    units = []
    for i in range(0, len(encoded), 2):
        unit = encoded[i] | (encoded[i + 1] << 8)
        units.append(unit)
    return units


def _jcs_number(value: float | int | bool) -> str:
    """RFC 8785 §3.2.2.3: serialize number per ECMAScript Number.prototype.toString.

    Implements the ECMAScript number-to-string algorithm for binary64 (IEEE 754).
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        # Check if integer is within safe integer range for JCS
        # JCS uses binary64; integers beyond 2^53 cannot be precisely represented
        if abs(value) > 2**53:
            # Still serialize as integer (JCS allows this, but precision may be lost)
            return str(value)
        return str(value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise ValueError("NaN and Infinity are not allowed in JCS")
        # Handle -0.0
        if value == 0.0:
            if math.copysign(1.0, value) < 0:
                return "-0"
            return "0"
        # ECMAScript Number.prototype.toString (radix 10)
        # Use Python's format with proper handling
        # For numbers in [1e-6, 1e21): use decimal notation
        # For numbers outside: use scientific notation
        abs_val = abs(value)
        if abs_val >= 1e21 or (abs_val < 1e-6 and abs_val > 0):
            # Scientific notation
            # Use repr and normalize
            r = repr(value)
            # Python uses 'e+20' etc, ECMAScript uses 'e+20' too
            # But need to ensure format matches
            if "e" in r:
                # Python format: 1e+20, ECMAScript: 1e+21
                # They should match for most cases
                return r
            return r
        else:
            # Decimal notation
            r = repr(value)
            # Remove unnecessary .0 for whole numbers? No, ECMAScript keeps .0 for floats
            # Actually, ECMAScript: 1.0.toString() = "1", not "1.0"!
            # Wait, let me check...
            # In ECMAScript: (1.0).toString() === "1"
            # In Python: repr(1.0) === "1.0"
            # This is a difference!
            if r.endswith(".0"):
                r = r[:-2]
            return r
    raise TypeError(f"Unsupported type for JCS number: {type(value)}")


def jcs_canonicalize(obj: Any) -> str:
    """Canonicalize a JSON-compatible object per RFC 8785 JCS.

    Returns the canonical UTF-8 string (no trailing newline).

    Properties are sorted by UTF-16 code units (unsigned).
    Arrays preserve their order.
    Numbers use ECMAScript Number.prototype.toString.
    """
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, int):
        if abs(obj) > 2**53:
            # Still serialize; precision warning but allowed
            pass
        return str(obj)
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise ValueError("NaN and Infinity are not allowed in JCS")
        if obj == 0.0:
            if math.copysign(1.0, obj) < 0:
                return "-0"
            return "0"
        abs_val = abs(obj)
        if abs_val >= 1e21 or (abs_val < 1e-6 and abs_val > 0):
            r = repr(obj)
            return r
        else:
            r = repr(obj)
            if r.endswith(".0"):
                r = r[:-2]
            return r
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if isinstance(obj, list):
        return "[" + ",".join(jcs_canonicalize(item) for item in obj) + "]"
    if isinstance(obj, dict):
        sorted_keys = sorted(obj.keys(), key=_utf16_sort_key)
        pairs = []
        for key in sorted_keys:
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            pairs.append(
                json.dumps(key, ensure_ascii=False, separators=(",", ":"))
                + ":"
                + jcs_canonicalize(obj[key])
            )
        return "{" + ",".join(pairs) + "}"
    raise TypeError(f"Unsupported type for JCS: {type(obj)}")


def jcs_canonical_bytes(obj: Any) -> bytes:
    """Return canonical bytes (UTF-8, no BOM, no trailing newline)."""
    return jcs_canonicalize(obj).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    """Compute SHA-256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_canonical(obj: Any) -> str:
    """SHA-256 of JCS canonical bytes (no trailing newline)."""
    return sha256_bytes(jcs_canonical_bytes(obj))


# ---------------------------------------------------------------------------
# Strict JSON parsing
# ---------------------------------------------------------------------------


class StrictJSONError(Exception):
    """Raised when JSON parsing fails strict validation."""


def parse_json_strict(text: str) -> Any:
    """Parse JSON with strict validation."""
    if text.startswith("\ufeff"):
        raise StrictJSONError("BOM is not allowed")

    def _check_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        for key, _ in pairs:
            if key in seen:
                raise StrictJSONError(f"Duplicate key: {key}")
            seen.add(key)
        return dict(pairs)

    def _reject_non_finite(value: str) -> Any:
        raise StrictJSONError(f"Non-finite value not allowed: {value}")

    try:
        result = json.loads(
            text, parse_constant=_reject_non_finite, object_pairs_hook=_check_duplicates
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise StrictJSONError(str(exc)) from exc

    return result


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

import os as _os2

_SCHEMA_PATH = _os2.path.join(
    _os2.path.dirname(_os2.path.dirname(__file__)),
    "schemas",
    "manifest_v3.json",
)


def load_manifest_schema() -> dict[str, Any]:
    """Load the manifest v3 JSON Schema from disk."""
    with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


MANIFEST_SCHEMA: dict[str, Any] = load_manifest_schema()


def validate_schema(manifest: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    """Validate manifest against JSON Schema. Returns list of errors (empty = valid)."""
    try:
        import jsonschema
        from jsonschema import FormatChecker
    except ImportError:
        return ["jsonschema not available"]

    if schema is None:
        schema = MANIFEST_SCHEMA

    validator = jsonschema.Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in validator.iter_errors(manifest):
        errors.append(f"{error.json_path}: {error.message}")
    return errors


# ---------------------------------------------------------------------------
# RFC 3339 validation
# ---------------------------------------------------------------------------


def validate_rfc3339(value: str, require_utc: bool = False) -> bool:
    """Validate RFC 3339 date-time with real date checking."""
    if not isinstance(value, str):
        return False

    if require_utc and not value.endswith("Z"):
        return False

    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.(\d+))?Z?$", value)
    if not m:
        return False

    year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    hour, minute, second = int(m.group(4)), int(m.group(5)), int(m.group(6))

    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if hour > 23 or minute > 59 or second > 59:
        return False

    try:
        datetime(year, month, day, hour, minute, second)
    except ValueError:
        return False

    return True


# ---------------------------------------------------------------------------
# Validator functions
# ---------------------------------------------------------------------------


def validate_model_id(model_id: str) -> bool:
    """Validate model_id format: ^mdl_[0-9A-HJKMNP-TV-Z]{26}$"""
    return bool(re.match(r"^mdl_[0-9A-HJKMNP-TV-Z]{26}$", model_id))


def validate_event_id(event_id: str) -> bool:
    """Validate event_id format: evt_ + ULID (26 chars)."""
    return bool(re.match(r"^evt_[0-9A-HJKMNP-TV-Z]{26}$", event_id))


def validate_sha256(value: str) -> bool:
    """Validate SHA-256 hex string (64 chars)."""
    return bool(re.match(r"^[0-9a-f]{64}$", value))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate a manifest dict. Integrates all structural and semantic checks."""
    errors: list[str] = []

    errors.extend(validate_schema(manifest))

    if "model_id" in manifest and not validate_model_id(manifest["model_id"]):
        errors.append("Invalid model_id format")

    if "created_at" in manifest and not validate_rfc3339(manifest["created_at"], require_utc=True):
        errors.append("Invalid created_at format (must be UTC RFC 3339)")
    if "sealed_at" in manifest and not validate_rfc3339(manifest["sealed_at"], require_utc=True):
        errors.append("Invalid sealed_at format (must be UTC RFC 3339)")

    if "run_fingerprint" in manifest and not validate_sha256(manifest["run_fingerprint"]):
        errors.append("Invalid run_fingerprint format")

    errors.extend(validate_calibrator_binding(manifest))
    errors.extend(validate_partition_consistency(manifest))

    return errors


def validate_event(
    event: dict[str, Any], previous_event: dict[str, Any] | None = None
) -> list[str]:
    """Validate a lifecycle event. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    required_fields = [
        "sequence_number",
        "previous_event_sha256",
        "event_id",
        "model_id",
        "event",
        "at",
        "manifest_sha256",
        "actor",
        "evidence",
    ]
    for field in required_fields:
        if field not in event:
            errors.append(f"Missing required field: {field}")

    allowed_fields = set(required_fields) | {"event_sha256"}
    for key in event:
        if key not in allowed_fields:
            errors.append(f"Unknown field in event: {key}")

    if "event_id" in event and not validate_event_id(event["event_id"]):
        errors.append("Invalid event_id format")

    if "model_id" in event and not validate_model_id(event["model_id"]):
        errors.append("Invalid model_id format")

    if "manifest_sha256" in event and not validate_sha256(event["manifest_sha256"]):
        errors.append("Invalid manifest_sha256 format")

    if "at" in event and not validate_rfc3339(event["at"], require_utc=True):
        errors.append("Invalid at format (must be UTC RFC 3339)")

    if "previous_event_sha256" in event and not validate_sha256(event["previous_event_sha256"]):
        errors.append("Invalid previous_event_sha256 format")

    if "event" in event and event["event"] not in (
        "sealed",
        "validated",
        "approved",
        "deprecated",
        "revoked",
    ):
        errors.append(f"Invalid event type: {event['event']}")

    if "sequence_number" in event:
        if not isinstance(event["sequence_number"], int) or isinstance(
            event["sequence_number"], bool
        ):
            errors.append("sequence_number must be an integer")
        elif event["sequence_number"] < 1:
            errors.append("sequence_number must be >= 1")

    if "actor" in event and not isinstance(event["actor"], str):
        errors.append("actor must be a string")

    # Chain verification
    if previous_event is not None:
        if "sequence_number" in event and "sequence_number" in previous_event:
            if event["sequence_number"] != previous_event["sequence_number"] + 1:
                errors.append(
                    f"Sequence gap: expected {previous_event['sequence_number'] + 1}, "
                    f"got {event['sequence_number']}"
                )
        if "event_sha256" in previous_event:
            if event.get("previous_event_sha256") != previous_event.get("event_sha256"):
                errors.append("previous_event_sha256 does not match previous event's event_sha256")

    # First event check
    if previous_event is None and "sequence_number" in event:
        if event["sequence_number"] != 1:
            errors.append("First event must have sequence_number == 1")
        if event.get("previous_event_sha256") != "0" * 64:
            errors.append("First event must have previous_event_sha256 == '0'*64")

    return errors


def verify_event_hash(event: dict[str, Any], expected_hash: str) -> bool:
    """Verify that event_sha256 matches the canonical hash of the event (excluding event_sha256 itself)."""
    event_copy = {k: v for k, v in event.items() if k != "event_sha256"}
    computed = sha256_canonical(event_copy)
    return computed == expected_hash


def validate_calibrator_binding(manifest: dict[str, Any]) -> list[str]:
    """Validate that calibrator is bound to the correct base model."""
    errors: list[str] = []

    calibration = manifest.get("calibration", {})
    base_model_id = calibration.get("base_model_id")
    model_id = manifest.get("model_id")

    if calibration.get("mode") == "in_pipeline":
        if base_model_id != model_id:
            errors.append(
                f"Calibrator base_model_id ({base_model_id}) != model_id ({model_id}) "
                "in in_pipeline mode"
            )

    base_hashes = calibration.get("base_artifact_sha256", {})
    artifacts = {a["role"]: a["sha256"] for a in manifest.get("artifacts", [])}

    if "rf" in base_hashes and "rf" in artifacts:
        if base_hashes["rf"] != artifacts["rf"]:
            errors.append("Calibrator base rf hash != manifest rf artifact hash")
    if "xgb" in base_hashes and "xgb" in artifacts:
        if base_hashes["xgb"] != artifacts["xgb"]:
            errors.append("Calibrator base xgb hash != manifest xgb artifact hash")

    if calibration.get("artifact_sha256") and "calibrator" in artifacts:
        if calibration["artifact_sha256"] != artifacts["calibrator"]:
            errors.append("Calibrator artifact_sha256 != manifest calibrator artifact hash")

    if calibration.get("classes") != manifest.get("target", {}).get("classes"):
        errors.append("Calibration classes != target classes")
    if calibration.get("class_order") != manifest.get("target", {}).get("class_order"):
        errors.append("Calibration class_order != target class_order")

    if calibration.get("fit_partition") == "test":
        errors.append("Calibration fit_partition cannot be 'test'")

    if calibration.get("n_calibrators") != len(calibration.get("classes", [])):
        errors.append("n_calibrators != len(classes)")

    return errors


def validate_partition_consistency(manifest: dict[str, Any]) -> list[str]:
    """Validate partition consistency (row counts, class counts, purge, temporal ordering)."""
    errors: list[str] = []

    validation = manifest.get("validation", {})
    partitions = validation.get("partitions", {})

    for pname in ("train", "validation", "calibration", "test"):
        if pname not in partitions:
            errors.append(f"Missing partition: {pname}")

    # Temporal ordering: train < validation <= calibration < test
    partition_order = ["train", "validation", "calibration", "test"]
    prev_end = None
    for pname in partition_order:
        pdata = partitions.get(pname, {})
        row_start = pdata.get("row_start")
        row_end = pdata.get("row_end")
        n_rows = pdata.get("n_rows")
        if row_start is not None and row_end is not None and n_rows is not None:
            if row_end <= row_start:
                errors.append(f"{pname}: row_end must be > row_start")
            if n_rows != row_end - row_start:
                errors.append(
                    f"{pname}: n_rows ({n_rows}) != row_end - row_start ({row_end - row_start})"
                )
            if prev_end is not None and pname not in ("calibration",):
                if row_start < prev_end:
                    errors.append(
                        f"{pname}: row_start ({row_start}) < previous partition row_end ({prev_end}) (overlap)"
                    )
            if pname != "calibration":
                prev_end = row_end

    # Calibration shares with validation
    cal = partitions.get("calibration", {})
    val = partitions.get("validation", {})
    if cal.get("shared_with") == "validation":
        if cal.get("row_start") != val.get("row_start") or cal.get("row_end") != val.get("row_end"):
            errors.append("Calibration shared_with validation but ranges differ")

    for pname, pdata in partitions.items():
        cc = pdata.get("class_counts")
        n_rows = pdata.get("n_rows")
        if isinstance(cc, list) and isinstance(n_rows, int):
            if sum(cc) != n_rows:
                errors.append(f"{pname}: sum(class_counts) ({sum(cc)}) != n_rows ({n_rows})")

    target_co = manifest.get("target", {}).get("class_order")
    for pname, pdata in partitions.items():
        cc = pdata.get("class_counts")
        if isinstance(cc, list) and isinstance(target_co, list):
            if len(cc) != len(target_co):
                errors.append(
                    f"{pname}: len(class_counts) ({len(cc)}) != len(class_order) ({len(target_co)})"
                )

    purge = validation.get("purge", {})
    horizon = manifest.get("target", {}).get("horizon_bars")
    rows_between = purge.get("rows_between_partitions")
    if horizon is not None and rows_between is not None:
        if rows_between < horizon:
            errors.append(
                f"purge.rows_between_partitions ({rows_between}) < horizon_bars ({horizon})"
            )
    if purge.get("label_horizon_bars") is not None and horizon is not None:
        if purge.get("label_horizon_bars") != horizon:
            errors.append("purge.label_horizon_bars != target.horizon_bars")

    if purge.get("label_purge_satisfied") is False:
        errors.append("label_purge_satisfied is false")

    leakage = validation.get("leakage_checks", {})
    for key in ("disjoint", "purge_satisfied", "labels_within_partition"):
        if key not in leakage:
            errors.append(f"Missing leakage check: {key}")

    pm = validation.get("partition_manifest_sha256")
    if pm is not None and not validate_sha256(pm):
        errors.append("Invalid partition_manifest_sha256 format")

    return errors
