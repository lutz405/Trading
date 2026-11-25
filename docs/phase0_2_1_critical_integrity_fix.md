# Fase 0.2.1 — Corrección de integridad crítica (AUD-01…AUD-03)

**Fecha:** 2026-11-25  
**Alcance:** gaps del backtest, colateral de cortos y validación finita del `RiskManager`.  
**Modo:** Paper Trading / investigación. No se añadió ejecución real, apalancamiento, margen, credenciales privadas ni nuevas estrategias.  
**Resultado:** AUD-01, AUD-02 y AUD-03 corregidos y cubiertos por regresiones. Las 238 pruebas históricas siguen pasando; la suite total es ahora **310 passed**.

---

## 1. Verificación previa del repositorio

| Comprobación | Resultado |
|---|---|
| Directorio de trabajo | `C:\TradingAI_BTC` |
| `.git` local | No existe |
| Git instalado | No (`git` no está en PATH ni en ubicaciones habituales) |
| Remoto oficial | `https://github.com/lutz405/Trading` (público, rama `main`) |
| Último commit remoto | `05e5373d1b8131f37479e672c07e24e6698f0a67` |
| Comparación local vs `origin/main` | Contenido idéntico antes de esta subfase; solo diferían finales de línea CRLF/LF y el `.gitattributes` remoto |
| Manifiesto base | 115/115 hashes válidos al inicio |
| Modificaciones locales previas | Ninguna divergente del remoto |
| Copia de seguridad | `C:\TradingAI_BTC_backups\TradingAI_BTC_pre_phase0_2_1_20261125_162602.zip` |
| SHA-256 de la copia | `3abc298bc02712583f399c186b8839acd369abfb5c658bd4a8ec0313695c76a0` |
| Archivos funcionales modificados | 4 (ver §3) |
| Archivos creados | 3 tests + este informe |

No se ejecutó ninguna operación Git destructiva ni se modificó el remoto.

### 1.1 Procedimiento seguro para conectar Git (no ejecutado)

Git no está instalado en esta máquina, por lo que no se pudo crear el repositorio local ni comparar con `git status`. Una vez instalado Git para Windows, el procedimiento seguro es:

```powershell
# 1. Crear una copia nueva antes de tocar Git
Compress-Archive -Path C:\TradingAI_BTC\* -DestinationPath C:\TradingAI_BTC_backups\pre_git.zip

# 2. Inicializar y enlazar el remoto
cd C:\TradingAI_BTC
git init
git remote add origin https://github.com/lutz405/Trading.git
git fetch origin

# 3. Fijar la rama local sobre origin/main sin tocar el árbol de trabajo
git branch --track main origin/main
git symbolic-ref HEAD refs/heads/main
git reset --mixed

# 4. Revisar antes de confirmar
git status
git diff --stat
```

`git reset --mixed` solo reconstruye el índice; **no** modifica archivos del usuario. No usar `--hard`, `git clean`, force push ni reescribir el remoto. El `.gitattributes` remoto normaliza a LF, por lo que `git status` puede mostrar ruido de finales de línea; revisarlo antes de hacer el primer commit. Después:

```powershell
git switch -c phase0.2.1-critical-fixes
git add src/tradingai/backtesting/engine.py src/tradingai/paper/broker.py src/tradingai/risk/risk_manager.py src/tradingai/risk/sizing.py tests/test_aud01_backtest_gaps.py tests/test_aud02_short_collateral.py tests/test_aud03_risk_finite.py docs/phase0_2_1_critical_integrity_fix.md
git commit -m "fix: correct backtest gaps, short collateral and risk NaN validation"
```

No se debe hacer push sin autorización expresa.

---

## 2. Causa raíz y corrección

### AUD-01 — Salidas ficticias en gaps

**Causa raíz:** `BacktestEngine.run()` llenaba la orden pendiente en `open[i]` y, en la misma vela, comparaba `low[i]`/`high[i]` con el stop/take calculado sobre el cierre anterior. Si la apertura ya había superado el nivel, el motor ejecutaba la salida **al nivel**, no al precio disponible. Eso convertía un gap adverso en ganancia y uno favorable en pérdida.

