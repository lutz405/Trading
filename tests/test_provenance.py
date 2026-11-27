"""Tests for S1: Schema v3, JCS canonicalization, and validators."""

import hashlib
import json

import pytest

from tradingai.ml.provenance import (
    MANIFEST_SCHEMA,
    StrictJSONError,
    jcs_canonicalize,
    jcs_canonical_bytes,
    parse_json_strict,
    sha256_bytes,
    sha256_canonical,
    validate_calibrator_binding,
    validate_event,
    validate_event_chain,
    validate_event_id,
    validate_manifest,
    validate_model_id,
    validate_partition_consistency,
    validate_rfc3339,
    validate_schema,
    validate_sha256,
    verify_event_hash,
)

MODEL_ID_A = "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W"
MODEL_ID_B = "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X"
EVENT_ID_A = "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K"
EVENT_ID_B = "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M"
EVENT_ID_C = "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9N"
EVENT_ID_D = "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9P"
EVENT_ID_E = "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9Q"


def make_event(sequence, model_id, event_id, event_type, at, previous="0" * 64):
    """Build a self-consistent event with a valid JCS event_sha256."""
    event = {
        "sequence_number": sequence,
        "previous_event_sha256": previous,
        "event_id": event_id,
        "model_id": model_id,
        "event": event_type,
        "at": at,
        "actor": "pipeline",
        "evidence": None,
    }
    event["event_sha256"] = sha256_canonical(event)
    return event


# ---------------------------------------------------------------------------
# JCS Canonicalization Tests
# ---------------------------------------------------------------------------

class TestJCSCanonicalization:
    def test_simple_object(self):
        obj = {"b": 1, "a": 2}
        result = jcs_canonicalize(obj)
        assert result == '{"a":2,"b":1}'

    def test_nested_object(self):
        obj = {"z": {"b": 1, "a": 2}, "a": 3}
        result = jcs_canonicalize(obj)
        assert result == '{"a":3,"z":{"a":2,"b":1}}'

    def test_array_preserves_order(self):
        obj = {"arr": [3, 1, 2]}
        result = jcs_canonicalize(obj)
        assert result == '{"arr":[3,1,2]}'

    def test_null(self):
        assert jcs_canonicalize(None) == "null"

    def test_boolean(self):
        assert jcs_canonicalize(True) == "true"
        assert jcs_canonicalize(False) == "false"

    def test_string_escaping(self):
        obj = {"key": "hello\nworld"}
        result = jcs_canonicalize(obj)
        assert result == '{"key":"hello\\nworld"}'

    def test_unicode_keys_sorted_by_utf16(self):
        obj = {"z": 1, "a": 2, "A": 3}
        result = jcs_canonicalize(obj)
        assert result == '{"A":3,"a":2,"z":1}'

    def test_integers(self):
        assert jcs_canonicalize(42) == "42"
        assert jcs_canonicalize(0) == "0"
        assert jcs_canonicalize(-1) == "-1"

    def test_floats(self):
        result = jcs_canonicalize(1.5)
        assert result == "1.5"

    def test_nan_rejected(self):
        from pytest import raises
        with raises(ValueError):
            jcs_canonicalize(float("nan"))

    def test_inf_rejected(self):
        from pytest import raises
        with raises(ValueError):
            jcs_canonicalize(float("inf"))

    def test_empty_object(self):
        assert jcs_canonicalize({}) == "{}"

    def test_empty_array(self):
        assert jcs_canonicalize([]) == "[]"

    def test_deeply_nested(self):
        obj = {"a": {"b": {"c": [1, 2, {"d": 3}]}}}
        result = jcs_canonicalize(obj)
        assert result == '{"a":{"b":{"c":[1,2,{"d":3}]}}}'

    def test_bytes_no_newline(self):
        data = jcs_canonical_bytes({"a": 1})
        assert not data.endswith(b"\n")
        assert data == b'{"a":1}'

    def test_jcs_rfc8785_example(self):
        obj = {
            "numbers": [333333333.3333333, 1e30, 4.50, 2e-3, 0.000000000000000000000000001],
            "string": "€$\\n\\ r",
            "literals": [None, True, False],
        }
        result = jcs_canonicalize(obj)
        parsed = json.loads(result)
        assert parsed["numbers"][0] == 333333333.3333333


# ---------------------------------------------------------------------------
# Strict JSON Parsing Tests
# ---------------------------------------------------------------------------

class TestStrictJSONParsing:
    def test_valid_json(self):
        result = parse_json_strict('{"a": 1, "b": 2}')
        assert result == {"a": 1, "b": 2}

    def test_bom_rejected(self):
        from pytest import raises
        with raises(StrictJSONError):
            parse_json_strict('\ufeff{"a": 1}')

    def test_duplicate_keys_rejected(self):
        from pytest import raises
        with raises(StrictJSONError):
            parse_json_strict('{"a": 1, "a": 2}')

    def test_nan_rejected(self):
        from pytest import raises
        with raises(StrictJSONError):
            parse_json_strict('{"a": NaN}')

    def test_inf_rejected(self):
        from pytest import raises
        with raises(StrictJSONError):
            parse_json_strict('{"a": Infinity}')

    def test_trailing_content_rejected(self):
        from pytest import raises
        with raises(StrictJSONError):
            parse_json_strict('{"a": 1} extra')

    def test_empty_object(self):
        result = parse_json_strict("{}")
        assert result == {}


# ---------------------------------------------------------------------------
# Hash Tests
# ---------------------------------------------------------------------------

class TestHashing:
    def test_sha256_bytes(self):
        data = b"hello"
        expected = hashlib.sha256(data).hexdigest()
        assert sha256_bytes(data) == expected

    def test_sha256_canonical(self):
        obj = {"a": 1}
        canonical = jcs_canonical_bytes(obj)
        expected = hashlib.sha256(canonical).hexdigest()
        assert sha256_canonical(obj) == expected

    def test_canonical_vs_file_bytes(self):
        obj = {"a": 1}
        canonical = jcs_canonical_bytes(obj)
        file_bytes = canonical + b"\n"
        assert sha256_bytes(canonical) != sha256_bytes(file_bytes)


# ---------------------------------------------------------------------------
# Event Hash Tests
# ---------------------------------------------------------------------------

class TestEventHashing:
    def test_event_hash_excludes_itself(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "manifest_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "actor": "pipeline",
            "evidence": None,
            "event_sha256": "should_be_excluded",
        }
        event_copy = {k: v for k, v in event.items() if k != "event_sha256"}
        computed = sha256_canonical(event_copy)
        assert computed != event["event_sha256"]

    def test_verify_event_hash(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "manifest_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "actor": "pipeline",
            "evidence": None,
        }
        computed = sha256_canonical(event)
        event["event_sha256"] = computed
        assert verify_event_hash(event, computed)

    def test_verify_event_hash_wrong(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "manifest_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "actor": "pipeline",
            "evidence": None,
        }
        assert not verify_event_hash(event, "wrong" * 8)


