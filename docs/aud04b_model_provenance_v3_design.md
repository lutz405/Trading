# AUD-04B.1 — Contrato de procedencia de modelos v3

**Estado:** diseño técnico. **No implementado.**
**Fecha:** 2026-11-25
**Commit de referencia:** `3ba460d5c02864d3355928d75b8fedf11e9ca517`
**Repositorio canónico:** `C:\Users\USER\Documents\GitHub\Trading`
**Alcance:** especificación del manifiesto, almacenamiento, loader, integración, ubicación canónica y plan de pruebas.
**Fuera de alcance:** implementación, entrenamiento, calibración, selección de modelo canónico y migración de artefactos legacy.

> Este documento no modifica código, configuraciones, modelos, datasets ni los documentos de cuarentena. El ejemplo de manifiesto es ficticio y no corresponde a ningún artefacto existente.

## Índice

1. Resumen de decisiones
2. Estado de partida y supuestos
3. Principios de diseño
4. Modelo conceptual
5. Manifiesto v3
6. Invariantes
7. Estructura de almacenamiento
8. Loader
9. Modelo de amenazas
10. Integración futura
11. Ubicación canónica
12. Plan de implementación
13. Plan de pruebas
14. Decisiones pendientes
15. Criterios de aceptación

---

## 1. Resumen de decisiones

| Decisión | Resultado |
|---|---|
| Identidad | `model_id` opaco e inmutable con formato `mdl_<ULID>`; `run_fingerprint` separado para comparar reproducibilidad |
| Inmutabilidad | Un directorio de run publicado no se modifica nunca; cualquier cambio exige un `model_id` nuevo |
| Hash del manifiesto | Hash **desacoplado** en `manifest.sha256`; el manifiesto no contiene su propio hash |
| Estado | `status_at_seal` en el manifiesto; el estado efectivo vive en un registro de ciclo de vida append-only |
| Calibración | `base_model_id` + hashes de RF/XGB + hash de las entradas de calibración |
| Almacenamiento | `models/runs/<model_id>/`; prohibidos los nombres genéricos en la raíz de `models/` |
| Publicación | Escritura en staging, validación, `fsync` y renombrado atómico; nunca sobrescritura |
| Loader | Fail-closed; verifica schema, hashes, estado, clases, features y versiones **antes** de deserializar |
| Autenticidad | Firma Ed25519 opcional pero obligatoria para `approved`; el hash por sí solo no autentica |
| Aprobación | Solo un evento humano firmado puede promover a `approved`; el pipeline solo puede sellar |
| Ubicación canónica | `C:\Users\USER\Documents\GitHub\Trading`; la copia sin Git queda congelada o se convierte en worktree |

---

## 2. Estado de partida y supuestos

| Elemento | Estado en AUD-04A |
|---|---|
| Commit | `3ba460d5c02864d3355928d75b8fedf11e9ca517`, `main`, igual a `origin/main` |
| Artefactos legacy | 30 archivos en `_t7`, `_t8`, `_t9`, `_test`, `_testcal`; todos en cuarentena documental |
| Modelo canónico | **Ninguno** |
| Loader de RF/XGB | **No existe** en producción |
| Loader de calibrador | `Calibrator.load()`, sin vínculo al modelo base |
| Configuración | `config/ml.yaml:7` usa `model_dir: models` |
| Escritura | `save_artifact()` escribe `.joblib` y `.json` sin checksum ni transacción conjunta |
| Métricas calibradas | Se calculan y se devuelven, pero no se persisten |
| Estado del artefacto | No existe; `config/decision.yaml:13` usa `model_version: "v0.1"` como texto libre |

### Supuestos de diseño

1. El repositorio y el almacén de artefactos son locales; no hay servicio remoto de modelos.
2. Un solo proceso escribe runs a la vez; la concurrencia multi-escritor se trata como no soportada y se detecta con locks.
3. `models/runs/` y `models/.staging/` están en el mismo volumen, requisito para el renombrado atómico.
4. El entorno de ejecución es Windows para desarrollo y puede ser Linux en CI; el diseño no depende de permisos POSIX.
5. Python 3.13, scikit-learn 1.9.x, xgboost 3.4.x y joblib 1.6.x son el entorno actual; el contrato registra versiones y el loader aplica una política de compatibilidad explícita.
6. Ningún artefacto legacy se migrará a v3; se conserva en cuarentena y se regenera desde cero cuando se autorice.
7. La autenticidad fuerte requiere una clave fuera del repositorio; si no existe, el sistema funciona en modo integridad, nunca en modo autenticado.

---

## 3. Principios de diseño

**P1 — Una ejecución, una identidad.** `model_id` se asigna una vez, al reservar el run, y no se reutiliza jamás. No se deriva del contenido para evitar ciclos y para permitir runs idénticos con fines de reproducibilidad.

**P2 — Los artefactos son inmutables.** Publicar es crear; corregir es crear otro run. No existe `--force`, `--overwrite` ni escritura in-place.

**P3 — Referencias, no copias.** El manifiesto referencia dataset, features, particiones y artefactos por hash. No incrusta matrices ni modelos.

**P4 — Fail-closed.** Cualquier campo ausente, hash incorrecto, estado desconocido o versión no soportada produce rechazo. Nunca hay un modelo por defecto.

**P5 — Integridad no es autenticidad.** Un SHA-256 correcto solo demuestra que los bytes no cambiaron respecto de lo registrado. No demuestra quién los produjo ni que sean seguros.

**P6 — La aprobación es un acto humano explícito.** El pipeline puede sellar y validar; no puede aprobar. Un manifiesto no puede auto-declararse aprobado.

**P7 — Sin rutas genéricas.** `models/rf.joblib`, `models/xgb.joblib` y `models/calibrator.json` dejan de ser válidos. Todo artefacto vive dentro de `models/runs/<model_id>/`.

**P8 — La reproducibilidad se mide, no se asume.** Se registra `run_fingerprint`, el entorno y los flags de determinismo; dos runs con el mismo fingerprint pueden compararse, pero no se declaran idénticos sin evidencia.

**P9 — El test se usa una vez.** La partición de test se evalúa para el informe final; no se usa para seleccionar hiperparámetros ni calibradores.

**P10 — El legado no se toca.** `_t7`, `_t8`, `_t9`, `_test`, `_testcal` y `QUARANTINE.*` permanecen intactos hasta una decisión explícita.

---

## 4. Modelo conceptual

| Término | Definición |
|---|---|
| **Run** | Una ejecución de entrenamiento con identidad propia, desde la reserva del `model_id` hasta la publicación sellada |
| **model_id** | Identificador opaco, único e inmutable del run y del ensemble producido |
| **Ensemble** | Conjunto RF + XGBoost + calibrador, evaluado como una unidad |
| **Artefacto** | Archivo binario o JSON producido por el run (`rf.joblib`, `xgb.joblib`, `calibrator.joblib`) |
| **Manifiesto** | Documento JSON inmutable que describe identidad, datos, features, entrenamiento, validación, calibración y hashes |
| **Sello** | Acto de calcular `manifest.sha256`, publicar el directorio y registrar el evento `sealed` |
| **Ciclo de vida** | Secuencia append-only de estados: `sealed → validated → approved → deprecated/revoked` |
| **Aprobación** | Evento humano firmado que autoriza el uso del run para inferencia |
| **Cuarentena** | Artefactos legacy o fallidos que el loader no puede cargar |
| **run_fingerprint** | Hash de la intención de entrenamiento (datos, features, target, hiperparámetros, código, entorno, split), sin artefactos, timestamps ni `model_id` |

### 4.1 Grafo de dependencias (sin ciclos)

```text
dataset bytes ──sha256──► data.dataset_sha256
features code + params ─► features.definition_sha256
feature matrix + labels ─► features.matrix_sha256 / target.rule_sha256
intención completa ──────► run_fingerprint
rf/xgb/calibrator bytes ─► artifacts[].sha256
metrics.json bytes ──────► metrics.sha256
todos los campos ────────► manifest.json ──sha256──► manifest.sha256
manifest.sha256 ─────────► registry.lifecycle.jsonl
```

Ningún nodo se apunta a sí mismo. `metrics.json` **no** contiene el hash del manifiesto; el manifiesto contiene el hash de `metrics.json`. `manifest.sha256` es un archivo externo. El registro contiene el hash del manifiesto.

### 4.2 Ciclo de vida

```text
(reserva) → .staging → [sealed] → [validated] → [approved] → [deprecated]
                            │           │            │
                            └───────────┴────────────┴──► [revoked]
```

- `sealed`: publicado, íntegro, no aprobado. Cargable solo para auditoría/evaluación controlada.
- `validated`: un verificador independiente recalculó métricas y emitió un informe.
- `approved`: un humano autorizó explícitamente el uso para inferencia.
- `deprecated`: sigue siendo válido, pero ya no es la elección operativa.
- `revoked`: prohibido su uso; el loader lo rechaza incluso si los hashes son correctos.

---

## 5. Manifiesto v3

### 5.1 Estructura de primer nivel

| Campo | Tipo | Obligatorio | Regla |
|---|---|:---:|---|
| `schema_version` | string | Sí | Semver exacto `"3.0.0"`; el loader rechaza un major distinto |
| `model_id` | string | Sí | `^mdl_[0-9A-HJKMNP-TV-Z]{26}$`; único e inmutable |
| `created_at` | string | Sí | RFC 3339 UTC con microsegundos y sufijo `Z` |
| `sealed_at` | string | Sí | RFC 3339 UTC; `>= created_at` |
| `status_at_seal` | string | Sí | Solo `"sealed"`; el estado efectivo está en el registro |
| `run_fingerprint` | string | Sí | SHA-256 hex de 64 caracteres sobre la intención canónica |
| `git` | object | Sí | Código usado, no el commit que contendrá el manifiesto |
| `producer` | object | Sí | Herramienta, versión, comando y hash de configuración |
| `data` | object | Sí | Identidad del dataset y política de datos |
| `target` | object | Sí | Etiqueta, horizonte y orden de clases |
| `features` | object | Sí | Lista ordenada y hashes de definición/matriz |
| `training` | object | Sí | Algoritmos, hiperparámetros, entorno y determinismo |
| `validation` | object | Sí | Particiones, purga, leakage checks y método de evaluación |
| `calibration` | object | Sí | Vínculo verificable con el modelo base |
| `artifacts` | array | Sí | Exactamente un `rf`, un `xgb` y un `calibrator` |
| `metrics` | object | Sí | Referencia y hash de `metrics.json` |
| `extensions` | object | Sí | Espacio de nombres; `{}` si no se usa |

El esquema se implementará como JSON Schema 2020-12 con `additionalProperties: false` en todos los objetos. La única extensión permitida es `extensions`, con claves namespaced (`vendor.feature`) que el loader ignora pero incluye en el hash.

### 5.2 Identidad

| Campo | Tipo | Regla |
|---|---|---|
| `git.commit` | string | 40 hex; commit del código usado para entrenar |
| `git.dirty` | boolean | Debe ser `false` para sellar; un árbol sucio no puede publicarse |
| `git.branch` | string\|null | Informativo; no se usa para identidad |
| `git.tag` | string\|null | Informativo; no sustituye al commit |
| `git.source_bundle_sha256` | string | SHA-256 del bundle de fuentes y configuración usados |
| `producer.name` | string | `"tradingai-btc"` |
| `producer.version` | string | Versión de la aplicación |
| `producer.python` | string | Versión exacta de Python |
| `producer.command` | string | Comando reproducible; secretos redactados |
| `producer.config_sha256` | string | Hash del YAML efectivo, no del archivo con comentarios |

`run_fingerprint` se calcula sobre un objeto canónico de intención que **no** incluye `model_id`, timestamps, rutas de staging, hashes de artefactos ni métricas. Sirve para responder “¿este run intentó exactamente lo mismo que aquel?” y para detectar duplicados. Dos runs con el mismo fingerprint pueden producir artefactos distintos por no determinismo; eso se registra, no se oculta.

### 5.3 Datos

| Campo | Tipo | Regla |
|---|---|---|
| `data.symbol` | string | Formato `BASE/QUOTE`, p. ej. `BTC/USDT` |
| `data.timeframe` | string | Enum cerrado (`1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`) |
| `data.provider` | string | P. ej. `binance`; no se infiere del nombre del archivo |
| `data.provider_version` | string | Versión o fecha del adaptador de descarga |
| `data.dataset_sha256` | string | SHA-256 de los bytes del parquet original |
| `data.snapshot_uri` | string | URI interna al snapshot inmutable; nunca una ruta mutable de `data/raw` |
| `data.raw_rows` | integer | Filas OHLCV descargadas |
| `data.feature_rows` | integer | Filas tras features y `dropna` de features |
| `data.labeled_rows` | integer | Filas con etiqueta válida |
| `data.time_range.start` | string | RFC 3339 UTC del primer bar |
| `data.time_range.end` | string | RFC 3339 UTC del último bar |
| `data.time_range.timezone` | string | Siempre `"UTC"` |
| `data.missing_data_policy` | string | Enum: `drop_incomplete_bars`, `reject`, `explicit_gaps` |
| `data.gap_policy` | string | Enum: `no_synthetic_fill`, `documented_fill` |
| `data.ohlcv_schema_version` | string | Versión del contrato OHLCV |
| `data.alignment` | string | Enum: `left_closed_right_open`, `left_closed_left_open` |

