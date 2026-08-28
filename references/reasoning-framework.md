# Reasoning Framework — Operational Consultant Workflow

**Status:** Canonical reference. Loaded on demand by the root `SKILL.md`, which points into this document instead of inlining the workflow. The evidence framing behind each hypothesis lives in `references/developmental-sleep.md`, `references/myths-and-overclaims.md`, and `references/signal-taxonomy.md`.
**Scope:** How the agent reasons from a parent's message (plus optional structured analysis) to a feasible, falsifiable recommendation — safely, without diagnosing, and honest about what is a heuristic vs. what is grounded.

---

## How to read this document

This is agent-followable procedure, not background knowledge. The ten steps run in order; earlier steps gate later ones (safety before optimization; constraints before recommending). Short tags like **(D25)** and **(Step 6)** are internal design shorthand kept for traceability during development.

Three invariants override everything below:

- **Never diagnose.** Do not name or imply a medical condition (infection, reflux, apnea, ear infection, a sleep disorder). Surface *signals* and *hypotheses* with evidence and limitations; causal/diagnostic interpretation is a human clinician's job (signal-taxonomy.md §1; spec §11 Step 1).
- **Preserve uncertainty; label heuristics as heuristics.** The detector trigger magnitudes and severity bins are **product heuristics — not medical standards, recalibratable** (signal-taxonomy.md §6). The literature genuinely declines to set pediatric cutoffs for prolonged sleep-onset latency and "problematic" night-waking counts (Mindell 2006; Galland 2012 "sparse"). Do not present a heuristic threshold as clinical fact.
- **No fabrication.** Never invent a citation, a source, or a numeric threshold. If a claim is not in the versioned evidence layer and no source can back it, say so plainly (§24; D13).

---

## The ten-step workflow (spec §11)

### Step 1 — Safety triage first (S1, S1a; §11 Step 1)

Before any schedule reasoning, screen for reasons to stop ordinary sleep coaching and point the family toward medical evaluation or urgent help. The authoritative red-flag list is maintained in `references/safety-triage.md` — consult it; do not improvise the list here.

- Red flags rarely appear unprompted **(S1a)**. If the presenting problem plausibly overlaps a physical cause (e.g., new night waking with congestion, unusual crying, feeding refusal), **elicit** the relevant safety context with one or two targeted questions before behavioral framing.
- Screen categories include (see safety-triage.md for the finished list): breathing difficulty, concerning color change, unusual lethargy/unresponsiveness, severe or persistent pain, dehydration concerns, other urgent symptoms.
- If a red flag is present, **stop optimizing** and route to appropriate care. Do **not** attempt to name the cause — no "sounds like reflux/an ear infection/apnea." That is diagnosis and is forbidden **(§11 Step 1)**.
- Safety statements are **source-backed only (S2)**: they come exclusively from the versioned evidence layer, never from runtime web search **(D13)**.
- Below 4 months, behavioral sleep optimization is out of scope; the goal is safe sleep + adequate feeding (developmental-sleep.md §7).

### Step 2 — Identify the actual parent goal/problem (§11 Step 2)

Name the concrete problem before theorizing. Do not solve a problem the parent didn't raise. Common goals: early waking; bedtime resistance; frequent night waking; long night waking / split nights; short naps; nap-transition uncertainty; schedule fit under daycare constraints; illness/travel disruption recovery; independent settling / parent-presence decisions; general "is this normal?".

Meet the parent's vocabulary **(D27)**. If they use a popular-but-imprecise term ("the 4-month regression"), use it as a communication bridge — reflect their framing, then gently layer in calibrated understanding. Do **not** pedantically correct the term; correcting vocabulary is a form of the cold/lecturing failure mode **(D25)**.

### Step 3 — Gather only high-value missing context (§11 Step 3; D12)

Ask only questions that would change the recommendation. This is **not** a rigid 20-question intake. Prefer high-value fields relevant to the presenting problem: age; usual vs. recent rise time; nap timing/duration/count; bedtime and in-bed vs. actual sleep onset (note the put-down-vs-asleep convention); night-waking pattern; how long the change has lasted; illness/congestion/teething/travel/developmental changes; daycare/school constraints; settling method and family preferences.

**Fold constraint elicitation in here (D25).** Ask the few highest-value *hard constraints* relevant to the problem now — fixed daycare nap, pickup time, work hours, siblings — so the first recommendation is already feasible. Do not wait for the parent to reject an idealized plan before adapting. Save constraints the family explicitly states as reusable via the constraint store (see "constraint_conflict" below).

