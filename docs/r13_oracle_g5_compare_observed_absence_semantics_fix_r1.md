# R13-ORACLE-G5-COMPARE-OBSERVED-ABSENCE-SEMANTICS-FIX-R1 — Corrección de semántica de ausencia en `compare_observed()`

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Hallazgo corregido:** `AUD-IMP-REP-R1-01` (MEDIUM), registrado en `docs/r13_audit_oracle_g5_independent_verification_representation_implementation_r1.md`.
**Alcance:** exclusivamente dos archivos en `tests/` y este informe.

---

## 1. Hallazgo original y causa raíz

El auditor reprodujo que `compare_observed()` usaba `actual.get(field)` frente al valor esperado. Cuando el valor normativo esperado era `None` —por ejemplo `manifest_required_when=None`—, un campo **ausente** en la observación devolvía también `None` y no generaba error. Evidencia original: al eliminar `manifest_required_when` de una entrada observada, la función devolvía `[]`.

**Causa raíz:** uso de `.get()` sin centinela, que colapsa dos estados distintos:

- clave ausente;
- clave presente con valor `None`.

**Consecuencia:** una observación incompleta podía recibir resultado limpio y convertirse en falso PASS durante la futura generación de ORACLE-ART-06.

---

## 2. Corrección implementada

Archivo modificado: `tests/oracle_verification_representation_v4_r5.py`.

1. Se eliminó el `import re` no utilizado.
2. Se añadió el centinela privado `_MISSING = object()`.
3. `compare_observed()` ahora:
   - detecta rutas duplicadas, ausentes y adicionales;
   - para cada campo de `METADATA_FIELDS`, distingue `field in actual` de `field not in actual` mediante `_MISSING`;
   - emite `METADATA_MISSING:<path>:<field>` cuando la clave falta;
   - emite `METADATA_DIVERGENCE:<path>:<field>:expected=…:observed=…` cuando la clave existe con valor distinto;
   - conserva `None` legítimo cuando coincide con el valor normativo;
   - emite `UNKNOWN_FIELD:<path>:<field>` para campos no reconocidos;
   - emite `RULE_MISSING:<path>` o `RULE_DIVERGENCE:<path>:…` según corresponda;
   - mantiene salida determinista y ordenada.

No se alteraron las reglas normativas, las 139 rutas, los 24 `rule_id` normativos ni los nueve metadatos. No se modificaron artefactos Oracle ni producción.

---

## 3. Pruebas añadidas

Archivo modificado: `tests/test_oracle_verification_representation_v4_r5.py`.

| Prueba | Objetivo |
|---|---|
| `test_auditor_case_absent_manifest_required_when_is_detected` | Reproduce el caso exacto del auditor |
| `test_present_none_matches_expected_none` | `None` presente y esperado coincide |
| `test_present_concrete_value_is_compared_and_reported_by_path_field` | Valor concreto distinto se reporta con ruta y campo |
| `test_absent_required_metadata_never_passes` | Un metadato `manifest_required=True` ausente nunca pasa |
| `test_unknown_and_missing_rule_fields_fail_closed` | Campos desconocidos y `rule_id` ausente fallan cerrado |

No se eliminó ni debilitó ninguna prueba anterior.

---

## 4. Evidencia antes/después del caso del auditor

| Momento | Operación | Resultado |
|---|---|---|
| Antes (auditoría) | Eliminar `manifest_required_when` de una entrada con valor esperado `None` | `ERRORS []`, `COUNT 0` — falso PASS |
| Después (esta corrección) | Misma operación sobre `calibration.base_artifact_sha256.rf` | `METADATA_MISSING:calibration.base_artifact_sha256.rf:manifest_required_when`; `ABSENCE_DETECTED True` |

Comando ejecutado para la evidencia posterior:

```text
python -c "import sys; sys.path.insert(0,'tests'); import oracle_verification_representation_v4_r5 as r; flat=[{**x['metadata'],'rule_id':x['rule_id']} for x in r.expected_entries()]; i=next(k for k,x in enumerate(flat) if x['manifest_required_when'] is None); p=flat[i]['path']; del flat[i]['manifest_required_when']; e=r.compare_observed(flat); print('PATH',p); print('ERRORS',e); print('ABSENCE_DETECTED', any(x.startswith('METADATA_MISSING:'+p+':manifest_required_when') for x in e))"
```

---

## 5. Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **12 passed**, 1 warning `anyio` |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed**, 1 warning `anyio` |
| `git diff --check` | exit 0 |

El warning de `anyio` (`CallSpec2`) no afecta los resultados. No se declaró resuelto el hallazgo únicamente por las pruebas: se reprodujo explícitamente el caso del auditor con resultado correcto.

---

## 6. Hashes SHA-256

| Archivo | Antes | Después |
|---|---|---|
| `tests/oracle_verification_representation_v4_r5.py` | `9c4dcc4088dbd07f84a65e3accf633d708a12088403bf36748354fa3949bab20` | `548da2fc507b38c5fe764050581a7ba4528cbfa1b31d788f98b3a8390d2e1cc6` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `c01aae850729f8343b075cd80fb820a467ca8c2ba21336d5ba8c41ed7af66f48` | `80dc8ea2076c2c4f863992c12dd5f242b59306508ebac2225100e1935801f164` |

Hashes Git después: representación `88b565ae…032`, pruebas `d697516e…164`.

Artefactos Oracle sin cambios: ORACLE-ART-01 `7c9c49a5…`, ORACLE-ART-03 `23306196…`, ORACLE-ART-05 `0cae6714…`; verificador `a67bf35a…`; `provenance_v4.py` `3216d891…`.

---

## 7. Estado Git

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff. Sin commits ni push. No se accedió a Parquet protegidos. Único documento nuevo: este informe.

---

## 8. Confirmaciones finales

- No se alteró la semántica normativa: 139 rutas, nueve metadatos, `rule_id` separado y 24 reglas normativas permanecen.
- No se crearon ORACLE-ART-04, ORACLE-ART-06 ni ORACLE-ART-07.
- No se ejecutó G5 ni G6; no se inició Fase C.
- No se modificaron producción, schemas, dependencias, datasets ni artefactos Oracle existentes.

```text
AUD-IMP-REP-R1-01: RESOLVED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La corrección habilita técnicamente ORACLE-ART-06, sin ejecutar G5 ni crear el artefacto en esta tarea.

**Fin de R13-ORACLE-G5-COMPARE-OBSERVED-ABSENCE-SEMANTICS-FIX-R1.**