El dataset debe existir en un almacén content-addressed (`data/store/sha256/<prefijo>/<hash>.parquet`) o en un snapshot inmutable equivalente. `dataset_sha256` por sí solo no impide que `data/raw` cambie; el snapshot sí.

### 5.4 Target y features

| Campo | Tipo | Regla |
|---|---|---|
| `target.name` | string | P. ej. `future_return_threshold` |
| `target.horizon_bars` | integer | `>= 1`; debe coincidir con la purga declarada |
| `target.vol_mult` | string | Decimal como string; prohibidos los floats en el manifiesto |
| `target.classes` | array[int] | Conjunto exacto de clases |
| `target.class_order` | array[int] | Orden posicional de las columnas de probabilidad |
| `target.rule_sha256` | string | Hash del código/regla de etiquetado |
| `target.nan_policy` | string | Enum: `drop_label`, `reject` |
| `features.ordered` | array[string] | Lista ordenada; el orden es parte del contrato |
| `features.count` | integer | Debe igualar `len(ordered)` y `n_features_in_` |
| `features.definition_sha256` | string | Hash de nombres + parámetros + código de features |
| `features.matrix_sha256` | string | SHA-256 de la matriz X canónica usada para entrenar |
| `features.pipeline_version` | string | Semver del pipeline de features |
| `features.code_sha256` | string | Hash del bundle de código de features |
| `features.parameters` | object | Ventanas, periodos y parámetros efectivos |
| `features.nan_policy` | string | Enum: `dropna_before_split`, `reject` |

`matrix_sha256` se calcula sobre una representación canónica de la matriz (orden de filas y columnas fijo, dtype fijo, sin NaN). Es la defensa más fuerte contra cambios silenciosos de features aunque el código no cambie.

### 5.5 Entrenamiento

| Campo | Tipo | Regla |
|---|---|---|
| `training.task` | string | `multiclass_classification` |
| `training.models.rf.library` | string | `scikit-learn` |
| `training.models.rf.version` | string | Versión exacta |
| `training.models.rf.params` | object | Hiperparámetros efectivos, no los del YAML con defaults implícitos |
| `training.models.xgb.library` | string | `xgboost` |
| `training.models.xgb.version` | string | Versión exacta |
| `training.models.xgb.params` | object | Hiperparámetros efectivos |
| `training.ensemble.method` | string | `mean_probability` |
| `training.ensemble.weights` | object | Decimales como strings |
| `training.seed` | integer | Semilla global |
| `training.environment` | object | Python, numpy, pandas, scikit-learn, xgboost, joblib, OS, arquitectura |
| `training.hardware.device` | string | `cpu` o `cuda`; el dispositivo efectivo, no el solicitado |
| `training.hardware.gpu_model` | string\|null | Modelo de GPU si aplica |
| `training.hardware.cuda_version` | string\|null | Versión de CUDA si aplica |
| `training.determinism.bitwise_reproducible` | boolean | Declaración medida, no asumida |
| `training.determinism.n_jobs` | integer | Debe ser `1` para runs canónicos |
| `training.determinism.omp_num_threads` | integer | Debe ser `1` para runs canónicos |
| `training.determinism.xgb_tree_method` | string | P. ej. `hist` |
| `training.determinism.xgb_deterministic_histogram` | boolean | Flag efectivo |
| `training.determinism.gpu_deterministic` | boolean | `false` si no se puede garantizar |

Regla: un run sellado no puede declarar `device: "cuda"` y `bitwise_reproducible: true` sin evidencia. Para el primer modelo canónico se recomienda CPU, `n_jobs=1`, `OMP_NUM_THREADS=1`.

### 5.6 Validación

| Campo | Tipo | Regla |
|---|---|---|
| `validation.split_method` | string | `chronological_holdout` o `walk_forward` |
| `validation.partitions.train` | object | Obligatorio |
| `validation.partitions.validation` | object | Obligatorio |
| `validation.partitions.calibration` | object | Obligatorio; puede compartir rango con validation |
| `validation.partitions.test` | object | Obligatorio |
| `partitions.*.row_start` | integer | Índice de fila etiquetada, inclusivo |
| `partitions.*.row_end` | integer | Exclusivo; `row_end > row_start` |
| `partitions.*.n_rows` | integer | `row_end - row_start` |
| `partitions.*.time_start` | string | RFC 3339 UTC |
| `partitions.*.time_end` | string | RFC 3339 UTC |
| `partitions.*.class_counts` | array[int] | Conteo por clase en el orden de `class_order` |
| `partitions.*.index_sha256` | string | Hash de la secuencia canónica `(fila, timestamp, etiqueta)` |
| `partitions.calibration.shared_with` | string\|null | `"validation"` si reutiliza la partición |
| `validation.purge.rows_between_partitions` | integer | Debe ser `>= horizon_bars` |
| `validation.purge.label_horizon_bars` | integer | Debe igualar `target.horizon_bars` |
| `validation.purge.label_purge_satisfied` | boolean | Calculado, no declarado a mano |
| `validation.purge.embargo_rows` | integer | `>= 0` |
| `validation.partition_manifest_sha256` | string | Hash del objeto `partitions` completo |
| `validation.leakage_checks.disjoint` | boolean | Verificado por el validador |
| `validation.leakage_checks.purge_satisfied` | boolean | Verificado por el validador |
| `validation.leakage_checks.labels_within_partition` | boolean | Verificado por el validador |
| `validation.evaluation.metric_spec_version` | string | Semver del esquema de métricas |
| `validation.evaluation.primary_metric` | string | P. ej. `macro_f1` |
| `validation.evaluation.test_evaluated_once` | boolean | Debe ser `true` para sellar |
| `validation.evaluation.evaluation_code_sha256` | string | Hash del código de evaluación |
| `validation.evaluation.evaluated_at` | string | RFC 3339 UTC |

Las particiones se expresan en coordenadas de fila etiquetada. Si el índice del DataFrame no es el rango por defecto, se añade `source_position_start`/`source_position_end`; el validador exige coherencia entre ambos sistemas. La partición de calibración debe ser exactamente la de validation o una anterior; nunca test.

### 5.7 Calibración

| Campo | Tipo | Regla |
|---|---|---|
| `calibration.mode` | string | `in_pipeline` o `external_run` |
| `calibration.base_model_id` | string | Igual a `model_id` si `mode=in_pipeline`; si no, un run aprobado |
| `calibration.base_artifact_sha256.rf` | string | Debe igualar el artefacto `rf` del manifiesto |
| `calibration.base_artifact_sha256.xgb` | string | Debe igualar el artefacto `xgb` del manifiesto |
| `calibration.method` | string | `sigmoid` o `isotonic` |
| `calibration.fit_partition` | string | `validation` (prohibido `test`) |
| `calibration.calibration_input_sha256` | string | Hash de `(proba_rf, proba_xgb, y, class_order)` usados para ajustar |
| `calibration.classes` | array[int] | Igual a `target.classes` |
| `calibration.class_order` | array[int] | Igual a `target.class_order` |
| `calibration.n_calibrators` | integer | Igual a `len(classes)` |
| `calibration.artifact_sha256` | string | Debe igualar el artefacto `calibrator` |

`base_model_id` es una **referencia**, no un hash del manifiesto; no genera ciclo. La igualdad `base_model_id == model_id` se verifica, no se asume.

### 5.8 Artefactos y métricas

