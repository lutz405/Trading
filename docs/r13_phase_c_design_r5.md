# R13-PHASE-C-DESIGN-R5 — Diseño técnico de Fase C (corrección de hallazgos AUD-R4)

**Estado del documento:** propuesta de diseño R5, preparada para auditoría independiente. No implementa Fase C, no declara Fase C aprobada y no autoriza su implementación.
**Fecha:** 2026-11-27.
**Base:** commit `259ca6ee11878f114cdcab4cef500074b3bc1a48` (`main`, `origin/main` alineados).
**Predecesores:** `docs/r13_phase_c_design_r1.md`, `docs/r13_phase_c_design_r2.md`, `docs/r13_phase_c_design_r3.md` y `docs/r13_phase_c_design_r4.md`, conservados sin modificaciones.
**Auditorías incorporadas:** `R13-AUDIT-PHASE-C-DESIGN-R1` (F-C-01…F-C-09), `R13-AUDIT-PHASE-C-DESIGN-R2` (AUD-R2-01…AUD-R2-04), `R13-AUDIT-PHASE-C-DESIGN-R3` (AUD-R3-01…AUD-R3-02) y `R13-AUDIT-PHASE-C-DESIGN-R4` (AUD-R4-01…AUD-R4-07).
**Fase C:** **BLOCKED** hasta auditoría independiente R5, aprobación expresa del propietario y autorización técnica separada.

---

## 1. Identificación y alcance de R5

R5 es un documento completo y autónomo: no requiere combinar R1, R2, R3 ni R4 para entender el diseño. Corrige los siete hallazgos de la auditoría R4:

- **AUD-R4-01 (MEDIUM):** §5.6 incorpora un algoritmo ordenado con una rama explícita para `projection_include_when` falso.
- **AUD-R4-02 (LOW):** I6 se reformula como implicación bidireccional y se añade `ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED`.
- **AUD-R4-03 (MEDIUM):** §5.8 amplía el oracle a metadatos y condiciones normativas, con transcripción independiente, versión y checksum.
- **AUD-R4-04 (LOW):** §5.8 documenta la derivación de `manifest_required_when`/`manifest_allowed_when` desde los `$defs` del schema.
- **AUD-R4-05 (LOW):** §9 y §9.1 corrigen la cobertura de CP-C-05 y CP-C-13.
- **AUD-R4-06 (LOW):** I9 referencia correctamente el vocabulario de condiciones de §5.3.
- **AUD-R4-07 (INFO):** §6.3 reconcilia Q-02 con V4-U11.

Conserva íntegramente las decisiones y correcciones anteriores:

- **F-C-01…F-C-09:** timestamp/DEC-06, parametrización derivada, CP-C, vector completo, `1.0 ≡ 1`, partición sin normalizar, RFC vs política, vectores oficiales y estructura formal.
- **AUD-R2-01…AUD-R2-04:** separación de obligatoriedad/proyección, `shared_with` por partición, semántica de tipos y conteos parametrizados.
- **AUD-R3-01…AUD-R3-02:** invariantes I1…I12, códigos `ALLOWLIST_*` y fuente normativa única.

No se autoriza implementación. El alcance futuro autorizable sigue siendo: `src/tradingai/ml/provenance_v4.py` y pruebas nuevas de Fase C. No se modificarán `provenance.py`, `manifest_v3.json`, `manifest_v4.json`, dependencias, modelos ni datasets.

R5 no añade rutas a la allowlist: la tabla §5.4 se conserva idéntica a R3/R4 (139 rutas tras expandir `{partition}`). Solo se precisan el algoritmo de preimagen, las invariantes, el oracle normativo y la cobertura de criterios.

---

## 2. Referencias normativas y documentales

| Documento | Uso |
|---|---|
| `docs/aud04b_model_provenance_v4_approval_r1.md` | DEC-03, DEC-05, DEC-06, DEC-09; estado `APPROVED` |
| `docs/aud04b_model_provenance_v4_implementation_plan_r1.md` | Plan R1.2, Fase C, V4-U10/V4-U11, CP-C |
| `docs/aud04b_model_provenance_v4_design.md` | §§5.2, 5.3, 9.1, 9.2, 9.4, 9.5 |
| `docs/r13_decision_resolution_r1.md` | Cierre V4-U06 / DEC-09 y límites de fases |
| `src/tradingai/schemas/manifest_v4.json` | Contrato real de obligatoriedad, nulabilidad y tipos |
| RFC 8785 (June 2020), `https://www.rfc-editor.org/rfc/rfc8785.txt` | Reglas y vectores JCS; consultado el 2026-11-27 |
| `docs/r13_phase_c_design_r3.md` | Diseño conservado; allowlist normativa de referencia |
| `docs/r13_phase_c_design_r4.md` | Diseño inmediatamente anterior, conservado |
| `R13-AUDIT-PHASE-C-DESIGN-R3` | Hallazgos AUD-R3-01 y AUD-R3-02 (entregado en la conversación; no publicado como archivo) |
| `R13-AUDIT-PHASE-C-DESIGN-R4` | Hallazgos AUD-R4-01 a AUD-R4-07 (entregado en la conversación; no publicado como archivo) |
| Código actual | `provenance.py`, `provenance_v4.py`, pruebas v3/v4, `pyproject.toml` |

---

## 3. Decisiones aprobadas por el propietario

### 3.1 Q-01 — Comparación de `run_fingerprint`

Fase C implementará el constructor determinista de `run_fingerprint`, pero **no integrará** su comparación con el valor declarado en la admisión de `validate_manifest_v4`. Dicha comparación requiere diseño y autorización posteriores.

### 3.2 Q-02 — Alcance de constructores

| Fase | Constructores asignados |
|---|---|
| C | `run_fingerprint`, `partition_manifest_sha256` |
| D | `index_sha256`, `calibration_input_sha256` |
| E | `event_sha256` |

No hay solapamientos. R5 no desarrolla los constructores de D/E.

### 3.3 Q-03 — Normalización UTC

Fase C define un único helper común de normalización UTC, reutilizable por Fase D. Contrato en §7. No se implementa en esta tarea documental. R5 conserva este extremo sin cambios.

### 3.4 Q-05 — Dependencia `rfc8785`

Decisión de diseño: fijar `rfc8785==0.1.4`. `pyproject.toml` actualmente declara `rfc8785>=0.1.4`; **no se modifica en R5**. Toda actualización futura exige revalidar los vectores de §8 y nueva auditoría.

---

## 4. Diseño técnico general

### 4.1 Canonicalización JCS `[PROPUESTA]`

```python
def _jcs_bytes_v4(obj: Any) -> bytes: ...
```

- Única primitiva: `rfc8785.dumps(obj)`.
- Sin `repr()`, `json.dumps()`, `sort_keys=True` ni serializadores alternativos.
- Bytes UTF-8 sin BOM ni LF final.
- Orden de propiedades por UTF-16BE; arrays en orden original; separadores sin espacios.
- NaN/Infinity → `FloatDomainError`; enteros fuera de rango → `IntegerDomainError`; ambos convertidos a errores tipados internos.
- No se modifica la implementación v3.

### 4.2 RFC 8785 frente a política de enteros seguros