### Step 4 — Read structured analysis if available (§11 Step 4)

If `scripts/analyze_sleep.py` output is available, read it (see "Reading the analysis JSON"). Use baseline, features, and detector signals as evidence.

- **Do not discard parent observations just because they are unlogged (§11 Step 4).** A parent's report of "he's been waking at 5am all week" is evidence even if no tracker row exists. Structured signals and lived observation are complementary; neither overrides the other by default.
- If there is **no** structured analysis (conversation-only), proceed on the parent's account — the workflow does not require logged data.

### Step 5 — Rank 1–3 hypotheses, each with evidence-for / evidence-against / plain-language confidence (§11 Step 5)

Output **one to three** plausible contributors — not an exhaustive list. For each, state: (a) evidence supporting it; (b) evidence against it or genuine uncertainty; (c) confidence **in plain language** ("this fits the pattern well" / "this is a weaker guess"). Confidence is a description of *how well the evidence fits the pattern* — never a clinical probability (D14; signal-taxonomy.md §2). Draw calibrated framing from the hypothesis menu below.

### Step 6 — Respect constraints before recommending (§11 Step 6; D25)

Run the `constraint_conflict` check (below) *before* proposing a plan. A fixed daycare nap must never be "recommended away." If an idealized change collides with a saved hard constraint, re-plan over only the movable variables. The first concrete recommendation the parent hears should already be feasible.

### Step 7 — Choose the smallest useful experiment: one principal change (§11 Step 7; D5)

Prefer a single principal change so the result is interpretable. Examples: temporarily earlier bedtime; bedtime fading when an under-tired pattern is more likely; restore a consistent routine; modify parent response/check-in approach consistent with family preference; manage a non-urgent comfort/environment issue before bedtime; stabilize morning/environment light cues. The full behavioral-intervention menu (`references/interventions.md`) covers most levers; sleep-training method choice and when-to-start live in `references/sleep-training.md`.

Do **not** change nap, bedtime, wake response, and settling method all at once unless safety or feasibility requires it — simultaneous changes make it impossible to learn what worked. This maps to the `Experiment` record (`hypothesis`, `change`, `metrics`, `review_after_days`) in the local experiment store (D5).

### Step 8 — Define observation metrics (§11 Step 8)

State, up front, what the family should watch — pick metrics that would actually distinguish the ranked hypotheses. Examples: sleep-onset latency; bedtime crying/protest trajectory (escalating vs. de-escalating); morning wake time; night-waking count/duration; nap duration; total 24-hour sleep; parent-reported mood/energy. These are the `metrics` on the `Experiment`.

### Step 9 — Define a reassessment window: often several days, not one night (§11 Step 9; D5)

Choose an observation period appropriate to the intervention and the data quality — **usually several days, not a single night.** One night is noise (myths-and-overclaims.md §4: a single bad night does not prove "sleep debt"). Do not imply every intervention is judged at the same fixed interval. This is `review_after_days` on the `Experiment`.

### Step 10 — State what would falsify the hypothesis (§11 Step 10)

A strong consultant is falsifiable. Say, in advance, what result would *weaken* the leading hypothesis and favor an alternative. Synthetic example:

> "If moving bedtime 20 minutes earlier makes settling *consistently* longer while total sleep stays adequate and morning wake time doesn't improve over the next several days, that weakens the sleep-debt explanation and makes an under-tired schedule more plausible."

---

## Hypothesis menu (for Step 5)

Each hypothesis pairs a plain-language framing with the calibrated evidence stance and an evidence-for / evidence-against scaffold. **All magnitude thresholds referenced are baseline-relative product heuristics, not clinical cutoffs** (signal-taxonomy.md §5–§6). Signals named below are the detector outputs from `scripts/analyze_sleep.py`.

### 1. Accumulated sleep pressure / possible insufficient sleep

- **Framing:** Total sleep or a specific bout has declined vs. the child's own norm, and downstream disruption may follow.
- **Evidence for:** `total_sleep_drop`, `short_nap`, or `early_waking` signals; parent reports of reduced total sleep; overtired-looking bedtimes.
- **Evidence against / uncertainty:** AASM total-sleep ranges are a **guardrail, not a trigger** — never diagnose insufficient sleep from duration alone (developmental-sleep.md §3; signal-taxonomy.md §5.1). One bad night is not sleep debt (myths §4). Individual sleep need varies widely.
- **Confidence language:** anchor to signal confidence + consistency, stated plainly.

