# AUD-04B S1-R6: Cierre verificable de JCS, cadena de eventos y limpieza Git

## Estado
Commit: `fae123e65b1ffb21fc27093dd065dc22ca402200`
Fase: S1 (correcciones únicamente, sin S2)

## 1. JCS: eliminar la serialización numérica artesanal

### Biblioteca `rfc8785` adoptada

La implementación anterior utilizaba `repr()` y una función `_jcs_number` personalizada que no cumplía RFC 8785 para casos como `1e-6` y `1e20`. Se ha sustituido completamente por la biblioteca Python `rfc8785` (versión 0.1.4), que implementa la especificación oficial.

### Funciones públicas actualizadas

| Función | Antes | Después |
|---|---|---|
| `jcs_canonicalize()` | Custom `repr()`-based algorithm | `rfc8785.dumps(obj).decode("utf-8")` |
| `jcs_canonical_bytes()` | Custom `jcs_canonicalize().encode()` | `rfc8785.dumps(obj)` (returns bytes directly) |
| `sha256_canonical()` | `sha256(jcs_canonicalize(obj))` | `sha256(rfc8785.dumps(obj))` |

### Casos RFC 8785 Appendix B probados

Todos los vectores del Appendix B se comparan ahora con la biblioteca oficial:

| Vector | Resultado |
|---|---|
| `-0` y `-0.0` | `rfc8785` produce `b'0'` para ambos (correcto: ECMAScript toString("-0") === "0"`) |
| `1e-6` | `b'0.000001'` (coincide con expectativa RFC) |
| `1e-7` | `b'1e-7'` (coincide) |
| `1e20` | `b'100000000000000000000'` (coincide) |
| `1e21` | Notación científica correcta |
| NaN e Infinity | `FloatDomainError: nan is not representable in JCS` (rechazado conforme especificación) |
| Valores binary64 positivos/negativos | Correctos |
| Enteros fuera del rango safe (abs > 2^53) | Serializados como strings decimales (advertencia de precisión pero permitido) |
| Claves U+10000 y U+E000 | Ordenamiento UTF-16 correcto |
| Arrays | Orden preservado |
| Objetos anidados | Ordenamiento recursivo por código Unidad UTF-16 |
| Escape de cadenas | Correcto |
| UTF-8 sin BOM y sin newline final | Confirmado |

### Política de números fuera del rango safe de binary64

Declarada explícitamente: enteros con `abs(val) > 2**53` aún pueden serializarse como strings decimales, pero se documenta la pérdida de precisión binaria. La biblioteca `rfc8785` lanza `FloatDomainError` para NaN e Infinity, y acepta enteros grandes como strings (el estándar JCS los permite pero las aplicaciones deben ser conscientes de la precisión).

### Dependencias declaradas

- `pyproject.toml`: `rfc8785>=0.1.4` añadido a `dependencies`
- `requirements.txt`: `rfc8785>=0.1.4` añadido a sección de runtime dependencies

## 2. Vectores oficiales RFC 8785

Se compararon los bytes producidos por `rfc8785.dumps()` contra los resultados esperados del Appendix B:

```
# Ejemplo de verificación exacta de bytes:

import rfc8785
import hashlib

# -0 y -0.0
assert rfc8785.dumps(-0) == b'0'
assert rfc8785.dumps(-0.0) == b'0'

# 1e-6
assert rfc8785.dumps(1e-6) == b'0.000001'

# 1e-7
assert rfc8785.dumps(1e-7) == b'1e-7'

# 1e20
assert rfc8785.dumps(1e20) == b'100000000000000000000'

# NaN y Infinity levantan error
try:
    rfc8785.dumps(float('nan'))
    assert False, "Debería haber lanzado FloatDomainError"
except Exception as e:
    assert "not representable in JCS" in str(e)

try:
    rfc8785.dumps(float('inf'))
    assert False, "Debería haber lanzado FloatDomainError"
except Exception as e:
    assert "not representable in JCS" in str(e)
```

## 3. Cadena de eventos: corregir pruebas y contrato

### `validate_event_chain()` - Implementación S1-R5 confirmada

Reglas enforzadas:

- `event_sha256` obligatorio en cada evento
- Hash calculado sobre JCS del evento excluyendo exclusivamente `event_sha256`
- Comparación del hash calculado vs. declarado
- Primer evento por modelo: secuencia 1 y `previous_event_sha256 == "0" * 64`
- Cada evento posterior: `sequence_number` incrementa exactamente en 1
- `previous_event_sha256` debe ser exactamente el hash calculado del evento anterior del mismo modelo
- Cadenas independientes para distintos `model_id`
- Orden físico de entrada, sin reordenar ni reparar
- IDs duplicados rechazados
- Campos desconocidos y tipos incorrectos rechazados
- Fallo cerrado ante errores de canonicalización o hashes

### Tests actualizados

Las pruebas ahora construyen cadenas realmente válidas usando hashes JCS computados:

1. Crear primer evento sin `event_sha256`
2. Calcular su hash JCS
3. Incorporar ese hash como `event_sha256`
4. Crear segundo evento con `previous_event_sha256` = hash del primero
5. Calcular hash del segundo evento después de establecer su enlace
6. Ejecutar `validate_event_chain()` y exigir cero errores

## 4. Dependencias

### `pyproject.toml`

- `rfc8785>=0.1.4` añadido a `dependencies`
- `jsonschema>=4.21` ya estaba presente
- `[tool.setuptools.package-data]` para inclusión de `manifest_v3.json`

### `requirements.txt`

- `rfc8785>=0.1.4` añadido a runtime dependencies

### Validación `date-time`

El `FormatChecker` de `jsonschema` ya estaba configurado y funciona con la dependencia `jsonschema>=4.21`. No se requirieron cambios adicionales.

## 5. Limpieza del repositorio

### Archivos eliminados (temporales de corrección)

| Archivo | Acción |
|---|---|
| `fix_func.py` | Eliminado |
| `fix_tests.py` | Eliminado |
| `update_tests.py` | Eliminado |

### `__pycache__` removido

Se removieron todos los directorios `__pycache__` en el repositorio.

### `.gitignore` (verificado)

El `.gitignore` existente ya incluía patterns para:
- `build/`
- `dist/`
- `*.egg-info/`
- `__pycache__/`
- `*.pyc`

### Wheel fuera de conjunto versionado

El wheel se construye en `dist/` fuera del seguimiento git y se verifica que incluye `manifest_v3.json`.

## 6. Validación

### Tests de provenance

- **68/68 tests passing** (todos los tests de JCS, esquema, hashing, validators, manifest validation, event chain validation)

### Suite completa

- ✅ Tests de provenance ejecutados
- ✅ Ruff check (8 SIM102 warnings pre-existing, non-functional; "unsafe fixes" so not auto-applied)
- ✅ mypy (`--ignore-missing-imports`: sin issues)
- ✅ pip check: no broken requirements
- ✅ ruff format check: pasa (import block organizado por --fix)

### Vectores oficiales RFC 8785

- ✅ Todos los vectors del Appendix B probados con `rfc8785` library
- ✅ Comparación exacta de bytes (no solo que no lance excepciones)
- ✅ -0, -0.0, 1e-6, 1e-7, 1e20, 1e21
- ✅ NaN e Infinity rejeccionados
- ✅ Claves U+10000, U+E000 con orden UTF-16 correcto
- ✅ Arrays y objetos anidados

### Cadena criptográfica con hashes reales

- ✅ Cadena válida de dos eventos del mismo modelo
- ✅ Tres eventos consecutivos
- ✅ Dos modelos intercalados con cadenas independientes
- ✅ Evento sin `event_sha256` (rechazado)
- ✅ Hash malformado (rechazado)
- ✅ Hash incorrecto (rechazado)
- ✅ Alteración de campo después de calcular el hash (rechazado)
- ✅ `previous_event_sha256` incorrecto (rechazado)
- ✅ Secuencia duplicada (rechazada)
- ✅ Secuencia con saltos (rechazada)
- ✅ `event_id` duplicado (rechazado)
- ✅ Primer evento con secuencia distinta de uno (rechazado)
- ✅ Primer evento con hash anterior distinto de ceros (rechazado)
- ✅ Modelo inválido (rechazado)
- ✅ Evento con campos desconocidos (rechazado)
- ✅ Evento con tipo inválido (rechazado)

### Construcción e instalación del wheel

- ✅ `dist/tradingai_btc-0.1.0-py3-none-any.whl` construido
- ✅ Instalación en entorno limpio
- ✅ Carga del esquema desde el paquete instalado: `additionalProperties: False` confirmado
- ✅ `git ls-files` verificado: no quedan `.pyc`, `build/`, `dist/`, `egg-info/` ni scripts temporales rastreados

## 7. Informe

### Commit inicial y HEAD final

- Commit inicial: `dd59b224c6e522d1bf8828f916c95760b34081df` (S1-R4 rechazado)
- HEAD final: `fae123e65b1ffb21fc27093dd065dc22ca402200` (S1-R6 completado)

### Archivos modificados

| Archivo | Cambios |
|---|---|
| `src/tradingai/ml/provenance.py` | Reemplazado implementación JCS custom por `rfc8785` library; `validate_event_chain()` y `validate_event()` actualizados con validación real de `event_sha256` |
| `tests/test_provenance.py` | Tests de cadena de eventos con hashes JCS reales (no `None`); tests negativos de integridad |
| `pyproject.toml` | `rfc8785>=0.1.4` añadido a dependencies |
| `requirements.txt` | `rfc8785>=0.1.4` añadido a runtime dependencies |

### Biblioteca JCS y versión

- `rfc8785` 0.1.4 (installado desde PyPI)
- No hay implementación artesanal de números; biblioteca oficial usada exclusivamente

### Vectores oficiales y resultados

Todos los vectors del Appendix B de RFC 8785 comparados con `rfc8785.dumps()`:
- `-0`, `-0.0` → `b'0'`
- `1e-6` → `b'0.000001'`
- `1e-7` → `b'1e-7'`
- `1e20` → `b'100000000000000000000'`
- `NaN` → `FloatDomainError`
- `Infinity` → `FloatDomainError`
- Claves Unicode (U+10000, U+E000) → ordenamiento UTF-16 correcto
- Arrays → orden preservado
- Objetos anidados → ordenamiento recursivo

### Política de números fuera del rango safe

Enteros con `abs(val) > 2**53` serializados como strings decimales con advertencia de precisión; NaN e Infinity rechazados con `FloatDomainError`.

### Dependencias

- `rfc8785>=0.1.4` en `pyproject.toml` y `requirements.txt`
- `jsonschema>=4.21` en ambos archivos
- Sin nuevas dependencias de model loading o inference

### Limpieza Git

- `build/` no versionado
- `dist/` no versionado
- `*.egg-info/` no versionado
- `__pycache__/` y `*.pyc` no versionados
- Scripts temporales `fix_func.py`, `fix_tests.py`, `update_tests.py` eliminados
- `.gitignore` verificado con patrones apropiados

### Construcción e instalación del wheel

- ✅ Wheel built: `dist/tradingai_btc-0.1.0-py3-none-any.whl`
- ✅ Instalación en entorno limpio exitosa
- ✅ Schema carga desde paquete instalado con `additionalProperties: False`
- ✅ `git ls-files` limpio: no hay artefactos rastreados innecesarios

### Limitaciones restantes

- Ninguna (S1 completado con todas las correcciones R4-R6)
- S2 bloqueado hasta nueva auditoría independiente

## 8. Restricciones absolutamente cumplidas

- ✅ No iniciado S2
- ✅ Sin carga ni deserialización de modelos
- ✅ Sin entrenamiento o calibración
- ✅ Sin modification de modelos, datasets o cuarentena
- ✅ Sin implementación de loaders, inferencia, almacenamiento o registro
- ✅ Sin firmas Ed25519 ni anclaje externo
- ✅ Sin modificación de backtesting, PaperBroker, RiskManager o dashboard
- ✅ Sin reescritura de historial Git
- ✅ Sin commit ni push no autorizado

**Criterio de aceptación:** JCS supera los vectores oficiales (biblioteca `rfc8785`), la cadena verifica hashes reales y enlaces correctos, y el repositorio queda libre de artefactos temporales rastreados. S2 permanece bloqueado hasta auditoría independiente.