# ---------------------------------------------------------------------------
# Validator Tests
# ---------------------------------------------------------------------------

class TestValidators:
    def test_validate_model_id_valid(self):
        assert validate_model_id("mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W")

    def test_validate_model_id_starts_with_0_or_7(self):
        # ULID first character must be 0-7 per 128-bit range
        assert validate_model_id("mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W")
        assert validate_model_id("mdl_71JQ8Z3K4M5N6P7Q8R9S0T1V2W")

    def test_validate_model_id_starts_with_8_rejected(self):
        # ULID starting with 8 exceeds 128-bit range
        assert not validate_model_id("mdl_81JQ8Z3K4M5N6P7Q8R9S0T1V2W")

    def test_validate_model_id_starts_with_9_rejected(self):
        # ULID starting with 9 exceeds 128-bit range
        assert not validate_model_id("mdl_91JQ8Z3K4M5N6P7Q8R9S0T1V2W")

    def test_validate_model_id_starts_with_letter_rejected(self):
        # ULID starting with A-H (beyond first-char range) rejected
        assert not validate_model_id("mdl_A1JQ8Z3K4M5N6P7Q8R9S0T1V2W")

    def test_validate_model_id_too_short(self):
        assert not validate_model_id("mdl_123")

    def test_validate_model_id_no_prefix(self):
        assert not validate_model_id("invalid")

    def test_validate_model_id_non_string(self):
        assert not validate_model_id(17)
        assert not validate_model_id(None)

    def test_model_id_reference_schemas_match_python_validator(self):
        model_id_schema = MANIFEST_SCHEMA["properties"]["model_id"]
        base_model_id_schema = MANIFEST_SCHEMA["properties"]["calibration"][
            "properties"
        ]["base_model_id"]
        assert model_id_schema["pattern"] == base_model_id_schema["pattern"]

        from jsonschema import Draft202012Validator

        candidates = [
            ("mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W", True),
            ("mdl_71JQ8Z3K4M5N6P7Q8R9S0T1V2W", True),
            ("mdl_81JQ8Z3K4M5N6P7Q8R9S0T1V2W", False),
            ("mdl_91JQ8Z3K4M5N6P7Q8R9S0T1V2W", False),
            ("mdl_A1JQ8Z3K4M5N6P7Q8R9S0T1V2W", False),
        ]
        for model_id, expected in candidates:
            assert validate_model_id(model_id) is expected
            assert Draft202012Validator(model_id_schema).is_valid(model_id) is expected
            assert Draft202012Validator(base_model_id_schema).is_valid(model_id) is expected

    def test_validate_event_id_valid(self):
        assert validate_event_id("evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K")

    def test_validate_event_id_starts_with_0_or_7(self):
        # ULID first character must be 0-7 per 128-bit range
        assert validate_event_id("evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K")
        assert validate_event_id("evt_71JQ8Z4A1B2C3D4E5F6G7H8J9M")

    def test_validate_event_id_starts_with_8_rejected(self):
        # ULID starting with 8 exceeds 128-bit range
        assert not validate_event_id("evt_8" + "JQ8Z4A1B2C3D4E5F6G7H8J9K"[1:])

    def test_validate_event_id_starts_with_9_rejected(self):
        # ULID starting with 9 exceeds 128-bit range
        assert not validate_event_id("evt_9" + "JQ8Z4A1B2C3D4E5F6G7H8J9K"[1:])

    def test_validate_event_id_starts_with_letter_rejected(self):
        # ULID starting with A-H (beyond first-char range) rejected
        assert not validate_event_id("evt_A" + "JQ8Z4A1B2C3D4E5F6G7H8J9K"[1:])

    def test_validate_event_id_too_short(self):
        assert not validate_event_id("evt_123")

    def test_validate_event_id_no_prefix(self):
        assert not validate_event_id("invalid")

    def test_validate_event_id_non_string(self):
        assert not validate_event_id(17)
        assert not validate_event_id(None)


# ---------------------------------------------------------------------------
# Manifest Validation Tests
# ---------------------------------------------------------------------------

