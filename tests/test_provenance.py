"""Tests for S1: Schema v3, JCS canonicalization, and validators."""

import hashlib
import json

import pytest

from tradingai.ml.provenance import (
    MANIFEST_SCHEMA,
    StrictJSONError,
    jcs_canonical_bytes,
    jcs_canonicalize,
    parse_json_strict,
    sha256_bytes,
    sha256_canonical,
    validate_calibrator_binding,
    validate_event,
    validate_event_id,
    validate_manifest,
    validate_model_id,
    validate_partition_consistency,
    validate_rfc3339,
    validate_schema,
    validate_sha256,
    verify_event_hash,
)

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
        with pytest.raises(ValueError):
            jcs_canonicalize(float("nan"))

    def test_inf_rejected(self):
        with pytest.raises(ValueError):
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
            "string": "\u20ac$\u000a\u000d\u0000 (backslash: \\)",
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
        with pytest.raises(StrictJSONError):
            parse_json_strict('\ufeff{"a": 1}')

    def test_duplicate_keys_rejected(self):
        with pytest.raises(StrictJSONError):
            parse_json_strict('{"a": 1, "a": 2}')

    def test_nan_rejected(self):
        with pytest.raises(StrictJSONError):
            parse_json_strict('{"a": NaN}')

    def test_inf_rejected(self):
        with pytest.raises(StrictJSONError):
            parse_json_strict('{"a": Infinity}')

    def test_trailing_content_rejected(self):
        with pytest.raises(StrictJSONError):
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


# ---------------------------------------------------------------------------
# Validator Tests
# ---------------------------------------------------------------------------