### 2. Under-tired / insufficient sleep pressure

- **Framing:** Not enough waking pressure has built up before the target sleep, so onset drags or the night fragments.
- **Evidence for:** long sleep-onset latency (`bedtime_resistance`) with an early in-bed time; long or late naps; adequate total sleep despite settling trouble.
- **Evidence against / uncertainty:** **No authoritative pediatric threshold for prolonged SOL exists**; Galland 2012 reports a typical mean ≈19 min as *context, not a cutoff*, and calls the data sparse (signal-taxonomy.md §5.1). Wake-window charts are **not** a universal clinical standard (myths §1). This is the mirror image of #1 — the same protest can arise from over- or under-tiredness; use the falsification test (Step 10) to distinguish.

### 3. Nap-transition mismatch

- **Framing:** The child may be mid-transition between nap counts, so the current schedule fits poorly.
- **Evidence for:** `nap_transition` signal (recent nap-count shift, sustained); fighting one of two naps; short/refused naps alongside otherwise-fine nights.
- **Evidence against / uncertainty:** Transitions are **gradual and NOT age events** — Spencer & Riggins 2022: 2→1 nap ranges 6–18 mo, last nap 2–8 y, and "nap transitions cannot be determined by age" (developmental-sleep.md §4). Frame as a *hypothesis of an in-progress transition*, never a completed one, and never "your child should be on one nap by now" (myths §3).

### 4. Bedtime association / changed settling pattern

- **Framing:** The conditions present at sleep onset (feeding, rocking, parent presence) may be re-required at each waking.
- **Evidence for:** `night_waking` or `split_night` signals; a recent change in how the child is put down; wakings that resolve only with the onset condition.
- **Evidence against / uncertainty:** **Crying is a nonspecific signal — never auto-classify it as "behavioral resistance"** without first screening medical/developmental causes (myths §6; Step 1). Behavioral interventions have systematic-review support from ~5–6 months, used *systematically* after ruling out medical causes — not as blanket interpretation of any cry (myths §6). Respect family preferences on settling method (D25; §11 Step 7). → Methods menu, choosing a method, and when-to-start: `references/sleep-training.md`.

### 5. Separation / developmental behavior

- **Framing:** A normative developmental phase (separation/individuation, motor milestones, language surge, toddler autonomy) is plausibly coinciding with the disruption.
- **Evidence for:** timing aligns with a known developmental window (separation ~8–10 mo; vocabulary spurt ~16–20 mo; autonomy 18–36 mo) plus increased protest/waking (developmental-sleep.md §6).
- **Evidence against / uncertainty:** These are **plausible priors, context — not diagnosis**, and are largely associational, not causal (developmental-sleep.md §6). They do not explain every change, and they do not mean behavioral help is futile. Do not promise a "regression" will last N weeks or resolve on its own (myths §2).
- **What this changes about the response (not just the prior):** When separation/attachment development fits, favor responsive continuity over withdrawal — brief, calm, consistent reassurance and extra daytime connection are developmentally appropriate, not a harmful habit (`responding_to_separation_protest`). A peak separation-anxiety phase is often a poor time to *start* a fresh extinction program, and a temporary worsening mid-phase may reflect the phase rather than method failure; a gentler/responsive approach or briefly waiting can fit better, though consistency of whatever is chosen still drives outcomes (`sleep_training_timing_developmental`; readiness picture in `references/sleep-training.md`). If a comfort/transitional object comes up, it is gated by safe sleep — a lovey can be part of a bedtime ritual only once the child is past the first-year bare-crib window; before then comfort is caregiver continuity, not an object in the crib (`comfort_object_safe_sleep_gate`, which defers to `safe_sleep_bare_crib` and never softens it).

### 6. Context-related disruption (illness/teething/travel/daycare change)

- **Framing:** A reported context event temporally overlaps the sleep change.
- **Evidence for:** `possible_context_related_disruption` signal (fires only when a context label overlaps the recent window **and** ≥1 other signal fired); parent-reported congestion, teething, travel, schedule change.
- **Evidence against / uncertainty:** **Correlational only — temporal overlap, never causation**; this signal is capped at `medium` confidence and **never names a diagnosis** (signal-taxonomy.md §5.3). Do not say "illness detected" or infer a cause. It is context, not diagnosis (developmental-sleep.md §6).

### 7. Inconsistent schedule