| Alcance | Regla |
|---|---|
| RFC 8785 | Números como IEEE 754 binary64; serialización ECMAScript; NaN/Infinity inválidos |
| Apéndice B nota (1) | Recomienda rango `[-9007199254740991, 9007199254740991]` para enteros verdaderos |
| Diseño v4 §9.1 | Hace obligatoria esa cota para todos los enteros del manifiesto |
| `rfc8785` 0.1.4 | Aplica `IntegerDomainError`; implementa la política de aplicación, no una definición nueva del RFC |

### 4.3 Timestamps en DEC-06

DEC-06 excluye timestamps de auditoría/salida: `created_at`, `sealed_at` y `validation.evaluation.evaluated_at`. La allowlist §9.2 incluye límites temporales de datos (`data.time_range.start/end` y `time_start/time_end` de particiones), que se normalizan en `run_fingerprint`.

### 4.4 Equivalencia `1.0 ≡ 1`

Se obtiene por la serialización JCS (`rfc8785` emite `1` para `1.0`). Los strings decimales permanecen strings; no se convierten. La validación de duplicados implementada en Fase B no se modifica.

---

## 5. Especificación formal de `ALLOWLIST_V4`

### 5.1 Estructura de una entrada `[PROPUESTA]`

```python
AllowlistEntry = {
    "path": str,                       # ruta dotted; {partition} es plantilla
    "type": str,                       # semántica definida en §5.2
    "manifest_required": bool,         # obligatoria en el manifiesto validado
    "manifest_required_when": str | None,
    "manifest_allowed_when": str | None,
    "projection_include_when": str,    # always | external_run_only
    "projection_optional": bool,       # ausencia permitida en la preimagen
    "nullable": bool,                  # None explícito se conserva
    "normalization": str,              # none | timestamp_utc_9
}
```

**Semántica precisa:**

| Propiedad | Significado |
|---|---|
| `manifest_required=True` | El JSON Schema declara la ruta obligatoria sin condición |
| `manifest_required_when` | Condición bajo la cual la ruta es obligatoria; `None` si no aplica. Si la condición es falsa, la ruta puede estar ausente o prohibida según `manifest_allowed_when` |
| `manifest_allowed_when` | Condición bajo la cual la ruta puede aparecer; `None` = permitida siempre que el schema la declare. Si es falsa, la ruta está prohibida por el schema |
| `projection_include_when` | Condición de inclusión en la preimagen: `always` (si aparece) o `external_run_only` |
| `projection_optional=True` | Si la ruta no aparece en el manifiesto o la condición de inclusión es falsa, la clave se omite; no se inventa `None` |
| `projection_optional=False` | La ausencia sería una violación de contrato; no ocurre para entradas válidas |
| `nullable=True` | El schema permite `None` explícito y se preserva |
| `normalization=timestamp_utc_9` | Aplicar `normalize_timestamp` (§7) antes de JCS |

**Reglas de separación (AUD-R2-01):**

- La obligatoriedad en el manifiesto y la inclusión en la preimagen son dimensiones independientes.
- Un campo puede ser `manifest_required=True` y quedar excluido del fingerprint por condición (caso `base_*` con `in_pipeline`).
- Un campo puede ser opcional en el manifiesto y, si aparece, incluirse en la preimagen.
- Ninguna exclusión de la preimagen se interpreta como permiso para ausentar un campo obligatorio del manifiesto.

### 5.2 Semántica de tipos (AUD-R2-03)

| `type` | Semántica |
|---|---|
| `string` | String JSON; se copia textualmente; JCS aplica escapes UTF-8 |
| `integer` | Entero JSON finito; `abs(n) <= 2^53−1`; JCS emite forma decimal entera; sin coerción desde string |
| `number` | Número JSON finito; JCS aplica serialización ECMAScript; sin coerción desde string |
| `boolean` | `true`/`false` JSON; nunca aceptado como entero |
| `array` | Array JSON; orden conservado; elementos validados por el schema |
| `object` | Objeto JSON; JCS ordena claves recursivamente |
| `timestamp` | String temporal validada por `format: date-time` y normalizada por §7; se emite como string canónico UTC de 9 dígitos; no es número ni string arbitraria |
| `string_decimal` | String que representa un decimal (p. ej. `target.vol_mult`, pesos); se conserva exactamente, sin conversión ni normalización numérica |

### 5.3 Vocabulario de condiciones

| Condición | Definición |
|---|---|
| `always` | Sin condición adicional; incluir si la ruta está presente |
| `external_run_only` | Incluir solo si `calibration.mode == "external_run"` |
| `partition == 'calibration'` | Cierta cuando la variable `{partition}` de la plantilla vale `calibration` |

### 5.4 Entradas incluidas

Leyenda abreviada: `MR` = `manifest_required`; `MRW` = `manifest_required_when`; `MAW` = `manifest_allowed_when`; `PIW` = `projection_include_when`; `PO` = `projection_optional`; `N` = `nullable`; `Norm` = `normalization`.

