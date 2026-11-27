"""CP-A: explicit schema_version dispatch and 3.0.0 isolation (Fase A).

These tests verify observable dispatcher behaviour: which validator is called,
which one is never called, and the exact public ``list[str]`` result.  Real
historical validation of a complete 3.0.0 manifest remains covered by
``tests/test_provenance.py::TestManifestValidation::test_valid_manifest``.
"""

import inspect

import pytest

from tradingai.ml import provenance, provenance_v4
from tradingai.ml.provenance import (
    MANIFEST_VERSION_V3,
    MANIFEST_VERSION_V4,
    V4_PENDING_MESSAGE,
    ManifestVersionError,
    ManifestVersionNotImplementedError,
    ManifestVersionUnsupportedError,
    _validate_manifest_v3,
    validate_manifest,
)


def _forbid(name: str):
    """Build a spy that fails the test if the forbidden callable is invoked."""

    def _forbidden(*args, **kwargs):
        pytest.fail(f'forbidden validator {name} was invoked')

    return _forbidden


class TestV3RoutePreserved:
    def test_v3_dispatch_reaches_frozen_validator_with_same_object(self, monkeypatch):
        calls = []

        def _spy(manifest):
            calls.append(manifest)
            return []

        monkeypatch.setattr(provenance, '_validate_manifest_v3', _spy)
        manifest = {'schema_version': MANIFEST_VERSION_V3}
        assert validate_manifest(manifest) == []
        assert calls == [manifest]

    def test_invalid_v3_manifest_keeps_historical_messages(self):
        manifest = {'schema_version': MANIFEST_VERSION_V3}
        historical = _validate_manifest_v3(manifest)
        actual = validate_manifest(manifest)
        assert actual == historical
        assert any("'model_id' is a required property" in e for e in actual)
        assert any('Missing partition: train' in e for e in actual)
        assert any('n_calibrators != len(classes)' in e for e in actual)

    def test_v3_route_is_the_only_route_for_v3(self, monkeypatch):
        original = provenance._validate_manifest_v3
        manifest = {'schema_version': MANIFEST_VERSION_V3}
        expected = original(manifest)
        calls = []
        schema_calls = []
        original_schema = provenance.validate_schema

        def _wrapped(manifest):
            calls.append(manifest)
            return original(manifest)

        def _schema_spy(*args, **kwargs):
            schema_calls.append((args, kwargs))
            return original_schema(*args, **kwargs)

        monkeypatch.setattr(provenance, '_validate_manifest_v3', _wrapped)
        monkeypatch.setattr(provenance, 'validate_schema', _schema_spy)
        assert validate_manifest(manifest) == expected
        assert calls == [manifest]
        assert len(schema_calls) == 1

    def test_v3_extra_v4_field_is_rejected_by_historical_contract(self):
        manifest = {'schema_version': MANIFEST_VERSION_V3, 'source_position_start': 0}
        errors = validate_manifest(manifest)
        assert any('source_position_start' in e for e in errors)