**Corrección (`backtesting/engine.py`):**
- Nuevo `_exit_gap(idx, open_price)`: si la apertura ya cruzó el stop o el take, se cierra **a la apertura** (con slippage de salida), no al nivel.
- La comprobación de gap se ejecuta antes de la comprobación intravela, tanto para posiciones recién abiertas como para posiciones existentes.
- Si el precio abre entre los niveles, se conserva la lógica intravela y la prioridad conservadora **stop-first** cuando ambos se tocan en la misma vela.
- Se valida que `open`, `high`, `low` sean finitos y positivos antes de usarlos.
- La decisión sigue tomándose con el cierre de la vela y la entrada en la apertura siguiente: no se introdujo lookahead.

**Evidencia antes/después (fee=0, slippage=0):**

| Caso | Antes | Después |
|---|---|---|
| Long, apertura 90, stop 99 | entrada 90, salida 99, **PnL +45** | entrada 90, salida 90, **PnL 0** |
| Long, apertura 120, take 102 | entrada 120, salida 102, **PnL −90** | entrada 120, salida 120, **PnL 0** |
| Short, apertura 110, stop 101 | entrada 110, salida 101, **PnL +45** | entrada 110, salida 110, **PnL 0** |
| Short, apertura 90, take 98 | entrada 90, salida 98, **PnL −40** | entrada 90, salida 90, **PnL 0** |

### AUD-02 — Colateral de cortos

**Causa raíz:** `calculate_cash_short()` dimensionaba la cantidad solo para cubrir la comisión:

```text
q_cash = cash / (fee_rate * entry_exec)
```

No exigía `q * P` de colateral. Además, `PaperBroker` y `BacktestEngine` solo comprobaban que la comisión cupiera en caja, no el notional completo del corto.

**Corrección:**
- `risk/sizing.py`: `calculate_cash_short()` ahora aplica el contrato documentado:

```text
free_cash >= q * P + fee
fee = q * P * fee_rate
q_cash = cash / (P * (1 + fee_rate))
```

- Si `cash <= 0`, devuelve `0.0`; con `fee_rate = 0` devuelve `cash / P` (finito), nunca `inf`.
- `PaperBroker.open_position()` y `BacktestEngine._enter()` exigen `notional + fee <= free_cash` para **long y short**.
- `calculate_position_size()` sigue siendo la función canónica; broker y backtest la usan. Las guardias adicionales solo verifican la invariante, no recalculan sizing.
- No se añadió apalancamiento ni margen: el corto sigue siendo totalmente colateralizado en cash.

**Evidencia antes/después (`capital=1000`, `fee=0.001`, `price=100`):**

| Comprobación | Antes | Después |
|---|---|---|
| `calculate_cash_short(1000, 100, 0.001)` | `10000.0` | `9.99000999` |
| Cantidad máxima de sizing | `20` (limitada por exposición) | `9.99` |
| Corto explícito de `20` en PaperBroker | aceptado, colateral 2000, caja 998 | **rechazado**, sin mutación |
| Corto explícito de `20` en BacktestEngine | abierto, colateral 2000 | **rechazado**, capital 1000 |

### AUD-03 — RiskManager ante NaN/Inf

**Causa raíz:** `update_capital()` y `register_trade_result()` asignaban el valor sin validarlo. `approve()` comparaba con `>`; cualquier comparación con `NaN` es falsa, de modo que un estado `NaN` evitaba drawdown, pérdida diaria y exposición. Tampoco se validaban volatilidad, precio, ATR ni probabilidades no finitas.

**Corrección (`risk/risk_manager.py`):**
- Helpers estrictos `_require_finite()` y `_require_periods()`: rechazan `bool`, tipos no numéricos, `NaN`, `+Inf` y `-Inf`; nunca convierten silenciosamente strings.
- `__post_init__()` valida capital inicial, parámetros y acumuladores.
- `_state_error()` valida todo el estado financiero antes de aprobar: capital, pico, pérdida diaria, exposición, parámetros, cooldown y coherencia `peak_capital >= capital`.
- `approve()` rechaza primero estados corruptos y luego valida probabilidades, volatilidad, precio y ATR antes de aplicar los límites.
- `update_capital()` y `register_trade_result()` validan **antes** de mutar; un resultado que dejaría capital negativo o no finito lanza `ValueError` y deja el estado intacto.
- `from_dict()` añade validación de rangos (`max_drawdown`, `max_daily_loss`, `uncertainty_threshold`, etc.).

