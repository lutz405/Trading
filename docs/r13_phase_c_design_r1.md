# R13-PHASE-C-DESIGN-R1 — Diseño técnico de canonicalización JCS y fingerprints

**Estado del documento:** propuesta de diseño. No implementa Fase C, no autoriza su implementación y no modifica decisiones aprobadas.
**Fecha:** 2026-11-27.
**Base:** commit `259ca6ee11878f114cdcab4cef500074b3bc1a48` (`main`, `origin/main` alineados, árbol limpio).
**Fase C:** **BLOCKED** hasta aprobación explícita del propietario.

**Convención:** todas las funciones, mensajes y estructuras descritas como `[PROPUESTA]` no existen hoy en el código. Se describen para su revisión, no como implementación.

---

## 1. Resumen ejecutivo

1. Fase C se limita a canonicalización JCS, proyección exacta de la allowlist de DEC-06, cálculo de `run_fingerprint` y primitivas de preimagen/hash reutilizables. No incluye Fase D, E, F, G ni S2.
2. El único mecanismo de canonicalización propuesto es la librería `rfc8785` ya declarada (`rfc8785>=0.1.4`), verificada en el entorno como versión `0.1.4`. No se propone `repr()`, `json.dumps()` ni serialización propia.
3. El validador público `validate_manifest_v4(...) -> list[str]` permanece sin cambios de firma; se propone añadir comprobación del `run_fingerprint` declarado contra el calculado.
4. La proyección debe construir un objeto nuevo con rutas normativas exactas, sin copiar el manifiesto, sin incluir el propio digest y sin rellenar defaults.
5. Los fingerprints identifican intención declarada; **no demuestran autenticidad, autoría ni autorización**. Las firmas Ed25519 pertenecen a Fase F.
6. Se proponen 30 pruebas de diseño y 18 criterios CP-C, ninguno ejecutado en este documento.
7. Quedan cuestiones que requieren decisión del propietario antes de autorizar la implementación (§14).

---

## 2. Estado y base revisada

| Elemento | Hecho verificado |
|---|---|
| HEAD / rama / remoto | `259ca6ee…`, `main`, `origin/main` alineado |
| Árbol de trabajo | Limpio; sin cambios locales |
| Cierre previo | `259ca6ee…` contiene el cierre documental R1.2 de V4-U06 / DEC-09 |
| Código v3 | `src/tradingai/ml/provenance.py`: `jcs_canonicalize`, `jcs_canonical_bytes`, `sha256_bytes`, `sha256_canonical`, `parse_json_strict` |
| Código v4 actual | `src/tradingai/ml/provenance_v4.py`: schema, patrones, enteros seguros, timestamps, evidencia, DEC-09. **No contiene JCS v4 ni fingerprints** |
| Schema v4 | `src/tradingai/schemas/manifest_v4.json`, cerrado, con campos de allowlist |
| Librería JCS | `rfc8785` 0.1.4: `dumps() -> bytes`; `FloatDomainError`, `IntegerDomainError`, `CanonicalizationError`; orden por UTF-16BE; rechazo de NaN/Inf y enteros fuera de `±(2^53−1)` |
| Pruebas v3 existentes | Vectores `1e-6`, `1e-7`, `1e20`, `1e21`, `-0`, Unicode UTF-16, rangos seguros, delegación a `rfc8785`, parsing estricto |

No se ejecutaron pruebas ni se modificó código para este diseño.

---

## 3. Objetivos y límites

### 3.1 Objetivos asignados a Fase C

- **C1** Canonicalización JCS conforme a RFC 8785.
- **C2** Proyección exacta de la allowlist normativa de §9.2.
- **C3** Cálculo reproducible de `run_fingerprint` y primitivas de preimagen/hash.
- **C4** Errores deterministas y compatibles con `list[str]`.
- **C5** Preservación exacta del comportamiento v3.
- **C6** Matriz de pruebas sin resultados inventados.

### 3.2 Exclusiones expresas

No se diseña ni implementa en este documento:

- Fase D: gaps, purga, embargo, equivalencia de calibration, verificación de particiones contra datos.
- Fase E: cadenas de eventos, transiciones, evidencia asociada en contexto de cadena.
- Fase F: sidecars, Ed25519, verificación criptográfica, confianza o autorización.
- Fase G: integración final.
- Loaders, registry, writer, deserialización, inferencia, entrenamiento, backtesting.
- Acceso a Parquet protegidos.

---

## 4. Requisitos normativos

