# R13-PHASE-C-DESIGN-R2 — Diseño corregido de canonicalización JCS y fingerprints

**Estado del documento:** propuesta de diseño R2, preparada para auditoría independiente. No implementa Fase C, no declara Fase C aprobada y no autoriza su implementación.
**Fecha:** 2026-11-27.
**Base:** commit `259ca6ee11878f114cdcab4cef500074b3bc1a48` (`main`, `origin/main` alineados).
**Predecesor:** `docs/r13_phase_c_design_r1.md` (R1), conservado sin modificaciones como historial.
**Auditoría incorporada:** `R13-AUDIT-PHASE-C-DESIGN-R1`, dictamen `ACCEPTED WITH FINDINGS`, nueve hallazgos F-C-01 a F-C-09.
**Fase C:** **BLOCKED** hasta auditoría independiente R2, aprobación expresa del propietario y autorización técnica separada.

---

## 1. Identificación y alcance de R2

R2 no sustituye retroactivamente a R1: lo corrige documentalmente para su revisión. R1 permanece como registro histórico. R2 incorpora:

- Las cuatro decisiones aprobadas por el propietario: Q-01, Q-02, Q-03 y Q-05.
- Las nueve correcciones obligatorias F-C-01 a F-C-09.
- La especificación formal de `ALLOWLIST_V4`.
- Los vectores del Apéndice B de RFC 8785 transcritos de la fuente oficial.
- La matriz CP-C-01 a CP-C-18 ajustada al alcance decidido.

**Alcance de implementación futura tras aprobación:** únicamente `src/tradingai/ml/provenance_v4.py` y pruebas nuevas de Fase C. No se modificarán `provenance.py`, `manifest_v3.json`, `manifest_v4.json`, dependencias, modelos ni datasets.

---

## 2. Referencias normativas y documentales

| Documento | Uso |
|---|---|
| `docs/aud04b_model_provenance_v4_approval_r1.md` | DEC-03, DEC-05, DEC-06, DEC-09; estado `APPROVED` |
| `docs/aud04b_model_provenance_v4_implementation_plan_r1.md` | Plan R1.2, Fase C, V4-U10/V4-U11, CP-C |
| `docs/aud04b_model_provenance_v4_design.md` | §§5.2, 5.3, 9.1, 9.2, 9.4, 9.5 |
| `docs/r13_decision_resolution_r1.md` | Cierre de V4-U06 / DEC-09 y límites de fases |
| `docs/r13_phase_c_design_r1.md` | Diseño previo, no modificado |
| `R13-AUDIT-PHASE-C-DESIGN-R1` | Hallazgos F-C-01 a F-C-09 (entregado en la conversación; no publicado como archivo en el repositorio) |
| RFC 8785 (June 2020), `https://www.rfc-editor.org/rfc/rfc8785.txt` | Vectores oficiales y reglas JCS; consultado el 2026-11-27 |
| Código real | `provenance.py`, `provenance_v4.py`, `manifest_v4.json`, pruebas v3/v4 |

---

## 3. Decisiones aprobadas por el propietario

### 3.1 Q-01 — Comparación de `run_fingerprint`

**Decisión aprobada:** Fase C implementará el constructor determinista de `run_fingerprint`, pero **no integrará** su comparación con el valor declarado en la semántica de admisión de `validate_manifest_v4`.

**Consecuencia:** la comparación durante la admisión queda fuera del alcance de Fase C y requiere diseño y autorización posteriores. CP-C-10 se reformula en §9.

### 3.2 Q-02 — Alcance de constructores de fingerprints

**Decisión aprobada:**

| Fase | Constructores asignados |
|---|---|
| C | `run_fingerprint`, `partition_manifest_sha256` |
| D | `index_sha256`, `calibration_input_sha256` |
| E | `event_sha256` |

**Consecuencia:** CP-C-11 y CP-C-18 se ajustan para no solaparse. R2 no diseña en detalle los constructores de D/E; solo registra la dependencia (§12).

### 3.3 Q-03 — Normalización UTC

**Decisión aprobada:** Fase C define **un único helper común** de normalización UTC, reutilizable por Fase D. El contrato se especifica en §7. No se implementa en esta tarea documental.