| Campo | Tipo | Regla |
|---|---|---|
| `artifacts[].role` | string | Exactamente `rf`, `xgb`, `calibrator`; sin duplicados |
| `artifacts[].path` | string | Basename simple, sin `/`, `\` ni `..` |
| `artifacts[].sha256` | string | 64 hex |
| `artifacts[].bytes` | integer | `> 0`; debe igualar el tamaño real |
| `artifacts[].media_type` | string | `application/octet-stream` o `application/json` |
| `artifacts[].format` | string | `joblib-pickle` o `json` |
| `artifacts[].serializer` | string | Versión de joblib o del serializador |
| `metrics.path` | string | `metrics.json` |
| `metrics.sha256` | string | 64 hex |
| `metrics.schema_version` | string | Semver del esquema de métricas |

`metrics.json` contiene métricas por modelo y por partición. Cada entrada incluye el hash de los artefactos evaluados y el `index_sha256` de la partición, de modo que una métrica no puede trasladarse a otro run o a otra partición sin detectarse.

### 5.9 Ejemplo completo de manifiesto (ficticio)

> Todos los identificadores, hashes, fechas y métricas de este ejemplo son ficticios. No describen ningún artefacto real de `models/` ni ningún dataset existente.

```json
{
  "schema_version": "3.0.0",
  "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
  "created_at": "2026-11-25T18:00:00.000000Z",
  "sealed_at": "2026-11-25T18:04:12.345678Z",
  "status_at_seal": "sealed",
  "run_fingerprint": "2222222222222222222222222222222222222222222222222222222222222222",
  "git": {
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "dirty": false,
    "branch": "design/provenance-v3",
    "tag": null,
    "source_bundle_sha256": "3333333333333333333333333333333333333333333333333333333333333333"
  },
  "producer": {
    "name": "tradingai-btc",
    "version": "0.2.0",
    "python": "3.13.15",
    "command": "python -m tradingai.ml.train --config config/ml.yaml",
    "config_sha256": "4444444444444444444444444444444444444444444444444444444444444444"
  },
  "data": {
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "provider": "binance",
    "provider_version": "2026.11",
    "dataset_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "snapshot_uri": "data/store/sha256/01/0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef.parquet",
    "raw_rows": 4320,
    "feature_rows": 4287,
    "labeled_rows": 4262,
    "time_range": {
      "start": "2026-01-01T00:00:00Z",
      "end": "2026-06-27T13:00:00Z",
      "timezone": "UTC"
    },
    "missing_data_policy": "drop_incomplete_bars",
    "gap_policy": "no_synthetic_fill",
    "ohlcv_schema_version": "1.0.0",
    "alignment": "left_closed_right_open"
  },
  "target": {
    "name": "future_return_threshold",
    "horizon_bars": 5,
    "vol_mult": "0.5",
    "classes": [
      0,
      1,
      2
    ],
    "class_order": [
      0,
      1,
      2
    ],
    "rule_sha256": "7777777777777777777777777777777777777777777777777777777777777777",
    "nan_policy": "drop_label"
  },
  "features": {
    "ordered": [
      "feat_01",
      "feat_02",
      "feat_03",
      "feat_04",
      "feat_05",
      "feat_06",
      "feat_07",
      "feat_08",
      "feat_09",
      "feat_10",
      "feat_11",
      "feat_12",
      "feat_13",
      "feat_14",
      "feat_15",
      "feat_16",
      "feat_17",
      "feat_18",
      "feat_19",
      "feat_20",
      "feat_21"
    ],
    "count": 21,
    "definition_sha256": "5555555555555555555555555555555555555555555555555555555555555555",
    "matrix_sha256": "6666666666666666666666666666666666666666666666666666666666666666",
    "pipeline_version": "2.0.0",
    "code_sha256": "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd",
    "parameters": {
      "lookback_max": 50,
      "vol_window": 20,
      "rsi_period": 14
    },
    "nan_policy": "dropna_before_split"
  },
  "training": {
    "task": "multiclass_classification",
    "models": {
      "rf": {
        "library": "scikit-learn",
        "version": "1.9.1",
        "params": {
          "n_estimators": 200,
          "max_depth": 8,
          "class_weight": "balanced",
          "random_state": 42,
          "n_jobs": 1
        }
      },
      "xgb": {
        "library": "xgboost",
        "version": "3.4.1",
        "params": {
          "n_estimators": 200,
          "max_depth": 6,
          "learning_rate": 0.05,
          "subsample": 0.8,
          "colsample_bytree": 0.8,
          "random_state": 42
        }
      }
    },
    "ensemble": {
      "method": "mean_probability",
      "weights": {
        "rf": "0.5",
        "xgb": "0.5"
      }
    },
    "seed": 42,
    "environment": {
      "python": "3.13.15",
      "numpy": "2.5.5",
      "pandas": "3.1.1",
      "scikit_learn": "1.9.1",
      "xgboost": "3.4.1",
      "joblib": "1.6.0",
      "os": "Windows-11",
      "arch": "x86_64"
    },
    "hardware": {
      "device": "cpu",
      "gpu_model": null,
      "cuda_version": null,
      "cpu_count": 16,
      "ram_gb": 32
    },
    "determinism": {
      "bitwise_reproducible": true,
      "n_jobs": 1,
      "omp_num_threads": 1,
      "xgb_tree_method": "hist",
      "xgb_deterministic_histogram": true,
      "gpu_deterministic": false
    }
  },
  "validation": {
    "split_method": "chronological_holdout",
    "partitions": {
      "train": {
        "row_start": 0,
        "row_end": 2548,
        "n_rows": 2548,
        "time_start": "2026-01-01T00:00:00Z",
        "time_end": "2026-04-17T03:00:00Z",
        "class_counts": [
          1530,
          340,
          678
        ],
        "index_sha256": "8888888888888888888888888888888888888888888888888888888888888888"
      },
      "validation": {
        "row_start": 2553,
        "row_end": 3405,
        "n_rows": 852,
        "time_start": "2026-04-17T08:00:00Z",
        "time_end": "2026-05-22T19:00:00Z",
        "class_counts": [
          510,
          115,
          227
        ],
        "index_sha256": "9999999999999999999999999999999999999999999999999999999999999999"
      },
      "calibration": {
        "row_start": 2553,
        "row_end": 3405,
        "n_rows": 852,
        "time_start": "2026-04-17T08:00:00Z",
        "time_end": "2026-05-22T19:00:00Z",
        "class_counts": [
          510,
          115,
          227
        ],
        "index_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "shared_with": "validation"
      },
      "test": {
        "row_start": 3410,
        "row_end": 4262,
        "n_rows": 852,
        "time_start": "2026-05-23T00:00:00Z",
        "time_end": "2026-06-27T11:00:00Z",
        "class_counts": [
          520,
          118,
          214
        ],
        "index_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
      }
    },
    "purge": {
      "rows_between_partitions": 5,
      "label_horizon_bars": 5,
      "label_purge_satisfied": true,
      "embargo_rows": 0
    },
    "partition_manifest_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    "leakage_checks": {
      "disjoint": true,
      "purge_satisfied": true,
      "labels_within_partition": true
    },
    "evaluation": {
      "metric_spec_version": "1.0.0",
      "primary_metric": "macro_f1",
      "test_evaluated_once": true,
      "evaluation_code_sha256": "4545454545454545454545454545454545454545454545454545454545454545",
      "evaluated_at": "2026-11-25T18:03:50.000000Z"
    }
  },
  "calibration": {
    "mode": "in_pipeline",
    "base_model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
    "base_artifact_sha256": {
      "rf": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
      "xgb": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    },
    "method": "sigmoid",
    "fit_partition": "validation",
    "calibration_input_sha256": "a1b2c3d4e5f60718a1b2c3d4e5f60718a1b2c3d4e5f60718a1b2c3d4e5f60718",
    "classes": [
      0,
      1,
      2
    ],
    "class_order": [
      0,
      1,
      2
    ],
    "n_calibrators": 3,
    "artifact_sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
  },
  "artifacts": [
    {
      "role": "rf",
      "path": "rf.joblib",
      "sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
      "bytes": 248123,
      "media_type": "application/octet-stream",
      "format": "joblib-pickle",
      "serializer": "joblib-1.6.0"
    },
    {
      "role": "xgb",
      "path": "xgb.joblib",
      "sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
      "bytes": 259991,
      "media_type": "application/octet-stream",
      "format": "joblib-pickle",
      "serializer": "joblib-1.6.0"
    },
    {
      "role": "calibrator",
      "path": "calibrator.joblib",
      "sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
      "bytes": 1688,
      "media_type": "application/octet-stream",
      "format": "joblib-pickle",
      "serializer": "joblib-1.6.0"
    }
  ],
  "metrics": {
    "path": "metrics.json",
    "sha256": "1234123412341234123412341234123412341234123412341234123412341234",
    "schema_version": "1.0.0"
  },
  "extensions": {}
}
```

### 5.10 Ejemplo de `metrics.json` (ficticio)

```json
{
  "schema_version": "1.0.0",
  "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
  "metric_spec_version": "1.0.0",
  "generated_at": "2026-11-25T18:03:50.000000Z",
  "partitions": {
    "validation": {
      "partition_index_sha256": "9999999999999999999999999999999999999999999999999999999999999999",
      "n_samples": 852,
      "models": {
        "rf": {
          "artifacts": {
            "rf": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
          },
          "accuracy": 0.6479,
          "macro_f1": 0.6301,
          "log_loss": 0.8421,
          "brier": 0.2314,
          "ece": 0.0512,
          "confusion_matrix": [
            [
              240,
              70,
              40
            ],
            [
              60,
              160,
              35
            ],
            [
              45,
              50,
              152
            ]
          ]
        },
        "xgb": {
          "artifacts": {
            "xgb": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
          },
          "accuracy": 0.6655,
          "macro_f1": 0.6512,
          "log_loss": 0.771,
          "brier": 0.2088,
          "ece": 0.0431,
          "confusion_matrix": [
            [
              245,
              65,
              40
            ],
            [
              55,
              165,
              35
            ],
            [
              40,
              50,
              157
            ]
          ]
        },
        "calibrated_ensemble": {
          "artifacts": {
            "rf": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            "xgb": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "calibrator": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
          },
          "accuracy": 0.6725,
          "macro_f1": 0.6604,
          "log_loss": 0.7123,
          "brier": 0.1902,
          "ece": 0.0318,
          "confusion_matrix": [
            [
              250,
              65,
              35
            ],
            [
              56,
              165,
              34
            ],
            [
              41,
              48,
              158
            ]
          ]
        }
      },
      "class_counts": [
        350,
        255,
        247
      ]
    },
    "test": {
      "partition_index_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "n_samples": 852,
      "models": {
        "calibrated_ensemble": {
          "artifacts": {
            "rf": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
            "xgb": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "calibrator": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
          },
          "accuracy": 0.689,
          "macro_f1": 0.6712,
          "log_loss": 0.6844,
          "brier": 0.1781,
          "ece": 0.0287,
          "confusion_matrix": [
            [
              250,
              60,
              40
            ],
            [
              50,
              170,
              35
            ],
            [
              35,
              45,
              167
            ]
          ]
        }
      },
      "class_counts": [
        350,
        255,
        247
      ]
    }
  }
}
```

### 5.11 Serialización canónica y hash del manifiesto

**Reglas de canonicalización:**

1. UTF-8 sin BOM; solo JSON válido; prohibidos `NaN`, `Infinity` y claves duplicadas.
2. Claves ordenadas por punto de código Unicode; separadores `,` y `:` sin espacios.
3. Sin floats en el manifiesto: los decimales se representan como strings (`"0.5"`), los conteos como enteros.
4. El archivo termina con exactamente un `\n`.
5. `manifest.sha256` es el SHA-256 de **los bytes exactos del archivo**, incluido el `\n` final. No se recalcula serializando de nuevo: se verifica sobre los bytes leídos.
6. `run_fingerprint` se calcula sobre un subconjunto canónico de intención, con las mismas reglas, sin `model_id`, timestamps ni artefactos.

**Evitación de referencia circular:**

- `manifest.json` contiene hashes de `rf`, `xgb`, `calibrator` y `metrics.json`.
- `metrics.json` contiene `model_id`, hashes de artefactos e `index_sha256`, pero **no** el hash del manifiesto.
- `manifest.sha256` es un archivo separado con el hash del manifiesto; no se incluye dentro de él.
- `registry/lifecycle.jsonl` registra `(model_id, manifest_sha256, evento)`.
- La firma, si existe, cubre los bytes del manifiesto o el contenido de `manifest.sha256`.

Alternativa rechazada: incluir un campo `manifest_sha256` y excluirlo del cálculo. Es frágil, difícil de auditar y fácil de implementar mal. El hash desacoplado es explícito y verificable con herramientas estándar.

---

## 6. Invariantes

### 6.1 Invariantes obligatorios

| ID | Invariante | Dónde se impone | Prueba |
|---|---|---|---|
| **I1** | Un `model_id` identifica una única ejecución y no se reutiliza | Reserva con lock + `mkdir` exclusivo + registro | U03, I10 |
| **I2** | Un artefacto no puede cambiar de contenido conservando el mismo identificador | Directorio inmutable + hashes + loader | U04, I02, I10 |
| **I3** | El calibrador pertenece exactamente al modelo base declarado | `base_model_id`, hashes base e `calibration_input_sha256` | I05, U08 |
| **I4** | Los hashes se verifican antes de cualquier deserialización | Loader: bytes en memoria → hash → recién después `joblib.load` | S01, I15 |
| **I5** | El loader rechaza archivos faltantes, hashes incorrectos e incompatibilidades | Loader fail-closed con códigos de error | I02-I04, I12 |
| **I6** | Las métricas están vinculadas a dataset, partición y modelo evaluado | `metrics.json` + `index_sha256` + hash de artefactos | U08, I13 |
| **I7** | No se declara validado un modelo con metadatos obligatorios ausentes | Validador de schema e invariantes | U01, I03 |
| **I8** | Un modelo experimental no se convierte automáticamente en aprobado | Ciclo de vida separado; aprobación humana firmada | U07, I14 |
| **I9** | No se sobrescribe una ejecución existente | Publicación con renombrado y comprobación de existencia | I10 |
| **I10** | Un manifiesto inválido nunca produce aprobación implícita | Default deny; estado ausente = rechazo | U01, S06 |
| **I11** | Ninguna ruta de artefacto sale del directorio del run | `path` es basename; `resolve()` confinado; sin symlinks | S02, S03 |
| **I12** | El dataset usado es un snapshot inmutable | `snapshot_uri` content-addressed + `dataset_sha256` | I07 |
| **I13** | La partición de test se evalúa una sola vez para el informe final | `test_evaluated_once` + revisión del verificador | V04 |
| **I14** | El orden de clases es único y consistente | `class_order` repetido en target, calibración y métricas | U08, V06 |
| **I15** | Un entorno incompatible no puede cargar el artefacto | Política de versiones del loader | I04, U09 |
| **I16** | Un árbol Git sucio no puede sellarse | `git.dirty == false` obligatorio para publicar | I03 |
| **I17** | El manifiesto no contiene su propio hash | `manifest.sha256` desacoplado | U02 |
| **I18** | Ningún campo del manifiesto puede aprobar por sí mismo | `approved` solo por evento externo firmado | U07, S06 |

### 6.2 Integridad, autenticidad, reproducibilidad y validez estadística

Estas cuatro propiedades son **independientes**. El contrato las registra por separado y el loader no las confunde.

| Propiedad | Pregunta que responde | Evidencia | Lo que **no** prueba | Control |
|---|---|---|---|---|
| **Integridad** | ¿Los bytes son exactamente los registrados? | SHA-256 de artefactos, métricas y manifiesto | Quién los creó, si son seguros o si son buenos | Hashes + manifiesto inmutable |
| **Autenticidad** | ¿Quién produjo y aprobó este run? | Firma Ed25519, clave pública fuera del repo, aprobación firmada | Que el modelo sea estadísticamente válido | Firma + registro + control de acceso |
| **Reproducibilidad** | ¿Puede recrearse el mismo resultado con las mismas entradas? | `run_fingerprint`, entorno, flags de determinismo, comparación de re-ejecuciones | Que el resultado sea correcto o generalizable | Entorno fijado + CPU + semillas + comparación |
| **Validez estadística** | ¿El rendimiento fuera de muestra es creíble? | Particiones purgadas, test no usado en selección, métricas, intervalos de confianza | Que los bytes no hayan cambiado ni quién los hizo | Diseño experimental + verificación independiente |

**Ejemplos de confusión prohibida:**

- Un modelo con hash correcto entrenado con leakage tiene **integridad** pero **no validez**.
- Un modelo firmado por el autor con accuracy pésima tiene **autenticidad** pero **no validez**.
- Un modelo reproducible al bit que sobreajusta tiene **reproducibilidad** pero **no validez**.
- Un modelo con excelentes métricas en un JSON no verificable tiene **apariencia de validez** pero **ni integridad ni autenticidad**.

### 6.3 Qué demuestra cada control

| Control | Demuestra | No demuestra |
|---|---|---|
| SHA-256 del artefacto | Que el archivo coincide con el hash del manifiesto | Que el manifiesto sea legítimo |
| SHA-256 del manifiesto | Que el manifiesto coincide con el hash registrado | Que el registro sea legítimo |
| Firma del manifiesto | Que quien firmó poseía la clave privada | Que el modelo sea bueno |
| Commit Git | Qué código se declaró usar | Que el artefacto haya sido producido por ese código |
| `run_fingerprint` | Que dos runs declararon la misma intención | Que los resultados sean idénticos |
| Métricas verificadas | Que el cálculo se reprodujo sobre el snapshot | Que el modelo generalice a datos futuros |

---

## 7. Estructura de almacenamiento

### 7.1 Layout propuesto

```text
models/
  QUARANTINE.md                  # existente, no se modifica
  QUARANTINE.sha256              # existente, no se modifica
  _t7/ _t8/ _t9/ _test/ _testcal/  # legacy, intactos
  runs/
    <model_id>/
      manifest.json
      manifest.sha256
      manifest.sig               # opcional; obligatorio para approved
      rf.joblib
      xgb.joblib
      calibrator.joblib
      metrics.json
  .staging/
    <model_id>.<nonce>/
  .failed/
    <model_id>.<nonce>/
      failure.json
  .locks/
    <model_id>.lock
  registry/
    lifecycle.jsonl
    index.json                   # derivado, reconstruible
    approvals/
      <model_id>.json            # aprobación firmada
