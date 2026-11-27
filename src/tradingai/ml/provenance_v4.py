"""Provenance 4.0.0 structural validation (Fase B).

Scope: JSON Schema structure, declared types/patterns, safe-integer limits,
timestamp format and closed evidence objects.  This module does NOT compute
JCS/fingerprints (Fase C), does NOT check source gaps or calibration equivalence
(Fase D), does NOT validate event chains (Fase E) and does NOT verify signatures
or sidecars cryptographically (Fase F).  All public functions return list[str].
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from collections.abc import Iterator
from datetime import datetime
from typing import Any

import jsonschema
from jsonschema import FormatChecker

MANIFEST_SCHEMA_V4_FILENAME = 'manifest_v4.json'

MAX_SAFE_INTEGER = 9007199254740991

_SHA256_RE = re.compile(r'^[0-9a-f]{64}$')
_ULID_RE = re.compile(r'^[0-7][0-9A-HJKMNP-TV-Z]{25}$')
_MODEL_ID_RE = re.compile(r'^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$')
_EVENT_ID_RE = re.compile(r'^evt_[0-7][0-9A-HJKMNP-TV-Z]{25}$')
_SIDECAR_ID_RE = re.compile(r'^sig_[0-7][0-9A-HJKMNP-TV-Z]{25}$')
_REASON_CODE_RE = re.compile(r'^[a-z][a-z0-9_]{0,63}$')
_ACTOR_RE = re.compile(r'^(human|service):[A-Za-z0-9][A-Za-z0-9._-]{0,119}$')
_TIMESTAMP_RE = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})'
    r'(?:\.(\d{1,9}))?(Z|[+-]\d{2}:\d{2})$'
)

EVIDENCE_FIELDS_V4: dict[str, frozenset[str] | None] = {
    'sealed': None,
    'validated': frozenset({'report_sha256', 'signature_sidecar_id'}),
    'approved': frozenset({'approval_ref', 'signature_sidecar_id'}),
    'deprecated': frozenset({'reason_code', 'replacement_model_id'}),
    'revoked': frozenset({'reason_code', 'incident_ref'}),
    'rejected': frozenset({'reason_code', 'report_sha256', 'signature_sidecar_id'}),
}

_TIMESTAMP_PATHS = (
    '$.created_at',
    '$.sealed_at',
    '$.data.time_range.start',
    '$.data.time_range.end',
    '$.validation.evaluation.evaluated_at',
    '$.validation.partitions.train.time_start',
    '$.validation.partitions.train.time_end',
    '$.validation.partitions.validation.time_start',
    '$.validation.partitions.validation.time_end',
    '$.validation.partitions.calibration.time_start',
    '$.validation.partitions.calibration.time_end',
    '$.validation.partitions.test.time_start',
    '$.validation.partitions.test.time_end',
)

_MISSING = object()


def load_manifest_schema_v4() -> dict[str, Any]:
    """Load the definitive 4.0.0 JSON Schema from package resources."""
    try:
        import importlib.resources as _ir

        return json.loads(_ir.read_text('tradingai.schemas', MANIFEST_SCHEMA_V4_FILENAME))
    except (FileNotFoundError, json.JSONDecodeError):
        _here = os.path.dirname(os.path.abspath(__file__))
        _path = os.path.join(_here, '..', 'schemas', MANIFEST_SCHEMA_V4_FILENAME)
        with open(os.path.normpath(_path), 'r', encoding='utf-8') as handle:
            return json.load(handle)


MANIFEST_SCHEMA_V4: dict[str, Any] = load_manifest_schema_v4()


def validate_schema_v4(
    manifest: dict[str, Any], schema: dict[str, Any] | None = None
) -> list[str]:
    """Validate against the 4.0.0 schema. Returns formatted errors (empty = valid)."""
    try:
        validator = jsonschema.Draft202012Validator(
            schema if schema is not None else MANIFEST_SCHEMA_V4,
            format_checker=FormatChecker(),
        )
    except ImportError:
        return ['jsonschema not available']
    return [f'{error.json_path}: {error.message}' for error in validator.iter_errors(manifest)]


def validate_sha256_v4(value: object) -> bool:
    return isinstance(value, str) and bool(_SHA256_RE.match(value))


def validate_ulid_v4(value: object) -> bool:
    """128-bit ULID body: Crockford Base32 with first character in 0-7."""
    return isinstance(value, str) and bool(_ULID_RE.match(value))


def validate_model_id_v4(value: object) -> bool:
    return isinstance(value, str) and bool(_MODEL_ID_RE.match(value))


def validate_event_id_v4(value: object) -> bool:
    return isinstance(value, str) and bool(_EVENT_ID_RE.match(value))


def validate_sidecar_id_v4(value: object) -> bool:
    return isinstance(value, str) and bool(_SIDECAR_ID_RE.match(value))


def validate_reason_code_v4(value: object) -> bool:
    """DEC-01: syntax only; no closed catalogue is implied."""
    return isinstance(value, str) and bool(_REASON_CODE_RE.match(value))


def validate_actor_v4(value: object) -> bool:
    """DEC-02: declared namespace only; no identity or authority is inferred."""
    return isinstance(value, str) and bool(_ACTOR_RE.match(value))


def validate_timestamp_v4(value: object) -> bool:
    """Structural RFC 3339 check with explicit zone, <= 9 fractional digits.

    Normalisation to UTC with nine fractional digits belongs to Fase C; this
    function only rejects forms that the 4.0.0 contract forbids.
    """
    if not isinstance(value, str):
        return False
    match = _TIMESTAMP_RE.match(value)
    if match is None:
        return False
    if match.group(8) == '-00:00':
        return False
    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    hour, minute, second = int(match.group(4)), int(match.group(5)), int(match.group(6))
    if hour > 23 or minute > 59 or second > 59:
        return False
    offset = match.group(8)
    if offset != 'Z':
        offset_hour, offset_minute = int(offset[1:3]), int(offset[4:6])
        if offset_hour > 23 or offset_minute > 59:
            return False
    try:
        datetime(year, month, day, hour, minute, second)
    except ValueError:
        return False
    return True


def _iter_safe_integer_candidates(obj: Any, path: str = '$') -> Iterator[tuple[str, int]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from _iter_safe_integer_candidates(value, f'{path}.{key}')
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from _iter_safe_integer_candidates(value, f'{path}[{index}]')
    elif isinstance(obj, int) and not isinstance(obj, bool):
        yield path, obj


def validate_safe_integers_v4(manifest: dict[str, Any]) -> list[str]:
    """§9.1: every JSON integer must satisfy abs(n) <= 2**53 - 1."""
    return [
        f'{path}: integer outside JCS safe range (+/-{MAX_SAFE_INTEGER})'
        for path, value in _iter_safe_integer_candidates(manifest)
        if abs(value) > MAX_SAFE_INTEGER
    ]


def _get_path(obj: Any, path: str) -> Any:
    current = obj
    for token in path.lstrip('$').lstrip('.').split('.'):
        if not isinstance(current, dict) or token not in current:
            return _MISSING
        current = current[token]
    return current


def _valid_opaque_ref(value: object) -> bool:
    """approval_ref / incident_ref: UTF-8 string, 1-256 chars, no controls."""
    if not isinstance(value, str) or not 1 <= len(value) <= 256:
        return False
    if value.strip() != value or not value.strip():
        return False
    return not any(unicodedata.category(char) == 'Cc' for char in value)


def validate_evidence_v4(
    event_type: object,
    evidence: object,
    *,
    model_id: object = None,
) -> list[str]:
    """DEC-01/02/07: closed evidence object per event type; syntax only."""
    if not isinstance(event_type, str) or event_type not in EVIDENCE_FIELDS_V4:
        return [f'evidence: unsupported event type {event_type!r}']
    expected = EVIDENCE_FIELDS_V4[event_type]
    if expected is None:
        return [] if evidence is None else ['evidence: sealed requires null']
    if not isinstance(evidence, dict):
        return ['evidence: must be an object']

    errors: list[str] = []
    for key in evidence:
        if key not in expected:
            errors.append(f'evidence: unknown field {key}')
    for key in sorted(expected):
        if key not in evidence:
            errors.append(f'evidence: missing required field {key}')
    for key, value in evidence.items():
        if key not in expected:
            continue
        if key == 'reason_code' and not validate_reason_code_v4(value):
            errors.append('evidence.reason_code: invalid syntax')
        elif key in ('report_sha256',) and not validate_sha256_v4(value):
            errors.append(f'evidence.{key}: invalid SHA-256')
        elif key == 'signature_sidecar_id' and not validate_sidecar_id_v4(value):
            errors.append('evidence.signature_sidecar_id: invalid sig_<ULID>')
        elif key == 'replacement_model_id':
            if not validate_model_id_v4(value):
                errors.append('evidence.replacement_model_id: invalid model ID')
            elif model_id is not None and value == model_id:
                errors.append('evidence.replacement_model_id: must differ from model_id')
        elif key in ('approval_ref', 'incident_ref') and not _valid_opaque_ref(value):
            errors.append(f'evidence.{key}: invalid opaque reference')
    return errors


def _validate_calibration_binding_v4(manifest: dict[str, Any]) -> list[str]:
    """§4: declared base model/hash relations; no cryptographic verification."""
    errors: list[str] = []
    calibration = manifest.get('calibration')
    if not isinstance(calibration, dict):
        return errors
    mode = calibration.get('mode')
    model_id = manifest.get('model_id')
    base_model_id = calibration.get('base_model_id')
    if (
        mode in ('in_pipeline', 'external_run')
        and isinstance(model_id, str)
        and isinstance(base_model_id, str)
    ):
        if mode == 'in_pipeline' and base_model_id != model_id:
            errors.append('$.calibration.base_model_id: must equal $.model_id in in_pipeline mode')
        elif mode == 'external_run' and base_model_id == model_id:
            errors.append('$.calibration.base_model_id: must differ from $.model_id in external_run mode')

    artifacts = manifest.get('artifacts')
    if isinstance(artifacts, list):
        hashes_by_role: dict[str, Any] = {}
        for artifact in artifacts:
            if isinstance(artifact, dict) and isinstance(artifact.get('role'), str):
                hashes_by_role[artifact['role']] = artifact.get('sha256')
        base_hashes = calibration.get('base_artifact_sha256')
        if isinstance(base_hashes, dict):
            for role in ('rf', 'xgb'):
                if (
                    role in base_hashes
                    and role in hashes_by_role
                    and base_hashes[role] != hashes_by_role[role]
                ):
                    errors.append(
                        f'$.calibration.base_artifact_sha256.{role}: '
                        f'does not match artifacts[{role}].sha256'
                    )
    return errors


def validate_manifest_v4(manifest: object) -> list[str]:
    """Full Fase B validation of a 4.0.0 manifest. Never mutates the input."""
    if not isinstance(manifest, dict):
        return ['Manifest must be a JSON object']

    errors = validate_schema_v4(manifest)
    errors.extend(validate_safe_integers_v4(manifest))
    for path in _TIMESTAMP_PATHS:
        value = _get_path(manifest, path)
        if value is not _MISSING and not validate_timestamp_v4(value):
            errors.append(f'{path}: invalid RFC 3339 timestamp with explicit zone')
    errors.extend(_validate_calibration_binding_v4(manifest))
    return errors
