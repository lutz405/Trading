# Fase 0.1 — Auditoría de línea base e integridad

**Fecha:** 2026-11-24  
**Proyecto:** TradingAI_BTC (`tradingai-btc==0.1.0`)  
**Alcance:** inventario, pruebas, calidad estática, dependencias, datos, artefactos, contratos contables, `RiskManager`, backtesting, deuda técnica y compatibilidad multi-activo.  
**Restricción respetada:** no se modificó ningún archivo funcional (fuente, tests, configuración, datos o modelos). Solo se añadieron este informe y el manifiesto de hashes.

---

## 1. Resumen ejecutivo

La línea base **ejecuta la suite completa sin fallos**: `238 passed`, `1 warning` de terceros (`anyio`/pytest). La instalación editable, las dependencias declaradas y los datos OHLCV son coherentes. Ruff y Mypy no están limpios.

La suite verde **no certifica la integridad del sistema**. Las pruebas reproducidas en esta auditoría encontraron defectos P0 que la suite no cubre:

1. **Backtesting con gaps**: una entrada pendiente se ejecuta en la apertura y, en la misma vela, se cierra en el `stop`/`take` aunque la apertura ya haya superado el nivel. Se generan resultados ficticios (ejemplo reproducido: `+47.24` en un gap bajista y `-87.01` en un gap alcista).
2. **Colateral de cortos**: el contrato documentado exige `free_cash >= q*P + fee`; el código solo comprueba la comisión. Se reprodujo un corto con `98.1` de caja libre y `1,000.0` de colateral.
3. **RiskManager**: `update_capital(NaN)` o `register_trade_result(NaN)` dejan el estado en `NaN` y `approve()` devuelve `True`, saltándose drawdown, pérdida diaria y exposición.
4. **Artefactos de modelo**: `models/_t8` y `models/_t9` tienen los `.joblib` byte-idénticos, pero métricas distintas en sus JSON; `models/_t7` usa un esquema de calibrador ya rechazado por el cargador. No hay modelo canónico ni procedencia reproducible.
5. **Sin control de versiones**: el directorio no es un repositorio Git. No existe commit de referencia; el manifiesto SHA-256 es la única referencia verificable.

**Estado global:** apto como base de investigación y paper trading experimental, **no apto** para validación de estrategia, multi-activo concurrente ni promoción de modelos sin resolver primero los P0.

---

## 2. Entorno y método

### 2.1 Entorno

| Elemento | Valor |
|---|---|
| Sistema | Windows, PowerShell |
| Python | 3.13.15 |
| pip | 26.2.1 |
| Paquete | `tradingai-btc==0.1.0`, editable en `C:\TradingAI_BTC` |
| `tradingai.__file__` | `C:\TradingAI_BTC\src\tradingai\__init__.py` |
| Repositorio Git | No (`.git` no existe) |
| `.gitignore` raíz | No existe |

### 2.2 Comandos ejecutados

```text
python -m pytest -q
python -m pytest --collect-only -q
python -m pytest -q -W error::FutureWarning
python -m ruff check .
python -m ruff check . --statistics
python -m ruff format --check .
python -m mypy src --ignore-missing-imports
python -m mypy src
python -m mypy src --ignore-missing-imports --check-untyped-defs
python -m pip check
python -m pip list --format=freeze
```

Además se ejecutaron comprobaciones de importación, integridad de parquet, carga de artefactos, hashes SHA-256 y pruebas controladas de contabilidad/backtesting/RiskManager. Todas las pruebas controladas se ejecutaron en memoria o en directorios temporales fuera del repositorio.

---

## 3. Inventario completo de módulos

**Fuente:** 35 archivos Python, 2,644 líneas.  
**Tests:** 29 archivos, 2,268 líneas, 238 tests recolectados.

### 3.1 Paquete `tradingai`

| Archivo | Líneas | Símbolos / responsabilidad |
|---|---:|---|
| `src/tradingai/__init__.py` | 2 | Versión del paquete. |
| `src/tradingai/accounting.py` | 84 | `validate_number`, `validate_side`, `execution_price`, `slippage_cost_amount`, `entry_notional`, `entry_fee_amount`, `exit_notional`, `exit_fee_amount`, `gross_pnl`, `unrealized_pnl`, `account_equity`. Primitivas contables. |
| `src/tradingai/backtesting/__init__.py` | 5 | Exporta `BacktestEngine`, `compute_metrics`. |
| `src/tradingai/backtesting/engine.py` | 246 | `Trade`, `BacktestEngine`: simulación long/short, stops/takes, sizing, equity, liquidación final. |
| `src/tradingai/backtesting/metrics.py` | 52 | `compute_metrics`: retorno, drawdown, Sharpe, Sortino, win rate, profit factor, exposición, fees y slippage. |
| `src/tradingai/dashboard/__init__.py` | 4 | Exporta helpers del dashboard. |
| `src/tradingai/dashboard/app.py` | 59 | `load_broker`, `equity_dataframe`, `candlestick_figure`, `main`: Streamlit paper trading. |
| `src/tradingai/data/__init__.py` | 6 | Exporta provider, storage y validación. |
| `src/tradingai/data/provider.py` | 49 | `BinanceOHLCVProvider`: descarga CCXT/Binance, paginación y normalización OHLCV. |
| `src/tradingai/data/storage.py` | 26 | `ParquetStorage`: rutas por símbolo/timeframe, save/load parquet. |
| `src/tradingai/data/validation.py` | 26 | `validate_ohlcv`: columnas, duplicados, orden, valores negativos, high/low. |
| `src/tradingai/decision/__init__.py` | 5 | Exporta `DecisionEngine`. |
| `src/tradingai/decision/engine.py` | 107 | `DecisionEngine`: probabilidades, señales multi-timeframe, conflicto, umbrales, aprobación de riesgo. |
| `src/tradingai/features/__init__.py` | 13 | Exporta indicadores y features. |
| `src/tradingai/features/engineering.py` | 34 | `build_features`: retornos, SMA/EMA/RSI/MACD/ATR/Bollinger/ADX/VWAP/volumen/rango. |
| `src/tradingai/features/indicators.py` | 86 | `sma`, `ema`, `rsi`, `macd`, `atr`, `bollinger_bands`, `adx`, `vwap`. |
| `src/tradingai/features/multitimeframe.py` | 85 | `_infer_bar_duration`, `align_higher_timeframe`: merge causal por `available_at`. |
| `src/tradingai/features/validation.py` | 39 | `validate_features`: filas mínimas, columnas, timestamps, NaN/inf, coherencia OHLC. |
| `src/tradingai/features/volume.py` | 18 | `volume_features`: media, relativo, cambio, z-score, anomalía. |
| `src/tradingai/ml/__init__.py` | 15 | Exporta dataset, ensemble, labels y pipeline. |
| `src/tradingai/ml/calibration.py` | 232 | `Calibrator`: isotonic/sigmoid por clase, validación estricta, persistencia v2 con checksum. |
| `src/tradingai/ml/dataset.py` | 36 | `build_dataset`, `chronological_split`. |
| `src/tradingai/ml/ensemble.py` | 19 | `ensemble_proba`, `predict_with_abstention`. |
| `src/tradingai/ml/labels.py` | 41 | `make_labels`: etiquetas 3 clases por retorno futuro y volatilidad. |
| `src/tradingai/ml/metrics.py` | 110 | `_valid_proba`, `compute_metrics`, `expected_calibration_error`. |
| `src/tradingai/ml/pipeline.py` | 390 | `gpu_available`, `train_rf`, `train_xgb`, `_aligned_proba`, `evaluate`, `_CalibratedEnsemble`, `save_artifact`, `_validate_temporal`, `_validate_label_purge`, `run_training`. |
| `src/tradingai/ml/walkforward.py` | 64 | `_validate_timestamps`, `run_walk_forward`. |
| `src/tradingai/paper/__init__.py` | 4 | Exporta `PaperBroker`. |
| `src/tradingai/paper/broker.py` | 427 | `Position`, `PaperBroker`: long/short, colateral, fees/slippage, stops, persistencia JSON v2. |
| `src/tradingai/paper/realtime.py` | 18 | `is_stale`, `fetch_latest`. |
| `src/tradingai/risk/__init__.py` | 6 | Exporta `RiskManager`, `position_size`, `atr_stops`. |
| `src/tradingai/risk/position_sizing.py` | 18 | `position_size`: helper legacy de sizing por volatilidad. |
| `src/tradingai/risk/risk_manager.py` | 168 | `RiskManager`: límites, drawdown, pérdida diaria, exposición, cooldown, persistencia v1. |
| `src/tradingai/risk/sizing.py` | 139 | `SizingInput`, `SizingResult`, `stop_exec`, `stop_hit`, `calculate_risk_incremental`, `calculate_cash_long`, `calculate_cash_short`, `floor_to_step`, `calculate_position_size`. |
| `src/tradingai/risk/stops.py` | 11 | `atr_stops`: stops ATR long-only. |

