"""Fase B: 4.0.0 JSON Schema and structural validators (CP-B evidence)."""

from __future__ import annotations

import copy

import pytest

from tradingai.ml import provenance
from tradingai.ml.provenance import parse_json_strict, validate_manifest
from tradingai.ml.provenance_v4 import (
    MANIFEST_SCHEMA_V4,
    MAX_SAFE_INTEGER,
    validate_actor_v4,
    validate_evidence_v4,
    validate_manifest_v4,
    validate_model_id_v4,
    validate_reason_code_v4,
    validate_schema_v4,
    validate_sha256_v4,
    validate_sidecar_id_v4,
    validate_timestamp_v4,
    validate_ulid_v4,
)

MODEL_ID = 'mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W'
OTHER_MODEL_ID = 'mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X'
SIDECAR_ID = 'sig_01JQ8Z4A1B2C3D4E5F6G7H8J9K'
EVENT_ID = 'evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K'


def _partition(row_start: int, row_end: int, source_start: int, source_end: int, digest: str):
    return {
        'row_start': row_start,
        'row_end': row_end,
        'source_position_start': source_start,
        'source_position_end': source_end,
        'n_rows': row_end - row_start,
        'time_start': '2026-01-01T00:00:00Z',
        'time_end': '2026-04-17T03:00:00Z',
        'class_counts': [2, 1, 1],
        'index_sha256': digest,
    }


