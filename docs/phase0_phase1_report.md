# Phase 0 / Phase 1 report

Date: 2026-11-23
Scope: environment stabilisation (Phase 0) and ML integrity P0 fixes (Phase 1).
Paper trading only: no real orders, leverage, margin or private endpoints.

## 1. Recovery point

- Archive: `C:\TradingAI_BTC_backups\TradingAI_BTC_pre_phase0_1_20261123_194912.zip`
- SHA256: `4214119B581B7BB500E03F02F5A8347EEA781634E426933EF3E8533A4522A5F7`
- Size: 2,164,393 bytes, 162 archive entries (159 files).
- All 7 raw-data files under `data/raw/` were re-hashed after the work and are
  byte-identical to the archive.
- No project source, data or model file was deleted. Only generated
  `__pycache__` content differs from the archive.

## 2. Fixes applied

### P0-1 — Higher-timeframe look-ahead

`features/multitimeframe.py` used to merge on the higher-timeframe open
timestamp, so a 4h bar was visible from 00:00 even though it only closes at
04:00.

- Added an explicit `available_at = timestamp + bar_duration`.
- Inferred duration from the higher timestamp spacing, with an optional
  explicit `bar_duration`.
- Enforced valid, duplicate-free timestamps.
- Allowed an exact match at the close instant only; earlier base rows see the
  previous bar.
- Documented the Binance/CCXT convention and the rule in
  `docs/market_data_conventions.md`; updated `docs/indicators.md`.

Verified against the public Binance endpoint: a 1h candle has
`open=1795482000000`, `close=1795485599999` (`delta=3,599,999 ms`), so the
timestamp is the open time and the bar closes at `timestamp + duration`.

### P0-2 — Calibrator accepted invalid state

`ml/calibration.py` now:

- resets state on every `fit` and on a failed refit;
- rejects wrong shapes, non-finite values, values outside `[0,1]`, rows not
  summing to one, duplicate classes, unknown labels, missing validation
  classes, fewer than 2 classes and fewer than 30 samples;
- raises explicit errors from `transform` instead of silently passing through;
- uses calibration schema v2;
- persists metadata and joblib atomically, with a SHA256 checksum;
- rejects schema v1, missing joblib, tampered metadata, tampered joblib,
  fitted/unfitted mismatches and class/method mismatches on load.

Operational impact: schema-1 calibrator files are no longer accepted. Only
test artifacts existed in `models/`; there is no production model.

### P0-3 — Undefined-volatility labels

`ml/labels.py` used to assign rows with undefined volatility to the sideways
class.

- Rows without a valid volatility estimate or future close remain `NaN`.
- `horizon` must be a positive integer and `vol_mult` a positive finite
  number.
- `close` must be finite and positive.
- `ml/dataset.py` propagates `vol_mult`, validates feature columns, rejects
  empty datasets and preserves the dataframe index for alignment.

### P0-4 / P0-5 — Temporal split, classes and evaluation

`ml/pipeline.py` now:

- builds datasets with the configured `vol_mult`;
- validates timestamps (valid, unique, sorted) and that `X`/`y` share the
  same unique index in chronological dataframe order;
- requires `gap >= horizon`;
- splits by dataframe row position, not by arithmetic on `X.index`;
- emits a split manifest with row ranges, dataframe positions and label ends;
- requires all `[0, 1, 2]` classes in train and validation;
- sets XGBoost `num_class` from the observed classes and rejects
  non-contiguous labels;
- aligns model probabilities to the expected class order and normalises rows;
- requires `classes_`, non-empty partitions and labels inside the model
  classes for `evaluate`;
- rejects an unfitted calibrator in `_CalibratedEnsemble`;
- computes finite multiclass metrics when a test partition misses a class;
- records versions and split metadata in the artifacts.

### P0-6 — Leakage tests were tautological

`tests/test_leakage_indices.py` now compares learned state, not just index
sets:

- train/validation/test positions come from the manifest;
- RF, XGBoost and calibrated ensemble outputs are compared between the full
  model and a model retrained without the holdout;
- train indices and the calibration sample count are captured and checked;
- artifacts are written to temporary directories.

### Phase 0 / hygiene

- Installed `mypy 2.4.1` and `setuptools 84.2.1`.
- Added `src/tradingai/decision/__init__.py` so the package is included in
  builds.
