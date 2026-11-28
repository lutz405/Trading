# R13-PHASE-C-DESIGN-R4 — Diseño técnico de Fase C (cierre de invariantes de `ALLOWLIST_V4`)

**Estado del documento:** propuesta de diseño R4, preparada para auditoría independiente. No implementa Fase C, no declara Fase C aprobada y no autoriza su implementación.
**Fecha:** 2026-11-27.
**Base:** commit `259ca6ee11878f114cdcab4cef500074b3bc1a48` (`main`, `origin/main` alineados).
**Predecesores:** `docs/r13_phase_c_design_r1.md`, `docs/r13_phase_c_design_r2.md` y `docs/r13_phase_c_design_r3.md`, conservados sin modificaciones.
**Auditorías incorporadas:** `R13-AUDIT-PHASE-C-DESIGN-R1` (F-C-01…F-C-09), `R13-AUDIT-PHASE-C-DESIGN-R2` (AUD-R2-01…AUD-R2-04) y `R13-AUDIT-PHASE-C-DESIGN-R3` (AUD-R3-01…AUD-R3-02).
**Fase C:** **BLOCKED** hasta auditoría independiente R4, aprobación expresa del propietario y autorización técnica separada.

---

## 1. Identificación y alcance de R4

R4 es un documento completo y autónomo: no requiere combinar R1, R2 ni R3 para entender el diseño. Corrige los dos hallazgos de la auditoría R3:

- **AUD-R3-01:** formaliza invariantes y combinaciones inválidas de `AllowlistEntry`.
- **AUD-R3-02:** documenta la fuente normativa única y las verificaciones automáticas de consistencia.

Conserva íntegramente las correcciones de R1, R2 y R3:

- **F-C-01…F-C-09:** timestamp/DEC-06, parametrización derivada, CP-C, vector completo, `1.0 ≡ 1`, partición sin normalizar, RFC vs política, vectores oficiales y estructura formal.
- **AUD-R2-01…AUD-R2-04:** separación de obligatoriedad/proyección, `shared_with` por partición, semántica de tipos y conteos parametrizados.

No se autoriza implementación. El alcance futuro autorizable sigue siendo: `src/tradingai/ml/provenance_v4.py` y pruebas nuevas de Fase C. No se modificarán `provenance.py`, `manifest_v3.json`, `manifest_v4.json`, dependencias, modelos ni datasets.

R4 añade dos secciones nuevas dentro del §5: **§5.7 Invariantes formales de `AllowlistEntry`** y **§5.8 Fuente normativa única y verificaciones de consistencia**. El resto del diseño se conserva.

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
| `docs/r13_phase_c_design_r3.md` | Diseño inmediatamente anterior, conservado |
| `R13-AUDIT-PHASE-C-DESIGN-R3` | Hallazgos AUD-R3-01 y AUD-R3-02 (entregado en la conversación; no publicado como archivo) |
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

No hay solapamientos. R4 no desarrolla los constructores de D/E.

### 3.3 Q-03 — Normalización UTC

Fase C define un único helper común de normalización UTC, reutilizable por Fase D. Contrato en §7. No se implementa en esta tarea documental. R4 conserva este extremo sin cambios.

### 3.4 Q-05 — Dependencia `rfc8785`

Decisión de diseño: fijar `rfc8785==0.1.4`. `pyproject.toml` actualmente declara `rfc8785>=0.1.4`; **no se modifica en R4**. Toda actualización futura exige revalidar los vectores de §8 y nueva auditoría.

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

### 5.6 Construcción de la preimagen

