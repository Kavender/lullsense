# Proactive detector evals

Deterministic, end-to-end coverage for every detector in the signal taxonomy
(`skills/lullsense/references/signal-taxonomy.md`). Two complementary tracks:

- **CLI cases** (`cases/*.yaml` + `fixtures/*.json`, run by `run_proactive_eval.py`):
  drive the real `scripts/analyze_sleep.py` subprocess on a synthetic log and assert
  the emitted `signals`. Fixtures use the generic-JSON shape (`start` / `end` /
  `location` only), so they can only express detectors derivable from raw session
  timing.
- **Pipeline cases** (`tests/evals/test_detector_coverage_e2e.py`, run by pytest):
  exercise the full engine in-process (`build_feature_series` → `build_baseline` →
  `run_detectors`). This track can set sleep-onset latency and context events, so it
  covers the detectors the CLI fixtures can't, and gives every detector a positive
  case plus a stable/insufficient/age-gated control.

## Coverage matrix

| Detector | CLI case | Pipeline case | Notes |
|---|---|---|---|
| `early_waking` | ✅ `early_waking_shift` | ✅ | |
| `night_waking` | — | ✅ | count comes from `night_wakings`; cleaner in-process |
| `short_nap` | ✅ `short_nap_drop` | ✅ | |
| `total_sleep_drop` | ✅ `total_sleep_drop` | ✅ | |
| `bedtime_resistance` | — | ✅ | needs sleep-onset latency — not in generic-JSON |
| `split_night` | ✅ `split_night_pattern` | ✅ | |
| `high_variability` | ✅ `high_variability` | ✅ | |
| `schedule_drift` | ✅ `schedule_drift` | ✅ | |
| `nap_transition` | ✅ `nap_transition` | ✅ | |
| `possible_context_related_disruption` | — | ✅ | needs context events — not in generic-JSON |

**Controls (pipeline):** stable child → no signals; fewer than the minimum days →
`insufficient_data`; below the 4-month floor → `below_supported_range`; a reported
context with no coincident deviation → no context signal. **CLI control:**
`stable_control` (no signals).

## Running

```bash
python evals/proactive/run_proactive_eval.py     # CLI cases
python evals/proactive/run_review_eval.py         # longitudinal review cases
pytest tests/evals/test_detector_coverage_e2e.py  # pipeline cases
```

All fixtures are synthetic.