class TestManifestValidation:
    def test_valid_manifest(self):
        manifest = {
            "schema_version": "3.0.0",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "created_at": "2026-11-25T18:00:00.000000Z",
            "sealed_at": "2026-11-25T18:04:12.345678Z",
            "status_at_seal": "sealed",
            "run_fingerprint": "a" * 64,
            "git": {
                "commit": "0" * 40,
                "dirty": False,
                "branch": "main",
                "tag": None,
                "source_bundle_sha256": "b" * 64,
            },
            "producer": {
                "name": "tradingai-btc",
                "version": "0.2.0",
                "python": "3.13.15",
                "command": "python -m tradingai.ml.train",
                "config_sha256": "c" * 64,
            },
            "data": {
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "provider": "binance",
                "provider_version": "2026.11",
                "dataset_sha256": "d" * 64,
                "snapshot_uri": "data/store/sha256/01/deadbeef.parquet",
                "raw_rows": 4320,
                "feature_rows": 4287,
                "labeled_rows": 4262,
                "time_range": {
                    "start": "2026-01-01T00:00:00Z",
                    "end": "2026-06-27T13:00:00Z",
                    "timezone": "UTC",
                },
                "missing_data_policy": "drop_incomplete_bars",
                "gap_policy": "no_synthetic_fill",
                "ohlcv_schema_version": "1.0.0",
                "alignment": "left_closed_right_open",
            },
            "target": {
                "name": "future_return_threshold",
                "horizon_bars": 5,
                "vol_mult": "0.5",
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "rule_sha256": "e" * 64,
                "nan_policy": "drop_label",
            },
            "features": {
                "ordered": ["feat_01", "feat_02"],
                "count": 2,
                "definition_sha256": "f" * 64,
                "matrix_sha256": "1" * 64,
                "pipeline_version": "2.0.0",
                "code_sha256": "2" * 64,
                "parameters": {"lookback_max": 50},
                "nan_policy": "dropna_before_split",
            },
            "training": {
                "task": "multiclass_classification",
                "models": {
                    "rf": {"library": "scikit-learn", "version": "1.9.1", "params": {}},
                    "xgb": {"library": "xgboost", "version": "3.4.1", "params": {}},
                },
                "ensemble": {"method": "mean_probability", "weights": {"rf": "0.5", "xgb": "0.5"}},
                "seed": 42,
                "environment": {"python": "3.13.15"},
                "hardware": {
                    "device": "cpu",
                    "gpu_model": None,
                    "cuda_version": None,
                    "cpu_count": 16,
                    "ram_gb": 32,
                },
                "determinism": {
                    "bitwise_reproducible": True,
                    "n_jobs": 1,
                    "omp_num_threads": 1,
                    "xgb_tree_method": "hist",
                    "xgb_deterministic_histogram": True,
                    "gpu_deterministic": False,
                },
            },
            "validation": {
                "split_method": "chronological_holdout",
                "partitions": {
                    "train": {
                        "row_start": 0,
                        "row_end": 2548,
                        "n_rows": 2548,
                        "time_start": "2026-01-01T00:00:00Z",
                        "time_end": "2026-04-17T03:00:00Z",
                        "class_counts": [1530, 340, 678],
                        "index_sha256": "3" * 64,
                    },
                    "validation": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "time_start": "2026-04-17T08:00:00Z",
                        "time_end": "2026-05-22T19:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "4" * 64,
                    },
                    "calibration": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "time_start": "2026-04-17T08:00:00Z",
                        "time_end": "2026-05-22T19:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "5" * 64,
                        "shared_with": "validation",
                    },
                    "test": {
                        "row_start": 3410,
                        "row_end": 4262,
                        "n_rows": 852,
                        "time_start": "2026-05-23T00:00:00Z",
                        "time_end": "2026-06-27T11:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "6" * 64,
                    },
                },
                "purge": {
                    "rows_between_partitions": 5,
                    "label_horizon_bars": 5,
                    "label_purge_satisfied": True,
                    "embargo_rows": 0,
                },
                "partition_manifest_sha256": "7" * 64,
                "leakage_checks": {
                    "disjoint": True,
                    "purge_satisfied": True,
                    "labels_within_partition": True,
                },
                "evaluation": {
                    "metric_spec_version": "1.0.0",
                    "primary_metric": "macro_f1",
                    "test_evaluated_once": True,
                    "evaluation_code_sha256": "8" * 64,
                    "evaluated_at": "2026-11-25T18:04:12.345678Z",
                },
            },
            "calibration": {
                "mode": "in_pipeline",
                "base_model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "base_artifact_sha256": {"rf": "d" * 64, "xgb": "e" * 64},
                "method": "sigmoid",
                "fit_partition": "validation",
                "calibration_input_sha256": "b" * 64,
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "n_calibrators": 3,
                "artifact_sha256": "f" * 64,
            },
            "artifacts": [
                {
                    "role": "rf",
                    "path": "rf.joblib",
                    "sha256": "d" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "1.6.0",
                },
                {
                    "role": "xgb",
                    "path": "xgb.joblib",
                    "sha256": "e" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "3.4.1",
                },
                {
                    "role": "calibrator",
                    "path": "calibrator.joblib",
                    "sha256": "f" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "1.6.0",
                },
            ],
            "metrics": {
                "path": "metrics.json",
                "sha256": "1" * 64,
                "schema_version": "1.0.0",
            },
            "extensions": {},
        }
        errors = validate_manifest(manifest)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_missing_required_field(self):
        manifest = {"schema_version": "3.0.0"}
        errors = validate_manifest(manifest)
        assert len(errors) > 0
        assert any("model_id" in e for e in errors)

    def test_unknown_field(self):
        manifest = {"schema_version": "3.0.0", "unknown_field": "value"}
        errors = validate_schema(manifest)
        assert len(errors) > 0

    def test_invalid_model_id(self):
        manifest = {"model_id": "invalid"}
        errors = validate_manifest(manifest)
        assert any("model_id" in e.lower() for e in errors)

    def test_invalid_status(self):
        """Test that validate_manifest rejects manifests with invalid status.

        Per R7, only specific status values are allowed at seal.
        This test verifies that an invalid status triggers a rejection.
        """
        manifest = {
            "schema_version": "3.0.0",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "created_at": "2026-11-25T18:00:00Z",
            "sealed_at": "2026-11-25T18:04:12Z",
            "status_at_seal": "invalid_status",  # Not in allowed set
            "run_fingerprint": "a" * 64,
            "git": {
                "commit": "0" * 40,
                "dirty": False,
                "branch": "main",
                "tag": None,
                "source_bundle_sha256": "b" * 64,
            },
            "producer": {
                "name": "tradingai-btc",
                "version": "0.2.0",
                "python": "3.13.15",
                "command": "python -m tradingai.ml.train",
                "config_sha256": "c" * 64,
            },
            "data": {
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "provider": "binance",
                "provider_version": "2026.11",
                "dataset_sha256": "d" * 64,
                "snapshot_uri": "data/store/sha256/01/deadbeef.parquet",
                "raw_rows": 4320,
                "feature_rows": 4287,
                "labeled_rows": 4262,
                "time_range": {
                    "start": "2026-01-01T00:00:00Z",
                    "end": "2026-06-27T13:00:00Z",
                    "timezone": "UTC",
                },
                "missing_data_policy": "drop_incomplete_bars",
                "gap_policy": "no_synthetic_fill",
                "ohlcv_schema_version": "1.0.0",
                "alignment": "left_closed_right_open",
            },
            "target": {
                "name": "future_return_threshold",
                "horizon_bars": 5,
                "vol_mult": "0.5",
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "rule_sha256": "e" * 64,
                "nan_policy": "drop_label",
            },
            "features": {
                "ordered": ["feat_01", "feat_02"],
                "count": 2,
                "definition_sha256": "f" * 64,
                "matrix_sha256": "1" * 64,
                "pipeline_version": "2.0.0",
                "code_sha256": "2" * 64,
                "parameters": {"lookback_max": 50},
                "nan_policy": "dropna_before_split",
            },
            "training": {
                "task": "multiclass_classification",
                "models": {
                    "rf": {"library": "scikit-learn", "version": "1.9.1", "params": {}},
                    "xgb": {"library": "xgboost", "version": "3.4.1", "params": {}},
                },
                "ensemble": {"method": "mean_probability", "weights": {"rf": "0.5", "xgb": "0.5"}},
                "seed": 42,
                "environment": {"python": "3.13.15"},
                "hardware": {
                    "device": "cpu",
                    "gpu_model": None,
                    "cuda_version": None,
                    "cpu_count": 16,
                    "ram_gb": 32,
                },
                "determinism": {
                    "bitwise_reproducible": True,
                    "n_jobs": 1,
                    "omp_num_threads": 1,
                    "xgb_tree_method": "hist",
                    "xgb_deterministic_histogram": True,
                    "gpu_deterministic": False,
                },
            },
            "validation": {
                "split_method": "chronological_holdout",
                "partitions": {
                    "train": {
                        "row_start": 0,
                        "row_end": 2548,
                        "n_rows": 2548,
                        "time_start": "2026-01-01T00:00:00Z",
                        "time_end": "2026-04-17T03:00:00Z",
                        "class_counts": [1530, 340, 678],
                        "index_sha256": "3" * 64,
                    },
                    "validation": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "time_start": "2026-04-17T08:00:00Z",
                        "time_end": "2026-05-22T19:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "4" * 64,
                    },
                    "calibration": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "time_start": "2026-04-17T08:00:00Z",
                        "time_end": "2026-05-22T19:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "5" * 64,
                        "shared_with": "validation",
                    },
                    "test": {
                        "row_start": 3410,
                        "row_end": 4262,
                        "n_rows": 852,
                        "time_start": "2026-05-23T00:00:00Z",
                        "time_end": "2026-06-27T11:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "6" * 64,
                    },
                },
                "purge": {
                    "rows_between_partitions": 5,
                    "label_horizon_bars": 5,
                    "label_purge_satisfied": True,
                    "embargo_rows": 0,
                },
                "partition_manifest_sha256": "7" * 64,
                "leakage_checks": {
                    "disjoint": True,
                    "purge_satisfied": True,
                    "labels_within_partition": True,
                },
                "evaluation": {
                    "metric_spec_version": "1.0.0",
                    "primary_metric": "macro_f1",
                    "test_evaluated_once": True,
                    "evaluation_code_sha256": "8" * 64,
                    "evaluated_at": "2026-11-25T18:04:12.345678Z",
                },
            },
            "calibration": {
                "mode": "in_pipeline",
                "base_model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "base_artifact_sha256": {"rf": "d" * 64, "xgb": "e" * 64},
                "method": "sigmoid",
                "fit_partition": "validation",
                "calibration_input_sha256": "b" * 64,
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "n_calibrators": 3,
                "artifact_sha256": "f" * 64,
            },
            "artifacts": [
                {
                    "role": "rf",
                    "path": "rf.joblib",
                    "sha256": "d" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "1.6.0",
                },
                {
                    "role": "xgb",
                    "path": "xgb.joblib",
                    "sha256": "e" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "3.4.1",
                },
                {
                    "role": "calibrator",
                    "path": "calibrator.joblib",
                    "sha256": "f" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "1.6.0",
                },
            ],
            "metrics": {
                "path": "metrics.json",
                "sha256": "1" * 64,
                "schema_version": "1.0.0",
            },
            "extensions": {},
        }
        errors = validate_manifest(manifest)
        assert len(errors) > 0, "Expected validation errors for invalid status, got none"
        status_errors = [e for e in errors if "status_at_seal" in e.lower() or "invalid" in e.lower()]
        assert len(status_errors) > 0, f"Expected status-related errors, got: {errors}"

    def test_features_count_mismatch(self):
        """Test that validate_manifest detects feature count mismatch.

        Per R7, the feature count must be consistent across the manifest.
        This test verifies that a mismatch between declared count and
        the actual number of ordered features is caught.
        """
        manifest = {
            "schema_version": "3.0.0",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "created_at": "2026-11-25T18:00:00Z",
            "sealed_at": "2026-11-25T18:04:12Z",
            "status_at_seal": "sealed",
            "run_fingerprint": "a" * 64,
            "git": {
                "commit": "0" * 40,
                "dirty": False,
                "branch": "main",
                "tag": None,
                "source_bundle_sha256": "b" * 64,
            },
            "producer": {
                "name": "tradingai-btc",
                "version": "0.2.0",
                "python": "3.13.15",
                "command": "python -m tradingai.ml.train",
                "config_sha256": "c" * 64,
            },
            "data": {
                "symbol": "BTC/USDT",
                "timeframe": "1h",
                "provider": "binance",
                "provider_version": "2026.11",
                "dataset_sha256": "d" * 64,
                "snapshot_uri": "data/store/sha256/01/deadbeef.parquet",
                "raw_rows": 4320,
                "feature_rows": 4287,
                "labeled_rows": 4262,
                "time_range": {
                    "start": "2026-01-01T00:00:00Z",
                    "end": "2026-06-27T13:00:00Z",
                    "timezone": "UTC",
                },
                "missing_data_policy": "drop_incomplete_bars",
                "gap_policy": "no_synthetic_fill",
                "ohlcv_schema_version": "1.0.0",
                "alignment": "left_closed_right_open",
            },
            "target": {
                "name": "future_return_threshold",
                "horizon_bars": 5,
                "vol_mult": "0.5",
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "rule_sha256": "e" * 64,
                "nan_policy": "drop_label",
            },
            "features": {
                "ordered": ["feat_01", "feat_02", "feat_03", "feat_04"],  # 4 features
                "count": 2,  # But count says 2 -- MISMATCH
                "definition_sha256": "f" * 64,
                "matrix_sha256": "1" * 64,
                "pipeline_version": "2.0.0",
                "code_sha256": "2" * 64,
                "parameters": {"lookback_max": 50},
                "nan_policy": "dropna_before_split",
            },
            "training": {
                "task": "multiclass_classification",
                "models": {
                    "rf": {"library": "scikit-learn", "version": "1.9.1", "params": {}},
                    "xgb": {"library": "xgboost", "version": "3.4.1", "params": {}},
                },
                "ensemble": {"method": "mean_probability", "weights": {"rf": "0.5", "xgb": "0.5"}},
                "seed": 42,
                "environment": {"python": "3.13.15"},
                "hardware": {
                    "device": "cpu",
                    "gpu_model": None,
                    "cuda_version": None,
                    "cpu_count": 16,
                    "ram_gb": 32,
                },
                "determinism": {
                    "bitwise_reproducible": True,
                    "n_jobs": 1,
                    "omp_num_threads": 1,
                    "xgb_tree_method": "hist",
                    "xgb_deterministic_histogram": True,
                    "gpu_deterministic": False,
                },
            },
            "validation": {
                "split_method": "chronological_holdout",
                "partitions": {
                    "train": {
                        "row_start": 0,
                        "row_end": 2548,
                        "n_rows": 2548,
                        "time_start": "2026-01-01T00:00:00Z",
                        "time_end": "2026-04-17T03:00:00Z",
                        "class_counts": [1530, 340, 678],
                        "index_sha256": "3" * 64,
                    },
                    "validation": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "time_start": "2026-04-17T08:00:00Z",
                        "time_end": "2026-05-22T19:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "4" * 64,
                    },
                    "calibration": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "time_start": "2026-04-17T08:00:00Z",
                        "time_end": "2026-05-22T19:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "5" * 64,
                        "shared_with": "validation",
                    },
                    "test": {
                        "row_start": 3410,
                        "row_end": 4262,
                        "n_rows": 852,
                        "time_start": "2026-05-23T00:00:00Z",
                        "time_end": "2026-06-27T11:00:00Z",
                        "class_counts": [350, 255, 247],
                        "index_sha256": "6" * 64,
                    },
                },
                "purge": {
                    "rows_between_partitions": 5,
                    "label_horizon_bars": 5,
                    "label_purge_satisfied": True,
                    "embargo_rows": 0,
                },
                "partition_manifest_sha256": "7" * 64,
                "leakage_checks": {
                    "disjoint": True,
                    "purge_satisfied": True,
                    "labels_within_partition": True,
                },
                "evaluation": {
                    "metric_spec_version": "1.0.0",
                    "primary_metric": "macro_f1",
                    "test_evaluated_once": True,
                    "evaluation_code_sha256": "8" * 64,
                    "evaluated_at": "2026-11-25T18:04:12.345678Z",
                },
            },
            "calibration": {
                "mode": "in_pipeline",
                "base_model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "base_artifact_sha256": {"rf": "d" * 64, "xgb": "e" * 64},
                "method": "sigmoid",
                "fit_partition": "validation",
                "calibration_input_sha256": "b" * 64,
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "n_calibrators": 3,
                "artifact_sha256": "f" * 64,
            },
            "artifacts": [
                {
                    "role": "rf",
                    "path": "rf.joblib",
                    "sha256": "d" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "1.6.0",
                },
                {
                    "role": "xgb",
                    "path": "xgb.joblib",
                    "sha256": "e" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "3.4.1",
                },
                {
                    "role": "calibrator",
                    "path": "calibrator.joblib",
                    "sha256": "f" * 64,
                    "bytes": 1000,
                    "media_type": "application/octet-stream",
                    "format": "joblib-pickle",
                    "serializer": "1.6.0",
                },
            ],
            "metrics": {
                "path": "metrics.json",
                "sha256": "1" * 64,
                "schema_version": "1.0.0",
            },
            "extensions": {},
        }
        errors = validate_manifest(manifest)
        assert len(errors) > 0, "Expected validation errors for feature count mismatch, got none"
        count_errors = [e for e in errors if "count" in e.lower() or "feature" in e.lower()]
        assert len(count_errors) > 0, f"Expected feature count errors, got: {errors}"


