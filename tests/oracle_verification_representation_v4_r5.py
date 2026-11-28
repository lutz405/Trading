"""Representación independiente de verificación del oracle normativo v4 R5.

Fuentes exclusivas: R13-PHASE-C-DESIGN-R9 §5.4, diseño v4 §9.2, schema v4 y
decisiones D1-D6 aprobadas. No lee ORACLE-ART-01, 02, 03 ni 05; no importa
módulos productivos y no añade dependencias. Solo habilita la verificación
posterior de los metadatos (ORACLE-ART-06) y de la mutación controlada
(ORACLE-ART-07).
"""

from __future__ import annotations

import copy
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parents[1]
R9_PATH = REPO_ROOT / "docs" / "r13_phase_c_design_r9.md"
DESIGN_PATH = REPO_ROOT / "docs" / "aud04b_model_provenance_v4_design.md"
SCHEMA_PATH = REPO_ROOT / "src" / "tradingai" / "schemas" / "manifest_v4.json"

VERSION = "ORACLE_NORMATIVE_V4_R5"
PARTITIONS = ("train", "validation", "calibration", "test")
MUTATION_PATHS = (
    "calibration.base_model_id",
    "calibration.base_artifact_sha256.rf",
    "calibration.base_artifact_sha256.xgb",
)

METADATA_FIELDS = (
    "path",
    "type",
    "manifest_required",
    "manifest_required_when",
    "manifest_allowed_when",
    "projection_include_when",
    "projection_optional",
    "nullable",
    "normalization",
)

_MISSING = object()

_TYPES_TO_STRING = {"string", "string_decimal", "timestamp"}
_SCHEMA_TYPE = {
    "string": "string",
    "string_decimal": "string",
    "timestamp": "string",
    "integer": "integer",
    "number": "number",
    "boolean": "boolean",
    "array": "array",
    "object": "object",
}


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _section(lines: list[str], start: str, end: str) -> list[str]:
    a = next(i for i, line in enumerate(lines) if line.startswith(start))
    b = next(i for i, line in enumerate(lines) if line.startswith(end))
    return lines[a:b]


def _yes(value: str) -> bool:
    return value == "Sí"


def _optional(value: str) -> str | None:
    return None if value in ("—", "") else value