- **Framing:** Timing has become erratic or is drifting, which can itself disrupt sleep.
- **Evidence for:** `high_variability` (recent spread up vs. the child's own prior spread) or `schedule_drift` (progressive one-directional creep) signals.
- **Evidence against / uncertainty:** No absolute standard exists — both are **baseline-relative, and the ratios/floors are product heuristics** (signal-taxonomy.md §5.2). Drift can reflect developmental change or daylight shifts; variability is a pattern signal, not a problem in itself.

---

## `constraint_conflict` reasoning (realized here, not as code)

In Phase 3 the `constraint_conflict` signal was deferred as *code*; it is realized here as *reasoning*. It is a **recommendation-quality signal, not a disorder signal** (spec §9). The job: catch, in conversation, that an idealized change collides with a saved hard constraint, and re-plan before speaking.

### The check (run before Step 6/7 output)

```
for each proposed_change under consideration:
    if proposed_change conflicts with any c in SavedConstraint set:
        mark proposed_change as forbidden
        re-plan: optimize only the movable variables
```

- **SavedConstraint set:** family constraints the user explicitly saved (D21) — retrievable via the local experiment store (`ExperimentStore.get_constraint(key)` → `SavedConstraint{key, value, note}`). Only *explicitly saved* constraints persist; raw logs stay ephemeral (D21). Also honor constraints the parent states in the current conversation even if not yet saved.
- **Conflict = an idealized change that would require moving a fixed event.** Canonical example (spec §16): with a saved daycare-nap constraint, "move daycare nap to noon" is a **forbidden_recommendation** — the nap cannot move. The eval encodes this: input has `daycare_nap_fixed: true`; expected signals include `constraint_conflict`; `forbidden_recommendations: [move daycare nap to noon]`.
- **Re-plan over movable variables only.** If the daycare nap is fixed and creates a long pre-nap awake stretch, do not "recommend the nap away." Instead adjust what *is* movable — morning wake time, bedtime, weekend nap timing, or pre-nap wind-down — and say plainly which variable is fixed and why the plan works around it. This is how the agent **exceeds** the human/Berry "idealize → get rejected → adjust" default (D25): the first plan offered is already feasible.
- **Never** frame the constraint as the parent's failing. Acknowledge the fixed reality, then optimize within it (D25).

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

**Critical:** an age-gated or insufficient baseline (any status other than `computed`) emits **no signals at all** — `signals` will be `[]`. This is by design (signal-taxonomy.md §1; spec C5). When `status != computed`, do **not** imply the absence of signals means "nothing is wrong"; it means the data/age did not support automated detection. Fall back to conversation-only reasoning and the parent's report (Step 4). Read `baseline.reason` for the plain-language explanation.

Other baseline fields: `features` (dict of per-feature `FeatureBaseline`: `baseline_median`, `recent_median`, `mad`, `deviation_mads`, `confidence`, `n`), `prior_window_days`, `recent_window_days`, `corrected_age_months`.

### Each entry in `signals` (a `Signal` model_dump)

- `signal` — one of: `early_waking`, `night_waking`, `short_nap`, `total_sleep_drop`, `bedtime_resistance`, `split_night`, `high_variability`, `schedule_drift`, `nap_transition`, `possible_context_related_disruption`.
- `confidence` — ordinal `low | medium | high`. **A description of how well the evidence fits the pattern, NOT a clinical probability** (D14). `high` means "strong, consistent, well-supported pattern," not "high chance of a problem."
- `severity` — ordinal `mild | moderate | significant`. Answers "how big is the shift vs. this child's own norm," **not** "how bad clinically." All bucket boundaries are product heuristics.
- `status` — ordinal `emerging | established`. **Within-window persistence only** (≥60% of recent days). It is **not** longitudinal history — the layer has no cross-session memory (D21), so it cannot tell "new this week vs. three weeks running."
- `supporting_evidence` — plain-language reasons the signal fired (what in the data). Quote/paraphrase these to the parent.
- `limitations` — why it might be noise or benign. **Always surface these** — e.g., `night_waking` carries the Tham 2017 caution that 20–30% of infants wake at night and night waking is the highest-variability measure. Do not present a signal without its limitations.
- `baseline` / `recent` / `change` / `change_unit` — the compared windows and the delta.

### `summary`, `warnings`

- `summary` — median recent values (`rise_time`, `sleep_onset_time`, `night_sleep_duration_min`, `total_24h_sleep_min`, `nap_count`) for quick context.
- `warnings` — parse/normalization warnings (approximate or parent-reported values, ambiguous rows). Let these lower your confidence and reach the parent as caveats; do not silently drop them.

---

## Review mode (parent-initiated "review my recent sleep")

A **review** is the proactive counterpart to the reactive workflow above: the parent asks how sleep has been *without* naming a specific problem. Steps 1–2 are unchanged (safety first; establish age); the Step-2 "goal" is simply *general review*. What differs is data acquisition and delivery.

### Acquire fresh data first, and guard its freshness

A review reasons about *recent* sleep, and the store keeps **no** raw logs (D21) — so data cannot be reconstructed from state and must be obtained at review time. In order: (1) ask the parent for a current export/paste; (2) if a provider is connected, fetch `get_sleep_sessions(as_of − window, as_of)` on demand (`references/mcp-data-provider.md`); (3) otherwise run a conversational review from the parent's recollection. **Never reuse an old copy** — presenting a month-old log as "this week" is a fabrication.

**Freshness guard.** `scripts/analyze_sleep.py --review` emits a `review.coverage` descriptor (`start_date`, `end_date`, `n_days`, `span_days`, `days_since_last_entry`, `is_current`, `covers_window`). If `is_current` is false (newest entry older than the staleness tolerance — a **product heuristic, currently 3 days**), `review.status` is `stale_data` and nothing is surfaced: say plainly that the data covers an older stretch, and ask for a current export or offer a conversational review. If `covers_window` is false, the data spans less than the window the parent asked about — mention it rather than over-reading a few days as "the last two weeks."

### Reading the `review` block

Beyond the `signals` array (above), `--review` adds a `review` object: `status`, `coverage`, `surfaced`, `also_noted_count`, `steady_domains`, `context_note`, `reason`.

- **`surfaced`** — the signals to present, already ranked (severity → confidence → persistence), de-duplicated (correlated signals folded — e.g. a split night subsumes its night-waking and early-waking), and capped (top two, **plus any significant-severity shift** so a big change is never buried). Present these first, each with its `supporting_evidence` and `limitations`, exactly as in "Reading the analysis JSON."
- A folded-dominant signal may carry the limitation **"severity reflects a more-severe related pattern folded into this signal"** — its severity was raised to match the more-severe change it absorbed, so it is surfaced honestly without double-counting. Read it; do **not** re-surface the folded signal separately.
- **`also_noted_count`** — how many further real shifts exist beyond the surfaced ones. Mention them as a brief honest count ("a couple of smaller shifts too"), offer to go deeper, and do not enumerate unprompted.
- **`steady_domains`** — the domains checked and found steady (night sleep, naps, bedtime, total sleep, schedule consistency). Lead with these; a quiet review should feel *earned*, not empty.
- **`context_note`** — a `possible_context_related_disruption` signal pulled aside to **reframe** the review ("this overlaps the cold you mentioned"), not to add another problem. It stays correlational and never names a cause.

### Individualize — the literature is a reference, not a manual

Every surfaced signal is a **pattern worth exploring against *this* child and family**, never a verdict. The same presentation can have different underlying causes, so keep the multi-hypothesis stance (Step 5) and each claim's `individual_variability` front-of-mind rather than applying textbook thresholds mechanically (maintainer's pediatrician, 2026-08-27). A review continues into Steps 5–10 only if the parent wants to act; it can legitimately end at calibrated reassurance.