| Ruta | type | MR | MRW | MAW | PIW | PO | N | Norm |
|---|---|---|---|---|---|---|---|---|
| `schema_version` | string | Sí | — | — | always | No | No | none |
| `git.source_bundle_sha256` | string | Sí | — | — | always | No | No | none |
| `producer.name` | string | Sí | — | — | always | No | No | none |
| `producer.version` | string | Sí | — | — | always | No | No | none |
| `producer.python` | string | Sí | — | — | always | No | No | none |
| `producer.config_sha256` | string | Sí | — | — | always | No | No | none |
| `data.symbol` | string | Sí | — | — | always | No | No | none |
| `data.timeframe` | string | Sí | — | — | always | No | No | none |
| `data.provider` | string | Sí | — | — | always | No | No | none |
| `data.provider_version` | string | Sí | — | — | always | No | No | none |
| `data.dataset_sha256` | string | Sí | — | — | always | No | No | none |
| `data.raw_rows` | integer | Sí | — | — | always | No | No | none |
| `data.feature_rows` | integer | Sí | — | — | always | No | No | none |
| `data.labeled_rows` | integer | Sí | — | — | always | No | No | none |
| `data.time_range.start` | timestamp | Sí | — | — | always | No | No | timestamp_utc_9 |
| `data.time_range.end` | timestamp | Sí | — | — | always | No | No | timestamp_utc_9 |
| `data.time_range.timezone` | string | Sí | — | — | always | No | No | none |
| `data.missing_data_policy` | string | Sí | — | — | always | No | No | none |
| `data.gap_policy` | string | Sí | — | — | always | No | No | none |
| `data.ohlcv_schema_version` | string | Sí | — | — | always | No | No | none |
| `data.alignment` | string | Sí | — | — | always | No | No | none |
| `target.name` | string | Sí | — | — | always | No | No | none |
| `target.horizon_bars` | integer | Sí | — | — | always | No | No | none |
| `target.vol_mult` | string_decimal | Sí | — | — | always | No | No | none |
| `target.classes` | array | Sí | — | — | always | No | No | none |
| `target.class_order` | array | Sí | — | — | always | No | No | none |
| `target.rule_sha256` | string | Sí | — | — | always | No | No | none |
| `target.nan_policy` | string | Sí | — | — | always | No | No | none |
| `features.ordered` | array | Sí | — | — | always | No | No | none |
| `features.count` | integer | Sí | — | — | always | No | No | none |
| `features.definition_sha256` | string | Sí | — | — | always | No | No | none |
| `features.matrix_sha256` | string | Sí | — | — | always | No | No | none |
| `features.pipeline_version` | string | Sí | — | — | always | No | No | none |
| `features.code_sha256` | string | Sí | — | — | always | No | No | none |
| `features.parameters.lookback_max` | integer | No | — | — | always | Sí | No | none |
| `features.parameters.lookback_min` | integer | No | — | — | always | Sí | No | none |
| `features.parameters.lookback_step` | integer | No | — | — | always | Sí | No | none |
| `features.parameters.lookback_total` | integer | No | — | — | always | Sí | No | none |
| `features.nan_policy` | string | Sí | — | — | always | No | No | none |
| `training.task` | string | Sí | — | — | always | No | No | none |
| `training.models.rf.library` | string | Sí | — | — | always | No | No | none |
| `training.models.rf.version` | string | Sí | — | — | always | No | No | none |
| `training.models.rf.params.n_estimators` | integer | No | — | — | always | Sí | No | none |
| `training.models.rf.params.max_depth` | integer | No | — | — | always | Sí | Sí | none |
| `training.models.rf.params.class_weight` | string | No | — | — | always | Sí | Sí | none |
| `training.models.rf.params.random_state` | integer | No | — | — | always | Sí | Sí | none |
| `training.models.rf.params.n_jobs` | integer | No | — | — | always | Sí | No | none |
| `training.models.xgb.library` | string | Sí | — | — | always | No | No | none |
| `training.models.xgb.version` | string | Sí | — | — | always | No | No | none |
| `training.models.xgb.params.n_estimators` | integer | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.max_depth` | integer | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.learning_rate` | number | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.subsample` | number | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.colsample_bytree` | number | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.random_state` | integer | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.tree_method` | string | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.device` | string | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.objective` | string | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.num_class` | integer | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.eval_metric` | string | No | — | — | always | Sí | No | none |
| `training.models.xgb.params.n_jobs` | integer | No | — | — | always | Sí | No | none |
| `training.ensemble.method` | string | Sí | — | — | always | No | No | none |
| `training.ensemble.weights.rf` | string_decimal | No | — | — | always | Sí | No | none |
| `training.ensemble.weights.xgb` | string_decimal | No | — | — | always | Sí | No | none |
| `training.seed` | integer | Sí | — | — | always | No | No | none |
| `training.environment.python` | string | Sí | — | — | always | No | No | none |
| `training.environment.numpy` | string | Sí | — | — | always | No | No | none |
| `training.environment.pandas` | string | Sí | — | — | always | No | No | none |
| `training.environment.scikit_learn` | string | Sí | — | — | always | No | No | none |
| `training.environment.xgboost` | string | Sí | — | — | always | No | No | none |
| `training.environment.joblib` | string | Sí | — | — | always | No | No | none |
| `training.environment.os` | string | Sí | — | — | always | No | No | none |
| `training.environment.arch` | string | Sí | — | — | always | No | No | none |
| `training.environment.cuda_version` | string | No | — | — | always | Sí | Sí | none |
| `training.environment.cudnn_version` | string | No | — | — | always | Sí | Sí | none |
| `training.hardware.device` | string | Sí | — | — | always | No | No | none |
| `training.hardware.gpu_model` | string | Sí | — | — | always | No | Sí | none |
| `training.hardware.cuda_version` | string | Sí | — | — | always | No | Sí | none |
| `training.hardware.cpu_count` | integer | Sí | — | — | always | No | No | none |
| `training.hardware.ram_gb` | integer | Sí | — | — | always | No | No | none |
| `training.determinism.bitwise_reproducible` | boolean | Sí | — | — | always | No | No | none |
| `training.determinism.n_jobs` | integer | Sí | — | — | always | No | No | none |
| `training.determinism.omp_num_threads` | integer | Sí | — | — | always | No | No | none |
| `training.determinism.xgb_tree_method` | string | Sí | — | — | always | No | No | none |
| `training.determinism.xgb_deterministic_histogram` | boolean | Sí | — | — | always | No | No | none |
| `training.determinism.gpu_deterministic` | boolean | Sí | — | — | always | No | No | none |
| `validation.split_method` | string | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.row_start` | integer | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.row_end` | integer | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.source_position_start` | integer | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.source_position_end` | integer | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.n_rows` | integer | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.time_start` | timestamp | Sí | — | — | always | No | No | timestamp_utc_9 |
| `validation.partitions.{partition}.time_end` | timestamp | Sí | — | — | always | No | No | timestamp_utc_9 |
| `validation.partitions.{partition}.class_counts` | array | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.index_sha256` | string | Sí | — | — | always | No | No | none |
| `validation.partitions.{partition}.shared_with` | string | No | `partition == 'calibration'` | `partition == 'calibration'` | always | Sí | No | none |
| `validation.purge.rows_between_partitions` | integer | Sí | — | — | always | No | No | none |
| `validation.purge.label_horizon_bars` | integer | Sí | — | — | always | No | No | none |
| `validation.purge.embargo_rows` | integer | Sí | — | — | always | No | No | none |
| `calibration.mode` | string | Sí | — | — | always | No | No | none |
| `calibration.method` | string | Sí | — | — | always | No | No | none |
| `calibration.fit_partition` | string | Sí | — | — | always | No | No | none |
| `calibration.classes` | array | Sí | — | — | always | No | No | none |
| `calibration.class_order` | array | Sí | — | — | always | No | No | none |
| `calibration.n_calibrators` | integer | Sí | — | — | always | No | No | none |
| `calibration.base_model_id` | string | Sí | — | — | external_run_only | Sí | No | none |
| `calibration.base_artifact_sha256.rf` | string | Sí | — | — | external_run_only | Sí | No | none |
| `calibration.base_artifact_sha256.xgb` | string | Sí | — | — | external_run_only | Sí | No | none |

**Nota AUD-R2-01 (caso `base_*`):** el schema declara `base_model_id` y `base_artifact_sha256` como obligatorios en ambos modos (`in_pipeline` y `external_run`). Por eso `manifest_required=Sí`. La exclusión de la preimagen con `in_pipeline` se expresa solo con `projection_include_when=external_run_only`; **no** autoriza ausencia en el manifiesto. La validación de binding implementada en Fase B permanece vigente.

**Nota AUD-R2-02 (caso `shared_with`):** `manifest_required_when` y `manifest_allowed_when` iguales a `partition == 'calibration'` reflejan exactamente el schema: `calibration_partition` lo exige; `partition` no lo declara y `additionalProperties:false` lo prohíbe en las otras tres particiones. Las pruebas parametrizadas derivan esta regla de la entrada, sin lista manual paralela.

### 5.5 Exclusiones normativas

| Rutas | Motivo |
|---|---|
| `model_id`, `created_at`, `sealed_at`, `status_at_seal`, `run_fingerprint` | Identidad de salida, timestamps de auditoría o resultado propio |
| `git.commit`, `git.dirty`, `git.branch`, `git.tag` | Localizador/meta; `dirty=false` es admisión |
| `producer.command` | Invocación no normalizada |
| `data.snapshot_uri` | Ubicación |
| `validation.purge.label_purge_satisfied`, `validation.leakage_checks.*` | Resultados derivados |
| `validation.partition_manifest_sha256` | Digest derivado |
| `validation.evaluation.*` | Protocolo/resultado de evaluación |
| `calibration.calibration_input_sha256`, `calibration.artifact_sha256` | Digests de entradas/salidas |
| `artifacts[]`, `metrics.*`, `extensions` | Outputs, resultados y extensiones vacías |

### 5.6 Construcción de la preimagen (orden normativo)

**Precondición:** el manifiesto ya pasó schema v4, enteros seguros, DEC-09 y validación de timestamps; la propia `ALLOWLIST_V4` ya pasó la validación interna de §5.7 y la comparación con el oracle de §5.8. Cualquier fallo previo impide calcular la preimagen.

El algoritmo se ejecuta **en este orden**. Cada decisión de admisión precede a la decisión de proyección; la proyección nunca modifica la admisión.

| Paso | Acción | Resultado |
|---|---|---|
| 1 | Validar `ALLOWLIST_V4` contra §5.7 (I1…I12 y códigos `ALLOWLIST_*`) y contra el oracle §5.8 | Fail-closed: `list[str]` determinista; sin preimagen |
| 2 | Recorrer las entradas de `ALLOWLIST_V4` en orden explícito, **no** recorrer el manifiesto | Conjunto de trabajo cerrado |
| 3 | Evaluar `manifest_required`, `manifest_required_when` y `manifest_allowed_when` en el contexto ya validado. Decidir si la ruta es obligatoria y si su presencia está permitida | Reglas de **admisión**; no afectan a la inclusión |
| 4 | Resolver la ruta en el manifiesto: `presente` o `ausente`. Si es obligatoria y está ausente, o si no está permitida y está presente, es error de contrato (no debería ocurrir tras la precondición) | Error determinista; sin síntesis de valores |
| 5 | Evaluar `projection_include_when`. Si es `always`, la ruta es candidata **si está presente**. Si es condicional y la condición es **verdadera**, la ruta es candidata **si está presente**. Si es condicional y la condición es **falsa**, la ruta se **excluye de la preimagen** | Exclusión aunque la ruta esté presente, aunque sea obligatoria en el manifiesto y con independencia de `projection_optional` |
| 6 | Si la ruta está **ausente** en el manifiesto y no fue excluida en el paso 5: con `projection_optional=True`, omitir sin inventar valor ni `None`; con `projection_optional=False`, error de contrato | Ausencia ≠ `null`; sin defaults |
| 7 | Si la ruta fue excluida en el paso 5, no aplicar el paso 6: la omisión es el comportamiento normativo previsto (caso `base_*` con `in_pipeline`). La exclusión **no** se interpreta como error ni como permiso para ausentar la ruta del manifiesto | Coherencia con `manifest_required=Sí` de `base_*` |
| 8 | Si la ruta es candidata: copiar el valor sin coerción; si `nullable=True` y el valor es `None`, copiar `None`; si `nullable=False`, `None` ya fue rechazado por el schema | Preservación exacta de tipos §5.2 |
| 9 | Si `normalization=timestamp_utc_9`, aplicar §7 **antes** de copiar; ninguna otra ruta se normaliza | String UTC canónico de 9 dígitos |
| 10 | No copiar exclusiones §5.5, digests derivados ni el propio `run_fingerprint`, ni como `None` | Sin circularidad |
| 11 | Construir el objeto resultante en orden explícito desde la allowlist; JCS ordena claves por UTF-16BE | El orden de inserción del manifiesto no afecta el digest |

**Precedencia y combinaciones inválidas:**

- El paso 5 **prevalece** sobre el paso 6: la exclusión por condición falsa se decide antes que la omisión por ausencia, pero ambas producen omisión sin inventar valores.
- `projection_include_when` condicional exige `projection_optional=True` (I6 reformulada); si no, se activa `ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED` en el paso 1 y no se llega al paso 5.
- Una condición fuera del vocabulario de §5.3, o usada fuera de su dominio, activa `ALLOWLIST_UNKNOWN_CONDITION`/`ALLOWLIST_CONDITION_CONTEXT` en el paso 1.
- `manifest_required`/`manifest_required_when`/`manifest_allowed_when` divergentes del schema activan `ALLOWLIST_SCHEMA_METADATA_DIVERGENCE` en el paso 1.
- La comparación con el oracle §5.8 es una verificación automática de la representación, ejecutada antes de construir la preimagen en el proceso de implementación; no introduce una segunda allowlist de producción ni sustituye a la validación interna §5.7.
- Ninguna rama del algoritmo puede convertir un campo obligatorio del manifiesto en opcional ni relajar la validación de admisión implementada en Fase A/B.

### 5.7 Invariantes formales de `AllowlistEntry` (AUD-R3-01)

**Dominios cerrados:**

| Propiedad | Dominio |
|---|---|
| `type` | `string` \| `integer` \| `number` \| `boolean` \| `array` \| `object` \| `timestamp` \| `string_decimal` |
| `manifest_required_when` | `None` \| `partition == 'calibration'` |
| `manifest_allowed_when` | `None` \| `partition == 'calibration'` |
| `projection_include_when` | `always` \| `external_run_only` |
| `projection_optional` | `True` \| `False` |
| `nullable` | `True` \| `False` |
| `normalization` | `none` \| `timestamp_utc_9` |

**Semántica de condiciones:**

- Toda condición es un predicado puro evaluado sobre el manifiesto **ya validado**; no infiere valores ni admite defaults.
- `partition == 'calibration'` solo tiene dominio en entradas con plantilla `{partition}`; es verdadera exclusivamente cuando la variable de plantilla vale `calibration`.
- `external_run_only` es verdadera exclusivamente cuando `calibration.mode == "external_run"`; por la norma §9.2 su dominio de uso son las tres rutas `calibration.base_*`.
- `always` es verdadera sin condición adicional.
- Una condición fuera de este vocabulario, o usada fuera de su dominio, es inválida.

**Invariantes normativas de la estructura:**

| ID | Invariante |
|---|---|
| I1 | `manifest_required=True` implica `manifest_required_when=None` |
| I2 | Si `manifest_required_when` está definido, `manifest_allowed_when` también debe estar definido |
| I3 | `nullable=True` solo es válido si el JSON Schema declara `null` para esa ruta (unión de tipos o rama `null`) |
| I4 | Una ruta no puede ser obligatoria en un contexto donde su presencia no esté permitida: si `manifest_required=True` entonces `manifest_allowed_when=None`; si `manifest_required_when=C` y `manifest_allowed_when=D`, debe cumplirse `C ⇒ D` |
| I5 | La exclusión o inclusión en la proyección (`projection_include_when`, `projection_optional`) **no** participa en la determinación de `manifest_required`, `manifest_required_when` ni `manifest_allowed_when`; esas tres propiedades se contrastan con el schema de forma independiente |
| I6 | `projection_optional` no convierte un campo obligatorio del manifiesto en opcional, y toda inclusión condicional permite la omisión: (a) si `manifest_required=True` y `projection_include_when=always`, entonces `projection_optional=False`; (b) si `projection_include_when` es condicional, `projection_optional=True` es obligatorio, con independencia de `manifest_required`. En (b), `projection_optional=True` autoriza omitir **solo** cuando la condición es falsa y nunca autoriza ausentar la ruta del manifiesto si este la exige. `projection_optional=False` con inclusión condicional se rechaza |
| I7 | Si `manifest_required=False`, entonces `projection_optional=True` (la ausencia en el manifiesto implica ausencia permitida en la preimagen) |
| I8 | Tipos y normalización compatibles con el schema: `string`/`string_decimal` ⇒ tipo JSON `string`; `timestamp` ⇒ `string` con `format: date-time`; `integer` ⇒ `integer`; `number` ⇒ `number`; `boolean` ⇒ `boolean`; `array` ⇒ `array`; `object` ⇒ `object`. `normalization=timestamp_utc_9` exige `type=timestamp`; los demás tipos exigen `normalization=none` |
| I9 | Toda condición pertenece al vocabulario de condiciones de §5.3, se evalúa solo en su dominio y contexto válidos; cualquier otra condición es inválida |
| I10 | Las rutas son únicas tras expandir `{partition}`; la expansión produce exactamente `train`, `validation`, `calibration` y `test`; ninguna ruta normativa §9.2 falta y ninguna ruta no normativa se añade |
| I11 | `projection_optional` gobierna solo la omisión; `nullable` gobierna solo la preservación de `None` explícito. Ninguna de las dos sintetiza valores ni `None` |
| I12 | Ninguna ruta de la allowlist es un digest derivado ni el propio `run_fingerprint` |

**Combinaciones inválidas y códigos de error de la futura validación interna de la allowlist:**

| Código | Combinación inválida | Invariante |
|---|---|---|
| `ALLOWLIST_REQUIRED_WITH_WHEN` | `manifest_required=True` con `manifest_required_when` definido | I1 |
| `ALLOWLIST_REQUIRED_WITHOUT_ALLOWED` | `manifest_required_when` definido sin `manifest_allowed_when` | I2 |
| `ALLOWLIST_REQUIRED_NOT_ALLOWED` | obligatoriedad condicional no implicada por admisibilidad, u obligatoria con `manifest_allowed_when` definido | I4 |
| `ALLOWLIST_NULLABLE_NOT_IN_SCHEMA` | `nullable=True` contra un tipo no anulable del schema | I3 |
| `ALLOWLIST_SCHEMA_METADATA_DIVERGENCE` | `manifest_required`/`manifest_required_when`/`manifest_allowed_when` no coinciden con el schema | I5 |
| `ALLOWLIST_REQUIRED_PROJECTION_OPTIONAL` | obligatoria, inclusión `always` y `projection_optional=True` | I6(a) |
| `ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED` | `projection_include_when` condicional (`external_run_only`) con `projection_optional=False` | I6(b) |
| `ALLOWLIST_OPTIONAL_PROJECTION_REQUIRED` | no obligatoria en el manifiesto y `projection_optional=False` | I7 |
| `ALLOWLIST_TYPE_MISMATCH` | `type` incompatible con el tipo declarado por el schema | I8 |
| `ALLOWLIST_NORMALIZATION_MISMATCH` | `timestamp_utc_9` sin `type=timestamp`, o timestamp sin esa normalización | I8 |
| `ALLOWLIST_UNKNOWN_CONDITION` / `ALLOWLIST_CONDITION_CONTEXT` | condición fuera del vocabulario o usada fuera de su dominio | I9 |
| `ALLOWLIST_DUPLICATE_PATH` / `ALLOWLIST_MISSING_PATH` / `ALLOWLIST_EXTRA_PATH` | rutas duplicadas, omitidas o añadidas tras expansión | I10 |
| `ALLOWLIST_TEMPLATE_EXPANSION_INVALID` | `{partition}` no se expande a las cuatro particiones | I10 |
| `ALLOWLIST_DEFAULT_SYNTHESIS` | proyección que intenta inventar valor o `None` | I11 |
| `ALLOWLIST_DERIVED_DIGEST_INCLUDED` | inclusión de `run_fingerprint` u otro digest derivado | I12 |

La futura validación interna de la allowlist debe ser **fail-closed**: cualquiera de estos códigos impide construir la preimagen y se convierte a `list[str]` en la API pública. No se corregirá automáticamente ninguna entrada inválida.

**Contrato determinista de mensajes:** cada error es una única línea con formato `<CODIGO>: <ruta expandida>: <razón>`, sin timestamps, sin representaciones `repr()` de objetos y sin depender del orden de iteración de diccionarios. La lista se ordena por `(ruta, código)` y se deduplica. Para `ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED` la razón exacta es:

```text
ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED: <ruta>: conditional projection_include_when requires projection_optional=True
```

**Compatibilidad de I6(b):** el nuevo código no debilita la obligatoriedad del manifiesto. `base_*` conserva `manifest_required=True` en ambos modos; el error se activa únicamente si se intenta declarar su inclusión condicional con `projection_optional=False`. La combinación válida es `manifest_required=True`, `projection_include_when=external_run_only`, `projection_optional=True`. I6(a), I7 y las demás invariantes siguen aplicándose de forma independiente; un mismo manifiesto puede producir varios códigos, todos reportados en la misma lista ordenada.

### 5.8 Fuente normativa única, oracle y verificaciones de consistencia (AUD-R3-02 / AUD-R4-03 / AUD-R4-04)

**Fuentes y autoridades (sin nueva fuente de verdad):**

1. **Autoridad normativa:** DEC-06 y el diseño v4 §9.2. Definen qué rutas entran en `run_fingerprint`, cuáles se excluyen y las condiciones normativas (`external_run_only`, `shared_with` en calibration, timestamps normalizados). R5 no las modifica.
2. **Contrato estructural canónico:** `src/tradingai/schemas/manifest_v4.json`. Define required, nulabilidad y tipos de cada ruta. R5 no lo modifica.
3. **Representación ejecutable única:** `ALLOWLIST_V4` en `provenance_v4.py`. Es el único listado que usará el código en Fase C. No es una nueva fuente normativa: es una representación derivada que debe demostrar igualdad con (1) y (2).
4. **Oracle normativo independiente:** constante de test `ORACLE_NORMATIVE_V4_R5`, transcrita **directamente de §9.2**, no de `ALLOWLIST_V4` ni del schema. Se usa solo para verificación; nunca es una allowlist de producción.

#### 5.8.1 Oracle normativo independiente

El oracle contiene, por cada ruta expandida, los diez campos:

```text
path, type, manifest_required, manifest_required_when, manifest_allowed_when,
projection_include_when, projection_optional, nullable, normalization, rule_id
```

`rule_id` identifica la fila correspondiente de §9.2 (por ejemplo, la regla de `base_*` con `mode=external_run` o la de `shared_with` en calibration). Las condiciones se transcriben como literales del vocabulario de §5.3, no como texto libre.

**Por qué no reproduce el error de `ALLOWLIST_V4`:**

- Origen distinto: el oracle se transcribe de la **tabla normativa §9.2**; `ALLOWLIST_V4` se codifica en `provenance_v4.py`. No se copia una estructura desde la otra.
- Forma distinta: el oracle se conserva como tabla de verificación con `rule_id`, no como el diccionario de entrada usado por el productor; un error de codificación en una no se propaga automáticamente a la otra.
- Tercera fuente: el schema se consulta por separado para requiredness, tipos y nulabilidad. Una divergencia debe aparecer en al menos una comparación independiente.
- Revisión humana: la transcripción se revisa contra §9.2 y esa revisión queda registrada en el informe de implementación; el checksum **no** sustituye esta revisión semántica.

**Versión y checksum:**

- Versión: `ORACLE_NORMATIVE_V4_R5`.
- Contenido cubierto: el objeto `{"version": <versión>, "entries": [<entradas ordenadas por path>]}`, donde cada entrada usa los diez campos anteriores en ese orden fijo.
- Checksum: `SHA-256` de `rfc8785.dumps` de ese objeto (JCS UTF-8 sin BOM ni LF), en hex minúsculo de 64 caracteres. Cubre versión, todas las rutas, todos los metadatos y todos los `rule_id`. No cubre `ALLOWLIST_V4`, el schema ni el manifiesto.
- El checksum se guarda junto con el oracle en el módulo de pruebas. Un cambio de versión o de contenido sin actualizar el checksum produce `ORACLE_VERSION_MISMATCH` / `ORACLE_CHECKSUM_MISMATCH`.

**Procedimiento ante un cambio normativo:** (1) aprobar el cambio de §9.2/DEC-06 en documentación y auditoría; (2) transcribir el nuevo oracle con versión nueva; (3) revisarlo semánticamente contra la autoridad aprobada; (4) recalcular el checksum; (5) actualizar `ALLOWLIST_V4`; (6) ejecutar todas las verificaciones. No basta con editar la estructura de código ni con igualar un checksum.

#### 5.8.2 Comparación ejecutable contra la autoridad

1. Verificar versión, checksum y completitud del oracle. Si falta algún campo o hay datos incompletos: `ORACLE_INCOMPLETE`; si difiere versión o checksum: códigos de oracle anteriores. **Fail-closed** antes de cualquier comparación.
2. Expandir `ALLOWLIST_V4` y el oracle a rutas concretas (`train`, `validation`, `calibration`, `test`).
3. Comparar conjuntos en ambos sentidos: `ALLOWLIST_MISSING_PATH` / `ALLOWLIST_EXTRA_PATH`.
4. Para cada ruta común, comparar los **nueve metadatos** de `AllowlistEntry` con el oracle: `ALLOWLIST_ORACLE_METADATA_DIVERGENCE`, indicando el campo divergente en la razón.
5. Contrastar además, de forma independiente, tipos, requiredness y nulabilidad contra el schema v4, resolviendo `$defs/partition` y `$defs/calibration_partition`.
6. Comprobar I1…I12 y los códigos `ALLOWLIST_*`, incluido `ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED`.
7. Comprobar exclusiones y ausencia de digests derivados.

**Detección de `external_run_only`:** el oracle declara `projection_include_when=external_run_only` para las tres rutas `calibration.base_*` porque §9.2 lo exige. El schema **no** codifica esa condición. Si `ALLOWLIST_V4` cambiara ese valor a `always`, el paso 4 detectaría la divergencia aunque los pasos 3, 5 y 6 (conjuntos de rutas, contraste con el schema e invariantes internas) pasaran. El oracle verifica condiciones normativas, no solo conjuntos de rutas.

Cualquier fallo produce error determinista, impide calcular el fingerprint y se reporta como `list[str]` ordenada; nunca se usa una representación alternativa ni un fallback.

#### 5.8.3 Derivación de condiciones desde el JSON Schema v4

La derivación se aplica solo a entradas con plantilla `{partition}` y se realiza una sola vez, de forma que la representación resultante sea coherente y no se dupliquen reglas manuales:

1. Expandir `{partition}` a `train`, `validation`, `calibration` y `test`.
2. Resolver cada ruta: `validation.partitions.properties.<partición>.$ref` apunta a `#/$defs/partition` para `train`, `validation` y `test`, y a `#/$defs/calibration_partition` para `calibration`.
3. Calcular `permitida(par)` = la propiedad existe en el `$defs` resuelto **y** no queda prohibida por `additionalProperties:false`.
4. Calcular `obligatoria(par)` = el nombre figura en la lista `required` del `$defs` resuelto.
5. Derivar:
   - Si `obligatoria` es verdadera en las cuatro particiones → `manifest_required=True`, `manifest_required_when=None`.
   - Si `obligatoria` y `permitida` son verdaderas solo en `calibration` → `manifest_required=False`, `manifest_required_when=partition == 'calibration'`, `manifest_allowed_when=partition == 'calibration'`.
   - Si `obligatoria` es falsa en todas → `manifest_required=False`; `manifest_required_when=None`; `manifest_allowed_when` según `permitida` en cada partición.
   - Si existe un caso con `obligatoria=True` y `permitida=False` → combinación inválida (`ALLOWLIST_REQUIRED_NOT_ALLOWED`).
