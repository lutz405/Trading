# Phase 0/1 final corrective audit

Date: 2026-11-23
Scope: two independent-review findings only. No Phase 2 implementation.

## 1. Label purge boundary

### Mathematical rule

`make_labels` builds the label at dataframe row position `p` from
`close.shift(-horizon)`. That label therefore reads the close at position
`p + horizon`.

Let:

- `t` = dataframe position of the last row in a partition;
- `v` = dataframe position of the first row in the next partition;
- `h` = label horizon.

Strict separation requires:

```text
t + h < v
<=> v - t > h
<=> v - t >= h + 1        (positions are integers)
```

The same rule is applied at both boundaries:

- last train row -> first validation row;
- last validation row -> first test row.

`gap` is the number of X rows skipped between partition starts:
`val_start = train_end + gap`. With contiguous dataframe positions,
`v - t = gap + 1`. Therefore:

- `gap == h` gives `v - t == h + 1`, the minimum safe position distance;
- `gap == h - 1` gives `v - t == h`, so the last train label reads the first
  validation close and is rejected.

For sparse dataframe positions, `v - t` can be smaller than `gap + 1`. The
new check uses actual dataframe positions, so missing feature rows cannot
silently shorten the purge. It fails closed instead of relying on row counts.

### Code change

`src/tradingai/ml/pipeline.py`:

- added `_validate_label_purge(...)`;
- computes `train_label_end_position`, `validation_label_end_position` and
  `test_label_end_position` as `last_row_position + horizon`;
- rejects `train_label_end_position >= validation_start_position`;
- rejects `validation_label_end_position >= test_start_position`;
- verifies every label close is inside the dataframe;
- runs the check **before** model training;
- manifest now records the exact label close for every partition, including
  test;
- purge records `train_label_to_validation` and
  `validation_label_to_test`, which are the distances from the last label
  close to the next partition start (must be at least 1).

Real 1h data after the change:

```text
train:      start_position=20,  end_position=407, label_end_position=412
validation: start_position=413, end_position=544, label_end_position=549
test:       start_position=550, end_position=681, label_end_position=686
purge:      train_to_validation=6, validation_to_test=6,
            train_label_to_validation=1, validation_label_to_test=1
```

The minimum label-close separation is one dataframe row: 412 < 413 and
549 < 550.

## 2. Finite price validation

`src/tradingai/ml/labels.py` now validates with:

```python
if not np.isfinite(close).all() or (close <= 0).any():
    raise ValueError("close must be finite and positive")
```

This rejects `NaN`, `+inf`, `-inf`, zero and negative prices, while keeping the
positive-price requirement. Previously `NaN`, zero and negatives were
rejected, but `+inf` and `-inf` passed validation.

## 3. Files modified

Modified:

- `src/tradingai/ml/pipeline.py`
- `src/tradingai/ml/labels.py`

Added:

- `tests/test_label_purge_contract.py`
- `tests/test_price_validation.py`
- `docs/phase0_phase1_final_audit.md` (this record)

No other module, existing test, data file, model artifact or backup was
modified. Model artifact hashes were re-checked after the suite and match the
pre-audit values.

## 4. New regression tests

| Test | Failure reproduced |
|---|---|
| `test_label_purge_distance_equal_to_horizon_is_rejected` | Old check accepted `v - t == horizon`, so the last train label used the first validation close. New code raises. |
| `test_label_purge_minimum_safe_distance_is_horizon_plus_one` | Pins the minimum safe distance `horizon + 1` and the exact label-close positions. |
| `test_label_purge_uses_actual_sparse_positions` | Reproduces the same leak across missing dataframe rows; a row-count-only check passes, actual-position check rejects. |
| `test_gap_equal_to_horizon_has_strict_label_separation` | End-to-end `gap == horizon` run; asserts `label_end < next_start`, purge label gaps >= 1, and position distance >= horizon + 1. |
| `test_label_close_position_is_used_and_first_validation_close_is_not` | Mutates the documented label close and proves the last train label changes; mutates the first validation close and proves it does not. |
| `test_gap_below_horizon_is_rejected` | Rejects the boundary `gap = horizon - 1`. |
| `test_make_labels_rejects_non_finite_or_non_positive_close` (5 cases) | Rejects `NaN`, `+inf`, `-inf`, `0` and negative prices; `+inf` and `-inf` previously passed. |
| `test_make_labels_accepts_finite_positive_close` | Guards against over-rejection of valid prices. |

## 5. Verification (fresh results)

Targeted new tests:

```text
python -m pytest tests/test_label_purge_contract.py tests/test_price_validation.py -q
12 passed, 1 warning in 3.58s
```

Related existing temporal/pipeline tests plus new tests:

```text
24 passed, 1 warning in 4.09s
```

Full suite:

```text
python -m pytest -q
167 passed, 1 warning in 9.11s
```

Ruff on modified files:

```text
python -m ruff check src/tradingai/ml/pipeline.py src/tradingai/ml/labels.py \
  tests/test_label_purge_contract.py tests/test_price_validation.py
All checks passed!
```

Format check on modified files:

```text
4 files already formatted
```

Mypy:

```text
python -m mypy src --ignore-missing-imports
Success: no issues found in 33 source files
```

Repository-wide Ruff remains at the pre-existing 53 errors (34 fixable),
outside the files touched by this audit.

## 6. Pending problems

- P1 remains intentionally unimplemented: short/collateral/equity accounting,
  final-exit metrics, risk integration, `PaperBroker` validation/persistence,
  general data validation, walk-forward purge integration, decision-engine
  cleanup and inference/serving.
- Sparse dataframe positions at a split boundary now fail closed. Automatically
  advancing the split to restore the purge belongs to the P1 data-validation
  work.
- `run_training` still uses the configured row-count `gap` to choose split
  indices; the new position-level check is the authoritative safety condition.
- Repository-wide Ruff/format debt remains pre-existing and unchanged.
- The 1d dataset still has only 30 rows and cannot produce labeled training
  rows; this is a data-coverage limit.

No Phase 2 code has been written. Awaiting authorization.
