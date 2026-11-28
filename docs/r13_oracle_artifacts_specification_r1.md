# R13-ORACLE-ARTIFACTS-SPECIFICATION-R1 — Especificación documental de los artefactos del oracle

**Proyecto:** `TradingAI_BTC`.
**Fecha:** 2026-11-27.
**Naturaleza:** especificación documental autónoma. No materializa artefactos, no implementa Fase C, no genera fingerprints y no autoriza implementación.
**Estado de AUD-R8-02:** `OPEN`.
**Estado de Fase C:** `BLOCKED_PENDING_TECHNICAL_AUTHORIZATION_AND_ORACLE_ARTIFACTS`.

---

## 1. Identificación y alcance

Esta especificación define los requisitos que deberán cumplir los siete artefactos materiales del oracle `ORACLE_NORMATIVE_V4_R5` exigidos por `docs/r13_phase_c_design_r9.md` §5.8.5. Su finalidad es permitir una futura materialización y auditoría independiente.

**No se afirma que ninguno de los siete artefactos exista.** Todos se registran aquí en estado `NOT_CREATED`. No se proporciona checksum, transcripción, registro de revisión ni evidencia de prueba, porque ninguno ha sido producido.

La aprobación del propietario registrada en `docs/r13_owner_design_approval_r1.md` cubre **solo el diseño R9**; no autoriza generar estos artefactos ni implementar Fase C.

---

## 2. Fuentes y jerarquía normativa

La jerarquía es la definida en R9 §5.8 y no se modifica:

| Nivel | Fuente | Uso en esta especificación |
|---|---|---|
| 1 | DEC-06 y diseño v4 §9.2 | Autoridad normativa para rutas, exclusiones y condiciones (`external_run_only`, `shared_with`, timestamps normalizados) |
| 2 | `src/tradingai/schemas/manifest_v4.json` | Contrato estructural canónico: `required`, nulabilidad, tipos, `$defs/partition` y `$defs/calibration_partition` |
| 3 | `ALLOWLIST_V4` en `provenance_v4.py` | Representación ejecutable aprobada; único listado que usará el código productivo |
| 4 | `ORACLE_NORMATIVE_V4_R5` | Transcripción independiente de §9.2, usada solo en CI/auditoría |
| 5 | Implementación aceptada de Fase A/B (`validate_manifest_v4` y rutinas auxiliares) | Contrato de validaciones productivas ya aprobadas; no se altera |

Referencias documentales adicionales: `docs/aud04b_model_provenance_v4_approval_r1.md` (DEC-01…DEC-09), `docs/aud04b_model_provenance_v4_implementation_plan_r1.md` (Fase C, V4-U10/V4-U11), `docs/aud04b_model_provenance_v4_design.md` (§§5.2, 9.1–9.5), `docs/r13_decision_resolution_r1.md` y `R13-AUDIT-PHASE-C-DESIGN-R9 — ACCEPTED`.

---

## 3. Convenciones, estados y responsabilidades

### 3.1 Estados de artefacto

| Estado | Significado |
|---|---|
| `NOT_CREATED` | El artefacto no existe materialmente |
| `CREATED_UNVERIFIED` | Existe, pero no ha superado verificación independiente |
| `VERIFIED` | Existe y ha superado verificación independiente documentada |
| `REJECTED` | Existe, pero la verificación concluyó desfavorablemente |

En esta especificación los siete artefactos tienen estado `NOT_CREATED`. Ninguno se marca `VERIFIED`.

### 3.2 Responsabilidades

| Rol | Responsabilidad |
|---|---|
| Productor del artefacto | Generar el artefacto en una futura tarea autorizada, conforme a esta especificación |
| Revisor independiente | Verificar semánticamente contra §9.2 y la autoridad aprobada; no debe ser el único generador del artefacto |
| Auditor independiente | Auditar la evidencia y el proceso, sin generar ni aprobar por sí mismo |
| Propietario | Emitir la aprobación del diseño (ya registrada) y la autorización técnica separada (pendiente) |