def parse_r9_allowlist() -> list[dict[str, Any]]:
    """Derivar los metadatos normativos de R9 §5.4, sin usar artefactos."""
    entries: list[dict[str, Any]] = []
    for line in _section(_read_lines(R9_PATH), "### 5.4 ", "### 5.5 "):
        if not line.startswith("| `"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 9 or cells[0] == "Ruta":
            continue
        path, typ, mr, mrw, maw, piw, po, nul, norm = cells[:9]
        metadata = {
            "path": path,
            "type": typ,
            "manifest_required": _yes(mr),
            "manifest_required_when": _optional(mrw),
            "manifest_allowed_when": _optional(maw),
            "projection_include_when": piw,
            "projection_optional": _yes(po),
            "nullable": _yes(nul),
            "normalization": norm,
        }
        expanded = (
            [path.replace("{partition}", p) for p in PARTITIONS]
            if "{partition}" in path
            else [path]
        )
        for concrete in expanded:
            item = dict(metadata)
            item["path"] = concrete
            entries.append(item)
    return sorted(entries, key=lambda e: e["path"])


def parse_design_rules() -> dict[str, str]:
    """Derivar `rule_id` por ruta desde las filas de diseño v4 §9.2 (D1)."""
    mapping: dict[str, str] = {}
    rows: list[str] = []
    for line in _section(_read_lines(DESIGN_PATH), "### 9.2 ", "### 9.3 "):
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cell = line.strip().strip("|").split("|")[0].strip()
        if cell.startswith("Rutas exactas"):
            continue
        rows.append(cell)
    for index, cell in enumerate(rows, start=1):
        rule_id = f"R9-9.2-{index:02d}"
        if "para cada partición" in cell:
            mapping["validation.split_method"] = rule_id
            for p in PARTITIONS:
                for field in (
                    "row_start",
                    "row_end",
                    "source_position_start",
                    "source_position_end",
                    "n_rows",
                    "time_start",
                    "time_end",
                    "class_counts",
                    "index_sha256",
                    "shared_with",
                ):
                    mapping[f"validation.partitions.{p}.{field}"] = rule_id
            continue
        for token in cell.split(","):
            token = token.strip().strip("`")
            if token and "artifacts[]" not in token:
                mapping[token] = rule_id
    return mapping


def expected_entries() -> list[dict[str, Any]]:
    """Representación esperada: nueve metadatos por ruta y `rule_id` separado."""
    rules = parse_design_rules()
    result: list[dict[str, Any]] = []
    for metadata in parse_r9_allowlist():
        path = metadata["path"]
        if path not in rules:
            raise ValueError(f"UNMAPPED_RULE:{path}")
        result.append({
            "path": path,
            "metadata": {field: metadata[field] for field in METADATA_FIELDS},
            "rule_id": rules[path],
        })
    return result


def _schema_node(path: str, schema: dict[str, Any]) -> dict[str, Any]:
    if path.startswith("validation.partitions."):
        parts = path.split(".")
        partition = parts[2]
        field = parts[3]
        ref = schema["properties"]["validation"]["properties"]["partitions"]["properties"][partition]["$ref"]
        definition = schema["$defs"][ref.rsplit("/", 1)[-1]]
        if field == "shared_with" and "shared_with" not in definition["properties"]:
            # El schema prohíbe esta ruta fuera de calibration; se representa
            # como tipo string no anulable para contrastar metadatos sin
            # inventar una propiedad inexistente.
            return {"type": "string"}
        return definition["properties"][field]
    node: dict[str, Any] = schema
    for part in path.split("."):
        node = node["properties"][part]
    return node


def schema_consistency_errors(entries: list[dict[str, Any]] | None = None) -> list[str]:
    """Contrastar tipos y nulabilidad de la representación contra el schema v4."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    for item in entries or expected_entries():
        path = item["path"]
        node = _schema_node(path, schema)
        if path.startswith("validation.partitions.") and path.endswith(".shared_with"):
            condition = "partition == 'calibration'"
            if item["metadata"]["manifest_required_when"] != condition:
                errors.append(f"REQUIRED_WHEN_MISMATCH:{path}")
            if item["metadata"]["manifest_allowed_when"] != condition:
                errors.append(f"ALLOWED_WHEN_MISMATCH:{path}")
        raw_type = node.get("type")
        types = [raw_type] if isinstance(raw_type, str) else list(raw_type or [])
        nullable = "null" in types
        concrete = [t for t in types if t != "null"]
        expected_type = _SCHEMA_TYPE[item["metadata"]["type"]]
        if concrete and concrete[0] != expected_type:
            errors.append(f"TYPE_MISMATCH:{path}:{concrete[0]}:{expected_type}")
        if nullable != item["metadata"]["nullable"]:
            errors.append(f"NULLABILITY_MISMATCH:{path}:{nullable}:{item['metadata']['nullable']}")
    return sorted(errors)


def _flatten(entry: dict[str, Any]) -> dict[str, Any]:
    if "metadata" in entry:
        flat = dict(entry["metadata"])
        if "rule_id" in entry:
            flat["rule_id"] = entry["rule_id"]
        return flat
    return dict(entry)


def compare_observed(observed: list[dict[str, Any]]) -> list[str]:
    """Comparar una observación con la representación normativa independiente."""
    expected = expected_entries()
    expected_paths = [item["path"] for item in expected]
    observed_flat = [_flatten(item) for item in observed]
    observed_paths = [item.get("path") for item in observed_flat]
    errors: list[str] = []
    if len(observed_paths) != len(set(observed_paths)):
        errors.append("DUPLICATE_PATH")
    expected_set, observed_set = set(expected_paths), set(observed_paths)
    for path in sorted(expected_set - observed_set):
        errors.append(f"MISSING_PATH:{path}")
    for path in sorted(observed_set - expected_set):
        errors.append(f"EXTRA_PATH:{path}")
    observed_by_path = {item["path"] if "path" in item else None: item for item in observed_flat}
    known_fields = set(METADATA_FIELDS) | {"rule_id"}
    for item in expected:
        path = item["path"]
        if path not in observed_by_path:
            continue
        actual = observed_by_path[path]
        for field in sorted(set(actual) - known_fields):
            errors.append(f"UNKNOWN_FIELD:{path}:{field}")
        for field in METADATA_FIELDS:
            observed_value = actual[field] if field in actual else _MISSING
            expected_value = item["metadata"][field]
            if observed_value is _MISSING:
                errors.append(f"METADATA_MISSING:{path}:{field}")
            elif observed_value != expected_value:
                errors.append(
                    f"METADATA_DIVERGENCE:{path}:{field}:expected={expected_value!r}:observed={observed_value!r}"
                )
        observed_rule = actual["rule_id"] if "rule_id" in actual else _MISSING
        if observed_rule is _MISSING:
            errors.append(f"RULE_MISSING:{path}")
        elif observed_rule != item["rule_id"]:
            errors.append(f"RULE_DIVERGENCE:{path}:{item['rule_id']}:{observed_rule}")
    return sorted(errors)


@contextmanager
def isolated_external_run_only_mutation(
    entries: list[dict[str, Any]],
) -> Iterator[list[dict[str, Any]]]:
    """Copia aislada y reversible de la mutación normativa autorizada."""
    if not isinstance(entries, list) or not entries:
        raise ValueError("ISOLATION_FAILED:INVALID_INPUT")
    original = copy.deepcopy(entries)
    observed_paths = {item.get("path") for item in original}
    if not set(MUTATION_PATHS).issubset(observed_paths):
        raise ValueError("ISOLATION_FAILED:MISSING_MUTATION_PATH")
    mutated = copy.deepcopy(original)
    for item in mutated:
        if item["path"] in MUTATION_PATHS:
            item["metadata"]["projection_include_when"] = "always"
    try:
        yield mutated
    finally:
        mutated.clear()
        copy.deepcopy(original)


def mutation_detection_evidence(mutated: list[dict[str, Any]]) -> dict[str, Any]:
    """Detectar la mutación controlada sin modificar la representación esperada."""
    flat = [_flatten(item) for item in mutated]
    by_path = {item.get("path"): item for item in flat}
    detected: list[str] = []
    for path in MUTATION_PATHS:
        actual = by_path.get(path, {}).get("projection_include_when")
        if actual == "always":
            detected.append(path)
    return {
        "status": "DETECTED" if len(detected) == len(MUTATION_PATHS) else "NOT_DETECTED",
        "detected_paths": sorted(detected),
        "expected_paths": sorted(MUTATION_PATHS),
        "version": VERSION,
    }