| Fuente | Requisito |
|---|---|
| DEC-05 | Contratos 3.0.0 y 4.0.0 independientes; sin conversión ni defaults de migración |
| DEC-06 | `run_fingerprint = SHA-256(JCS(allowlist §9.2))`; presencia vs `null`; excluir identificadores de salida, timestamps, artefactos, métricas y hashes derivados; verificar independientemente cuatro digests |
| DEC-03 | `extensions={}` y excluido del fingerprint |
| DEC-09 | `class_order` permutación exacta de `classes`; normalización `1 ≡ 1.0` |
| Diseño v4 §5.2 | Timestamps RFC 3339 con zona explícita, UTC sin pérdida, 9 decimales |
| Diseño v4 §5.3 | Normalización numérica limitada; booleanos no normalizados |
| Diseño v4 §9.1 | RFC 8785 única; finitos permitidos donde el esquema declare number; NaN/Inf rechazados; enteros `abs(n) <= 2^53−1` |
| Diseño v4 §9.4 | Preimágenes: `index_sha256`, `partition_manifest_sha256`, `calibration_input_sha256`, `run_fingerprint`, `event_sha256`; sin ciclos; JCS sin LF para digests; `manifest.sha256` con LF |
| Plan R1.2 Fase C | Modificar `provenance_v4.py`; reutilizar `rfc8785`; no tocar v3; V4-U10/V4-U11 |
| Matriz §6.1 | V4-U10 (mutación de rutas incluidas/excluidas), V4-U11 (recalculación independiente) |

---

## 5. Diseño de canonicalización JCS (C1)

### 5.1 Primitiva única `[PROPUESTA]`

```python
def _jcs_bytes_v4(obj: Any) -> bytes: ...
```

- Debe invocar directamente `rfc8785.dumps(obj)`.
- No debe usar `repr()`, `json.dumps()`, `sort_keys=True` ni comparaciones dependientes de locale.
- Devuelve bytes UTF-8, sin BOM y sin salto de línea final.
- Se define en `provenance_v4.py` como wrapper privado. No se importa `provenance.jcs_canonical_bytes` desde v4 para evitar ciclo (`provenance.py` ya importa `provenance_v4`).
- No se modifica la implementación v3.

### 5.2 Reglas exactas delegadas a `rfc8785`

| Regla | Comportamiento esperado de la librería 0.1.4 |
|---|---|
| Orden de propiedades | Orden lexicográfico por unidades UTF-16 sin signo (implementado con `utf-16be`) |
| Arrays | Conservan su orden; no se ordenan |
| Separadores | `,` y `:` sin espacios |
| Strings | Escapes JCS/RFC 8259; UTF-8; surrogates no representables rechazados |
| Números | Formato ECMAScript `Number::toString`; `1e-6 → 0.000001`; `1e-7 → 1e-7`; `1e20 → 100000000000000000000`; `1e21 → 1e+21` |
| `-0` | `-0` y `-0.0` → `0` |
| NaN/Infinito | `FloatDomainError` |
| Enteros seguros | `±(2^53−1)` aceptados; fuera de rango `IntegerDomainError` |
| Tipos no JSON | `CanonicalizationError` u error equivalente; convertir a error tipado interno |

### 5.3 Tratamiento de valores no representables

- `parse_json_strict` en la entrada evita BOM, claves duplicadas y `NaN`/`Infinity` literales.
- `validate_safe_integers_v4` rechaza enteros fuera del rango antes de JCS.
- El wrapper debe capturar `rfc8785.CanonicalizationError` y subclases y convertirlas a `[PROPUESTA] CanonicalizationV4Error`, sin exponer tracebacks al contrato público.
- No se coercean strings numéricos a números.

### 5.4 Bytes hasheados

- Para `run_fingerprint` y los cuatro digests declarados: `SHA-256(JCS UTF-8 sin LF)`.
- `manifest.sha256` (fuera de esta fase): bytes JCS + exactamente un LF; no debe confundirse con los anteriores.
- Ninguna preimagen incluye el digest que produce.

---

## 6. Diseño de proyección (C2)

### 6.1 Principio

Construir un objeto nuevo, no filtrar el manifiesto. Cada ruta incluida se copia explícitamente desde el manifiesto validado a su posición exacta en la preimagen. La tabla de allowlist debe residir en el módulo v4 como dato versionado `[PROPUESTA] ALLOWLIST_V4`.

### 6.2 Allowlist exacta