### 3.4 Q-05 — Dependencia `rfc8785`

**Decisión aprobada de diseño:** fijar `rfc8785==0.1.4`.

**Razón:** versión verificada en el entorno, con semántica conocida (`IntegerDomainError`, `FloatDomainError`, orden UTF-16BE) y compatibilidad demostrada con los vectores existentes en v3.

**Riesgo:** una actualización futura podría cambiar serialización o excepciones. Toda actualización exigirá revalidación de vectores RFC 8785 y nueva auditoría.

**Estado actual:** `pyproject.toml` declara `rfc8785>=0.1.4`. **No se modifica en R2**; el cambio a `==0.1.4` requiere autorización de dependencias en una tarea posterior.

---

## 4. Diseño técnico corregido

### 4.1 Síntesis de correcciones

| Hallazgo | Corrección aplicada en R2 |
|---|---|
| F-C-01 | §4.2 distingue timestamps de auditoría/salida excluidos de límites temporales de datos incluidos |
| F-C-02 | §9 y §5 eliminan el número fijo de 51 rutas; las pruebas se derivan de `ALLOWLIST_V4` |
| F-C-03 | §9 reformula CP-C-10, CP-C-11 y CP-C-18 según Q-01/Q-02 |
| F-C-04 | §8.2 incorpora el hash completo del vector reducido |
| F-C-05 | §4.3 explica `1.0 ≡ 1` por serialización JCS, sin convertir strings |
| F-C-06 | §6.2 especifica que `partition_manifest_sha256` usa tiempos declarados sin normalizar |
| F-C-07 | §4.4 distingue RFC 8785 de la política de enteros seguros §9.1 |
| F-C-08 | §8 transcribe vectores oficiales del Apéndice B y de §§3.2.2–3.2.4 |
| F-C-09 | §5 especifica formalmente `ALLOWLIST_V4` |

### 4.2 Timestamps: alcance de la exclusión de DEC-06 (F-C-01)

DEC-06 excluye **timestamps de auditoría/salida**: `created_at`, `sealed_at` y `validation.evaluation.evaluated_at` (además de identificadores de salida, artefactos, métricas y hashes derivados).

La allowlist normativa §9.2 **sí incluye límites temporales de datos**, que forman parte de la intención del run:

- `data.time_range.start` y `data.time_range.end`.
- `time_start` y `time_end` de cada partición.

Estos valores se normalizan antes de JCS en `run_fingerprint`. Esta lectura no altera la semántica normativa: DEC-06 remite expresamente a la allowlist de §9.2 para las rutas exactas.

### 4.3 Equivalencia `1.0 ≡ 1` (F-C-05)

La equivalencia exigida por DEC-09 y por el diseño v4 §5.3 se obtiene en la preimagen por la propia serialización JCS: `rfc8785` emite `1` para el float integral `1.0`. No se convierte el string `"1"` a número; los strings decimales permanecen strings conforme a §9.1. La validación semántica de duplicados entre `1` y `1.0` ya fue implementada en Fase B y no se modifica.

### 4.4 RFC 8785 frente a política de enteros seguros (F-C-07)

| Alcance | Regla |
|---|---|
| RFC 8785 | Los números JSON deben ser representables como IEEE 754 binary64 y serializarse según ECMAScript; NaN/Infinity terminan con error; I-JSON recomienda strings para precisiones superiores |
| Apéndice B nota (1) | Recomienda que los enteros "verdaderos" estén en `[-9007199254740991, 9007199254740991]` |
| Diseño v4 §9.1 | Hace obligatoria esa cota para todos los enteros del manifiesto |
| `rfc8785` 0.1.4 | Aplica `IntegerDomainError` en `±(2^53−1)`; es una implementación de la política de aplicación, no una definición nueva de RFC |

R2 mantiene ambas capas separadas.

---

## 5. Especificación formal de `ALLOWLIST_V4` (F-C-02, F-C-09)

### 5.1 Estructura de cada entrada `[PROPUESTA]`