No se inventan nombres de personas, herramientas ni fechas de ejecución. La identidad funcional del revisor y la fecha real se registrarán cuando la revisión ocurra.

---

## 4. Los siete artefactos

### 4.1 ORACLE-ART-01 — Transcripción normativa completa e independiente

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-01` |
| Propósito | Fijar, de forma revisable, la autoridad normativa §9.2/DEC-06 como datos comparables frente a `ALLOWLIST_V4` |
| Fuente normativa | R9 §5.8.1 y §5.8.5 artefacto 1; diseño v4 §9.2; DEC-06 |
| Estado actual | `NOT_CREATED` |

**Contenido mínimo obligatorio**

- Las **139 rutas expandidas** (`{partition}` → `train`, `validation`, `calibration`, `test`).
- Los diez campos por entrada definidos en R9 §5.8.1: `path`, `type`, `manifest_required`, `manifest_required_when`, `manifest_allowed_when`, `projection_include_when`, `projection_optional`, `nullable`, `normalization`, `rule_id`.
- Cada `rule_id` referencia la fila correspondiente de §9.2; el esquema de identificación de `rule_id` se registrará durante la generación y se someterá a revisión semántica. No se prescribe aquí un valor concreto.
- Los patrones P1–P5 y la matriz O/A de nueve combinaciones de R9 §5.8.3.
- Las invariantes I1–I12 y los códigos `ALLOWLIST_*` de R9 §5.7.
- Las reglas de normalización temporal de R9 §7 y la semántica de tipos de R9 §5.2.
- Las reglas de exclusión de proyección de R9 §5.5 y la separación admisión/proyección de R9 §5.1 y §5.6.
- Las condiciones fail-closed y los códigos `ORACLE_INCOMPLETE`, `ORACLE_VERSION_MISMATCH`, `ORACLE_CHECKSUM_MISMATCH`, `ALLOWLIST_ORACLE_METADATA_DIVERGENCE`, `ALLOWLIST_MISSING_PATH`, `ALLOWLIST_EXTRA_PATH` de R9 §5.8.2.
- Separación explícita entre **texto normativo** (citas de §9.2/DEC-06), **datos derivados** (entradas expandidas y metadatos) y **material auxiliar** (notas de generación, sin valor normativo).

**Formato y estructura:** objeto con `version` y `entries`, entradas ordenadas por `path`, diez campos en orden fijo. Las condiciones se transcriben como literales del vocabulario de R9 §5.3, no como texto libre.

**Método de generación futuro:** transcripción directa desde §9.2/DEC-06, sin copiar `ALLOWLIST_V4` ni derivar del schema; expansión controlada de `{partition}`; registro de las decisiones de transcripción.

**Método de verificación independiente:** revisión semántica fila por fila contra §9.2, comprobación de que las 139 rutas coinciden con la allowlist normativa y de que la transcripción no procede del código productivo.

**Criterios de aceptación:** completitud de diez campos por entrada; 139 rutas; coherencia con P1–P5, I1–I12 y §§5.2/5.5/5.7; separación texto/datos/auxiliar; revisión documentada.

**Condiciones de rechazo:** campo ausente; ruta duplicada u omitida; `rule_id` sin referencia normativa; condición fuera del vocabulario; texto normativo mezclado con datos derivados; transcripción copiada del código productivo.

**Dependencias:** ninguna para su generación; es prerequisite de ORACLE-ART-02, -03, -04, -05, -06 y -07.

**Evidencia de reproducibilidad:** conservar la versión exacta de §9.2/DEC-06 consultada, las notas de expansión y la correspondencia `rule_id` → fila normativa.

**Responsable de revisión y aprobación:** revisor independiente; aprobación final del propietario como prerrequisito de autorización técnica.

**Relación CP-C:** CP-C-05 y CP-C-13.

---

### 4.2 ORACLE-ART-02 — Versión ejecutable del oracle

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-02` |
| Propósito | Proporcionar una implementación independiente de la transcripción para las verificaciones de CI/auditoría |
| Fuente normativa | R9 §5.8.1 y §5.8.5 artefacto 2; R9 §5.8.5 «Separación oracle/producción» |
| Estado actual | `NOT_CREATED` |

