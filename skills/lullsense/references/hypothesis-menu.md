# Hypothesis Menu (for Step 6 — ranking 1–3 contributors)

**Loaded on demand** from `SKILL.md` Step 6 (hypothesis ranking).
**Terminating leaf** — the provenance tags below (e.g. `myths §4`, `signal-taxonomy.md §5`, `developmental-sleep.md §6`, claim ids) cite evidence files for attribution; you do not need to open them to use this menu.

---

## Hypothesis menu (for Step 6)

Each hypothesis pairs a plain-language framing with the calibrated evidence stance and an evidence-for / evidence-against scaffold. **All magnitude thresholds referenced are baseline-relative product heuristics, not clinical cutoffs** (signal-taxonomy.md §5–§6). Signals named below are the detector outputs from `scripts/analyze_sleep.py`.

### 1. Accumulated sleep pressure / possible insufficient sleep

- **Framing:** Total sleep or a specific bout has declined vs. the child's own norm, and downstream disruption may follow.
- **Evidence for:** `total_sleep_drop`, `short_nap`, or `early_waking` signals; parent reports of reduced total sleep; overtired-looking bedtimes.
- **Evidence against / uncertainty:** AASM total-sleep ranges are a **guardrail, not a trigger** — never diagnose insufficient sleep from duration alone (developmental-sleep.md §3; signal-taxonomy.md §5.1). One bad night is not sleep debt (myths §4). Individual sleep need varies widely.
- **Confidence language:** anchor to signal confidence + consistency, stated plainly.

### 2. Under-tired / insufficient sleep pressure

- **Framing:** Not enough waking pressure has built up before the target sleep, so onset drags or the night fragments.
- **Evidence for:** long sleep-onset latency (`bedtime_resistance`) with an early in-bed time; long or late naps; adequate total sleep despite settling trouble.
- **Evidence against / uncertainty:** **No authoritative pediatric threshold for prolonged SOL exists**; Galland 2012 reports a typical mean ≈19 min as *context, not a cutoff*, and calls the data sparse (signal-taxonomy.md §5.1). Wake-window charts are **not** a universal clinical standard (myths §1). This is the mirror image of #1 — the same protest can arise from over- or under-tiredness; use the falsification test (Step 7) to distinguish.

### 3. Nap-transition mismatch

- **Framing:** The child may be mid-transition between nap counts, so the current schedule fits poorly.
- **Evidence for:** `nap_transition` signal (recent nap-count shift, sustained); fighting one of two naps; short/refused naps alongside otherwise-fine nights.
- **Evidence against / uncertainty:** Transitions are **gradual and NOT age events** — Spencer & Riggins 2022: 2→1 nap ranges 6–18 mo, last nap 2–8 y, and "nap transitions cannot be determined by age" (developmental-sleep.md §4). Frame as a *hypothesis of an in-progress transition*, never a completed one, and never "your child should be on one nap by now" (myths §3).

### 4. Bedtime association / changed settling pattern

- **Framing:** The conditions present at sleep onset (feeding, rocking, parent presence) may be re-required at each waking.
- **Evidence for:** `night_waking` or `split_night` signals; a recent change in how the child is put down; wakings that resolve only with the onset condition.
- **Evidence against / uncertainty:** **Crying is a nonspecific signal — never auto-classify it as "behavioral resistance"** without first screening medical/developmental causes (myths §6; Step 1). Behavioral interventions have systematic-review support from ~5–6 months, used *systematically* after ruling out medical causes — not as blanket interpretation of any cry (myths §6). Respect family preferences on settling method. → Methods menu, choosing a method, and when-to-start: `references/sleep-training.md`.

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

### 8. Sleep environment / comfort mismatch

- **Framing:** An environmental factor — in evidence order **light > noise > temperature** — may be interfering with onset or consolidation. This hypothesis is **parent-report-driven** (there is no detector signal for it); surface it *conversationally, 2–3 factors at a time, opt-in* — never as a checklist dump. Full per-factor detail: `references/environment-comfort-factors.md`.
- **Evidence for:** a bright or stimulating pre-bed environment / late light exposure; a very quiet room where onset is hard, or a loud sound machine close to the crib; parent reports of a hot or stuffy room.
- **Evidence against / uncertainty:** the light evidence is **mechanistic and preschool-aged** — melatonin markers, not measured infant sleep outcomes (`env_light_dim_pre_bed`; sources caveated in `knowledge/sources.yaml`). White-noise sleep benefit is **limited and mostly from newborn/hospital settings** — short-term and variable, not established for our age band (`env_noise_efficacy_uncertain`). Temperature is **preference-level with no quality evidence** (`env_temperature_preference`). **Sleep-surface "comfort" is not optimizable — it is safety-governed and defers to `safe_sleep_firm_flat_surface`** (`env_surface_comfort_defers_to_safety`); the "baby doesn't like this bed" report lands here and is **never** a reason to change the surface.
- **What this changes about the response (not just the prior):** light → a **dim wind-down** as the smallest experiment (Step 7) with onset latency as its metric; noise → **safer-use** guidance (low volume, across-room, time-limited — `env_noise_safer_use`), not a blanket endorsement or prohibition; surface → **acknowledge + route to safe sleep** (acknowledge-don't-criticize), never a comfort swap; temperature → gentle, preference-framed. Below **4 months** this hypothesis is out of scope (safe sleep + adequate feeding only), like the rest of the behavioral layer. Individualize: each factor is a hypothesis against *this* child with evidence-for/against, and only **one** principal change is tested at a time (Step 7).
- **Confidence language:** state plainly that this is a *thing to observe and rule out*, not a diagnosed cause; label the evidence strength honestly (mechanistic/preschool for light, weak/preference for noise-efficacy and temperature, documented for noise safer-use).