### 3.2 Scripts

| Archivo | Líneas | Responsabilidad |
|---|---:|---|
| `scripts/download_data.py` | 41 | CLI de descarga para símbolo/timeframes desde `config/settings.yaml`; guarda parquet y valida. |

### 3.3 API pública y código paralelo

Exportado por los `__init__.py`: `BacktestEngine`, `compute_metrics`, `BinanceOHLCVProvider`, `ParquetStorage`, `validate_ohlcv`, `DecisionEngine`, indicadores/features, `build_dataset`, `ensemble_proba`, `predict_with_abstention`, `make_labels`, `gpu_available`, `run_training`, `PaperBroker`, `RiskManager`, `position_size`, `atr_stops`, helpers del dashboard.

No se exportan: `risk.sizing` (usado internamente por broker/engine), `ml.walkforward` (solo importado por tests) y `paper.realtime` (sin integración).

Hay **implementaciones paralelas/legacy**:

- `risk.position_sizing.position_size` no se usa en `BacktestEngine`/`PaperBroker`; estos usan `risk.sizing`.
- `risk.stops.atr_stops` solo lo usan tests; el backtest fija stops en `price * 0.99/1.01` y no usa ATR.
- `ml.ensemble.ensemble_proba` no lo usa `run_training`; `_CalibratedEnsemble` fija pesos 50/50.
- `ml.dataset.chronological_split` solo lo usan tests; `run_training` implementa su propio split.
- Varias primitivas de `accounting.py` (`entry_notional`, `entry_fee_amount`, `exit_notional`, `exit_fee_amount`, `unrealized_pnl`, `account_equity`) no se usan fuera de tests/definición.

Esto incrementa el riesgo de divergencia de contratos.

### 3.4 Tests

| Archivo | Tests | Líneas |
|---|---:|---:|
| `tests/test_phase2a_accounting.py` | 57 | 310 |
| `tests/test_state_validation_full.py` | 48 | 79 |
| `tests/test_risk_sizing_contract.py` | 14 | 162 |
| `tests/test_metrics.py` | 9 | 80 |
| `tests/test_decision.py` | 8 | 63 |
| `tests/test_calibration_contract.py` | 8 | 102 |
| `tests/test_pipeline_contract.py` | 7 | 135 |
| `tests/test_indicators.py` | 7 | 69 |
| `tests/test_leakage_indices.py` | 6 | 166 |
| `tests/test_price_validation.py` | 6 | 20 |
| `tests/test_state_validation.py` | 6 | 92 |
| `tests/test_label_purge_contract.py` | 6 | 159 |
| `tests/test_ml.py` | 5 | 84 |
| `tests/test_ml_temporal.py` | 5 | 95 |
| `tests/test_risk.py` | 5 | 41 |
| `tests/test_calibration_integration.py` | 4 | 62 |
| `tests/test_calibration.py` | 4 | 40 |
| `tests/test_labels_dataset_contract.py` | 4 | 53 |
| `tests/test_critical_fixes.py` | 4 | 57 |
| `tests/test_features.py` | 4 | 53 |
| `tests/test_paper.py` | 4 | 31 |
| `tests/test_validation.py` | 3 | 38 |
| `tests/test_multitimeframe_causality.py` | 3 | 58 |
| `tests/test_backtesting.py` | 3 | 46 |
| `tests/test_dashboard.py` | 3 | 22 |
| `tests/test_walkforward.py` | 2 | 75 |
| `tests/test_calibration_pipeline.py` | 1 | 45 |
| `tests/test_storage.py` | 1 | 12 |
| `tests/test_provider.py` | 1 | 19 |
| **Total** | **238** | **2,268** |

No hay tests directos para `paper.realtime`, `scripts/download_data.py` ni para las primitivas de `accounting.py`; la contabilidad se cubre indirectamente vía broker/engine.

---

## 4. Ejecución de pruebas

### 4.1 Resultado principal

```text
python -m pytest -q
........................................................................ [ 30%]
........................................................................ [ 60%]
........................................................................ [ 90%]
......................                                                   [100%]
238 passed, 1 warning in 23.68s
```

- **Fallos:** 0.
- **Errores de colección:** 0.
- **Skips:** 0.
- **Warning:** `PytestRemovedIn10Warning` de `anyio` (`CallSpec2`), ajeno al proyecto.
- Repetición con `-W error::FutureWarning`: **238 passed** (8.57 s en caliente), lo que indica que el código no emite `FutureWarning` con pandas 3.1.1.
- Recolección: **238 tests en 4.12 s**.

### 4.2 Cobertura funcional observada

La suite está concentrada en contabilidad/estado (105 tests) y ML/calibración/purga temporal. Los huecos relevantes son:

- Backtesting: 3 tests básicos; no cubre gaps, métricas anualizadas, integración de riesgo ni benchmarks.
- RiskManager: 5 tests directos; no cubre NaN, arrays NumPy, límites exactos ni integración.
- PaperBroker: buenos tests de identidades y persistencia; no cubre el requisito de caja libre para cortos.
- Multi-activo: sin tests.
- `realtime`, `scripts`, dashboard `main`: sin tests reales.
- No hay configuración de cobertura ni informe de líneas/branches.

**Conclusión:** suite estable y reproducible, pero insuficiente para certificar integridad financiera o multi-activo.

---

## 5. Calidad estática

### 5.1 Ruff

```text
python -m ruff check .
Found 47 errors.
[*] 30 fixable with `--fix` (13 unsafe fixes available with `--fix --unsafe-fixes`).
```

Distribución:

| Regla | Cantidad | Significado |
|---|---:|---|
| `I001` | 15 | Imports desordenados |
| `F401` | 8 | Imports sin uso |
| `F841` | 6 | Variables sin uso |
| `RUF059` | 5 | Variables desempaquetadas sin uso |
| `TRY004` | 4 | Excepción de tipo incorrecta |
| `RUF022` | 3 | `__all__` sin ordenar |
| `UP017` | 2 | `datetime.UTC` |
| `UP035` | 1 | Import obsoleto |
| `FURB162` | 1 | Reemplazo de timezone innecesario |
| `SIM103` | 1 | Condición redundante |
| `UP037` | 1 | Anotación entre comillas |

**24 errores están en `src/` y 23 en `tests/`.** Los más relevantes funcionalmente:

- `src/tradingai/dashboard/app.py:18` — `cap` sin uso.
- `src/tradingai/decision/engine.py:7,46,66` — `yaml` y `p_side` sin uso; `penalty` calculado y nunca aplicado.
- `src/tradingai/data/provider.py:5` — `Iterable` sin uso.
- `src/tradingai/features/validation.py:3` — `math` sin uso.
- `src/tradingai/risk/risk_manager.py` — `TRY004` en validaciones de tipo, `UP037`, `UP017`, `FURB162`.

Formato:

```text
python -m ruff format --check .
31 files would be reformatted, 40 files already formatted
```

No es un fallo de ejecución, pero impide usar `ruff format --check` como puerta de calidad.

### 5.2 Mypy

```text
python -m mypy src --ignore-missing-imports
Success: no issues found in 35 source files
```

Con la configuración real del proyecto:

```text
python -m mypy src
Found 26 errors in 16 files (checked 35 source files)
```

Los 26 errores son `import-untyped`: faltan stubs/`py.typed` para `pandas`, `yaml`, `sklearn`, `joblib` y `plotly`. No hay errores de lógica detectados por Mypy en modo normal.

Chequeo más profundo:

```text
python -m mypy src --ignore-missing-imports --check-untyped-defs
src/tradingai/ml/walkforward.py:24: error: Need type annotation for "results"  [var-annotated]
src/tradingai/ml/walkforward.py:61: error: Value of type "object" is not indexable  [index]
Found 2 errors in 1 file
```

**No existe `[tool.mypy]` en `pyproject.toml`.** El comando que “pasa” requiere `--ignore-missing-imports`; no es una puerta reproducible sin documentar. Faltan `pandas-stubs` y `types-PyYAML` en `dev` si se quiere `mypy src` limpio.

---

## 6. Verificación de dependencias

### 6.1 Estado de instalación

```text
python -m pip check
No broken requirements found.
```

Paquete editable correctamente instalado:

```text
Name: tradingai-btc
Version: 0.1.0
Editable project location: C:\TradingAI_BTC
```

### 6.2 Dependencias declaradas vs. imports reales

Imports de terceros en `src/` y `scripts/`:

| Import | Distribución | Declarada |
|---|---|---|
| `ccxt` | `ccxt` | Sí |
| `joblib` | `joblib` | Sí |
| `numpy` | `numpy` | Sí |
| `pandas` | `pandas` | Sí |
| `plotly` | `plotly` | Sí |
| `sklearn` | `scikit-learn` | Sí |
| `streamlit` | `streamlit` | Sí |
| `xgboost` | `xgboost` | Sí |
| `yaml` | `pyyaml` | Sí |

No hay imports de terceros no declarados.

**Dependencias declaradas pero no importadas:** `pydantic` y `loguru`. `pyarrow` no se importa directamente pero es necesario para parquet; está correctamente declarado.

### 6.3 Versiones instaladas relevantes

```text
ccxt==4.5.94          numpy==2.5.5         pandas==3.1.1
pyarrow==26.0.1       pydantic==2.13.4      PyYAML==6.0.4
scikit-learn==1.9.1   scipy==1.18.1         xgboost==3.4.1
streamlit==1.67.0     plotly==7.1.0         joblib==1.6.0
pytest==9.2.0         ruff==0.17.6          mypy==2.4.1
```

Todas cumplen los mínimos de `pyproject.toml` y `requirements.txt`.

### 6.4 Riesgos de reproducibilidad

- No hay lockfile (`requirements.lock`, `poetry.lock`, `uv.lock`): las versiones resueltas pueden cambiar.
- `requirements.txt` y `pyproject.toml` duplican dependencias; hoy coinciden, pero pueden divergir.
- Rango `requires-python = ">=3.12"` con `target-version = "py313"`: solo se validó 3.13.15.
- GPU: `gpu_available()` devuelve `True` y XGBoost entrena con `device="cuda"` en este equipo. No hay fallback automático a CPU si el entorno no tiene GPU/driver; `use_gpu: true` en `config/ml.yaml` puede fallar en otra máquina.

---

## 7. Integridad de datos y artefactos

### 7.1 Datos OHLCV

Los 7 parquet de `data/raw/` están íntegros para el periodo descargado:

| Archivo | Filas | Inicio UTC | Fin UTC | Rejilla | Duplicados | NaN |
|---|---:|---|---|---|---:|---:|
| `BTC_USDT_1m.parquet` | 43,201 | 2026-10-24 22:39 | 2026-11-23 22:39 | 1 min | 0 | 0 |
| `BTC_USDT_5m.parquet` | 8,640 | 2026-10-24 22:40 | 2026-11-23 22:35 | 5 min | 0 | 0 |
| `BTC_USDT_15m.parquet` | 2,880 | 2026-10-24 22:45 | 2026-11-23 22:30 | 15 min | 0 | 0 |
| `BTC_USDT_30m.parquet` | 1,440 | 2026-10-24 23:00 | 2026-11-23 22:30 | 30 min | 0 | 0 |
| `BTC_USDT_1h.parquet` | 720 | 2026-10-24 23:00 | 2026-11-23 22:00 | 1 h | 0 | 0 |
| `BTC_USDT_4h.parquet` | 180 | 2026-10-25 00:00 | 2026-11-23 20:00 | 4 h | 0 | 0 |
| `BTC_USDT_1d.parquet` | 30 | 2026-10-25 00:00 | 2026-11-23 00:00 | 1 d | 0 | 0 |