```

Reglas de la raíz:

- `models/` no contiene `rf.joblib`, `xgb.joblib`, `calibrator.json` ni ningún modelo activo con nombre genérico.
- `models/runs/` contiene únicamente runs sellados.
- `models/.staging/`, `models/.failed/` y `models/.locks/` son internos y no se sirven.
- El legacy permanece donde está; no se mueve ni se renombra en esta fase.

### 7.2 Convenciones de nombres

| Elemento | Convención |
|---|---|
| `model_id` | `mdl_` + ULID de 26 caracteres Crockford Base32 |
| Directorio del run | Exactamente `models/runs/<model_id>/` |
| Artefactos | Nombres fijos: `rf.joblib`, `xgb.joblib`, `calibrator.joblib` |
| Métricas | `metrics.json` |
| Manifiesto | `manifest.json` + `manifest.sha256` (+ `manifest.sig`) |
| Staging | `models/.staging/<model_id>.<pid>.<8hex>/` |
| Fallido | `models/.failed/<model_id>.<pid>.<8hex>/` |

No se usan símbolo, timeframe ni alias en la ruta. Esos datos viven en el manifiesto. Un alias legible puede existir en `registry/index.json`, pero el loader nunca lo acepta como identidad.

El ULID aporta orden temporal aproximado y 80 bits de aleatoriedad; la unicidad real se impone con la reserva exclusiva, no con la probabilidad.

### 7.3 Inmutabilidad

1. Un run publicado es de solo lectura para el writer. En Windows se aplican ACL best-effort; en POSIX, modo `0444` para archivos y `0555` para el directorio.
2. La inmutabilidad primaria no depende de permisos: el publisher se niega a escribir en un directorio existente y el loader verifica hashes.
3. `manifest.json` no se edita nunca. Cambiar cualquier campo, incluido el estado, exige un run nuevo.
4. El estado efectivo vive en `registry/lifecycle.jsonl`, que es append-only.
5. Una corrección de metadatos no se hace “in place”: se crea un run nuevo con `supersedes: <model_id>` en `extensions` o en el registro.

### 7.4 Protocolo de escritura

**Precondiciones**

1. Árbol Git limpio (`git.dirty == false`); en caso contrario, abortar antes de entrenar.
2. Dataset resuelto a un snapshot content-addressed y verificado contra `dataset_sha256`.
3. Configuración efectiva serializada y hasheada; sin defaults implícitos sin registrar.
4. `models/runs/` y `models/.staging/` en el mismo volumen.

**Pasos**

| Paso | Acción | Fallo |
|---:|---|---|
| 1 | Generar `model_id` (ULID) y `created_at` | Abortar |
| 2 | Crear `models/.locks/<model_id>.lock` con `O_CREAT|O_EXCL` | Si existe, regenerar ID o abortar |
| 3 | Crear `models/.staging/<model_id>.<nonce>/` | Abortar y liberar lock |
| 4 | Entrenar y calibrar en memoria | Mover staging a `.failed` con `failure.json` |
| 5 | Escribir `rf.joblib`, `xgb.joblib`, `calibrator.joblib` con nombres temporales internos; `flush` + `fsync` | Mover a `.failed` |
| 6 | Calcular SHA-256 y tamaño de cada artefacto desde los bytes escritos | Mover a `.failed` |
| 7 | Escribir `metrics.json`; calcular su hash | Mover a `.failed` |
| 8 | Construir `run_fingerprint` y `manifest.json`; serializar canónicamente | Mover a `.failed` |
| 9 | Validar schema, invariantes, particiones, clases y coherencia de hashes | Mover a `.failed` |
| 10 | Escribir `manifest.sha256`; `fsync` de archivos y directorio (POSIX) | Mover a `.failed` |
| 11 | Publicar: comprobar que `models/runs/<model_id>` no existe y renombrar staging → final | Si existe, abortar sin tocar el run previo |
| 12 | Añadir evento `sealed` a `lifecycle.jsonl` con `manifest_sha256`; `fsync` | Run queda publicado pero no registrado; recuperación obligatoria |
| 13 | Actualizar `registry/index.json` (derivado); liberar lock | Reintentar; el índice se puede reconstruir |

**Invariante de fallo:** antes del paso 11 no existe nada visible en `models/runs/`. Entre 11 y 12 existe un run íntegro pero no registrado; el loader lo rechaza hasta que la recuperación añada el evento `sealed`. Nunca se publica un run parcial.

### 7.5 Publicación atómica y plataformas

- El renombrado de directorio dentro del mismo volumen es atómico en POSIX y en Windows (`MoveFileEx` sin reemplazo).
- En POSIX se usa `renameat2(RENAME_NOREPLACE)` cuando está disponible; si no, se comprueba la ausencia del destino y se documenta la ventana de carrera, mitigada por el lock.
- En Windows, `os.rename` falla si el destino existe; esa propiedad se usa a favor.
- `fsync` de directorio no está disponible en Windows; se documenta como limitación y se compensa con la verificación de hashes al cargar.
- No se publica a través de una unidad de red ni de una carpeta sincronizada (OneDrive, Dropbox); el renombrado y los locks no son fiables allí.

### 7.6 Runs incompletos y fallidos

| Situación | Tratamiento | Visible para el loader |
|---|---|---|
| Fallo antes del paso 11 | Staging movido a `.failed/<id>.<nonce>/` con `failure.json` | No |
| Fallo entre 11 y 12 | Run íntegro sin evento `sealed`; job de recuperación verifica y registra | No hasta registrar |
| Fallo después de 12 | Run completo; el índice se reconstruye | Sí |
| Staging huérfano > 24 h | Movido a `.failed` con motivo `orphaned_staging` | No |
| `failure.json` ausente o corrupto | Se conserva; se marca `unclassified_failure` | No |

`failure.json` contiene `model_id`, `stage`, `error_class`, `message` redactado, `at` y `manifest_sha256` si llegó a existir. Los fallidos se conservan 30 días por defecto, configurables; **nunca se auto-eliminan runs sellados, validados o aprobados**.

### 7.7 Colisiones y concurrencia

- La reserva del `model_id` es exclusiva: lock `O_EXCL` + comprobación de directorio.
- Dos procesos con el mismo `run_fingerprint` pueden producir dos runs distintos; el registro marca `duplicate_of` y exige justificación, pero no bloquea.
- El writer no soporta múltiples escritores concurrentes al mismo `model_id`; el lock lo impide.
- La publicación nunca reemplaza; si el destino existe, se aborta y se conserva el original.
- El índice derivado puede regenerarse desde `lifecycle.jsonl`; nunca es la fuente de verdad.



### 7.8 Registro de ciclo de vida

`models/registry/lifecycle.jsonl` es un registro append-only, una l?nea JSON por evento, que registra la historia completa del ciclo de vida de cada run identificado por `model_id`. El registro sirve como fuente de verdad para la verificaci?n de estado, autenticidad y recuperaci?n ante fallos.

#### 7.8.1 Arquitectura de la cadena de eventos

El registro utiliza una **cadena de eventos monot?nica por model_id**. Cada `model_id` tiene su propia cadena independiente; no hay una cadena global ?nica que abarque todos los modelos. Esto evita la confusi?n entre secuencia global y secuencia por modelo, y permite que la verificaci?n sea escalable y decidible.

**Secuencia:** El `sequence_number` es monot?nico y empieza en 1 para cada `model_id`. Cada nuevo evento appended incrementa el `sequence_number` en 1 respecto al evento anterior para ese mismo `model_id`. No hay brechas permitidas: si el ?ltimo evento tiene `sequence_number = N`, el pr?ximo debe tener `sequence_number = N+1`.

**Cadena de hashes:** Cada evento encadena al anterior mediante `previous_event_sha256`, que es el SHA-256 hex de 64 caracteres de la canonicalizaci?n completa del evento anterior. El primer evento de un `model_id` tiene `previous_event_sha256 = "0"*64`.

**Evento ?nico:** Cada evento debe tener un `event_id` ?nico (formato `evt_` + ULID). La duplicaci?n de `event_id` en la cadena para el mismo `model_id` es una violaci?n grave y debe provocar el rechazo de la carga.

#### 7.8.2 Canonicalizaci?n RFC 8785 (JKCS)

La canonicalizaci?n de cada evento para los prop?sitos de `event_sha256` y `previous_event_sha256` sigue el **JSON Canonicalization Scheme (RFC 8785)** adaptado para este contexto. Este esquema garantiza que la misma estructura de datos siempre produzca la misma representaci?n binaria, independientemente de la plataforma o lenguaje empleado.

**Regules de canonicalizaci?n:**

1. **Codificaci?n:** UTF-8 sin BOM.
2. **Estructura del documento:** El evento se representa como un objeto JSON con los campos en el orden can?nico especificado a continuaci?n. Se proh?ben las claves duplicadas.
3. **Tipos de datos:**
   - **N?meros enteros:** Se serializan como n?meros enteros JSON sin cifrado leading zero (excepto el cero mismo: `0`), ni espacios innecesarios. Ejemplo: `42`, no `042` ni ` 42`.
   - **N?meros de punto flotante:** No est?n permitidos en el evento. Si se requiere un n?mero real, debe convertirse a una representaci?n de fixed-point (entero) con precisi?n documentada, o excluirse.
   - **Strings:** Se codifican como cadenas JSON UTF-8 sin BOM. Los caracteres especiales deben escaparse seg?n la especificaci?n JSON est?ndar (RFC 8259). No se permite la inclusi?n de l?neas enteras sin procesar.
   - **null:** Se representa como el literal JSON `null` (cuatro letras min?sculas, sin comillas circundantes).
4. **Orden de campos can?nico:** Los campos aparecen en el siguiente orden obligatorio. Este orden es parte integral de la canonicalizaci?n; cambiar el orden produce una cadena diferente.
   `sequence_number`, `previous_event_sha256`, `event_id`, `model_id`, `event`, `at`, `manifest_sha256`, `actor`, `evidence`.
5. **Separadores:** Los separadores de objeto y elementos deben ser `,` (coma) y `:` (dos puntos) seg?n el est?ndar JSON, sin espacios adicionales alrededor de los separadores en la representaci?n can?nica (esto es consistente con la canonicalizaci?n RFC 8785 Level 1).
6. **Evidence serializaci?n:**
   - Si `evidence` es `null`, se representa como la palabra `null` en la posici?n can?nica.
   - Si `evidence` es un objeto JSON, debe serializarse usando la canonicalizaci?n JSON RFC 8785 recursivamente (mismo orden de campos, mismos separadores, sin espacio despu?s de los dos puntos ni antes de las comas).
   - No se permiten valores `NaN` o `Infinity` en ning?n nivel del objeto `evidence`.
7. **Exclusi?n del propio `event_sha256`:** El campo `event_sha256` **no forma parte** de la string que se hashea para producir itself. La canonicalizaci?n se calcula sobre los 9 campos enumerados en el paso 4, sin incluir `event_sha256`. Esto evita el ciclo circular y es consistente con la dise?o del contrato.

**Procedimiento de canonicalizaci?n paso a paso:**

1. Tomar el objeto evento con sus 9 campos en el orden can?nico.
2. Serializar el objeto a JSON usando las reglas de la regla 4 (orden de campos, sin espacios despu?s de `:` ni antes de `,`, sin BOM, UTF-8).
3. Si `evidence` no es `null`, reemplazar el valor del campo `evidence` por la serializaci?ncan?nica recursiva del objeto `evidence` (mismo proceso recursivo).
4. El resultado es una string UTF-8.
5. Calcular `event_sha256 = SHA-256(canonical_string)`.
6. Para el evento N>1, calcular `previous_event_sha256 = SHA-256(canonical_string_del_evento_anterior)`. Para el evento 1, `previous_event_sha256 = "0"*64`.

#### 7.8.3 Verificaci?n de la cadena de eventos

El loader (o cualquier verificador) debe verificar la cadena de la siguiente manera para cada `model_id`:

1. **Leer todos los eventos** para ese `model_id` del `lifecycle.jsonl`, ordenados por `sequence_number` (que debe ser estrictamente creciente).
2. **Verificar el evento 1:**
   - Confirmar que `sequence_number == 1`.
   - Confirmar que `previous_event_sha256 == "0"*64`.
   - Calcular `event_sha256` usando la canonicalizaci?n RFC 8785 y comparar con el valor declarado.
3. **Para cada evento subsiguiente (N > 1):**
   - Confirmar que `sequence_number == previous.sequence_number + 1`, i.e., la secuencia incrementa en exactamente 1 respecto al evento anterior sin saltos.
   - Confirmar que `previous_event_sha256` coincide con el `event_sha256` calculado del evento anterior.
   - Calcular `event_sha256` y comparar con el valor declarado.
4. **Si en cualquier punto la cadena se rompe** (hash mismatch, sequence gap, evento duplicado, event_id duplicado), el loader debe:
   - **Rechazar la carga** de ese run con c?digo de error `E_CHAIN_BROKEN`.
   - **No intentes reordenar ni "reparar" la cadena autom?ticamente.**
   - **Registrar el evento de fallo** para auditor?a, pero no continuar en un estado de incertidumbre.

#### 7.8.4 Detecci?n de ataques y integridad del registro

| Ataque | Detecci?n | Acci?n del loader |
|---|---|---|
| **Truncamiento** (eliminaci?n de eventos finales) | Una cadena local **no puede detectar por s? sola** la eliminaci?n de su propia cola. La ?nica defensa es un **anclaje externo** (ver ?7.8.6). Si se sospecha truncamiento (por ejemplo, el run esperaba m?s eventos pero el registro se detuvo), y no hay anclaje externo v?lido, el loader debe cambiar al modo *integrity-only*. | Modo integrity-only: sin deserializaci?n `approved`/`validated`. Permitir solo `audit` con verificaci?n de hashes. |
| **Eliminaci?n de eventos del medio** | Si `sequence_number` salta de N a M donde M > N+1, se detecta brecha. | Rechazar con `E_CHAIN_BROKEN`. |
| **Sustituci?n de evento** | Si el `event_sha256` calculado no coincide con el declarado, o el `previous_event_sha256` no coincide con el `event_sha256` del anterior. | Rechazar con `E_CHAIN_BROKEN`. |
| **Reordenamiento** | Si los `sequence_number` no son estrictamente crecientes despu?s de ordenar por `at` (marca de tiempo). | Rechazar con `E_CHAIN_BROKEN`. No reordenar autom?ticamente. |
| **Duplicados de `sequence_number`** | Si dos eventos tienen el mismo `sequence_number` para el mismo `model_id`. | Rechazar ambos eventos con `E_CHAIN_DUPLICATE`. |
| **Duplicados de `event_id`** | Si dos eventos tienen el mismo `event_id` para el mismo `model_id`. | Rechazar ambos eventos con `E_EVENT_ID_DUPLICATE`. |
| **Falsificaci?n de `previous_event_sha256`** | Si el `previous_event_sha256` no es el hash del evento anterior calculado canonicalmente. | Rechazar con `E_CHAIN_BROKEN`. |

#### 7.8.5 Recuperaci?n ante cadena rota

Si el loader detecta que la cadena de eventos est? rota (cualquier violaci?n de las reglas de la secci?n 7.8.4):

1. **No deserializar** el run con fines de `inference` o `evaluation` que requieran confianza en la procedencia.
2. Permitir **inspecci?n de solo metadata** (`audit` purpose) si los hashes de artefactos y el manifiesto son v?lidos, aunque la cadena de eventos no sea verificable.
3. **Registrar** el fallo de verificaci?n con:
   - `model_id`
   - `sequence_number` donde se rompi? la cadena
   - `error_code` (`E_CHAIN_BROKEN`)
   - `acci?n` ("rechazado", "modo integrity-only")
4. **No generar eventos compensatorios** ni "reparar" la cadena automaticamente. La recuperaci?n requiere revisi?n expl?cita por parte de un operador humano con acceso al anclaje externo.

#### 7.8.6 Anclaje externo del ?ltimo hash conocido

Una cadena de hashes local **no puede detectar por s? sola** la eliminaci?n de eventos de su propia cola final, ni puede garantizar que el evento m?s reciente sea el "?ltimo verdadero" sin un mecanismo de externalidad.

**Mecanismo de anclaje externo:**

- Cada vez que se agrega un nuevo evento al `lifecycle.jsonl`, su `event_sha256` debe **anclarse** (registrarse) en un almac?n de confianza externo. Las opciones incluyen:
  - Una transacci?n en un **Git firmado** del repositorio can?nico (el commit que contiene el `lifecycle.jsonl` actualizado).
  - Un **registro Merkle root** en un servicio de tiempo distribuido (e.g., AWS Quantum Ledger Database, o servicios equivalentes).
  - Un **hash grabado en un almac?n WORM** (Write Once Read Many) de alta disponibilidad.
  - Una **firma digital** del evento m?s reciente por una clave fuera del control del pipeline (clave privada fuera del repositorio, en un HSM o keychain del sistema operativo).

- El propio `lifecycle.jsonl` **no puede ser** la fuente de anclaje externo (evita el ciclo circular).

- Si el anclaje externo no est? disponible en un momento dado, el loader debe operar en **modo integrity-only**:
  - **No deserializar** runs con estado `approved` o `validated` para `inference` o `evaluation`.
  - Permitir **solo `audit` purpose** con verificaci?n de hashes de artefactos y manifiesto.
  - Registrar el evento con c?digo `E_ANCHOR_UNAVAILABLE`.

- El anclaje externo debe actualizarse **cada vez** que se agrega un nuevo evento. La frecuencia de actualizaci?n y el m?todo espec?fico son decisiones de pol?tica operativa, pero la regla fundamental es: **ning?n nuevo evento debe agregarse al registro sin que su `event_sha256` sea anclado externamente** (o el sistema opere en modo conservativo `integrity-only` hasta que el anclaje se restablezca).

#### 7.8.7 Pol?tica ante eventos duplicados o fuera de orden

**Reglas obligatorias (sin excepciones):**

1. **Un `sequence_number` duplicado** para el mismo `model_id` implica **rechazo inmediato**. No se selecciona "el m?s reciente por timestamp" ni "el de mayor entrop?a". Ambos eventos son inv?lidos y el loader debe rechazarlos con `E_CHAIN_DUPLICATE`.

2. **Un `event_id` duplicado** para el mismo `model_id` implica **rechazo inmediato**. Tanto si los `sequence_number` son diferentes como si son iguales, la duplicaci?n de `event_id` invalida la carga.

3. **Un evento fuera de orden** (i.e., despu?s de leer todos los eventos para un `model_id`, ordenarlos por `sequence_number` revela que un evento tiene un `sequence_number` que no es exactamente 1 m?s que el precedente) implica **rechazo inmediato** con `E_CHAIN_BROKEN`.

4. **No reordenar autom?ticamente** el registro. El orden de inserci?n es el orden l?gico. Las marcas de tiempo `at` se registran para referencia, pero no desplazan la secuencia `sequence_number`.

5. **No descartar ni sustituir eventos autom?ticamente.** Si un evento falta (brecha en la secuencia), el loader debe rechazar la cadena, no llenar el hueco con un evento imaginario.

6. **No crear eventos compensatorios** para ocultar corrupci?n. No se permite a?adir eventos `revoked` o `superseded` para "arreglar" una cadena rota. La corrupci?n debe reportarse tal como se detect?.

7. **La recuperaci?n debe requerir revisi?n expl?cita y evidencia verificable.** Si la cadena est? rota, un operador humano debe:
   - Verificar el anclaje externo m?s reciente.
   - Determinar si los eventos faltantes fueron intencionales o por error.
   - Decidir si el run puede operar en modo `integrity-only` o debe rechazarse completamente.
   - **Ninguna de estas decisiones puede ser autom?tica** ni tomada por el loader.

**Regla transversal:** cualquier violaci?n de estas reglas implica rechazo de la carga con c?digo de error `E_CHAIN_POLICY_VIOLATION`, y el loader debe cambiar al modo *integrity-only* hasta que se resuelva la discrepancia mediante revisi?n humana con anclaje externo.
### 8.1 Contrato

```text
load_model(model_id: str, purpose: Literal["inference","evaluation","audit"],
           expected_manifest_sha256: str | None = None) -> LoadedModel