```python
AllowlistEntry = {
    "path": str,            # ruta dotted; usa {partition} como plantilla
    "type": str,            # string | integer | number | boolean | array | object |
                            # timestamp | string_decimal
    "optional": bool,       # False = obligatoria en el manifiesto validado
    "nullable": bool,       # True = None explícito se conserva
    "condition": str,       # always | external_run_only
    "normalization": str,   # none | timestamp_utc_9
}
```

`ALLOWLIST_V4` es una tupla ordenada de `AllowlistEntry`. Las pruebas parametrizadas se generan iterando esta estructura; **no existe un número fijo de rutas escrito manualmente**. Las entradas con `{partition}` se expanden para `train`, `validation`, `calibration` y `test`; `shared_with` se incluye solo cuando aparece, y es obligatoria en `calibration` por el schema.

### 5.2 Entradas incluidas

| Ruta | type | optional | nullable | condition | normalization |
|---|---|---|---|---|---|
| `schema_version` | string | False | False | always | none |
| `git.source_bundle_sha256` | string | False | False | always | none |
| `producer.name` | string | False | False | always | none |
| `producer.version` | string | False | False | always | none |
| `producer.python` | string | False | False | always | none |
| `producer.config_sha256` | string | False | False | always | none |
| `data.symbol` | string | False | False | always | none |
| `data.timeframe` | string | False | False | always | none |
| `data.provider` | string | False | False | always | none |
| `data.provider_version` | string | False | False | always | none |
| `data.dataset_sha256` | string | False | False | always | none |
| `data.raw_rows` | integer | False | False | always | none |
| `data.feature_rows` | integer | False | False | always | none |
| `data.labeled_rows` | integer | False | False | always | none |
| `data.time_range.start` | timestamp | False | False | always | timestamp_utc_9 |
| `data.time_range.end` | timestamp | False | False | always | timestamp_utc_9 |
| `data.time_range.timezone` | string | False | False | always | none |
| `data.missing_data_policy` | string | False | False | always | none |
| `data.gap_policy` | string | False | False | always | none |
| `data.ohlcv_schema_version` | string | False | False | always | none |
| `data.alignment` | string | False | False | always | none |
| `target.name` | string | False | False | always | none |
| `target.horizon_bars` | integer | False | False | always | none |
| `target.vol_mult` | string_decimal | False | False | always | none |
| `target.classes` | array | False | False | always | none |
| `target.class_order` | array | False | False | always | none |
| `target.rule_sha256` | string | False | False | always | none |
| `target.nan_policy` | string | False | False | always | none |
| `features.ordered` | array | False | False | always | none |
| `features.count` | integer | False | False | always | none |
| `features.definition_sha256` | string | False | False | always | none |
| `features.matrix_sha256` | string | False | False | always | none |
| `features.pipeline_version` | string | False | False | always | none |
| `features.code_sha256` | string | False | False | always | none |
| `features.parameters.lookback_max` | integer | True | False | always | none |
| `features.parameters.lookback_min` | integer | True | False | always | none |
| `features.parameters.lookback_step` | integer | True | False | always | none |
| `features.parameters.lookback_total` | integer | True | False | always | none |
| `features.nan_policy` | string | False | False | always | none |
| `training.task` | string | False | False | always | none |
| `training.models.rf.library` | string | False | False | always | none |
| `training.models.rf.version` | string | False | False | always | none |
| `training.models.rf.params.n_estimators` | integer | True | False | always | none |
| `training.models.rf.params.max_depth` | integer | True | True | always | none |
| `training.models.rf.params.class_weight` | string | True | True | always | none |
| `training.models.rf.params.random_state` | integer | True | True | always | none |
| `training.models.rf.params.n_jobs` | integer | True | False | always | none |
| `training.models.xgb.library` | string | False | False | always | none |
| `training.models.xgb.version` | string | False | False | always | none |
| `training.models.xgb.params.n_estimators` | integer | True | False | always | none |
| `training.models.xgb.params.max_depth` | integer | True | False | always | none |
| `training.models.xgb.params.learning_rate` | number | True | False | always | none |
| `training.models.xgb.params.subsample` | number | True | False | always | none |
| `training.models.xgb.params.colsample_bytree` | number | True | False | always | none |
| `training.models.xgb.params.random_state` | integer | True | False | always | none |
| `training.models.xgb.params.tree_method` | string | True | False | always | none |
| `training.models.xgb.params.device` | string | True | False | always | none |
| `training.models.xgb.params.objective` | string | True | False | always | none |
| `training.models.xgb.params.num_class` | integer | True | False | always | none |
| `training.models.xgb.params.eval_metric` | string | True | False | always | none |
| `training.models.xgb.params.n_jobs` | integer | True | False | always | none |
| `training.ensemble.method` | string | False | False | always | none |
| `training.ensemble.weights.rf` | string_decimal | True | False | always | none |
| `training.ensemble.weights.xgb` | string_decimal | True | False | always | none |
| `training.seed` | integer | False | False | always | none |
| `training.environment.python` | string | False | False | always | none |
| `training.environment.numpy` | string | False | False | always | none |
| `training.environment.pandas` | string | False | False | always | none |
| `training.environment.scikit_learn` | string | False | False | always | none |
| `training.environment.xgboost` | string | False | False | always | none |
| `training.environment.joblib` | string | False | False | always | none |
| `training.environment.os` | string | False | False | always | none |
| `training.environment.arch` | string | False | False | always | none |
| `training.environment.cuda_version` | string | True | True | always | none |
| `training.environment.cudnn_version` | string | True | True | always | none |
| `training.hardware.device` | string | False | False | always | none |
| `training.hardware.gpu_model` | string | False | True | always | none |
| `training.hardware.cuda_version` | string | False | True | always | none |
| `training.hardware.cpu_count` | integer | False | False | always | none |
| `training.hardware.ram_gb` | integer | False | False | always | none |
| `training.determinism.bitwise_reproducible` | boolean | False | False | always | none |
| `training.determinism.n_jobs` | integer | False | False | always | none |
| `training.determinism.omp_num_threads` | integer | False | False | always | none |
| `training.determinism.xgb_tree_method` | string | False | False | always | none |
| `training.determinism.xgb_deterministic_histogram` | boolean | False | False | always | none |
| `training.determinism.gpu_deterministic` | boolean | False | False | always | none |
| `validation.split_method` | string | False | False | always | none |
| `validation.partitions.{partition}.row_start` | integer | False | False | always | none |
| `validation.partitions.{partition}.row_end` | integer | False | False | always | none |
| `validation.partitions.{partition}.source_position_start` | integer | False | False | always | none |
| `validation.partitions.{partition}.source_position_end` | integer | False | False | always | none |
| `validation.partitions.{partition}.n_rows` | integer | False | False | always | none |
| `validation.partitions.{partition}.time_start` | timestamp | False | False | always | timestamp_utc_9 |
| `validation.partitions.{partition}.time_end` | timestamp | False | False | always | timestamp_utc_9 |
| `validation.partitions.{partition}.class_counts` | array | False | False | always | none |
| `validation.partitions.{partition}.index_sha256` | string | False | False | always | none |
| `validation.partitions.{partition}.shared_with` | string | True | False | always | none |
| `validation.purge.rows_between_partitions` | integer | False | False | always | none |
| `validation.purge.label_horizon_bars` | integer | False | False | always | none |
| `validation.purge.embargo_rows` | integer | False | False | always | none |
| `calibration.mode` | string | False | False | always | none |
| `calibration.method` | string | False | False | always | none |
| `calibration.fit_partition` | string | False | False | always | none |
| `calibration.classes` | array | False | False | always | none |
| `calibration.class_order` | array | False | False | always | none |
| `calibration.n_calibrators` | integer | False | False | always | none |
| `calibration.base_model_id` | string | True | False | external_run_only | none |
| `calibration.base_artifact_sha256.rf` | string | True | False | external_run_only | none |
| `calibration.base_artifact_sha256.xgb` | string | True | False | external_run_only | none |

