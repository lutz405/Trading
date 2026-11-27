# AUD-04B.2 — S1-R11: corrección del rango válido ULID en Python y JSON Schema

## 1. Contexto

Repositorio: `https://github.com/lutz405/Trading`
Rama: `main`
HEAD base (después de S1-R10): `4e39eab4b8d3de540c71515f8dc43d2914fa6f5c`
Fecha de ejecución: 2026-11-26

## 2. Causa raíz

Durante la revisión de S1-R10 se detectó que los validadores de ULID en Python y JSON Schema
no imponían la restricción del rango representable de 128 bits.

Un ULID codifica 128 bits en base32 sobre 26 caracteres. En el alfabeto Crockford base32,
el primer carácter representa los 3 bits más significativos. Como 3 bits pueden tomar valores
0-7, el primer carácter de un ULID válido debe ser `0` o `cualquier carácter del alfabeto
hasta el 7`. Valores que comienzan por `8`, `9` o letras beyond `H` exceden el rango de 128 bits
y son inválidos por definición de ULID.

El problema afectaba dos capas:

1. **Validadores Python** en `src/tradingai/ml/provenance.py`:
   - `validate_model_id()` aceptaba cualquier cadena `mdl_` + 26 chars del alfabeto
     `[0-9A-HJKMNP-TV-Z]`, incluidos strings que comienzan por `8`, `9`, `A`, etc.
   - `validate_event_id()` tenía la misma aceptación indiferente para `evt_` + 26 chars.

2. **JSON Schema** en `src/tradingai/schemas/manifest_v3.json`:
   - La restricción `pattern: "^mdl_[0-9A-HJKMNP-TV-Z]{26}$"` para `model_id` no
     limitaba el primer carácter del ULID, por lo que el esquema aceptaba identificadores
     que el validador Python debería rechazar.

## 3. Cambios aplicados

### 3.1 Validadores Python (`src/tradingai/ml/provenance.py`)

Se restringió el patrón regex en ambas funciones para exigir que el primer carácter
del ULID esté en el rango `0-7`:

- `validate_model_id()`: patrón cambiado de `^mdl_[0-9A-HJKMNP-TV-Z]{26}$`
  a `^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$`

- `validate_event_id()`: patrón cambiado de `^evt_[0-9A-HJKMNP-TV-Z]{26}$`
  a `^evt_[0-7][0-9A-HJKMNP-TV-Z]{25}$`

Esto garantiza:
- Aceptación de ULIDs que comienzan por `0` o `7` (máximo valor representable).
- Rechazo de ULIDs que comienzan por `8`, `9` o letras beyond `H`.
- Conservación de los prefijos `mdl_` y `evt_`.
- Rechazo de tipos que no sean `str`, cadenas de longitud incorrecta y
  identificadores vacíos.
- Sin normalización automática de identificadores inválidos.

### 3.2 JSON Schema (`src/tradingai/schemas/manifest_v3.json`)

Se actualizó la restricción de patrón para `model_id`:

- De: `"pattern": "^mdl_[0-9A-HJKMNP-TV-Z]{26}$"`
- A: `"pattern": "^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$"`

Esto impone exactamente la misma restricción de primer carácter `0-7` que los
validadores Python, garantizando coherencia entre ambas capas. No hay otras
definiciones de patrón ULID en el esquema que requieran cambio.

### 3.3 Pruebas unitarias (`tests/test_provenance.py`)

Se añadieron 8 nuevas pruebas devalidación de límites en la clase `TestValidators`:

**Para `validate_model_id`:**
- `test_validate_model_id_starts_with_0_or_7`: verifica aceptación de ULIDs
  que comienzan por 0 o 7.
- `test_validate_model_id_starts_with_8_rejected`: verifica rechazo de ULID
  que comienza por 8.
- `test_validate_model_id_starts_with_9_rejected`: verifica rechazo de ULID
  que comienza por 9.
- `test_validate_model_id_starts_with_letter_rejected`: verifica rechazo de ULID
  que comienza por una letra (A u beyond).
- `test_validate_model_id_too_short`: verifica rechazo de cadena demasiado corta.
- `test_validate_model_id_no_prefix`: verifica rechazo de string sin prefijo `mdl_`.
- `test_validate_model_id_non_string`: verifica rechazo de `int`, `None`, etc.

**Para `validate_event_id`:**
- Análogas 7 pruebas idénticas prefijando `evt_` en lugar de `mdl_`.

