# R13-ORACLE-G5-ART-05-COVERAGE-COMPLETION-R1 — Completión de evidencia de cobertura

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Alcance:** exclusivamente `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` y este informe. No se ejecuta G5/G6 ni se inicia Fase C.

---

## 1. Estado Git inicial y final

| Momento | HEAD | Rama / remoto | Estado |
|---|---|---|---|
| Inicial | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Sin staged ni diff; `diff --check` exit 0 |
| Final | `259ca6ee11878f114cdcab4cef500074b3bc1a48` | `main`, alineado | Sin staged ni diff; `diff --check` exit 0 |

Sin commits ni push. No se accedió a Parquet protegidos.

---

## 2. Hashes iniciales y finales

| Archivo | Antes | Después |
|---|---|---|
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | SHA-256 `0cae6714d99f3f3acc6ab724577afb240f7610a6f17624effcd4f5f4dd74569f`; Git `5286798016d1cd5ea446e1597e300bfaf8daab25` | SHA-256 `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c`; Git `ec0803f2d47f4fe2a64191662018f69183bb5a2a` |

Sin cambios: ART-01 `7c9c49a5…` / `076716ef…`; ART-03 `23306196…` / `83a84f65…`; ART-06 `9c133937…` / `fa812bd1…`; ART-07 `9a3d4674…` / `9f10594f…`; representación `23e37afa…` / `8f3f066f…`; pruebas `132bad37…` / `730f2987…`; `provenance_v4.py` `3216d891…`; schema `c98ef476…`.

---

## 3. Requisitos de ART-05 y cumplimiento

| Requisito R2 §4.5 | Antes | Después |
|---|---|---|
| 139 rutas únicas y normativas | Sí | Sí |
| Trazabilidad `rule_id` conservada | Parcial (`rule_id` por ruta) | Sí, con 13 `rule_id` distintos dentro de 24 filas normativas |
| Condición de aplicabilidad | Presente | Presente desde la representación aprobada |
| Comportamiento esperado | Presente, derivado de la misma tabla | Presente desde la representación aprobada |
| Resultado observado | `MATCH_R9_5_4`, no independiente | `MATCH` por comparación representación vs ART-01 |
| Caso positivo/negativo por ruta | **Faltaban** identificadores por ruta | 139 positivos y 556 negativos (4 por ruta) |
| Evidencia reproducible | Referencia simple a ART-01 | Referencias a ART-01 y a la representación, con comandos reproducibles |
| Correspondencia con el oracle | Parcial (`rule_id`) | `rule_id` + nueve metadatos esperados/observados |
| Detección de rutas ausentes, duplicadas, desconocidas o divergentes | No demostrada | Demostrada por ruta |

Durante la generación se detectó y corrigió un defecto en la sonda de ruta desconocida (el campo `path` de los metadatos sobrescribía el valor de la clave); el artefacto final registra 0 fallos. No se modificó la representación auditada.

---

## 4. Cobertura y evidencia

- **Rutas:** 139, únicas, coincidentes con la representación auditada y con R9 §5.4.
- **Reglas:** 13 `rule_id` usados por las 139 rutas; 24 filas normativas en el diseño v4 §9.2.
- **Metadatos:** nueve campos exactos; `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`. `rule_id` separado.
- **Esperados:** derivados de `tests/oracle_verification_representation_v4_r5.py`, aprobado y auditado; **no** de ART-01.
- **Observados:** tomados de ART-01 únicamente como objeto de comparación.
- **Positivos:** 139 casos `POSITIVE:<path>` con resultado `DETECTED`; comparación completa sin errores.
- **Negativos:** 556 casos — `NEGATIVE_ABSENT`, `NEGATIVE_DUPLICATE`, `NEGATIVE_UNKNOWN` y `NEGATIVE_DIVERGENT` por ruta — todos `DETECTED`.
- **Resultado agregado:** `NO_DIVERGENCE`, `negative_probe_failures: []`.
- **Determinismo:** regeneración byte-idéntica; SHA-256 antes y después igual.

La verificación independiente reconstruyó 139 rutas, 139 casos positivos y 556 negativos con **0 errores**.

---

## 5. Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| Verificación de 139 rutas y casos positivos/negativos (script temporal eliminado) | `ROWS 139`, `POSITIVE_CASES 139`, `NEGATIVE_CASES 556`, `ERRORS 0` |
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **17 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed** |
| `python -m pytest -q tests/test_provenance.py tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **182 passed** |
| Regeneración determinista de ART-05 | Hash idéntico |
| `git diff --check` | exit 0 |

El warning de `anyio` no afecta los resultados.

---

## 6. Hallazgos, limitaciones y estado

**Hallazgos:** ninguno que bloquee la finalización. El defecto de la sonda negativa se corrigió dentro de esta tarea y no afecta al artefacto final.

**Limitación principal:** esta ejecución y sus pruebas no constituyen auditoría independiente. Por tanto, ART-05 permanece `CREATED_UNVERIFIED`; el paso a `VERIFIED` exige auditoría independiente favorable y registro separado.

**Limitación adicional:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen.

```text
ORACLE-ART-05: CREATED_UNVERIFIED (recomendado mantener)
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

ART-04 continúa `NOT_CREATED`. No se creó un octavo artefacto. La completión de ART-05 no completa G5 ni autoriza G6 o Fase C.

**Fin de R13-ORACLE-G5-ART-05-COVERAGE-COMPLETION-R1.**