### 5.3 Exclusiones normativas

| Rutas | Motivo |
|---|---|
| `model_id`, `created_at`, `sealed_at`, `status_at_seal`, `run_fingerprint` | Identidad de salida, timestamps de auditoría o resultado del propio cálculo |
| `git.commit`, `git.dirty`, `git.branch`, `git.tag` | Localizador/meta; `dirty=false` es condición de admisión |
| `producer.command` | Texto de invocación no normalizado |
| `data.snapshot_uri` | Ubicación, no contenido |
| `validation.purge.label_purge_satisfied`, `validation.leakage_checks.*` | Resultados derivados |
| `validation.partition_manifest_sha256` | Digest derivado |
| `validation.evaluation.*` | Protocolo/resultado de evaluación |
| `calibration.calibration_input_sha256`, `calibration.artifact_sha256` | Digests de entradas/artefactos |
| `artifacts[]`, `metrics.*`, `extensions` | Outputs, resultados evaluativos, extensiones vacías |

La proyección se construye **recorriendo estas entradas**, no filtrando el manifiesto. Ninguna exclusión se copia como clave con valor `None`.

---

## 6. Definiciones de fingerprints dentro del alcance

### 6.1 `run_fingerprint` `[PROPUESTA]`

```python
def build_run_fingerprint(manifest: dict[str, Any]) -> str: ...
```