- Timestamps UTC, ordenados, sin duplicados, sin NaN y sin huecos de rejilla en el periodo.
- Cobertura: ~30 días; suficiente para 1m–4h, **insuficiente para 1d**.
- `build_dataset` con 1d falla con `ValueError: no labeled rows with complete features` (30 filas no cubren warmup de features + ventana de volatilidad + horizonte). Es una limitación de datos, no un fallo del pipeline.
- Dataset etiquetado por timeframe (horizonte 5, `vol_mult=0.5`): 1m 43,163; 5m 8,602; 15m 2,842; 30m 1,402; 1h 682; 4h 142; 1d 0.

### 7.2 Artefactos de modelo

`models/` contiene 5 directorios de pruebas y 30 archivos. No hay modelo canónico ni registro de versiones.

| Directorio | Estado | Incidencia |
|---|---|---|
| `models/_t7` | Legacy | `calibrator.json` es schema 1; el `Calibrator` actual lo rechaza (`ValueError: incompatible calibration schema`). `rf.json`/`xgb.json` no tienen `split`, `classes` ni `created_at`. |
| `models/_t8` | Schema 2 | Split sin `start_position`/`end_position` y sin purga de etiquetas. |
| `models/_t9` | Schema 2 | Split sin posiciones; **ver incidencia de procedencia**. |
| `models/_test` | Schema 2 | Split con posiciones, pero sin claves de purga de etiquetas. |
| `models/_testcal` | Schema 2 | Split sin posiciones; artefacto de prueba. |

**Incidencia de procedencia (P0):** los `rf.joblib`, `xgb.joblib` y `calibrator.joblib` de `_t8` y `_t9` son **byte-idénticos** (mismo SHA-256), pero sus JSON declaran métricas distintas:

| Modelo | `_t8` accuracy | `_t9` accuracy |
|---|---:|---:|
| RF | 0.3088 | 0.0882 |
| XGB | 0.2941 | 0.0147 |

Los `created_at` difieren en ~0.5 s y los splits declarados son iguales. Si el artefacto y el split son los mismos, las métricas deberían coincidir; la evidencia indica que los JSON no son una procedencia fiable de los `.joblib`. No se deben usar estas métricas ni estos artefactos como referencia de rendimiento.

Además:

- `save_artifact()` guarda `.joblib` y `.json` por separado, sin checksum del `.joblib` ni escritura atómica conjunta.
- El calibrador sí tiene checksum y validación de esquema, pero el par `.json`/`.joblib` no es una transacción atómica.
- El nombre de artefacto es fijo (`rf`, `xgb`, `calibrator`) dentro de `model_dir`; no incluye símbolo, timeframe, versión ni hash de dataset. Dos entrenamientos multi-activo se sobrescribirían.

---

## 8. Revisión de contratos contables

### 8.1 Contrato documentado

`docs/market_data_conventions.md` define un corto **totalmente colateralizado en cash**:

- Al abrir: exigir `free_cash >= q*P + fee`; mover `q*P` a colateral restringido; acreditar proceeds `q*P` a caja libre; descontar fee.
- Mientras abierto: `equity = free_cash + collateral - q*current_price`.
- Al cerrar: liberar colateral; debitar `q*Px`; descontar fee.
- Identidad: `final_equity == initial_capital + sum(net PnL)`.

### 8.2 Implementación

| Invariante | `PaperBroker` | `BacktestEngine` | Estado |
|---|---|---|---|
| Largo: caja disminuye por notional + fee | Sí | Sí | OK |
| Largo: equity = caja + market value | Sí | Sí | OK |
| Corto: fee descontada | Sí | Sí | OK |
| Corto: colateral `q*entry` registrado | Sí (propiedad derivada) | Sí (`self.collateral`) | Parcial |
| Corto: exigir `free_cash >= q*P + fee` antes de abrir | **No** | **No** | **Falla** |
| Corto: reservar/restar colateral de caja libre | No (solo seguimiento) | No (solo seguimiento) | Parcial |
| Corto: al cerrar, liberar colateral y recomprar | Algebraicamente equivalente | Algebraicamente equivalente | OK |
| PnL neto = bruto − fees | Sí | Sí | OK |
| `final_equity == initial + sum(net PnL)` | Sí (500 casos aleatorios, 0 fallos) | Sí (200 casos, 0 fallos) | OK |
| Fees y slippage registrados | Sí | Sí | OK |
| Persistencia valida estado completo | Parcial (sin invariante de equity con posiciones abiertas) | N/A | Parcial |
| Multi-activo | No | No | **Falla** |

### 8.3 Evidencia del fallo de colateral

`risk/sizing.py::calculate_cash_short` calcula:

```text
q_cash = cash / (fee_rate * entry_exec)
```

Eso dimensiona la cantidad solo para cubrir la comisión, no el colateral. `PaperBroker.open_position` y `BacktestEngine._enter` solo comprueban `entry_fee <= capital`.

Reproducción con `capital=1000`, `fee=0.001`, `max_exposure=2.0`, `risk_budget=10.0`:

```text
long 9@100  -> aceptado; cash libre = 99.1
short 10@100 -> aceptado; cash libre = 98.1; colateral = 1000.0
```

El contrato exige `free_cash >= 1000 + fee`; el sistema lo acepta con `98.1`. En la configuración por defecto (`max_exposure=0.5`) el límite de exposición suele enmascarar el problema, pero **la invariante no está garantizada por el código**.

### 8.4 Otras observaciones contables

- `validate_number` acepta `True`/`False` como `1.0`/`0.0` y acepta strings numéricos (`"1.0"`); puede ocultar errores de tipo.
- `execution_price` no limita `slippage`; con `slippage >= 1` puede devolver un precio de ejecución no positivo. Los llamadores suelen fallar después, pero la primitiva no falla en el origen.
- `account_equity` y varias funciones de fees/noional no se usan; no hay una clase `Ledger` única que centralice las invariantes.
- `PaperBroker.save` valida `capital == realized_equity` solo cuando no hay posiciones; con posiciones abiertas no valida una identidad de equity completa.
- `PaperBroker.load` asume que `risk_state["capital"]` existe; un `risk_state` sin esa clave produce `KeyError`, no un `ValueError` controlado.
- `PaperBroker` usa `risk_budget_ratio=0.1` por defecto, mientras `config/risk.yaml` define `risk_per_trade=0.01` y `BacktestEngine` usa `0.01` como fallback. La composición del dashboard no carga `config/risk.yaml`.

---

## 9. Revisión de `RiskManager`

### 9.1 Comportamiento correcto

`approve()` rechaza, en este orden: cooldown, datos insuficientes, datos obsoletos, probabilidades inválidas (longitud 3, rango, suma 1), incertidumbre alta, volatilidad alta, drawdown, pérdida diaria y exposición. La persistencia `schema_version=1` valida campos requeridos, tipos, finitud y coherencia básica en `from_dict`.

### 9.2 Defectos y huecos

