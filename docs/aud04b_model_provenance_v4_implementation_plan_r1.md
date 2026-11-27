# R13-IMPLEMENTATION-PLAN-R1 — Plan técnico de implementación de provenance 4.0.0

**Estado del documento:** PLAN TÉCNICO. No implementa nada. No autoriza implementación.
**Fecha de emisión:** 2026-11-27.
**HEAD inicial inspeccionado:** `274f4cc0f909e360fe455c9d49f81a1a8745cd4a`.
**HEAD final inspeccionado:** `274f4cc0f909e360fe455c9d49f81a1a8745cd4a`.
**Clasificación de esta tarea:** **COMPLETADO** (plan entregado; sin cambios de código, schema, tests, fixtures, dependencias, modelos ni datasets; sin ejecución de pruebas; sin commits ni push).

**Convención de etiquetas usada en todo el documento:**

| Etiqueta | Significado |
|---|---|
| **H** | Hecho inspeccionado directamente en el repositorio o en la API pública de GitHub durante esta tarea. |
| **I** | Inferencia del planificador a partir de hechos; no es comprobación de ejecución. |
| **P** | Propuesta de trabajo futuro; no está implementada ni autorizada por este documento. |
| **R** | Riesgo identificado; no es un hallazgo de fallo ejecutado. |
| **NV** | Aspecto que no pudo verificarse en esta tarea (por ejemplo, resultados de pruebas). |

---

## 1. Resumen ejecutivo

1. **H** — El repositorio está limpio, en `main`, con HEAD local igual a `origin/main` y al `refs/heads/main` remoto consultado por API y por `git ls-remote`: `274f4cc0f909e360fe455c9d49f81a1a8745cd4a`. El `7b779f8a757f990910f395cd47f687913799d60f` comunicado como último HEAD es el **padre** de ese commit.
2. **H** — El documento de aprobación `docs/aud04b_model_provenance_v4_approval_r1.md` contiene las ocho decisiones DEC-01 a DEC-08 marcadas **APPROVED**, tanto en la matriz (§2) como en el registro §4 y en cada sección individual (§3). Los cambios locales que se reportaron sin commit ya fueron confirmados y publicados en `274f4cc0f…`; no había cambios sin commitear al iniciar esta tarea y no se descartó ninguno.
3. **H** — La aprobación normativa **no implica implementación**: el documento mismo lo declara en §1, §6 y §7, y el diseño 4.0.0 conserva sus etiquetas históricas de "propuesta/pendiente" (§2 y §13 del diseño). No se encontró ningún artefacto 4.0.0 en código: no existe `manifest_v4.json`, no hay dispatch por `schema_version`, no hay campos `source_position_*`, no hay validación de sidecars ni código/dependencia Ed25519.
4. **H** — Toda la lógica de provenance ejecutable vive en un único módulo, `src/tradingai/ml/provenance.py`, cuyo encabezado dice explícitamente "Provenance v3". Su único consumidor en el repositorio es `tests/test_provenance.py` (116 definiciones de test verificadas por conteo). No hay loader, registry, writer, verify run ni lifecycle real.
5. **I** — El trabajo de implementación debe separarse en siete fases con dependencias explícitas: **A** (aislamiento de versiones) → **B** (contrato estructural) → **C** (JCS/fingerprint) y **D** (particiones/calibration) → **E** (eventos/lifecycle) → **F** (sidecars/Ed25519) → **G** (integración y auditoría independiente). C y D son paralelizables después de B; E depende de B y C; F depende de E; G depende de todas.
6. **P** — Cada fase debe conservar el wrapper público `validate_manifest(...) -> list[str]` y los mensajes históricos usados por los tests 3.0.0; el contrato 3.0.0 queda congelado y las fixtures históricas no se reescriben.
7. **R** — El riesgo principal no es la sintaxis sino la **sobreafirmación**: validar estructura no demuestra firma verificada, confianza, autorización ni correspondencia con el dataset original. El plan prohíbe explícitamente presentar esas capacidades como implementadas.
8. **NV** — No se ejecutó ninguna prueba, ningún entrenamiento, ninguna deserialización ni ningún comando que modifique archivos. Los resultados "116 passed"/"441 passed" citados en informes históricos se registran como **documentación previa**, no como resultados de esta tarea.

---

## 2. Estado real del repositorio

### 2.1 Estado Git (H)

| Elemento | Valor inspeccionado | Método |
|---|---|---|
| Git ejecutable | `C:\Users\USER\AppData\Local\GitHubDesktop\app-3.7.0\resources\app\git\cmd\git.exe` (no estaba en `PATH`) | búsqueda en sistema de archivos |
| Directorio de trabajo | `C:\Users\USER\Documents\GitHub\Trading` (repositorio Git; `.git/` presente) | lectura de directorio |
| Branch actual | `main`, con upstream `origin/main` | `git branch -vv` |
| HEAD inicial | `274f4cc0f909e360fe455c9d49f81a1a8745cd4a` | `git rev-parse HEAD`, `.git/refs/heads/main` |
| `origin/main` local | `274f4cc0f909e360fe455c9d49f81a1a8745cd4a` | `.git/refs/remotes/origin/main` |
| Remoto `main` | `274f4cc0f909e360fe455c9d49f81a1a8745cd4a` | `git ls-remote origin refs/heads/main` y API `api.github.com/repos/lutz405/Trading/commits/main` |
| `origin` URL | `https://github.com/lutz405/Trading.git` | `.git/config` |
| Estado local | **Limpio**: `git status --porcelain=v1 --untracked-files=all` sin salida al iniciar | `git status` |
| Commit padre | `7b779f8a757f990910f395cd47f687913799d60f` | `git log`/`.git/logs/HEAD`; confirmado por API |
| Diff del nuevo commit | Un único archivo: `docs/aud04b_model_provenance_v4_approval_r1.md`, 57 inserciones y 36 borrados | `git diff --stat 7b779f8..274f4cc` |

**Conclusión (H):** la afirmación previa de "documento de aprobación con cambios locales sin commit" ya no describe el estado actual: esos cambios están commiteados y publicados. No se hizo `checkout`, `reset`, `stash`, `clean`, `commit` ni `push`.

### 2.2 Verificación de la aprobación normativa (H)

`docs/aud04b_model_provenance_v4_approval_r1.md`:

- Línea 3: **"APPROVED — aprobación normativa humana explícita de DEC-01 a DEC-08"**.
- Líneas 39–48: matriz con `APPROVED` en las ocho filas.
- Líneas 52–146: cada `### DEC-0x` con `**Estado:** APPROVED.` y `**Decisión aprobada:**`.
- Líneas 154–163: tabla "Aprobadas" con las ocho decisiones `APPROVED`; "Rechazadas: Ninguna".
- Líneas 171–177: aplazamientos.
- Líneas 35 y 190: la aprobación **no autoriza** modificar schema/código/tests/fixtures/loaders/registry/writer/inferencia/S2.

Decisiones aprobadas (texto normativo, **H**):

| ID | Decisión aprobada |
|---|---|
| DEC-01 | `reason_code` ASCII `^[a-z][a-z0-9_]{0,63}$`, sin catálogo cerrado. |
| DEC-02 | `actor` con `human:` o `service:`; patrón `^(human|service):[A-Za-z0-9][A-Za-z0-9._-]{0,119}$`; sin autoridad implícita. |
| DEC-03 | `extensions = {}` obligatorio en 4.0.0 inicial. |
| DEC-04 | Calibration compartida exactamente con validation; `fit_partition = "validation"`, `shared_with = "validation"`. |
| DEC-05 | 3.0.0 congelado; 4.0.0 independiente; dispatch explícito por `schema_version`; sin fallback ni defaults de migración. |
| DEC-06 | `run_fingerprint` sobre allowlist normativa; presencia vs null; JCS + SHA-256. |
| DEC-07 | Payload de 9 campos; evento almacenado de 10; sidecar Ed25519 separado; S1 no verifica firmas ni concede autorización. |
| DEC-08 | Posiciones fuente ordenadas, únicas, no negativas; límites semiabiertos; `gap_source >= max(H,E)`. |