| Rutas | Regla |
|---|---|
| `schema_version` | Incluir |
| `model_id`, `created_at`, `sealed_at`, `status_at_seal`, `run_fingerprint` | Excluir |
| `git.source_bundle_sha256` | Incluir |
| `git.commit`, `git.dirty`, `git.branch`, `git.tag` | Excluir (`dirty=false` solo admisión) |
| `producer.name`, `producer.version`, `producer.python`, `producer.config_sha256` | Incluir |
| `producer.command` | Excluir |
| `data.symbol`, `data.timeframe`, `data.provider`, `data.provider_version`, `data.dataset_sha256`, `data.raw_rows`, `data.feature_rows`, `data.labeled_rows`, `data.time_range.start`, `data.time_range.end`, `data.time_range.timezone`, `data.missing_data_policy`, `data.gap_policy`, `data.ohlcv_schema_version`, `data.alignment` | Incluir; timestamps normalizados |
| `data.snapshot_uri` | Excluir |
| `target.name`, `target.horizon_bars`, `target.vol_mult`, `target.classes`, `target.class_order`, `target.rule_sha256`, `target.nan_policy` | Incluir |
| `features.ordered`, `features.count`, `features.definition_sha256`, `features.matrix_sha256`, `features.pipeline_version`, `features.code_sha256`, `features.parameters.lookback_max`, `features.parameters.lookback_min`, `features.parameters.lookback_step`, `features.parameters.lookback_total`, `features.nan_policy` | Incluir si están presentes; ausencia se conserva |
| `training.task`, `training.models.rf.library`, `training.models.rf.version`, `training.models.rf.params.n_estimators`, `training.models.rf.params.max_depth`, `training.models.rf.params.class_weight`, `training.models.rf.params.random_state`, `training.models.rf.params.n_jobs`, `training.models.xgb.library`, `training.models.xgb.version`, `training.models.xgb.params.n_estimators`, `training.models.xgb.params.max_depth`, `training.models.xgb.params.learning_rate`, `training.models.xgb.params.subsample`, `training.models.xgb.params.colsample_bytree`, `training.models.xgb.params.random_state`, `training.models.xgb.params.tree_method`, `training.models.xgb.params.device`, `training.models.xgb.params.objective`, `training.models.xgb.params.num_class`, `training.models.xgb.params.eval_metric`, `training.models.xgb.params.n_jobs`, `training.ensemble.method`, `training.ensemble.weights.rf`, `training.ensemble.weights.xgb`, `training.seed` | Incluir si están presentes; `null` permitido se conserva |
| `training.environment.python`, `.numpy`, `.pandas`, `.scikit_learn`, `.xgboost`, `.joblib`, `.os`, `.arch`, `.cuda_version`, `.cudnn_version` | Incluir; CUDA/cuDNN ausentes o `null` conservan distinción |
| `training.hardware.device`, `.gpu_model`, `.cuda_version`, `.cpu_count`, `.ram_gb` | Incluir; anulables conservan `null` |
| `training.determinism.bitwise_reproducible`, `.n_jobs`, `.omp_num_threads`, `.xgb_tree_method`, `.xgb_deterministic_histogram`, `.gpu_deterministic` | Incluir |
| `validation.split_method`; para `train`, `validation`, `calibration`, `test`: `row_start`, `row_end`, `source_position_start`, `source_position_end`, `n_rows`, `time_start`, `time_end`, `class_counts`, `index_sha256`, `shared_with` cuando exista | Incluir; timestamps normalizados |
| `validation.purge.rows_between_partitions`, `.label_horizon_bars`, `.embargo_rows` | Incluir |
| `validation.purge.label_purge_satisfied`, `validation.leakage_checks.disjoint`, `.purge_satisfied`, `.labels_within_partition` | Excluir: resultados derivados |
| `validation.partition_manifest_sha256` | Excluir: digest derivado |
| `validation.evaluation.*` | Excluir: protocolo/resultado de evaluación |
| `calibration.mode`, `.method`, `.fit_partition`, `.classes`, `.class_order`, `.n_calibrators` | Incluir |
| `calibration.base_model_id`, `calibration.base_artifact_sha256.rf`, `.xgb` | Incluir **solo** si `mode = external_run`; excluir si `in_pipeline` |
| `calibration.calibration_input_sha256`, `calibration.artifact_sha256` | Excluir |
| `artifacts[]` y propiedades | Excluir |
| `metrics.*` | Excluir |
| `extensions` | Excluir |

### 6.3 Algoritmo `[PROPUESTA]`

```python
def project_allowlist(manifest: dict[str, Any]) -> dict[str, Any]: ...
```

