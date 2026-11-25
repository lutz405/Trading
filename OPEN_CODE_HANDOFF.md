# TradingAI_BTC — handoff técnico para OpenCode

## Estado de este paquete

Este ZIP es una **base de trabajo auditada y limpiada**, no una certificación de que el sistema esté libre de errores ni de que sea rentable. Se conservaron los módulos fuente y los datos OHLCV locales. Se eliminaron artefactos de ejecución, cachés y modelos de pruebas generados, para que OpenCode trabaje sobre un estado reproducible y no confunda modelos experimentales con modelos vigentes.

Se actualizaron `requirements.txt` y las dependencias de runtime de `pyproject.toml` para declarar paquetes que el código importa pero que no estaban declarados: NumPy, scikit-learn, XGBoost, joblib, Streamlit y Plotly.

## Restricciones del proyecto

- BTC/USDT; datos públicos de Binance.
- Solo análisis, backtesting y Paper Trading con capital virtual.
- No añadir ejecución de órdenes reales, apalancamiento ni conexión con fondos/cuentas reales.
- No afirmar rentabilidad ni presentar resultados de backtesting como garantía de resultados futuros.
- Mantener trazabilidad, reproducibilidad y separación temporal estricta en ML.

## Auditoría prioritaria confirmada en el código incluido

### P0 — Integridad temporal y leakage (`src/tradingai/ml/pipeline.py`)

1. `chronological_split` se importa pero no se utiliza.
2. El pipeline divide por posiciones y aplica dos gaps, pero solo valida explícitamente el gap train-validation; debe validar también validation-test y documentar la semántica exacta del gap.
3. El gap se calcula con diferencias de índices (`X.index[...]`). Eso solo equivale a filas si el índice es un RangeIndex continuo; no representa tiempo transcurrido cuando hay huecos o índices no consecutivos.
4. `_validate_temporal` valida timestamps del DataFrame, pero no demuestra que los índices de X/y correspondan uno a uno a esas filas después de `build_dataset` ni que los índices de X sean monótonos.
5. Debe probarse que las etiquetas calculadas con `shift(-horizon)` no cruzan los límites de cada partición. El purgado debe basarse en el horizonte de etiqueta y en la semántica de las ventanas, no solo en un test de no solapamiento de índices.
6. `calibrated_test` se calcula y no se usa. Revisar y eliminar el cálculo redundante o usarlo de forma explícita, evitando evaluaciones duplicadas o divergentes.
7. `_CalibratedEnsemble` no expone `classes_`; `evaluate()` infiere clases desde `y` cuando el modelo no la expone. Esto puede desalinear columnas de probabilidades y etiquetas si el conjunto evaluado no contiene todas las clases.

### P0 — Calibración (`src/tradingai/ml/calibration.py`)

1. `fit()` no valida que `len(proba_val) == len(y_val)`.
2. No valida que las probabilidades estén dentro de [0, 1] ni que cada fila sume aproximadamente 1.
3. Las clases se ordenan desde `y_val`, pero la clase/columna original del estimador no se pasa explícitamente. La correspondencia de columnas debe ser explícita y comprobada.
4. `transform()` devuelve silenciosamente la entrada si la forma o los valores son inválidos. Definir un contrato estricto y coherente (error explícito o fallback documentado), sin ocultar datos corruptos.
5. `load()` acepta `fitted=True` aunque falte el archivo `.joblib`, dejando un calibrador marcado como ajustado pero sin calibradores cargados.
6. Guardado JSON/joblib no es una transacción atómica conjunta. Diseñar un mecanismo seguro de versionado/validación de artefactos.

### P0 — Pruebas de leakage (`tests/test_leakage_indices.py`)

1. La instrumentación solo captura índices de `train_rf`; no captura índices de `train_xgb`.
2. La prueba no espía las llamadas a `predict_proba` ni `evaluate`; no prueba de forma directa qué partición alimenta entrenamiento, calibración y evaluación.
3. `test_holdout_independence` solo compara `rf.get_params()` y metadatos superficiales del calibrador. No compara el estado aprendido del RF/XGBoost ni el estado real del calibrador. Carga `xgb1`/`xgb2` pero no los compara.
4. Faltan pruebas negativas: particiones solapadas, gaps insuficientes en ambos límites, validación entrando en entrenamiento, test entrando en calibración, índices desordenados/duplicados, tamaños desalineados y probabilidades/etiquetas incompatibles.
5. La prueba actual modifica `close` en el tramo final, pero no demuestra por sí sola que el holdout no afecta parámetros ni calibración. Diseñar una prueba de independencia que altere únicamente información estrictamente posterior al límite permitido y compare hashes/estados aprendidos deterministas; separar métricas de holdout de los artefactos entrenados.

### P1 — Métricas (`src/tradingai/ml/metrics.py`)

1. `_valid_proba()` no valida el número de filas contra `y` ni la suma de probabilidades por fila.
2. Validar que `labels` sea único, estable y coincida con el orden de columnas.
3. Revisar métricas multiclase cuando falten clases en `y`; deben devolver resultados y razones coherentes sin mezclar columnas.

### P1 — Walk-forward (`src/tradingai/ml/walkforward.py`)

1. Revisar que construir datasets por separado en train/test no reinicie indebidamente ventanas de indicadores/volatilidad y provoque diferencias respecto al flujo real.
2. Documentar y validar purga temporal por horizonte entre ventanas.
3. Reportar dispersión por ventana (no solo promedio), número de observaciones y métricas no definidas.
4. Revisar el literal `...` dentro de la función: aunque es una expresión válida sin efecto, debe eliminarse si es residuo accidental.

### P1 — Dependencias y calidad

- Antes de ejecutar pruebas, instalar `python -m pip install -e ".[dev]"` y las dependencias declaradas.
- Ejecutar `python -m pytest -q`, `ruff check .` y `mypy src` (si la configuración de tipos lo permite).
- El intento de pytest realizado durante esta preparación no pudo completar la colección porque el entorno de auditoría no tenía instalados `ccxt` y `streamlit`; también faltaba `pyarrow`. **No se reporta un resultado de suite aprobado.**
- README anterior no representa el alcance actual de las fases 1–9. Actualizarlo cuando se estabilice la arquitectura, no inventar comandos o módulos.

## Orden de trabajo recomendado para OpenCode

1. Leer este documento y auditar el código actual; no asumir que los informes históricos describen el ZIP actual.
2. Resolver P0 de integridad temporal, calibración y pruebas antes de añadir más modelos o estrategias.
3. Ejecutar pruebas específicas y suite completa tras cada cambio; añadir pruebas negativas.
4. Revisar backtesting, contabilidad, broker Paper Trading, persistencia y Risk Manager con invariantes y pruebas de regresión.
5. Resolver P1 de métricas, walk-forward, documentación y calidad estática.
6. Solo después proponer nuevas funciones, siempre detrás de interfaces claras y pruebas.

## Protocolo de cambios

- Inspeccionar antes de editar.
- Presentar un plan acotado y los archivos afectados.
- No reescribir módulos completos si basta un cambio localizado.
- No eliminar datos del usuario ni configuraciones sin autorización.
- No relajar ni borrar pruebas para conseguir que la suite pase.
- Mantener Paper Trading como único modo de ejecución.
- Entregar resumen de archivos, pruebas ejecutadas, resultados exactos y limitaciones.
