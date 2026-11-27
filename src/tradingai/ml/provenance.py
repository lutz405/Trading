# Provenance v3: schema validation, JCS canonicalization, and integrity checks

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime
from typing import Any

import rfc8785

# Manifest version dispatch (Fase A)
# ---------------------------------
MANIFEST_VERSION_V3 = '3.0.0'
MANIFEST_VERSION_V4 = '4.0.0'

V4_PENDING_MESSAGE = 'schema_version 4.0.0: implementación pendiente (Fase B)'


class ManifestVersionError(Exception):
    """Typed internal signal: a manifest version cannot be dispatched."""


class ManifestVersionNotImplementedError(ManifestVersionError):
    """4.0.0 is recognized, but its validator belongs to Fase B."""


class ManifestVersionUnsupportedError(ManifestVersionError):
    """Version is missing, malformed or unknown; fail closed."""


def _version_error_message(version: object) -> str:
    prefix = (
        'Missing schema_version'
        if version is None
        else f'Unsupported schema_version {version!r}'
    )
    return (
        f'{prefix}: expected {MANIFEST_VERSION_V3!r} or {MANIFEST_VERSION_V4!r}; '
        'manifest fields (including model_id) cannot be validated'
    )


_MANIFEST_NOT_OBJECT_MESSAGE = (
    'Manifest must be a JSON object: cannot select schema_version; '
    'model_id cannot be validated'
)

# JCS Canonicalization (RFC 8785)
def jcs_canonicalize(obj: Any) -> str:
    """Canonicalize a JSON-compatible object per RFC 8785 JCS.
    Returns the canonical UTF-8 string (no trailing newline).
    Properties are sorted by UTF-16 code units (unsigned).
    Arrays preserve their order.
    Numbers use the rfc8785 library's ECMAScript Number.prototype.toString
    algorithm, which correctly handles -0, NaN, Infinity, scientific notation,
    and integers outside the binary64 safe domain (abs > 2**53 - 1) are rejected
    per policy R8-02.
    Raises rfc8785.FloatDomainError: If NaN or Infinity is encountered.
    """
    return rfc8785.dumps(obj).decode('utf-8')

def jcs_canonical_bytes(obj: Any) -> bytes:
    """Return canonical bytes (UTF-8, no BOM, no trailing newline).
    Equivalent to jcs_canonicalize(obj).encode('utf-8').
    """
    return rfc8785.dumps(obj)