### 2.3 Lo que NO existe hoy (H)

- No hay `src/tradingai/schemas/manifest_v4.json`; el único schema es `manifest_v3.json` y `pyproject.toml` declara solo `schemas/manifest_v3.json` en `package-data`.
- No hay rama condicional por `schema_version` en `validate_manifest`; el wrapper siempre usa `MANIFEST_SCHEMA` (v3).
- No hay campos `source_position_start` / `source_position_end` en el schema ni en los validadores.
- No hay tabla de transiciones de lifecycle; `validate_event` acepta cinco estados y no acepta `rejected`.
- No hay evidence cerrada por tipo de evento; no hay validación de sidecars; no hay `signature_b64`, `key_id` ni `format_version`.
- No hay dependencia de cripto en `pyproject.toml` ni `requirements.txt` (`rfc8785` y `jsonschema` sí están declarados).
- No hay archivos `lifecycle.jsonl`, sidecars ni manifiestos de modelos generados en el árbol inspeccionado.
- No hay loaders, registry, writer ni verificación de firmas en `src/`.

### 2.4 Archivos protegidos (H)

`data/raw/` contiene los siete Parquet esperados, incluidos `BTC_USDT_1m.parquet` y `BTC_USDT_5m.parquet`. Solo se listaron nombres de directorio; **no se abrieron, leyeron ni hashearon**. El estado Git limpio confirma que no hay modificaciones en ellos.

---

## 3. Inventario técnico real del código

### 3.1 Punto de entrada único y funciones públicas (H)

Archivo: `src/tradingai/ml/provenance.py` (495 líneas; encabezado: "Provenance v3: schema validation, JCS canonicalization, and integrity checks").

| Función / símbolo | Firma observada | Comportamiento comprobado |
|---|---|---|
| `jcs_canonicalize` | `(obj: Any) -> str` | `rfc8785.dumps(obj).decode('utf-8')`; sin LF final. |
| `jcs_canonical_bytes` | `(obj: Any) -> bytes` | `rfc8785.dumps(obj)` directamente. |
| `sha256_bytes`, `sha256_canonical` | `(bytes)->str`, `(Any)->str` | SHA-256 hex de bytes y de bytes canónicos. |
| `StrictJSONError`, `parse_json_strict` | `(text: str) -> Any` | Rechaza BOM, claves duplicadas, `NaN`/`Infinity` y contenido tras el JSON válido. |
| `load_manifest_schema`, `MANIFEST_SCHEMA` | `()->dict`, constante | Carga `tradingai.schemas:manifest_v3.json` con fallback a ruta de sistema de archivos; se ejecuta al importar. |
| `validate_schema` | `(manifest, schema=None) -> list[str]` | `jsonschema.Draft202012Validator` + `FormatChecker`; mensajes `f'{json_path}: {message}'`; devuelve `['jsonschema not available']` si falta la librería. |
| `validate_rfc3339` | `(value, require_utc=False) -> bool` | Regex `Z?` opcional, con `require_utc` exige `Z`; valida calendario; **no** acepta offsets numéricos, **no** normaliza a 9 decimales, **no** comprueba unicidad/orden. |
| `validate_model_id`, `validate_event_id` | `(object) -> bool` | `^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$`, `^evt_[0-7][0-9A-HJKMNP-TV-Z]{25}$`. |
| `validate_sha256` | `(object) -> bool` | `^[0-9a-f]{64}$`. |
| `validate_event` | `(event, previous_event=None, *, skip_first_event_check=False) -> list[str]` | Verifica `event_sha256` obligatorio y formato; 7 campos obligatorios; campos permitidos = esos + `previous_event_sha256` + `manifest_sha256`; rechaza desconocidos; `manifest_sha256` **opcional**; estados `sealed/validated/approved/deprecated/revoked` (**sin `rejected`**); `actor` solo `isinstance(str)`; `evidence` objeto o null; secuencia entera ≥ 1 y +1 respecto a `previous_event`; genesis solo cuando no es cadena y no se omite. **No** valida evidence cerrada, transiciones ni sidecars. |
| `verify_event_hash` | `(event, expected_hash) -> bool` | Recalcula SHA-256/JCS excluyendo solo `event_sha256`. |
| `validate_calibrator_binding` | `(manifest) -> list[str]` | `in_pipeline` ⇒ `base_model_id == model_id`; hashes base vs artefactos; `artifact_sha256` vs calibrador; clases/orden vs target; `fit_partition != 'test'`; `n_calibrators == len(classes)`. |
| `validate_partition_consistency` | `(manifest) -> list[str]` | Requiere 4 particiones; aritmética de filas; solapamiento por filas (excluye calibration); `calibration.shared_with == 'validation'` ⇒ compara **solo** `row_start`/`row_end`; `class_counts`; `rows_between_partitions >= horizon`; `label_horizon_bars == horizon`; `label_purge_satisfied is not False`; presence de `leakage_checks`; formato de `partition_manifest_sha256`. **No** usa posiciones fuente. |
| `validate_event_chain` | `(events: list[dict]) -> list[str]` | Orden físico, sin ordenar; estado por `model_id` (`next_sequence`, `prior_computed_hash`, `seen_ids`); genesis `0`*64; continuidad de hash; `event_sha256` recalculado por evento; IDs duplicados por modelo; entradas malformadas producen errores, no excepciones (catch de `AttributeError, OverflowError, RecursionError, TypeError, ValueError`). **Sin tabla de transiciones ni sidecars.** |
| `validate_manifest` | `(manifest: dict) -> list[str]` | Compone: `validate_schema` (siempre v3) + `model_id` + `created_at`/`sealed_at` + formato de `run_fingerprint` + `features.count` + binding + particiones. **Sin dispatch por versión.** |

**(I)** La arquitectura actual es un "validador v3 monolítico": no hay capa de proyección, no hay preimagen de fingerprint, no hay constructor de manifiestos y no hay estado persistente.

**(R)** `validate_calibrator_binding` indexa `a['role']`/`a['sha256']` directamente sobre `artifacts`; llamado de forma aislada con una entrada malformada podría propagar `KeyError`. `validate_manifest` mitiga ejecutando el schema primero, pero debe verificarse en la fase B que el nuevo validador 4.0.0 mantenga fail-closed también en llamadas directas.

### 3.2 Schema y versionado (H)

`src/tradingai/schemas/manifest_v3.json` (983 líneas): JSON Schema 2020-12, `$id = https://tradingai.local/schemas/manifest-v3.json`, `additionalProperties: false` en raíz y objetos núcleo; `schema_version` con `const: "3.0.0"`; 17 campos raíz obligatorios. Puntos relevantes para el contraste 4.0.0:

| Área | v3 inspeccionado | Requisito 4.0.0 (-normativo) |
|---|---|---|
| `extensions` | Objeto con `patternProperties` namespaced; **acepta no vacío**. | DEC-03: solo `{}`. |
| Particiones | `$defs/partition` con `row_start/end`, `n_rows`, `time_start/end`, `class_counts`, `index_sha256`, `shared_with` opcional (`string|null`). | DEC-08: añadir límites fuente obligatorios. |
| `calibration.shared_with` | Opcional, `string|null`; en calibration no es requerido. | DEC-04: requerido y `= "validation"`. |
| `calibration.fit_partition` | `enum: ["validation"]` (ya restringido en v3). | DEC-04: se mantiene, más equivalencia completa. |
| `training.environment` | Solo `python` (opcional), `cuda_version`, `cudnn_version`. | §9.3: 8 versiones obligatorias. |
| Purga | `rows_between_partitions`, `label_horizon_bars`, `label_purge_satisfied`, `embargo_rows`. | DEC-08: `embargo_rows` cuenta posiciones fuente; `gap_source >= max(H,E)`. |
| Eventos | Sin schema de evento/evidence/sidecar en JSON Schema. | DEC-07: objetos cerrados por tipo de evento. |