```

`LoadedModel` contiene el ensemble reconstruido y una `ModelIdentity` inmutable con `model_id`, `manifest_sha256`, hashes de artefactos, estado efectivo y `purpose`. Nunca se devuelve un objeto parcial.

Cualquier fallo lanza `ModelLoadError(code, model_id, detail)`; no hay valor por defecto, no hay fallback a “el último modelo”, no hay búsqueda por nombre.

### 8.2 Flujo de carga

| Paso | Acción | Rechazo |
|---:|---|---|
| 1 | Validar `model_id` contra `^mdl_[0-9A-HJKMNP-TV-Z]{26}$` | `E_ID_INVALID` |
| 2 | Resolver `models/runs/<model_id>`; `realpath`; confinar al `runs_root`; rechazar symlinks, junctions y reparse points | `E_PATH_ESCAPE` |
| 3 | Leer `manifest.json` con límite de tamaño (2 MiB) y profundidad; parsear sin claves duplicadas ni `NaN` | `E_MANIFEST_PARSE` |
| 4 | Validar JSON Schema y `schema_version` soportado | `E_SCHEMA_UNSUPPORTED` |
| 5 | Leer `manifest.sha256`; comparar con los bytes exactos del manifiesto; contrastar con el evento `sealed` del registro; verificar `manifest.sig` si el estado lo exige | `E_MANIFEST_HASH`, `E_SIGNATURE` |
| 6 | Obtener el estado efectivo del registro y aplicar la política de `purpose` | `E_STATUS_DENIED` |
| 7 | Para cada artefacto y para `metrics.json`: verificar basename, existencia, tipo regular, tamaño y SHA-256; leer los bytes una sola vez en memoria (con límite) | `E_ARTIFACT_MISSING`, `E_ARTIFACT_SIZE`, `E_ARTIFACT_HASH` |
| 8 | Verificar coherencia: `features.count`, orden y `definition_sha256`; `class_order` en target/calibración/métricas; `base_model_id` y hashes base; `calibration_input_sha256`; versiones compatibles; `git.dirty == false` | `E_FEATURE_MISMATCH`, `E_CLASS_ORDER`, `E_CALIBRATION_BINDING`, `E_VERSION_INCOMPATIBLE` |
| 9 | Verificar que cada métrica referencia el hash del artefacto evaluado y el `index_sha256` de su partición | `E_METRICS_BINDING` |
| 10 | Recién ahora deserializar **desde los bytes en memoria**; reconstruir el ensemble; comprobar `n_features_in_`, `classes_` y que el calibrador transforme correctamente una sonda; registrar la identidad usada | `E_DESERIALIZE`, `E_POST_LOAD_CHECK` |

La deserialización ocurre una sola vez y sobre el mismo buffer que se hasheó. No se vuelve a abrir la ruta después del paso 7.

### 8.3 Política de estado por propósito

La deserialización solo está permitida cuando la cadena de ciclo de vida y la autenticidad del manifiesto son verificables. La política por propósito es la siguiente:

| Estado efectivo | `inference` | `evaluation` | `audit` (solo metadata) |
|---|:---:|:---:|:---:|
| `sealed` | **No recomendado** para inferencia producción. Solo para auditoría/evaluación controlada si no hay firma válida. | **No** para evaluación formal. Puede usarse con verificación de integridad manual. | **Sí** — solo metadata, sin deserializar el payload. |
| `validated` | **No** para inferencia. Solo con autorización del verificador que emitió el informe firmado y anclaje externo válido. | **Sí** — con informe de re-evaluación firmado, cadena de ciclo de vida verificada y `manifest.sig` verificado. | **Sí** — metadata + verificación de integridad. |
| `approved` | **No** sin firma Ed25519 válida y cadena de eventos verificada. | **No** sin cadena de ciclo de vida verificada y anclaje externo. | **Sí** — solo con firma Ed25519 válida en `manifest.sig`, evento `approved` firmado en el registro, cadena verificada y estado vigente (sin caducidad). |
| `deprecated` | **No**. Requiere run sustituto `approved`. | **No**. Usar run sustituto. | **Sí** — metadata, sin deserializar. |
| `revoked` | **No**. Prohibido su uso incluso si los hashes son correctos. | **No**. Prohibido. | **Solo forense** — con autorización administrativa. |
| `rejected` | **No**. | **No**. | **No**. |
| Ausente o desconocido | **No**. | **No**. | **No**. |

#### Límites y advertencias adicionales

- **Firma no disponible:** Si no hay clave Ed25519 privada para verificar `manifest.sig` y los eventos `approved` en el registro, el sistema debe limitarse a modo *integrity-only*: los hashes de artefactos y el manifiesto pueden verificarse, pero **nunca** se permite la deserialización para `inference` o `evaluation` con fines de confianza. Solo `audit` purpose con inspección de metadatos está permitido.

- **Registro manipulado o sin anclaje externo:** Si el `lifecycle.jsonl` no puede verificarse (cadena rota, eventos faltantes, sin firma Ed25519 en eventos `approved`, o sin anclaje externo confiable), el loader debe:
  1. **No deserializar** ningún run con estado `approved` o `validated` para inferencia o evaluación.
  2. Permitir inspección de solo metadata (`audit`) de runs `sealed` si los hashes de artefactos y el manifiesto son válidos.
  3. Registrar el fallo con código de error `E_CHAIN_UNAVAILABLE` y continuar en modo *integrity-only*.

- **Confusión de firma con seguridad del pickle:** Una firma Ed25519 válida autentica el origen del run, pero **no** garantiza que el contenido del pickle sea seguro. La firma forma parte de un plan de migración futura a un formato de inferencia más seguro (ONNX o equivalente). Mantener el aislamiento del proceso de carga (mínimos privilegios, sandbox, límites de memoria/tiempo) sigue siendo obligatorio independientemente de la firma.

- **Corrida entre verificación y deserialización (TOCTOU):** El loader debe usar el buffer único verificado en los pasos 7-9 (hashes, estado, coherencia) y **nunca** volver a abrir la ruta del archivo para `joblib.load`. La deserialización debe ocurrir exclusivamente sobre los bytes ya leídos y cuya integridad fue comprobada.

- **Carga de runs `sealed` sin firma:** Un run `sealed` (sin evento `approved` en el registro) puede cargarse con propósito `audit` para inspección de metadatos y verificación de hashes, pero **no** para inferencia ni evaluación formal. Si se necesita inferencia, el run debe promocionarse a `validated` o `approved` mediante los flujos correspondientes.

### 8.6 Autenticidad de los eventos validated y approved

**Definición de evento `validado`:**

El evento `validado` es emitido por un verificador independiente humano o sistema autorizado, después de:
1. Re-evaluar el run sobre particiones purgadas con métricas verificables.
2. Firmar el informe de re-evaluación con su clave Ed25519 privada.
3. Verificar que la cadena de ciclo de vida sea continua y no rota para ese `model_id`.
4. Anclar el `event_sha256` más reciente en un almacén de confianza externo.

**Firma:** El evento `validado` debe llevar una firma Ed25519 sobre la canonicalización RFC 8785 del evento completo (todos los campos en orden canónico, incluida la cadena de hashes verificable). La firma se verifica usando la clave pública del verificador, la cual debe estar fuera del repositorio y del control del pipeline de entrenamiento.

**Autenticación del informe del verificador:**
1. El informe debe contener: `model_id`, `manifest_sha256`, métricas de evaluación, y la afirmación de que las particiones fueron evaluadas una sola vez.
2. El loader verifica la firma Ed25519 del informe usando la clave pública registrada del verificador.
3. El loader verifica que `manifest.sha256` en el informe coincida con el manifiesto del run.
4. El loader verifica la continuidad de la cadena de eventos en `lifecycle.jsonl` para ese `model_id`.
5. El loader verifica que el `event_sha256` del evento `validado` sea consistente con la canonicalización RFC 8785.

**Verificación de la transición de estado:**
- `sealed` → `validado`: Requiere evento `validado` firmado en el registro con cadena verificable y anclaje externo.
- `validado` → `approved`: Requiere evento `approved` firmado por autoridad humana, con cadena de ciclo de vida continua y estado vigente.
- El pipeline de entrenamiento **no puede emitir** el evento `validado` por sí mismo. Solo puede emitir `sealed`. La transición a `validado` y `approved` requiere intervención humana firmada y verificación de cadena.

**Vinculación de informe, manifiesto, model_id y hashes:**
- `model_id` debe ser idéntico en: manifiesto, metrics.json, event_id en lifecycle.jsonl, y el evento `validado`/`approved` en el registro.
- `manifest_sha256` debe ser coherente entre el manifiesto y el evento en el registro.
- Los hashes de artefactos (rf.joblib, xgb.joblib, calibrator.joblib) deben coincidir con los declarados en el manifiesto.
- La cadena de hashes debe ser continua: `sequence_number` monotónica, `previous_event_sha256` = `event_sha256` del evento anterior, `event_sha256` calculado vía canonicalización RFC 8785.

**Contrato coherente para validated y approved:**
- Ambas requieren: cadena de eventos verificable, firma Ed25519 válida, anclaje externo.
- `validado` requiere: informe firmado del verificador + cadena verificable.
- `approved` requiere: evento `approved` firmado en el registro + cadena verificable + estado vigente + anclaje externo.
- La ausencia de firma verificada o anclaje externo obliga al loader a modo *integrity-only* y deniega `approved`/`validado` para `inference` o `evaluation`.

**Regla transversal:** si no hay firma Ed25519 verificable en el evento y no hay anclaje externo confiable, el loader debe operar en modo *integrity-only* y denegar cualquier deserialización para `inference` o `evaluation` que requiera confianza en la procedencia.

#### Tabla de decisión rápida para el loader

| Acción | Estado `sealed` | Estado `validated` | Estado `approved` | Sin cadena verificable |
|---|---|---|---|---|
| Deserializar para `inference` | **No** (solo audit) | **No** (solo con autorización del verificador y anclaje externo) | **No** (sin firma verificada y anclaje) | **No** |
| Deserializar para `evaluation` | **No** (solo audit con integridad) | **Sí** (con informe firmado, cadena verificada y anclaje) | **Sí** (con firma válida y cadena verificada) | **No** |
| Cargar metadata (`audit`) | **Sí** (hashes OK) | **Sí** (hashes OK) | **Sí** (hashes + firma OK) | **No** (cadena rota) |
| Firmar aprobación pendiente | N/A | N/A | Requiere clave Ed25519 + evento en registro | N/A |

### 8.4 Códigos de error

| Código | Causa |
|---|---|
| `E_ID_INVALID` | Formato de `model_id` inválido |
| `E_NOT_FOUND` | Run inexistente |
| `E_PATH_ESCAPE` | Ruta fuera de `runs/`, symlink o junction |
| `E_MANIFEST_TOO_LARGE` | Manifiesto por encima del límite |
| `E_MANIFEST_PARSE` | JSON inválido, duplicado o no finito |
| `E_SCHEMA_UNSUPPORTED` | `schema_version` no soportado |
| `E_MANIFEST_HASH` | Hash del manifiesto incorrecto o ausente |
| `E_SIGNATURE` | Firma ausente o inválida cuando se exige |
| `E_NOT_SEALED` | Sin evento `sealed` en el registro |
| `E_STATUS_DENIED` | Estado incompatible con el propósito |
| `E_ARTIFACT_MISSING` | Artefacto obligatorio ausente |
| `E_ARTIFACT_SIZE` | Tamaño distinto del declarado |
| `E_ARTIFACT_HASH` | Hash distinto del declarado |
| `E_CALIBRATION_BINDING` | Calibrador no pertenece al modelo base |
| `E_CLASS_ORDER` | Orden o conjunto de clases inconsistente |
| `E_FEATURE_MISMATCH` | Features distintas en cantidad, orden o definición |
| `E_VERSION_INCOMPATIBLE` | Entorno o serializador incompatible |
| `E_METRICS_BINDING` | Métricas no vinculadas al artefacto o partición |
| `E_DESERIALIZE` | Fallo al reconstruir el objeto |
| `E_POST_LOAD_CHECK` | Objeto cargado no cumple el contrato |

### 8.5 Riesgo de joblib/pickle

`joblib` usa `pickle` para reconstruir objetos. Un pickle malicioso puede ejecutar código arbitrario durante `load`, antes de que el objeto exista. Los controles de este diseño se ordenan así:

1. **Verificación previa:** schema, hashes, estado y coherencia antes de tocar el deserializador.
2. **Lectura única:** se hashea y se deserializa el mismo buffer; no hay ventana para sustituir el archivo.
3. **Autenticidad:** firma del manifiesto y aprobación firmada; sin clave válida, un run no puede llegar a `approved`.
4. **Aislamiento:** el proceso de carga corre con mínimos privilegios, sin red, sin secretos y con límites de memoria/tiempo; para artefactos no confiables, en un subproceso desechable.
5. **Formato seguro a futuro:** para inferencia, exportar a ONNX o a un formato de arrays sin ejecución de código; mantener pickle solo para reentrenamiento local.

**Por qué un hash no basta:** si un atacante puede escribir en `models/runs/<id>/`, puede sustituir `rf.joblib`, recalcular su hash, reescribir `manifest.json`, recalcular `manifest.sha256` y añadir un evento al registro. Todos los hashes cuadrarán. Sin una firma con una clave que el atacante no posea, o sin un ancla externa (log inmutable, Git firmado, almacén WORM), el sistema no puede distinguir ese run de uno legítimo. El hash detecta corrupción accidental y mezclas; no autentica.

**Riesgo residual:** incluso con firma, un modelo legítimo puede tener código vulnerable en su cadena de dependencias. La firma autentica el origen, no la seguridad del contenido.

### 8.6 TOCTOU

El patrón inseguro es: hashear la ruta → cerrar → volver a abrir → `joblib.load(ruta)`. Entre ambos pasos el archivo puede cambiar. El diseño lo evita leyendo los bytes una vez, verificando el hash de ese buffer y deserializando ese mismo buffer. Aun así, la deserialización ejecuta código: la única defensa real contra un payload malicioso es no cargarlo (firma/aislamiento/formato seguro), no el orden de las comprobaciones.

### 8.7 Auditoría de carga

Cada carga registra en un log append-only:

```text
timestamp, model_id, manifest_sha256, rf_sha256, xgb_sha256, calibrator_sha256,
effective_status, purpose, loader_version, outcome, error_code, caller
```

El log no contiene rutas absolutas ni secretos. Un fallo de carga también se registra. El `model_id` y los hashes se propagan a `DecisionEngine` y a cualquier resultado de inferencia.

---

## 9. Modelo de amenazas

### 9.1 Fronteras de confianza

| Frontera | Confianza | Control |
|---|---|---|
| Código fuente en Git | Alta si el repo y la revisión son confiables | Revisión, commit, CI |
| Directorio de artefactos | **Baja para ejecución**; alta solo si está firmado | Hashes + firmas + permisos |
| Registro de ciclo de vida | Media; puede ser manipulado por quien tenga escritura | Append-only + firma + réplica externa |
| Clave de firma | **Raíz de confianza** | Offline, OS keychain, nunca en el repo |
| Proceso de carga | Baja | Mínimo privilegio, sandbox, sin red |
| Dataset | Media | Snapshot content-addressed + hash |
| Dependencias | Media/baja | Lockfile, hashes de wheels, entorno aislado |

### 9.2 Amenazas y controles

| ID | Amenaza | Vector | Impacto | Control | Residual |
|---|---|---|---|---|---|
| T01 | Sobrescritura accidental | Reentrenar con el mismo `model_dir` | Pérdida de trazabilidad | `model_id` único, publicación sin reemplazo | Bajo |
| T02 | Sustitución de artefacto | Copiar `rf.joblib` de otro run | Modelo equivocado | Hash por artefacto + manifiesto | Bajo sin escritura |
| T03 | Sustitución de manifiesto | Reescribir hashes y manifiesto | Artefacto malicioso “válido” | Firma + registro + ancla externa | **Alto sin firma** |
| T04 | Calibrador cruzado | Mezclar calibrador de otro run | Probabilidades calibradas incorrectas | `base_model_id` + hashes + input hash | Bajo |
| T05 | Deriva de dataset | Descargar datos nuevos y reetiquetar | Métricas no reproducibles | Snapshot + `dataset_sha256` + `matrix_sha256` | Bajo |
| T06 | Escritura interrumpida | Crash o corte de energía | Run parcial | Staging + renombrado + evento | Bajo |
| T07 | Pickle malicioso | `__reduce__` en `.joblib` | RCE | Firma, aislamiento, formato seguro | **Medio** |
| T08 | Path traversal / symlink | `model_id` o artefacto con `..` | Lectura fuera del store | Regex + `realpath` + basename + no symlinks | Bajo |
| T09 | Falsificación de estado | Editar `lifecycle.jsonl` | Modelo no aprobado usado como aprobado | Eventos firmados + aprobación firmada | Medio sin firma |
| T10 | Rollback | Volver a un run aprobado antiguo | Uso de modelo obsoleto | Registro secuenciado + pin + monitoreo | Medio |
| T11 | Fabricación de métricas | Reescribir `metrics.json` | Selección engañosa | Hash de métricas + re-evaluación independiente | Bajo |
| T12 | Supply chain | Dependencia comprometida | Código arbitrario o resultados falsos | Lockfile + hashes + entorno aislado | Medio |
| T13 | No determinismo GPU | Distintas ejecuciones en CUDA | Reproducibilidad falsa | CPU para canónicos + flags + comparación | Medio |
| T14 | Colisión de ID / reloj | ULID duplicado o reloj adverso | Confusión de runs | Unicidad por lock + aleatoriedad + verificación | Muy bajo |
| T15 | Carga de cuarentena | Apuntar el loader a `_t9` | Uso de artefacto no verificado | Loader solo acepta `runs/<id>` registrado | Bajo |
| T16 | TOCTOU | Cambiar archivo entre hash y load | Ejecución de bytes no verificados | Buffer único + firma + aislamiento | Bajo/medio |

### 9.3 Qué pruebas aporta Git y qué no

- `git.commit` documenta el código declarado en el momento del entrenamiento.
- El commit que contiene el manifiesto es posterior y **no** se usa como identidad, para evitar otra referencia circular.
- Git no prueba que el artefacto haya sido producido por ese código, ni que el entorno fuera el declarado, ni que nadie haya reescrito la historia.
- Para autenticidad se necesita una firma con clave fuera del repositorio; Git es evidencia de revisión, no de origen criptográfico.

---

## 10. Integración futura

Ningún archivo de esta sección se modifica en AUD-04B.1. Las referencias de línea describen el estado en `3ba460d`.

### 10.1 `src/tradingai/ml/pipeline.py`

| Estado actual | Cambio v3 |
|---|---|
| `run_training(df, feature_cols, cfg)` en 244-390 | Orquestador `TrainingRun` que recibe un dataset identificado y un `runs_root`; devuelve `model_id` y `manifest_sha256` |
| `save_artifact()` en 151-154 escribe `.joblib` + JSON sin checksum | Sustituido por `ArtifactWriter` con staging, hashes y publicación atómica |
| `meta` en 351-365 registra features, horizonte, label, GPU, params, clases, split, `created_at` y versiones | Se amplía a todos los campos v3; el manifiesto se construye desde el contexto del run, no desde un dict ad hoc |
| Escrituras en 366-377 con `Path(cfg["model_dir"])` y nombres fijos | Se elimina `model_dir`; se escribe solo en `models/runs/<model_id>/` |
| `evaluate()` en 73-78 muta XGBoost con `set_params(device="cpu")` | La evaluación no debe mutar el modelo persistido; el dispositivo efectivo se fija antes de entrenar y se registra |
| `calibrated_metrics` se calcula (312-315) pero no se persiste | Se guarda en `metrics.json` con su hash y vínculo al calibrador |
| Sin comprobación de Git limpio ni de identidad del dataset | Precondiciones obligatorias: `git.dirty == false`, snapshot verificado, config hasheada |

Compatibilidad: durante la migración, `run_training` puede mantener una firma legacy que escriba en un directorio temporal explícito, marcado `experimental` y sin manifiesto publicable. Nunca debe volver a escribir en la raíz de `models/`.

### 10.2 `src/tradingai/ml/calibration.py`

| Estado actual | Cambio v3 |
|---|---|
| `Calibrator.save()` en 168-188 escribe joblib + JSON schema 2 con `joblib_sha256` | Se conserva como escritor de artefacto dentro del staging; el manifiesto pasa a ser la autoridad |
| `Calibrator.load()` en 190-232 verifica el hash contra el JSON del propio calibrador | Se vuelve interno: solo lo llama el loader v3, después de verificar el manifiesto |
| `_payload()` en 158-166 no registra modelo base ni partición | Se añade, en el manifiesto, `base_model_id`, hashes base, `fit_partition` y `calibration_input_sha256` |
| El calibrador se ajusta sobre `val_ensemble` en pipeline 307-308 | Se prohíbe ajustar sobre test; el manifiesto lo verifica |
| El hash del calibrador está en su propio JSON | Es necesario, pero insuficiente: el manifiesto debe fijar el mismo hash de forma independiente |

El esquema interno del calibrador puede seguir siendo 2 durante la migración. La vinculación fuerte vive en el manifiesto v3; un calibrador schema 2 sin manifiesto v3 no es cargable por el loader nuevo.

### 10.3 `src/tradingai/decision/engine.py`

| Estado actual | Cambio v3 |
|---|---|
| `decide(..., model_version: str | None = None)` en 28 | `decide(..., model: ModelIdentity)` obligatorio |
| Fallback `model_version or cfg.get("model_version", "unknown")` en 30 | Eliminado; sin identidad verificada no hay decisión |
| La salida copia `model_version` como texto en 31-33 | La salida incluye `model_id`, `manifest_sha256` y hashes de artefactos |
| No comprueba estado ni procedencia | Exige `purpose="inference"` y estado `approved`; en caso contrario, `HOLD` o excepción según política |

`ModelIdentity` es un objeto inmutable, no un string. Un llamador no puede inventar `"v0.1"` ni omitir la identidad. En tests se inyecta una identidad ficticia explícita, nunca un valor por defecto.

### 10.4 `config/ml.yaml`

| Estado actual | Cambio v3 |
|---|---|
| `model_dir: models` en línea 7 | `runs_root: models/runs`, `registry_path: models/registry`, `schema_version: "3.0.0"` |
| Sin política de sobrescritura | `allow_overwrite: false` (no configurable a `true` en producción) |
| Sin política de Git | `require_clean_git: true` |
| Sin política de estado | `allow_unsealed: false`, `require_signature_for_approval: true` |
| Hiperparámetros en 12-25 | Se conservan, pero el manifiesto registra los valores efectivos, incluidos defaults aplicados |

El YAML no selecciona modelo. La selección es un `model_id` explícito en tiempo de ejecución o en `decision.yaml`, nunca “el último”.

### 10.5 `config/decision.yaml`

| Estado actual | Cambio v3 |
|---|---|
| `model_version: "v0.1"` en línea 13 | Eliminado |
| Sin modelo declarado | `model_id: null` (debe resolverse explícitamente al arrancar) |
| Sin política de aprobación | `require_approved: true`, `on_missing_model: "halt"` |

Un `model_id` nulo con `require_approved: true` impide operar; es preferible a operar con una etiqueta inventada.

### 10.6 Tests de leakage

| Test actual | Extensión v3 |
|---|---|
| `test_holdout_independence_compares_learned_state` (97-123) muta solo features de test y compara predicciones | Añadir: `run_fingerprint` distinto, `dataset_sha256`/`matrix_sha256` distintos, `index_sha256` de test distinto, `index_sha256` de train/validation iguales, y bytes de `rf`/`xgb`/`calibrator` idénticos si el entrenamiento es determinista |
| `test_gap_smaller_than_horizon_rejected` usa `models/_never_written` (126-132) | Migrar a `tmp_path`; ningún test debe nombrar `models/` |
| `test_artifacts_include_classes_and_split_manifest` (159-166) valida el JSON legacy | Sustituir por validación del manifiesto v3 y de `manifest.sha256` |
| No hay test de no contaminación | Añadir: snapshot de hashes de `models/` antes/después de la suite; debe ser idéntico |

Los tests deben usar un `runs_root` temporal y un registro temporal. La suite nunca debe escribir en `models/`.

### 10.7 Dashboard

- `src/tradingai/dashboard/app.py:10-11` solo carga `PaperBroker`; no carga modelos.
- Integración futura: leer `registry/index.json` en modo lectura para mostrar `model_id`, estado y fecha; nunca deserializar un `.joblib` para visualizar.
- Si no hay modelo `approved`, mostrar “sin modelo aprobado” y no inferir métricas de directorios legacy.
- Las métricas mostradas deben provenir de `metrics.json` verificado, con su `model_id` y estado.

### 10.8 Backtesting

- Los resultados deben registrar `ModelIdentity` (o `model_id` + `manifest_sha256`), no una etiqueta libre.
- Un backtest de “validación” solo acepta `approved`; un backtest experimental puede aceptar `sealed` con una marca explícita y sin presentarse como evidencia de producción.
- No se implementa en AUD-04B.1, pero el contrato debe preverlo para no volver a perder la trazabilidad.

### 10.9 Estrategia de migración

1. Añadir el módulo de procedencia sin tocar el comportamiento por defecto.
2. Escribir runs v3 solo con un flag explícito y en un `runs_root` temporal.
3. Migrar los tests a v3 y eliminar `models/_never_written`.
4. Cambiar `DecisionEngine` a `ModelIdentity` y `config/decision.yaml` a `model_id`.
5. Retirar `model_dir` del pipeline cuando ningún test lo use.
6. Mantener el legacy en cuarentena; no migrarlo ni borrarlo sin autorización.

---

## 11. Ubicación canónica

### 11.1 Evidencia

| Criterio | `C:\Users\USER\Documents\GitHub\Trading` | `C:\TradingAI_BTC` |
|---|---|---|
| Repositorio Git | Sí | **No** (sin `.git` ni padre) |
| Remoto `origin` | `https://github.com/lutz405/Trading.git` | No aplica |
| HEAD | `3ba460d...` | No verificable |
| Estado | Limpio (antes de este documento) | Sin control de versiones |
| `.gitattributes` | Presente | Ausente |
| Archivos no-caché | 129 | 128 |
| Cachés | `.mypy_cache`, `.ruff_cache`, `__pycache__` | Equivalentes, con diferencias menores |
| Uso por OpenCode | No es el directorio de sesión | **Sí** |