6. Colapsar los cuatro resultados en **una única entrada plantilla**, conservando el significado de las definiciones originales; las pruebas derivan su comportamiento de esa entrada.

**Caso `shared_with`:** `$defs/calibration_partition.required` incluye `shared_with`, por lo que es obligatorio en `calibration`; `$defs/partition` no lo declara y tiene `additionalProperties:false`, por lo que está prohibido en `train`, `validation` y `test`. De ahí la única entrada `MR=No`, `MRW=MAW=partition == 'calibration'`. El diseño v4 §6 exige además que su valor sea `validation` y rechaza `null`; esa comprobación de valor pertenece a la admisión y no se reimplementa en la proyección.

#### 5.8.4 Verificaciones automáticas

| Verificación | Detecta |
|---|---|
| Versión, checksum y completitud del oracle | Transcripción incompleta o no revisada |
| Igualdad de conjuntos contra el oracle | Rutas omitidas o adicionales |
| Comparación de los nueve metadatos contra el oracle | Divergencia de tipos, requiredness, nulabilidad, condiciones, opcionalidad y normalización, incluido `external_run_only` |
| Resolución de cada ruta contra el schema (`$defs/partition`, `calibration_partition`) | Rutas inexistentes y condiciones de presencia incompatibles |
| Comparación de `type` y `nullable` con el schema | Tipos divergentes y nulabilidad incompatible |
| Derivación §5.8.3 frente a `manifest_required_when`/`manifest_allowed_when` | Reglas de obligatoriedad contradictorias |
| Comprobación de I1…I12 y códigos `ALLOWLIST_*` | Combinaciones inválidas de metadatos |
| Comprobación de exclusiones y ausencia de digests derivados | Campos derivados incluidos indebidamente |