class TestV4Delegation:
    """Fase B replaced the Fase A pending error with real v4 validation."""

    def test_v4_delegates_to_v4_validator(self, monkeypatch):
        calls = []

        def _spy(manifest):
            calls.append(manifest)
            return []

        monkeypatch.setattr(provenance_v4, 'validate_manifest_v4', _spy)
        manifest = {'schema_version': MANIFEST_VERSION_V4}
        assert validate_manifest(manifest) == []
        assert calls == [manifest]

    def test_v4_does_not_call_any_v3_validator(self, monkeypatch):
        monkeypatch.setattr(provenance, '_validate_manifest_v3', _forbid('_validate_manifest_v3'))
        monkeypatch.setattr(provenance, 'validate_schema', _forbid('validate_schema'))
        monkeypatch.setattr(
            provenance,
            'validate_partition_consistency',
            _forbid('validate_partition_consistency'),
        )
        monkeypatch.setattr(
            provenance,
            'validate_calibrator_binding',
            _forbid('validate_calibrator_binding'),
        )
        manifest = {
            'schema_version': MANIFEST_VERSION_V4,
            'model_id': 'invalid',
            'unknown_field': 'value',
        }
        errors = validate_manifest(manifest)
        assert isinstance(errors, list) and errors
        assert all(isinstance(error, str) for error in errors)
        assert V4_PENDING_MESSAGE not in errors
        assert any('model_id' in error for error in errors)

    def test_v4_dispatch_typed_internal_error(self):
        with pytest.raises(ManifestVersionNotImplementedError, match='Fase B'):
            provenance._dispatch_manifest_version({'schema_version': MANIFEST_VERSION_V4})
        assert issubclass(ManifestVersionNotImplementedError, ManifestVersionError)

    def test_no_partial_validation_no_defaults_and_no_mutation(self):
        manifest = {
            'schema_version': MANIFEST_VERSION_V4,
            'model_id': 42,
            'artifacts': 'not-a-list',
            'extensions': {'x.y': {}},
        }
        before = dict(manifest)
        errors = validate_manifest(manifest)
        assert errors
        assert V4_PENDING_MESSAGE not in errors
        assert 'Invalid model_id format' not in errors  # v3 body message never applied
        assert manifest == before


class TestInvalidVersions:
    @pytest.mark.parametrize(
        'manifest',
        [
            {},
            {'schema_version': None},
            {'schema_version': 3.0},
            {'schema_version': 3},
            {'schema_version': ''},
            {'schema_version': '1.0.0'},
            {'schema_version': '4.0.1'},
            {'schema_version': ' 3.0.0 '},
            {'schema_version': ['3.0.0']},
            {'schema_version': {'v': '3.0.0'}},
            {'schema_version': True},
            {'schema_version': '3.0.0\n'},
        ],
    )
    def test_unknown_or_malformed_version_is_rejected(self, monkeypatch, manifest):
        monkeypatch.setattr(provenance, '_validate_manifest_v3', _forbid('_validate_manifest_v3'))
        monkeypatch.setattr(provenance, 'validate_schema', _forbid('validate_schema'))
        errors = validate_manifest(manifest)
        assert len(errors) == 1
        assert 'schema_version' in errors[0].lower()
        assert errors[0] != V4_PENDING_MESSAGE
        assert all('is a required property' not in e for e in errors)

    def test_unknown_version_does_not_fall_back_to_v3(self):
        manifest = {'schema_version': '9.9.9', 'model_id': 'invalid'}
        historical_result = _validate_manifest_v3(manifest)
        errors = validate_manifest(manifest)
        assert errors != historical_result
        assert len(errors) == 1
        assert 'Unsupported schema_version' in errors[0]

    def test_missing_version_keeps_model_id_substring_without_v3_call(self, monkeypatch):
        monkeypatch.setattr(provenance, '_validate_manifest_v3', _forbid('_validate_manifest_v3'))
        errors = validate_manifest({'model_id': 'invalid'})
        assert len(errors) == 1
        assert 'model_id' in errors[0]


class TestRobustness:
    @pytest.mark.parametrize('value', [None, [], 'manifest', 42, object()])
    def test_non_object_inputs_return_list_without_raising(self, value):
        errors = validate_manifest(value)
        assert isinstance(errors, list)
        assert len(errors) == 1
        assert isinstance(errors[0], str)

    def test_public_contract_is_preserved(self):
        assert list(inspect.signature(validate_manifest).parameters) == ['manifest']
        for manifest in (
            {'schema_version': MANIFEST_VERSION_V3},
            {'schema_version': MANIFEST_VERSION_V4},
            {},
        ):
            errors = validate_manifest(manifest=manifest)
            assert isinstance(errors, list)
            assert all(isinstance(e, str) for e in errors)

    def test_unsupported_version_uses_typed_internal_error(self):
        with pytest.raises(ManifestVersionUnsupportedError, match='schema_version'):
            provenance._dispatch_manifest_version({'schema_version': 'unknown'})
        assert issubclass(ManifestVersionUnsupportedError, ManifestVersionError)