**Evidencia antes/después:**

| Entrada | Antes | Después |
|---|---|---|
| `update_capital(NaN)` | capital `NaN`, `approve=True` | `ValueError`, estado intacto |
| `register_trade_result(NaN)` | capital `NaN`, `approve=True` | `ValueError`, estado intacto |
| `exposure = NaN` | `approve=True` | `(False, "invalid risk state: exposure must be finite")` |
| volatilidad `NaN` | `approve=True` | `(False, "invalid volatility")` |
| volatilidad negativa | `approve=True` | `(False, "invalid volatility")` |
| precio `NaN` | `approve=True` | `(False, "invalid price")` |
| probabilidades con `NaN` | `approve=True` | `(False, "invalid probabilities")` |
| estado válido | `True` | `(True, "approved")` |

---

## 3. Archivos

### Modificados

| Archivo | Líneas | SHA-256 antes | SHA-256 después |
|---|---:|---|---|
| `src/tradingai/backtesting/engine.py` | 280 | `b476c891…0bc6b2` | `ec2272af…7a87ef` |
| `src/tradingai/paper/broker.py` | 427 | `5e0ebb49…a282dd` | `07685b89…a0656e` |
| `src/tradingai/risk/risk_manager.py` | 287 | `5894a7d5…02e95e` | `b03dd666…efc531` |
| `src/tradingai/risk/sizing.py` | 145 | `86d5cb26…4c981d` | `9e4deabd…f4d99c` |

### Creados

| Archivo | Líneas | SHA-256 |
|---|---:|---|
| `tests/test_aud01_backtest_gaps.py` | 118 | `22bd5e52…10191b` |
| `tests/test_aud02_short_collateral.py` | 145 | `6953b975…130fa9` |
| `tests/test_aud03_risk_finite.py` | 167 | `98ebc058…d146dd` |
| `docs/phase0_2_1_critical_integrity_fix.md` | — | — |

No se modificaron datos, modelos, configuración, dashboard ni pruebas existentes.

---

## 4. Pruebas nuevas

**72 tests nuevos**, todos pasan:

- **AUD-01 (8):** gap long a la baja, gap long al alza, gap short al alza, gap short a la baja, gap sobre posición existente long/short, y stop-first intravela long/short. Verifican salida a la apertura, PnL sin ficción, fees y identidad de capital/equity.
- **AUD-02 (11):** fórmula de colateral con y sin fee, cash no positivo, límite de sizing, rechazo de cortos no financiados en broker/backtest, frontera exacta de colateral y identidades contables al abrir/cerrar.
- **AUD-03 (53):** NaN/Inf/bool/strings en capital, resultados y exposición; capital negativo; estado corrupto; parámetros corruptos; probabilidades/volatilidad/precio/ATR inválidos; no mutación; estado válido; rangos de `from_dict`; constructor.

Las 238 pruebas históricas siguen pasando sin cambios.

---

## 5. Comandos y resultados exactos

```text
python -m pytest -q
310 passed, 1 warning in 10.47s

python -m pytest -q tests/test_aud01_backtest_gaps.py tests/test_aud02_short_collateral.py tests/test_aud03_risk_finite.py
72 passed, 1 warning in 0.94s

python -m pytest -q tests/test_phase2a_accounting.py tests/test_risk_sizing_contract.py tests/test_backtesting.py tests/test_paper.py tests/test_risk.py tests/test_state_validation.py tests/test_state_validation_full.py tests/test_critical_fixes.py
141 passed, 1 warning in 3.37s

python -m ruff check .
Found 47 errors.
30 fixable with --fix

python -m ruff format --check .
31 files would be reformatted, 44 files already formatted

python -m mypy src --ignore-missing-imports --check-untyped-defs
src/tradingai/ml/walkforward.py:24: error: Need type annotation for "results"  [var-annotated]
src/tradingai/ml/walkforward.py:61: error: Value of type "object" is not indexable  [index]
Found 2 errors in 1 file (checked 35 source files)

python -m mypy src
Found 26 errors in 16 files (import-untyped, preexistentes)

python -m pip check
No broken requirements found.
```