---

## 6. Fingerprints dentro del alcance C

### 6.1 `run_fingerprint` `[PROPUESTA]`

```python
def build_run_fingerprint(manifest: dict[str, Any]) -> str: ...
```

`SHA-256` de `rfc8785.dumps(project_allowlist(manifest))`, hex minúsculo de 64 caracteres. Sin LF. Sin inclusión de `run_fingerprint`. Conforme a Q-01, `validate_manifest_v4` **no** añade error de comparación.

### 6.2 `partition_manifest_sha256` `[PROPUESTA]`

```python
def build_partition_manifest_sha256(manifest: dict[str, Any]) -> str: ...
```

Preimagen: objeto con `train`, `validation`, `calibration` y `test`, cada uno con el objeto completo de partición tal como figura en el manifiesto, incluidos `time_start`/`time_end` declarados, `index_sha256` y `shared_with` cuando corresponda. No se aplica normalización UTC aquí.

### 6.3 Constructores diferidos (Q-02)

| Constructor | Fase | Estado en R5 |
|---|---|---|
| `build_index_sha256(rows)` | D | Referencia; secuencia explícita, sin datos originales |
| `build_calibration_input_sha256(inputs)` | D | Referencia; `f64be` y entradas efectivas |
| `build_event_sha256(payload)` | E | Referencia; payload de nueve campos sin `event_sha256` |