def _valid_manifest() -> dict:
    """Fictitious, self-consistent 4.0.0 manifest used only for validation tests."""
    manifest = {
        'schema_version': '4.0.0',
        'model_id': MODEL_ID,
        'created_at': '2026-11-25T18:00:00.000000Z',
        'sealed_at': '2026-11-25T18:04:12.345678Z',
        'status_at_seal': 'sealed',
        'run_fingerprint': 'a' * 64,
        'git': {
            'commit': '0' * 40,
            'dirty': False,
            'branch': 'main',
            'tag': None,
            'source_bundle_sha256': 'b' * 64,
        },
        'producer': {
            'name': 'tradingai-btc',
            'version': '0.2.0',
            'python': '3.13.15',
            'command': 'python -m tradingai.ml.train',
            'config_sha256': 'c' * 64,
        },
        'data': {
            'symbol': 'BTC/USDT',
            'timeframe': '1h',
            'provider': 'binance',
            'provider_version': '2026.11',
            'dataset_sha256': 'd' * 64,
            'snapshot_uri': 'data/store/sha256/01/deadbeef.parquet',
            'raw_rows': 100,
            'feature_rows': 90,
            'labeled_rows': 80,
            'time_range': {
                'start': '2026-01-01T00:00:00Z',
                'end': '2026-04-17T03:00:00Z',
                'timezone': 'UTC',
            },
            'missing_data_policy': 'drop_incomplete_bars',
            'gap_policy': 'no_synthetic_fill',
            'ohlcv_schema_version': '1.0.0',
            'alignment': 'left_closed_right_open',
        },
        'target': {
            'name': 'future_return_threshold',
            'horizon_bars': 3,
            'vol_mult': '0.5',
            'classes': [0, 1, 2],
            'class_order': [0, 1, 2],
            'rule_sha256': 'e' * 64,
            'nan_policy': 'drop_label',
        },
        'features': {
            'ordered': ['feat_01', 'feat_02'],
            'count': 2,
            'definition_sha256': 'f' * 64,
            'matrix_sha256': '1' * 64,
            'pipeline_version': '2.0.0',
            'code_sha256': '2' * 64,
            'parameters': {'lookback_max': 50},
            'nan_policy': 'dropna_before_split',
        },
        'training': {
            'task': 'multiclass_classification',
            'models': {
                'rf': {'library': 'scikit-learn', 'version': '1.9.1', 'params': {}},
                'xgb': {'library': 'xgboost', 'version': '3.4.1', 'params': {}},
            },
            'ensemble': {'method': 'mean_probability', 'weights': {'rf': '0.5', 'xgb': '0.5'}},
            'seed': 42,
            'environment': {
                'python': '3.13.15',
                'numpy': '2.5.5',
                'pandas': '3.1.1',
                'scikit_learn': '1.9.1',
                'xgboost': '3.4.1',
                'joblib': '1.6.0',
                'os': 'Windows-11',
                'arch': 'x86_64',
                'cuda_version': None,
            },
            'hardware': {
                'device': 'cpu',
                'gpu_model': None,
                'cuda_version': None,
                'cpu_count': 16,
                'ram_gb': 32,
            },
            'determinism': {
                'bitwise_reproducible': True,
                'n_jobs': 1,
                'omp_num_threads': 1,
                'xgb_tree_method': 'hist',
                'xgb_deterministic_histogram': True,
                'gpu_deterministic': False,
            },
        },
        'validation': {
            'split_method': 'chronological_holdout',
            'partitions': {
                'train': _partition(0, 4, 0, 5, '3' * 64),
                'validation': _partition(4, 8, 10, 13, '4' * 64),
                'calibration': _partition(4, 8, 10, 13, '4' * 64),
                'test': _partition(8, 12, 20, 23, '6' * 64),
            },
            'purge': {
                'rows_between_partitions': 5,
                'label_horizon_bars': 3,
                'label_purge_satisfied': True,
                'embargo_rows': 2,
            },
            'partition_manifest_sha256': '7' * 64,
            'leakage_checks': {
                'disjoint': True,
                'purge_satisfied': True,
                'labels_within_partition': True,
            },
            'evaluation': {
                'metric_spec_version': '1.0.0',
                'primary_metric': 'macro_f1',
                'test_evaluated_once': True,
                'evaluation_code_sha256': '8' * 64,
                'evaluated_at': '2026-11-25T18:04:12.345678Z',
            },
        },
        'calibration': {
            'mode': 'in_pipeline',
            'base_model_id': MODEL_ID,
            'base_artifact_sha256': {'rf': 'd' * 64, 'xgb': 'e' * 64},
            'method': 'sigmoid',
            'fit_partition': 'validation',
            'calibration_input_sha256': 'b' * 64,
            'classes': [0, 1, 2],
            'class_order': [0, 1, 2],
            'n_calibrators': 3,
            'artifact_sha256': 'f' * 64,
        },
        'artifacts': [
            {
                'role': 'rf',
                'path': 'rf.joblib',
                'sha256': 'd' * 64,
                'bytes': 1000,
                'media_type': 'application/octet-stream',
                'format': 'joblib-pickle',
                'serializer': '1.6.0',
            },
            {
                'role': 'xgb',
                'path': 'xgb.joblib',
                'sha256': 'e' * 64,
                'bytes': 1000,
                'media_type': 'application/octet-stream',
                'format': 'joblib-pickle',
                'serializer': '3.4.1',
            },
            {
                'role': 'calibrator',
                'path': 'calibrator.joblib',
                'sha256': 'f' * 64,
                'bytes': 1000,
                'media_type': 'application/octet-stream',
                'format': 'joblib-pickle',
                'serializer': '1.6.0',
            },
        ],
        'metrics': {'path': 'metrics.json', 'sha256': '1' * 64, 'schema_version': '1.0.0'},
        'extensions': {},
    }
    manifest['validation']['partitions']['calibration']['shared_with'] = 'validation'
    return manifest


