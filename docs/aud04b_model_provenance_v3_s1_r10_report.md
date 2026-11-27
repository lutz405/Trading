# AUD-04B.2 — S1-R10: cierre de validación de procedencia e higiene del repositorio

## Estado

- Repositorio: `C:\Users\USER\Documents\GitHub\Trading`
- Rama: `main`
- HEAD inicial (antes de los cambios de R10): `12d1d8b51f434fba841a8c20aae95caee29bf60e`
- Remoto: `https://github.com/lutz405/Trading.git`
- Fecha de ejecución: 2026-11-26
- Alcance: S1 exclusivamente. S2 no fue iniciado.

Este informe no constituye una auditoría independiente: documenta la ejecución
interna de las comprobaciones de S1-R10. El hash completo del commit de
publicación no puede figurar dentro del propio commit que crea este archivo; se
registra en la entrega final y se verifica con `git rev-parse HEAD`.

---

## 1. R10-01 — Fixtures ULID

Los dos fallos de la suite de procedencia eran fixtures inválidos, no defectos
del validador:

- IDs de evento de 27 caracteres en lugar de 26.
- Uso de `L`, excluida del alfabeto ULID (`0-9A-HJKMNP-TV-Z`).

Corrección aplicada únicamente a los fixtures:

| Antes | Después |
|---|---|
| `evt_...J9L0` | `evt_...J9M` |
| `evt_...J9L1` | `evt_...J9N` |
| `evt_...J9L2` | `evt_...J9P` |

Se conservaron las pruebas negativas `evt_123` y `mdl_DIFFERENT`, y
`validate_event()` sigue rechazando IDs mal formados. Todos los IDs únicos de
los fixtures son de 26 caracteres y usan el alfabeto permitido.

Resultado: `tests/test_provenance.py` pasó de `78 passed, 2 failed` a
`107 passed`; la suite completa pasó de `403 passed, 2 failed` a `432 passed`.

---

## 2. R10-02 — Endurecimiento de `validate_event()` y `validate_event_chain()`

### 2.1 Validadores de formato

`validate_model_id()`, `validate_event_id()` y `validate_sha256()` aceptan
`object` y devuelven `False` para cualquier valor que no sea `str`, sin lanzar
`TypeError`/`AttributeError`.

### 2.2 `validate_event()`

- Un evento que no es `dict` devuelve `['Event must be a JSON object']`.
- `previous_event` no-dict produce `previous_event must be a JSON object`.
- `previous_event` sin `sequence_number` entero produce
  `previous_event has invalid sequence_number`; no se evalúa `sequence - 1`
  sobre tipos no enteros.
- Se mantiene la validación estricta existente: campos requeridos, campos
  desconocidos, ULID, SHA-256, RFC 3339 UTC, tipo de evento, `actor` string,
  `evidence` objeto/null.
- `manifest_sha256` sigue siendo opcional a nivel de evento y, si está
  presente, se valida como SHA-256; está incluido en `allowed_fields`.

### 2.3 `validate_event_chain()`

La implementación anterior duplicaba comprobaciones de `validate_event()` y
podía lanzar excepciones con entradas malformadas. La versión R10:

- Rechaza entradas que no son lista:
  `['Event chain must be a list of events']`.
- Rechaza elementos que no son objeto con
  `Event {idx}: event must be a JSON object`, sin acceso a atributos.
- Delega la validación de campos en `validate_event(..., skip_first_event_check=True)`;
  no duplica required/unknown/formatos/tipos.
- Mantiene estado independiente por `model_id`, con `next_sequence` que avanza
  a `sequence + 1` (soporta cadenas válidas de tres o más eventos).
- Solo asigna eventos a una cadena cuando `model_id` es `str`; IDs no
  hashables no llegan a diccionarios/sets.
- Solo compara `event_sha256` declarado cuando es `str`.
- Calcula el hash JCS dentro de un bloque controlado que captura
  `AttributeError`, `OverflowError`, `RecursionError`, `TypeError` y `ValueError`
  (incluye los errores de `rfc8785`), reportando
  `error computing JCS hash` en lugar de propagar la excepción.
