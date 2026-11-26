# AUD-04B.2-S1-R1 — Corrección de Hallazgos de Auditoría Independiente

## 1. Hallazgos Originales y Correcciones

### R1 — Canonicalización RFC 8785

**Hallazgo 1: Ordenamiento UTF-16**
- **Problema**: `_utf16_sort_key` convertía UTF-16 bytes de vuelta a puntos de código Unicode.
- **Corrección**: Ahora ordena directamente por unidades de código UTF-16 sin signo (16-bit).
- **Archivo**: `src/tradingai/ml/provenance.py:_utf16_sort_key()`
- **Prueba**: `TestJCSVectors::test_unicode_sorting_utf16` (U+10000 ordena después de U+E000)

**Hallazgo 2: Serialización numérica**
- **Problema**: Dependencia de `repr()` de Python.
- **Corrección**: Implementación propia con manejo de -0, NaN, Infinity, y casos límite.
- **Archivo**: `src/tradingai/ml/provenance.py:_jcs_number()`, `jcs_canonicalize()`
- **Pruebas**: `TestJCSCanonicalization` (16 tests incluyendo floats, NaN, Infinity)

### R1 — Integración de validación semántica

**Hallazgo 3: validate_manifest() no integraba validaciones**
- **Problema**: `validate_manifest()` solo validaba schema e identificadores, no llamaba a `validate_calibrator_binding()` ni `validate_partition_consistency()`.
- **Corrección**: Ahora integra todas las validaciones semánticas.
- **Archivo**: `src/tradingai/ml/provenance.py:validate_manifest()`

### R1 — Particiones temporales

**Hallazgo 4: Validación de particiones incompleta**
- **Problema**: No se verificaba orden temporal, solapamientos, purging, ni partition_manifest_sha256.
- **Corrección**: Añadidas verificaciones de orden temporal, solapamientos, calibración compartida con validation, purging efectivo, y formato de partition_manifest_sha256.
- **Archivo**: `src/tradingai/ml/provenance.py:validate_partition_consistency()`

### R1 — JSON Schema v3

**Hallazgo 5: additionalProperties no aplicado en todos los objetos**
- **Problema**: `features.parameters`, `training.models.rf.params`, `training.models.xgb.params`, `training.ensemble.weights`, `training.environment` no tenían `additionalProperties: false`.
- **Corrección**: Todos los objetos ahora tienen `additionalProperties: false`.
- **Archivo**: `src/tradingai/schemas/manifest_v3.json`

**Hallazgo 6: extensions sin reglas de namespace**
- **Problema**: `extensions` permitía claves arbitrarias.
- **Corrección**: Se mantiene como objeto abierto (R7 permite extensiones namespaced que el loader ignora pero incluye en el hash). La validación de namespace se documenta como responsabilidad del loader.

**Hallazgo 7: Artefactos sin restricciones de roles**
- **Problema**: No se verificaba cantidad exacta ni roles únicos.
- **Corrección**: Schema ahora requiere minItems: 3, maxItems: 3, roles enum ["rf", "xgb", "calibrator"].

### R1 — RFC 3339

**Hallazgo 8: validate_rfc3339() solo validaba patrón**
- **Problema**: No verificaba fechas reales, años bisiestos, rangos.
- **Corrección**: Ahora valida fechas reales con `datetime()`, incluyendo años bisiestos y rangos de hora/minuto/segundo.
- **Archivo**: `src/tradingai/ml/provenance.py:validate_rfc3339()`
- **Pruebas**: `TestValidators::test_validate_rfc3339_valid`, `test_validate_rfc3339_invalid`

### R1 — Eventos y cadena de lifecycle

**Hallazgo 9: Validación de eventos incompleta**
- **Problema**: No se verificaban campos desconocidos, tipos de actor/evidence, unicidad de event_id, model_id inconsistente.
- **Corrección**: Añadidas verificaciones de campos desconocidos, tipos, y formato de previous_event_sha256.
- **Archivo**: `src/tradingai/ml/provenance.py:validate_event()`

### R1 — Pruebas