**Fuente de verdad:** ORACLE-ART-01 y la autoridad normativa §9.2/DEC-06. No `ALLOWLIST_V4`, no el schema como sustituto de la norma, no resultados de Fase C.

**Independencia:** no importa módulos productivos para obtener la transcripción; el módulo productivo no importa este artefacto; las verificaciones se ejecutan fuera del camino productivo.

**Comportamiento exigible:** determinista, reproducible, sin fallback silencioso, manejo explícito de errores con códigos deterministas (`ORACLE_INCOMPLETE`, `ORACLE_VERSION_MISMATCH`, `ORACLE_CHECKSUM_MISMATCH`), cobertura verificable de los casos normativos.

**Formato y estructura:** a decidir en la futura tarea autorizada, sin ampliar el alcance aprobado. Esta especificación no impone lenguaje, biblioteca ni arquitectura.

**Método de generación futuro:** implementación independiente a partir de ORACLE-ART-01; registro de la decisión de arquitectura; revisión de independencia antes de usarla como verificador.

**Método de verificación independiente:** ejecutar la versión sobre datos de prueba aislados, comparar resultados con la transcripción revisada y comprobar ausencia de importaciones productivas.

**Criterios de aceptación:** mismos resultados ante entradas idénticas; errores deterministas; sin dependencias de `tests/` en producción; sin fallback; auditoría de independencia documentada.

**Condiciones de rechazo:** resultados no deterministas; importación del código productivo como fuente; dependencia de módulos de tests en producción; silencio ante datos incompletos.

**Dependencias:** ORACLE-ART-01.

**Evidencia de reproducibilidad:** conservar la versión ejecutable, sus entradas de prueba aisladas y el registro de arquitectura aprobado.

**Responsable de revisión y aprobación:** revisor independiente y auditor; aprobación del propietario para cualquier decisión de arquitectura que amplíe alcance.

**Relación CP-C:** CP-C-05, CP-C-13.

---

### 4.3 ORACLE-ART-03 — SHA-256 de la versión ejecutable / transcripción canonicalizada

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-03` |
| Propósito | Fijar la integridad de la transcripción canonicalizada y detectar cambios no revisados |
| Fuente normativa | R9 §5.8.1 «Versión y checksum»; §5.8.5 artefacto 3; §6.4 |
| Estado actual | `NOT_CREATED` |

**Bytes exactos sometidos a hash:** la serialización JCS de:

```text
{"version": <versión>, "entries": [<entradas ordenadas por path>]}
```

donde cada entrada usa los diez campos de R9 §5.8.1 en orden fijo.

**Codificación:** UTF-8 sin BOM. JCS no emite salto de línea final; los finales de línea de los archivos de origen no intervienen porque se serializa el objeto parseado, no el texto original.

**Archivos auxiliares:** no se incluyen en la preimagen. El propio checksum no se incluye en su preimagen.

**Procedimiento de cálculo:** sobre la transcripción canonicalizada de ORACLE-ART-01, mediante RFC 8785, y posterior `SHA-256` de esos bytes.

**Formato del resultado:** hex minúsculo de 64 caracteres.

**Verificación reproducible:** recalcular desde ORACLE-ART-01 y comparar con el valor registrado; discrepancia → `ORACLE_CHECKSUM_MISMATCH`.

**Criterios de aceptación:** preimagen documentada campo por campo; resultado reproducible por un verificador distinto del generador; checksum no usado como sustituto de la revisión semántica.

**Condiciones de rechazo:** checksum calculado sobre archivos auxiliares, sobre el propio checksum o sobre bytes sin canonicalizar; valor no reproducible; uso del checksum para declarar corrección semántica.

**Dependencias:** ORACLE-ART-01, ORACLE-ART-02.

**Evidencia de reproducibilidad:** conservar la transcripción exacta, la versión y el procedimiento de canonicalización.

**Responsable de revisión y aprobación:** revisor independiente; el checksum no sustituye su dictamen.

**Relación CP-C:** CP-C-05, CP-C-13.

---

### 4.4 ORACLE-ART-04 — Registro de revisión humana independiente

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-04` |
| Propósito | Evidenciar que la transcripción fue revisada semánticamente contra §9.2 por un revisor distinto del generador |
| Fuente normativa | R9 §5.8.1 «Revisión humana»; §5.8.5 artefacto 4 |
| Estado actual | `NOT_CREATED` |