1. `projection = project_allowlist(manifest)` usando §5.
2. `payload = rfc8785.dumps(projection)` (sin LF).
3. `digest = hashlib.sha256(payload).hexdigest()` (64 hex minúsculas).
4. El manifiesto no se modifica; `run_fingerprint` no se incluye en la preimagen.
5. Conforme a Q-01, **no se añade error de comparación** en `validate_manifest_v4`.

### 6.2 `partition_manifest_sha256` `[PROPUESTA]`

```python
def build_partition_manifest_sha256(manifest: dict[str, Any]) -> str: ...
```

Preimagen:

```text
{
  "train": <objeto completo de validation.partitions.train>,
  "validation": <objeto completo ...>,
  "calibration": <objeto completo ...>,
  "test": <objeto completo ...>
}
```

(F-C-06) Se copian los objetos de partición **tal como figuran en el manifiesto**, incluidos `time_start`/`time_end` declarados, `index_sha256` y `shared_with` cuando corresponda. No se aplica `normalize_timestamp` aquí: esa normalización pertenece a `run_fingerprint`. Solo si una norma futura lo indicara se cambiaría esta regla con cambio de contrato explícito.

### 6.3 Fuera del alcance de C (Q-02)

| Constructor | Fase responsable | Estado en R2 |
|---|---|---|
| `build_index_sha256(rows)` | D | Solo referencia; requiere secuencia explícita y reglas de partición |
| `build_calibration_input_sha256(inputs)` | D | Solo referencia; requiere `f64be` y entradas efectivas |
| `build_event_sha256(payload)` | E | Solo referencia; payload de nueve campos sin `event_sha256` |

R2 no desarrolla sus interfaces completas ni los incluye en CP-C de Fase C.

### 6.4 Bytes, LF y representación

- Para todos los digests de provenance: `SHA-256(JCS UTF-8 sin BOM ni LF)`.
- `manifest.sha256` (fuera de C): bytes JCS + exactamente un LF.
- Digest final: hexadecimal minúsculo de 64 caracteres.
- Ninguna preimagen contiene el digest que produce.

---

## 7. Contrato de normalización UTC (Q-03) `[PROPUESTA]`

```python
def normalize_timestamp(value: str) -> str: ...
```

| Aspecto | Regla |
|---|---|
| Entrada | String RFC 3339 con `Z` o desplazamiento numérico `±HH:MM` |
| Rechazo | Zona ausente, `-00:00`, segundo `60`, más de 9 dígitos fraccionarios, fecha/offset inválidos, desbordamiento de rango |
| Validación | Calendario (`datetime`) y offset `HH <= 23`, `MM <= 59` |
| Precisión | Fracción conservada como entero de nanosegundos; sin truncamiento ni redondeo |
| Conversión | Ajuste de UTC por aritmética entera de segundos de offset; la fracción se mantiene separada |
| Formato canónico | `YYYY-MM-DDTHH:MM:SS.fffffffffZ` con exactamente 9 dígitos, rellenados a la derecha con ceros |
| Salida | String; determinista; apto para JCS |
| Reutilización | Fase D debe usar este mismo helper en lugar de definir otro |

Python `datetime` solo ofrece microsegundos; por ello la fracción de nanosegundos se maneja como entero separado y se formatea al final.

