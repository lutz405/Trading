# Fase 0.2.1 — AUD-02.1: efectivo libre acumulado en PaperBroker

**Fecha:** 2026-11-25  
**Alcance:** autorización de nuevas operaciones contra el efectivo libre, descontando el colateral de todos los cortos abiertos.  
**Modo:** Paper Trading / investigación. Sin apalancamiento, margen, órdenes reales ni cambios de estrategia.  
**Resultado:** AUD-02.1 corregido; **15 regresiones nuevas**; suite total **325 passed**.

---

## 1. Causa raíz

`PaperBroker.open_position()` usaba `self.capital` como efectivo disponible:

```text
cash = self.capital
if notional + fee > self.capital:
    return False
```

El modelo contable mantiene el colateral de los cortos dentro de `capital` y lo expone aparte en `collateral` para que se cumpla:

```text
Equity = Cash + Collateral + LongAssets - ShortLiabilities
```

Por tanto, `capital` es efectivo **total**, no efectivo libre. Al no restar el colateral ya comprometido, cada nueva operación podía reutilizar el efectivo reservado por cortos anteriores. Se reprodujo con dos cortos de 600 sobre 1.000 de capital: ambos se aceptaban, dejando `free_cash = -200`, aunque la equity contable siguiera mostrando 1.000.

## 2. Corrección

Se añadió una propiedad derivada, sin campo persistido y sin duplicar el ledger:

```text
free_cash = capital - collateral
```

`collateral` ya suma `qty * entry_price` de **todas** las posiciones short abiertas. La autorización quedó:

```text
free_cash = capital - Σ(q_i * entry_i)   para todo short abierto i
new_notional + new_entry_fee <= free_cash
```

Cambios en `src/tradingai/paper/broker.py`:

1. `open_position()` pasa `cash=self.free_cash` al sizing canónico `calculate_position_size()`.
2. La guardia final exige `notional + fee <= self.free_cash` para long y short.
3. Se documentaron `cash` (total) y `collateral` (comprometido).

No se modificó la identidad de equity, ni las fórmulas de `capital`/`collateral`, ni `BacktestEngine`, `RiskManager`, `sizing.py`, datos, modelos o configuración. No se añadió un segundo cálculo de sizing: el broker sigue usando la función canónica y solo verifica la invariante de caja.

## 3. Pruebas

Archivo creado: `tests/test_aud02_1_paper_free_cash.py` (15 tests, parametrizados con y sin comisión/slippage).

| Requisito | Cobertura |
|---|---|
| Dos shorts individualmente financiables, conjuntamente no | 6 + 6 sobre 1.000: el segundo se rechaza |
| Varios shorts cuya suma sí cabe | 3 × 3 sobre 1.000: los tres se aceptan |
| Long después de short | long 5 rechazado con 400 libres; long 3,9 aceptado |
| Short después de long | short 5 rechazado con ~400 libres; short 3,9 aceptado |
| Rechazo sin mutaciones | capital, colateral, posiciones, trades, fees, slippage y realizados intactos |
| Cierre libera colateral | tras cerrar el short, `free_cash == capital` y se puede reabrir |
| Identidades en secuencia | equity, colateral, `capital == initial + realized_net` al quedar plano |
| Persistencia | `save`/`load` conserva capital, colateral y `free_cash`; cierre posterior consistente |

Casos con `fee=0.001` y `slippage=0.0005` incluidos en las principales regresiones y en el caso de persistencia.

## 4. Validación

```text
python -m pytest -q
325 passed, 1 warning in 9.34s

python -m pytest -q tests/test_aud02_1_paper_free_cash.py tests/test_aud02_short_collateral.py tests/test_phase2a_accounting.py tests/test_risk_sizing_contract.py tests/test_paper.py tests/test_backtesting.py
104 passed, 1 warning in 1.00s

python -m ruff check .
Found 47 errors.            # idéntico a la línea base

python -m ruff format --check .
31 files would be reformatted, 47 already formatted   # idéntico a la base en archivos sin formatear

python -m mypy src --ignore-missing-imports --check-untyped-defs
src/tradingai/ml/walkforward.py:24: error: Need type annotation for "results"
src/tradingai/ml/walkforward.py:61: error: Value of type "object" is not indexable
Found 2 errors in 1 file (checked 35 source files)   # preexistentes

python -m pip check
No broken requirements found.
```

Verificación aleatoria fuera de la suite (300 escenarios, 30 pasos, long/short, fees y slippage variables):

```text
aperturas aceptadas verificadas = 4171
intentos de sobrecompromiso verificados = 1088
fallos = 0
```

Invariantes comprobadas en cada paso:

- `free_cash == capital - collateral`.
- `collateral == Σ(q_i * entry_i)` de shorts abiertos.
- `equity(mark) == capital + collateral + longMV - shortLiab`.
- Tras una apertura aceptada, `free_cash >= 0`.
- Al quedar plano: `capital == initial_capital + realized_net_pnl`, `free_cash == capital`.
- `fees_paid == Σ fees`, `slippage_cost == Σ slippage`, `trade.pnl == gross_pnl - fees`.

## 5. Limitaciones restantes

- `free_cash` es derivado y no se persiste; no se añadió un segundo campo que pudiera desincronizarse. `load()` sigue validando el colateral persistido contra las posiciones.
- `free_cash` puede volverse negativo tras un cierre adverso; las nuevas aperturas se rechazan, pero no existe liquidación automática ni gestión de riesgo de cartera. Es el contrato preexistente de `PaperBroker`, que permite capital negativo al cerrar.
- `BacktestEngine` mantiene una sola posición y no requiere esta acumulación; no se tocó.
- El repo sigue trackeando `__pycache__`; ejecutar pruebas modifica el `.pyc` compilado. No es un cambio de código fuente.
- La integración del `RiskManager` en el flujo de ejecución (AUD-08) y la procedencia de modelos (AUD-04) siguen fuera de alcance.