`src/tradingai/schemas/__init__.py`: solo docstring "JSON Schema definitions for model provenance v3."

### 3.3 Canonicalización, hashes y fingerprints (H)

- La canonicalización usa la librería externa `rfc8785` (declarada en `pyproject.toml` y `requirements.txt`). Los tests `TestJCSCanonicalization` y `TestJCSVectors` cubren orden UTF-16, escapes, `-0`, `1e-6`, `1e-7`, `1e20`, `1e21`, enteros fuera del rango seguro, NaN/Inf y delegación exacta a `rfc8785.dumps`. **NV:** no ejecutados en esta tarea.
- `index_sha256`, `partition_manifest_sha256`, `calibration_input_sha256` y `run_fingerprint` **no se calculan en código**: solo se valida su formato (`validate_sha256`) o se reciben como literales en fixtures (p. ej. `"a"*64`, `"3"*64` en `tests/test_provenance.py`). No hay función de preimagen.
- `verify_event_hash` es el único recálculo de hash implementado y cubre exclusivamente el payload del evento (excluyendo `event_sha256`).
- El diseño 4.0.0 §9.5 conserva un vector JCS **reducido** con `schema_version: "3.0.0"` y hash `ed01f9cea45b644c561b6eb0346c7450b7836abb35f4ece1ede5b265e3722157`; sus rutas `validation_intent`/`calibration_intent` no son rutas del manifiesto. No es un vector dorado 4.0.0 (DEC-06, aplazamiento).

### 3.4 Eventos y lifecycle (H)

- `tests/test_provenance.py` construye eventos con `make_event(...)`: 8 campos, `actor = "pipeline"`, `evidence: None`, **sin `manifest_sha256`**, y calcula `event_sha256` con `sha256_canonical`. Esto es consistente con v3 (donde `manifest_sha256` es opcional) e **incompatible** con el payload de 9 campos de DEC-07.
- `validate_event_chain` comprueba cadena e integridad, pero **no** comprueba transiciones. Un salto `sealed → approved` no se detecta hoy. **I:** la fase E debe añadir la tabla de transiciones sin romper los mensajes de error existentes.
- No hay concepto de "estado terminal" en el código actual: `rejected` ni siquiera es un valor admitido.

### 3.5 Particiones, purga, posiciones fuente y calibration (H)

- Capa de provenance: descrita en §3.1; opura por **filas** (`row_start`/`row_end`) y no por posiciones fuente.
- Capa de entrenamiento: `src/tradingai/ml/pipeline.py`:
  - `_validate_temporal(df, X, y, horizon, gap)` valida timestamps, índices y calcula `positions = df.index.get_indexer(X.index)`; exige posiciones estrictamente crecientes y `gap >= horizon`.
  - `_validate_label_purge(...)` calcula `label_end = posición_última_fila + horizon` y exige `siguiente_inicio > label_end` (equivalente a `v - t >= horizon + 1`). Sus tests están en `tests/test_label_purge_contract.py` (6 tests, incluido el caso de posiciones dispersas `[0,1,2,3,4,9,...]`).
  - `run_training(...)` produce un diccionario `split` con `start/end`, `start_position/end_position`, `label_end_position` y `purge` (`train_to_validation`, `validation_to_test`, `train_label_to_validation`, `validation_label_to_test`). **No** construye un manifiesto de provenance ni calcula `run_fingerprint`.
  - `Calibrator.fit(val_ensemble, yval, ...)` en `src/tradingai/ml/calibration.py` ajusta sobre validation: calibración compartida *de facto* en el pipeline, pero sin representación de `shared_with` en el manifiesto. `Calibrator.load` deserializa joblib (capacidad existente, fuera de alcance; este plan no la habilita ni la usa).
- **(I/R)** Las "posiciones" del pipeline son ordinales del DataFrame de features filtrado, mientras que DEC-08 define `source_position` como ordinal de la serie OHLCV **original antes del filtrado**. No se puede afirmar que sean la misma coordenada; la fase D debe declarar explícitamente la distinción y dejar la reconstrucción efectiva a un verificador posterior con el dataset original.

### 3.6 Firmas y sidecars (H)

- No hay código de Ed25519, Base64, `key_id`, `format_version` ni sidecars en `src/` ni en `tests/` (búsqueda sin resultados).
- No hay dependencia criptográfica en `pyproject.toml` ni `requirements.txt`.
- El diseño v3 §5.11 (líneas 801–806 y 1098–1101) dice que la firma cubre **los mismos bytes canónicos de 9 campos** que `event_sha256`, sin LF. El diseño v4 §8.1 afirma que "AUD-04B.1 §8.6 actualmente describe una firma que incluye `event_sha256`" y debe corregirse. Al inspeccionar v3 §8.6 (línea 1271), el texto dice "firma Ed25519 sobre la canonicalización RFC 8785 del evento completo (todos los campos en orden canónico, incluida la cadena de hashes verificable)", lo cual es **ambiguo** y no dice literalmente "incluye `event_sha256`".
- **(I)** Contradicción documental registrada sin corregir: v4 §8.1 describe una corrección cuya premisa no coincide literalmente con v3 §5.11; v3 §8.6 es ambiguo. El contrato aprobado (DEC-07) manda 9 campos firmados; el plan sigue DEC-07 y no reinterpretan v3.

### 3.7 Interfaces públicas y consumidores (H)

- Importaciones de provenance en código de producción: **ninguna**. `src/tradingai/ml/__init__.py` exporta `build_dataset`, `ensemble_proba`, `gpu_available`, `make_labels`, `predict_with_abstention`, `run_training`; **no** exporta provenance.
- Único consumidor: `tests/test_provenance.py` (import directo de 18 símbolos).
- Referencias documentales a `MANIFEST_SCHEMA` en informes y diseños no constituyen consumidores de runtime.
- **I:** cualquier cambio de nombres o mensajes tiene impacto directo y casi exclusivo en esa suite; por eso DEC-05 exige preservar nombres, retorno `list[str]` y mensajes.

### 3.8 Fixtures y tests existentes (H)

| Archivo | Contenido relevante |
|---|---|
| `tests/test_provenance.py` | 116 definiciones de test. Clases: `TestJCSCanonicalization`, `TestStrictJSONParsing`, `TestHashing`, `TestEventHashing`, `TestValidators`, `TestManifestValidation`, `TestEventValidation`, `TestEventValidationHardening`, `TestSchemaValidation`, `TestJCSVectors`, `TestEventChainValidation`. |
| Fixture 3.0.0 en `TestManifestValidation.test_valid_manifest` | `schema_version="3.0.0"`, `extensions={}`, `training.environment={"python": ...}` solamente, sin `source_position_*`, `calibration.shared_with="validation"`, `calibration.index_sha256 = "5"*64` mientras `validation.index_sha256 = "4"*64`. Esto último es válido en v3 (solo se comparan filas) y sería rechazado por DEC-04. |
| Mensajes asertados | `"model_id"`, `"Sequence gap"`, `"sequence_number"`, `"Invalid event type"`, `"event_id"`, `"previous_event_sha256"`, `"event_sha256"`, `"previous_event must be a JSON object"`, `"actor must be a string"`, `"evidence must be an object"`, `"unknown field"`, `"missing required field"`, `"first event"`, `"error computing JCS hash"`, `"duplicate event_id"`, etc. Son restricción de regresión. |
| `tests/test_label_purge_contract.py` | 6 tests de `_validate_label_purge` y `run_training` con posiciones de DataFrame. |
| `tests/test_leakage_indices.py`, `tests/test_pipeline_contract.py` | Instrumentación de índices, independencia del holdout, contratos de split y clases. |
| `tests/test_calibration*.py` | Contrato de `Calibrator` (longitudes, rango, columnas, persistencia, checksum) e integración en pipeline. |