1. Verificar que el manifiesto ya pasó schema v4, enteros seguros, DEC-09 y validación de timestamps.
2. Recorrer la tabla de allowlist, no el manifiesto.
3. Para cada ruta incluida, leer el valor con acceso exacto; si la ruta no existe y es opcional, omitir la clave; si es `null` permitted, copiar `None` explícito.
4. Normalizar timestamps incluidos usando `normalize_timestamp`.
5. Aplicar condicional de `calibration.base_*` según `mode`.
6. No copiar ningún campo excluido, ni siquiera como clave con valor `None`.
7. No modificar el objeto recibido.
8. El dict resultante se construye en orden explícito de la allowlist; JCS ordena de todos modos por UTF-16, por lo que el orden de inserción del manifiesto original no afecta el resultado.

### 6.4 Ausencia frente a `null`

- Ausente → clave no presente en la preimagen.
- `null` explícito → clave presente con valor `None` solo si la ruta es anulable según schema/diseño.
- No se usa `.get(path, default)` con defaults que inventen presencia.

### 6.5 Prevención de campos derivados

La tabla excluye explícitamente resultados derivados, digests de outputs, métricas y `extensions`. La proyección no debe usar "copiar todo y quitar"; debe construir desde cero.

---

## 7. Diseño de fingerprints (C3)

### 7.1 `run_fingerprint` `[PROPUESTA]`

```python
def build_run_fingerprint(manifest: dict[str, Any]) -> str: ...
```

Algoritmo:

1. `projection = project_allowlist(manifest)`
2. `payload = _jcs_bytes_v4(projection)`
3. `digest = hashlib.sha256(payload).hexdigest()` (minúsculas, 64 caracteres)
4. No incluir `run_fingerprint` en `projection`.

### 7.2 Comparación con el valor declarado `[PROPUESTA]`

```python
def validate_fingerprints_v4(manifest: dict[str, Any]) -> list[str]: ...
```

- Si `manifest['run_fingerprint']` no es válido, el schema ya reporta el formato; no duplicar.
- Si es válido pero distinto del calculado, devolver `$.run_fingerprint: does not match computed run_fingerprint`.
- Si la proyección o JCS falla, devolver error determinista y no aceptar el manifiesto por omisión.

**Cuestión pendiente de aprobación:** confirmar que Fase C debe exigir esta igualdad dentro de `validate_manifest_v4`, en lugar de exponer solo el constructor. Ver §14.

### 7.3 Primitiva común de digest `[PROPUESTA]`

```python
def _digest_preimage(preimage: Any) -> str: ...
```

`sha256(_jcs_bytes_v4(preimage)).hexdigest()`. Sin LF. Reutilizable para los cuatro digests.

### 7.4 Otras preimágenes `[PROPUESTA]`

| Digest | Preimagen | Constructor propuesto | Límite de Fase C |
|---|---|---|---|
| `run_fingerprint` | allowlist §9.2 | `build_run_fingerprint(manifest)` | Completo |
| `partition_manifest_sha256` | `{"train": ..., "validation": ..., "calibration": ..., "test": ...}` con objetos completos de partición, incluidos `index_sha256` y `shared_with` | `build_partition_manifest_sha256(manifest)` | Completo; sin Fase D |
| `index_sha256` | `[[row, source_position, timestamp_utc, label], ...]` en orden de filas | `build_index_sha256(rows)` | Requiere secuencia explícita; **sin reconstrucción desde OHLCV ni Fase D** |
| `calibration_input_sha256` | `{"schema":"tradingai.calibration-input.v1","index_sha256":...,"class_order":...,"y":...,"proba_rf_f64be":...,"proba_xgb_f64be":...}` | `build_calibration_input_sha256(inputs)` | Requiere entradas efectivas; sin datos reales |
| `event_sha256` | payload canónico de nueve campos, excluyendo `event_sha256` | `build_event_sha256(payload)` | Primitiva para Fase E; **sin cadenas ni transiciones** |

Detalles:

- `partition_manifest_sha256` no omite campos por redundantes; conserva `class_counts` y `index_sha256`.
- `proba_*_f64be`: cada probabilidad se convierte a IEEE-754 binary64 big-endian y se representa como 16 hexadecimales minúsculos; se rechazan no finitos y fuera de `[0,1]`; `-0.0` se normaliza a positivo.
- `event_sha256`: los nueve campos son los de DEC-07; no se incluye `event_sha256` ni sidecar.
- Ningún constructor accede a archivos ni a datasets.

