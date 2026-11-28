"""Pruebas de la representación independiente de verificación del oracle v4 R5."""

from __future__ import annotations

from pathlib import Path

import pytest

import oracle_verification_representation_v4_r5 as representation


MODULE_PATH = Path(__file__).resolve().parent / "oracle_verification_representation_v4_r5.py"


def test_representation_is_deterministic_and_complete() -> None:
    first = representation.expected_entries()
    second = representation.expected_entries()
    assert first == second
    assert len(first) == 139
    assert len({item["path"] for item in first}) == 139
    assert [item["path"] for item in first] == sorted(item["path"] for item in first)


def test_rule_ids_are_independent_and_traceable() -> None:
    entries = representation.expected_entries()
    rules = {item["rule_id"] for item in entries}
    assert len(rules) == 13
    assert all(rule.startswith("R9-9.2-") for rule in rules)
    assert len(set(representation.parse_design_rules().values())) == 24
    assert all(set(item["metadata"]) == set(representation.METADATA_FIELDS) for item in entries)
    assert all("rule_id" not in item["metadata"] for item in entries)


def test_schema_consistency() -> None:
    assert representation.schema_consistency_errors() == []


def test_compare_observed_detects_divergences() -> None:
    expected = representation.expected_entries()
    flat = [{**item["metadata"], "rule_id": item["rule_id"]} for item in expected]
    assert representation.compare_observed(flat) == []

    divergent = [{**dict(item), "rule_id": item["rule_id"]} for item in flat]
    divergent[0]["type"] = "number"
    errors = representation.compare_observed(divergent)
    assert any(error.startswith("METADATA_DIVERGENCE:") for error in errors)

    missing = [dict(item) for item in flat[:-1]]
    assert any(error.startswith("MISSING_PATH:") for error in representation.compare_observed(missing))

    extra = [dict(item) for item in flat] + [{"path": "extra.path"}]
    assert any(error.startswith("EXTRA_PATH:") for error in representation.compare_observed(extra))


def test_mutation_is_detected_and_isolated() -> None:
    original = representation.expected_entries()
    before = representation.compare_observed(
        [{**item["metadata"], "rule_id": item["rule_id"]} for item in original]
    )
    assert before == []
    with representation.isolated_external_run_only_mutation(original) as mutated:
        evidence = representation.mutation_detection_evidence(mutated)
    assert evidence["status"] == "DETECTED"
    assert evidence["detected_paths"] == sorted(representation.MUTATION_PATHS)
    after = representation.compare_observed(
        [{**item["metadata"], "rule_id": item["rule_id"]} for item in original]
    )
    assert after == []


def test_mutation_fails_closed_on_unisolated_input() -> None:
    with pytest.raises(ValueError, match="ISOLATION_FAILED"):
        with representation.isolated_external_run_only_mutation([]):
            pass


def test_representation_has_no_production_or_artifact_dependencies() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "from tradingai" not in source
    assert "import tradingai" not in source
    assert "docs/oracle_artifacts" not in source
    assert "ORACLE-ART-01.json" not in source
    assert "ORACLE-ART-02.json" not in source
    assert "ORACLE-ART-03.json" not in source
    assert "ORACLE-ART-05.json" not in source
    assert "rfc8785" not in source


def _flat_expected() -> list[dict[str, object]]:
    return [
        {**item["metadata"], "rule_id": item["rule_id"]}
        for item in representation.expected_entries()
    ]


def test_auditor_case_absent_manifest_required_when_is_detected() -> None:
    """Caso reproducido por la auditoría: ausencia con valor esperado None."""
    flat = _flat_expected()
    index = next(
        i for i, item in enumerate(flat) if item["manifest_required_when"] is None
    )
    path = flat[index]["path"]
    del flat[index]["manifest_required_when"]
    errors = representation.compare_observed(flat)
    assert f"METADATA_MISSING:{path}:manifest_required_when" in errors
    assert errors == representation.compare_observed(flat)


