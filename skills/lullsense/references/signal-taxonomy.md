# Signal Taxonomy — Detector Semantics & Grounding Reference

**Status:** Canonical Phase 3 reference for `baby_sleep/detect/`. Do not edit a threshold here without updating the corresponding constant in `baby_sleep/detect/grading.py`, `deviation.py`, or `trend.py` in the same commit.
**Last updated:** 2026-08-25
**Scope:** Behavior of the 10 signal detectors that consume Phase 2's `FeatureSeries` + `Baseline` and emit the structured detector contract (spec §10).

---

## How to read this document

The detectors described here are **pattern-change flags computed relative to a single child's own established baseline** — not diagnoses, not schedule prescriptions, and not measurements against a population "should." Where a genuine population-level anchor exists in the peer-reviewed literature (AASM total-sleep ranges, Spencer nap-transition ranges, infant sleep-cycle length), it is used only as a **guardrail or context band**, never as a per-child trigger. Where the literature explicitly *declines* to set a pediatric cutoff (prolonged sleep-onset latency; a "problematic" night-waking count), the detector is **baseline-relative by design** and its trigger magnitude is labeled a **product heuristic — not a medical standard, recalibratable**.

Source references use the IDs defined in `knowledge/sources.yaml`. Page references (`p.X`) are given for the primary PDFs. Every quantitative value in this document is tagged in the Heuristic Threshold Table (§6) and the Provenance Table (§7) as either **grounded** (cited to a verified source) or **heuristic** (a product knob).

---

## 1. Purpose & principles

The detector layer exists to surface *inspectable, evidence-carrying observations about how a child's sleep is changing*, so a downstream consultant layer can respond helpfully. Four principles govern every detector:

- **Your child is the baseline.** Detectors fire on deviation from *this child's* own recent-history median, computed by Phase 2 (`Baseline`). Population norms are used as guardrails and reassurance context, never as the trigger. This mirrors the epistemic stance of `references/developmental-sleep.md §5`.
- **Norms are guardrails, not per-child triggers.** The only population anchors used are the ones with real published grounding (AASM duration ranges, Spencer nap-transition windows, infant sleep-cycle length). They contextualize a change; they do not by themselves generate a signal.
- **Never diagnose.** No detector names or implies a medical condition (infection, reflux, apnea, a sleep disorder). Output is a *signal* — a labeled pattern change with supporting evidence and explicit limitations (spec §10). Causal or diagnostic interpretation is out of scope for this layer and is the job of a human, not the code.
- **Inspectable and honest about uncertainty.** Every `Signal` carries `supporting_evidence` (what in the data caused it) and `limitations` (why it might be noise or benign). Confidence is ordinal, not a fabricated probability.

An age gate (spec C5) sits above all detectors: the runner returns `[]` unless `Baseline.status == COMPUTED`. Below the supported age range, with unknown age, or with insufficient data, **no signals are emitted at all**.

---

## 2. Confidence semantics (ordinal, D14)

Confidence is an **ordinal label — `low | medium | high`** (reusing `analyze.models.Confidence`). Per decision D14, the numeric confidence shown in the spec §10 example (e.g. `0.87`) is explicitly deferred; calibrated numeric confidence requires evaluation data that does not yet exist.

**These are NOT clinical probabilities.** A `high` confidence means "the data pattern is strong, consistent, and well-supported," not "there is an 87% chance of a clinical problem." It is a description of the *evidence for the pattern*, nothing more.

Confidence is a deterministic function of four factors (`grade_confidence` in `grading.py`):

1. **Magnitude** — how far the recent value has moved from baseline, measured in **MAD units** (robust standard deviations; median absolute deviation). `MADS_TRIGGER = 1.5` is the minimum interesting shift; `MADS_STRONG = 3.0` is a strong shift.
2. **Within-window consistency** — what fraction of the recent window moved in the signal's direction (`consistency()`). A one-off blip scores low; a sustained shift scores high.
3. **Baseline quality** — the `Confidence` Phase 2 attached to the baseline itself (a thin or highly variable baseline caps confidence down).
4. **Approximate-data share** — the fraction of recent days built from approximate or parent-reported values; a high share pulls confidence down.

Roughly: `high` requires a strong (or stable-baseline) magnitude **and** high consistency (≥0.8) **and** a non-low baseline **and** a low approximate share; `medium` requires at least the minimum magnitude and moderate consistency (≥0.5); everything weaker is `low`. Some detectors additionally **cap** confidence (see `possible_context_related_disruption`, capped at `medium`).

---

## 3. Severity semantics (ordinal)

Severity is an **ordinal label — `mild | moderate | significant`** derived purely from the *magnitude* of the change against per-detector buckets (`grade_severity`). It answers "how big is this shift?", not "how bad is it clinically."