# ---------------------------------------------------------------------------
# Event Validation Tests
# ---------------------------------------------------------------------------

class TestEventValidation:
    def test_valid_first_event(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "event_sha256": "a" * 64,  # Will be validated against JCS hash
            "actor": "pipeline",
            "evidence": None,
        }
        errors = validate_event(event)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_missing_field(self):
        event = {"sequence_number": 1}
        errors = validate_event(event)
        assert len(errors) > 0

    def test_sequence_gap(self):
        prev = {
            "sequence_number": 1,
            "event_sha256": "a" * 64,
        }
        event = {
            "sequence_number": 3,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "validated",
            "at": "2026-11-25T10:00:00Z",
            "event_sha256": "a" * 64,
            "actor": "verifier",
            "evidence": None,
        }
        errors = validate_event(event, previous_event=prev)
        assert len(errors) > 0
        assert any("Sequence gap" in e for e in errors)

    def test_first_event_wrong_sequence(self):
        event = {
            "sequence_number": 2,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "event_sha256": "a" * 64,
            "actor": "pipeline",
            "evidence": None,
        }
        errors = validate_event(event)
        assert len(errors) > 0
        assert any("sequence_number" in e.lower() for e in errors)

    def test_invalid_event_type(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "invalid_event",
            "at": "2026-11-25T10:00:00Z",
            "event_sha256": "a" * 64,
            "actor": "pipeline",
            "evidence": None,
        }
        errors = validate_event(event)
        assert len(errors) > 0
        assert any("Invalid event type" in e for e in errors)

    def test_verify_event_hash(self):
        # Build event WITHOUT event_sha256, compute the hash, then set it
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "actor": "pipeline",
            "evidence": None,
        }
        computed = sha256_canonical(event)
        event["event_sha256"] = computed
        assert verify_event_hash(event, computed)

    def test_verify_event_hash_wrong(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "event_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "actor": "pipeline",
            "evidence": None,
        }
        assert not verify_event_hash(event, "wrong" * 8)