1. El manifiesto ya pasó schema v4, enteros seguros, DEC-09 y validación de timestamps.
2. Se recorre `ALLOWLIST_V4`, no el manifiesto.
3. Se evalúan `manifest_required`, `manifest_required_when`, `manifest_allowed_when` y `projection_include_when`.
4. Si la ruta está ausente y `projection_optional=True`, se omite; si `projection_optional=False`, la ausencia es error de contrato.
5. Si `nullable=True` y el valor es `None`, se copia `None`; si `nullable=False`, `None` ya fue rechazado por el schema.
6. Si `normalization=timestamp_utc_9`, se aplica §7 antes de copiar.
7. No se copia ninguna exclusión, ni como `None`.
8. El objeto resultante se construye en orden explícito; JCS ordena claves por UTF-16BE, por lo que el orden de inserción del manifiesto original no afecta el digest.

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
| I6 | `projection_optional` no convierte un campo obligatorio del manifiesto en opcional: si `manifest_required=True` y `projection_include_when=always`, entonces `projection_optional=False`; si `manifest_required=True` y la inclusión es condicional, `projection_optional=True` solo autoriza omitir cuando la condición es falsa |
| I7 | Si `manifest_required=False`, entonces `projection_optional=True` (la ausencia en el manifiesto implica ausencia permitida en la preimagen) |
| I8 | Tipos y normalización compatibles con el schema: `string`/`string_decimal` ⇒ tipo JSON `string`; `timestamp` ⇒ `string` con `format: date-time`; `integer` ⇒ `integer`; `number` ⇒ `number`; `boolean` ⇒ `boolean`; `array` ⇒ `array`; `object` ⇒ `object`. `normalization=timestamp_utc_9` exige `type=timestamp`; los demás tipos exigen `normalization=none` |
| I9 | Toda condición pertenece a su dominio definido y se evalúa solo en el contexto válido (I8 del vocabulario de condiciones) |
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
| `ALLOWLIST_REQUIRED_PROJECTION_OPTIONAL` | obligatoria, inclusión `always` y `projection_optional=True` | I6 |
| `ALLOWLIST_OPTIONAL_PROJECTION_REQUIRED` | no obligatoria en el manifiesto y `projection_optional=False` | I7 |
| `ALLOWLIST_TYPE_MISMATCH` | `type` incompatible con el tipo declarado por el schema | I8 |
| `ALLOWLIST_NORMALIZATION_MISMATCH` | `timestamp_utc_9` sin `type=timestamp`, o timestamp sin esa normalización | I8 |
| `ALLOWLIST_UNKNOWN_CONDITION` / `ALLOWLIST_CONDITION_CONTEXT` | condición fuera del vocabulario o usada fuera de su dominio | I9 |
| `ALLOWLIST_DUPLICATE_PATH` / `ALLOWLIST_MISSING_PATH` / `ALLOWLIST_EXTRA_PATH` | rutas duplicadas, omitidas o añadidas tras expansión | I10 |
| `ALLOWLIST_TEMPLATE_EXPANSION_INVALID` | `{partition}` no se expande a las cuatro particiones | I10 |
| `ALLOWLIST_DEFAULT_SYNTHESIS` | proyección que intenta inventar valor o `None` | I11 |
| `ALLOWLIST_DERIVED_DIGEST_INCLUDED` | inclusión de `run_fingerprint` u otro digest derivado | I12 |

La futura validación interna de la allowlist debe ser **fail-closed**: cualquiera de estos códigos impide construir la preimagen y se convierte a `list[str]` en la API pública. No se corregirá automáticamente ninguna entrada inválida.

### 5.8 Fuente normativa única y verificaciones de consistencia (AUD-R3-02)

**Fuentes y autoridades (sin nueva fuente de verdad):**

1. **Autoridad normativa:** DEC-06 y el diseño v4 §9.2. Definen qué rutas entran en `run_fingerprint`, cuáles se excluyen y las condiciones normativas (`external_run_only`, `shared_with` en calibration). R4 no las modifica.
2. **Contrato estructural canónico:** `src/tradingai/schemas/manifest_v4.json`. Define required, nulabilidad y tipos de cada ruta. R4 no lo modifica.
3. **Representación ejecutable única:** `ALLOWLIST_V4` en `provenance_v4.py`. Es el único listado que usará el código en Fase C. No es una nueva fuente normativa: es una representación derivada que debe demostrar igualdad con (1) y (2).
4. **Oracle de prueba:** una constante de test transcrita literalmente de §9.2. Se usa solo para verificación; **no** es una segunda allowlist de producción.

**Verificaciones automáticas que deben implementarse con Fase C:**