### 3.9 Archivos auxiliares no normativos (H)

`compute_hash.py`, `compute_hash2.py`, `analyze.py`, `fix2.py` en la raíz contienen implementaciones JCS propias y experimentos de hash de eventos con `manifest_sha256: None`. No son importados por `src/` ni por `tests/`. **I:** no deben usarse como referencia normativa; la única implementación canónica es `rfc8785` a través de `provenance.py`.

### 3.10 Dependencias (H)

`pyproject.toml`: `ccxt`, `jsonschema`, `pandas`, `pyarrow`, `pydantic`, `pyyaml`, `loguru`, `numpy`, `scikit-learn`, `xgboost`, `joblib`, `streamlit`, `plotly`, `rfc8785`; `dev = pytest, ruff, mypy`; `package-data` solo `schemas/manifest_v3.json`. `requirements.txt` coherente. No hay dependencia Ed25519.

---

## 4. Matriz DEC → componentes → archivos → pruebas

| DEC | Componente actual inspeccionado | Cambio futuro requerido (P) | Archivos (reales / nuevos) | Pruebas objetivo (futuras) | Fase |
|---|---|---|---|---|---|
| **DEC-01** `reason_code` | `validate_event`: `evidence` solo objeto/null; sin campos por estado. | Evidence cerrada por evento; patrón `^[a-z][a-z0-9_]{0,63}$` en `deprecated`, `revoked`, `rejected`; sin enum. | `src/tradingai/ml/provenance.py` (v3 congelado), `src/tradingai/ml/provenance_v4.py` (nuevo), `src/tradingai/schemas/manifest_v4.json` (nuevo) | V4-U08 + válidos/inválidos (mayúsculas, espacios, no ASCII, 64/65 chars) | B, E |
| **DEC-02** `actor` | `validate_event`: solo `isinstance(str)`; fixtures usan `"pipeline"`, `"verifier"`. | Patrón `^(human|service):...$`, ASCII, sin inferencia de identidad ni autoridad. | ídem | V4-U08 + namespaces y casos de no autoridad | B, E |
| **DEC-03** `extensions={}` | Schema v3 acepta extensiones namespaced no vacías. | Constante objeto vacío en schema 4.0.0; rechazo de cualquier namespace; excluido del fingerprint. | `manifest_v4.json`, `provenance_v4.py` | V4-U13 | B, C |
| **DEC-04** calibration | `validate_partition_consistency` compara solo `row_start/row_end`; fixture con `index_sha256` distinto. | Equivalencia completa de límites, límites fuente, `n_rows`, timestamps normalizados, conteos e índice; `shared_with` requerido; sin frontera validation→calibration. | `manifest_v4.json`, `provenance_v4.py`; `pipeline.py` solo como referencia (sin cambio automático) | V4-U04 | D |
| **DEC-05** versionado | `validate_manifest` sin dispatch; `schema_version` solo validado por `const` v3. | Schema y validador 4.0.0 separados; wrapper `list[str]`; rechazo de versión ausente/desconocida; sin fallback ni defaults. | `provenance.py` (dispatch delgado), `provenance_v4.py`, `manifest_v4.json`, `pyproject.toml` (package-data) | V4-U01, V4-U12 | A, G |
| **DEC-06** fingerprint | No hay cálculo de fingerprint; solo formato SHA-256. | Proyección allowlist exacta §9.2; presencia vs null; JCS+SHA-256; preimágenes independientes; vectores completos aplazados. | `provenance_v4.py` (módulo de preimagen/allowlist) | V4-U10, V4-U11 (vectores reducidos existentes; completos aplazados) | C |
| **DEC-07** eventos/sidecar | Cadena con 8–9 campos, `manifest_sha256` opcional, sin `rejected`, sin evidence cerrada, sin sidecar. | Payload 9 campos obligatorio; evento 10; transiciones; evidence por estado; sidecar Ed25519 estructural; sin verificación de firma. | `provenance_v4.py`, `manifest_v4.json`, nuevo `tests/test_provenance_v4_events.py`, nuevo `tests/test_provenance_v4_sidecars.py` | V4-U07, V4-U08, V4-U09, V4-U11 | E, F |
| **DEC-08** posiciones/purga | Purga por filas en `validate_partition_consistency`; posiciones de DataFrame en `pipeline.py`. | `source_position_*` obligatorios; semiabiertos, orden/unicidad/no negatividad; `gap_source >= max(H,E)`; verificación efectiva separada con datos originales. | `manifest_v4.json`, `provenance_v4.py`; verificador posterior **fuera de S1** (solo propuesto) | V4-U02, V4-U03, V4-U14, V4-U15 | D |

**Leyenda de pruebas (V4-Uxx):** identificadores del diseño 4.0.0 §11; son **criterios futuros**, no pruebas ejecutadas.

---

## 5. Fases de implementación (propuestas; NO ejecutadas)

### Regla global aplicable a todas las fases

- **P** Ninguna fase se acepta solo porque sus propios tests pasan: cada cierre pasa por el punto de control independiente de §8.
- **P** Los archivos 3.0.0 (`manifest_v3.json`, comportamiento y mensajes de `validate_manifest`, `validate_event`, `validate_event_chain`, `validate_schema`) permanecen sin cambios. Las fixtures 3.0.0 no se editan; se añaden fixtures 4.0.0 nuevas.
- **P** No se crea loader, registry, writer, integración de pipeline, deserialización ni inferencia. No se inicia S2.
- **P** No se habilita fallback silencioso entre versiones ni inferencia de versión.

---

### Fase A — Aislamiento de versiones 3.0.0 y 4.0.0

1. **Archivos que se modificarían:** `src/tradingai/ml/provenance.py` (solo el wrapper `validate_manifest`, convertido en dispatcher explícito); `pyproject.toml` (añadir `schemas/manifest_v4.json` a `package-data`). **Nuevos:** `src/tradingai/ml/provenance_v4.py`, `src/tradingai/schemas/manifest_v4.json`, `tests/test_provenance_v4_dispatch.py`. `manifest_v3.json` **no se toca**.
2. **Funciones y contratos afectados:** `validate_manifest(manifest) -> list[str]` conserva nombre, firma y mensajes de la ruta 3.0.0; se añade lectura de `schema_version` con tres ramas: `"3.0.0"` → validador congelado; `"4.0.0"` → validador 4.0.0; ausente/desconocida → error explícito, sin default.
3. **DEC aplicables:** DEC-05 (núcleo), DEC-07 y DEC-08 indirectamente (no se aplican reglas 4.0.0 a un 3.0.0).
4. **Dependencias:** ninguna fase previa. Es la base de B–G.
5. **Pruebas unitarias:** `validate_manifest` con `3.0.0` idéntico al comportamiento actual; con `4.0.0` delega al nuevo validador; con versión ausente, `""`, `"1.0.0"`, `"4.0.1"`, `None`, número o lista se rechaza; ningún caso produce excepción.
6. **Pruebas de integración:** misma fixture 3.0.0 de `tests/test_provenance.py::test_valid_manifest` pasa sin cambios; una fixture 4.0.0 mínima se enruta al validador nuevo; verificación de que `MANIFEST_SCHEMA` sigue siendo v3.
7. **Negativas/adversariales:** `schema_version` con tipos no string; clave duplicada en JSON de entrada (vía `parse_json_strict`); manifiesto 3.0.0 con un campo 4.0.0 inyectado (`source_position_start`) debe rechazarse; manifiesto 4.0.0 con campo exclusivo 3.0.0 no admitido por el schema nuevo debe rechazarse.
8. **Regresiones que deben permanecer verdes:** los 116 tests de `tests/test_provenance.py`; mensajes asertados listados en §3.8; `test_manifest_schema_loaded` y `test_schema_requires_fields`.
9. **Criterios de aceptación:** V4-U01 y V4-U12; diff de `manifest_v3.json` vacío; diff de los cuerpos de validadores v3 vacío salvo el dispatch; ninguna excepción no controlada; `package-data` incluye ambos schemas.
10. **Riesgos / rollback:** **R** fallback accidental por `else: v3`. Mitigación: rama `else` de rechazo y test adversarial. **R** ruptura de mensajes históricos. **P** rollback = revertir el commit de fase y restaurar `validate_manifest` sin despacho; nunca añadir un flag que omita el rechazo.