---

## 8. Vectores RFC 8785 completos y verificables (F-C-04, F-C-08)

**Procedencia:** RFC 8785, June 2020, §3.2.2, §3.2.3 y Appendix B Table 1. Consultado en `https://www.rfc-editor.org/rfc/rfc8785.txt` el 2026-11-27. Los valores se transcriben de esa fuente, no se reconstruyen de memoria.

### 8.1 Objeto canónico del §3.2.2 / §3.2.3

Entrada:

```json
{
  "numbers": [333333333.33333329, 1E30, 4.50, 2e-3, 0.000000000000000000000000001],
  "string": "\u20ac$\u000F\u000aA'\u0042\u0022\u005c\\\"\/",
  "literals": [null, true, false]
}
```

Salida canónica exacta (una línea; el salto del RFC es solo de presentación):

```text
{"literals":[null,true,false],"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],"string":"€$\u000f\nA'B\"\\\\\"/"}
```

Bytes UTF-8 en hexadecimal, según §3.2.4:

```text
7b 22 6c 69 74 65 72 61 6c 73 22 3a 5b 6e 75 6c 6c 2c 74 72
75 65 2c 66 61 6c 73 65 5d 2c 22 6e 75 6d 62 65 72 73 22 3a
5b 33 33 33 33 33 33 33 33 33 2e 33 33 33 33 33 33 33 2c 31
65 2b 33 30 2c 34 2e 35 2c 30 2e 30 30 32 2c 31 65 2d 32 37
5d 2c 22 73 74 72 69 6e 67 22 3a 22 e2 82 ac 24 5c 75 30 30
30 66 5c 6e 41 27 42 5c 22 5c 5c 5c 5c 5c 22 2f 22 7d
```

### 8.2 Orden de propiedades del §3.2.3

Datos de prueba con claves `\u20ac`, `\r`, `\ufb33`, `1`, emoji, `\u0080`, `\u00f6`. Orden esperado de argumentos tras ordenar:

```text
"Carriage Return"
"One"
"Control"
"Latin Small Letter O With Diaeresis"
"Euro Sign"
"Emoji: Grinning Face"
"Hebrew Letter Dalet With Dagesh"
```

### 8.3 Appendix B Table 1 — muestras de serialización numérica

| IEEE 754 | JSON Representation | Comentario |
|---|---|---|
| `0000000000000000` | `0` | Zero |
| `8000000000000000` | `0` | Minus zero |
| `0000000000000001` | `5e-324` | Min pos number |
| `8000000000000001` | `-5e-324` | Min neg number |
| `7fefffffffffffff` | `1.7976931348623157e+308` | Max pos number |
| `ffefffffffffffff` | `-1.7976931348623157e+308` | Max neg number |
| `4340000000000000` | `9007199254740992` | Max pos int (1) |
| `c340000000000000` | `-9007199254740992` | Max neg int (1) |
| `4430000000000000` | `295147905179352830000` | ~2**68 (2) |
| `7fffffffffffffff` | *(sin representación; error)* | NaN (3) |
| `7ff0000000000000` | *(sin representación; error)* | Infinity (3) |
| `44b52d02c7e14af5` | `9.999999999999997e+22` | |
| `44b52d02c7e14af6` | `1e+23` | |
| `44b52d02c7e14af7` | `1.0000000000000001e+23` | |
| `444b1ae4d6e2ef4e` | `999999999999999700000` | |
| `444b1ae4d6e2ef4f` | `999999999999999900000` | |
| `444b1ae4d6e2ef50` | `1e+21` | |
| `3eb0c6f7a0b5ed8c` | `9.999999999999997e-7` | |
| `3eb0c6f7a0b5ed8d` | `0.000001` | |
| `41b3de4355555553` | `333333333.3333332` | |
| `41b3de4355555554` | `333333333.33333325` | |
| `41b3de4355555555` | `333333333.3333333` | |
| `41b3de4355555556` | `333333333.3333334` | |
| `41b3de4355555557` | `333333333.33333343` | |
| `becbf647612f3696` | `-0.0000033333333333333333` | |
| `43143ff3c1cb0959` | `1424953923781206.2` | Round to even (4) |