- Removed the repository-writing test: `tests/test_ml.py` now uses a temporary
  `model_dir`. A full test run no longer changes `models/`.
- Fixed `paper/realtime.py` typing (`-> Any`, `datetime.UTC`, no unused
  import).
- Replaced blind metric exceptions with explicit exception types and unified
  multiclass label binarisation in `ml/metrics.py`.
- Removed dead imports/placeholders from `ml/walkforward.py`.
- Updated `pyproject.toml` Ruff `target-version` to `py313`, `README.md` to
  Python 3.13 and added pointers to the conventions document.

## 3. Files changed

Source:

- `src/tradingai/ml/pipeline.py`
- `src/tradingai/ml/calibration.py`
- `src/tradingai/ml/dataset.py`
- `src/tradingai/ml/labels.py`
- `src/tradingai/ml/metrics.py`
- `src/tradingai/ml/walkforward.py`
- `src/tradingai/ml/__init__.py` (import order only)
- `src/tradingai/features/multitimeframe.py`
- `src/tradingai/paper/realtime.py`

Documentation and configuration:

- `docs/market_data_conventions.md` (new)
- `docs/indicators.md`
- `README.md`
- `pyproject.toml`

Tests added:

- `tests/test_multitimeframe_causality.py` (3)
- `tests/test_calibration_contract.py` (8)
- `tests/test_labels_dataset_contract.py` (4)
- `tests/test_pipeline_contract.py` (7)

Tests strengthened/repaired:

- `tests/test_leakage_indices.py` (6)
- `tests/test_ml.py` (5)
- `tests/test_ml_temporal.py` (5)
- `tests/test_calibration_pipeline.py` (1)
- `tests/test_calibration_integration.py` (4)
- `tests/test_walkforward.py` (2)

Generated/build metadata also changed by `pip install -e .`:
`src/tradingai_btc.egg-info/*`. Existing `models/_t7`, `_t8`, `_t9`, `_test`
and `_testcal` test artifacts were left in place, as instructed. Earlier runs
regenerated their schema-v2 files; they are now frozen because tests use
temporary directories.

## 4. Regression coverage (old failure -> now passing test)

| Old failure | Regression test |
|---|---|
| 4h bar visible at its own open | `test_higher_bar_not_visible_at_its_open` |
| higher bar visible before close boundary | `test_higher_bar_visibility_at_minute_boundary` |
| duplicate higher timestamps merged silently | `test_align_rejects_duplicate_higher_timestamps` |
| out-of-range probabilities accepted | `test_fit_rejects_probabilities_outside_unit_interval` |
| mismatched proba/label lengths accepted | `test_fit_rejects_mismatched_lengths` |
| missing validation class accepted | `test_fit_rejects_missing_validation_class` |
| failed refit kept old fitted state | `test_invalid_refit_resets_previous_state` |
| calibrator loaded without joblib | `test_load_without_joblib_fails` |
| tampered metadata accepted | `test_load_rejects_tampered_metadata` |
| tampered joblib accepted | `test_load_rejects_tampered_joblib` |
| transform accepted wrong class count | `test_fitted_transform_requires_matching_class_columns` |
| undefined volatility became sideways | `test_undefined_volatility_rows_are_not_sideways` |
| invalid horizon accepted | `test_horizon_must_be_positive` |
| invalid vol_mult accepted | `test_vol_mult_must_be_positive_finite` |
| dataset dropped or misaligned rows | `test_dataset_drops_only_rows_without_label_or_features` |
| evaluation crashed/NaN with missing test class | `test_calibrated_ensemble_evaluates_when_test_misses_a_class` |
| single-class test partition failed | `test_calibrated_ensemble_evaluates_with_single_class_test_partition` |
| evaluation without explicit model classes | `test_evaluate_requires_explicit_model_classes` |
| XGBoost accepted non-contiguous labels | `test_train_xgb_rejects_non_contiguous_labels` |
| training proceeded with a missing label class | `test_run_training_fails_when_a_label_class_is_missing` |
| shuffled `X` rows passed temporal validation | `test_temporal_validation_rejects_shuffled_rows` |
| duplicate timestamps passed temporal validation | `test_temporal_validation_rejects_duplicate_timestamps` |