class TestSchemaV4:
    def test_valid_v4_manifest_is_accepted(self):
        assert validate_manifest_v4(_valid_manifest()) == []

    def test_schema_is_definitive_v4_not_v3(self):
        assert MANIFEST_SCHEMA_V4['$id'].endswith('manifest-v4.json')
        assert MANIFEST_SCHEMA_V4['properties']['schema_version']['const'] == '4.0.0'
        assert MANIFEST_SCHEMA_V4 is not provenance.MANIFEST_SCHEMA
        assert validate_schema_v4({'schema_version': '3.0.0'})

    def test_wrapper_uses_v4_route(self, monkeypatch):
        def _forbidden(*args, **kwargs):
            pytest.fail('v3 validator invoked for a 4.0.0 manifest')

        monkeypatch.setattr(provenance, '_validate_manifest_v3', _forbidden)
        manifest = _valid_manifest()
        assert validate_manifest(manifest) == []

    def test_missing_required_field_is_rejected(self):
        manifest = _valid_manifest()
        del manifest['training']['environment']['numpy']
        errors = validate_manifest_v4(manifest)
        assert any('numpy' in error for error in errors)

    def test_unknown_root_and_nested_fields_are_rejected(self):
        manifest = _valid_manifest()
        manifest['unexpected_root'] = 1
        manifest['git']['unexpected_git'] = 2
        errors = validate_manifest_v4(manifest)
        assert any('unexpected_root' in error for error in errors)
        assert any('unexpected_git' in error for error in errors)

    def test_wrong_types_are_rejected(self):
        manifest = _valid_manifest()
        manifest['target']['horizon_bars'] = True
        manifest['data']['raw_rows'] = '100'
        errors = validate_manifest_v4(manifest)
        assert errors

    def test_extensions_must_be_empty(self):
        manifest = _valid_manifest()
        assert validate_manifest_v4(manifest) == []
        manifest['extensions'] = {'x.y': {}}
        errors = validate_manifest_v4(manifest)
        assert any('extensions' in error for error in errors)

    def test_null_is_rejected_where_not_nullable(self):
        manifest = _valid_manifest()
        assert validate_manifest_v4(manifest) == []
        manifest['model_id'] = None
        assert validate_manifest_v4(manifest)
        restored = _valid_manifest()
        restored['git']['branch'] = None
        assert validate_manifest_v4(restored) == []

    def test_shared_with_and_fit_partition_are_constrained(self):
        manifest = _valid_manifest()
        del manifest['validation']['partitions']['calibration']['shared_with']
        assert validate_manifest_v4(manifest)
        manifest = _valid_manifest()
        manifest['calibration']['fit_partition'] = 'test'
        assert validate_manifest_v4(manifest)

    def test_source_position_fields_are_required(self):
        manifest = _valid_manifest()
        del manifest['validation']['partitions']['train']['source_position_end']
        errors = validate_manifest_v4(manifest)
        assert any('source_position_end' in error for error in errors)

    def test_class_duplicates_are_rejected(self):
        manifest = _valid_manifest()
        manifest['target']['class_order'] = [0, 0, 2]
        assert validate_manifest_v4(manifest)


class TestStructuralValidators:
    def test_reason_code_pattern_boundaries(self):
        assert validate_reason_code_v4('a')
        assert validate_reason_code_v4('a' + 'b' * 63)
        assert not validate_reason_code_v4('A')
        assert not validate_reason_code_v4('a b')
        assert not validate_reason_code_v4('ñ')
        assert not validate_reason_code_v4('a' * 65)
        assert not validate_reason_code_v4(None)

    def test_actor_namespace_pattern(self):
        assert validate_actor_v4('human:alice')
        assert validate_actor_v4('service:bot.1-2_3')
        assert not validate_actor_v4('pipeline')
        assert not validate_actor_v4('admin:alice')
        assert not validate_actor_v4('human:')
        assert not validate_actor_v4('human:á')

    def test_hash_and_ulid_patterns(self):
        assert validate_sha256_v4('a' * 64)
        assert not validate_sha256_v4('A' * 64)
        assert validate_ulid_v4('01JQ8Z3K4M5N6P7Q8R9S0T1V2W')
        assert not validate_ulid_v4('8' + '0' * 25)
        assert validate_model_id_v4(MODEL_ID)
        assert validate_sidecar_id_v4(SIDECAR_ID)
        assert not validate_sidecar_id_v4(EVENT_ID)

    def test_safe_integer_bounds(self):
        manifest = _valid_manifest()
        manifest['training']['seed'] = MAX_SAFE_INTEGER
        assert validate_manifest_v4(manifest) == []
        manifest['training']['seed'] = MAX_SAFE_INTEGER + 1
        errors = validate_manifest_v4(manifest)
        assert any('training.seed' in error for error in errors)
        assert any('safe range' in error for error in errors)

    def test_timestamp_format_check(self):
        assert validate_timestamp_v4('2026-11-25T18:00:00Z')
        assert validate_timestamp_v4('2026-11-25T18:00:00.123456789Z')
        assert validate_timestamp_v4('2026-11-25T12:00:00-06:00')
        assert not validate_timestamp_v4('2026-11-25T18:00:00')
        assert not validate_timestamp_v4('2026-11-25T18:00:00-00:00')
        assert not validate_timestamp_v4('2026-11-25T18:00:00.1234567890Z')
        assert not validate_timestamp_v4('2026-11-25T18:00:60Z')
        assert not validate_timestamp_v4('2026-02-30T18:00:00Z')

    def test_strict_json_parsing_rejects_non_finite_and_duplicates(self):
        from tradingai.ml.provenance import StrictJSONError

        with pytest.raises(StrictJSONError):
            parse_json_strict('{"a": NaN}')
        with pytest.raises(StrictJSONError):
            parse_json_strict('{"a": 1, "a": 2}')