### 7.5 Fingerprint frente a firma

| Propiedad | Fingerprint | Firma Ed25519 |
|---|---|---|
| Qué demuestra | Misma intención declarada | Posesión de clave privada |
| Entrada | Allowlist canónica | Bytes JCS del payload de nueve campos (eventos) o política futura |
| Clave | Ninguna | Privada fuera del repositorio |
| Autoría/autorización | No demuestra | Tampoco por sí sola; requiere política |

No se debe afirmar autenticidad, identidad del autor ni autorización a partir de `run_fingerprint`.

---

## 8. Contratos e interfaces propuestos

### 8.1 Públicas existentes (sin cambios de firma)

- `validate_manifest_v4(manifest: object) -> list[str]` — permanece; solo añade errores de fingerprint si se aprueba §7.2.
- `validate_manifest(manifest: dict[str, Any]) -> list[str]` en `provenance.py` — permanece intacto; dispatch v3/v4 sin cambios.

### 8.2 Privadas propuestas en `provenance_v4.py`

| Función | Entrada | Salida |
|---|---|---|
| `_jcs_bytes_v4(obj)` | JSON-compatible | `bytes` |
| `_digest_preimage(preimage)` | JSON-compatible | `str` hex 64 |
| `normalize_timestamp(value)` | `str` RFC 3339 | `str` normalizado 9 decimales UTC |
| `project_allowlist(manifest)` | `dict` validado | `dict` proyectado |
| `build_run_fingerprint(manifest)` | `dict` validado | `str` hex 64 |
| `build_partition_manifest_sha256(manifest)` | `dict` validado | `str` hex 64 |
| `build_index_sha256(rows)` | secuencia de filas | `str` hex 64 |
| `build_calibration_input_sha256(inputs)` | entradas efectivas | `str` hex 64 |
| `build_event_sha256(payload)` | payload de 9 campos | `str` hex 64 |
| `validate_fingerprints_v4(manifest)` | `dict` validado | `list[str]` |

### 8.3 Excepciones internas propuestas

- `CanonicalizationV4Error`
- `ProjectionV4Error`
- `TimestampNormalizationV4Error`
- `FingerprintV4Error`

Todas se convierten a mensajes `list[str]` antes de cruzar la API pública. No se capturan errores para convertirlos en aceptación.

### 8.4 Normalización de timestamps `[PROPUESTA]`

`normalize_timestamp(value)`:

1. Aceptar `Z` o desplazamiento numérico `±HH:MM`.
2. Rechazar zona ausente, `-00:00`, segundo `60`, más de 9 dígitos fraccionarios y fechas inválidas.
3. Validar offsets (`HH <= 23`, `MM <= 59`).
4. Convertir a UTC usando aritmética entera de nanosegundos para no perder precisión (Python `datetime` solo tiene microsegundos).
5. Formatear exactamente `YYYY-MM-DDTHH:MM:SS.fffffffffZ`, rellenando con ceros a la derecha; sin truncamiento ni redondeo.

---

## 9. Gestión de errores (C4)

| Condición | Comportamiento propuesto | Ruta/mensaje |
|---|---|---|
| Campo desconocido en preimagen | No se copia; si schema ya lo rechaza, no duplicar | Schema existente |
| Campo obligatorio ausente | Schema reporta; proyección no inventa valor | `$.<ruta>` |
| `null` en campo no anulable | Schema reporta; fingerprint no se calcula | `$.<ruta>` |
| Booleano donde se espera número | Schema/JCS rechazan; sin coerción | `$.<ruta>` |
| Entero fuera de rango seguro | `validate_safe_integers_v4` + `IntegerDomainError` convertido | `$.<ruta>: integer outside JCS safe range` |
| NaN/Infinity | `parse_json_strict` y `FloatDomainError` convertido | `$.<ruta>: non-finite value` |
| String Unicode / surrogate | JCS serializa o rechaza surrogate | Error tipado interno |
| Estructura profundamente anidada | Capturar `RecursionError` y convertir | `$.<ruta>: structure too deep` |
| Valor no serializable | `CanonicalizationError` convertido | Error determinista |
| Entrada inválida al constructor | `FingerprintV4Error` → `list[str]` | Sin traceback |
| `run_fingerprint` declarado distinto | Error de comparación | `$.run_fingerprint: does not match computed run_fingerprint` |
| Preimagen con su propio digest | Prohibido por construcción; prueba de regresión | Sin ciclo |

---

## 10. Compatibilidad v3/v4 (C5)