| Comprobación | Resultado | Evidencia |
|---|---|---|
| `update_capital` valida finitud/positividad | **No** | `update_capital(float("nan"))` deja `capital=nan`; `drawdown()` devuelve `nan`; `approve()` devuelve `True`. |
| `register_trade_result` valida finitud | **No** | `register_trade_result(float("nan"))` deja `capital=nan`; `approve()` devuelve `True`. |
| `exposure` se actualiza automáticamente | No | Es un campo público; nadie lo actualiza en `src/`. Un `exposure=nan` también evita el rechazo (`nan > max` es `False`). |
| `daily_loss` se reinicia automáticamente | No | Solo `update_time()` lo reinicia; no se llama en `src/` ni en `scripts/`. |
| `cooldown` avanza automáticamente | No | Solo `advance()`; no se llama en `src/`. |
| `approve` acepta arrays NumPy | **No** | `np.array([0.2,0.3,0.5])` lanza `ValueError: truth value ... ambiguous` en `if not proba`. |
| `approve` valida volatilidad no negativa | **No** | Una volatilidad negativa pasa la comparación `volatility > threshold`. |
| Límites exactos | Parcial | Usa `>`; un drawdown exactamente `0.15` o una pérdida diaria exactamente `0.03` se aprueban. |
| `price` y `atr` se usan | **No** | Parámetros presentes pero ignorados. |
| `from_dict` valida rangos de parámetros | Parcial | Valida finitud/tipos, pero no `risk_per_trade > 0`, `0 <= max_drawdown <= 1`, etc. |
| Integración en backtest | **No** | `BacktestEngine` solo lee `risk_per_trade` y `max_exposure`; no llama `approve`, `update_capital`, `register_trade_result`, `advance` ni actualiza `exposure`. |
| Integración en broker | **No** | `PaperBroker` solo persiste `risk_state`; no lo usa para aprobar operaciones. |
| Multi-activo | **No** | Un único capital, una exposición y un estado global. |

**Conclusión:** el `RiskManager` es una pieza de decisión aislada, no un control de riesgo integrado en el ciclo de ejecución. Los NaN permiten saltarse todos los límites; es el defecto más grave de esta sección.

---

## 10. Revisión del backtesting

### 10.1 Flujo implementado

1. En la vela `i`, si hay una orden pendiente, se ejecuta en `open[i]`.
2. Si hay posición, se comprueban `stop`/`take` con `high[i]`/`low[i]`; si ambos se tocan, se prioriza el stop.
3. Se marca equity con `close[i]`.
4. Si no hay posición, `decision_fn(i, row, engine)` puede dejar una orden pendiente para la siguiente apertura.
5. Al final, se liquida la posición abierta al último `close` y se ajusta `equity[-1]`.

### 10.2 Defecto P0: gaps en la misma vela

La orden pendiente se llena en la apertura, pero los stops/takes se evalúan con los extremos de la **misma** vela sin comprobar si la apertura ya cruzó el nivel:

- Gap bajista: cierre previo 100, `open=90`, `low=85`, stop calculado `99.495`.
  Resultado del motor: entra a `90`, sale a `99.495` con razón `stop`, **PnL +47.24**. Es ficticio: el stop ya estaba por encima del mercado al entrar.
- Gap alcista: `open=120`, take calculado `102.51`.
  Resultado: entra a `120`, sale a `102.51` con razón `take`, **PnL −87.01**. También ficticio.

Un backtest así puede convertir gaps adversos en ganancias y gaps favorables en pérdidas. **Invalida cualquier métrica de estrategia que use stops/takes y datos con gaps.**

### 10.3 Otras deficiencias

| Elemento | Estado | Detalle |
|---|---|---|
| Entrada en apertura siguiente | OK | Evita look-ahead de la señal de cierre. |
| Stop-first si ambos se tocan | OK (conservador) | No modela el orden intra-vela. |
| Fees y slippage | OK | Se aplican a entrada/salida y se registran. |
| Liquidación final | OK | Actualiza `equity[-1]` y `capital`. |
| Identidad contable | OK | 200 casos aleatorios, 0 fallos. |
| Integración de `RiskManager` | **No** | No hay `approve`, drawdown, pérdida diaria, cooldown ni actualización de exposición. |
| Stops/takes | **No usa ATR** | Fijos al 1%/2%; `atr_stop_mult`/`atr_take_profit_mult` no se usan. |
| Benchmarks | **No** | `benchmarks` de `config/backtesting.yaml` no se implementa. |
| Sharpe/Sortino | **Incorrecto para intradía** | Anualiza con `sqrt(252)` sin conocer el timeframe; para 1h/15m/5m no es válido. |
| Sortino | Parcial | Divide por la desviación de los retornos negativos únicamente, no por la downside deviation estándar sobre todas las observaciones. |
| `exposure` | **Métrica inválida** | `len(trades)/len(equity)` no mide tiempo en mercado ni notional expuesto. |
| `gross_return` | Parcial | Suma fees pero no slippage, aunque el slippage ya está incorporado al precio de ejecución. |
| Win rate | Parcial | `pnl <= 0` cuenta breakeven como pérdida. |
| Profit factor / Sortino | Parcial | Pueden devolver `inf`; no hay política de serialización/representación. |
| Drawdown | Parcial | Solo drawdown a cierre de vela; ignora drawdown intra-vela. |
| Timestamps/trades | Parcial | `Trade` guarda índices, no timestamps; no hay benchmark ni atribución. |
| Multi-activo | **No** | Una sola posición y un solo `mark_price`. |
| Pending al final | Parcial | Una señal en la última vela se descarta silenciosamente. |
| Validación de columnas | Parcial | Solo exige `open`; `high/low/close` pueden fallar a mitad de ejecución con `KeyError`. |

### 10.4 Resultado de métricas de ejemplo

Un motor con equity `[1000, 1010, 1005]`, sin trades, devuelve `sharpe=5.36`, `sortino=8.10`, `net_return=0.005`. El Sharpe positivo con dos retornos y sin contexto de timeframe demuestra que la métrica no es interpretable tal cual; además se anualiza con 252.

---

## 11. Revisión de ML e integridad temporal

### 11.1 Fortalezas verificadas

- `run_training` usa posiciones reales del DataFrame, no aritmética de índices.
- `_validate_label_purge` comprueba ambos límites (`train→validation`, `validation→test`) y que el cierre de etiqueta exista dentro del DataFrame.
- El manifiesto registra `start_position`, `end_position`, `label_end_position` y distancias de purga.
- `Calibrator` rechaza formas incorrectas, no finitos, fuera de `[0,1]`, sumas distintas de 1, clases duplicadas/faltantes y menos de 30 muestras; guarda schema 2 con checksum SHA-256.
- `evaluate` exige `classes_`, alinea columnas y soporta particiones de test sin todas las clases.
- `_CalibratedEnsemble` expone `classes_`.

### 11.2 Smoke test con datos reales 1h

