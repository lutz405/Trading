# Cuarentena de artefactos de modelo — AUD-04A

Fecha: 2026-11-25
Commit de referencia: `3ba460d5c02864d3355928d75b8fedf11e9ca517`
Alcance: `models/_t7`, `models/_t8`, `models/_t9`, `models/_test`, `models/_testcal`
Contenido inventariado: 30 archivos, 353 686 bytes

## Aviso

Estos cinco directorios contienen **artefactos experimentales no aprobados**. No deben usarse para inferencia, selección de modelo, comparación de rendimiento, backtesting de estrategia ni como base de decisiones de trading.

`QUARANTINE.sha256` fija los bytes existentes en la fecha indicada para detectar cambios accidentales. **No es una certificación de autenticidad, corrección, reproducibilidad ni seguridad.** Un hash válido solo demuestra identidad byte a byte con el estado auditado; no demuestra que el modelo sea válido ni que sus métricas correspondan a sus datos.

Durante AUD-04A no se deserializó, reentrenó, recalibró, renombró, movió ni eliminó ningún artefacto original.

## Clasificación

Todos los directorios se clasifican como **experimentales y no aprobados**. Las etiquetas siguientes describen el motivo de contención y no implican corrupción.

| Directorio | Clasificación | Evidencia verificada | Lo que no se afirma |
|---|---|---|---|
| `_t7` | Esquema incompatible; procedencia no verificable; relación modelo-métricas no demostrable | Calibrador `schema_version=1` sin `joblib_sha256` y con payload de tipo lista; el loader actual exige schema 2 y lanza `ValueError: incompatible calibration schema`. `rf.json`/`xgb.json` sin `split`, `classes` ni `created_at`. | No se afirma corrupción. No se sabe con qué dataset ni split se obtuvieron sus métricas. |
| `_t8` | Procedencia no verificable; relación modelo-métricas no demostrable; probable residuo de test | `rf.joblib`, `xgb.joblib` y `calibrator.joblib` byte-idénticos a `_t9`; JSON con métricas distintas; split declarado sin posiciones. Distribución implícita de `y_test` `[23, 14, 31]`, compatible con el fixture sintético `make_ohlcv(400, seed=11)`. | No se afirma qué ejecución produjo el artefacto ni que sea un modelo de producción. |
| `_t9` | Procedencia no verificable; relación modelo-métricas no demostrable; origen no reconstruible | Mismos bytes de modelo que `_t8`; distribución implícita de `y_test` `[6, 50, 12]`; no coincide con ninguna semilla 0–300 del generador sintético plano. Mismo split y mismos hiperparámetros declarados que `_t8`. | No se afirma cuál de los dos JSON corresponde al modelo serializado. El mecanismo que produjo `_t9` no está demostrado. |
| `_test` | Artefacto de prueba; procedencia no verificable en sentido estricto | `n_rows=242`, 10 estimadores, GPU off, `y_test` `[7, 6, 35]`; coincide de forma única con `make_ohlcv(300, seed=3)` de `tests/test_ml.py` entre semillas 0–100. | No es un modelo canónico. La coincidencia con el fixture es fuerte pero no prueba la ejecución concreta. |
| `_testcal` | Artefacto de prueba; procedencia no verificable en sentido estricto | `n_rows=342`, 5 estimadores, `y_test` `[30, 15, 23]`; coincide con `make_ohlcv(400, seed=7)` de `tests/test_calibration_pipeline.py` (también con seed 10). | No es un modelo canónico. GPU declarada difiere del test actual. |

Ningún directorio contiene un registro de dataset, símbolo, timeframe, commit Git, hash de features ni hash del modelo base.

## Reglas de uso

1. No cargar ni deserializar estos `.joblib` para inferencia.
2. No usar sus métricas para seleccionar modelo ni para reporting de rendimiento.
3. No editar, regenerar ni sobrescribir los archivos originales.
4. Cualquier modelo nuevo debe generarse en un directorio de run nuevo, nunca dentro de estos directorios.
5. No eliminar ni mover estos directorios sin autorización expresa.
6. Este documento no designa ningún modelo canónico.

## Riesgo de uso accidental

| Punto de entrada | Archivo:línea | Condición | Consecuencia | Recomendación para AUD-04B |
|---|---|---|---|---|
| Configuración de entrenamiento por defecto | `config/ml.yaml:7` + `src/tradingai/ml/pipeline.py:366-377` | Invocar `run_training` con la configuración tal cual | Escribe `models/rf.joblib`, `models/xgb.joblib` y `models/calibrator.json` en la raíz de la zona en cuarentena | Rechazar `model_dir` dentro de `models/` o exigir un directorio de run explícito y versionado |
| Guardado sin protección de sobrescritura | `src/tradingai/ml/pipeline.py:151-154` | `model_dir` apunta a `_t7`, `_t8`, `_t9`, `_test` o `_testcal` | Sobrescribiría originales sin comprobar hash ni existencia | Guardia de ruta, escritura atómica y manifiesto por run |
| Carga de calibrador por ruta arbitraria | `src/tradingai/ml/calibration.py:191-232` | Cualquier llamada con una ruta a un `calibrator.json` schema 2 | Carga el calibrador sin verificar a qué RF/XGB pertenece | Vincular calibrador, modelos y dataset por hash en un manifiesto verificable |
| Atribución de versión en decisiones | `src/tradingai/decision/engine.py:28-33` + `config/decision.yaml:13` | Un llamador externo pasa probabilidades y `model_version="v0.1"` | El resultado declara una versión no ligada a ningún artefacto | Registrar `model_id` y hash exactos; validarlos en el cargador |
| Ruta de test dentro de `models/` | `tests/test_leakage_indices.py:126-132` | Si cambia el orden de validación antes del guardado | El test podría crear o escribir en `models/_never_written` | Usar `tmp_path`; el directorio no existe hoy y el test falla antes de guardar |

No se encontró ningún cargador de RF/XGB en `src/`, `scripts/` ni `dashboard/`. El dashboard solo carga el estado del `PaperBroker`; backtesting no carga modelos; `scripts/download_data.py` solo descarga datos; `pyproject.toml` no declara entry points.

## Verificación de integridad

Desde el directorio `models/`:

```bash
sha256sum -c QUARANTINE.sha256
```

En PowerShell, comparar cada línea con `Get-FileHash -Algorithm SHA256`. El manifiesto usa rutas relativas a `models/`.

Cualquier discrepancia indica que un artefacto cambió después de AUD-04A y debe tratarse como incidente de integridad, no como actualización.

## Limitaciones

- Los hashes solo prueban identidad byte a byte en la fecha de auditoría.
- No se deserializó ningún `.joblib`; no se verificó el comportamiento interno de los modelos.
- Los 30 archivos fueron añadidos en bloque en el commit `9ca2bd6`; Git no documenta su generación.
- La atribución de `_test`, `_testcal` y `_t8` a fixtures concretos es una coincidencia estadística fuerte, no una prueba de ejecución.
- El origen de `_t9` sigue sin demostrarse.
- No se evaluó rendimiento ni rentabilidad.

## Siguiente fase

AUD-04B deberá definir el manifiesto de artefacto, el cargador verificable, la escritura atómica y el procedimiento de regeneración. AUD-04B no ha comenzado.
