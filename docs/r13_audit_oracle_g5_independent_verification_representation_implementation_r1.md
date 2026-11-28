# R13-AUDIT-ORACLE-G5-INDEPENDENT-VERIFICATION-REPRESENTATION-IMPLEMENTATION-R1 — Informe de auditoría independiente

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Objeto auditado:** implementación de la representación independiente de verificación en `tests/`.
**Restricción:** auditoría de solo lectura, salvo este informe. No se corrigió la implementación.

---

## 1. Dictamen

**ACCEPTED WITH FINDINGS.** La representación es normativamente correcta, independiente, determinista y cubre las 139 rutas y los 24 `rule_id` normativos. La afirmación «139 rutas, 13 `rule_id` válidos dentro de 24 filas normativas» se confirma y no supone pérdida de trazabilidad. Queda un hallazgo MEDIUM en `compare_observed()` que impide declarar lista para ORACLE-ART-06 hasta corregirlo; ORACLE-ART-07 sí puede prepararse con la implementación actual.

---

## 2. Matriz de criterios y evidencias

| Criterio | Evidencia | Resultado |
|---|---|---|
| Integridad Git | HEAD `259ca6ee…`, `main`, alineado; sin staged/diff; `diff --check` exit 0 | ✅ |
| Fuentes normativas | R9 §5.4, diseño §9.2, schema v4 y D1–D6 | ✅ |
| Independencia de artefactos | Sin `docs/oracle_artifacts` ni nombres de artefactos como fuente en el módulo | ✅ |
| Sin imports productivos | Sin `from tradingai`/`import tradingai` | ✅ |
| Sin dependencias nuevas | Solo stdlib; `pytest` ya declarado | ✅ |
| 139 rutas | Reconstrucción independiente desde R9 §5.4 | ✅ |
| 24 filas normativas | Reconstrucción independiente desde diseño §9.2 | ✅ |
| Nueve metadatos separados de `rule_id` | `METADATA_FIELDS` + comprobación por entrada | ✅ |
| Tipos/nulabilidad | `schema_consistency_errors() == []` | ✅ |
| Determinismo | `expected_entries()` idempotente; pruebas | ✅ |
| Mutación aislada | Copia `deepcopy`, fail-closed, detección en tres rutas | ✅ |
| `compare_observed()` | Comparación de metadatos y reglas; **hallazgo MEDIUM** | ⚠️ |
| Pruebas | 7 nuevas + 66 regresión reproducidas | ✅ |

---

## 3. Análisis detallado de `rule_id`

Recuento reconstruido **directamente desde las fuentes normativas**, sin usar ORACLE-ART-01:

| Magnitud | Valor |
|---|---|
| Filas de diseño v4 §9.2 | 24 |
| `rule_id` normativos posibles (`R9-9.2-01…24`) | 24 |
| Rutas R9 §5.4 expandidas | 139 (139 únicas) |
| Rutas del mapping de diseño | 172 (incluye rutas excluidas y agregadas) |
| `rule_id` distintos usados por las 139 rutas | 13 |
| Rutas sin `rule_id` | 0 |
| `rule_id` normativos no usados | 11 |
| Tokens asignados a más de una regla | 0 |
| Cardinalidad | **muchos a uno** (hasta 41 rutas comparten una regla) |

Los 13 `rule_id` usados son: `01, 03, 05, 07, 09, 10, 11, 12, 13, 14, 15, 19, 20`.

Los 11 no usados corresponden **íntegramente a reglas de exclusión**, no a omitidas inválidas: `02` (identidad de salida/timestamps), `04` (localizadores/meta), `06` (`producer.command`), `08` (`data.snapshot_uri`), `16` (resultados derivados), `17` (`validation.partition_manifest_sha256`), `18` (evaluación), `21` (digests de calibración), `22` (artifacts), `23` (métricas) y `24` (`extensions`). Ninguna de esas rutas pertenece a la allowlist, por lo que no debe aparecer en la representación de verificación de las 139 rutas.

Cada una de las 139 rutas tiene exactamente un `rule_id`; la correspondencia es muchos a uno por agrupación normativa de filas. D1 se conserva: el identificador es secuencial por fila de §9.2 (dos dígitos) y la trazabilidad es completa. **No hay omisión ni pérdida de trazabilidad.**

---

## 4. Cobertura normativa

- Las 139 rutas coinciden con la reconstrucción independiente de R9 §5.4; sin rutas adicionales ni ausentes.
- Los nueve metadatos exactos están presentes por ruta; `rule_id` se mantiene fuera del diccionario de metadatos.
- Los tipos son los normativos (`string`, `string_decimal`, `timestamp`, `integer`, `number`, `boolean`, `array`, `object`), con nulabilidad y condiciones sin simplificaciones; `schema_consistency_errors()` devuelve `[]`.
- El caso `shared_with` se verifica contra `$defs/partition` y `$defs/calibration_partition` (obligatorio/permitido solo en calibration).

---

## 5. Independencia arquitectónica

El módulo reside en `tests/`, lee solo R9, diseño v4 §9.2 y schema v4, y no importa producción ni artefactos. `parse_design_rules()` y `parse_r9_allowlist()` derivan reglas de documentos normativos. No se convirtió en fuente normativa ni en octavo artefacto: es una herramienta de verificación aprobada. No se detectaron reglas duplicadas contradictorias ni circularidad.

Observación INFO: hay un `import re` no utilizado en el módulo; no afecta la corrección ni añade dependencias.

---

## 6. Auditoría de `compare_observed()`

