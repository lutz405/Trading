# R13-AUDIT-ORACLE-ART-06-07-R1 — Informe de auditoría técnica independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto:** ORACLE-ART-06 y ORACLE-ART-07 materializados en `docs/oracle_artifacts/v4/r5/`.
**Restricción:** auditoría de solo lectura, salvo este informe. No se corrigieron artefactos ni implementación.

---

## 1. Dictamen

| Artefacto | Dictamen | Estado recomendado |
|---|---|---|
| ORACLE-ART-06 | **ACCEPTED** | `VERIFIED` |
| ORACLE-ART-07 | **ACCEPTED** | `VERIFIED` |
| General | **ACCEPTED** | Ambos cumplen la especificación R2 y la evidencia exigida |

No se detectaron hallazgos. La auditoría no ejecuta G5/G6, no crea artefactos adicionales y no autoriza Fase C.

---

## 2. Hashes verificados

| Archivo | SHA-256 | Git hash |
|---|---|---|
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `83a84f653a1c55579733afe89b8a4a2c2268b711` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `0cae6714d99f3f3acc6ab724577afb240f7610a6f17624effcd4f5f4dd74569f` | `5286798016d1cd5ea446e1597e300bfaf8daab25` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | `fa812bd125b01a7a4e7a9b994b7124e1b0d6fd0a` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | `9f10594fea28152a7f651e8f8d1864b0d63f7f40` |
| `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` | `8f3f066fd4712f2752a8ca06bbbd198b9bb3b527` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `132bad37b05960e828e8271b7b3cfeaebe220df7506d0af8a1fa0d9367649058` | `730f29877f540d1383381aab07eec4197755e336` |
| `src/tradingai/ml/provenance_v4.py` | `3216d8919a82e61ff4c1fba238f130ce2283e2c363e46c315114042c002c8a6b` | `9b4c16ea08591d649bbdc6e4641eca62fa25e8f7` |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |

ART-01/03/05 y la representación conservan los hashes auditados; producción y schema sin cambios.

---

## 3. Métodos de reproducción

Se ejecutaron scripts temporales en `%TEMP%` (eliminados) que:

1. Cargaron la representación auditada `oracle_verification_representation_v4_r5.py`.
2. Reconstruyeron los valores esperados desde `expected_entries()`.
3. Recalcularon 1.251 sondas negativas sobre ORACLE-ART-01.
4. Reprodujeron control, mutación, control incompleto, restauración y determinismo de ART-07.
5. Regeneraron ambos artefactos en archivos temporales y compararon sus bytes con los artefactos almacenados.

No se usó ORACLE-ART-01 como fuente de valores esperados, solo como objeto de comparación.

---

## 4. Auditoría de ORACLE-ART-06

| Criterio | Evidencia | Resultado |
|---|---|---|
| 139 rutas únicas y normativas | `ART06_ROWS 139`, `UNIQUE 139`, `PATH_SET_OK True` | ✅ |
| Nueve metadatos por ruta | `ART06_FIELD_ERRORS 0` | ✅ |
| 1.251 comparaciones completas | 139 × 9; `VALUE_ERRORS 0` | ✅ |
| `rule_id` separado | `RULE_ERRORS 0`; campo no incluido en metadatos | ✅ |
| Esperados desde representación aprobada | Reconstrucción independiente coincide; sin uso de ART-01 como fuente | ✅ |
| Sin circularidad | Esperados vs observados con fuentes separadas | ✅ |
| Ausencia vs `None` | Sondas por clase: `METADATA_MISSING` y `METADATA_DIVERGENCE` correctos | ✅ |
| Divergencias detectadas | `ART06_STORED_NEGATIVE_ERRORS 0`; `REPRODUCED_NEGATIVE_FAILURES 0` | ✅ |
| Sondas negativas reales | 1.251 sondas reproducidas; 0 fallos | ✅ |
| `NO_DIVERGENCE` justificado | `COMPARE_ERRORS 0`, `negfail 0` | ✅ |
| Formato sin campos normativos adicionales | Metadatos exactos; campos de evidencia no normativos | ✅ |
| Determinismo | Regeneración temporal byte-idéntica al artefacto | ✅ |

Evidencia positiva: 1.251 resultados `MATCH`. Evidencia negativa: 1.251 sondas `DETECTED`. Matriz por clase: `path` → `MISSING_PATH`/`EXTRA_PATH`; los otros ocho campos → `METADATA_MISSING`/`METADATA_DIVERGENCE`.

---

## 5. Auditoría de ORACLE-ART-07

| Criterio | Evidencia | Resultado |
|---|---|---|
| Control sin mutación ejecutado | `CONTROL_ERRORS 0`, detección `NOT_DETECTED` | ✅ |
| Mutación aplicada en tres rutas | `DETECTED` en `calibration.base_artifact_sha256.rf`, `.xgb`, `calibration.base_model_id` | ✅ |
| Detección por ruta | Las tres rutas aparecen en `detected_paths` | ✅ |
| Control incompleto | `NOT_DETECTED`; no falso PASS | ✅ |
| `NOT_DETECTED` interpretado correctamente | `negative_controls.result=NO_PASS_ON_ABSENT_OR_AMBIGUOUS_DETECTION` | ✅ |
| Aislamiento | Solo copias `deepcopy`; producción y datasets sin cambios | ✅ |
| Restauración | `ORIGINAL_RESTORED True`; `POST_ERRORS 0` | ✅ |
| Sin cambios residuales | Hashes de artefactos y schema sin cambios; `git status` sin diff | ✅ |
| Reproducibilidad y determinismo | Control y mutación repetidos con resultados idénticos | ✅ |
| Reconstrucción de la evidencia | Artefacto contiene control, mutación, control incompleto, aislamiento y determinismo | ✅ |

El artefacto declara `detection_status: DETECTED` y `status: CREATED_UNVERIFIED`, coherente con un producto generado y probado pero pendiente de esta auditoría.

---

## 6. Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **17 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed** |
| `python -m pytest -q tests/test_provenance.py tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **182 passed** |
| `git diff --check` | exit 0 |

El warning de `anyio` no afecta los resultados.

---

## 7. Hallazgos

Ninguno. No hay hallazgos CRITICAL, HIGH, MEDIUM, LOW ni INFO que impidan la transición a `VERIFIED` de ART-06 y ART-07.

**Limitación:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen. ART-04 continúa pendiente de revisión humana real y ART-05 de verificación completa; ello mantiene G5 bloqueada aunque estos dos artefactos sean conformes.

---

## 8. Estado Git

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin cambios staged ni unstaged. `git diff --check`: exit 0. Sin commits ni push. No se accedió a Parquet protegidos. Único archivo creado por esta auditoría: este informe. ART-04 no existe.

---

## 9. Conclusión y estados recomendados

```text
ORACLE-ART-06: VERIFIED (recomendado por esta auditoría)
ORACLE-ART-07: VERIFIED (recomendado por esta auditoría)
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La auditoría de ART-06 y ART-07 no equivale a completar G5, aprobar G6 ni autorizar Fase C. El cambio efectivo de estado de los artefactos debe registrarse en una tarea documental separada.

**Fin de R13-AUDIT-ORACLE-ART-06-07-R1.**