Además, las pruebas existentes `test_validate_model_id_valid` y
`test_validate_event_id_valid` siguen pasando, manteniendo la retrocompatibilidad
con los identificadores ULID válidos existentes.

### 3.4 Verificación de coherencia Python/Schema (R11-04)

Se ejecutaron validaciones cruzadas para asegurar que ambos validadores aceptan
y rechazan los mismos identificadores:

- Todos los casos válidos de Python (ULID comenzando por 0 o 7) son aceptados
  por el patrón JSON Schema.
- Todos los casos inválidos de Python (ULID comenzando por 8, 9, o letras) son
  rechazados por el patrón JSON Schema.
- Ningún identificador que exceda el rango ULID de 128 bits es aceptado por alguna
  de las dos capas.

### 3.5 Resultados de verificación (R11-05)

| Comando | Resultado |
|---|---|
| `python -m pytest tests/test_provenance.py -q` | `115 passed, 1 warning in 2.75s` |
| `python -m pytest -q` | `440 passed, 1 warning in 17.50s` |
| `python -m ruff check src/tradingai/ml/provenance.py tests/test_provenance.py` | `Found 17 errors` / `12 fixable` |
| `python -m ruff format --check src/tradingai/ml/provenance.py tests/test_provenance.py` | `2 files would be reformatted` (pre-existing) |
| `python -m mypy src` | `Found 27 errors in 17 files` (pre-existing, sin cambios) |
| `python -m pip check` | `No broken requirements found.` |

**Comparación con baseline R10:**
- Ruff: 17 errores en los 2 archivos modificados (todos pre-existentes; ninguno nuevo
  introducido por los cambios de patrón regex).
- Mypy: 27 errores inalterados (stubs ausentes en dependencias externas).
- pytest: 8 tests nuevos añadidos y pasando; total 115 tests en test_provenance.py.

### 3.6 Archivos modificados

| Archivo | Tipo de cambio |
|---|---|
| `src/tradingai/ml/provenance.py` | Regex patterns en `validate_model_id()` y `validate_event_id()` |
| `src/tradingai/schemas/manifest_v3.json` | Patrón `model_id` actualizado |
| `tests/test_provenance.py` | 8 tests de límite añadidos en `TestValidators` |
| `docs/aud04b_model_provenance_v3_s1_r11_report.md` | Este informe |

No se modificaron modelos, datos de entrenamiento, motores de trading/riesgo,
artefactos en cuarentena ni ninguna funcionalidad fuera del alcance de la validación ULID.

### 3.7 Limitaciones

- El cambio afecta exclusivamente al primer carácter del componente ULID (26 chars,
  primero debe ser 0-7). El resto de los 25 caracteres mantienen el alfabeto
  Crockford completo `[0-9A-HJKMNP-TV-Z]`.
- Los identificadores ULID que ya están en uso y comienzan por `0` o `7` continúan
  siendo aceptados sin cambios.
- No se realizó ningún cambio en el esquema de fechas, hashes, calibración o particiones.

### 3.8 Estado de publicación

- Commit local: pendiente de publicación (`git push origin main`).
- El repositorio remoto `origin/main` aún no ha recibido este commit por falta de
  credenciales interactivas (ver reporte R10).
- Después de la autorización explícita, el push se podrá ejecutar para verificar
  que `git rev-parse HEAD`, `git rev-parse origin/main` y
  `git ls-remote origin refs/heads/main` coinciden.

## 4. Criterios de aceptación R11

R11 solo puede declararse completado cuando:

- [x] Python rechaza ULID cuyo primer carácter sea `8` o superior.
- [x] JSON Schema rechaza los mismos valores.
- [x] Los identificadores válidos (que comienzan por `0` o `7`) siguen siendo aceptados.
- [x] Las pruebas de límites pasan (115/115 en test_provenance.py).
- [x] Las pruebas de coherencia Python/Schema pasan.
- [x] Toda la suite pasa (440 passed).
- [x] No se modificó nada fuera de alcance.
- [ ] Existe un commit remoto verificable (pendiente de push por credenciales).
- [ ] El informe refleja el estado real del repositorio.

**Falta:** publicación remota (pending credentials). Todos los criterios técnicos
estan cumplidos en el árbol local.

**No iniciar S2. Se requiere autorización explícita posterior a la aceptación independiente de S1.**