**Reconciliación Q-02 / V4-U11:** el plan R1.2 (Fase C, punto 6) exige el recálculo independiente de cuatro digests desde sus propias preimágenes. Bajo Q-02, esa obligación se distribuye: en Fase C se implementa y recalcula **`partition_manifest_sha256`**; `index_sha256` y `calibration_input_sha256` quedan diferidos a Fase D; `event_sha256` queda diferido a Fase E. Esta distribución **no elimina** el requisito normativo V4-U11 y **no afirma** que los tres constructores diferidos estén implementados: cada fase aportará su recálculo cuando se implemente. CP-C-11 cubre el recálculo de `partition_manifest_sha256` en C y CP-C-18 impide incorporar capacidades de D/E en C.

### 6.4 Reglas comunes

- `SHA-256(JCS UTF-8 sin BOM ni LF)` para todos los digests de provenance.
- `manifest.sha256` (fuera de C): JCS + exactamente un LF.
- Ninguna preimagen incluye el digest que produce; sin circularidad.
- Fingerprint ≠ firma: no demuestra autenticidad, autoría ni autorización.

---

## 7. Contrato de normalización UTC (Q-03) `[PROPUESTA]`

```python
def normalize_timestamp(value: str) -> str: ...
```

| Aspecto | Regla |
|---|---|
| Entrada | String RFC 3339 con `Z` o `±HH:MM` |
| Rechazo | Zona ausente, `-00:00`, segundo `60`, >9 dígitos fraccionarios, fecha/offset inválidos, desbordamiento |
| Validación | Calendario y offset `HH <= 23`, `MM <= 59` |
| Precisión | Fracción como entero de nanosegundos; sin truncamiento ni redondeo |
| Conversión | UTC por aritmética entera de segundos de offset |
| Formato | `YYYY-MM-DDTHH:MM:SS.fffffffffZ`, exactamente 9 dígitos rellenos a la derecha |
| Salida | String determinista apto para JCS |
| Reutilización | Fase D debe usar este helper |