def test_present_none_matches_expected_none() -> None:
    flat = _flat_expected()
    index = next(
        i for i, item in enumerate(flat) if item["manifest_required_when"] is None
    )
    flat[index]["manifest_required_when"] = None
    errors = representation.compare_observed(flat)
    assert not [error for error in errors if "manifest_required_when" in error]
    assert errors == []


def test_present_concrete_value_is_compared_and_reported_by_path_field() -> None:
    flat = _flat_expected()
    path = flat[0]["path"]
    flat[0]["type"] = "number"
    errors = representation.compare_observed(flat)
    assert any(
        error.startswith(f"METADATA_DIVERGENCE:{path}:type:") for error in errors
    )
    assert errors == representation.compare_observed(flat)


def test_absent_required_metadata_never_passes() -> None:
    flat = _flat_expected()
    index = next(i for i, item in enumerate(flat) if item["manifest_required"] is True)
    path = flat[index]["path"]
    del flat[index]["manifest_required"]
    errors = representation.compare_observed(flat)
    assert f"METADATA_MISSING:{path}:manifest_required" in errors


def test_unknown_and_missing_rule_fields_fail_closed() -> None:
    flat = _flat_expected()
    path = flat[0]["path"]
    flat[0]["campo_desconocido"] = "x"
    del flat[0]["rule_id"]
    errors = representation.compare_observed(flat)
    assert f"UNKNOWN_FIELD:{path}:campo_desconocido" in errors
    assert f"RULE_MISSING:{path}" in errors


def _native_expected() -> list[dict[str, object]]:
    return [dict(item) for item in representation.expected_entries()]


def test_auditor_case_native_rule_id_absence_is_rule_missing() -> None:
    """Caso detectado por la auditoría: formato nativo sin rule_id outer."""
    native = _native_expected()
    path = native[0]["metadata"]["path"]
    expected_rule = native[0]["rule_id"]
    del native[0]["rule_id"]
    errors = representation.compare_observed(native)
    assert f"RULE_MISSING:{path}" in errors
    assert not [error for error in errors if f"observed={expected_rule}" in error]
    assert errors == representation.compare_observed(native)


def test_native_rule_id_present_none_is_divergence_not_absence() -> None:
    native = _native_expected()
    path = native[0]["metadata"]["path"]
    native[0]["rule_id"] = None
    errors = representation.compare_observed(native)
    assert any(error.startswith(f"RULE_DIVERGENCE:{path}:") for error in errors)
    assert not any(error.startswith(f"RULE_MISSING:{path}") for error in errors)


def test_native_rule_id_present_correct_has_no_errors() -> None:
    native = _native_expected()
    assert representation.compare_observed(native) == []
    assert representation.compare_observed(native) == representation.compare_observed(native)


def test_native_rule_id_divergent_is_reported() -> None:
    native = _native_expected()
    path = native[0]["metadata"]["path"]
    native[0]["rule_id"] = "R9-9.2-99"
    errors = representation.compare_observed(native)
    assert any(error.startswith(f"RULE_DIVERGENCE:{path}:") for error in errors)


def test_flat_rule_id_absence_and_divergence_remain_distinct() -> None:
    path = _flat_expected()[0]["path"]
    rule = _flat_expected()[0]["rule_id"]

    absent = _flat_expected()
    del absent[0]["rule_id"]
    errors_absent = representation.compare_observed(absent)
    assert f"RULE_MISSING:{path}" in errors_absent
    assert errors_absent == representation.compare_observed(absent)

    divergent = _flat_expected()
    divergent[0]["rule_id"] = "R9-9.2-99"
    errors_divergent = representation.compare_observed(divergent)
    assert any(
        error.startswith(f"RULE_DIVERGENCE:{path}:{rule}:")
        for error in errors_divergent
    )
    assert errors_divergent == representation.compare_observed(divergent)