| Verificación | Detecta |
|---|---|
| Igualdad de conjuntos: expandir `ALLOWLIST_V4` y comparar con el oracle §9.2 | Rutas omitidas o adicionales |
| Resolución de cada ruta contra el schema (incluyendo `$defs/partition` y `calibration_partition`) | Rutas inexistentes y condiciones de presencia incompatibles |
| Comparación de `type` con el tipo declarado por el schema | Tipos divergentes |
| Comparación de `manifest_required`/`manifest_required_when`/`manifest_allowed_when` con `required` del schema | Reglas de obligatoriedad contradictorias |
| Comparación de `nullable` con uniones que incluyen `null` | Nulabilidad incompatible |
| Comprobación de I1…I12 y códigos `ALLOWLIST_*` | Combinaciones inválidas de metadatos |
| Comprobación de exclusiones y ausencia de digests derivados | Campos derivados incluidos indebidamente |

Cualquier fallo produce error determinista, impide calcular el fingerprint y se reporta como `list[str]`; nunca se usa una representación alternativa ni un fallback. Si el contrato normativo cambiara, debe actualizarse primero la documentación aprobada y repetirse la auditoría; no basta con editar la estructura de código.

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

| Constructor | Fase | Estado en R4 |
|---|---|---|
| `build_index_sha256(rows)` | D | Referencia; secuencia explícita, sin datos originales |
| `build_calibration_input_sha256(inputs)` | D | Referencia; `f64be` y entradas efectivas |
| `build_event_sha256(payload)` | E | Referencia; payload de nueve campos sin `event_sha256` |

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
| CP-C-05 | Proyección igual a `ALLOWLIST_V4` | C2 | §5 + pruebas generadas | Definido, pendiente |
| CP-C-06 | Campos excluidos no alteran el fingerprint | C2/DEC-06 | Pruebas de exclusiones §5.5 | Definido, pendiente |
| CP-C-07 | Ausencia vs `null` distinguidos | C2 | Pruebas por `nullable`/`projection_optional` | Definido, pendiente |
| CP-C-08 | `base_*` incluidos solo en `external_run_only` | C2/Q-02 | Pruebas por `projection_include_when` | Definido, pendiente |
| CP-C-09 | `run_fingerprint` reproducible | C3/V4-U10 | Mutación y repetición | Definido, pendiente |
| CP-C-10 | Constructor implementado sin comparación de admisión | Q-01 | Prueba de ausencia de error añadido | Reformulado, pendiente |
| CP-C-11 | `partition_manifest_sha256` recalculable | Q-02 | Prueba con particiones completas | Definido, pendiente |
| CP-C-12 | Ninguna preimagen contiene su digest | §9.4 | Prueba de allowlist sin `run_fingerprint` | Definido, pendiente |
| CP-C-13 | Errores deterministas y tipados | C4 | Timestamps y JCS inválido | Definido, pendiente |
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

No se suman cantidades solapadas: 507 es el total de la suite completa, no un quinto módulo independiente. No se afirma que estas pruebas se ejecutaron durante R4.

Las verificaciones introducidas en §§5.7–5.8 se cubren con los criterios existentes CP-C-05, CP-C-07, CP-C-08, CP-C-12 y CP-C-13. No se añaden identificadores CP-C nuevos y ninguno se marca PASS.

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

| Hallazgo | Sección R4 | Estado documental |
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

| Hallazgo | Corrección | Sección R4 | Estado documental |
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

### 10.4 Preservación de decisiones

Q-01, Q-02, Q-03 y Q-05 permanecen exactamente como fueron aprobadas (§3). CP-C-01 a CP-C-18 se conservan (§9). Ningún criterio marca PASS.

---

## 11. Riesgos y límites de alcance

| Riesgo / límite | Estado |
|---|---|
| Deriva de `ALLOWLIST_V4` | Mitigado por estructura versionada, invariantes §5.7, fuente única §5.8 y pruebas generadas desde la estructura |
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

R4 es una propuesta de diseño completa y autónoma que incorpora las decisiones del propietario y corrige los hallazgos de las auditorías R1, R2 y R3. No modifica R1, R2 ni R3, no implementa código, no ejecuta pruebas y no cambia dependencias ni datos.

**Fase C continúa BLOCKED**, pendiente de auditoría independiente R4, aprobación expresa del diseño y autorización técnica separada para implementar. La aprobación futura no autorizaría Fase D, E, F, G ni S2.

**Fin de R13-PHASE-C-DESIGN-R4.**