### 11.2 Riesgos de mantener dos copias

1. **Ediciones invisibles:** un cambio en `C:\TradingAI_BTC` no aparece en `git status` del repo y puede perderse.
2. **Divergencia silenciosa:** dos conjuntos de modelos, tests y configuraciones pueden evolucionar por separado.
3. **Commits incompletos:** un commit hecho en el repo no incluye cambios de la copia sin Git.
4. **Auditorías sobre el árbol equivocado:** los hashes y las pruebas pueden ejecutarse contra una copia que no es la publicada.
5. **Duplicación de cuarentena:** `QUARANTINE.*` existe en ambas copias; si una se actualiza y la otra no, la contención deja de ser fiable.

### 11.3 Opciones

| Opción | Descripción | Ventaja | Riesgo | Recomendación |
|---|---|---|---|---|
| **A** | Usar solo el repo Git; abrir OpenCode allí | Una única fuente de verdad; Git audita todo | Requiere cambiar el directorio de sesión | **Recomendada** |
| **B** | Convertir `C:\TradingAI_BTC` en `git worktree` del repo | Dos árboles Git-aware, mismo object store | Ramas y modelos pueden divergir; más complejidad | Aceptable si se necesita trabajo paralelo |
| **C** | Mantener copia plana con script de sincronización y verificación de hashes | No cambia el flujo actual | Toil, carreras, olvidos; no recomendable | Solo transitoria |
| **D** | Junction/symlink de `C:\TradingAI_BTC` al repo | Una sola ubicación física | Git, backups y herramientas pueden seguirlo mal; difícil de auditar | **No recomendada** |