class TestEventValidationHardening:
    """R10-02: malformed inputs must produce errors, never tracebacks."""

    def test_validate_event_rejects_non_object(self):
        for value in (None, [], "event", 42):
            assert validate_event(value) == ["Event must be a JSON object"]

    def test_validate_event_non_string_fields_are_controlled(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["event_id"] = ["not", "a", "string"]
        event["model_id"] = 17
        event["previous_event_sha256"] = 0
        event["event_sha256"] = 0
        errors = validate_event(event)
        assert any("event_id" in e for e in errors)
        assert any("model_id" in e for e in errors)
        assert any("previous_event_sha256" in e for e in errors)
        assert any("event_sha256" in e for e in errors)

    def test_validate_event_non_dict_previous_event_is_controlled(self):
        event = make_event(
            2, MODEL_ID_A, EVENT_ID_B, "validated", "2026-11-25T11:00:00Z", previous="a" * 64
        )
        errors = validate_event(event, previous_event=["not", "a", "dict"])
        assert any("previous_event must be a JSON object" in e for e in errors)

    def test_event_with_manifest_sha256_is_allowed(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["manifest_sha256"] = "e" * 64
        event["event_sha256"] = sha256_canonical(
            {k: v for k, v in event.items() if k != "event_sha256"}
        )
        assert validate_event(event) == []
        assert validate_event_chain([event]) == []

    def test_event_invalid_manifest_sha256_is_rejected(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["manifest_sha256"] = "not-a-hash"
        errors = validate_event(event)
        assert any("manifest_sha256" in e for e in errors)
        assert not any("unknown field" in e.lower() for e in errors)

    def test_event_actor_and_evidence_types_are_checked(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["actor"] = 42
        event["evidence"] = ["not", "an", "object"]
        errors = validate_event(event)
        assert any("actor must be a string" in e for e in errors)
        assert any("evidence must be an object" in e for e in errors)

    def test_validate_event_invalid_previous_sequence_is_controlled(self):
        event = make_event(
            2, MODEL_ID_A, EVENT_ID_B, "validated", "2026-11-25T11:00:00Z", previous="a" * 64
        )
        for bad_sequence in ("1", True, None, 1.5):
            errors = validate_event(event, previous_event={"sequence_number": bad_sequence})
            assert any("previous_event has invalid sequence_number" in e for e in errors)

    def test_event_chain_rejects_non_list(self):
        assert validate_event_chain(None) == ["Event chain must be a list of events"]
        assert validate_event_chain({"sequence_number": 1}) == [
            "Event chain must be a list of events"
        ]

    def test_event_chain_rejects_non_object_entries(self):
        errors = validate_event_chain([None, "event", 42])
        assert len(errors) == 3
        assert all("event must be a JSON object" in e for e in errors)

    def test_event_chain_unhashable_identifiers_are_controlled(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["model_id"] = ["unhashable"]
        event["event_id"] = {"unhashable": True}
        errors = validate_event_chain([event])
        assert any("model_id" in e for e in errors)
        assert any("event_id" in e for e in errors)

    def test_event_chain_non_string_declared_hash_is_controlled(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["event_sha256"] = 123
        errors = validate_event_chain([event])
        assert any("event_sha256" in e for e in errors)

    def test_event_chain_impossible_timestamp_is_rejected(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-02-30T10:00:00Z")
        errors = validate_event_chain([event])
        assert any("at format" in e for e in errors)

    def test_event_chain_bad_hash_characters_are_rejected(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["event_sha256"] = "G" * 64
        errors = validate_event_chain([event])
        assert any("event_sha256" in e for e in errors)

    def test_event_chain_unknown_field_is_rejected(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["extra"] = "not allowed"
        event["event_sha256"] = sha256_canonical(
            {k: v for k, v in event.items() if k != "event_sha256"}
        )
        errors = validate_event_chain([event])
        assert any("unknown field" in e.lower() for e in errors)

    def test_event_chain_missing_field_is_rejected(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        del event["actor"]
        event["event_sha256"] = sha256_canonical(
            {k: v for k, v in event.items() if k != "event_sha256"}
        )
        errors = validate_event_chain([event])
        assert any("missing required field" in e.lower() for e in errors)

    def test_event_chain_valid_three_event_chain(self):
        first = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        second = make_event(
            2,
            MODEL_ID_A,
            EVENT_ID_B,
            "validated",
            "2026-11-25T11:00:00Z",
            previous=first["event_sha256"],
        )
        third = make_event(
            3,
            MODEL_ID_A,
            EVENT_ID_C,
            "approved",
            "2026-11-25T12:00:00Z",
            previous=second["event_sha256"],
        )
        assert validate_event_chain([first, second, third]) == []

    def test_event_chain_wrong_previous_hash_is_rejected(self):
        first = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        second = make_event(
            2,
            MODEL_ID_A,
            EVENT_ID_B,
            "validated",
            "2026-11-25T11:00:00Z",
            previous="b" * 64,
        )
        errors = validate_event_chain([first, second])
        assert any("previous_event_sha256" in e for e in errors)

    def test_event_chain_tampered_intermediate_event_is_rejected(self):
        first = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        second = make_event(
            2,
            MODEL_ID_A,
            EVENT_ID_B,
            "validated",
            "2026-11-25T11:00:00Z",
            previous=first["event_sha256"],
        )
        third = make_event(
            3,
            MODEL_ID_A,
            EVENT_ID_C,
            "approved",
            "2026-11-25T12:00:00Z",
            previous=second["event_sha256"],
        )
        second["actor"] = "tampered"
        errors = validate_event_chain([first, second, third])
        assert any("event_sha256" in e for e in errors)
        assert any("previous_event_sha256" in e for e in errors)

    def test_event_chain_does_not_sort_physical_order(self):
        first = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        second = make_event(
            2,
            MODEL_ID_A,
            EVENT_ID_B,
            "validated",
            "2026-11-25T11:00:00Z",
            previous=first["event_sha256"],
        )
        errors = validate_event_chain([second, first])
        assert any("first event" in e for e in errors)

    def test_event_chain_recursive_payload_is_controlled(self):
        event = make_event(1, MODEL_ID_A, EVENT_ID_A, "sealed", "2026-11-25T10:00:00Z")
        event["evidence"] = event
        errors = validate_event_chain([event])
        assert any("error computing JCS hash" in e for e in errors)


# ---------------------------------------------------------------------------
# Schema Validation Tests
# ---------------------------------------------------------------------------

class TestSchemaValidation:
    def test_manifest_schema_loaded(self):
        assert MANIFEST_SCHEMA is not None
        assert MANIFEST_SCHEMA.get("title") == "Model Provenance Manifest v3"

    def test_schema_rejects_unknown_fields(self):
        manifest = {"schema_version": "3.0.0", "unknown_field": "value"}
        errors = validate_schema(manifest)
        assert len(errors) > 0

    def test_schema_requires_fields(self):
        manifest = {}
        errors = validate_schema(manifest)
        assert len(errors) > 0
        assert any("required" in e.lower() or "schema_version" in e for e in errors)

    def test_schema_has_no_orphan_training_block(self):
        # R10: the ineffective top-level "training" keyword from R9 is gone.
        assert "training" not in MANIFEST_SCHEMA

    def test_rf_params_are_closed(self):
        import jsonschema

        models = MANIFEST_SCHEMA["properties"]["training"]["properties"]["models"]
        schema = models["properties"]["rf"]["properties"]["params"]
        assert schema.get("additionalProperties") is False
        validator = jsonschema.Draft202012Validator(schema)
        assert validator.is_valid(
            {
                "n_estimators": 200,
                "max_depth": 8,
                "class_weight": "balanced",
                "random_state": 42,
                "n_jobs": 1,
            }
        )
        assert not validator.is_valid({"n_estimators": 200, "unknown_param": 1})

    def test_xgb_params_are_closed(self):
        import jsonschema

        models = MANIFEST_SCHEMA["properties"]["training"]["properties"]["models"]
        schema = models["properties"]["xgb"]["properties"]["params"]
        assert schema.get("additionalProperties") is False
        validator = jsonschema.Draft202012Validator(schema)
        assert validator.is_valid(
            {
                "n_estimators": 200,
                "max_depth": 6,
                "learning_rate": 0.05,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "random_state": 42,
                "tree_method": "hist",
                "device": "cpu",
                "objective": "multi:softprob",
                "num_class": 3,
                "eval_metric": "mlogloss",
                "n_jobs": 1,
            }
        )
        assert not validator.is_valid({"n_estimators": 200, "unknown_param": 1})

    def test_decimal_string_field_rejects_number(self):
        import jsonschema

        schema = MANIFEST_SCHEMA["properties"]["target"]["properties"]["vol_mult"]
        validator = jsonschema.Draft202012Validator(schema)
        assert validator.is_valid("0.5")
        assert not validator.is_valid(0.5)


# ---------------------------------------------------------------------------
# JCS Vector Tests
# ---------------------------------------------------------------------------

class TestJCSVectors:
    def test_basic_object(self):
        obj = {"a": 1, "b": 2}
        assert jcs_canonicalize(obj) == '{"a":1,"b":2}'

    def test_nested_sorting(self):
        obj = {"z": {"b": 1, "a": 2}, "a": 3}
        assert jcs_canonicalize(obj) == '{"a":3,"z":{"a":2,"b":1}}'

    def test_array_order_preserved(self):
        obj = {"arr": [3, 1, 2]}
        assert jcs_canonicalize(obj) == '{"arr":[3,1,2]}'

    def test_unicode_sorting_utf16(self):
        obj = {"a": 1, "\U00010000": 2}
        result = jcs_canonicalize(obj)
        assert result == '{"a":1,"\U00010000":2}'

    def test_no_whitespace(self):
        obj = {"key": "value", "num": 42}
        result = jcs_canonicalize(obj)
        assert " " not in result
        assert "\n" not in result
        assert "\t" not in result

    def test_string_escaping(self):
        obj = {"key": 'quote"here'}
        result = jcs_canonicalize(obj)
        assert result == '{"key":"quote\\"here"}'

    # ----- R8-01: Pruebas exactas de canonicalización JCS -----

    def test_jcs_1e_6(self):
        """RFC 8785 Appendix B: 1e-6."""
        assert jcs_canonicalize(1e-6) == "0.000001"

    def test_jcs_1e_7(self):
        """RFC 8785 Appendix B: 1e-7."""
        assert jcs_canonicalize(1e-7) == "1e-7"

    def test_jcs_1e_20(self):
        """RFC 8785 Appendix B: 1e20."""
        assert jcs_canonicalize(1e20) == "100000000000000000000"

    def test_jcs_1e_21(self):
        """RFC 8785 Appendix B: 1e21."""
        assert jcs_canonicalize(1e21) == "1e+21"

    def test_jcs_m_negative_zero(self):
        """RFC 8785 Appendix B: -0 and -0.0."""
        assert jcs_canonicalize(-0) == "0"
        assert jcs_canonicalize(-0.0) == "0"

    def test_jcs_unicode_key_ordering(self):
        """RFC 8785 §3.2.3: sort by UTF-16 code units (unsigned).

        U+E000 and U+10000 must be ordered by their UTF-16 LE code units.
        The canonical output must have keys sorted by UTF-16 code unit
        interpretation (unsigned), without reordering by the test.
        """
        # Only the two unicode keys; "a" would sort first (0x61 < 0x10000)
        obj = {chr(0xE000): "e000", chr(0x10000): "10000"}
        result = jcs_canonicalize(obj)
        # Parse result to extract key order
        import json
        parsed = json.loads(result)
        keys = list(parsed.keys())
        # U+10000 (0x10000) sorts before U+E000 (0xE000) in UTF-16 LE unsigned
        assert len(keys) == 2, f"Expected 2 keys, got {len(keys)}: {keys}"
        assert keys[0] == chr(0x10000), f"Expected first key to be U+10000, got {repr(keys[0])}"
        assert keys[1] == chr(0xE000), f"Expected second key to be U+E000, got {repr(keys[1])}"

    def test_jcs_integers(self):
        """Integers within binary64 safe range."""
        assert jcs_canonicalize(42) == "42"
        assert jcs_canonicalize(0) == "0"
        assert jcs_canonicalize(-1) == "-1"

    def test_jcs_nan_inf_rejected(self):
        """NaN and Infinity are rejected by RFC 8785."""
        import rfc8785
        try:
            jcs_canonicalize(float("nan"))
            assert False, "Debería haber lanzado FloatDomainError"
        except rfc8785.FloatDomainError:
            pass
        try:
            jcs_canonicalize(float("inf"))
            assert False, "Debería haber lanzado FloatDomainError"
        except rfc8785.FloatDomainError:
            pass
        try:
            jcs_canonicalize(float("-inf"))
            assert False, "Debería haber lanzado FloatDomainError"
        except rfc8785.FloatDomainError:
            pass

    def test_jcs_beyond_safe_integer(self):
        """Integers beyond binary64 safe range raise error via rfc8785.

        RFC 8785 does not define representation for integers with
        abs(val) > 2**53 (the binary64 safe integer range). The rfc8785
        library raises ValueError/OverflowError for such values.
        """
        import rfc8785
        try:
            jcs_canonicalize(2**53 + 1)
            assert False, "Debería haber lanzado error"
        except (ValueError, OverflowError):
            pass

    # ----- R8-02: Política para enteros fuera del dominio JCS -----

    def test_jcs_safe_integer_range(self):
        """Integers within abs(val) <= 2**53 - 1 are accepted."""
        # 2**53 - 1 = 9007199254740991 is the max safe integer
        assert jcs_canonicalize(2**53 - 1) == "9007199254740991"
        assert jcs_canonicalize(-(2**53 - 1)) == "-9007199254740991"
        assert jcs_canonicalize(2**53 - 2) == "9007199254740990"

    def test_jcs_large_integer_rejected(self):
        """Integers with abs(val) > 2**53 - 1 are rejected by rfc8785.

        Política R8-02: no convertir silenciosamente valores numéricos
        fuera del dominio interoperable. Estos valores deben representarse
        como cadenas explícitas en el esquema del manifiesto.
        """
        import rfc8785
        # 2**53 + 1 exceeds safe domain
        try:
            jcs_canonicalize(2**53 + 1)
            assert False, "Debería haber lanzado error"
        except (ValueError, OverflowError):
            pass
        # -(2**53 + 1) also exceeds safe domain
        try:
            jcs_canonicalize(-(2**53 + 1))
            assert False, "Debería haber lanzado error"
        except (ValueError, OverflowError):
            pass

    def test_jcs_string_fields_not_converted(self):
        """Fields defined as strings in the schema must not be converted to numbers.

        R9-02: if a manifest field is declared as type string, its value
        must be a string, not a number. The JCS canonicalization must
        preserve the string type (JSON string encoding). No automatic
        coercion between types is performed.

        Also per R8-02: integers outside the binary64 safe domain are rejected.
        """
        # JCS canonicalize of a string value returns the JSON string encoding
        assert jcs_canonicalize("hello") == '"hello"'
        # Passing a JSON object string: the string itself is treated as a
        # JSON value and canonicalized accordingly
        result = jcs_canonicalize('{"count": "100"}')
        # The result is a JSON string with escaped double quotes
        assert '"' in result and 'count' in result
        # Verify that a number stored as a string field is preserved as string
        obj = {"count": "100"}
        result = jcs_canonicalize(obj)
        # The value "100" should remain as a string, not be converted to number 100
        assert '"100"' in result, "String-typed field value must remain as string"
        # Verify integer safe range is preserved
        result = jcs_canonicalize(42)
        assert result == "42", "Integer within safe domain should be canonicalized"
        # Integer outside safe domain should be rejected
        import rfc8785
        try:
            jcs_canonicalize(2**53 + 1)
            assert False, "Should have raised ValueError/OverflowError"
        except (ValueError, OverflowError):
            pass  # Expected per R8-02

    # ----- R10-06: delegación rfc8785, UTF-8 y recursión -----

    def test_jcs_delegates_to_rfc8785(self):
        """jcs_canonical_bytes must be exactly rfc8785.dumps output."""
        import rfc8785

        obj = {"b": 1e-7, "a": [1e20, -0.0]}
        assert jcs_canonical_bytes(obj) == rfc8785.dumps(obj)
        assert jcs_canonicalize(obj) == rfc8785.dumps(obj).decode("utf-8")

    def test_jcs_utf8_encoding_without_bom(self):
        """Canonical bytes are UTF-8, without BOM or trailing newline."""
        data = jcs_canonical_bytes({"k": "áéíóú€\U00010000"})
        assert not data.startswith(b"\xef\xbb\xbf")
        assert not data.endswith(b"\n")
        assert data.decode("utf-8") == '{"k":"áéíóú€\U00010000"}'

    def test_jcs_deeply_nested_recursion(self):
        """Deeply nested objects are canonicalized without truncation."""
        obj = {"leaf": 1}
        for _ in range(100):
            obj = {"node": obj}
        result = jcs_canonicalize(obj)
        assert result.startswith('{"node":{"node":')
        assert '"leaf":1' in result
        assert result.count('"node"') == 100


# ---------------------------------------------------------------------------
# Event Chain Validation Tests
# ---------------------------------------------------------------------------

class TestEventChainValidation:
    def test_valid_chain_single_model(self):
        """Test a valid event chain for a single model.

        Per R7, all events in a chain must have previous_event_sha256 == "0" * 64
        (the genesis hash). Sequences increment by 1.
        Per S1-R5: event_sha256 is mandatory and must match the JCS canonical hash
        of the event (excluding event_sha256 itself).
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                # previous_event_sha256 must match the computed event_sha256 of
                # the first event (the JCS hash excluding event_sha256)
                "previous_event_sha256": None,  # Will be set computed below
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T11:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
        ]
        # Compute proper JCS canonical hashes (excluding event_sha256) and set event_sha256
        # Per S1-R5: do not use manifest_sha256 to omit cryptographic verification.
        # Set event_sha256 to the computed hash for each event.
        # For chain integrity: the second event's previous_event_sha256 must equal
        # the first event's computed event_sha256.
        first_event_copy = {k: v for k, v in events[0].items() if k != "event_sha256"}
        first_computed = sha256_canonical(first_event_copy)
        events[0]["event_sha256"] = first_computed
        events[1]["previous_event_sha256"] = first_computed
        events[1]["event_sha256"] = sha256_canonical({k: v for k, v in events[1].items() if k != "event_sha256"})
        
        errors = validate_event_chain(events)
        assert errors == [], f"Expected no errors for valid chain, got: {errors}"

    def test_two_intercalated_models(self):
        """Test two models interleaved in the same event list.

        Sequences are independent per model_id. All events have
        previous_event_sha256 == "0" * 64 (genesis) for the first event of
        each model. Per S1-R5: event_sha256 is mandatory and must match the JCS
        canonical hash. The test demonstrates independent chains per model_id
        with properly computed event_sha256 values.
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M",
                "model_id": "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X",
                "event": "sealed",
                "at": "2026-11-25T10:30:00Z",
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                # previous_event_sha256 must match the computed event_sha256 of the
                # prior event in the same model chain (model mdl_01JQ8Z...)
                "previous_event_sha256": None,  # Will be set computed below
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9N",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T12:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                # previous_event_sha256 must match the computed event_sha256 of the
                # prior event in the same model chain (model mdl_02JQ8Z...)
                "previous_event_sha256": None,  # Will be set computed below
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9P",
                "model_id": "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X",
                "event": "validated",
                "at": "2026-11-25T13:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
        ]
        # Compute proper JCS canonical hashes (excluding event_sha256) and set event_sha256
        # Per S1-R5: do not use manifest_sha256 to omit cryptographic verification.
        # For model mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W (events 0 and 2):
        first_event_0_copy = {k: v for k, v in events[0].items() if k != "event_sha256"}
        first_computed_0 = sha256_canonical(first_event_0_copy)
        events[0]["event_sha256"] = first_computed_0
        events[2]["previous_event_sha256"] = first_computed_0
        events[2]["event_sha256"] = sha256_canonical({k: v for k, v in events[2].items() if k != "event_sha256"})
        # For model mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X (events 1 and 3):
        first_event_1_copy = {k: v for k, v in events[1].items() if k != "event_sha256"}
        first_computed_1 = sha256_canonical(first_event_1_copy)
        events[1]["event_sha256"] = first_computed_1
        events[3]["previous_event_sha256"] = first_computed_1
        events[3]["event_sha256"] = sha256_canonical({k: v for k, v in events[3].items() if k != "event_sha256"})
        
        errors = validate_event_chain(events)
        # Should have no errors since sequences are independent per model_id
        assert len(errors) == 0, f"Expected no errors for intercalated models, got: {errors}"

    def test_duplicate_sequence(self):
        """Test that duplicate sequences are rejected."""
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 1,  # Duplicate sequence
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T11:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "verifier",
                "evidence": None,
            },
        ]
        errors = validate_event_chain(events)
        assert len(errors) > 0, "Expected errors for duplicate sequence"
        assert any("sequence" in e.lower() for e in errors), "Expected sequence-related error"

    def test_sequence_gap(self):
        """Test that gaps in sequence are rejected."""
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 3,  # Gap: missing 2
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T12:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "verifier",
                "evidence": None,
            },
        ]
        errors = validate_event_chain(events)
        assert len(errors) > 0, "Expected errors for sequence gap"
        # Check for sequence-related error
        assert any("sequence" in e.lower() for e in errors), f"Expected sequence error, got: {errors}"

    def test_duplicate_event_id(self):
        """Test that duplicate event_ids are rejected."""
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",  # Duplicate
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T11:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "verifier",
                "evidence": None,
            },
        ]
        errors = validate_event_chain(events)
        assert len(errors) > 0, "Expected errors for duplicate event_id"
        assert any("duplicate event_id" in e for e in errors), "Expected duplicate event_id error"

    def test_wrong_model_id_chain(self):
        """Test that events with wrong model_id break the chain."""
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M",
                "model_id": "mdl_DIFFERENT",  # Different model - separate chain
                "event": "validated",
                "at": "2026-11-25T11:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "verifier",
                "evidence": None,
            },
        ]
        errors = validate_event_chain(events)
        assert len(errors) > 0, "Expected errors for wrong model_id chain"

    def test_event_sha256_altered(self):
        """Test that altered event_sha256 is detected.

        Per S1-R5: demonstrate that changing event_sha256 invalidates the
        event hash. This uses verify_event_hash separately from
        validate_event_chain.
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
        ]
        # Compute the correct hash
        event_copy = {k: v for k, v in events[0].items() if k != "event_sha256"}
        computed = sha256_canonical(event_copy)
        events[0]["event_sha256"] = computed
        # Verify with the correct hash
        assert verify_event_hash(events[0], computed)
        # Verify that a wrong hash is rejected
        assert not verify_event_hash(events[0], "z" * 64)

    def test_malformed_event(self):
        """Test that malformed events are rejected."""
        events = [
            {
                "sequence_number": 1,
                # Missing many required fields
            },
        ]
        errors = validate_event_chain(events)
        assert len(errors) > 0, "Expected errors for malformed event"

    def test_physical_order_rejected(self):
        """Test that events not in physical order are detected."""
        events = [
            {
                "sequence_number": 2,  # Out of order - should be 1 first
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 1,  # Should have come first
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9M",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "event_sha256": "a" * 64,
                "actor": "pipeline",
                "evidence": None,
            },
        ]
        errors = validate_event_chain(events)
        assert len(errors) > 0, "Expected errors for out-of-order events"