Con `config/ml.yaml`, `use_gpu=False`, 20 estimadores y `model_dir` temporal:

```text
split: train 0-388 (pos 20-407, label_end 412)
       validation 393-525 (pos 413-544, label_end 549)
       test 530-662 (pos 550-681, label_end 686)
purga: train→val 6, val→test 6, label→val 1, label→test 1
RF:   accuracy 0.3409, f1 0.2064, brier 0.2527, log_loss 1.3480
XGB:  accuracy 0.3864, f1 0.3488, brier 0.2222, log_loss 1.0947
Cal:  accuracy 0.4318, f1 0.2011, brier 0.2191, log_loss 1.0789
```

El pipeline funciona sobre datos reales y la separación temporal declarada es correcta para este caso.

### 11.3 Deficiencias

| Área | Estado | Detalle |
|---|---|---|
| Purga de etiquetas | OK en pipeline | Verificada; falla cerrado con posiciones dispersas. |
| Selección de split | Parcial | Sigue usando `gap` en filas; la comprobación por posiciones es la autoridad, pero no auto-ajusta el split. |
| `chronological_split` | Legacy | No se usa en producción; no purga. |
| Walk-forward | **Parcial/riesgoso** | Construye `build_dataset` por separado para train y test, reiniciando indicadores/volatilidad en cada ventana; no valida purga de etiquetas; no reporta dispersión ni observaciones. |
| Métricas ML | **Parcial** | `_valid_proba` no comprueba longitud contra `y` ni suma por fila; labels duplicados no se rechazan. Con filas que suman 0.5 se calculan métricas silenciosamente. |
| Features finitas | Parcial | `build_dataset` hace `dropna()` pero no rechaza `inf`; `validate_features` no se invoca en `run_training`. |
| Pesos del ensemble | **No aplicados** | `w_rf`/`w_xgb` de config no se usan; `_CalibratedEnsemble` fija 50/50. |
| Abstención | **No cableada** | `abstain_threshold` no se usa en pipeline/decisión. |
| GPU | Riesgo de portabilidad | `gpu_available()` depende de `USE_CUDA`; no hay fallback a CPU si el entrenamiento CUDA falla. En este equipo funciona. |
| Artefactos | **P0/P1** | Nombres fijos sin símbolo/timeframe; JSON y joblib no atómicos; procedencia inconsistente en `_t8/_t9`. |
| 1d | Limitación de datos | 30 filas; no se pueden generar filas etiquetadas. |

---

## 12. Compatibilidad arquitectónica multi-activo

### 12.1 Matriz por capa

| Capa | ¿Soporta múltiples activos? | Evidencia / límite |
|---|---|---|
| Configuración | **Parcial** | `settings.yaml` tiene un solo `symbol`; `timeframes` global. |
| Provider | **Parcial** | `BinanceOHLCVProvider(symbol=...)` acepta símbolo, pero la clase instancia `ccxt.binance` y `market_type=spot` fijos; `exchange`/`market_type` de config no se usan. |
| Storage | **Sí (nombres)** | `path_for(symbol, timeframe)` incluye el símbolo; no hay aislamiento por exchange. |
| Validación de datos | **Sí (genérica)** | No depende del símbolo, pero no valida gaps ni metadatos de mercado. |
| Features/indicadores | **Sí (genérica)** | Cálculos por serie; no hay metadatos de instrumento. |
| Multi-timeframe | **Sí (genérica)** | `align_higher_timeframe` funciona por par base/higher; no hay orquestación multi-símbolo. |
| Labels/dataset | **Parcial** | Horizonte en número de barras; no incluye símbolo/timeframe en el dataset. |
| Pipeline ML | **No** | Manifiesto sin símbolo/timeframe; artefactos `rf/xgb/calibrator` fijos; un `model_dir` compartido se sobrescribe. |
| DecisionEngine | **No** | Sin `symbol`; umbrales/pesos globales; un estado de decisión por llamada. |
| RiskManager | **No** | Un capital, una exposición y un estado de cooldown globales; sin límites por activo. |
| Sizing | **No** | `quantity_step=0.0001`, `q_min=0.00001` globales; sin tick size, min notional ni metadatos de exchange. |
| Accounting | **Parcial** | Funciones genéricas, pero sin moneda/activo; la colateralización no está centralizada. |
| BacktestEngine | **No** | Una sola posición y un solo `mark_price`; no hay cartera. |
| PaperBroker | **No** | `Position`/trade no tienen `symbol`; `check_stops(high, low)` aplica el mismo precio a todas las posiciones; el estado JSON no segrega activos. |
| Dashboard | **No** | Un único broker/estado; no hay selector de activo. |
| CLI | **Parcial** | `download_data.py --symbol` permite descargar otro símbolo, pero no hay orquestación de entrenamiento/backtest por símbolo. |

### 12.2 Conclusión

**Compatibilidad multi-activo: parcial, solo en ingesta y cálculo de features para un activo a la vez.** No es posible operar una cartera concurrente BTC+ETH con el código actual sin cambios arquitectónicos en:

1. identidad de instrumento en posiciones, trades, órdenes y estado;
2. contabilidad por activo y valoración multi-mercado;
3. `RiskManager` y sizing por instrumento (tick, step, min notional, concentración);
4. motor de backtest de cartera y benchmarks por activo;
5. registro de modelos por símbolo/timeframe/versión;
6. orquestación y dashboard multi-símbolo.

Los defaults BTC (`step=0.0001`, `q_min=1e-5`) no son válidos para todos los activos.

---

## 13. Informe de errores priorizado

### P0 — Integridad financiera / procedencia

| ID | Defecto | Evidencia | Impacto | Archivos |
|---|---|---|---|---|
| AUD-01 | Gap en apertura supera stop/take y se cierra al nivel | Gap bajista: `+47.24` ficticio; gap alcista: `-87.01` ficticio | Backtest inválido; métricas y decisiones no confiables | `backtesting/engine.py` |
| AUD-02 | Cortos sin exigir caja libre para colateral | `cash=98.1`, `collateral=1000.0` aceptado | Riesgo de corto sin colateral; contrato documentado incumplido | `risk/sizing.py`, `paper/broker.py`, `backtesting/engine.py` |
| AUD-03 | `RiskManager` acepta NaN y aprueba | `update_capital(nan)` / `register_trade_result(nan)` → `approve=True` | Se saltan drawdown, pérdida diaria y exposición | `risk/risk_manager.py` |
| AUD-04 | Procedencia de artefactos inconsistente | `_t8` y `_t9` joblib idénticos, métricas distintas; `_t7` schema 1 | Métricas/modelos no auditables; riesgo de usar el artefacto equivocado | `ml/pipeline.py`, `models/*` |
| AUD-05 | Sin control de versiones | `.git` inexistente | No hay commit/rollback ni diff verificable | Raíz del proyecto |

### P1 — Integración, validación y corrección