### 11.4 Recomendación

1. **Canónico:** `C:\Users\USER\Documents\GitHub\Trading`.
2. **Sesión de OpenCode:** abrirla en ese directorio (o mover la sesión con la herramienta de sesión, sin mover carpetas). No se ejecuta ningún movimiento en esta fase.
3. **Copia de trabajo:** congelarla como snapshot de solo lectura hasta que se decida archivarla; no usarla para entrenar, testear ni cargar modelos.
4. **Si se necesita un segundo árbol:** usar `git worktree add`, no una copia plana, y asignar ramas distintas.
5. **Preflight obligatorio** en entrenamiento y carga:

```text
git -C <root> rev-parse --show-toplevel  == root esperado
git -C <root> status --porcelain          == vacío (o solo docs permitidos)
git -C <root> rev-parse HEAD              == commit declarado
```

Si falla, abortar. El `runs_root` y el `registry_path` deben resolverse bajo el mismo root canónico.

### 11.5 Qué no se hace ahora

- No se mueven carpetas.
- No se sincronizan archivos.
- No se modifica `.gitattributes` ni configuraciones.
- No se crea un worktree.
- No se commitea este documento.

---

## 12. Plan de implementación por etapas

| Etapa | Objetivo | Depende de | Riesgo principal |
|---|---|---|---|
| S0 | Aprobar este diseño y resolver decisiones pendientes | — | Diseño ambiguo |
| S1 | Schema, canonicalización y validador puros | S0 | Sobrevalidar o dejar campos ambiguos |
| S2 | Identidad, almacén, publicación y registro | S1 | Atomicidad y concurrencia |
| S3 | Integración en pipeline detrás de flag | S2 | Romper tests existentes |
| S4 | Loader y CLI de verificación | S2, S3 | Deserialización prematura |
| S5 | Integración en DecisionEngine y configuración | S4 | Cambiar el comportamiento operativo |
| S6 | Validación independiente y aprobación firmada | S4, S5 | Aprobación automática accidental |
| S7 | Regeneración de un candidato y retirada del legado | S6 | Selección implícita de modelo |

### S0 — Aprobación del diseño

- **Entregable:** este documento revisado y firmado; decisiones pendientes resueltas o explícitamente aplazadas.
- **Criterio de salida:** no quedan decisiones que cambien el esquema o el modelo de amenazas.
- **Rollback:** ninguno; no hay código.

### S1 — Schema, canonicalización y validador

- **Alcance:** `schema/model-manifest-3.0.0.json`, `canonical_json`, `validate_manifest`, `validate_invariants`.
- **Reglas:** funciones puras, sin I/O, sin deserialización, con errores tipados.
- **Criterio de salida:** el manifiesto de ejemplo valida; los negativos de schema fallan; el hash canónico es estable entre ejecuciones y plataformas.
- **Rollback:** módulo aislado, sin llamadas desde producción.

### S2 — Identidad, almacén, publicación y registro

- **Alcance:** generación de ULID, reserva con lock, staging, escritura, hashes, publicación atómica, `lifecycle.jsonl`, índice derivado, recuperación de runs no registrados.
- **Criterio de salida:** simulación de fallo en cada paso deja el sistema en un estado seguro; no se puede sobrescribir; dos writers no colisionan.
- **Rollback:** feature flag; los runs creados en pruebas viven en un root temporal.

### S3 — Integración en el pipeline

- **Alcance:** `TrainingRun`, construcción del manifiesto, dataset snapshot, hashes de features, métricas persistidas, flag `provenance.enabled`.
- **Criterio de salida:** un entrenamiento de prueba produce un run sellado en `tmp_path`; la suite legacy sigue pasando; nada se escribe en `models/` durante los tests.
- **Rollback:** flag desactivado; el pipeline vuelve al comportamiento actual sin tocar artefactos existentes.

### S4 — Loader y CLI de verificación

- **Alcance:** `load_model`, `ModelLoadError`, `verify_run`, `list_runs`, lectura de estado, verificación de firmas.
- **Criterio de salida:** carga un run v3 de prueba; rechaza todos los negativos de la sección 13; nunca deserializa antes de verificar.
- **Rollback:** el loader no se usa en producción; solo tests y CLI.

### S5 — Integración en DecisionEngine y configuración

- **Alcance:** `ModelIdentity`, firma de `decide`, `config/decision.yaml`, `config/ml.yaml`, arranque con modelo aprobado o halt.
- **Criterio de salida:** no existe fallback a `"v0.1"` ni a `"unknown"`; sin identidad aprobada no se emite decisión; los tests usan identidades ficticias explícitas.
- **Rollback:** flag de configuración; el motor puede seguir recibiendo probabilidades en tests, pero no en producción.

### S6 — Validación independiente y aprobación

- **Alcance:** verificador que re-evalúa sobre el snapshot, genera informe firmado, y flujo de aprobación humana con alcance y caducidad.
- **Criterio de salida:** `validated` requiere informe reproducible; `approved` requiere firma humana y manifiesto firmado; el pipeline no puede aprobar.
- **Rollback:** los estados permanecen en `sealed`; no hay promoción automática.

### S7 — Regeneración y retirada del legado

- **Alcance:** elegir un dataset identificado, entrenar en CPU determinista, sellar, validar, revisar y aprobar un candidato; decidir el destino de `_t7..._testcal` con autorización.
- **Criterio de salida:** un run v3 reproducible y verificado; el legado sigue intacto hasta la decisión explícita; `models/` no contiene modelos genéricos.
- **Rollback:** el candidato se rechaza; la cuarentena no se toca.

**Regla transversal:** ninguna etapa puede escribir en `models/` fuera de `runs/`, `.staging/`, `.failed/` y `registry/`. Ninguna etapa puede modificar los documentos de cuarentena.

---