## 5. Verification results

Environment: Python 3.13.15, mypy 2.4.1, setuptools 84.2.1.

Full test suite:

```text
python -m pytest -q
155 passed, 1 warning in 8.20s
```

The single warning is third-party: `anyio`'s pytest plugin deprecates
`CallSpec2` for pytest 10.

Targeted regression group (new + strengthened test files):

```text
45 passed, 1 warning in 6.30s
```

Ruff on every changed/added Python file:

```text
python -m ruff check <changed files>
All checks passed!
```

```text
python -m ruff format --check <changed files>
19 files already formatted
```

Mypy:

```text
python -m mypy src --ignore-missing-imports
Success: no issues found in 33 source files
```

Only informational notes remain about untyped bodies in
`src/tradingai/backtesting/engine.py` (outside this phase's changes).

Repository-wide Ruff status (pre-existing debt outside this phase):

```text
python -m ruff check .
Found 53 errors (34 fixable)
```

Breakdown: 16 `I001` import order, 9 `F401` unused imports, 6 `F841` unused
variables, 5 `RUF059` unused unpacked variables, 4 `TRY004`, 3 `RUF022`,
2 `BLE001`, 2 `UP017`, 2 `UP037`, and one each of `UP035`, `FURB162`,
`SIM114`, `SIM103`. Concentrated in `risk/`, `paper/broker.py`,
`decision/engine.py`, `dashboard/`, `data/` and older tests. None are in the
corrected ML modules.

```text
python -m ruff format --check .
27 files would be reformatted, 36 files already formatted
```

The only unformatted file in `src/tradingai/ml/` is the untouched
`ensemble.py`.

End-to-end smoke test with the local parquet data and reduced estimators:

```text
1h: 662 labeled rows; train 0-388, validation 393-525, test 530-662;
    purge 6/6; classes [0,1,2]; calibration sigmoid; OK
1d: rejected with "no labeled rows with complete features" (only 30 raw rows)
```

The 1d rejection is expected with the current 30-day download; it is a data
coverage limit, not a pipeline regression.

## 6. Pending problems (not implemented in this phase)

P1 items, intentionally untouched:

- short/collateral/equity accounting and final-exit metrics;
- risk integration and `PaperBroker` validation/persistence;
- general data validation (gaps, duplicates, outliers, exchange downtimes);
- walk-forward purge enforcement (`run_walk_forward` still has only a fixed
  gap parameter and no explicit label-end purge validation);
- decision-engine ndarray/weight handling and its Ruff findings;
- inference/serving layer;
- repository-wide Ruff/format debt.

## 7. Residual risks

1. Row-based `horizon`/`gap` assume a regularly spaced bar series. Missing
   bars can shorten the wall-clock purge even though the row purge is correct.
   This needs data validation and walk-forward purge work in P1.
2. Calibration schema v2 is intentionally incompatible with schema v1; any
   external schema-1 artifact must be regenerated.
3. Calibration on small validation partitions (<30 samples), or with a class
   absent from validation, now fails training explicitly rather than silently
   degrading. Real 1d data currently has too few rows to train at all.
4. Calibration is per-class followed by row renormalisation; this preserves a
   valid probability vector but is not a joint multiclass calibration method.
5. The repository is not a git repository. The only rollback point is the ZIP
   archive; all changes are uncommitted filesystem edits.
6. `models/_test*` artifacts remain on disk and their timestamps/content
   changed during earlier test runs. They are not production models and were
   not deleted.
7. `pyproject.toml` still declares `requires-python = ">=3.12"` while the
   validated environment is 3.13.15; the code is 3.12-compatible, but only
   3.13 was exercised here.

## 8. Phase 2 recommendation

Proceed with P1 only after explicit authorisation, in this order:

1. Implement the documented cash/collateral/equity ledger for paper shorts and
   enforce the equity identity in tests (`final_equity == initial_capital +
   sum(net PnL)`), including a final forced exit.
2. Validate `PaperBroker` state transitions and persistence against that
   ledger, preserving paper-only constraints.
3. Add data validation and walk-forward purge checks in time units, then
   integrate risk sizing/stops with the broker ledger.
4. Only after those are green, address decision-engine input handling and
   inference/serving.

No Phase 2 code has been written. Awaiting authorisation.