def sha256_bytes(data: bytes) -> str:
    """Compute SHA-256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()

def sha256_canonical(obj: Any) -> str:
    """SHA-256 of JCS canonical bytes (no trailing newline).
    Computes the JCS canonical form of *obj* and returns the SHA-256 hex digest.
    """
    canonical = jcs_canonical_bytes(obj)
    return hashlib.sha256(canonical).hexdigest()

# Strict JSON parsing
class StrictJSONError(Exception):
    """Raised when JSON parsing fails strict validation."""

def parse_json_strict(text: str) -> Any:
    """Parse JSON with strict validation.
    Rejects BOM, trailing content after valid JSON, NaN/Infinity, duplicate keys.
    """
    if text.startswith('\ufeff'):
        raise StrictJSONError('BOM is not allowed')
    def _check_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        for key, _ in pairs:
            if key in seen:
                raise StrictJSONError(f'Duplicate key: {key}')
            seen.add(key)
        return dict(pairs)
    def _reject_non_finite(value: str) -> Any:
        raise StrictJSONError(f'Non-finite value not allowed: {value}')
    try:
        result = json.loads(
            text, parse_constant=_reject_non_finite, object_pairs_hook=_check_duplicates
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise StrictJSONError(str(exc)) from exc
    return result

# Schema validation
def load_manifest_schema() -> dict[str, Any]:
    """Load the manifest v3 JSON Schema from package resources."""
    try:
        import importlib.resources as _ir
        schema = _ir.read_text('tradingai.schemas', 'manifest_v3.json')
        return json.loads(schema)
    except (FileNotFoundError, json.JSONDecodeError):
        _here = os.path.dirname(os.path.abspath(__file__))
        _schema_path = os.path.join(_here, '..', 'schemas', 'manifest_v3.json')
        with open(os.path.normpath(_schema_path), 'r', encoding='utf-8') as f:
            return json.load(f)

MANIFEST_SCHEMA: dict[str, Any] = load_manifest_schema()

def validate_schema(manifest: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    """Validate manifest against JSON Schema. Returns list of errors (empty = valid)."""
    try:
        import jsonschema
        from jsonschema import FormatChecker
    except ImportError:
        return ['jsonschema not available']
    if schema is None:
        schema = MANIFEST_SCHEMA
    validator = jsonschema.Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in validator.iter_errors(manifest):
        errors.append(f'{error.json_path}: {error.message}')
    return errors

# RFC 3339 validation
def validate_rfc3339(value: str, require_utc: bool = False) -> bool:
    """Validate RFC 3339 date-time with real date checking."""
    if not isinstance(value, str):
        return False
    if require_utc and not value.endswith('Z'):
        return False
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?Z?$', value)
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

# Validator functions
def validate_model_id(model_id: object) -> bool:
    """Validate model_id format: ^mdl_[0-7][0-9A-HJKMNP-TV-Z]{26}$"""
    if not isinstance(model_id, str):
        return False
    # ULID first character must be 0-7 (128-bit range constraint)
    return bool(re.match(r'^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$', model_id))

def validate_event_id(event_id: object) -> bool:
    """Validate event_id format: evt_ + ULID (26 chars), first char 0-7."""
    if not isinstance(event_id, str):
        return False
    # ULID first character must be 0-7 (128-bit range constraint)
    return bool(re.match(r'^evt_[0-7][0-9A-HJKMNP-TV-Z]{25}$', event_id))

def validate_sha256(value: object) -> bool:
    """Validate SHA-256 hex string (64 chars)."""
    if not isinstance(value, str):
        return False
    return bool(re.match(r'^[0-9a-f]{64}$', value))

def validate_event(event: dict[str, Any], previous_event: dict[str, Any] | None = None, *, skip_first_event_check: bool = False) -> list[str]:
    """Validate a lifecycle event. Returns list of errors (empty = valid).

    Per S1-R5:
    - event_sha256 is mandatory and its SHA-256 format is validated here.
      The chain-level verifier compares it against the JCS canonical hash
      of the event (excluding the field itself).
    - manifest_sha256 is a manifest-level concept, optional at event level;
      when present it must be a valid SHA-256 hex string (checked below).
    - evidence must be a JSON object or null.

    Malformed inputs are rejected with error strings; the function does not
    raise TypeError/AttributeError for non-object events or non-string fields.
    """
    if not isinstance(event, dict):
        return ['Event must be a JSON object']

    errors: list[str] = []

    # event_sha256 is mandatory per S1-R5
    if 'event_sha256' not in event:
        errors.append('Missing required field: event_sha256')
    else:
        # Validate SHA-256 format
        if not validate_sha256(event['event_sha256']):
            errors.append('Invalid event_sha256 format')

    required_fields = [
        'sequence_number', 'event_id', 'model_id', 'event', 'at',
        'actor', 'evidence',
    ]
    for field in required_fields:
        if field not in event:
            errors.append(f'Missing required field: {field}')

    # Allow event_sha256, previous_event_sha256 and manifest_sha256 as valid
    # event fields.  manifest_sha256 is optional at event level per S1-R5 but,
    # when present, its format is validated above.
    allowed_fields = {
        'event_sha256', 'previous_event_sha256', 'manifest_sha256',
    } | set(required_fields)
    for key in event:
        if key not in allowed_fields:
            errors.append(f'Unknown field in event: {key}')

    if 'event_id' in event and not validate_event_id(event['event_id']):
        errors.append('Invalid event_id format')

    if 'model_id' in event and not validate_model_id(event['model_id']):
        errors.append('Invalid model_id format')

    if 'manifest_sha256' in event and not validate_sha256(event['manifest_sha256']):
        errors.append('Invalid manifest_sha256 format')

    if 'at' in event and not validate_rfc3339(event['at'], require_utc=True):
        errors.append('Invalid at format (must be UTC RFC 3339)')

    if 'previous_event_sha256' in event and not validate_sha256(event['previous_event_sha256']):
        errors.append('Invalid previous_event_sha256 format')

    if 'event' in event and event['event'] not in ('sealed', 'validated', 'approved', 'deprecated', 'revoked'):
        errors.append(f'Invalid event type: {event["event"]}')

    if 'actor' in event and not isinstance(event['actor'], str):
        errors.append('actor must be a string')

    if (
        'evidence' in event
        and event['evidence'] is not None
        and not isinstance(event['evidence'], dict)
    ):
        errors.append('evidence must be an object or null')

    if 'sequence_number' in event:
        sequence = event['sequence_number']
        if not isinstance(sequence, int) or isinstance(sequence, bool):
            errors.append('sequence_number must be an integer')
        elif sequence < 1:
            errors.append('sequence_number must be >= 1')
        elif previous_event is not None:
            # Check sequence gap: must increment by exactly 1 from previous
            # event.  A malformed previous_event must not raise
            # TypeError/AttributeError while computing the expectation.
            if not isinstance(previous_event, dict):
                errors.append('previous_event must be a JSON object')
            else:
                previous_sequence = previous_event.get('sequence_number')
                if not isinstance(previous_sequence, int) or isinstance(previous_sequence, bool):
                    errors.append('previous_event has invalid sequence_number')
                else:
                    expected = previous_sequence + 1
                    if sequence != expected:
                        errors.append(f'Sequence gap: expected {expected}, got {sequence}')

    # First event check (only when not in a chain context)
    # These checks apply only to the first event of each model_id in a chain.
    # When skip_first_event_check is True, these are intentionally omitted
    # so that subsequent events in a chain can be validated independently.
    if not skip_first_event_check and previous_event is None and 'sequence_number' in event:
        if event['sequence_number'] != 1:
            errors.append('First event must have sequence_number == 1')
        if event.get('previous_event_sha256') != '0' * 64:
            errors.append('First event must have previous_event_sha256 == \'0\'*64')

    return errors

def verify_event_hash(event: dict[str, Any], expected_hash: str) -> bool:
    """Verify that event_sha256 matches the canonical hash of the event (excluding event_sha256 itself)."""
    event_copy = {k: v for k, v in event.items() if k != 'event_sha256'}
    computed = sha256_canonical(event_copy)
    return computed == expected_hash

def validate_calibrator_binding(manifest: dict[str, Any]) -> list[str]:
    """Validate that calibrator is bound to the correct base model."""
    errors: list[str] = []
    calibration = manifest.get('calibration', {})
    base_model_id = calibration.get('base_model_id')
    model_id = manifest.get('model_id')
    if calibration.get('mode') == 'in_pipeline' and base_model_id != model_id:
        errors.append(f'Calibrator base_model_id ({base_model_id}) != model_id ({model_id}) in in_pipeline mode')
    base_hashes = calibration.get('base_artifact_sha256', {})
    artifacts = {a['role']: a['sha256'] for a in manifest.get('artifacts', [])}
    if 'rf' in base_hashes and 'rf' in artifacts and base_hashes['rf'] != artifacts['rf']:
        errors.append('Calibrator base rf hash != manifest rf artifact hash')
    if 'xgb' in base_hashes and 'xgb' in artifacts and base_hashes['xgb'] != artifacts['xgb']:
        errors.append('Calibrator base xgb hash != manifest xgb artifact hash')
    if calibration.get('artifact_sha256') and 'calibrator' in artifacts:
        if calibration['artifact_sha256'] != artifacts['calibrator']:
            errors.append('Calibrator artifact_sha256 != manifest calibrator artifact hash')
    if calibration.get('classes') != manifest.get('target', {}).get('classes'):
        errors.append('Calibration classes != target classes')
    if calibration.get('class_order') != manifest.get('target', {}).get('class_order'):
        errors.append('Calibration class_order != target class_order')
    if calibration.get('fit_partition') == 'test':
        errors.append('Calibration fit_partition cannot be \'test\'')
    if calibration.get('n_calibrators') != len(calibration.get('classes', [])):
        errors.append('n_calibrators != len(classes)')
    return errors

def validate_partition_consistency(manifest: dict[str, Any]) -> list[str]:
    """Validate partition consistency (row counts, class counts, purge, temporal ordering)."""
    errors: list[str] = []
    validation = manifest.get('validation', {})
    partitions = validation.get('partitions', {})
    for pname in ('train', 'validation', 'calibration', 'test'):
        if pname not in partitions:
            errors.append(f'Missing partition: {pname}')
    partition_order = ['train', 'validation', 'calibration', 'test']
    prev_end = None
    for pname in partition_order:
        pdata = partitions.get(pname, {})
        row_start = pdata.get('row_start')
        row_end = pdata.get('row_end')
        n_rows = pdata.get('n_rows')
        if row_start is not None and row_end is not None and n_rows is not None:
            if row_end <= row_start:
                errors.append(f'{pname}: row_end must be > row_start')
            if n_rows != row_end - row_start:
                errors.append(f'{pname}: n_rows ({n_rows}) != row_end - row_start ({row_end - row_start})')
            if prev_end is not None and pname not in ('calibration',):
                if row_start < prev_end:
                    errors.append(f'{pname}: row_start ({row_start}) < previous partition row_end ({prev_end}) (overlap)')
            if pname != 'calibration':
                prev_end = row_end
    cal = partitions.get('calibration', {})
    val = partitions.get('validation', {})
    if cal.get('shared_with') == 'validation':
        if cal.get('row_start') != val.get('row_start') or cal.get('row_end') != val.get('row_end'):
            errors.append('Calibration shared_with validation but ranges differ')
    for pname, pdata in partitions.items():
        cc = pdata.get('class_counts')
        n_rows = pdata.get('n_rows')
        if isinstance(cc, list) and isinstance(n_rows, int) and sum(cc) != n_rows:
            errors.append(f'{pname}: sum(class_counts) ({sum(cc)}) != n_rows ({n_rows})')
    target_co = manifest.get('target', {}).get('class_order')
    for pname, pdata in partitions.items():
        cc = pdata.get('class_counts')
        if isinstance(cc, list) and isinstance(target_co, list):
            if len(cc) != len(target_co):
                errors.append(f'{pname}: len(class_counts) ({len(cc)}) != len(class_order) ({len(target_co)})')
    purge = validation.get('purge', {})
    horizon = manifest.get('target', {}).get('horizon_bars')
    rows_between = purge.get('rows_between_partitions')
    if horizon is not None and rows_between is not None and rows_between < horizon:
        errors.append(f'purge.rows_between_partitions ({rows_between}) < horizon_bars ({horizon})')
    if purge.get('label_horizon_bars') is not None and horizon is not None:
        if purge.get('label_horizon_bars') != horizon:
            errors.append('purge.label_horizon_bars != target.horizon_bars')
    if purge.get('label_purge_satisfied') is False:
        errors.append('label_purge_satisfied is false')
    leakage = validation.get('leakage_checks', {})
    for key in ('disjoint', 'purge_satisfied', 'labels_within_partition'):
        if key not in leakage:
            errors.append(f'Missing leakage check: {key}')
    pm = validation.get('partition_manifest_sha256')
    if pm is not None and not validate_sha256(pm):
        errors.append('Invalid partition_manifest_sha256 format')
    return errors

# validate_event_chain - R7 + R9-03
def validate_event_chain(events: list[dict[str, Any]]) -> list[str]:
    """Validate a complete lifecycle event chain per R7.
    Rules (strict, fail-closed):
    - Events are processed in physical insertion order (no reordering).
    - Sequences are independent per model_id.
    - First event of each model_id has sequence_number == 1 and
      previous_event_sha256 == "0" * 64.
    - Each subsequent event increments sequence_number by exactly 1
      and references the prior event's event_sha256.
    - event_id must be unique within each model_id.
    - event_sha256 must match the JCS canonical hash of the event
      (excluding the field itself). This is mandatory for every event.
    - Different model_id groups maintain separate chains.
    - No event may belong to a different model_id chain than previous.
    - Unknown/extra fields in events are rejected.
    - Event types must be from the allowed set.
    The order of events in the input list is the authoritative physical
    insertion order. Events are NOT sorted by timestamp or sequence_number.
    Returns a list of error strings (empty = valid).
    """
    errors: list[str] = []
    if not isinstance(events, list):
        return ['Event chain must be a list of events']
    model_state: dict[str, dict[str, Any]] = {}
    for idx, event in enumerate(events):
        # A chain element must be a JSON object.  Reject anything else without
        # attempting attribute access, and keep the physical order intact.
        if not isinstance(event, dict):
            errors.append(f'Event {idx}: event must be a JSON object')
            continue
        # Individual field validation is centralized in validate_event().
        # skip_first_event_check=True avoids rejecting continuation events
        # while the chain-specific first-event rules are applied below.
        for e in validate_event(event, skip_first_event_check=True):
            errors.append(f'Event {idx}: {e}')
        model_id = event.get('model_id')
        sequence = event.get('sequence_number')
        eid = event.get('event_id')
        declared_hash = event.get('event_sha256')
        # validate_event() already reports a missing or invalid model_id.
        # Without a string model_id the event cannot be assigned to a chain.
        if not isinstance(model_id, str):
            continue
        state = model_state.setdefault(
            model_id,
            {'next_sequence': 1, 'prior_computed_hash': None, 'seen_ids': set()},
        )
        # Chain-specific sequence continuity.  Physical insertion order is
        # authoritative; events are never sorted or repaired.
        if isinstance(sequence, int) and not isinstance(sequence, bool):
            expected = state['next_sequence']
            if sequence != expected:
                if expected == 1:
                    errors.append(
                        f'Event {idx} ({model_id}): first event must have '
                        f'sequence_number == 1, got {sequence}'
                    )
                else:
                    errors.append(
                        f'Event {idx} ({model_id}): sequence_number must be '
                        f'{expected}, got {sequence}'
                    )
            if expected == 1:
                if event.get('previous_event_sha256') != '0' * 64:
                    errors.append(
                        f'Event {idx} ({model_id}): first event must have '
                        f'previous_event_sha256 == \'0\'*64'
                    )
            elif event.get('previous_event_sha256') != state['prior_computed_hash']:
                errors.append(
                    f'Event {idx} ({model_id}): previous_event_sha256 does not '
                    f'match prior event\'s computed event_sha256'
                )
            # Advance even when the sequence is wrong so later events are
            # checked against the physical chain rather than a repaired one.
            state['next_sequence'] = sequence + 1
        # Compute the JCS hash with a controlled error path.  Malformed or
        # unsupported values must become validation errors, not tracebacks.
        try:
            event_copy = {k: v for k, v in event.items() if k != 'event_sha256'}
            computed_hash = sha256_canonical(event_copy)
        except (AttributeError, OverflowError, RecursionError, TypeError, ValueError) as exc:
            errors.append(f'Event {idx} ({model_id}): error computing JCS hash: {exc}')
            computed_hash = None
        # Missing/format errors for event_sha256 are reported by
        # validate_event(); only compare when a string hash was declared.
        if (
            computed_hash is not None
            and isinstance(declared_hash, str)
            and computed_hash != declared_hash
        ):
            errors.append(
                f'Event {idx} ({model_id}): event_sha256 '
                f'\'{declared_hash[:16]}...\' does not match computed JCS hash '
                f'\'{computed_hash[:16]}...\'.'
            )
        # Duplicate IDs are tracked per model.  Non-string IDs were already
        # rejected by validate_event() and must not reach the set.
        if isinstance(eid, str):
            if eid in state['seen_ids']:
                errors.append(f'Event {idx} ({model_id}): duplicate event_id \'{eid}\'')
            state['seen_ids'].add(eid)
        if computed_hash is not None:
            state['prior_computed_hash'] = computed_hash
    return errors

# Dependencies and packaging (documented separately)
# ----------------------------------------------------------
def _dispatch_manifest_version(manifest: dict[str, Any]) -> str:
    """Select the validator by declared schema_version; never infer a version."""
    version = manifest.get('schema_version')
    if version == MANIFEST_VERSION_V3:
        return MANIFEST_VERSION_V3
    if version == MANIFEST_VERSION_V4:
        raise ManifestVersionNotImplementedError(V4_PENDING_MESSAGE)
    raise ManifestVersionUnsupportedError(_version_error_message(version))


def _validate_manifest_v3(manifest: dict[str, Any]) -> list[str]:
    """Frozen 3.0.0 validator body: historical checks and messages."""
    errors: list[str] = []

    errors.extend(validate_schema(manifest))

    if 'model_id' in manifest and not validate_model_id(manifest['model_id']):
        errors.append('Invalid model_id format')

    if 'created_at' in manifest and not validate_rfc3339(manifest['created_at'], require_utc=True):
        errors.append('Invalid created_at format (must be UTC RFC 3339)')
    if 'sealed_at' in manifest and not validate_rfc3339(manifest['sealed_at'], require_utc=True):
        errors.append('Invalid sealed_at format (must be UTC RFC 3339)')

    if 'run_fingerprint' in manifest and not validate_sha256(manifest['run_fingerprint']):
        errors.append('Invalid run_fingerprint format')

    # Feature count consistency (R7)
    features = manifest.get('features', {})
    ordered = features.get('ordered', [])
    count = features.get('count', 0)
    if isinstance(ordered, list) and isinstance(count, (int, float)) and len(ordered) != count:
        errors.append(
            f'Features count mismatch: len(ordered) ({len(ordered)}) != count ({count})'
        )

    errors.extend(validate_calibrator_binding(manifest))
    errors.extend(validate_partition_consistency(manifest))

    return errors


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate a manifest dict through explicit schema_version dispatch.

    - '3.0.0': frozen historical validator, with unchanged checks and messages.
    - '4.0.0': typed internal error converted to the historical list[str]
      contract; Fase B pending. No partial validation, no 3.0.0 defaults and
      no call to the 3.0.0 validator.
    - missing/unknown/malformed version: explicit fail-closed rejection.
    Public name, signature and return type are preserved.
    """
    if not isinstance(manifest, dict):
        return [_MANIFEST_NOT_OBJECT_MESSAGE]
    try:
        version = _dispatch_manifest_version(manifest)
    except ManifestVersionError as exc:
        return [str(exc)]
    if version == MANIFEST_VERSION_V3:
        return _validate_manifest_v3(manifest)
    # Defensive only: the dispatcher never returns V4 without raising.
    return [V4_PENDING_MESSAGE]