- Conserva el orden físico de inserción: no ordena, no repara y no reordena.
- Verifica secuencia, `previous_event_sha256 == '0'*64` en el primer evento,
  enlace con el hash **computado** del evento anterior y unicidad de
  `event_id` por `model_id`.

Se añadieron 20 pruebas en `TestEventValidationHardening`, incluidas:

- cadena válida de tres eventos;
- hash previo incorrecto;
- evento intermedio manipulado;
- orden físico invertido;
- campos faltantes/desconocidos;
- `model_id`/`event_id` no hashables;
- hash declarado no string;
- timestamp imposible y hash con caracteres inválidos;
- payload recursivo.

Además se ejecutó un script de sondeo con valores `None`, booleanos, enteros,
flotantes (`nan`, `inf`), strings, listas, dicts, `object()`, `bytes`, tuplas,
campos ausentes y `previous_event` malformados: todas las llamadas devolvieron
listas de error sin excepciones (`OK: all malformed inputs returned error lists
without exceptions`).

---

## 3. R10-03 — Artefactos generados fuera del índice de Git

Se eliminaron explícitamente del índice (no del disco) 49 archivos:

- `analyze.py`, `fix2.py`, `compute_hash.py`, `compute_hash2.py`,
  `unicode_result.txt` (5).
- `build/lib/tradingai/**` (38).
- `dist/tradingai_btc-0.1.0-py3-none-any.whl` (1).
- `src/tradingai_btc.egg-info/*` (5).

Comando: `git rm -r --cached build dist src/tradingai_btc.egg-info analyze.py
fix2.py compute_hash.py compute_hash2.py unicode_result.txt`.

Actualización de `.gitignore`:

- Se eliminó la exclusión de `docs/aud04b_model_provenance_v3_s1_r8_report.md`.
- Se añadieron las rutas de los scripts temporales de la raíz.

Verificación:

- `git ls-files` para todos esos artefactos devuelve **0** entradas.
- Los archivos de la raíz siguen existiendo en disco, ahora ignorados.
- Los parquet de `data/` y los artefactos en cuarentena `models/_t*` se
  conservaron sin cambios (39 rutas de `data`/`models` siguen bajo seguimiento).

---

## 4. R10-04 — Informes R8 y R9

### 4.1 Informe R8

El informe R8 existía localmente pero estaba excluido por `.gitignore`. Se
publica **sin modificar su contenido**, con estos datos verificables:

- Ruta: `docs/aud04b_model_provenance_v3_s1_r8_report.md`
- Tamaño: 13 936 bytes
- Líneas: 320
- SHA-256: `407080b8ffe9d61a6c104d32b5356762dfcbb8fff72b60511e163f450ac1561c`

El informe se publica como artefacto histórico recuperado. Sus afirmaciones no
fueron verificadas de forma independiente y, según la revisión de R10, algunas
de las pruebas que declara no están presentes en el árbol; R10 no las avala.

### 4.2 Informe R9

Se añadió un banner de corrección al inicio del informe R9 (sin reescribir su
cuerpo) que indica:

- R9-02/R9-03/R9-04 no coinciden con el árbol publicado.
- El cambio de `additionalProperties` de R9 se aplicó en un bloque `training`
  de nivel superior sin efecto sobre las rutas reales.
- Los hashes de HEAD del informe son incorrectos.
- El HEAD real al iniciar R10 era `12d1d8b51f434fba841a8c20aae95caee29bf60e`.

---

## 5. R10-06 — Vectores JCS, delegación y cierre de esquema

### 5.1 Vectores JCS (salida exacta)