| ID | Defecto | Evidencia | Archivos |
|---|---|---|---|
| AUD-06 | `DecisionEngine` rechaza `np.ndarray` | `np.array([0.1,0.2,0.7])` → `HOLD / invalid probabilities`; lista → `LONG_SIMULATED` | `decision/engine.py` |
| AUD-07 | Señal long/short con cero timeframes | `{}` → `LONG_SIMULATED` con razón “timeframe agreement”; `conflict_penalty` no se aplica | `decision/engine.py` |
| AUD-08 | `RiskManager` no integrado en backtest/broker | `approve/update_time/advance/update_capital/register_trade_result` sin llamadas en `src/` | `backtesting/engine.py`, `paper/broker.py` |
| AUD-09 | Métricas de backtest no interpretables | `sqrt(252)` fijo; `exposure=trades/bars`; `gross_return` sin slippage; breakeven como pérdida | `backtesting/metrics.py` |
| AUD-10 | Validación OHLCV incompleta | `NaN` en `open` aceptado; duplicados eliminados en silencio; `open` fuera de `[low,high]` aceptado | `data/validation.py` |
| AUD-11 | Métricas ML aceptan probabilidades inválidas | Filas que suman 0.5 producen `roc_auc/brier/log_loss`; longitud `y≠proba` genera métricas parciales | `ml/metrics.py` |
| AUD-12 | Walk-forward reinicia features y no purga | `build_dataset(train_df)` y `build_dataset(test_df)` separados; sin comprobación de label-end | `ml/walkforward.py` |
| AUD-13 | Configuración no cableada | `w_rf`, `w_xgb`, `abstain_threshold`, `atr_*`, `benchmarks`, `exchange`, `market_type`, `storage_format` sin uso | `config/*`, `ml/pipeline.py`, `backtesting/engine.py` |
| AUD-14 | Multi-activo no soportado fuera de datos/features | Sin `symbol` en posición/trade/backtest/risk/artefactos; `check_stops` usa un solo precio | Varios |
| AUD-15 | 1d sin datos suficientes | `build_dataset` 1d lanza “no labeled rows” | `data/raw/BTC_USDT_1d.parquet` |
| AUD-16 | Guardado de modelos no atómico | `save_artifact` escribe joblib y JSON por separado; sin checksum | `ml/pipeline.py` |
| AUD-17 | Provider acoplado a Binance/red | `ccxt.binance` en `__post_init__`; `exchange`/`market_type` ignorados | `data/provider.py` |
| AUD-18 | `is_stale` falla con datetime naive | `TypeError: can't subtract offset-naive and offset-aware datetimes` | `paper/realtime.py` |
| AUD-19 | Cobertura de tests insuficiente en rutas críticas | Sin tests de gaps, colateral, NaN, multi-activo, configuración | `tests/*` |

### P2 — Calidad, robustez y documentación

| ID | Defecto | Evidencia |
|---|---|---|
| AUD-20 | `validate_number` acepta bool/strings | `True→1.0`, `"1.0"→1.0` |
| AUD-21 | `execution_price` permite slippage extremo | `slippage>=1` puede producir precio ≤ 0 |
| AUD-22 | Código/duplicados legacy | `position_sizing`, `stops`, `chronological_split`, `ensemble_proba` |
| AUD-23 | Defaults de riesgo inconsistentes | `PaperBroker.risk_budget_ratio=0.1` vs config `0.01` |
| AUD-24 | Persistencia de broker incompleta | `risk_state` sin `capital` produce `KeyError`; sin identidad de equity con posiciones abiertas |
| AUD-25 | Dashboard incompleto | `equity_dataframe` no devuelve timestamp/equity y `cap` no se usa; páginas placeholder |
| AUD-26 | Ruff/Mypy/format no limpios | 47 errores Ruff; 31 archivos sin formato; 2 errores con `--check-untyped-defs` |
| AUD-27 | Documentación desactualizada | `phase0_phase1_report.md` dice 155 tests/53 Ruff/27 format; hoy 238/47/31; dice que faltan contratos contables ya parcialmente implementados |
| AUD-28 | Sin CI, cobertura ni lockfile | No `.github`, no `coverage`, no lock |
| AUD-29 | Sin stubs de tipos en `dev` | `pandas-stubs`, `types-PyYAML` ausentes |
| AUD-30 | Sin `[tool.mypy]` | `mypy src` solo pasa con `--ignore-missing-imports` |

---

## 14. Registro de deuda técnica

| ID | Tipo | Descripción | Severidad | Fase propuesta |
|---|---|---|---|---|
| TD-01 | Integridad backtest | Modelar gaps: si `open` cruza stop/take, ejecutar en `open` o rechazar la entrada; no cerrar en un nivel ya superado. | P0 | 0.2 |
| TD-02 | Contabilidad | Unificar un ledger de caja/colateral/equity y exigir `free_cash >= q*P+fee` en cortos; corregir `calculate_cash_short`. | P0 | 0.2 |
| TD-03 | Riesgo | Validar finitud en `update_capital`, `register_trade_result` y `exposure`; fallar cerrado con NaN. | P0 | 0.2 |
| TD-04 | Artefactos | Registro de modelos con símbolo, timeframe, versión, hash de dataset, checksum y escritura atómica. | P0 | 0.2 |
| TD-05 | Proceso | Inicializar Git y crear commit de línea base con el manifiesto. | P0 | 0.1/0.2 |
| TD-06 | Integración riesgo | Conectar `RiskManager` a backtest y broker: approve, equity, drawdown, daily loss, exposure, cooldown. | P1 | 0.3 |
| TD-07 | Decisiones | Aceptar arrays/listas; exigir al menos una confirmación temporal; aplicar `conflict_penalty`; eliminar código muerto. | P1 | 0.3 |
| TD-08 | Métricas | Timeframe explícito para Sharpe/Sortino; exposición por tiempo/notional; gross return con slippage; benchmarks. | P1 | 0.3 |
| TD-09 | Datos | Validar NaN/inf/OHLC completo, `open` dentro de rango, gaps, zona horaria y no eliminar duplicados sin reportar. | P1 | 0.3 |
| TD-10 | Métricas ML | Validar longitud `y/proba`, suma por fila, labels únicos y orden de columnas. | P1 | 0.3 |
| TD-11 | Walk-forward | Construir features una vez sobre la serie completa y recortar ventanas; purga explícita; dispersión y conteos. | P1 | 0.3 |
| TD-12 | Config | Schema validado (Pydantic) y cableado real de todas las claves; perfiles por símbolo. | P1 | 0.3 |
| TD-13 | Multi-activo | Añadir `instrument` a Position/Trade/Order/Decision/Risk; portfolio engine; límites por activo; metadatos de mercado. | P1 | 0.4 |
| TD-14 | Datos 1d | Ampliar histórico (≥ 6–12 meses) o impedir explícitamente el entrenamiento 1d con mensaje de cobertura. | P1 | 0.3 |
| TD-15 | Provider | Abstraer exchange; inyectar cliente; añadir reintentos/backoff y validación de `limit`; no crear red en el constructor. | P1 | 0.3 |
| TD-16 | Realtime | Normalizar timestamps naive/aware y probar `is_stale`. | P1 | 0.3 |
| TD-17 | Persistencia | Validar `risk_state` y la identidad de equity con posiciones abiertas; esquema con `symbol`/timestamps. | P1 | 0.3 |
| TD-18 | Tests | Añadir regresiones negativas para AUD-01…AUD-18, multi-activo y configuración. | P1 | 0.2+ |
| TD-19 | Calidad | Ruff 47→0, formato 31→0, Mypy configurado y `--check-untyped-defs` limpio. | P2 | 0.5 |
| TD-20 | Documentación | Actualizar README y reportes; documentar el estado real de Phase 2a y los artefactos. | P2 | 0.5 |
| TD-21 | CI/CD | Pipeline con pytest, Ruff, Mypy, cobertura mínima y hash de artefactos. | P2 | 0.5 |
| TD-22 | Dependencias | Eliminar `pydantic`/`loguru` si no se usan; añadir stubs; lockfile. | P2 | 0.5 |
| TD-23 | Dashboard | Implementar curvas de equity reales, selector de símbolo y estados; o marcar como no funcional. | P2 | 0.5 |
| TD-24 | API legacy | Consolidar `position_sizing`/`stops`/`chronological_split`/`ensemble_proba` o eliminarlos. | P2 | 0.5 |

