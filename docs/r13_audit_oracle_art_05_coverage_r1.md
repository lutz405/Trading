# R13-AUDIT-ORACLE-ART-05-COVERAGE-R1 — Informe de auditoría técnica independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto:** `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json`.
**Restricción:** auditoría de solo lectura, salvo este informe. No se corrigió ni modificó artefacto alguno.

---

## 1. Dictamen

**ACCEPTED.** ORACLE-ART-05 cumple íntegramente la especificación R2 §4.5. Se recomienda su transición a `VERIFIED` mediante registro documental separado. No se detectaron hallazgos.

---

## 2. Hashes verificados

| Archivo | SHA-256 | Git hash |
|---|---|---|
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-05.json` | `35b705b923543e7328dfa137f4e61a30e191850e4588c988defb675ee018d07c` | `ec0803f2d47f4fe2a64191662018f69183bb5a2a` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-01.json` | `7c9c49a5cc34dd616f37dcdee11d349549ee9e6a039ebfdd1141785f360b300b` | `076716efd872cb89d67f3a9d3a23288e2b73b6ea` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-03.txt` | `23306196fb588376bfd59024737991edc91caa2af195d10089415ac67f4702a5` | `83a84f653a1c55579733afe89b8a4a2c2268b711` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-06.json` | `9c1339377062c81aadb982f6765e8a0366f74be8d0036956e9e49c56e1fb59e0` | `fa812bd125b01a7a4e7a9b994b7124e1b0d6fd0a` |
| `docs/oracle_artifacts/v4/r5/ORACLE-ART-07.json` | `9a3d467431846f6b406a93ce4c92cb1b20086d0a38d667b03b675c577a48ea24` | `9f10594fea28152a7f651e8f8d1864b0d63f7f40` |
| `tests/oracle_verification_representation_v4_r5.py` | `23e37afa1fb9cc448a6378352a032b0066242727839550720ce6e0b71cf48736` | `8f3f066fd4712f2752a8ca06bbbd198b9bb3b527` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `132bad37b05960e828e8271b7b3cfeaebe220df7506d0af8a1fa0d9367649058` | `730f29877f540d1383381aab07eec4197755e336` |
| `src/tradingai/ml/provenance_v4.py` | `3216d8919a82e61ff4c1fba238f130ce2283e2c363e46c315114042c002c8a6b` | `9b4c16ea08591d649bbdc6e4641eca62fa25e8f7` |
| `src/tradingai/schemas/manifest_v4.json` | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |

Todos los artefactos y fuentes conservan los hashes esperados; ART-04 no existe.

---

## 3. Cobertura y correspondencia normativa

| Requisito | Evidencia | Resultado |
|---|---|---|
| JSON válido y estructura conforme a R2 | Parseo directo; campos de evidencia no normativos | ✅ |
| 139 rutas únicas | `ROWS 139`, `UNIQUE 139`, conjunto igual al de la representación | ✅ |
| Correspondencia con R9 §5.4 y diseño §9.2 | Reconstrucción independiente desde `expected_entries()` | ✅ |
| 13 `rule_id` usados | `rule_ids_distinct 13`; trazabilidad por ruta correcta | ✅ |
| 24 `rule_id` normativos | 13 usados por la allowlist; 11 restantes son reglas de exclusión (`model_id`, meta, `producer.command`, `snapshot_uri`, resultados derivados, digests, `artifacts`, `metrics`, `extensions`) | ✅ |
| Nueve metadatos exactos por ruta | `METADATA_FIELDS` coincide; 0 errores | ✅ |
| `rule_id` separado | No incluido en `expected_metadata`/`observed_metadata` | ✅ |
| Sin rutas duplicadas, omitidas o desconocidas | Conjuntos comparados; 0 errores | ✅ |
| Sin campos normativos adicionales | Solo campos de evidencia admitidos | ✅ |
| Ausencia vs `None` | `ABSENCE_VS_NONE True` | ✅ |
| Divergencia por tipo de valor | 8 metadatos detectados como `METADATA_DIVERGENCE`; `path` se detecta como `MISSING_PATH`/`EXTRA_PATH` por ser identidad, comportamiento correcto | ✅ |

---

## 4. Independencia

- Los valores esperados se reconstruyeron desde `tests/oracle_verification_representation_v4_r5.py`, versión auditada y aprobada.
- ART-01 se utilizó únicamente como objeto observado; no como fuente de los esperados.
- `expected_source` y `observed_source` quedan declarados y son verificables.
- La representación no importa producción, no introduce dependencias y no depende de ART-01.
- No hay circularidad entre fuente normativa, representación y artefacto.

---

## 5. Reproducción de los 695 casos

| Categoría | Resultado |
|---|---|
| Casos positivos reproducidos | **139/139** |
| Negativos de ausencia | **139/139** con `MISSING_PATH:<ruta>` |
| Negativos de duplicación | **139/139** con `DUPLICATE_PATH`, inserción al inicio y al final |
| Negativos de ruta desconocida | **139/139** con `EXTRA_PATH:__AUDIT_UNKNOWN__` |
| Negativos de divergencia | **139/139** con `METADATA_DIVERGENCE:<ruta>:type` |
| Total | **695/695**, 0 errores |
| Campo desconocido adicional | `UNKNOWN_FIELD` detectado |
| Ausencia frente a `None` | Detectada correctamente |
| Divergencia en los nueve campos | 8 `METADATA_DIVERGENCE`; `path` vía `MISSING_PATH`/`EXTRA_PATH` |

Ningún negativo fue aceptado como válido. No se detectaron falsos positivos ni falsos negativos.

---

## 6. Pruebas y determinismo

| Comando / comprobación | Resultado |
|---|---|
| Script de auditoría de 695 casos (temporal, eliminado) | `ERRORS 0`, `POSITIVE_OK 139`, `NEGATIVE_OK 556` |
| Regeneración independiente byte a byte | `DETERMINISTIC True`; hash `35b705b9…` |
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | **17 passed**, 1 warning anyio |
| `python -m pytest -q tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **66 passed** |
| `python -m pytest -q tests/test_provenance.py tests/test_provenance_v4_schema.py tests/test_provenance_v4_dispatch.py` | **182 passed** |
| `git diff --check` | exit 0 |

El warning de `anyio` no afecta los resultados. La regeneración no modificó ART-01 ni ningún otro artefacto.

---

## 7. Hallazgos y limitaciones

**Hallazgos:** ninguno.

**Limitación:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen. ART-04 continúa pendiente de revisión humana real; ART-05 no completa G5 por sí solo.

---

## 8. Estado Git

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, `origin/main` alineado. Sin staged ni diff; `git diff --check` exit 0. Sin commits ni push. No se accedió a Parquet protegidos. Único archivo creado: este informe.

---

## 9. Conclusión y estado recomendado

```text
ORACLE-ART-05: VERIFIED (recomendado; registro separado pendiente)
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

La auditoría de ART-05 no completa G5 ni autoriza G6 o Fase C. El cambio efectivo de estado debe formalizarse en un registro documental separado.

**Fin de R13-AUDIT-ORACLE-ART-05-COVERAGE-R1.**
