"""Provenance v3: schema validation, JCS canonicalization, and integrity checks.

Implements S1 of AUD-04B: JSON Schema v3, RFC 8785 JCS canonicalization,
and pure validators for manifest integrity and consistency.

No model loading, no deserialization, no training.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any

# ---------------------------------------------------------------------------
# JCS Canonicalization (RFC 8785)
# ---------------------------------------------------------------------------


def _jcs_sort_key(s: str) -> list[int]:
    """RFC 8785 §3.2.3: sort by UTF-16 code units (unsigned)."""
    return [ord(c) for c in s.encode("utf-16-le").decode("utf-16-le")]


def jcs_canonicalize(obj: Any) -> str:
    """Canonicalize a JSON-compatible object per RFC 8785 JCS.

    Returns the canonical UTF-8 string (no trailing newline).

    Properties are sorted by UTF-16 code units (unsigned).
    Arrays preserve their order.
    Numbers use shortest round-trip representation.
    """
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise ValueError("NaN and Infinity are not allowed in JCS")
        return repr(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if isinstance(obj, list):
        return "[" + ",".join(jcs_canonicalize(item) for item in obj) + "]"
    if isinstance(obj, dict):
        sorted_keys = sorted(obj.keys(), key=lambda k: [ord(c) for c in k.encode("utf-16-le").decode("utf-16-le")])
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
    """Parse JSON with strict validation.

    Rejects:
    - BOM
    - Trailing content after valid JSON
    - NaN/Infinity
    - Duplicate keys
    """
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
        result = json.loads(text, parse_constant=_reject_non_finite, object_pairs_hook=_check_duplicates)
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
    except ImportError:
        return ["jsonschema not available"]

    if schema is None:
        schema = MANIFEST_SCHEMA

    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for error in validator.iter_errors(manifest):
        errors.append(f"{error.json_path}: {error.message}")
    return errors


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


def validate_rfc3339(value: str) -> bool:
    """Basic RFC 3339 UTC validation."""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$", value))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate a manifest dict. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    errors.extend(validate_schema(manifest))

    if "model_id" in manifest and not validate_model_id(manifest["model_id"]):
        errors.append("Invalid model_id format")

    if "created_at" in manifest and not validate_rfc3339(manifest["created_at"]):
        errors.append("Invalid created_at format")

    if "sealed_at" in manifest and not validate_rfc3339(manifest["sealed_at"]):
        errors.append("Invalid sealed_at format")

    if "run_fingerprint" in manifest and not validate_sha256(manifest["run_fingerprint"]):
        errors.append("Invalid run_fingerprint format")

    return errors


def validate_event(event: dict[str, Any], previous_event: dict[str, Any] | None = None) -> list[str]:
    """Validate a lifecycle event. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    required_fields = [
        "sequence_number", "previous_event_sha256", "event_id",
        "model_id", "event", "at", "manifest_sha256", "actor", "evidence",
    ]
    for field in required_fields:
        if field not in event:
            errors.append(f"Missing required field: {field}")

    if "event_id" in event and not validate_event_id(event["event_id"]):
        errors.append("Invalid event_id format")

    if "model_id" in event and not validate_model_id(event["model_id"]):
        errors.append("Invalid model_id format")

    if "manifest_sha256" in event and not validate_sha256(event["manifest_sha256"]):
        errors.append("Invalid manifest_sha256 format")

    if "at" in event and not validate_rfc3339(event["at"]):
        errors.append("Invalid at format")

    if "event" in event and event["event"] not in ("sealed", "validated", "approved", "deprecated", "revoked"):
        errors.append(f"Invalid event type: {event['event']}")

    if "sequence_number" in event:
        if not isinstance(event["sequence_number"], int) or isinstance(event["sequence_number"], bool):
            errors.append("sequence_number must be an integer")
        elif event["sequence_number"] < 1:
            errors.append("sequence_number must be >= 1")

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
    """Validate partition consistency (row counts, class counts, purge)."""
    errors: list[str] = []

    validation = manifest.get("validation", {})
    partitions = validation.get("partitions", {})

    for pname in ("train", "validation", "calibration", "test"):
        if pname not in partitions:
            errors.append(f"Missing partition: {pname}")

    for pname, pdata in partitions.items():
        row_start = pdata.get("row_start")
        row_end = pdata.get("row_end")
        n_rows = pdata.get("n_rows")
        if row_start is not None and row_end is not None and n_rows is not None:
            if row_end <= row_start:
                errors.append(f"{pname}: row_end must be > row_start")
            if n_rows != row_end - row_start:
                errors.append(f"{pname}: n_rows ({n_rows}) != row_end - row_start ({row_end - row_start})")

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
                errors.append(f"{pname}: len(class_counts) ({len(cc)}) != len(class_order) ({len(target_co)})")

    purge = validation.get("purge", {})
    horizon = manifest.get("target", {}).get("horizon_bars")
    rows_between = purge.get("rows_between_partitions")
    if horizon is not None and rows_between is not None:
        if rows_between < horizon:
            errors.append(f"purge.rows_between_partitions ({rows_between}) < horizon_bars ({horizon})")
    if purge.get("label_horizon_bars") is not None and horizon is not None:
        if purge.get("label_horizon_bars") != horizon:
            errors.append("purge.label_horizon_bars != target.horizon_bars")

    leakage = validation.get("leakage_checks", {})
    for key in ("disjoint", "purge_satisfied", "labels_within_partition"):
        if key not in leakage:
            errors.append(f"Missing leakage check: {key}")

    return errors