**All severity bucket boundaries are product heuristics — not medical standards, recalibratable.** They exist to prioritize and phrase output, not to grade a disorder. A `significant` early-waking shift means the wake time moved a lot versus this child's own norm; it does not mean anything is medically wrong.

---

## 4. Status semantics (emerging vs established)

Status is an **ordinal label — `emerging | established`** derived from **within-window persistence only** (`grade_status`, threshold `STATUS_ESTABLISHED_FRAC = 0.6`). If ≥60% of recent-window days show the change, the signal is `established`; otherwise `emerging`.

Per decision **D21 the detector layer has no cross-session memory.** It cannot know whether a pattern is "new this week vs three weeks running," because it sees only the current data window. `emerging`/`established` is a *within-window* persistence label, not a longitudinal history. Cross-session status (new / ongoing / resolving across weeks) is deferred until persistence beyond D21's ephemeral scope exists.

---

## 5. Per-detector reference

Each detector is a pure function returning a `Signal | None`. "Feature" names are Phase 2 `DailyFeatures` fields. "Trigger" is the rule that must hold in the signal's direction. Every trigger magnitude below is a **product heuristic** unless a grounded anchor is named; the exact numbers live in §6.

### 5.1 Deviation detectors (6)

| Detector | Meaning (spec §9) | Feature(s) | Trigger rule | Evidence line |
|---|---|---|---|---|
| `early_waking` | Child is waking earlier than their own norm | `rise_time_min` | rise time earlier by ≥1.5 MAD **or** ≥20 min | **No absolute pediatric standard for "too early" exists.** Purely baseline-relative; the 20-min floor and severity bins are product heuristics. |
| `night_waking` | More overnight wakings than the child's norm | `night_waking_count` | count up by ≥1.5 MAD **or** ≥1 waking | **No authoritative threshold for a "problematic" waking count exists.** Mindell 2006 (`mindell_2006_behavioral_treatment_review`, p.1264) states waking criteria "are not consistent across studies"; ICSD criteria are qualitative. Galland 2012 (`galland_2012_normal_sleep_patterns`) gives *typical-value context only* — wakings decline ~1.7/night at 0–2 mo → ~0.8 at 3–6 mo → ~0.7 at 1–2 y — not a cutoff. So this is baseline-relative; the +1 floor is a heuristic. |
| `short_nap` | Daytime sleep dropped below the child's norm | `total_daytime_sleep_min` | daytime sleep down by ≥1.5 MAD **or** ≥20 min | The "under one cycle" intuition rests on a **soft physiological anchor**: infant sleep-cycle length ≈50–60 min (lengthening toward ~90 min in adults), per Patel 2024 (`patel_2024_physiology_sleep_stages`: "The total NREM and REM sleep cycle is typically 50 minutes instead of the adult 90-minute cycle"; adult cycle "roughly 90 to 110 minutes"). Cycle length is highly variable — treat it as a heuristic anchor, **not a hard constant**. The 20-min floor and bins are product heuristics. **Intended limitation:** `short_nap` measures *shorter* naps; total nap *elimination* (recent `total_daytime_sleep_min` becomes None) is out of its scope and is surfaced instead by `nap_transition` / `total_sleep_drop`. (Note: Galland 2012 supplies SOL means and waking counts, **not** the cycle-length figure.) |
| `total_sleep_drop` | 24h total sleep fell below the child's norm | `total_24h_sleep_min` | 24h sleep down by ≥1.5 MAD **or** ≥30 min | AASM total-sleep ranges are a **GUARDRAIL, not a trigger** (`aasm_child_sleep_duration_2016`, p.785: 4–12 mo 12–16 h; 1–2 y 11–14 h; 3–5 y 10–13 h). This detector flags a **baseline-relative decline only**; it **must not diagnose from duration alone** (developmental-sleep.md §3). AASM ranges provide reassurance/out-of-range context, not the fire condition. |
| `bedtime_resistance` | Falling asleep is taking longer than the child's norm | `sleep_onset_latency_min` (SOL) | SOL up by ≥1.5 MAD **or** ≥10 min | **No authoritative pediatric threshold for prolonged SOL exists.** Galland 2012 (`galland_2012_normal_sleep_patterns`) reports SOL data are *sparse* and gives a typical **mean ≈19 min** in infants as context, **not a cutoff**; ICSD criteria are qualitative. Baseline-relative; the 10-min floor and bins are product heuristics. |
| `split_night` | A single long mid-night waking (fragmented night) | `longest_night_waking_min` | longest waking up by ≥1.5 MAD **or** ≥30 min | **No authoritative threshold for a "notable" WASO / longest-waking exists** (same Mindell 2006 / ICSD caveat as `night_waking`). Baseline-relative; the 30-min floor and bins are product heuristics. |

