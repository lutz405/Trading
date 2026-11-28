# R13-ORACLE-G5-ART-06-07-MATERIALIZATION-R1 — Materialización de ORACLE-ART-06 y ORACLE-ART-07

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Alcance:** exclusivamente ORACLE-ART-06 y ORACLE-ART-07. No se ejecuta G5 ni G6; no se crea ORACLE-ART-04.

---

## 1. Estado inicial y preflight

| Elemento | Valor verificado |
|---|---|
| HEAD / rama / remoto | `259ca6ee11878f114cdcab4cef500074b3bc1a48`, `main`, `origin/main` alineado |
| Estado inicial | Sin staged ni diff; `git diff --check` exit 0 |
| Autorización | `MATERIALIZATION_AUTHORIZATION_STATUS: GRANTED` (autorización R2) |
| Auditoría de representación | `R13-AUDIT-NATIVE-RULE-ID-ABSENCE-FIX-R1 — ACCEPTED`; ambos hallazgos `RESOLVED` |
| Aprobación de representación | `VERIFICATION_REPRESENTATION_OWNER_APPROVAL: APPROVED` |
| ART-01 / 03 / 05 | Hashes idénticos a los registros; contenido sin cambios |
| Representación y pruebas | Hashes `23e37afa…` y `132bad37…`, coincidentes con la versión auditada |
| Artefactos 04/06/07 antes | No existían |

No se detectó discrepancia de preflight.

---

## 2. Archivos creados y hashes

| Artefacto | SHA-256 | Git hash | Estado |
|---|---|---|---|
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | `fa812bd125b01a7a4e7a9b994b7124e1b0d6fd0a` | `CREATED_UNVERIFIED` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | `9f10594fea28152a7f651e8f8d1864b0d63f7f40` | `CREATED_UNVERIFIED` |
| `docs/r13_oracle_g5_art_06_07_materialization_r1.md` | Se reporta en el cierre | Se reporta en el cierre | Informe |

No se creó un octavo artefacto ni ORACLE-ART-04.

---

## 3. Método de generación de ORACLE-ART-06

- **Esperado:** derivado exclusivamente de `tests/oracle_verification_representation_v4_r5.py` (`expected_entries()`), aprobado y auditado. No se derivó de ORACLE-ART-01.
- **Observado:** ORACLE-ART-01 se usó únicamente como objeto de comparación, nunca como fuente normativa.
- **Comparación:** `compare_observed()` sobre las entradas planas de ORACLE-ART-01; salida `[]`.
- **Cobertura:** 139 rutas y 1.251 comparaciones (139 × 9 metadatos).
- **Metadatos:** `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`.
- **`rule_id`:** campo de trazabilidad separado, no décimo metadato.
- **Resultado agregado:** `NO_DIVERGENCE`. No se declaró `PASS`.
- **Evidencia negativa:** para cada ruta y metadato se ejecutó una sonda controlada. Si la sonda no se detectaba, se registraba fallo. Tras corregir el planteamiento de la sonda para `path` (se elimina la ruta y se exige `MISSING_PATH`, porque cambiar `path` destruye la identidad de la ruta), `negative_probe_failures = 0`.
- **Salida determinista:** JSON con claves ordenadas, UTF-8 y salto final; regenerado dos veces con hash idéntico.

ART-06 contiene por ruta: `path`, `rule_id`, los nueve metadatos con `expected`, `observed`, `result` (`MATCH`) y `negative_probe` (`DETECTED`). No hay `MISSING`, `DIVERGENCE` ni ruta sin comprobar.

---

## 4. Método y resultados de ORACLE-ART-07

Mecanismo: `isolated_external_run_only_mutation()` y `mutation_detection_evidence()`, sin modificar producción ni la representación normativa.

| Caso | Resultado |
|---|---|
| Control sin mutación | `NOT_DETECTED` — esperado; comparación base sin errores |
| Mutación aplicada en las tres rutas `calibration.base_*` | `DETECTED`; rutas: `calibration.base_artifact_sha256.rf`, `.xgb`, `calibration.base_model_id` |
| Control con mutación incompleta (dos de tres rutas) | `NOT_DETECTED` — no se clasifica como PASS |
| Repetición de control y mutación | Resultados idénticos |
| Restauración | `original_restored: True`; `post_context_errors: []` |
| Aislamiento | Solo copias `deepcopy`; producción y datasets sin cambios; sin escritura en Parquet |
| Estado agregado | `DETECTED` |

No se dejaron cambios residuales: la representación original conserva sus 139 rutas y la comparación posterior devuelve `[]`.

---

## 5. Verificación ejecutada

| Comando / comprobación | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **17 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed**, 1 warning anyio |
| Script de materialización (generación y comprobaciones de ART-06/07) | 139 rutas, 1.251 comparaciones, 0 errores, 0 fallos de sonda negativa, detección de mutación correcta |
| Regeneración determinista | Hashes de ART-06 y ART-07 idénticos antes/después |
| Comprobación estructural de artefactos | `status=CREATED_UNVERIFIED`, 139 filas, 9 metadatos, `rule_id` separado |
| `git diff --check` | exit 0 |

El warning de `anyio` (`CallSpec2`) no afecta los resultados. No se ejecutaron G5 ni G6.

---

## 6. Hallazgos y limitaciones

**Hallazgos:** ninguno que bloquee la materialización. Durante la generación se corrigió el diseño de la sonda negativa para `path` dentro del propio procedimiento, sin modificar la representación aprobada; el artefacto final registra 0 fallos.

**Limitación principal:** ART-06 y ART-07 se generaron y probaron con sus propias comprobaciones; esto **no sustituye** la auditoría independiente exigida para elevarlos a `VERIFIED`. Por ello ambos permanecen `CREATED_UNVERIFIED`.

**Limitación adicional:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen. ART-04 sigue pendiente de revisión humana real; ART-05 sigue requiriendo la verificación completa definida en la especificación.

---

## 7. Estado Git final

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni diff. Sin commits ni push. No se modificaron `provenance_v4.py`, schemas, dependencias ni datasets; no se accedió a Parquet protegidos. Únicos artefactos nuevos: ORACLE-ART-06 y ORACLE-ART-07; único documento nuevo: este informe.

---

## 8. Estados finales

```text
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
ORACLE-ART-01: VERIFIED
ORACLE-ART-02: VERIFIED
ORACLE-ART-03: VERIFIED
ORACLE-ART-04: NOT_CREATED
ORACLE-ART-05: CREATED_UNVERIFIED
ORACLE-ART-06: CREATED_UNVERIFIED
ORACLE-ART-07: CREATED_UNVERIFIED
```

La materialización no equivale a completar G5 ni autoriza G6 o Fase C. Se detiene la ejecución.

**Fin de R13-ORACLE-G5-ART-06-07-MATERIALIZATION-R1.**