## 13. Plan de pruebas

### 13.1 Pruebas unitarias

| ID | Escenario | Setup | Resultado esperado |
|---|---|---|---|
| U01 | Manifiesto con campo obligatorio ausente | JSON sin `calibration` | `SchemaError` con ruta del campo |
| U02 | Canonicalización y hash | Mismo objeto, distinto orden de claves | Bytes idénticos; `manifest.sha256` estable; sin floats |
| U03 | `model_id` inválido o duplicado | ID con `../`, longitud incorrecta, repetido | `E_ID_INVALID` / colisión detectada |
| U04 | Hash y tamaño de artefacto | Bytes alterados en un bit | `E_ARTIFACT_HASH`; tamaño distinto → `E_ARTIFACT_SIZE` |
| U05 | Confinamiento de rutas | Artefacto con `../x`, ruta absoluta o symlink | `E_PATH_ESCAPE` |
| U06 | Aritmética de particiones | Solape, hueco menor que horizonte, `row_end` mal | `PartitionError` |
| U07 | Transiciones de estado | `sealed → approved` sin `validated`; `revoked → approved` | Rechazo; `approved` solo con evidencia firmada |
| U08 | Vínculo de métricas | Métrica con hash de otro artefacto o índice de otra partición | `E_METRICS_BINDING` |
| U09 | Política de versiones | sklearn incompatible, schema 4.x | `E_VERSION_INCOMPATIBLE` / `E_SCHEMA_UNSUPPORTED` |
| U10 | Reserva sin sobrescritura | Directorio destino ya existe | `E_EXISTS`; original intacto |
| U11 | `run_fingerprint` | Cambiar `model_id`, timestamp o hash de artefacto | Fingerprint **no** cambia; cambiar dataset/params/código sí cambia |
| U12 | Hash desacoplado | Manifiesto sin campo de auto-hash; sidecar correcto/incorrecto | Verificación correcta; nunca se busca `manifest_sha256` dentro del manifiesto |

### 13.2 Pruebas de integración

| ID | Escenario | Resultado esperado |
|---|---|---|
| I01 | Camino feliz: escribir → sellar → registrar → cargar | `LoadedModel` con identidad y hashes correctos |
| I02 | Hash de artefacto incorrecto | `E_ARTIFACT_HASH`; no se deserializa |
| I03 | Manifiesto incompleto o truncado | `E_MANIFEST_PARSE` / `SchemaError`; no se publica |
| I04 | `schema_version` incompatible | `E_SCHEMA_UNSUPPORTED` |
| I05 | Calibrador de otro run | `E_CALIBRATION_BINDING` |
| I06 | `rf.joblib` de otro `model_id` | `E_ARTIFACT_HASH` o `E_CALIBRATION_BINDING` |
| I07 | Dataset distinto con mismas features | `E_ARTIFACT_HASH`/`E_METRICS_BINDING`; el snapshot no coincide |
| I08 | Features distintas en orden o cantidad | `E_FEATURE_MISMATCH` |
| I09 | Particiones solapadas o sin purga | `PartitionError` antes de sellar |
| I10 | Intento de sobrescribir un run existente | `E_EXISTS`; run original byte-idéntico |
| I11 | Interrupción en cada paso del protocolo | Antes de publicar: `.failed`; entre publicar y registrar: no cargable; recuperación idempotente |
| I12 | Artefacto faltante | `E_ARTIFACT_MISSING` |
| I13 | Modelo sin `metrics.json` o sin partición de test | `E_METRICS_BINDING`/`SchemaError`; no se sella |
| I14 | Run `sealed` usado para inferencia; `_t9` referenciado por ruta | `E_STATUS_DENIED`/`E_PATH_ESCAPE` |
| I15 | Modificación conjunta de manifiesto y artefacto | Con firma: `E_SIGNATURE`; sin firma: el hash cuadra y el test documenta el riesgo residual |
| I16 | Manipulación del registro | Evento con hash distinto o transición inválida → rechazo; estado no aprobado |
| I17 | Rollback a un manifiesto anterior | El registro detecta secuencia/manifest hash distinto; se rechaza |
| I18 | Dos reservas concurrentes del mismo ID | Solo una gana; la otra aborta sin tocar el run |
| I19 | `metrics.json` alterado | `E_METRICS_BINDING`/hash distinto |
| I20 | Run `approved` con firma válida | Carga correcta y log con identidad completa |

### 13.3 Pruebas de seguridad

| ID | Escenario | Resultado esperado |
|---|---|---|
| S01 | Pickle malicioso en artefacto no verificado | El canario **no** se ejecuta; el loader rechaza antes de `joblib.load` |
| S02 | `model_id` con `../` o unidad absoluta | `E_ID_INVALID`/`E_PATH_ESCAPE` |
| S03 | Symlink o junction dentro de `runs/` | Rechazo por tipo de archivo y `realpath` |
| S04 | Manifiesto gigante o profundamente anidado | `E_MANIFEST_TOO_LARGE`; sin agotamiento de memoria |
| S05 | Claves duplicadas, `NaN`, `Infinity` | `E_MANIFEST_PARSE` |
| S06 | Manifiesto o aprobación sin firma cuando se exige | `E_SIGNATURE`; no hay aprobación implícita |
| S07 | Rotación/revocación de clave | Firma antigua rechazada según política; run revocado no carga |
| S08 | Replay o rollback del registro | Secuencia/hash detecta el replay; estado efectivo no retrocede |
| S09 | Carga en proceso sin privilegios | Sin red, sin escritura fuera de temp, límites de memoria/tiempo |
| S10 | Fuga de secretos en logs | El log no contiene rutas absolutas, tokens ni contenido de artefactos |
| S11 | TOCTOU: sustituir el archivo tras el hash | El loader usa el buffer ya hasheado; la sustitución no afecta la deserialización |
| S12 | Objeto cargado que no cumple `n_features_in_`/`classes_` | `E_POST_LOAD_CHECK`; no se devuelve parcial |

**Nota:** las pruebas con pickles maliciosos se construyen en un directorio temporal y nunca se cargan en el proceso de test; se verifica la ausencia del archivo canario. No se ejecuta carga de artefactos del repositorio.

### 13.4 Pruebas de validez estadística

| ID | Escenario | Resultado esperado |
|---|---|---|
| V01 | Independencia del holdout | Mutar solo test no cambia los bytes de RF/XGB/calibrador si el entrenamiento es determinista; sí cambia el hash de test y las métricas |
| V02 | Purga entre particiones | Ninguna etiqueta de train usa precios de validation/test; `label_end_position` < inicio de la siguiente partición |
| V03 | Calibración solo en validation | El calibrador no ve test; `fit_partition == "validation"` |
| V04 | Test usado una vez | `test_evaluated_once: true`; el informe de selección no usa test |
| V05 | Re-evaluación independiente | El verificador recalcula y obtiene las mismas métricas dentro de tolerancia documentada |
| V06 | Alineación de clases | `class_order` consistente en target, modelos, calibrador y métricas |
| V07 | Clase ausente o muestra pequeña | Métricas definidas o declaradas no aplicables; no se inventan valores |
| V08 | Intervalos de confianza | Se reportan bootstrap o intervalos; no se declara superioridad por una diferencia mínima |
| V09 | Comparaciones múltiples | El informe declara cuántos modelos/variantes se compararon y el riesgo de selección |

### 13.5 Cobertura de los escenarios exigidos

| Escenario exigido | Pruebas |
|---|---|
| Hash incorrecto | U04, I02, I19 |
| Manifiesto incompleto | U01, I03 |
| Schema incompatible | U09, I04 |
| Calibrador cruzado | I05, U08 |
| Modelo de otro `model_id` | I06 |
| Dataset diferente | I07 |
| Features diferentes | I08, U08 |
| Particiones temporales inconsistentes | I09, U06 |
| Sobrescritura de run existente | I10, U10 |
| Interrupción durante escritura | I11 |
| Artefactos incompletos | I12 |
| Modelo sin evaluación | I13 |
| Carga de artefacto experimental en cuarentena | I14 |
| Modificación conjunta de manifiesto y artefacto | I15, S06 |
| Ausencia de autenticación confiable | S06, S07, I15 |

### 13.6 Fixtures y reglas de ejecución

1. **`tmp_runs_root`:** cada test crea su propio `runs_root`, `registry` y `.staging`; nunca usa `models/`.
2. **Canario de pickle:** payload que, si se ejecutara, escribiría un archivo marcador; el test verifica que el marcador no existe.
3. **Inyección de fallos:** monkeypatch de `fsync`, `os.replace`, `os.rename` y escritura para simular corte en cada paso.
4. **Reloj e IDs:** ULID y timestamps inyectables para pruebas deterministas.
5. **Sin red:** los tests no descargan datos ni consultan servicios externos.
6. **Sin artefactos reales:** ningún test deserializa `_t7..._testcal` ni los usa como fixture.
7. **Snapshot de `models/`:** antes y después de la suite se comparan los 30 hashes de `QUARANTINE.sha256`; deben ser idénticos.
8. **Aislamiento:** los tests de seguridad se ejecutan en un subproceso con límites y sin credenciales.

### 13.7 Puertas de CI

- Schema válido para todos los manifiestos de prueba.
- Hash canónico estable entre sistemas (Windows/Linux, Python 3.13).
- Ninguna escritura en `models/` durante la suite.
- `QUARANTINE.sha256` verificado.
- Todos los negativos devuelven el código de error esperado.
- Ningún test llama a `joblib.load` sobre una ruta no verificada.
- Cobertura de las ramas de error del loader.

---

## 14. Decisiones pendientes

| # | Decisión | Opciones | Recomendación | Impacto |
|---|---|---|---|---|
| D01 | Esquema de `model_id` | ULID / UUIDv7 / hash determinista | ULID | Cambia la regex y el orden |
| D02 | Autenticidad | Sin firma / HMAC / Ed25519 | Ed25519 con clave fuera del repo | Bloquea `approved` |
| D03 | Almacén de dataset | Solo hash / snapshot content-addressed | Snapshot content-addressed | Requiere espacio y política de GC |
| D04 | Granularidad del manifiesto | Uno por ensemble / uno por estimador | Uno por ensemble | Afecta a calibración y loader |
| D05 | Calibración externa | Solo in-pipeline / runs separados | In-pipeline ahora, `external_run` después | Añade un campo, no rompe el esquema |
| D06 | Autoridad de aprobación | Una persona / dos personas / comité | Una persona firmante al inicio | Afecta al flujo humano |
| D07 | Registro | JSONL / SQLite / servicio externo | JSONL + índice derivado | Afecta a concurrencia y consultas |
| D08 | Métrica primaria | Accuracy / macro-F1 / log loss | Macro-F1 con log loss y Brier como apoyo | Afecta a selección y reporting |
| D09 | Canonicalización | RFC 8785 / subconjunto propio | Subconjunto sin floats, documentado | Afecta al hash |
| D10 | Compatibilidad de schema | Exacta / minor hacia atrás | Exacta para 3.x al inicio | Afecta a evolución |
| D11 | Permisos en Windows | ACL / solo hash | Hash como control primario; ACL best-effort | Afecta a inmutabilidad local |
| D12 | Git sucio | Permitir con marca / prohibir | Prohibir para sellar | Afecta a experimentos |
| D13 | Formato de inferencia | joblib/pickle / ONNX / safetensors | ONNX o equivalente a medio plazo | Afecta a seguridad y dependencias |
| D14 | Destino del legado | Mantener / archivar / borrar | Mantener en cuarentena; decidir tras S7 | Afecta a limpieza |
| D15 | Retención de fallidos | 7 / 30 / 90 días | 30 días, configurable | Afecta a espacio y auditoría |
| D16 | Frecuencia de re-validación | Por run / periódica / ante cambio de datos | Por run + revisión periódica | Afecta a operación |

Ninguna de estas decisiones se resuelve en AUD-04B.1. Las que bloquean S1 son D01, D02, D09 y D10; las que bloquean S6 son D06 y D16.

---

## 15. Criterios de aceptación

| Criterio | Dónde se cumple |
|---|---|
| Diseño coherente y sin referencias circulares | §4.1, §5.11 |
| Identidad inequívoca entre modelo, calibrador, dataset y métricas | §5, §6 |
| Separación entre integridad, autenticidad y validez estadística | §6.2, §6.3 |
| Política clara de inmutabilidad | §7.3, §7.4 |
| Estrategia de carga segura | §8 |
| Plan de pruebas verificable | §13 |
| Ningún artefacto original alterado | Verificación final de AUD-04B.1 |
| Ningún código fuente modificado | `git status` solo muestra este documento |

### Verificación final de esta fase

- Los 30 artefactos de `models/` conservan sus SHA-256 y coinciden con `QUARANTINE.sha256`.
- Los 7 datasets conservan sus hashes.
- No se deserializó ningún `.joblib`.
- No se entrenó ni calibró.
- No se modificó `pipeline.py`, `calibration.py`, `engine.py` ni las configuraciones.
- No se modificaron `QUARANTINE.md` ni `QUARANTINE.sha256`.
- No se seleccionó ningún modelo canónico.
- No se hizo commit ni push.
- El único archivo nuevo es `docs/aud04b_model_provenance_v3_design.md`.

**AUD-04B.1 termina aquí.** No se inicia AUD-04B.2, no se implementa el contrato y no se elige ningún modelo. A la espera de autorización expresa.