**`night_waking` limitation (required in output).** The detector's `limitations` must carry the Tham 2017 caution: 20–30% of infants wake at night through the first two years, and night waking shows "the highest levels of variability across all sleep measures" (`tham_2017_infant_sleep_cognition_growth`, p.135). A rise in wakings is a change vs *this child's own* norm, not evidence of a problem.

### 5.2 Trend / structural detectors (3)

| Detector | Meaning (spec §9) | Feature(s) | Trigger rule | Evidence line |
|---|---|---|---|---|
| `high_variability` | Timing has become erratic vs a previously steadier pattern | `sleep_onset_time`, `rise_time` (MAD of clock minutes) | recent MAD ≥1.75× prior MAD **and** ≥25 min; or ≥40 min if the prior window was essentially stable | **No absolute standard exists.** Purely baseline-relative (this child's recent spread vs their own prior spread); ratio and floors are product heuristics. Variability is a pattern signal, not a problem in itself. |
| `schedule_drift` | Bedtime/wake is creeping progressively in one direction | `sleep_onset_time`, `rise_time` | net first→last shift ≥45 min across the recent window **and** ≥70% of day-to-day steps in the same direction | **No absolute standard exists.** Baseline-relative and directional; magnitude/monotonicity are product heuristics. Drift can reflect developmental change or daylight — context, not a problem by itself. |
| `nap_transition` | The child may be dropping a nap | `nap_count` | median recent nap_count differs from baseline by ≥1, on ≥60% of recent days | Framed by Spencer 2022 (`spencer_2022_nap_transitions_pnas`, p.1: 2→1 nap 6–18 mo; last nap 2–8 y) as a **multi-month hypothesis, NOT an age event** — "nap transitions cannot be determined by age" (p.7). Output is a *hypothesis of an in-progress transition*, never a completed one. The Δ≥1 / 60% rule is a product heuristic. |

### 5.3 Context detector (1)

| Detector | Meaning (spec §9) | Reads | Trigger rule | Evidence line |
|---|---|---|---|---|
| `possible_context_related_disruption` | A logged/reported context (teething, travel, illness, daycare, medication) **temporally overlaps** other sleep changes | `events`, `reported_context`, plus the other detectors' output | fires only when (a) a context label/event overlaps the recent window **and** (b) ≥1 other signal fired | **Correlational only — temporal overlap, never causation.** Confidence is **capped at `medium`**. It **never names a diagnosis**; its `limitations` state explicitly that causality is not established and this is not a medical diagnosis. This mirrors developmental-sleep.md §6: contextual contributors are "context, not diagnosis." |

---

## 6. Heuristic threshold table

Every value below is a **product heuristic — not a medical standard, recalibratable** against real cohort data. They are the exact constants the code uses (Tasks 4–7 of the Phase 3 plan). MAD-unit triggers (`MADS_TRIGGER`, `MADS_STRONG`) and severity bins apply on top of the per-detector absolute floors.

| Constant / rule | Value | Where | Nature |
|---|---|---|---|
| `MADS_TRIGGER` | 1.5 | `grading.py` | product heuristic |
| `MADS_STRONG` | 3.0 | `grading.py` | product heuristic |
| `STATUS_ESTABLISHED_FRAC` | 0.60 | `grading.py` | product heuristic |
| Confidence `high` consistency gate | ≥0.80 | `grading.py` | product heuristic |
| Confidence `medium` consistency gate | ≥0.50 | `grading.py` | product heuristic |
| Confidence approximate-share cap | ≤0.34 | `grading.py` | product heuristic |
| `early_waking` abs floor | rise earlier ≥20 min | `deviation.py` | product heuristic |
| `early_waking` severity bins (mild_hi / moderate_hi) | 40 / 60 min | `deviation.py` | product heuristic |
| `night_waking` abs floor | count +≥1 waking | `deviation.py` | product heuristic |
| `night_waking` severity bins | 1 / 2 wakings | `deviation.py` | product heuristic |
| `short_nap` abs floor | daytime ↓≥20 min | `deviation.py` | product heuristic |
| `short_nap` severity bins | 40 / 60 min | `deviation.py` | product heuristic |
| `total_sleep_drop` abs floor | 24h ↓≥30 min | `deviation.py` | product heuristic |
| `total_sleep_drop` severity bins | 60 / 90 min | `deviation.py` | product heuristic |
| `bedtime_resistance` abs floor | SOL ↑≥10 min | `deviation.py` | product heuristic |
| `bedtime_resistance` severity bins | 20 / 35 min | `deviation.py` | product heuristic |
| `split_night` abs floor | longest waking ↑≥30 min | `deviation.py` | product heuristic |
| `split_night` severity bins | 60 / 90 min | `deviation.py` | product heuristic |
| `high_variability` MAD ratio trigger | recent MAD ≥1.75× prior MAD | `trend.py` | product heuristic |
| `high_variability` abs floor | recent MAD ≥25 min | `trend.py` | product heuristic |
| `high_variability` stable-prior floor | recent MAD ≥40 min (if prior stable) | `trend.py` | product heuristic |
| `high_variability` severity (significant / moderate) | ratio >4 or recent MAD ≥90 / ratio >2.5 or recent MAD ≥50 | `trend.py` | product heuristic |
| `schedule_drift` net shift | ≥45 min across recent window | `trend.py` | product heuristic |
| `schedule_drift` monotonicity | ≥70% of steps same direction | `trend.py` | product heuristic |
| `schedule_drift` severity bins (mild_hi / moderate_hi) | 75 / 120 min | `trend.py` | product heuristic |
| `nap_transition` count delta | median nap_count Δ≥1 | `trend.py` | product heuristic |
| `nap_transition` consistency | on ≥60% of recent days | `trend.py` | product heuristic |
| `possible_context_related_disruption` confidence cap | `medium` | `context.py` | product heuristic |

**Grounded context bands (NOT triggers, listed for transparency).** These are cited values used only as guardrails/reassurance context, never as fire conditions:

| Anchor | Value | Source | Nature |
|---|---|---|---|
| AASM total-sleep ranges | 4–12 mo 12–16 h; 1–2 y 11–14 h; 3–5 y 10–13 h | `aasm_child_sleep_duration_2016`, p.785 | grounded (guardrail) |
| Spencer nap-transition windows | 2→1 nap 6–18 mo; last nap 2–8 y | `spencer_2022_nap_transitions_pnas`, p.1 | grounded (context) |
| Infant sleep-cycle length | ≈50–60 min infancy → ~90 min adult | `patel_2024_physiology_sleep_stages` (~50 min infant, ~90 min adult) | grounded, soft anchor |
| Typical infant SOL | mean ≈19 min (sparse data) | `galland_2012_normal_sleep_patterns` | grounded (typical-value context) |
| Typical night wakings | ~1.7/night 0–2 mo → ~0.7/night 1–2 y | `galland_2012_normal_sleep_patterns` | grounded (typical-value context) |
| Night-waking prevalence/variability | 20–30% of infants; highest-variability measure | `tham_2017_infant_sleep_cognition_growth`, p.135 | grounded (limitation) |

---

## 7. Provenance table

| Anchor / claim used by a detector | Source ID | Grounded / Heuristic |
|---|---|---|
| AASM total-sleep ranges (guardrail for `total_sleep_drop`) | `aasm_child_sleep_duration_2016` (p.785) | grounded |
| "must not diagnose from duration alone" caveat | `aasm_child_sleep_duration_2016` (p.786) / developmental-sleep.md §3 | grounded |
| Nap-transition windows + "not an age event" (`nap_transition`) | `spencer_2022_nap_transitions_pnas` (p.1, p.7) | grounded |
| Infant sleep-cycle length ≈50 min → ~90 min adult (soft anchor for `short_nap`) | `patel_2024_physiology_sleep_stages` | grounded (soft) |
| Typical SOL mean ≈19 min; data sparse (context for `bedtime_resistance`) | `galland_2012_normal_sleep_patterns` | grounded (context) |
| Typical night-waking counts ~0.7–1.7/night (context for `night_waking`) | `galland_2012_normal_sleep_patterns` | grounded (context) |
| Waking criteria "not consistent across studies" (no SOL/waking threshold) | `mindell_2006_behavioral_treatment_review` (p.1264) | grounded |
| Night-waking prevalence 20–30% + highest variability (`night_waking` limitation) | `tham_2017_infant_sleep_cognition_growth` (p.135) | grounded |
| All detector trigger magnitudes, floors, severity bins, MAD units, ratios, fractions, caps | — (no source; product knobs) | heuristic |

---

## 8. Honest limitations of this layer

- **The trigger magnitudes are not validated.** They were chosen to be reasonable, not calibrated. They are marked recalibratable throughout; real cohort data should replace them.
- **No cross-session memory (D21).** The layer cannot see history beyond the current window; `emerging/established` is within-window only.
- **No causality, ever.** `possible_context_related_disruption` reports temporal overlap and is capped at `medium`; nothing here establishes cause.
- **The literature genuinely lacks pediatric cutoffs** for prolonged SOL and problematic night-waking counts. That absence is itself cited (Mindell 2006; Galland 2012 "sparse"). We do not invent one — we go baseline-relative and label the knobs as heuristics.