| Elemento | Garantía |
|---|---|
| `jcs_canonicalize`, `jcs_canonical_bytes`, `sha256_bytes`, `sha256_canonical`, `parse_json_strict` | Congelados; sin cambios de cuerpo |
| `validate_manifest_v3` | Cuerpo ejecutable idéntico; verificación por extracción contra commit base |
| Dispatch en `provenance.py` | Sin cambios; `3.0.0` → v3, `4.0.0` → v4, desconocida → rechazo |
| Código v4 | Nuevas funciones en `provenance_v4.py`; sin importar `provenance` desde v4 para evitar ciclo |
| JCS | Misma librería `rfc8785`; wrapper privado v4, no refactor v3 |
| Regresiones | `TestJCSCanonicalization`, `TestJCSVectors`, `TestStrictJSONParsing`, `TestHashing`, 116 pruebas v3 y 29 de dispatch |
| Fallback | Ninguno; versión desconocida nunca se envía a v3 ni a v4 |

---

## 11. Arquitectura y diagramas

### 11.1 Flujo de datos `[PROPUESTA]`

```text
Manifiesto 4.0.0 (dict)
        │
        ▼
validate_manifest_v4  (schema + enteros seguros + DEC-09 + timestamps)
        │
        ├──▶ project_allowlist ──▶ normalize_timestamp ──▶ objeto proyectado
        │                                                   │
        │                                                   ▼
        │                                            _jcs_bytes_v4
        │                                                   │
        │                                                   ▼
        │                                            _digest_preimage
        │                                                   │
        ├──▶ validate_fingerprints_v4 ◀──────────────────────┘
        │            │
        │            └──▶ $.run_fingerprint: error si diverge
        │
        └──▶ list[str]  (contrato público)
```

Flujos auxiliares sin datos externos:

```text
partition objects ─▶ build_partition_manifest_sha256 ─▶ SHA-256(JCS)
rows explícitas ───▶ build_index_sha256 ──────────────▶ SHA-256(JCS)
entradas calibración ─▶ build_calibration_input_sha256 ▶ SHA-256(JCS)
payload 9 campos ───▶ build_event_sha256 ─────────────▶ SHA-256(JCS)
```

### 11.2 Componentes y responsabilidades

| Componente | Responsabilidad |
|---|---|
| `provenance_v4.py` | Proyección, normalización, JCS v4, fingerprints, errores tipados |
| `manifest_v4.json` | Declara campos; no implementa canonicalización |
| `provenance.py` | Dispatch y validador v3 congelado |
| `rfc8785` | Única serialización canónica |
| `hashlib.sha256` | Único algoritmo de hash |
| Pruebas v4 | Vectores, mutación de rutas, errores, determinismo, integración |

### 11.3 Dependencias

- Fase A: dispatch presente.
- Fase B: schema v4 y validador semántico presentes.
- Dependencia externa existente: `rfc8785>=0.1.4`; no se añaden dependencias.
- Sin dependencia de Fase D/E/F para las primitivas auxiliares.

### 11.4 Garantías de determinismo

1. JCS ordena claves por UTF-16BE.
2. Arrays conservan orden.
3. Números usan el algoritmo ECMAScript de la librería.
4. Proyección construida desde allowlist, no desde iteración de diccionario.
5. Timestamps normalizados a forma canónica antes de JCS.
6. Digest siempre lowercase hex de 64 caracteres.
7. Sin LF en bytes hasheados.
8. Sin mutación del manifiesto de entrada.

---

## 12. Matriz de pruebas propuestas

**Todas son propuestas; ninguna se ejecutó en este documento.**