---

## 15. Referencia verificable

Se añadió:

```text
docs/phase0_1_baseline_manifest.sha256
```

Contiene 115 hashes SHA-256 de:

- `scripts/`
- `src/tradingai/` (sin `egg-info`)
- `tests/`
- `config/`
- `data/`
- `models/`
- `docs/` existentes
- `pyproject.toml`, `requirements.txt`, `README.md`, `OPEN_CODE_HANDOFF.md`

El manifiesto **no incluye** este informe ni a sí mismo. Formato compatible con `sha256sum -c`:

```text
<hash>  <ruta relativa>
```

Verificación:

```text
Get-Content docs/phase0_1_baseline_manifest.sha256 | ...
```

Los hashes de fuente, tests, configuración, datos y modelos se comprobaron antes y después de esta auditoría; no cambiaron. Los únicos archivos nuevos son los dos documentos indicados.

No hay commit Git; el manifiesto es la referencia de integridad disponible. Se recomienda crear un commit de línea base antes de cualquier cambio funcional.

---

## 16. Limitaciones de esta auditoría

1. **No hay cobertura de líneas/branches**; no se instaló `coverage` para no alterar el entorno. La evaluación de huecos es por inspección y por los tests existentes.
2. **No se probó la red** de Binance/CCXT; el provider se validó con mock y por inspección. No se descartan cambios de API/rate limits.
3. **No se ejecutó una estrategia completa** con datos reales; el backtest se probó con datos sintéticos y casos controlados de gaps/contabilidad.
4. **No se modificó ni regeneró ningún modelo**; los artefactos existentes se cargaron/inspeccionaron, no se reentrenaron en `models/`.
5. **No se probó multi-activo** porque la arquitectura no lo permite; la conclusión es por análisis de firmas/estado.
6. **No se evaluó rentabilidad**. Ningún resultado de backtest o modelo debe interpretarse como expectativa de rendimiento.
7. **No se revisó seguridad de credenciales** porque el proyecto es paper-only y no usa endpoints privados; el provider es público.
8. **La auditoría es de línea base**, no una certificación de ausencia de errores.

---

## 17. Prioridad recomendada para Fase 0.2

Sin implementar nada en esta fase, el orden técnico sugerido es:

1. **Congelar la línea base**: crear Git y commit con el manifiesto.
2. **AUD-01**: corregir la semántica de gaps en el backtest y añadir tests de gap alcista/bajista.
3. **AUD-02**: decidir y hacer cumplir el contrato de colateral; corregir `calculate_cash_short` y las comprobaciones de broker/engine.
4. **AUD-03**: validación finita en `RiskManager` y fallo cerrado ante NaN.
5. **AUD-04**: registrar/aislar artefactos; no usar `_t8/_t9` como referencia; definir modelo canónico.
6. **AUD-06/07/08**: integrar decisión/riesgo/ejecución y sanear entradas.
7. **AUD-09/10/11/12**: métricas, datos, métricas ML y walk-forward.
8. **AUD-13/14**: cablear configuración y diseñar multi-activo antes de añadir estrategias.
9. **Calidad**: Ruff/Mypy/format/CI al final, cuando el comportamiento esté cubierto.

---

## Apéndice A — Evidencia de comandos

```text
python --version
Python 3.13.15

python -m pip check
No broken requirements found.

python -m pytest --collect-only -q
238 tests collected

python -m pytest -q
238 passed, 1 warning in 23.68s

python -m ruff check .
Found 47 errors.
30 fixable with --fix

python -m ruff format --check .
31 files would be reformatted, 40 files already formatted

python -m mypy src --ignore-missing-imports
Success: no issues found in 35 source files

python -m mypy src
Found 26 errors in 16 files (all import-untyped)

python -m mypy src --ignore-missing-imports --check-untyped-defs
src/tradingai/ml/walkforward.py:24: error: Need type annotation for "results"
src/tradingai/ml/walkforward.py:61: error: Value of type "object" is not indexable
Found 2 errors in 1 file

python -c "import ... all package modules"
34 modules imported; IMPORT_OK
```

## Apéndice B — Comprobaciones controladas reproducidas

```text
# Backtest gap bajista
entrada 90.0, stop 99.495, salida 99.495, PnL +47.2386

# Backtest gap alcista
entrada 120.0, take 102.51, salida 102.51, PnL -87.0145

# Colateral de corto
capital 1000, long 9@100 -> cash 99.1
short 10@100 -> aceptado, cash 98.1, collateral 1000.0

# RiskManager NaN
update_capital(nan) -> approve(...) == (True, "approved")
register_trade_result(nan) -> capital nan, approve(...) == (True, "approved")

# DecisionEngine
list [0.1,0.2,0.7] -> LONG_SIMULATED
np.array([0.1,0.2,0.7]) -> HOLD / invalid probabilities
{} timeframes -> LONG_SIMULATED / "bullish ensemble and timeframe agreement"

# Validación OHLCV
open=NaN -> validado sin error
filas duplicadas -> reducidas de 2 a 1 en silencio

# Métricas ML
proba rows sum 0.5 -> roc_auc=1.0, brier=0.315, log_loss=1.4067, ece=0.55
y len 2 / proba len 3 -> métricas None con razones de broadcast

# Realtime
'2024-01-01T00:00:00' -> TypeError naive/aware

# Identidades contables
500 casos PaperBroker -> 0 fallos
200 casos BacktestEngine -> 0 fallos
```

---

**Fin del informe.**