class TestEvidenceV4:
    def test_sealed_requires_null(self):
        assert validate_evidence_v4('sealed', None) == []
        assert validate_evidence_v4('sealed', {'report_sha256': 'a' * 64})

    def test_validated_evidence(self):
        valid = {'report_sha256': 'a' * 64, 'signature_sidecar_id': SIDECAR_ID}
        assert validate_evidence_v4('validated', valid) == []
        assert validate_evidence_v4('validated', {**valid, 'extra': 1})
        assert validate_evidence_v4('validated', {'report_sha256': 'A' * 64,
                                                  'signature_sidecar_id': SIDECAR_ID})

    def test_approved_and_rejected_evidence(self):
        assert validate_evidence_v4(
            'approved', {'approval_ref': 'APP-1', 'signature_sidecar_id': SIDECAR_ID}
        ) == []
        assert validate_evidence_v4(
            'approved', {'approval_ref': '  APP-1  ', 'signature_sidecar_id': SIDECAR_ID}
        )
        assert validate_evidence_v4(
            'rejected',
            {'reason_code': 'bad_data', 'report_sha256': 'a' * 64,
             'signature_sidecar_id': SIDECAR_ID},
        ) == []

    def test_deprecated_and_revoked_evidence(self):
        assert validate_evidence_v4(
            'deprecated', {'reason_code': 'superseded', 'replacement_model_id': OTHER_MODEL_ID},
            model_id=MODEL_ID,
        ) == []
        assert validate_evidence_v4(
            'deprecated', {'reason_code': 'superseded', 'replacement_model_id': MODEL_ID},
            model_id=MODEL_ID,
        )
        assert validate_evidence_v4(
            'revoked', {'reason_code': 'incident_7', 'incident_ref': 'INC-7'}
        ) == []

    def test_unknown_event_type_is_rejected(self):
        errors = validate_evidence_v4('unknown', None)
        assert errors and 'unsupported event type' in errors[0]


class TestInvariants:
    def test_determinism_and_no_mutation(self):
        manifest = _valid_manifest()
        before = copy.deepcopy(manifest)
        first = validate_manifest_v4(manifest)
        second = validate_manifest_v4(manifest)
        assert first == second == []
        assert manifest == before

    def test_calibration_binding_relations(self):
        manifest = _valid_manifest()
        manifest['calibration']['base_model_id'] = OTHER_MODEL_ID
        assert any('base_model_id' in e for e in validate_manifest_v4(manifest))

        manifest = _valid_manifest()
        manifest['calibration']['mode'] = 'external_run'
        manifest['calibration']['base_model_id'] = MODEL_ID
        assert any('base_model_id' in e for e in validate_manifest_v4(manifest))

        manifest = _valid_manifest()
        manifest['calibration']['base_artifact_sha256']['rf'] = '9' * 64
        assert any('base_artifact_sha256.rf' in e for e in validate_manifest_v4(manifest))

    def test_v3_fixture_is_not_accepted_as_v4(self):
        manifest = _valid_manifest()
        manifest['schema_version'] = '3.0.0'
        errors = validate_manifest_v4(manifest)
        assert any('schema_version' in error for error in errors)