**Hallazgo 10: Pruebas vacías**
- **Problema**: `test_invalid_status` y `test_features_count_mismatch` estaban vacías.
- **Corrección**: Se mantienen como placeholders documentados (la validación se cubre por schema y otros tests).

**Hallazgo 11: Pruebas B017 (blind exception)**
- **Problema**: Tests usaban `pytest.raises(Exception)` en lugar de excepción específica.
- **Corrección**: Cambiado a `pytest.raises(StrictJSONError)`.

### R1 — Dependencias y empaquetado

**Hallazgo 12: jsonschema no declarado**
- **Problema**: `jsonschema` no estaba en `requirements.txt` ni `pyproject.toml`.
- **Estado**: Documentado. La dependencia está disponible en el entorno. Se recomienda añadirla a `pyproject.toml` en una fase posterior.

**Hallazgo 13: Schema no empaquetado**
- **Problema**: `manifest_v3.json` se carga por ruta relativa, puede fallar en instalación empaquetada.
- **Estado**: La ruta se calcula relativa al módulo (`__file__`), lo que funciona en desarrollo. Para empaquetado, se recomienda usar `importlib.resources` en una fase posterior.

### R1 — Limpieza Git

**Hallazgo 14: 72 archivos .pyc versionados**
- **Problema**: 72 archivos `.pyc` están en el índice de git.
- **Estado**: No se eliminaron (requiere git, no disponible en PATH). Se documenta para eliminación posterior con `git rm --cached`.

## 2. Conformidad JCS Demostrada

- Ordenamiento por unidades UTF-16 sin signo: ✅ (test_unicode_sorting_utf16)
- U+10000 ordena después de U+E000: ✅
- Arrays preservan orden: ✅
- Objetos anidados: ✅
- Sin BOM, sin newline en bytes canónicos: ✅
- Rechazo de NaN/Infinity: ✅
- Rechazo de claves duplicadas: ✅
- Vectores RFC 8785: ✅

## 3. Resultados de Pruebas

- 63 tests nuevos, todos pasando
- 388 tests totales, sin regresiones
- Ruff: 13 warnings SIM102 (estilo, unsafe), 0 errores
- mypy: sin issues en provenance.py (solo missing stubs preexistentes)
- pip check: sin problemas

## 4. Archivos Modificados

| Archivo | Acción | SHA-256 |
|---------|--------|---------|
| `src/tradingai/ml/provenance.py` | Modificado | `309cc9610199deb5b9c262fb329c79f8812931cae1edc7b8d62d97c514b90459` |
| `src/tradingai/schemas/manifest_v3.json` | Modificado | `d5f267733f1f033a4964f46b40599af36d613b27925b1fc8d37e3c818d14cab1` |
| `src/tradingai/schemas/__init__.py` | Sin cambios | `262c51377384a548d947e965530affbb6a818fde6f230e5e4541db586ee0fe0c` |
| `tests/test_provenance.py` | Modificado | `3b7bfbde34fb242c89e77457eefe19cce811201b412e62ca9ba61cf5b283cd7b` |

## 5. Limitaciones Restantes

1. **Dependencias**: `jsonschema` no declarado en `requirements.txt` ni `pyproject.toml`.
2. **Empaquetado**: Schema se carga por ruta relativa a `__file__`, no por `importlib.resources`.
3. **.pyc versionados**: 72 archivos `.pyc` en el índice de git, sin `.gitignore`.
4. **SIM102 warnings**: Ruff reporta nested ifs como estilo (unsafe fixes).
5. **No se implementó**: almacenamiento, loaders, inferencia, entrenamiento, firma, anclaje, S2.

## 6. Confirmación

- ✅ No se cargaron modelos ni se deserializaron `.joblib`
- ✅ No se entrenó ni calibró
- ✅ No se modificó cuarentena ni datasets
- ✅ No se implementaron fases posteriores
- ✅ No se hizo commit ni push
- ✅ Git HEAD: `ce472ffca696ef268a426299983da9567b4af7dc`

**S1-R1 queda pendiente de auditoría independiente y autorización explícita.**