| ID | Objetivo | Entrada | Resultado esperado | Justificación | Criterio |
|---|---|---|---|---|---|
| C-T01 | Vector oficial RFC 8785 | Objeto del Apéndice B | Bytes iguales al texto oficial del RFC | Cumplimiento normativo | PASS si coinciden exactamente |
| C-T02 | Vector numérico `1e-6` | `1e-6` | `0.000001` | Vector ya usado en v3 | PASS |
| C-T03 | Vector numérico `1e-7` | `1e-7` | `1e-7` | Límite notación | PASS |
| C-T04 | Vector `1e20` | `1e20` | `100000000000000000000` | Decimal vs exponencial | PASS |
| C-T05 | Vector `1e21` | `1e21` | `1e+21` | Cambio de notación | PASS |
| C-T06 | `-0` y `-0.0` | ambos | `0` | Regla ECMAScript | PASS |
| C-T07 | Entero seguro máximo | `2**53-1` | `9007199254740991` | Rango permitido | PASS |
| C-T08 | Entero seguro mínimo | `-(2**53-1)` | `-9007199254740991` | Rango permitido | PASS |
| C-T09 | Entero fuera de rango | `2**53` | Error tipado, sin conversión truncada | DEC/§9.1 | PASS si error determinista |
| C-T10 | NaN / Infinity | `float('nan')`, `float('inf')` | Error `FloatDomainError` convertido | §9.1 | PASS |
| C-T11 | Orden UTF-16 | claves `U+E000`, `U+10000` | `U+10000` antes que `U+E000` | RFC 8785 §3.2.3 | PASS |
| C-T12 | String con escape | `quote"here`, Euro, salto | Escape JCS exacto | RFC 8259/JCS | PASS |
| C-T13 | Surrogate aislado | `'\ud800'` | Error, no bytes inválidos | UTF-8/JCS | PASS |
| C-T14 | Duplicados en JSON parse | `{"a":1,"a":2}` | `StrictJSONError` | Parsing estricto | PASS |
| C-T15 | Vector reducido §9.5 | Objeto del diseño | Hash `ed01f9…` como control JCS | No es vector 4.0.0 | PASS |
| C-T16 | Proyección mínima válida | Manifiesto fixture v4 | Objeto con solo rutas allowlist | C2 | PASS |
| C-T17 | Mutación de cada ruta incluida | Parametrizada por 51 rutas | Fingerprint cambia | V4-U10/DEC-06 | PASS por ruta |
| C-T18 | Mutación de rutas excluidas | `model_id`, `git.commit`, `command`, `snapshot_uri`, derived flags, `artifacts`, `metrics`, `extensions` | Fingerprint no cambia | DEC-06 | PASS por ruta |
| C-T19 | Ausencia vs null | `cuda_version` ausente / `None` | Preimagen distinta | §9.1/§9.3 | PASS |
| C-T20 | `1.0` vs `1` en clases | DEC-09 fixture | Fingerprint igual | DEC-09 | PASS |
| C-T21 | Condición `base_*` | `in_pipeline` vs `external_run` | Solo `external_run` incluye base | §9.2 | PASS |
| C-T22 | Timestamp normalización | `2026-11-25T12:00:00-06:00` | `2026-11-25T18:00:00.000000000Z` | §5.2 | PASS |
| C-T23 | Timestamp >9 decimales | `...1234567890Z` | Error | §5.2 | PASS |
| C-T24 | `run_fingerprint` declarado distinto | Manifest con hash ajeno | `$.run_fingerprint` error | C3 | PASS |
| C-T25 | Preimagen sin ciclo | Intentar incluir `run_fingerprint` en allowlist | Error de proyección | §9.4 | PASS |
| C-T26 | Determinismo | Mismo manifest 100 veces | Mismo fingerprint | C3 | PASS |
| C-T27 | No mutación | deepcopy antes/después | Iguales | C4 | PASS |
| C-T28 | Estructura profunda | 10.000 niveles | Error tipado, no traceback | C4 | PASS |
| C-T29 | Regresión v3 | suites v3 + dispatch | 116 + 29 + vectores | C5 | PASS |
| C-T30 | Integración v4 | schema v4 + DEC-09 + fingerprint | Sin errores en fixture válido | C6 | PASS |

Los vectores literales del Apéndice B distintos de C-T02…T08 se transcribirán del RFC oficial antes de implementar; no se inventan aquí.

---

## 13. Matriz CP-C propuesta