---

### Fase B — Schema y validación estructural 4.0.0

1. **Archivos que se modificarían:** `src/tradingai/schemas/manifest_v4.json` (nuevo, independiente); `src/tradingai/ml/provenance_v4.py` (nuevo). Sin tocar v3.
2. **Funciones y contratos afectados:** `validate_schema_v4`, validadores de tipo/patrón (`reason_code`, `actor`, `sha256`, `ulid`, timestamps), `extensions = {}`, evidence cerrada por tipo de evento, `additionalProperties: false` en objetos núcleo; todos devuelven `list[str]`.
3. **DEC aplicables:** DEC-01, DEC-02, DEC-03, DEC-07 (estructura de evidence/sidecar), DEC-05.
4. **Dependencias:** Fase A. La Fase C necesita los campos nuevos del schema; la Fase E necesita los patrones de esta fase.
5. **Pruebas unitarias:** patrones válidos/inválidos de `reason_code` y `actor`; `extensions={}` aceptado y `{"x.y": {}}` rechazado; campos desconocidos rechazados en cada objeto cerrado; `null` solo donde el schema lo declara anulable; enteros fuera de `±(2^53−1)` rechazados.
6. **Pruebas de integración:** `validate_manifest` con fixture 4.0.0 completa; verificación de que `jsonschema.Draft202012Validator` usa el schema v4 en esa rama.
7. **Negativas/adversariales:** booleanos donde se exige entero; `"1"` como entero; `NaN`/`Infinity` vía `parse_json_strict`; claves duplicadas; `reason_code` con 65 caracteres; `actor` sin namespace; evidence de `sealed` con campos; campos extra en evidence de `approved`.
8. **Regresiones verdes:** toda la suite 3.0.0; en particular `TestSchemaValidation` y `TestValidators`.
9. **Criterios de aceptación:** V4-U08 y V4-U13 a nivel estructural; ningún error sin prefijo de ruta; sin enum implícito de `reason_code`; sin inferencia de autoridad desde `actor`.
10. **Riesgos / rollback:** **R** copiar el schema v3 y heredar `extensions` abierto o `environment` incompleto. **R** endurecer v3 por accidente. **P** rollback = eliminar el schema v4 y el módulo v4, y revertir el dispatch de A.

---

### Fase C — Canonicalización JCS y `run_fingerprint`

1. **Archivos que se modificarían:** `src/tradingai/ml/provenance_v4.py` (nuevo: proyección allowlist, normalización de timestamps y preimágenes). Se reutiliza `rfc8785`; **no** se reemplaza la implementación v3.
2. **Funciones y contratos afectados:** `build_run_fingerprint(manifest) -> str`, `jcs_bytes(...)`, `project_allowlist(...)`, `normalize_timestamp(...)`; conservan el retorno `str`/`bytes` y la ausencia de LF en bytes hasheados. El archivo manifiesto (si se implementa en el futuro) incluye LF exactamente uno, según §9.4; los hashes de preimagen no lo incluyen.
3. **DEC aplicables:** DEC-06, DEC-05; DEC-03 (extensions excluido).
4. **Dependencias:** Fases A y B.
5. **Pruebas unitarias:** por cada ruta incluida en §9.2, mutarla y comprobar que el fingerprint cambia; por cada ruta excluida (`model_id`, timestamps de salida, `git.commit/branch/tag`, `producer.command`, `snapshot_uri`, resultados de leakage/evaluación, `partition_manifest_sha256`, `calibration_input_sha256`, `artifacts`, `metrics`, `extensions`), comprobar que **no** cambia; ausencia vs `null` distinguidos; `1.0` vs `1` conforme a la regla documentada.
6. **Pruebas de integración:** recálculo independiente de `index_sha256`, `partition_manifest_sha256`, `calibration_input_sha256` y `event_sha256` desde sus propias preimágenes (V4-U11); verificación del vector reducido §9.5 como control de JCS, **sin presentarlo como vector 4.0.0**.
7. **Negativas/adversariales:** `NaN`/`Infinity`; `-0`; `1e-6`, `1e-7`, `1e20`, `1e21`; `2^53−1` y `2^53`; claves unicode ordenadas por UTF-16; string decimal que no se convierte a número; preimagen que contiene accidentalmente el propio digest (ciclo).
8. **Regresiones verdes:** `TestJCSCanonicalization`, `TestJCSVectors`, `TestStrictJSONParsing` y `TestHashing` sin cambios.
9. **Criterios de aceptación:** V4-U10 y V4-U11; ninguna preimagen contiene el hash que produce; no se rellenan defaults; `extensions` no altera el fingerprint; vectores dorados completos siguen **aplazados** (no se inventan).
10. **Riesgos / rollback:** **R** deriva de allowlist (incluir un hash derivado o una ruta de salida). Mitigación: tabla de rutas versionada en el propio módulo y tests de mutación por ruta. **R** normalización de timestamps distinta entre fingerprint e índice. **P** rollback = revertir módulo v4 de fingerprint; no afecta a v3.

---

### Fase D — Particiones, posiciones fuente, purga y calibration

1. **Archivos que se modificarían:** `src/tradingai/ml/provenance_v4.py` (validación de particiones, gap, equivalencia de calibration); `src/tradingai/schemas/manifest_v4.json` (campos `source_position_start/end`, `shared_with` requerido). `src/tradingai/ml/pipeline.py` **solo se lee como referencia**; cualquier cambio en él requiere autorización separada. **Nuevo:** `tests/test_provenance_v4_partitions.py`.
2. **Funciones y contratos afectados:** `validate_partitions_v4`, `gap_rows`, `gap_source`, `validate_purge_v4`, `validate_shared_calibration_v4`; `list[str]`; distinción explícita entre comprobación estructural (S1) y verificación efectiva con dataset original (fuera de S1).
3. **DEC aplicables:** DEC-04 y DEC-08 (núcleo); DEC-06 (las nuevas rutas entran en la allowlist de C).
4. **Dependencias:** Fases A, B y C (normalización de timestamps e `index_sha256`).
5. **Pruebas unitarias:** límites semiabiertos; `source_position_start < source_position_end`; secuencia no negativa, estrictamente creciente y única **cuando se entrega la secuencia**; `source_position_end == última + 1`; `gap_rows` y `gap_source` calculados por separado; ejemplo normativo con filas descartadas (`gap_rows = 0`, `gap_source = 3`, H=3, E=2 ⇒ válido; H=4 ⇒ inválido); `gap_source < 0` rechazado; equivalencia total de calibration; `fit_partition = "validation"`.
6. **Pruebas de integración:** manifiesto 4.0.0 válido con calibration compartida; manifiesto con `shared_with = null` rechazado; comprobación de que solo existen fronteras train→validation y validation→test; verificación de que un futuro verificador con datos originales recalcularía secuencia/límites/digest (V4-U15, como contrato de interfaz, **no** implementado en S1).
7. **Negativas/adversariales:** posiciones duplicadas, negativas o desordenadas; límites que no coinciden con extremos de la secuencia; `rows_between_partitions` sustituyendo a `gap_source`; doble conteo `H + E`; `index_sha256` de calibration distinto de validation; `embargo_rows` interpretado como filas filtradas; calibración independiente.
8. **Regresiones verdes:** `tests/test_label_purge_contract.py`, `tests/test_leakage_indices.py`, `tests/test_pipeline_contract.py` y toda la suite 3.0.0.
9. **Criterios de aceptación:** V4-U02, V4-U03, V4-U04, V4-U14 y V4-U15 (la última como especificación de un verificador separado, no como capacidad S1); ningún mensaje afirme haber verificado la secuencia contra datos originales si solo se recibió el manifiesto.
10. **Riesgos / rollback:** **R** confundir posiciones de DataFrame (`pipeline.py`) con posiciones fuente OHLCV (DEC-08). Mitigación: nombres distintos y documentación de coordenadas. **R** afirmar purga efectiva sin datos originales. **P** rollback = revertir validación v4 y campos del schema v4; no tocar pipeline ni Parquet.