Notas del RFC: (1) recomienda rango `-9007199254740991..9007199254740991` para enteros verdaderos; (2) JCS no considera precisión extendida; (3) valores fuera de rango no permitidos en JSON; (4) `1424953923781206.25` se redondea al par más cercano.

### 8.4 Vector reducido del diseño v4 §9.5 (F-C-04)

Entrada:

```json
{"calibration_intent":{"fit_partition":"validation","method":"sigmoid","mode":"in_pipeline"},"data":{"dataset_sha256":"b"},"features":{"ordered":["close","volume"]},"git":{"source_bundle_sha256":"a"},"schema_version":"3.0.0","target":{"horizon_bars":1},"training":{"seed":42},"validation_intent":{"split_method":"chronological_holdout"}}
```

SHA-256 esperado (completo):

```text
ed01f9cea45b644c561b6eb0346c7450b7836abb35f4ece1ede5b265e3722157
```

Este vector verifica JCS sobre un objeto reducido; **no es un vector dorado completo de `run_fingerprint`**, que sigue aplazado.

---

## 9. Matriz CP-C-01 a CP-C-18

Ningún criterio se marca PASS: no existe implementación de Fase C.

| ID | Criterio | Requisito | Prueba | Estado |
|---|---|---|---|---|
| CP-C-01 | JCS usa `rfc8785` 0.1.4, sin `repr`/`json.dumps` propios | C1/Q-05 | C-T01…T08, verificación de dependencia | Definido, pendiente |
| CP-C-02 | Vectores oficiales RFC 8785 reproducidos | C1/F-C-08 | §8.1–8.3 | Definido, pendiente |
| CP-C-03 | `-0`, límites y NaN/Inf correctos | C1/F-C-07 | §8.3 | Definido, pendiente |
| CP-C-04 | Orden UTF-16 y escapes correctos | C1 | §8.1–8.2 | Definido, pendiente |
| CP-C-05 | Proyección contiene exactamente `ALLOWLIST_V4` | C2/F-C-09 | §5 + pruebas generadas de la estructura | Definido, pendiente |
| CP-C-06 | Campos excluidos no alteran el fingerprint | C2/DEC-06 | Pruebas parametrizadas de exclusiones §5.3 | Definido, pendiente |
| CP-C-07 | Ausencia vs `null` distinguidos | C2 | Pruebas por entrada `nullable` | Definido, pendiente |
| CP-C-08 | Condición `base_*` aplicada solo en `external_run_only` | C2 | Pruebas por `condition` | Definido, pendiente |
| CP-C-09 | `build_run_fingerprint` reproducible y determinista | C3/V4-U10 | Pruebas de mutación y repetición | Definido, pendiente |
| CP-C-10 | Constructor de `run_fingerprint` implementado **sin comparación de admisión** | Q-01 | Prueba de que `validate_manifest_v4` no añade error de comparación | Reformulado, pendiente |
| CP-C-11 | `partition_manifest_sha256` recalculable desde preimagen declarada | Q-02/F-C-06 | Prueba con particiones completas | Reformulado, pendiente |
| CP-C-12 | Ninguna preimagen contiene su digest | §9.4 | Prueba de allowlist sin `run_fingerprint` | Definido, pendiente |
| CP-C-13 | Errores deterministas y tipados | C4 | Pruebas de timestamps y JCS inválido | Definido, pendiente |
| CP-C-14 | No mutación del manifiesto | C4 | `deepcopy` antes/después | Definido, pendiente |
| CP-C-15 | v3 idéntico | C5 | `provenance.py` sin diff; suites v3 | Definido, pendiente |
| CP-C-16 | Sin fallback entre versiones | C5/DEC-05 | Dispatch tests | Definido, pendiente |
| CP-C-17 | Regresiones documentadas | C6 | Ver §9.1 | Precisado, pendiente |
| CP-C-18 | C no incluye constructores de D/E ni capacidades de Fases D–F | Q-02 | Revisión de diff y pruebas | Reformulado, pendiente |

### 9.1 CP-C-17 — suites enumeradas

Conteos documentados en el estado actual; **no reejecutados en R2**:

