# AUD-04B.2-S1-R12 — Cierre de consistencia ULID en referencias y pruebas de límite

## Estado

- Alcance: corrección puntual de S1; no se inició S2.
- HEAD base obligatorio: `f128bdab681d859e61f0b0dc85be7132ed8020c7`.
- Commit base: `AUD-04B.2-S1-R11: enforce ULID 128-bit range`.
- El remoto `main` fue comprobado antes del cambio y apuntaba al HEAD base obligatorio.

## Cambios realizados

### R12-01 — Referencia `base_model_id`

Se añadió a `calibration.properties.base_model_id` el mismo patrón que usa `model_id`:

```text
^mdl_[0-7][0-9A-HJKMNP-TV-Z]{25}$
```

La revisión de referencias del esquema encontró solo dos campos que representan un identificador de modelo: `model_id` y `calibration.base_model_id`. Ambos aplican ahora el patrón ULID. Los otros campos de identificación conservan sus contratos propios.

### R12-02 — Pruebas de límites y coherencia

Se corrigió `test_validate_event_id_starts_with_0_or_7`: el segundo ID empieza ahora por `7`. Las pruebas de Python ya incluyen los límites `0`, `7`, `8`, `9` y `A` para `event_id` y `model_id`.

Se añadió `test_model_id_reference_schemas_match_python_validator`, que compara el validador Python con las definiciones JSON Schema tanto para `model_id` como para `base_model_id`, usando esos cinco límites.

### Conteo exacto de cambios de pruebas

| Tipo | Métodos | Casos/assertions |
|---|---:|---:|
| Añadidos | 1 | 5 IDs límite, comprobados contra Python y ambas referencias JSON Schema (15 comprobaciones de validez) |
| Modificados | 1 | 1 valor de prueba cambiado de prefijo `0` a `7`; el caso `0` permanece |
| Eliminados | 0 | 0 |

## Verificación

Comandos ejecutados en este árbol de trabajo:

| Comando | Resultado |
|---|---|
| `python -m pytest tests/test_provenance.py -q` | `116 passed, 1 warning in 5.20s` |
| `python -m pytest -q` | `441 passed, 1 warning in 15.49s` |
| `python -m ruff check src/tradingai/ml/provenance.py tests/test_provenance.py` | `17 errors`, los mismos 17 diagnósticos preexistentes documentados en R11; ninguno en las líneas añadidas o cambiadas por R12 |
| `python -m mypy src` | `27 errors in 17 files`, igual al baseline R11; son avisos por stubs externos faltantes |
| `python -m pip check` | `No broken requirements found.` |

La advertencia de pytest es `PytestRemovedIn10Warning` de `anyio` (`CallSpec2` renombrado a `CallSpec`), también ajena a R12.

## Diferencias respecto a R11

- El patrón ULID válido de 128 bits establecido en R11 se reutiliza para `base_model_id`.
- El caso superior de `event_id` ahora prueba realmente un identificador que comienza por `7`.
- Se añadió una prueba de coherencia Python/JSON Schema para ambas referencias a modelos.
- La suite pasa con 441 pruebas, una más que las 440 reportadas en R11.
- Ruff permanece en 17 errores y mypy en 27 errores; R12 no añade diagnósticos.

## Archivos modificados

1. `src/tradingai/schemas/manifest_v3.json`
2. `tests/test_provenance.py`
3. `docs/aud04b_model_provenance_v3_s1_r12_report.md`

No se modificaron modelos, datos, artefactos en cuarentena ni módulos de ejecución o riesgo. No se entrenaron ni deserializaron modelos, no se ejecutó inferencia y no se habilitó live trading.

## Publicación

Este informe se incluye en el commit R12 solicitado. La verificación final de SHA remoto y de `main` debe hacerse después de publicar el commit; no se afirma aquí un resultado antes de esa comprobación.

S2 permanece sin iniciar y bloqueada hasta la aceptación independiente de S1 y una autorización explícita posterior.