**Contenido mínimo:** identidad funcional del revisor (rol, no nombre inventado); declaración de independencia respecto de la implementación; versión revisada; checksum revisado; alcance de la revisión; casos examinados; hallazgos; resolución de hallazgos; dictamen; fecha real de la revisión; evidencia de aprobación.

**Formato:** registro documental estructurado, con secciones para alcance, hallazgos, resolución y dictamen.

**Método de generación futuro:** revisión efectiva realizada por persona funcionalmente independiente, posterior a ORACLE-ART-01/03.

**Método de verificación independiente:** auditoría del registro, comprobando que los casos examinados cubren las 139 rutas, los nueve metadatos y la mutación; que los hallazgos tienen resolución; y que la fecha y el dictamen son reales.

**Criterios de aceptación:** revisión realizada y documentada; independencia declarada; versión y checksum coincidentes con los artefactos revisados; hallazgos resueltos; dictamen favorable.

**Condiciones de rechazo:** registro vacío o plantilla sin revisión; revisor que es el único generador; ausencia de hallazgos examinados; fecha o dictamen no verificables; checksum distinto del artefacto revisado.

**Dependencias:** ORACLE-ART-01, ORACLE-ART-03.

**Evidencia de reproducibilidad:** conservar la lista de casos examinados y la correspondencia con `rule_id`.

**Responsable de revisión y aprobación:** revisor independiente; aprobación del propietario como prerrequisito de autorización técnica.

**Relación CP-C:** CP-C-05, CP-C-13.

---

### 4.5 ORACLE-ART-05 — Evidencia de cobertura de las 139 rutas

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-05` |
| Propósito | Demostrar que cada ruta normativa fue comparada semánticamente, no solo contada |
| Fuente normativa | R9 §5.4 (allowlist), §5.8.2 pasos 2–3, §5.8.5 artefacto 5 |
| Estado actual | `NOT_CREATED` |

**Estructura de la matriz:** una fila por cada una de las **139 rutas expandidas**, con columnas:

| Columna | Contenido |
|---|---|
| Ruta normativa | Ruta expandida, con la partición concreta cuando corresponda |
| Condición de aplicabilidad | Según R9 §5.1/§5.3/§5.8.3 |
| Comportamiento esperado | Derivado de §9.2 y de la entrada de allowlist, incluida la pertenencia o no a la proyección |
| Resultado observado | A registrar en la futura ejecución; **no se completa ahora** |
| Caso positivo/negativo | Identificador del caso de prueba que cubre la ruta |
| Evidencia reproducible | Referencia a salida de la verificación, sin inventarla |
| Correspondencia con el oracle | `rule_id` y metadatos de ORACLE-ART-01 |

**Criterios de aceptación:** 139 filas únicas; cada fila con resultado observado y caso asociado; compartimentos `train`/`validation`/`calibration`/`test` correctamente expandidos; coincidencia con la tabla §5.4.

**Condiciones de rechazo:** contar 139 filas sin semántica por fila; rutas duplicadas; `shared_with` tratado como permitido fuera de calibration; omisión de `base_*` condicionales.

**Dependencias:** ORACLE-ART-01, ORACLE-ART-02.

**Evidencia de reproducibilidad:** conservar entradas y salidas de la comparación de conjuntos en ambos sentidos (`ALLOWLIST_MISSING_PATH` / `ALLOWLIST_EXTRA_PATH`).

**Responsable de revisión y aprobación:** revisor independiente y auditor.

**Relación CP-C:** CP-C-05, CP-C-08.

---

### 4.6 ORACLE-ART-06 — Evidencia de comprobación de los nueve metadatos

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-06` |
| Propósito | Demostrar que `ALLOWLIST_V4` coincide con el oracle en los nueve campos de `AllowlistEntry` |
| Fuente normativa | R9 §5.1 (estructura), §5.8.1 (diez campos del oracle), §5.8.2 paso 4, §5.8.5 artefacto 6 |
| Estado actual | `NOT_CREATED` |

