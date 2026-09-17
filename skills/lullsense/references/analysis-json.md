# Reading the Analysis JSON (`scripts/analyze_sleep.py`)

**Loaded on demand** from `SKILL.md` Step 5 (data-enhanced mode) when the analysis CLI has been run.
Terminating leaf — `signal-taxonomy.md §N` tags are attribution for the confidence/severity/status semantics, not load-now instructions.

---

## Reading the analysis JSON (`scripts/analyze_sleep.py`)

The script emits one JSON object. Top-level keys: `child`, `days`, `baseline`, `signals`, `warnings`, `summary`.

### `baseline.status` — gate on this FIRST

`baseline.status` is one of (`BaselineStatus`):

| Status | Meaning | What signals to expect |
|---|---|---|
| `computed` | A usable per-child baseline was built | Detectors may fire |
| `insufficient_data` | Not enough history to establish a baseline | **No signals emitted** |
| `below_supported_range` | Child is below the supported age range | **No signals emitted** |
| `age_unknown` | Age missing/unusable | **No signals emitted** |

**Critical:** an age-gated or insufficient baseline (any status other than `computed`) emits **no signals at all** — `signals` will be `[]`. This is by design (signal-taxonomy.md §1). When `status != computed`, do **not** imply the absence of signals means "nothing is wrong"; it means the data/age did not support automated detection. Fall back to conversation-only reasoning and the parent's report (Step 4). Read `baseline.reason` for the plain-language explanation.

Other baseline fields: `features` (dict of per-feature `FeatureBaseline`: `baseline_median`, `recent_median`, `mad`, `deviation_mads`, `confidence`, `n`), `prior_window_days`, `recent_window_days`, `corrected_age_months`.

### Each entry in `signals` (a `Signal` model_dump)

- `signal` — one of: `early_waking`, `night_waking`, `short_nap`, `total_sleep_drop`, `bedtime_resistance`, `split_night`, `high_variability`, `schedule_drift`, `nap_transition`, `possible_context_related_disruption`.
- `confidence` — ordinal `low | medium | high`. **A description of how well the evidence fits the pattern, NOT a clinical probability.** `high` means "strong, consistent, well-supported pattern," not "high chance of a problem."
- `severity` — ordinal `mild | moderate | significant`. Answers "how big is the shift vs. this child's own norm," **not** "how bad clinically." All bucket boundaries are product heuristics.
- `status` — ordinal `emerging | established`. **Within-window persistence only** (≥60% of recent days). It is **not** longitudinal history — the layer has no cross-session memory, so it cannot tell "new this week vs. three weeks running."
- `supporting_evidence` — plain-language reasons the signal fired (what in the data). Quote/paraphrase these to the parent.
- `limitations` — why it might be noise or benign. **Always surface these** — e.g., `night_waking` carries the Tham 2017 caution that 20–30% of infants wake at night and night waking is the highest-variability measure. Do not present a signal without its limitations.
- `baseline` / `recent` / `change` / `change_unit` — the compared windows and the delta.

### `summary`, `warnings`

- `summary` — median recent values (`rise_time`, `sleep_onset_time`, `night_sleep_duration_min`, `total_24h_sleep_min`, `nap_count`) for quick context.
- `warnings` — parse/normalization warnings (approximate or parent-reported values, ambiguous rows). Let these lower your confidence and reach the parent as caveats; do not silently drop them.