| Suite | Conteo documentado |
|---|---|
| `tests/test_provenance_v4_schema.py` | 37 pruebas |
| `tests/test_provenance_v4_dispatch.py` | 29 pruebas |
| `tests/test_provenance.py` | 116 pruebas |
| Suite completa | 507 pruebas |
| `tests/test_provenance_v4_canonical.py` (nueva, propuesta) | Conteo no inventado; se fijará al crearla |

### 9.2 Criterios pendientes de decisiones futuras

| Criterio futuro | Dependencia |
|---|---|
| Comparación de `run_fingerprint` durante admisión | Diseño y autorización posteriores a C (Q-01) |
| `index_sha256` y `calibration_input_sha256` | Fase D (Q-02) |
| `event_sha256` | Fase E (Q-02) |
| Cambio de dependencia a `rfc8785==0.1.4` | Autorización de dependencias (Q-05) |

---

## 10. Matriz de trazabilidad de hallazgos F-C-01 a F-C-09

| Hallazgo | Sección corregida en R2 | Criterio CP-C | Estado documental |
|---|---|---|---|
| F-C-01 | §4.2 | CP-C-05, CP-C-06 | Resuelto |
| F-C-02 | §5, §9 | CP-C-05 | Resuelto |
| F-C-03 | §9, §9.2 | CP-C-10, CP-C-11, CP-C-18 | Resuelto |
| F-C-04 | §8.4 | CP-C-02 | Resuelto |
| F-C-05 | §4.3 | CP-C-09 | Resuelto |
| F-C-06 | §6.2 | CP-C-11 | Resuelto |
| F-C-07 | §4.4 | CP-C-02, CP-C-03 | Resuelto |
| F-C-08 | §8.1–8.3 | CP-C-02 | Resuelto |
| F-C-09 | §5.1–5.3 | CP-C-05, CP-C-07, CP-C-08 | Resuelto |

"Resuelto" significa corrección documental; **no** implica implementación ni aceptación de CP-C.

---

## 11. Riesgos residuales y decisiones futuras

| Riesgo / decisión | Estado | Acción futura |
|---|---|---|
| Admisión de `run_fingerprint` divergente | Fuera de C por Q-01 | Diseño posterior si se decide comparar |
| Constructores D/E | Asignados por Q-02 | Diseñar en Fase D/E con sus propias CP |
| Cambio de `>=0.1.4` a `==0.1.4` | Decidido pero no aplicado | Tarea de dependencias con autorización |
| Actualización futura de `rfc8785` | Riesgo | Revalidar §8 y CP-C-02 antes de actualizar |
| Deriva de `ALLOWLIST_V4` | Riesgo | Tabla versionada; pruebas derivadas de la estructura |
| Confusión LF / sin LF | Riesgo | Pruebas separadas en implementación futura |

---

## 12. Límites explícitos de Fase C y dependencias con D/E

- Fase C produce, como máximo: `_jcs_bytes_v4`, `normalize_timestamp`, `project_allowlist`, `build_run_fingerprint`, `build_partition_manifest_sha256` y errores tipados asociados.
- No implementa comparación de admisión (Q-01).
- No implementa `index_sha256` ni `calibration_input_sha256` (Fase D).
- No implementa `event_sha256` (Fase E).
- No implementa purga, particiones efectivas, calibration equivalente, cadenas, sidecars, Ed25519, loaders, registry, writer ni inferencia.
- Depende de Fase A (dispatch) y Fase B (schema y validadores), ambas cerradas.
- Fase D reutilizará `normalize_timestamp` (Q-03) y diseñará sus propios constructores.
- Fase E reutilizará el primitive JCS para `event_sha256`.

---

## 13. Conclusión

R2 incorpora las cuatro decisiones del propietario y corrige documentalmente los nueve hallazgos de la auditoría R1. No modifica R1, no implementa código, no ejecuta pruebas, no cambia dependencias ni toca datos.

**Fase C continúa BLOCKED**, pendiente de auditoría independiente R2, aprobación expresa del diseño y autorización técnica separada para implementar. Esta aprobación no autorizaría Fase D, E, F, G ni S2.

**Fin de R13-PHASE-C-DESIGN-R2.**