**Los nueve metadatos exactos** (obtenidos de R9 §5.1, no reconstruidos de memoria):

| # | Nombre | Dominio / semántica según R9 |
|---|---|---|
| 1 | `path` | Ruta dotted; `{partition}` es plantilla (§5.1) |
| 2 | `type` | `string`, `integer`, `number`, `boolean`, `array`, `object`, `timestamp`, `string_decimal` (§5.2, §5.7) |
| 3 | `manifest_required` | Booleano; obligatoriedad sin condición (§5.1) |
| 4 | `manifest_required_when` | `None` o `partition == 'calibration'` (§5.3, §5.7) |
| 5 | `manifest_allowed_when` | `None` o `partition == 'calibration'` (§5.3, §5.7) |
| 6 | `projection_include_when` | `always` o `external_run_only` (§5.3, §5.7) |
| 7 | `projection_optional` | Booleano; omisión sin inventar `None` (§5.1) |
| 8 | `nullable` | Booleano; preservación de `None` explícito (§5.1) |
| 9 | `normalization` | `none` o `timestamp_utc_9` (§5.1, §5.7, §7) |

El décimo campo del oracle, `rule_id`, se usa para trazabilidad normativa, no forma parte de los nueve metadatos comparados (R9 §5.8.1–5.8.2).

**Estructura de la evidencia:** una fila por ruta común y por campo, con valor del oracle, valor de `ALLOWLIST_V4`, resultado de la comparación y código de error si hay divergencia (`ALLOWLIST_ORACLE_METADATA_DIVERGENCE`).

**Casos mínimos:** incluir al menos los casos de `base_*` (`external_run_only`), `shared_with` (P2), un campo con `nullable=True`, un timestamp con `timestamp_utc_9` y un `string_decimal`.

**Criterios de aceptación:** los nueve campos presentes y comparados para cada ruta; divergencias reportadas con el campo divergente; ausencia de fallback.

**Condiciones de rechazo:** campo omitido en la comparación; comparación limitada a conjuntos de rutas; valores tomados del schema para sustituir una condición normativa ausente del schema; divergencia silenciada.

**Dependencias:** ORACLE-ART-01, ORACLE-ART-02, ORACLE-ART-05.

**Evidencia de reproducibilidad:** conservar la salida determinista de la comparación con orden y deduplicación.

**Responsable de revisión y aprobación:** revisor independiente y auditor.

**Relación CP-C:** CP-C-05, CP-C-07, CP-C-13.

---

### 4.7 ORACLE-ART-07 — Evidencia de la mutación `external_run_only`

| Campo | Especificación |
|---|---|
| Identificador estable | `ORACLE-ART-07` |
| Propósito | Demostrar que el oracle detecta una alteración de la condición normativa `external_run_only`, aunque el schema no la codifica |
| Fuente normativa | R9 §5.8.2 «Detección de external_run_only»; §5.8.5 artefacto 7; diseño v4 §9.2 |
| Estado actual | `NOT_CREATED` |

**Estado original:** las tres rutas `calibration.base_model_id`, `calibration.base_artifact_sha256.rf` y `calibration.base_artifact_sha256.xgb` declaran `projection_include_when=external_run_only` en `ALLOWLIST_V4` y en el oracle.