```text
JCS 1e-6: '0.000001' expected '0.000001' [OK]
JCS 1e-7: '1e-7' expected '1e-7' [OK]
JCS 1e20: '100000000000000000000' expected '100000000000000000000' [OK]
JCS 1e21: '1e+21' expected '1e+21' [OK]
JCS -0.0: '0' expected '0' [OK]
JCS 2**53-1: '9007199254740991' expected '9007199254740991' [OK]
JCS -(2**53-1): '-9007199254740991' expected '-9007199254740991' [OK]
Unicode key order: ['0x10000', '0xe000']
UTF-8 bytes: b'{"k":"\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xe2\x82\xac\xf0\x90\x80\x80"}'
rfc8785 delegation: OK
Integer 9007199254740992: rejected (IntegerDomainError)
Integer 9007199254740993: rejected (IntegerDomainError)
Integer -9007199254740993: rejected (IntegerDomainError)
Schema rf.params: closed, known params accepted, unknown rejected
Schema xgb.params: closed, known params accepted, unknown rejected
Schema string field vol_mult: string accepted, number rejected
OK: all R10-06 vectors and schema checks passed
```

Comprobaciones cubiertas:

- Notación numérica ECMAScript exacta (`1e-6`, `1e-7`, `1e20`, `1e21`, `-0.0`).
- Orden de claves UTF-16: U+10000 antes que U+E000.
- UTF-8 sin BOM y sin salto de línea final.
- `jcs_canonical_bytes()` es exactamente `rfc8785.dumps()` (delegación real,
  sin reimplementación).
- Entradas recursivas y objetos profundamente anidados (100 niveles).
- Política de enteros: fuera de `±(2**53-1)` se rechaza con
  `IntegerDomainError`, que es subclase de `ValueError` y por tanto se
  clasifica como error controlado.

### 5.2 Cierre de esquema

Se eliminó el bloque `training` de nivel superior que R9 había añadido por
error (no era una ruta efectiva del esquema). En las rutas reales:

- `properties.training.properties.models.properties.rf.properties.params`:
  `additionalProperties: false` con cinco claves de `config/ml.yaml`
  (`n_estimators`, `max_depth`, `class_weight`, `random_state`, `n_jobs`).
- `properties.training.properties.models.properties.xgb.properties.params`:
  `additionalProperties: false` con las seis claves de `config/ml.yaml`
  (`n_estimators`, `max_depth`, `learning_rate`, `subsample`,
  `colsample_bytree`, `random_state`) más seis claves usadas por la ruta de
  entrenamiento XGBoost en `src/tradingai/ml/pipeline.py` (`tree_method`,
  `device`, `objective`, `num_class`, `eval_metric`, `n_jobs`).
- Tipos estrictos: `integer`, `number`, `string`, con `minimum`/`maximum` donde
  corresponde.
- Los parámetros desconocidos se rechazan en ambas rutas.
- El campo string `target.vol_mult` acepta `"0.5"` y rechaza `0.5`.
- `training` ya no existe como palabra clave de nivel superior en
  `MANIFEST_SCHEMA`.

Pruebas añadidas: `test_schema_has_no_orphan_training_block`,
`test_rf_params_are_closed`, `test_xgb_params_are_closed`,
`test_decimal_string_field_rejects_number`, `test_jcs_delegates_to_rfc8785`,
`test_jcs_utf8_encoding_without_bom`, `test_jcs_deeply_nested_recursion`.

---

## 6. R10-05 — Verificación final

Comandos ejecutados sobre el árbol final, con salida exacta:

| Comando | Resultado |
|---|---|
| `python -m pytest -q` | `432 passed, 1 warning in 15.82s` |
| `python -m pytest tests/test_provenance.py -q` | `107 passed, 1 warning in 3.79s` |
| `python -m ruff check .` | `Found 62 errors.` / `40 fixable with --fix` |
| `python -m ruff format --check .` | `34 files would be reformatted, 58 files already formatted` |
| `python -m mypy src` | `Found 27 errors in 17 files (checked 37 source files)` |
| `python -m pip check` | `No broken requirements found.` |

### 6.1 Clasificación de Ruff (nuevos vs. preexistentes)