---

### Fase E — Eventos, hashes y lifecycle

1. **Archivos que se modificarían:** `src/tradingai/ml/provenance_v4.py` (payload de 9 campos, tabla de transiciones, evidence cerrada, validación de cadena v4); `src/tradingai/schemas/manifest_v4.json` o schema de evento nuevo; **nuevos:** `tests/test_provenance_v4_events.py` y fixtures 4.0.0 propias (sin editar `make_event` de v3).
2. **Funciones y contratos afectados:** `validate_event_v4`, `validate_event_chain_v4`, `canonical_event_payload`, `verify_event_hash_v4`; retorno `list[str]`/`bool`; `manifest_sha256` pasa a obligatorio; se añade `rejected`; `sequence_number <= 9007199254740991`; timestamp normalizado a 9 decimales UTC; `event_sha256` = SHA-256 del payload de 9 campos; evento almacenado = 10 campos.
3. **DEC aplicables:** DEC-01, DEC-02, DEC-05, DEC-07.
4. **Dependencias:** Fases A, B y C (patrones, JCS, hash). La Fase F depende de esta.
5. **Pruebas unitarias:** eventos válidos por estado con evidence correcta; transiciones permitidas de §7.1; `rejected` y `revoked` terminales; estados repetidos y re-aprobación rechazados; `previous_event_sha256` = 64 ceros solo en genesis; `manifest_sha256` estable por modelo; `event_id` globalmente único.
6. **Pruebas de integración:** cadena de tres eventos con dos `model_id` intercalados; orden físico no reordenado; recálculo de hashes por evento; association de `signature_sidecar_id` con el sidecar (estructura, en F).
7. **Negativas/adversariales:** `sealed → approved`, `approved → validated`, salida de `rejected`/`revoked`; evidence con campos desconocidos o falta de campo obligatorio; `reason_code` inválido; `actor` sin `human:`/`service:`; timestamp con offset numérico, `-00:00`, segundo intercalar o >9 decimales; eventos duplicados/tamperados; entradas no objeto; hash no string; payload recursivo.
8. **Regresiones verdes:** `TestEventValidation`, `TestEventValidationHardening`, `TestEventChainValidation` (v3 intacto), incluidos mensajes exactos asertados.
9. **Criterios de aceptación:** V4-U07, V4-U08, V4-U11; la cadena falla cerrada ante cualquier anomalía; ningún mensaje afirme firma verificada.
10. **Riesgos / rollback:** **R** romper mensajes v3 al compartir código. Mitigación: módulos separados. **R** `rfc8785.FloatDomainError` no cubierto por el `try/except` actual (lista vista en §3.1); verificar cobertura en la fase E. **P** rollback = eliminar validador v4 de eventos; el dispatcher de A rechaza `4.0.0` hasta nueva autorización.

---

### Fase F — Sidecars y Ed25519 (estructura, NO verificación criptográfica)

1. **Archivos que se modificarían:** `src/tradingai/ml/provenance_v4.py` (validación estructural de sidecar); **nuevo:** `tests/test_provenance_v4_sidecars.py`; `pyproject.toml`/`requirements.txt` **solo si se autoriza explícitamente** una dependencia criptográfica en el futuro (no necesaria para validación estructural).
2. **Funciones y contratos afectados:** `validate_sidecar(sidecar, event) -> list[str]`; `check_sidecar_association(...)`; `canonical_base64(...)`; objeto exacto de 7 campos: `format_version=1`, `sidecar_id=sig_<ULID>`, `event_id`, `event_sha256`, `key_id`, `algorithm="Ed25519"`, `signature_b64`.
3. **DEC aplicables:** DEC-07.
4. **Dependencias:** Fase E (necesita `event_id`, `event_sha256` y evidence con `signature_sidecar_id`).
5. **Pruebas unitarias:** decode→encode de Base64 canónico RFC 4648 sin espacios; 64 bytes decodificados; `key_id` ASCII 1–128 del conjunto `[A-Za-z0-9._:-]`; `format_version` distinto de 1 rechazado; `algorithm` distinto de Ed25519 rechazado; campos desconocidos rechazados; unicidad de `(event_id, key_id)`.
6. **Pruebas de integración:** sidecar correctamente asociado al evento; sidecar ausente, duplicado o referido a otro evento rechazado; evidencia de `validated`/`approved`/`rejected` con `signature_sidecar_id` consistente.
7. **Negativas/adversariales:** Base64 no canónico (espacios, padding alternativo); 63/65 bytes; `event_sha256` divergente del evento; `sidecar_id` duplicado; doble sidecar para el mismo `event_id`; intento de inferir confianza/rol desde `key_id`.
8. **Regresiones verdes:** cadena v4 de la Fase E y toda la suite v3.
9. **Criterios de aceptación:** V4-U09; **la validación solo declara forma, unicidad y asociación**; ningún mensaje, docstring ni test afirme "firma verificada", "clave de confianza", "autorización" ni "anclaje externo".
10. **Riesgos / rollback:** **R** presentar la estructura como verificación criptográfica; mitigación: nombres de función y mensajes explícitamente "structural". **R** añadir dependencia criptográfica por consecuencia implícita; mitigación: prohibirla en esta fase. **P** rollback = eliminar validador de sidecar; la trusted/key verification queda **aplazada**.

---

### Fase G — Integración, regresiones y auditoría independiente

1. **Archivos que se modificarían:** documentación de auditoría (nuevo informe de cierre); ningún archivo de runtime salvo ajustes localizados detectable en A–F. No se crean loader/registry/writer.
2. **Funciones y contratos afectados:** solo el wrapper público `validate_manifest` y la estabilidad de todos los mensajes; superficie de API pública sin cambios de nombre/retorno.
3. **DEC aplicables:** todos; énfasis en DEC-05 y en la separación de niveles de §10 del diseño 4.0.0.
4. **Dependencias:** A, B, C, D, E y F completadas y auditadas.
5. **Pruebas unitarias:** reejecución de todas las unidades nuevas; matriz V4-U01…U15 completa.
6. **Pruebas de integración:** fixtures 3.0.0 y 4.0.0 coexistiendo en la misma suite; manifiesto 4.0.0 completo recorriendo schema → allowlist → particiones → eventos → sidecar; ninguna ruta toca modelos, Parquet ni cuarentena.
7. **Negativas/adversariales:** paquete mixto de manifiestos de versiones distintas; manipulación simultánea de manifiesto y artefactos (documentar riesgo residual, no afirmar detección criptográfica); entradas malformadas en todos los wrappers.
8. **Regresiones verdes:** suite completa; baseline reportado históricamente como 441 tests (**NV** en esta tarea); `ruff`/`mypy` con el baseline documentado, sin nuevos diagnósticos atribuibles a los cambios.
9. **Criterios de aceptación:** todos los puntos de control de §8 firmados por auditor independiente; cero cambios en `manifest_v3.json`, Parquet y archivos de cuarentena; cero commits/push automáticos; S2 sigue sin iniciar.
10. **Riesgos / rollback:** **R** cierre "verde" sin auditoría independiente. Mitigación: CP-G obligatorio. **P** rollback = revertir el conjunto de fases en orden inverso (G→F→E→D→C→B→A), preservando 3.0.0.