**Mutación exacta:** en una **copia aislada** de `ALLOWLIST_V4`, cambiar `external_run_only` por `always` en esas tres rutas, manteniendo los demás metadatos sin cambios.

**Resultado esperado antes de la mutación:** la comparación no reporta divergencia de `projection_include_when`.

**Resultado esperado después de la mutación:** la comparación contra el oracle reporta `ALLOWLIST_ORACLE_METADATA_DIVERGENCE` con campo `projection_include_when` para las tres rutas. Pueden aparecer además errores internos de I6(a); la aceptación exige específicamente la detección por el oracle.

**Evidencia de detección:** salida determinista de la verificación, con las tres rutas y el campo divergente; registro de que la mutación se aplicó solo a la copia.

**Criterio de aceptación:** detección exacta en las tres rutas; ninguna ruta addicional; ausencia de fallback que restaure silenciosamente el valor original.

**Reversibilidad y aislamiento:** la mutación se ejecuta solo en entorno aislado durante futura tarea autorizada; se conserva la copia mutada y su salida; la copia se descarta sin afectar `ALLOWLIST_V4` ni producción.

**Condiciones de rechazo:** mutación ejecutada sobre la representación productiva; detección atribuida solo a validaciones internas; mutación no reversible; ausencia de registro de la copia.

**Dependencias:** ORACLE-ART-01, ORACLE-ART-02, ORACLE-ART-06.

**Evidencia de reproducibilidad:** conservar la copia original, la copia mutada, la salida antes/después y el procedimiento de aislamiento.

**Responsable de revisión y aprobación:** revisor independiente y auditor.

**Relación CP-C:** CP-C-05, CP-C-08, CP-C-13.

---

## 5. Matriz consolidada de aceptación

| Artefacto | Requisitos clave | Criterio de aceptación | Verificación independiente | CP-C | Dependencias | Estado actual |
|---|---|---|---|---|---|---|
| ORACLE-ART-01 | 139 rutas, diez campos, P1–P5, I1–I12, §§5.2/5.5/5.7, fail-closed | Revisión semántica contra §9.2 sin copiar código productivo | Revisor distinto del generador | 05, 13 | — | `NOT_CREATED` |
| ORACLE-ART-02 | Independiente, determinista, reproducible, sin fallback | Auditoría de independencia y resultados | Ejecución aislada y revisión | 05, 13 | 01 | `NOT_CREATED` |
| ORACLE-ART-03 | JCS de `{version, entries}`, SHA-256 hex | Reproducible por verificador distinto | Recálculo independiente | 05, 13 | 01, 02 | `NOT_CREATED` |
| ORACLE-ART-04 | Revisor, alcance, casos, hallazgos, dictamen, fecha | Revisión real y documentada | Auditoría del registro | 05, 13 | 01, 03 | `NOT_CREATED` |
| ORACLE-ART-05 | 139 filas con semántica por ruta | Cobertura completa y correcta | Comparación de conjuntos | 05, 08 | 01, 02 | `NOT_CREATED` |
| ORACLE-ART-06 | Nueve metadatos por ruta | Sin divergencia no reportada | Comparación campo por campo | 05, 07, 13 | 01, 02, 05 | `NOT_CREATED` |
| ORACLE-ART-07 | Mutación aislada de `external_run_only` | Detección por oracle en tres rutas | Revisión de antes/después | 05, 08, 13 | 01, 02, 06 | `NOT_CREATED` |

La transición entre estados solo puede producirse con evidencia material. Ningún artefacto se marca `VERIFIED` en esta especificación.

---

## 6. Independencia y prevención de circularidad

| Riesgo | Control exigido |
|---|---|
| El oracle reproduzca el resultado del código productivo | Transcripción desde §9.2/DEC-06, no desde `ALLOWLIST_V4`; `rule_id` por fila normativa |
| Producción importe el oracle | Prohibición explícita en R9 §5.6 y §5.8.5; verificación de importaciones en CI |
| Los tests se conviertan en fuente normativa | El oracle es verificador; la autoridad es §9.2/DEC-06 y el schema en su nivel |
| El mismo generador sea el único verificador | Revisor funcionalmente independiente y auditoría externa del proceso |
| Checksum válido interpretado como corrección semántica | R9 §5.8.1: la revisión humana no se sustituye por checksum |
| Revisión humana interpretada como aprobación automática | La aprobación técnica sigue siendo decisión separada del propietario |