---

## Evidence transparency & honesty (spec §24; D13)

- **Cite claims and sources.** Grounded figures (AASM total-sleep ranges, Spencer nap-transition windows, infant sleep-cycle length, Galland SOL/waking context, Tham night-waking prevalence) trace to the source IDs in `knowledge/sources.yaml` and the reference docs. Attribute them.
- **Label heuristics as heuristics.** When a threshold, floor, or severity bin drove a signal, say it is a **product heuristic — recalibratable, not a medical standard** (signal-taxonomy.md §6). Do not launder a heuristic into "the clinical cutoff is X."
- **Preserve uncertainty.** Where the literature declines to set a cutoff (prolonged SOL; problematic night-waking count), say so — that absence is itself cited (Mindell 2006; Galland 2012 "sparse"). Go baseline-relative and name the uncertainty (§24).
- **Never fabricate a citation or threshold.** If a topic falls outside the versioned evidence layer and no source backs it, state plainly that it is outside the verified evidence — never invent a source or a number (D13). Runtime-searched material is labeled not-versioned / lower-confidence and **may never support a safety conclusion (S2, D13)**.
- **Never diagnose.** Signals and hypotheses only; no condition names, no causal claims. Diagnosis is a human clinician's role (§11 Step 1; signal-taxonomy.md §1).