Línea base antes de R10: `69 errors`, `42 fixable`.
Final: `62 errors`, `40 fixable`.

- **Nuevos hallazgos: 0.**
- `src/tradingai/ml/provenance.py`: 7 → 6 (se eliminó un `SIM102` al reescribir
  la cadena; los 6 restantes son preexistentes).
- `tests/test_provenance.py`: 9 → 9 (sin cambios en el conjunto de reglas).
- `src/tradingai/schemas/manifest_v3.json`: 0 → 0.
- Los 6 hallazgos restantes de la diferencia corresponden a `analyze.py`,
  `compute_hash.py` y `compute_hash2.py`, ahora excluidos por `.gitignore`
  (los archivos siguen en disco, pero ya no están bajo seguimiento).
- Los 62 hallazgos restantes son preexistentes y no se abordan en R10 para no
  ampliar el alcance.

`ruff format --check`: 38 → 34 archivos. La diferencia son exactamente los
cuatro scripts de la raíz ahora ignorados (`analyze.py`, `compute_hash.py`,
`compute_hash2.py`, `fix2.py`). Ningún archivo nuevo pasa a estar sin
formatear; `provenance.py` y `tests/test_provenance.py` ya estaban sin
formatear antes de R10 y se mantienen así (no se reformateó el repositorio).

### 6.2 mypy

`python -m mypy src` produce los mismos 27 errores en 17 archivos antes y
después de R10, todos por stubs ausentes (`import-untyped`) en dependencias.
No hay errores nuevos ni cambios en `provenance.py` (1 error preexistente por
`jsonschema`).

Comprobación adicional documentada, no sustitutiva:
`python -m mypy --ignore-missing-imports src` →
`Success: no issues found in 37 source files`.

### 6.3 pip check

Sin dependencias rotas antes ni después.

---

## 7. R10-07 — Integridad del alcance

Archivos modificados por R10:

- `.gitignore`
- `src/tradingai/ml/provenance.py`
- `src/tradingai/schemas/manifest_v3.json`
- `tests/test_provenance.py`
- `docs/aud04b_model_provenance_v3_s1_r9_report.md` (banner de corrección)
- `docs/aud04b_model_provenance_v3_s1_r8_report.md` (publicado sin cambios)
- `docs/aud04b_model_provenance_v3_s1_r10_report.md` (este informe)
- 49 eliminaciones de artefactos generados del índice

No se modificaron broker, riesgo, backtesting, dashboard, entrenamiento,
inferencia, trading en vivo ni los modelos en cuarentena. No se inició S2 ni se
añadieron almacenamiento inmutable, registro, bloqueos, staging, publicación
atómica o ciclos de vida adicionales.

---

## 8. R10-08 — Publicación

- Mensaje de commit: `AUD-04B.2-S1-R10: finalize provenance validation and repository hygiene`
- `git diff --check` y `git diff --cached --check`: sin errores (solo avisos
  informativos de conversión LF/CRLF).
- El commit se crea después de redactar este informe; su hash completo se
  registra en la entrega final y se verifica contra `origin/main` con
  `git rev-parse HEAD`, `git rev-parse origin/main` y
  `git ls-remote origin refs/heads/main`.

## Criterios de aceptación

| Criterio | Estado |
|---|---|
| R10-01 fixtures ULID y suite sin fallos | Cumplido |
| R10-02 validación endurecida y fail-closed | Cumplido |
| R10-03 artefactos fuera del índice | Cumplido |
| R10-04 informes R8/R9/R10 veraces | Cumplido en este árbol |
| R10-05 seis comandos ejecutados y clasificados | Cumplido |
| R10-06 JCS, rfc8785 y cierre de esquema | Cumplido |
| R10-07 alcance sin cambios indebidos | Cumplido |
| R10-08 commit y push verificados | Pendiente al redactar; se declara en la entrega final |

La declaración final de S1-R10 completado solo es válida si la publicación
termina correctamente y el HEAD remoto coincide con el commit local.