| ID | Criterio objetivo | Requisito | Prueba asociada | Resultado esperado |
|---|---|---|---|---|
| CP-C-01 | JCS usa `rfc8785`, sin `repr`/`json.dumps` | C1 | C-T01…T08 | Verificación de código + vectores |
| CP-C-02 | Vectores RFC 8785 reproducidos | C1 | C-T01…T08 | Todos PASS |
| CP-C-03 | `-0` y límites numéricos correctos | C1 | C-T06…T09 | Todos PASS |
| CP-C-04 | Orden UTF-16 y escapes correctos | C1 | C-T11, C-T12 | PASS |
| CP-C-05 | Proyección contiene exactamente la allowlist | C2 | C-T16…T18 | PASS por ruta |
| CP-C-06 | Ningún campo excluido altera el fingerprint | C2/DEC-06 | C-T18 | PASS |
| CP-C-07 | Ausencia vs `null` distinguidos | C2 | C-T19 | PASS |
| CP-C-08 | Condición `base_*` aplicada | C2 | C-T21 | PASS |
| CP-C-09 | `run_fingerprint` reproducible | C3/V4-U10 | C-T17, C-T26 | PASS |
| CP-C-10 | `run_fingerprint` declarado se compara | C3 | C-T24 | PASS (si owner aprueba §7.2) |
| CP-C-11 | Cuatro digests recalculables desde preimágenes | V4-U11 | C-T30 + pruebas auxiliares | PASS |
| CP-C-12 | Ninguna preimagen contiene su digest | §9.4 | C-T25 | PASS |
| CP-C-13 | Errores deterministas y tipados | C4 | C-T09, C-T10, C-T23, C-T28 | PASS |
| CP-C-14 | No mutación del manifiesto | C4 | C-T27 | PASS |
| CP-C-15 | v3 permanece idéntico | C5 | C-T29 + diff de cuerpo | PASS |
| CP-C-16 | Sin fallback entre versiones | C5/DEC-05 | C-T29 + dispatch tests | PASS |
| CP-C-17 | Sin regresiones v4 | C5/C6 | suite completa | PASS |
| CP-C-18 | Sin capacidades de Fases D–F | Límites | Revisión de diff | PASS |

---

## 14. Riesgos y cuestiones pendientes

| ID | Riesgo / cuestión | Impacto | Acción propuesta | Requiere propietario |
|---|---|---|---|---|
| Q-01 | ¿`validate_manifest_v4` debe rechazar `run_fingerprint` divergente en Fase C? | Cambia admisión | Decidir entre comparación integrada o solo constructor público | Sí |
| Q-02 | ¿Los constructores `index_sha256`/`calibration_input_sha256`/`event_sha256` se incluyen en C o se difieren a D/E? | Alcance | El diseño los propone como primitivas sin datos externos | Sí |
| Q-03 | Normalización UTC de 9 decimales en fingerprint vs Fase D | Posible divergencia | Un único helper en v4; D debe reutilizarlo | Sí, si cambia contrato |
| Q-04 | Deriva de allowlist por futuras versiones | Cambio silencioso de identidad | Tabla versionada y pruebas por ruta | No |
| Q-05 | Versión de `rfc8785` distinta en producción | Vectores diferentes | Registrar versión y no actualizar sin revalidar | Sí, si se fija versión |
| Q-06 | Confusión `manifest.sha256` (LF) vs digests JCS (sin LF) | Hash inválido | Documentar y probar separadamente | No |
| Q-07 | Campos derivados filtrándose en proyección | Fingerprint incorrecto | Construcción desde allowlist, no filtrado inverso | No |
| Q-08 | Strings decimales convertidos a números | Cambio de identidad | Mantener como strings; prueba C-T14 | No |

No se han introducido decisiones normativas nuevas. Las cuestiones marcadas "Sí" requieren aprobación antes de autorizar implementación.

---

## 15. Dependencias

- Fase A (dispatch) y Fase B (schema/validador v4): completadas y cerradas.
- DEC-05, DEC-06, DEC-03, DEC-09: aprobadas.
- `rfc8785` 0.1.4 y `jsonschema`: ya declarados.
- Sin dependencias nuevas, sin loaders, sin registry, sin writer, sin inferencia.
- Sin acceso a datasets ni Parquet.

---

## 16. Criterios para solicitar autorización de implementación

1. Propietario aprueba este diseño y resuelve Q-01, Q-02, Q-03 y Q-05.
2. Se confirma que Fase C modifica solo `provenance_v4.py` y pruebas nuevas.
3. Se confirma que no se tocará `provenance.py`, `manifest_v3.json`, `manifest_v4.json`, dependencias ni v3.
4. Se acepta la matriz de pruebas como criterio de aceptación.
5. Se acepta que los vectores dorados completos siguen aplazados y que el vector reducido es solo control JCS.
6. Se mantiene Fase D, E, F y G bloqueadas.

---

## 17. Conclusión y estado de Fase C

Este documento propone un diseño completo y verificable para canonicalización JCS y fingerprints conforme a DEC-06 y al plan R1.2. No implementa ninguna función, no ejecuta pruebas y no crea módulos.

**Fase C continúa BLOCKED.** La implementación solo podrá iniciarse tras aprobación explícita del diseño y autorización técnica separada del propietario. La aceptación de este diseño no autoriza Fase D, E, F, G ni S2.

**Fin de R13-PHASE-C-DESIGN-R1.**