La verificación de consistencia se ejecuta fuera del camino productivo. La ausencia o discrepancia del oracle bloquea CI y la aceptación, sin fallback ni representación alternativa.

---

## 7. Trazabilidad normativa

| Requisito | Referencia |
|---|---|
| Los siete artefactos y su contenido mínimo | R9 §5.8.5, artefactos 1–7 |
| Diez campos del oracle y nueve metadatos comparados | R9 §5.8.1 y §5.8.2 paso 4; §5.1 |
| Autoridad normativa | DEC-06; diseño v4 §9.2; aprobación DEC-01…DEC-09 |
| Contrato estructural | `manifest_v4.json`, `$defs/partition` y `$defs/calibration_partition` |
| Patrones y condiciones | R9 §5.8.3 (P1–P5, matriz O/A) y §5.3 |
| Invariantes y errores | R9 §5.7 (I1…I12, códigos `ALLOWLIST_*`) |
| Normalización temporal | R9 §7 y diseño v4 §5.2 |
| JCS y digest | R9 §6.4, §8; RFC 8785 |
| Validaciones productivas | R9 §5.6; `provenance_v4.py::validate_manifest_v4`; Fase A/B |
| Separación producción/CI | R9 §5.6, §5.8.2, §5.8.5 |
| Criterios de aceptación futuros | R9 §9: CP-C-05, CP-C-07, CP-C-08, CP-C-13; plan V4-U10/V4-U11 |
| Aprobación del diseño y límites | `docs/r13_owner_design_approval_r1.md`; AUD-R8-02 `OPEN` |

---

## 8. Cuestiones pendientes y ambigüedades

Se registran como pendientes, sin resolver unilateralmente:

1. **Esquema concreto de `rule_id`:** R9 exige que identifique la fila de §9.2, pero no fija su formato. Deberá proponerse en la futura tarea autorizada y aprobarse con la revisión de ORACLE-ART-01.
2. **Ubicación de la versión ejecutable y del checksum:** R9 §5.8.1 dice que el checksum se guarda junto con el oracle «en el módulo de pruebas»; la ubicación física deberá decidirse sin introducir dependencia productiva.
3. **Identidad funcional del revisor y del auditor:** no se prescribe nombre ni rol organizativo adicional; se registrará cuando exista la revisión real.
4. **Formato de la evidencia de ejecución:** no se elige herramienta ni formato de salida; debe ser reproducible y auditable.
5. **Convención de versiones futuras:** `ORACLE_NORMATIVE_V4_R5` se conserva mientras §9.2 no cambie; cualquier cambio requiere nueva versión aprobada conforme a R9 §5.8.1.

Ninguna de estas cuestiones se resuelve aquí mediante una decisión normativa nueva.

---

## 9. Límites y estado

Esta especificación:

- No crea los siete artefactos; todos permanecen `NOT_CREATED`.
- No genera transcripción, checksum, evidencia ni revisión humana.
- No implementa Fase C, no ejecuta pruebas, no produce fingerprints.
- No modifica R9, su registro de aprobación, documentos históricos, código, tests, schemas, dependencias, modelos ni datasets.
- No autoriza la implementación ni declara cumplido prerrequisito alguno.

AUD-R8-02 continúa `OPEN`. La autorización técnica de implementación sigue sin concederse. Fase C permanece `BLOCKED_PENDING_TECHNICAL_AUTHORIZATION_AND_ORACLE_ARTIFACTS`; D, E, F, G y S2 permanecen sin autorización.

**Fin de R13-ORACLE-ARTIFACTS-SPECIFICATION-R1.**