**Ruff:** 47 errores, idéntico a la línea base; no se introdujeron errores nuevos. El único `TRY004` nuevo se documentó y suprimió conscientemente para mantener `ValueError` como contrato único de validación de riesgo.  
**Formato:** 31 archivos pendientes, idéntico a la línea base; los 3 tests nuevos ya están formateados.  
**Mypy:** los 2 errores de `walkforward.py` y los 26 `import-untyped` son preexistentes y quedan fuera de alcance.  
**Warning:** `PytestRemovedIn10Warning` de `anyio`, ajeno al proyecto.

---

## 6. Invariantes contables verificadas

Se ejecutaron comprobaciones aleatorias fuera de la suite, con long/short, fees y slippage variables:

```text
PaperBroker: 600 aperturas/cierres financiados -> 0 fallos
BacktestEngine: 300 aperturas/cierres financiados -> 0 fallos
Cortos no financiados: 300 casos -> 0 aceptados
```

Invariantes comprobadas:

- `capital == initial_capital + realized_net_pnl` al cerrar.
- `trade.pnl == gross_pnl - fees`.
- Corto: `collateral == qty * entry_price`; `collateral + entry_fee <= free_cash` en la apertura.
- Equity de apertura: `initial_capital - entry_fee - slippage` (marcando al precio de referencia).
- `equity[-1] == capital` tras la liquidación final del backtest.

Los tests de identidad existentes (`test_phase2a_accounting.py`, etc.) siguen pasando.

---

## 7. Deuda técnica que permanece

Fuera del alcance de esta subfase:

- **AUD-04 (P0):** procedencia de artefactos de modelo; `_t8`/`_t9` tienen `.joblib` idénticos y métricas JSON distintas; `_t7` usa schema 1.
- **AUD-05 (P0):** no hay repositorio Git local ni commit de referencia.
- **AUD-06 (P1):** `DecisionEngine` sigue rechazando `np.ndarray` y `RiskManager.approve()` aún no acepta arrays (mantiene `if not proba`).
- **AUD-07 (P1):** señales con cero timeframes y `conflict_penalty` no aplicado.
- **AUD-08 (P1):** `RiskManager` no está integrado en el ciclo de ejecución de backtest/broker (solo se usa para sizing/config).
- **AUD-09…AUD-19 (P1):** métricas anualizadas, validación OHLCV, métricas ML, walk-forward, configuración no cableada, multi-activo, etc.
- El backtest sigue usando stops/takes fijos ±1 %/±2 % y no ATR; no se cambió para no alterar la estrategia.
- Los cortos siguen siendo mono-activo y sin ledger de cartera; la colateralización es por apertura, no un motor de cartera multi-activo.
- `PaperBroker` sigue permitiendo capital negativo al cerrar una posición (contrato preexistente), mientras `RiskManager` rechaza resultados que harían su capital negativo. Son estados separados y no integrados todavía.
- Ruff/format/Mypy globales siguen sin estar limpios.

---

## 8. Confirmación de alcance

- Solo se modificaron los 4 archivos indicados y se crearon 3 tests + este informe.
- No se tocaron datos históricos, modelos, configuración, dashboard, estrategias ni pruebas existentes.
- No se añadieron órdenes reales, apalancamiento, margen, credenciales privadas ni endpoints privados.
- No se declaró rentabilidad ni validez estadística.
- El manifiesto base `docs/phase0_1_baseline_manifest.sha256` se conserva intacto como referencia histórica.

---

## 9. Recomendación para la siguiente subfase

1. Auditoría independiente en modo solo lectura que reproduzca AUD-01…AUD-03 y busque regresiones.
2. Resolver AUD-04 (registro/procedencia de artefactos) y AUD-05 (Git) antes de nuevos modelos.
3. Después, AUD-06/AUD-07 (decisiones) y AUD-08 (integración real del riesgo), con pruebas negativas.
4. No avanzar a multi-activo ni a nuevas estrategias hasta cerrar los P0 restantes.

**Fin del informe.**