---

## 6. Criterios de aceptación

### 6.1 Matriz de criterios V4-Uxx (futuros; no ejecutados)

| ID | Criterio | Fase | Estado actual |
|---|---|---|---|
| V4-U01 | 3.0.0 solo con reglas 3.0.0; 4.0.0 solo con reglas 4.0.0; versión desconocida rechazada. | A | No implementado (sin dispatch). |
| V4-U02 | `gap_rows` y `gap_source` separados, con ejemplo de filas descartadas. | D | No implementado. |
| V4-U03 | Purga en todas las fronteras con `max(H,E)`. | D | Parcial: solo `rows_between_partitions >= horizon` en v3. |
| V4-U04 | Calibration compartida con equivalencia completa; sin frontera propia. | D | Parcial: solo `row_start/row_end`. |
| V4-U05 | Timestamps duplicados/desordenados, >9 decimales y zona desconocida rechazados; UTC sin redondeo. | C/D | No implementado en provenance; parcial en `pipeline._validate_temporal`. |
| V4-U06 | Clases duplicadas, booleanos, strings y etiquetas fuera de `classes` rechazados. | B | Parcial: schema v3 usa `integer`; sin permutación ni normalización explícita. |
| V4-U07 | Transiciones fuera de tabla, estados repetidos y salidas de terminales rechazados. | E | No implementado. |
| V4-U08 | Evidence con campos desconocidos o tipos incorrectos rechazada. | B/E | No implementado (`evidence` solo objeto/null). |
| V4-U09 | Sidecars ausentes/duplicados/mal asociados rechazados; sin afirmar firma verificada. | F | No implementado. |
| V4-U10 | Cambiar ruta incluida altera fingerprint; excluida no; ausencia ≠ null. | C | No implementado (solo formato SHA-256). |
| V4-U11 | Recálculo independiente de 4 digests desde preimágenes propias. | C/E | Parcial: solo `event_sha256`. |
| V4-U12 | Wrappers públicos mantienen `list[str]` y mensajes históricos. | A/G | Condición de regresión. |
| V4-U13 | `extensions={}` aceptado; namespace no vacío rechazado; fingerprint invariante. | B/C | v3 acepta no vacío; v4 pendiente. |
| V4-U14 | Secuencia de posiciones: negativas/repetidas/no crecientes rechazadas si se entrega; límites = extremos. | D | No implementado. |
| V4-U15 | Verificador posterior reconstruye posiciones desde dataset original; **no** parte de S1. | D (contrato) / fuera de S1 | No implementado; aplazado como capacidad separada. |

### 6.2 Criterios globales de cierre

- **Hitos de código:** `git diff` sobre `manifest_v3.json` vacío; `git diff` sobre el cuerpo de los validadores v3 vacío salvo el dispatch; `git status` sin cambios en Parquet/modelos/cuarentena.
- **API:** `validate_manifest`, `validate_event`, `validate_event_chain`, `validate_schema`, `verify_event_hash` conservan nombre, firma y retorno; mensajes v3 idénticos.
- **Seguridad:** ninguna función nueva llama a `joblib.load`, `pickle`, `load_model` ni a conexión de exchange; ninguna habilita inferencia.
- **Afirmaciones:** ningún docstring, mensaje, test ni informe dice que S1 verificó firma, clave, confianza, autorización o datos originales.
- **Trazabilidad:** cada cambio cita el ID DEC y el ID V4-Uxx correspondiente.
- **NV:** la suite no se ejecutó en esta tarea; los criterios son requisitos de aceptación futura, no resultados.

---

## 7. Riesgos y dependencias

### 7.1 Orden recomendado y grafo

```
A (Aislamiento DEC-05)
├── B (Schema/DEC-01,02,03,07)
│   ├── C (JCS/fingerprint DEC-06)
│   │   └── E (Eventos DEC-07)
│   │       └── F (Sidecar DEC-07)
│   └── D (Particiones DEC-04,DEC-08)   [requiere además C para timestamps/hashes]
└── G (Integración + auditoría)  [requiere A,B,C,D,E,F]
```

C y D pueden ejecutarse en paralelo después de B, pero D consume la normalización de timestamps y las preimágenes de C; en caso de duda, ejecutar C antes que D.

### 7.2 Registro de riesgos

| ID | Riesgo | Fase | Mitigación | Rollback |
|---|---|---|---|---|
| R-01 | Fallback silencioso a v3 para versiones desconocidas. | A | `else` de rechazo + test adversarial. | Revertir dispatcher. |
| R-02 | Mutación accidental del contrato 3.0.0. | A–G | Módulos y schema separados; diff v3 vacío como criterio. | Revertir commit de fase. |
| R-03 | Deriva de la allowlist (incluir hash derivado o salida). | C | Tabla de rutas versionada y tests por ruta. | Revertir módulo de fingerprint. |
| R-04 | Doble conteo de embargo y horizonte. | D | Fórmula única `max(H,E)` sobre `gap_source`; test del ejemplo §4.2. | Revertir validación v4 de particiones. |
| R-05 | Confundir validación estructural con verificación criptográfica. | F/G | Nomenclatura "structural"; prohibición de mensajes "verified/trust/authorized". | Revertir validador de sidecar. |
| R-06 | Confundir posiciones de DataFrame con posiciones fuente OHLCV. | D/G | Coordenadas con nombres distintos; verificador de datos fuera de S1. | Revertir cambios v4 de particiones. |
| R-07 | Habilitar por consecuencia implícita loader/registry/writer/deserialización. | Todas | Lista de prohibición en el alcance de cada fase. | Revertir; no aplicar change. |
| R-08 | Extensiones no vacías filtrándose como configuración efectiva. | B/C | `extensions={}` en schema; exclusión del fingerprint. | Revertir schema v4. |
| R-09 | Divergencia de normalización de timestamps entre fingerprint, índice y eventos. | C/D/E | Única función de normalización compartida con tests comunes. | Revertir las tres áreas. |
| R-10 | Omisión de `manifest_v4.json` en `package-data`. | A/G | Criterio de aceptación explícito. | Añadir al revertir/reescribir. |
| R-11 | Entradas malformadas que lancen excepciones en vez de errores. | B–F | Patrón fail-closed de `validate_event` v3 como modelo; tests de tipos raros. | Revertir validador afectado. |
| R-12 | Inventar vectores dorados completos sin preimagen implementada. | C | Vectores completos aplazados; solo vector reducido como control JCS. | No generar artefactos. |
| R-13 | Cierre de fase sin auditoría independiente. | G | CP-A…CP-G obligatorios. | No aceptar fase. |

### 7.3 Estrategia de rollback

- **P** Cada fase se entrega en un commit atómico independiente (cuando se autorice implementar), con mensaje que cite DEC y fase.
- **P** Rollback = `git revert` del commit de la fase, **nunca** un flag en runtime que restaure v3 para una entrada `4.0.0`.
- **P** Si se revierte A, se revierten B–G en orden inverso; el wrapper queda otra vez v3-only y `4.0.0` pasa a rechazo por schema.
- **P** Ningún rollback toca `data/raw/`, modelos ni cuarentena.

---

## 8. Plan de auditoría independiente

**Principio rector (P):** una fase no se considera aceptada porque sus propios tests pasen. Cada cierre requiere un auditor distinto del implementador, con entrada propia (diff, fixtures y comandos) y un veredicto escrito.

