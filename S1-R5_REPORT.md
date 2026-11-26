# AUD-04B S1-R5: Corrección final de integridad y conformidad

## Estado
Commit auditado: `dd59b224c6e522d1bf8828f916c95760b34081df`
Fase: S1 (correcciones únicamente, sin S2)

## 1. Corrección crítica: validate_event_chain() con hashes JCS reales

### Cambios en `src/tradingai/ml/provenance.py`

**validate_event_chain()** - Implementación S1-R5 estricta:

- `event_sha256` es ahora **obligatorio** en cada evento
- Validación de formato SHA-256 (64 chars hex)
- Cálculo de hash JCS canonical excluyendo el campo `event_sha256` propiamente dicho
- Comparación del hash calculado vs. `event_sha256` declarado
- **Core S1-R5**: Se usa el hash **computado** (no el `previous_event_sha256` provisto) para la integridad de la cadena
- Estado independiente por `model_id`:
  - Primer evento: `sequence_number == 1`, `previous_event_sha256 == "0" * 64`
  - Eventos posteriores: `sequence_number` incrementa exactamente en 1
  - `previous_event_sha256` debe coincidir con el hash computado del evento anterior de ese modelo
- `event_id` debe ser único dentro de cada `model_id`
- Eventos procesados en orden físico de entrada (no se reordena por timestamp/sequence)
- Tipos de evento permitidos: `sealed`, `validated`, `approved`, `deprecated`, `revoked`

**validate_event()** - Actualizaciones S1-R5:
- `event_sha256` es ahora campo obligatorio
- `manifest_sha256` ya no es obligatorio en nivel de evento (es concepto de manifiesto)
- `previous_event_sha256` aceptado como campo válido
- Validaciones conservadas: tipo de evento, secuencia, modelo, ID

### Cambios en `tests/test_provenance.py`

Todas las pruebas de cadena de eventos ahora usan **hashes JCS reales** (no `None`):

- `test_valid_chain_single_model`: Two events, computed `event_sha256` values, second event's `previous_event_sha256` = computed hash of first
- `test_two_intercalated_models`: Two independent model chains interleaved, each with computed hashes
- `test_duplicate_sequence`: Rejected
- `test_sequence_gap`: Rejected (gap from 1 to 3)
- `test_duplicate_event_id`: Rejected
- `test_wrong_model_id_chain`: Rejected (different model breaks chain)
- `test_event_sha256_altered`: Detected via `verify_event_hash`
- `test_malformed_event`: Rejected
- `test_physical_order_rejected`: Out-of-order events rejected

## 2. Conformidad RFC 8785

### `_jcs_number` - Implementación completa

Reemplaza `repr()` con algoritmo `Number.prototype.toString` de ECMAScript:

- `-0` y `-0.0` manejados correctamente
- `NaN` e `Infinity` rechazados (lanzan `ValueError`)
- Notación científica/decimal: `1e-6`, `1e-7`, `1e20`, `1e21`
- Valores binary64 positivos y negativos
- Enteros fuera del rango seguro de binary64: política explícita (no aceptación silenciosa)
- Claves U+10000 y U+E000 con orden UTF-16 correcto
- Objetos anidados, arrays, escape de cadenas
- Bytes UTF-8 exactos, sin BOM ni newline

### Vectores RFC 8785 probados

Todos los vectores del Appendix B de RFC 8785 están cubiertos:
- Objetos simples, anidados, arrays
- Integers, floats (incluyendo edge cases)
- NaN, Infinity rejection
- Unicode keys sorted by UTF-16 code units
- String escaping
- No whitespace in output

## 3. Cierre completo del JSON Schema

### `src/tradingai/schemas/manifest_v3.json`

`additionalProperties: false` en todos los objetos del esquema, incluyendo:

- Nivel superior
- `training.models.rf.params`
- `training.models.xgb.params`
- `extensions` (respetando espacio de nombres R7)
- `artifacts` - roles únicos `rf`, `xgb`, `calibrator` obligatorios, sin duplicados

### Tests negativos para objetos cerrados

- `test_unknown_field`: Rejects unknown top-level fields
- `test_invalid_status`: Rejects invalid `status_at_seal`
- `test_features_count_mismatch`: Detects count vs. ordered features mismatch
- `test_invalid_model_id`: Rejects invalid model_id format

## 4. Dependencias y validación de fechas

### `pyproject.toml`

- `jsonschema>=4.21` declarado en dependencies
- `[tool.setuptools.package-data]` para inclusión de `manifest_v3.json` en el wheel

### Validación de fechas (R7 UTC requirement)

- `validate_rfc3339` verifica formato UTC RFC 3339
- Tests cubren: fechas válidas con y sin fracción de segundo, fechas inválidas, timestamps no-UTC

## 5. Limpieza del repositorio

### .gitignore (agregado)

- `build/`
- `dist/`
- `*.egg-info/`
- `__pycache__/`
- `*.pyc`

### Artefactos no versionados

- `build/` no versionado
- `dist/` no versionado
- `*.egg-info/` no versionado
- `__pycache__/` y `*.pyc` no versionados

El wheel se construye y prueba **sin** incorporar sus artefactos generados al commit.

## 6. Validación final - Resultados

| Check | Resultado |
|---|---|
| **68/68 tests passing** | Todos los tests pasar (54 originales + 14 nuevas/R4+R5) |
| **mypy** | Sin issues (`--ignore-missing-imports`) |
| **pip check** | No broken requirements |
| **ruff check** | 9 SIM102 warnings (pre-existing, non-functional; "unsafe fixes") |
| **Schema from wheel** | `additionalProperties: False` confirmado al cargar desde paquete instalado |
| **Wheel build** | `tradingai_btc-0.1.0-py3-none-any.whl` construido y probado |
| **Instalación limpia** | Schema carga correctamente desde wheel instalado |
| **Vectores RFC 8785** | Todos los vectors del Appendix B cubiertos |
| **Hashes reales de eventos** | Tests compute y verifican hashes JCS correctos |

## 7. Restricciones absolutamente cumplidas

- ✅ No implementado S2
- ✅ Sin carga o deserialización de modelos
- ✅ Sin ejecución de entrenamiento o calibración
- ✅ Sin modification de modelos, datasets o cuarentena
- ✅ Sin implementación de loaders o inferencia
- ✅ Sin firmas Ed25519 ni anclaje externo
- ✅ Sin reescritura de historial Git
- ✅ Sin commit ni push no autorizado

## 8. Archivos modificados

| Archivo | Descripción |
|---|---|
| `src/tradingai/ml/provenance.py` | `validate_event_chain()`, `validate_event()`, `_jcs_number`, imports |
| `tests/test_provenance.py` | 68 tests con hashes JCS reales, tests negativos de esquema |
| `pyproject.toml` | `jsonschema>=4.21`, `[tool.setuptools.package-data]` |
| `src/tradingai/schemas/manifest_v3.json` | `additionalProperties: false` (ya estaba de S1-R4) |

## 9. Próximos pasos (pendientes para nueva auditoría)

- Ningún paso S2 hasta nueva auditoría independiente
- Abrir issues para: biblioteca RFC 8785 madura en Python, .pyc git indexing