class TestValidators:
    def test_validate_model_id_valid(self):
        assert validate_model_id("mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W")

    def test_validate_model_id_invalid(self):
        assert not validate_model_id("invalid")
        assert not validate_model_id("mdl_123")
        assert not validate_model_id("")

    def test_validate_event_id_valid(self):
        assert validate_event_id("evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K")

    def test_validate_event_id_invalid(self):
        assert not validate_event_id("invalid")
        assert not validate_event_id("evt_123")

    def test_validate_sha256_valid(self):
        assert validate_sha256("a" * 64)

    def test_validate_sha256_invalid(self):
        assert not validate_sha256("abc")
        assert not validate_sha256("G" * 64)
        assert not validate_sha256("")

    def test_validate_rfc3339_valid(self):
        assert validate_rfc3339("2026-11-25T10:00:00Z")
        assert validate_rfc3339("2026-11-25T10:00:00.123456Z")

    def test_validate_rfc3339_invalid(self):
        assert not validate_rfc3339("2026-11-25")
        assert not validate_rfc3339("not-a-date")


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
        pass

    def test_invalid_hash_format(self):
        assert not validate_sha256("abc")
        assert not validate_sha256("G" * 64)

    def test_features_count_mismatch(self):
        pass

    def test_calibration_binding(self):
        manifest = {
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "calibration": {
                "mode": "in_pipeline",
                "base_model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "base_artifact_sha256": {"rf": "a" * 64, "xgb": "b" * 64},
                "method": "sigmoid",
                "fit_partition": "validation",
                "calibration_input_sha256": "c" * 64,
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "n_calibrators": 3,
                "artifact_sha256": "d" * 64,
            },
            "target": {"classes": [0, 1, 2], "class_order": [0, 1, 2]},
            "artifacts": [
                {"role": "rf", "sha256": "a" * 64},
                {"role": "xgb", "sha256": "b" * 64},
                {"role": "calibrator", "sha256": "d" * 64},
            ],
        }
        errors = validate_calibrator_binding(manifest)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_calibration_wrong_base_model(self):
        manifest = {
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "calibration": {
                "mode": "in_pipeline",
                "base_model_id": "mdl_DIFFERENT",
                "base_artifact_sha256": {"rf": "a" * 64, "xgb": "b" * 64},
                "method": "sigmoid",
                "fit_partition": "validation",
                "calibration_input_sha256": "c" * 64,
                "classes": [0, 1, 2],
                "class_order": [0, 1, 2],
                "n_calibrators": 3,
                "artifact_sha256": "d" * 64,
            },
            "target": {"classes": [0, 1, 2], "class_order": [0, 1, 2]},
            "artifacts": [
                {"role": "rf", "sha256": "a" * 64},
                {"role": "xgb", "sha256": "b" * 64},
                {"role": "calibrator", "sha256": "d" * 64},
            ],
        }
        errors = validate_calibrator_binding(manifest)
        assert len(errors) > 0
        assert any("base_model_id" in e for e in errors)

    def test_partition_consistency(self):
        manifest = {
            "target": {"class_order": [0, 1, 2]},
            "validation": {
                "partitions": {
                    "train": {
                        "row_start": 0,
                        "row_end": 2548,
                        "n_rows": 2548,
                        "class_counts": [1530, 340, 678],
                    },
                    "validation": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                    "calibration": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                    "test": {
                        "row_start": 3410,
                        "row_end": 4262,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                },
                "purge": {
                    "rows_between_partitions": 5,
                    "label_horizon_bars": 5,
                    "label_purge_satisfied": True,
                    "embargo_rows": 0,
                },
                "leakage_checks": {
                    "disjoint": True,
                    "purge_satisfied": True,
                    "labels_within_partition": True,
                },
            },
        }
        errors = validate_partition_consistency(manifest)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_partition_row_count_mismatch(self):
        manifest = {
            "target": {"class_order": [0, 1, 2]},
            "validation": {
                "partitions": {
                    "train": {
                        "row_start": 0,
                        "row_end": 2548,
                        "n_rows": 9999,
                        "class_counts": [1530, 340, 678],
                    },
                    "validation": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                    "calibration": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                    "test": {
                        "row_start": 3410,
                        "row_end": 4262,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                },
                "purge": {
                    "rows_between_partitions": 5,
                    "label_horizon_bars": 5,
                    "label_purge_satisfied": True,
                    "embargo_rows": 0,
                },
                "leakage_checks": {
                    "disjoint": True,
                    "purge_satisfied": True,
                    "labels_within_partition": True,
                },
            },
        }
        errors = validate_partition_consistency(manifest)
        assert len(errors) > 0
        assert any("n_rows" in e for e in errors)

    def test_partition_class_counts_sum_mismatch(self):
        manifest = {
            "target": {"class_order": [0, 1, 2]},
            "validation": {
                "partitions": {
                    "train": {
                        "row_start": 0,
                        "row_end": 2548,
                        "n_rows": 2548,
                        "class_counts": [100, 100, 100],
                    },
                    "validation": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                    "calibration": {
                        "row_start": 2553,
                        "row_end": 3405,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                    "test": {
                        "row_start": 3410,
                        "row_end": 4262,
                        "n_rows": 852,
                        "class_counts": [350, 255, 247],
                    },
                },
                "purge": {
                    "rows_between_partitions": 5,
                    "label_horizon_bars": 5,
                    "label_purge_satisfied": True,
                    "embargo_rows": 0,
                },
                "leakage_checks": {
                    "disjoint": True,
                    "purge_satisfied": True,
                    "labels_within_partition": True,
                },
            },
        }
        errors = validate_partition_consistency(manifest)
        assert len(errors) > 0
        assert any("sum(class_counts)" in e for e in errors)


class TestEventValidation:
    def test_valid_first_event(self):
        event = {
            "sequence_number": 1,
            "previous_event_sha256": "0" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "sealed",
            "at": "2026-11-25T10:00:00Z",
            "manifest_sha256": "a" * 64,
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
            "previous_event_sha256": "a" * 64,
            "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
            "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
            "event": "validated",
            "at": "2026-11-25T10:00:00Z",
            "manifest_sha256": "b" * 64,
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
            "manifest_sha256": "a" * 64,
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
            "manifest_sha256": "a" * 64,
            "actor": "pipeline",
            "evidence": None,
        }
        errors = validate_event(event)
        assert len(errors) > 0
        assert any("Invalid event type" in e for e in errors)

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