La función compara conjuntos de rutas (duplicados, ausentes, extra), los nueve metadatos y `rule_id`, con salida determinista y errores ordenados. Detecta tipos divergentes, rutas ausentes/extra y divergencia de regla en las pruebas reproducidas.

**Hallazgo AUD-IMP-REP-R1-01 — MEDIUM.** La comparación usa `actual.get(field)` frente al valor esperado. Cuando el valor esperado es `None` (p. ej., `manifest_required_when=None`), un campo **ausente** en la observación produce también `None` y **no se reporta divergencia**. Comprobación reproducida: eliminar `manifest_required_when` de una entrada observada devuelve `[]`. Esto confunde ausencia con `null`, contra el criterio de diferenciación exigido para ORACLE-ART-06.

- Evidencia: `tests/oracle_verification_representation_v4_r5.py` líneas 233–236; prueba directa reproducida con salida `ERRORS [], COUNT 0`.
- Impacto: una observación incompleta podría recibir resultado limpio y convertirse en falso PASS.
- Corrección requerida: usar centinela para distinguir `field not in actual` de `actual[field] is None`, y añadir caso de prueba para campo ausente con valor esperado `None`.
- Bloquea: preparar/aceptar ORACLE-ART-06. No bloquea ORACLE-ART-07.

No se corrigió durante la auditoría, conforme a las restricciones.

---

## 7. Auditoría de mutación

`isolated_external_run_only_mutation()` valida entrada no vacía y presencia de las tres rutas; trabaja con `deepcopy`, deja el original intacto y limpia la copia en `finally`, por lo que la restauración no depende de escritura en disco. Falla cerrado con `ISOLATION_FAILED:*` si no puede garantizar el aislamiento. `mutation_detection_evidence()` marca `DETECTED` solo cuando las tres rutas tienen `projection_include_when=always`. Prueba reproducida: detección en tres rutas y observación posterior sin errores. Sin falso PASS detectado en el alcance normativo.

---

## 8. Pruebas reproducidas

| Comando | Resultado |
|---|---|
| `python -m pytest -q tests/test_oracle_verification_representation_v4_r5.py` | 7 passed, 1 warning anyio |
| Reconstrucción normativa independiente (script temporal, eliminado) | 24 filas, 139 rutas, 13 usados, 11 exclusión, 0 sin mapear |
| Prueba directa de campo ausente vs `None` | Confirmó el hallazgo MEDIUM |

El warning de `anyio` (`CallSpec2`) no afecta los resultados. No se ejecutaron G5 ni G6.

---

## 9. Hallazgos y severidades

| ID | Severidad | Evidencia | Impacto | Corrección | Bloquea |
|---|---|---|---|---|---|
| AUD-IMP-REP-R1-01 | **MEDIUM** | `compare_observed()` usa `.get()` | Ausencia confundida con `null`; falso PASS en ART-06 | Centinela de ausencia + prueba | ORACLE-ART-06; aceptación plena |
| AUD-IMP-REP-R1-02 | **INFO** | `import re` sin uso | Ninguno | Retirar en revisión futura | No |

---

## 10. Hashes

| Archivo | SHA-256 | Git hash |
|---|---|---|
| `tests/oracle_verification_representation_v4_r5.py` | `9c4dcc4088dbd07f84a65e3accf633d708a12088403bf36748354fa3949bab20` | `05a7b1977fe9d75939d38e6d9e79b7aa349f46ac` |
| `tests/test_oracle_verification_representation_v4_r5.py` | `c01aae850729f8343b075cd80fb820a467ca8c2ba21336d5ba8c41ed7af66f48` | `8eca609dd055be16dab99244d5608e874e54f48b` |
| Informe de implementación | `580bc8fb4fbc0e882e72d11102074a6f7171266275b974c468f3a86958888c5e` | `42c0b7a0e00ffdceef3c512a9124043c9e4b0257` |
| R9 | `884ee501bc80b68e57274894cba12ddba82eb96b9899214608ad11bbfbda5ead` | `d21de0f112329ad9a9c30f167189a1f81ecef685` |
| Diseño v4 | `78addb7400ce3d1861511ea12afc5d5c310442296b38a2f444010c013c5ad7a3` | `fbe7215c5199c418e16f6968fb4b662427f8d70a` |
| Schema v4 | `c98ef476f8d1a8199d57f4ed3d2532a2ce06589dcaa01efc2f13c490b1707840` | `b97527ccbe395c6e90cfe630d916f4b92786ba6c` |

Artefactos Oracle 01/03/05 y verificador sin cambios.

---

## 11. Estado Git, limitaciones y conclusión

HEAD `259ca6ee11878f114cdcab4cef500074b3bc1a48`, rama `main`, alineado. Sin staged ni diff; `git diff --check` exit 0. Sin commits ni push; sin acceso a Parquet protegidos. Único archivo creado por la auditoría: este informe.

**Limitación:** los informes de auditoría independiente no están como archivos del repositorio; los registros de aprobación no los sustituyen.

**Conclusión sobre ART-06/ART-07:** puede prepararse ORACLE-ART-07 con la implementación actual. **No debe prepararse ORACLE-ART-06** hasta corregir AUD-IMP-REP-R1-01. No se ejecutó G5/G6 ni se autorizó Fase C.

```text
G5_STATUS: BLOCKED
G6_STATUS: NOT_STARTED
AUD_R8_02: OPEN
PHASE_C_IMPLEMENTATION_AUTHORIZATION: NOT_GRANTED
PHASE_C_STATUS: BLOCKED
```

**Fin de R13-AUDIT-ORACLE-G5-INDEPENDENT-VERIFICATION-REPRESENTATION-IMPLEMENTATION-R1.**