| Punto de control | Momento | Auditoría requerida | Evidencia de salida | Criterio de paso |
|---|---|---|---|---|
| CP-0 | Antes de A | Conformidad normativa: APPROVED vigente; ninguna autorización de implementación asumida. | Verificación de `274f4cc` y de las 8 DEC. | Todo coincides con §2. |
| CP-A | Tras A | Compatibilidad 3.0.0 + rechazo de versiones desconocidas. | Diff v3 vacío; matriz de entradas de versión. | V4-U01, V4-U12. |
| CP-B | Tras B | Conformidad estructural; sin enum implícito; sin autoridad inferida. | Revisión de `manifest_v4.json` y mensajes. | V4-U08, V4-U13. |
| CP-C | Tras C | Integridad de hashes y canonicalización; allowlist exacta; ausencia vs null. | Recálculo independiente de preimágenes y vectores. | V4-U10, V4-U11; vector completo **aplazado**. |
| CP-D | Tras D | Ausencia de leakage; coordenadas fuente vs filas; purga; calibration compartida. | Tabla de fronteras y ejemplo §4.2 recalculado. | V4-U02/03/04/14/15; sin afirmación de datos originales. |
| CP-E | Tras E | Transiciones de lifecycle; orden físico; terminales; fail-closed. | Matriz de transiciones permitidas/prohibidas. | V4-U07, V4-U11. |
| CP-F | Tras F | Tratamiento de entradas malformadas; sidecar estructural; **sin** afirmación criptográfica. | Revisión de mensajes/docstrings y tests de Base64. | V4-U09. |
| CP-G | Antes del cierre | Manejo fail-closed de todos los wrappers; regresiones; alcance (sin S2/loader/inferencia/Parquet). | Suite completa + `git status` + informe de auditoría. | Todas las dimensiones siguientes en verde. |

**Dimensiones obligatorias de auditoría independiente (P):**

1. **Conformidad normativa** — cada cambio trazable a DEC-01…DEC-08 y a §§ del diseño 4.0.0; ninguna decisión reinterpretada.
2. **Compatibilidad 3.0.0** — contrato y mensajes congelados; fixtures históricas intactas; ninguna reinterpretación de manifiestos antiguos.
3. **Integridad de hashes y canonicalización** — preimagens independientes, JCS RFC 8785, LF solo en bytes de archivo, ningún digest contenido en su propia preimagen.
4. **Ausencia de leakage** — fronteras reales, `gap_source >= max(H,E)`, calibration sin frontera artificial; separación clara entre validación estructural y verificación con datos.
5. **Transiciones de lifecycle** — tabla completa, terminales, orden físico, genesis, sin reordenación.
6. **Tratamiento de entradas malformadas** — ningún traceback, errores `list[str]`, fail-closed.
7. **Manejo fail-closed** — versión desconocida, sidecar ausente/duplicado, hash divergente y evidence inválida se rechazan; no hay default permisivo.

**NV:** estos puntos de control son un plan; no se ejecutaron ni se emitió veredicto de auditoría en esta tarea.

---

## 9. Aplazamientos que permanecen

| Tema | Estado | Condición para reabrir (según aprobación §4 y diseño) |
|---|---|---|
| Catálogo cerrado de `reason_code` | Aplazado (DEC-01) | Catálogo versionado con semántica, compatibilidad y pruebas; cambio explícito de contrato. |
| Calibration independiente | Aplazada (DEC-04) | Contrato completo de partición, `fit_partition`, purga, embargo y hashes. |
| Extensiones no vacías | Aplazadas (DEC-03) | Namespaces registrados, schemas, límites de tamaño y política de sensibilidad/estabilidad. |
| Vectores dorados completos de manifiesto y fingerprint | Aplazados (DEC-06) | Implementación independiente de preimágenes/canonicalización y pruebas reproducibles. Solo se conserva el vector JCS reducido §9.5. |
| Verificación criptográfica de firmas, confianza de claves, roles, revocaciones y autorización | Aplazada / fuera de S1 (DEC-07) | Diseño e implementación de verificador criptográfico y política de autorización **fuera de S1**, con autorización separada y dependencias declaradas. |
| Verificación efectiva contra dataset original (`source_position`, límites, `index_sha256`) | Aplazada / fuera de S1 (DEC-08) | Verificador posterior con los bytes identificados por `dataset_sha256` y reglas de filtrado. |
| Loader, registry, writer, integración de pipeline, inferencia y S2 | Fuera de alcance | Autorización explícita posterior y aceptación independiente de S1. |

---

## 10. Recomendación del siguiente paso

**P** Solicitar autorización explícita y acotada para ejecutar **únicamente la Fase A** (aislamiento de versiones y dispatch), con estos entregables y límites:

1. `src/tradingai/ml/provenance.py`: dispatcher explícito por `schema_version`, sin fallback; mensajes v3 intactos.
2. `src/tradingai/schemas/manifest_v4.json` y `src/tradingai/ml/provenance_v4.py` como esqueleto mínimo que rechaza todo hasta la Fase B (o, si se prefiere, crear el schema en B; en ese caso A solo añade el rechazo explícito de `4.0.0`).
3. `pyproject.toml`: `package-data` con ambos schemas.
4. `tests/test_provenance_v4_dispatch.py`: V4-U01 y V4-U12.
5. Verificación CP-A por auditor independiente antes de pasar a B.

**No se recomienda** iniciar B–G, tocar 3.0.0, añadir dependencias, crear writer/loader o abrir S2 sin esa autorización y sin cerrar CP-A.

---

## 11. Informe final de esta tarea (R13-IMPLEMENTATION-PLAN-R1)

| Ítem | Resultado |
|---|---|
| Plan completado | **Sí** — documento `docs/aud04b_model_provenance_v4_implementation_plan_r1.md`. |
| HEAD inicial | `274f4cc0f909e360fe455c9d49f81a1a8745cd4a` |
| HEAD final | `274f4cc0f909e360fe455c9d49f81a1a8745cd4a` (idéntico; sin commits) |
| Estado Git local | Branch `main`; antes de escribir el documento, **limpio** (`git status --porcelain` sin salida). Tras escribir, el único cambio es este documento, **sin seguimiento** (`?? docs/aud04b_model_provenance_v4_implementation_plan_r1.md`). |
| Estado Git remoto | `origin/main` local = `refs/heads/main` remoto = `274f4cc0f…`, verificado por `git ls-remote` y API de GitHub. Sin push. |
| Archivos modificados/creados | Solo `docs/aud04b_model_provenance_v4_implementation_plan_r1.md` (creado). Ningún otro archivo. |
| Inspecciones realizadas | `.git` (HEAD, refs, logs, config, FETCH_HEAD, ORIG_HEAD); estado y diff Git; API de GitHub; los tres documentos normativos; `src/tradingai/ml/provenance.py` completo; `src/tradingai/schemas/manifest_v3.json` completo; `pyproject.toml`, `requirements.txt`, `.gitattributes`; `pipeline.py`, `labels.py`, `calibration.py`; `src/tradingai/ml/__init__.py`; `tests/test_provenance.py` (índice, fixture, clases y mensajes; 116 tests contados); tests de calibration/purge/leakage; scripts auxiliares de hash; listado de `data/raw/`. |
| Pruebas ejecutadas | **Ninguna.** No se ejecutó pytest, ruff, mypy ni entrenamiento. Los resultados citados de informes históricos son documentación, no verificación propia. |
| Cambios prohibidos confirmados | Sin código, schemas, tests, fixtures, dependencias, modelos, datasets, Parquet ni cuarentena modificados. Sin commits, push, S2, loader, registry, writer, deserialización ni inferencia. |
| Contradicción documental | Registrada en §3.6 (v4 §8.1 vs v3 §5.11/§8.6) sin corregir; el contrato aprobado DEC-07 prevalece para el trabajo futuro. |
| Limitaciones | No se ejecutaron pruebas; no se verificó comportamiento runtime de `jsonschema`/`rfc8785`; la auditoría y los puntos de control son propuestas; las posiciones del pipeline no se pudieron identificar con posiciones fuente OHLCV sin datos originales (no consultados). |
| Clasificación | **COMPLETADO** — plan entregado bajo las restricciones de alcance. La implementación queda **BLOQUEADA** a la espera de autorización explícita. |

**Fin de R13-IMPLEMENTATION-PLAN-R1.**