---

## 8. Vectores RFC 8785

**Procedencia:** RFC 8785, June 2020, §§3.2.2–3.2.4 y Appendix B Table 1, `https://www.rfc-editor.org/rfc/rfc8785.txt`, consultado el 2026-11-27.

### 8.1 Objeto canónico

Entrada:

```json
{
  "numbers": [333333333.33333329, 1E30, 4.50, 2e-3, 0.000000000000000000000000001],
  "string": "\u20ac$\u000F\u000aA'\u0042\u0022\u005c\\\"\/",
  "literals": [null, true, false]
}
```

Salida exacta:

```text
{"literals":[null,true,false],"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],"string":"€$\u000f\nA'B\"\\\\\"/"}
```

Bytes UTF-8 (hex):

```text
7b 22 6c 69 74 65 72 61 6c 73 22 3a 5b 6e 75 6c 6c 2c 74 72
75 65 2c 66 61 6c 73 65 5d 2c 22 6e 75 6d 62 65 72 73 22 3a
5b 33 33 33 33 33 33 33 33 33 2e 33 33 33 33 33 33 33 2c 31
65 2b 33 30 2c 34 2e 35 2c 30 2e 30 30 32 2c 31 65 2d 32 37
5d 2c 22 73 74 72 69 6e 67 22 3a 22 e2 82 ac 24 5c 75 30 30
30 66 5c 6e 41 27 42 5c 22 5c 5c 5c 5c 5c 22 2f 22 7d
```

Orden de propiedades del §3.2.3: `"Carriage Return"`, `"One"`, `"Control"`, `"Latin Small Letter O With Diaeresis"`, `"Euro Sign"`, `"Emoji: Grinning Face"`, `"Hebrew Letter Dalet With Dagesh"`.

### 8.2 Appendix B Table 1

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
| `7fffffffffffffff` | *(error)* | NaN (3) |
| `7ff0000000000000` | *(error)* | Infinity (3) |
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

Notas: (1) rango recomendado para enteros verdaderos; (2) sin precisión extendida; (3) valores fuera de rango inválidos en JSON; (4) redondeo al par más cercano.

### 8.3 Vector reducido §9.5

Entrada:

```json
{"calibration_intent":{"fit_partition":"validation","method":"sigmoid","mode":"in_pipeline"},"data":{"dataset_sha256":"b"},"features":{"ordered":["close","volume"]},"git":{"source_bundle_sha256":"a"},"schema_version":"3.0.0","target":{"horizon_bars":1},"training":{"seed":42},"validation_intent":{"split_method":"chronological_holdout"}}
```

SHA-256 esperado: `ed01f9cea45b644c561b6eb0346c7450b7836abb35f4ece1ede5b265e3722157`. Es control JCS, no vector dorado completo de `run_fingerprint`.

---

## 9. Matriz CP-C-01 a CP-C-18

Ningún criterio se marca PASS: no existe implementación de Fase C.

| ID | Criterio | Requisito | Prueba | Estado |
|---|---|---|---|---|
| CP-C-01 | JCS usa `rfc8785` 0.1.4, sin serializadores alternativos | C1/Q-05 | §8 + verificación de dependencia | Definido, pendiente |
| CP-C-02 | Vectores oficiales reproducidos | C1 | §8.1–8.3 | Definido, pendiente |
| CP-C-03 | `-0`, límites y NaN/Inf correctos | C1 | §8.2 | Definido, pendiente |
| CP-C-04 | Orden UTF-16 y escapes correctos | C1 | §8.1 | Definido, pendiente |
| CP-C-05 | Proyección igual a `ALLOWLIST_V4` **y** a `ORACLE_NORMATIVE_V4_R5` (rutas y nueve metadatos); invariantes I1…I12 validados | C2 | §5.6–5.8 + pruebas generadas desde la allowlist y el oracle | Definido, pendiente |
| CP-C-06 | Campos excluidos no alteran el fingerprint | C2/DEC-06 | Pruebas de exclusiones §5.5 | Definido, pendiente |
| CP-C-07 | Ausencia vs `null` distinguidos | C2 | Pruebas por `nullable`/`projection_optional` | Definido, pendiente |
| CP-C-08 | `base_*` incluidos solo en `external_run_only` | C2/Q-02 | Pruebas por `projection_include_when` | Definido, pendiente |
| CP-C-09 | `run_fingerprint` reproducible | C3/V4-U10 | Mutación y repetición | Definido, pendiente |
| CP-C-10 | Constructor implementado sin comparación de admisión | Q-01 | Prueba de ausencia de error añadido | Reformulado, pendiente |
| CP-C-11 | `partition_manifest_sha256` recalculable | Q-02 | Prueba con particiones completas | Definido, pendiente |
| CP-C-12 | Ninguna preimagen contiene su digest | §9.4 | Prueba de allowlist sin `run_fingerprint` | Definido, pendiente |
| CP-C-13 | Errores deterministas y tipados, incluidos los códigos `ALLOWLIST_*` y su rechazo fail-closed | C4 | §5.7 y §5.8.2 + timestamps y JCS inválido | Definido, pendiente |
| CP-C-14 | No mutación del manifiesto | C4 | `deepcopy` antes/después | Definido, pendiente |
| CP-C-15 | v3 idéntico | C5 | `provenance.py` sin diff; suites v3 | Definido, pendiente |
| CP-C-16 | Sin fallback entre versiones | C5/DEC-05 | Dispatch tests | Definido, pendiente |
| CP-C-17 | Regresiones documentadas | C6 | §9.1 | Precisado, pendiente |
| CP-C-18 | C sin capacidades de D/E/F | Q-02 | Revisión de diff | Definido, pendiente |

