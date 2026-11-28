# R13-ORACLE-G5-NATIVE-RULE-ID-ABSENCE-FIX-R1 — Corrección de ausencia de `rule_id` en formato nativo

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Hallazgo corregido:** `AUD-ABS-FIX-R1-01` (LOW), registrado en `docs/r13_audit_compare_observed_absence_semantics_fix_r1.md`.
**Alcance:** exclusivamente dos archivos en `tests/` y este informe.

---

## 1. Hallazgo original y causa raíz

`_flatten()` convertía una entrada nativa `{"path":…, "metadata":{…}}` sin clave `rule_id` outer en una observación plana con `rule_id=None`, mediante `flat["rule_id"] = entry.get("rule_id")`. `compare_observed()` veía entonces un valor `None` presente y emitía `RULE_DIVERGENCE:…:None` en lugar de `RULE_MISSING:…`. No producía falso PASS, pero confundía ausencia con valor nulo para `rule_id`.

---

## 2. Corrección implementada

Archivo: `tests/oracle_verification_representation_v4_r5.py`.

```python
if "metadata" in entry:
    flat = dict(entry["metadata"])
    if "rule_id" in entry:
        flat["rule_id"] = entry["rule_id"]
    return flat
return dict(entry)
```

- No se sintetiza `rule_id=None`.
- Si `rule_id` está ausente, no se inserta la clave y `compare_observed()` produce `RULE_MISSING` mediante el centinela `_MISSING`.
- Si está presente con `None`, se conserva y produce `RULE_DIVERGENCE` frente al `rule_id` normativo esperado.
- Si está presente y es correcto, no genera error.
- Si diverge, genera `RULE_DIVERGENCE` con valor observado real.

No se alteraron las 139 rutas, los nueve metadatos, las 24 filas normativas ni las reglas D1–D6.

---

## 3. Pruebas añadidas

Archivo: `tests/test_oracle_verification_representation_v4_r5.py`.

| Prueba | Caso |
|---|---|
| `test_auditor_case_native_rule_id_absence_is_rule_missing` | Reproduce el caso del auditor: formato nativo sin `rule_id` → `RULE_MISSING` |
| `test_native_rule_id_present_none_is_divergence_not_absence` | `rule_id=None` presente → `RULE_DIVERGENCE`, no `RULE_MISSING` |
| `test_native_rule_id_present_correct_has_no_errors` | `rule_id` correcto → sin errores y determinista |
| `test_native_rule_id_divergent_is_reported` | `rule_id` distinto → `RULE_DIVERGENCE` |
| `test_flat_rule_id_absence_and_divergence_remain_distinct` | Ausencia y divergencia en forma plana siguen diferenciadas |

No se eliminó ni debilitó ninguna prueba existente.

---

## 4. Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **17 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed**, 1 warning anyio |
| `git diff --check` | exit 0 |

El warning de `anyio` (`CallSpec2`) no afecta los resultados.

---

## 5. Reproducción del caso nativo

| Momento | Operación | Salida |
|---|---|---|
| Antes (auditoría) | Eliminar `rule_id` de una entrada nativa | `RULE_DIVERGENCE:calibration.base_artifact_sha256.rf:R9-9.2-20:None` |
| Después (esta corrección) | Misma operación | `RULE_MISSING:calibration.base_artifact_sha256.rf` |

Comando de verificación ejecutado:

```text
python -c "import sys; sys.path.insert(0,'tests'); import oracle_verification_representation_v4_r5 as r; n=[dict(x) for x in r.expected_entries()]; p=n[0]['metadata']['path']; del n[0]['rule_id']; e=r.compare_observed(n); print('PATH',p); print('ERRORS',[x for x in e if p in x]); print('RULE_MISSING_DETECTED', any(x.startswith('RULE_MISSING:'+p) for x in e))"
```

Salida: `PATH calibration.base_artifact_sha256.rf`; `ERRORS ['RULE_MISSING:calibration.base_artifact_sha256.rf']`; `RULE_MISSING_DETECTED True`.

---

## 6. Hashes SHA-256

| Archivo | Antes | Después |
|---|---|---|
| `tests/oracle_verification_representation_v4_r5.py` | `548da2fc507b38c5fe764050581a7ba4528cbfa1b31d788f98b3a8390d2e1cc6` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `80dc8ea2076c2c4f863992c12dd5f242b59306508ebac2225100e1935801f164` | `132bad37b05960e828e8271b7b3cfeaebe220df7506d0af8a1fa0d9367649058` |

Hashes Git después: representación `8f3f066f…527`, pruebas `730f2987…336`.

Artefactos sin cambios: ORACLE-ART-01 `7c9c49a5…`, ORACLE-ART-03 `23306196…`, ORACLE-ART-05 `0cae6714…`; verificador `a67bf35a…`; `provenance_v4.py` `3216d891…`; schema `c98ef476…`.

---

## 7. Estado Git y restricciones

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff. Sin commits ni push. No se accedió a Parquet protegidos.

No se modificaron producción, schemas, dependencias ni artefactos Oracle. No se crearon ORACLE-ART-04, ORACLE-ART-06 ni ORACLE-ART-07. No se ejecutó G5 ni G6; no se inició Fase C.

---

## 8. Cierre

```text
AUD-IMP-REP-R1-01: RESOLVED
AUD-ABS-FIX-R1-01: RESOLVED
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La semántica de ausencia, `None` y valores concretos queda cerrada tanto en formato plano como nativo. La corrección habilita técnicamente ORACLE-ART-06 sin ejecutar G5 ni crear el artefacto.

**Fin de R13-ORACLE-G5-NATIVE-RULE-ID-ABSENCE-FIX-R1.**