### 9.1 CP-C-17 — conteos (AUD-R2-04)

| Suite | Conteo documentado | Naturaleza |
|---|---|---|
| `tests/test_provenance_v4_schema.py` | 37 | Definiciones `def test_` verificadas por auditoría |
| `tests/test_provenance.py` | 116 | Definiciones `def test_` verificadas por auditoría |
| `tests/test_provenance_v4_dispatch.py` | 29 | Casos recogidos con parametrización (14 definiciones) |
| Suite completa | 507 | Casos recogidos con parametrización (364 definiciones estáticas) |
| `tests/test_provenance_v4_canonical.py` (propuesta) | No inventado | Se fijará al crear la suite |

No se suman cantidades solapadas: 507 es el total de la suite completa, no un quinto módulo independiente. No se afirma que estas pruebas se ejecutaron durante R5.

Las verificaciones de §§5.7–5.8 quedan cubiertas explícitamente por los criterios existentes, sin crear identificadores nuevos:

- **CP-C-05:** igualdad `ALLOWLIST_V4` ↔ oracle normativo §9.2 en rutas y nueve metadatos, más validación de I1…I12.
- **CP-C-13:** códigos `ALLOWLIST_*`, mensajes deterministas y rechazo fail-closed, además de errores de timestamps y JCS.
- **CP-C-07:** ausencia frente a `null`.
- **CP-C-08:** inclusión condicional de `base_*` (`external_run_only`) y exclusión con `in_pipeline`.
- **CP-C-12:** ausencia de digests derivados en las preimágenes.

Ningún criterio se marca PASS.

### 9.2 Criterios futuros fuera de CP-C

| Criterio | Dependencia |
|---|---|
| Comparación de `run_fingerprint` en admisión | Diseño posterior (Q-01) |
| `index_sha256`, `calibration_input_sha256` | Fase D (Q-02) |
| `event_sha256` | Fase E (Q-02) |
| Fijación `rfc8785==0.1.4` | Autorización de dependencias (Q-05) |

---

## 10. Matriz de trazabilidad

### 10.1 Hallazgos F-C-01 a F-C-09 (auditoría R1)

| Hallazgo | Sección R5 | Estado documental |
|---|---|---|
| F-C-01 | §4.3 | Resuelto |
| F-C-02 | §5, §9 | Resuelto |
| F-C-03 | §9, §9.2 | Resuelto |
| F-C-04 | §8.3 | Resuelto |
| F-C-05 | §4.4 | Resuelto |
| F-C-06 | §6.2 | Resuelto |
| F-C-07 | §4.2 | Resuelto |
| F-C-08 | §8.1–8.2 | Resuelto |
| F-C-09 | §5.1–5.6 | Resuelto |

### 10.2 Hallazgos AUD-R2-01 a AUD-R2-04 (auditoría R2)

| Hallazgo | Corrección | Sección R5 | Estado documental |
|---|---|---|---|
| AUD-R2-01 | Separación de obligatoriedad en manifiesto y opcionalidad en proyección; caso `base_*` | §5.1 y nota en §5.4 | Resuelto |
| AUD-R2-02 | Condición `partition == 'calibration'` para `shared_with` | §5.1, §5.3 y nota en §5.4 | Resuelto |
| AUD-R2-03 | Semántica de todos los tipos, incluidos `timestamp` y `string_decimal` | §5.2 | Resuelto |
| AUD-R2-04 | Nota de conteos parametrizados | §9.1 | Resuelto |

### 10.3 Hallazgos AUD-R3-01 a AUD-R3-02 (auditoría R3)

| Hallazgo | Resolución | Resultado |
|---|---|---|
| AUD-R3-01 | Invariantes formales I1…I12 y códigos `ALLOWLIST_*` para combinaciones inválidas (§5.7) | Pendiente de auditoría |
| AUD-R3-02 | Fuente normativa única, representación ejecutable derivada y verificaciones automáticas de consistencia (§5.8) | Pendiente de auditoría |

### 10.4 Hallazgos AUD-R4-01 a AUD-R4-07 (auditoría R4)

| Hallazgo | Resolución | Resultado |
|---|---|---|
| AUD-R4-01 | Algoritmo ordenado de preimagen con rama explícita para condición falsa (§5.6) | Pendiente de auditoría |
| AUD-R4-02 | I6 bidireccional y `ALLOWLIST_CONDITIONAL_PROJECTION_REQUIRED` (§5.7) | Pendiente de auditoría |
| AUD-R4-03 | Oracle normativo con metadatos, condiciones, versión y checksum (§5.8.1–5.8.2) | Pendiente de auditoría |
| AUD-R4-04 | Derivación de `MRW`/`MAW` desde los `$defs` (§5.8.3) | Pendiente de auditoría |
| AUD-R4-05 | Cobertura explícita en CP-C-05 y CP-C-13 (§9, §9.1) | Pendiente de auditoría |
| AUD-R4-06 | I9 referencia §5.3 (§5.7) | Pendiente de auditoría |
| AUD-R4-07 | Reconciliación Q-02 / V4-U11 (§6.3) | Pendiente de auditoría |

### 10.5 Preservación de decisiones

DEC-01 a DEC-09 permanecen sin reinterpretación. Q-01, Q-02, Q-03 y Q-05 permanecen exactamente como fueron aprobadas (§3). CP-C-01 a CP-C-18 se conservan (§9). Ningún criterio marca PASS.

---

## 11. Riesgos y límites de alcance

| Riesgo / límite | Estado |
|---|---|
| Deriva de `ALLOWLIST_V4` | Mitigado por estructura versionada, invariantes §5.7, oracle normativo independiente §5.8 y pruebas generadas desde ambas representaciones |
| Actualización de `rfc8785` | Requiere revalidar §8 y auditoría |
| LF vs sin LF | Pruebas separadas en implementación futura |
| Comparación de admisión | Fuera de C por Q-01 |
| Constructores D/E | Asignados por Q-02 |
| Fases D, E, F, G y S2 | No autorizadas |
| Loaders, registry, writer, inferencia | No incluidos |
| Parquet protegidos | No accesados |

Fase C solo produciría `_jcs_bytes_v4`, `normalize_timestamp`, `project_allowlist`, `build_run_fingerprint`, `build_partition_manifest_sha256` y errores tipados asociados, tras autorización separada.

---

## 12. Conclusión

R5 es una propuesta de diseño completa y autónoma que incorpora las decisiones del propietario y corrige los hallazgos de las auditorías R1, R2, R3 y R4. No modifica R1, R2, R3 ni R4, no implementa código, no ejecuta pruebas y no cambia dependencias ni datos.

**Fase C continúa BLOCKED**, pendiente de auditoría independiente R5, aprobación expresa del diseño y autorización técnica separada para implementar. La aprobación futura no autorizaría Fase D, E, F, G ni S2.

**Fin de R13-PHASE-C-DESIGN-R5.**
