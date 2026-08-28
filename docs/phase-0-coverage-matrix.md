# Phase 0 Coverage Matrix + Acceptance Review

**Status:** Phase 0 acceptance artifact.
**Last updated:** 2026-08-24
**Scope:** Confirms Phase 0 (research + evidence map) meets its spec §18 acceptance criteria before Phase 1 begins.

This document maps every controlled parent goal and every high-impact recommendation category to its backing `claim_id`(s) and `source_id`(s), records what remains uncertain or unverified with a confirmation plan, and checks the Phase 0 acceptance criteria. The tables are derived directly from `skills/lullsense/knowledge/claims.yaml` and `skills/lullsense/knowledge/sources.yaml` (45 claims, 23 sources) and can be regenerated from those files.

---

## 1. Summary

- **Claims:** 45 total — 12 `A_safety`, 15 `B_developmental`, 9 `C_behavioral`, 9 `D_practice`.
- **Sources:** 23 total — **13 verified** (all `A_safety` sources + AASM/Spencer/Tham), 10 `verified: false` (non-safety B/C/D journal + consultant material).
- **Parent-goal coverage:** all 10 goals backed by ≥1 claim; validator prints **no COVERAGE GAP**.
- **Validator:** exit 0. The only warnings are 3× on `graduated_extinction_efficacy` (an intentionally `high`-evidence behavioral claim whose systematic-review sources are not yet PDF-verified — the intended honest signal, not an error).

---

## 2. Table 1a — Parent goal → backing claims

The 10 controlled goals (`skills/lullsense/references/evidence-methodology.md §6`). "Evidence spine" names the strongest verified backing; heuristic-only goals are flagged for honesty.

| Parent goal | # claims | Backing `claim_id`s | Evidence spine / note |
|---|---|---|---|
| `early_waking` | 3 | constraint_first_recommending, wake_windows_as_heuristic, early_waking_common_causes | **Heuristic-only** (`D_practice`). Practice-based troubleshooting; no direct evidence source. Acceptable per spec (professional-practice source counts), but thin — see §5. |
| `bedtime_resistance` | 10 | developmental_context_sleep_shifts, sleep_regression_reframe, bedtime_resistance_toddler_autonomy, bedtime_routine_benefits, graduated_extinction_efficacy, medical_ruleout_before_behavioral, bedtime_fading, positive_routines_reinforcement, constraint_first_recommending, wake_windows_as_heuristic | Strong: SR-backed behavioral (`mindell_2006`, `meltzer_mindell_2014`, `reuter_2020`) + `B` developmental context. |
| `night_waking` | 11 | night_waking_normal_variability, sleep_consolidation_trajectory, developmental_context_sleep_shifts, sleep_regression_reframe, bedtime_routine_benefits, graduated_extinction_efficacy, behavioral_interventions_safety, medical_ruleout_before_behavioral, consistent_response_settling, sleep_associations_context, split_night_time_in_bed | Strong: `tham_2017` (verified) for normalization + behavioral SRs. |
| `split_night` | 1 | split_night_time_in_bed | **Thinnest goal — single heuristic, no source.** See §5. |
| `short_naps` | 7 | nap_phase_progression, naps_support_memory, sleep_regression_reframe, constraint_first_recommending, wake_windows_as_heuristic, daycare_schedule_alignment, short_naps_context | `spencer_2022` + `tham_2017` (both verified) for the developmental spine; heuristics for troubleshooting. |
| `nap_transition` | 8 | nap_phase_progression, nap_transition_2to1_timing, nap_transition_last_nap_timing, nap_transition_driven_by_maturation, naps_support_memory, wake_windows_as_heuristic, daycare_schedule_alignment, nap_transition_readiness_signs | Strong: `spencer_2022_nap_transitions_pnas` (verified) throughout. |
| `daycare_schedule_fit` | 3 | constraint_first_recommending, daycare_schedule_alignment, jetlag_gradual_shift | **Heuristic-only** (`D_practice`). By nature a logistics/constraint problem, not an evidence one — see §5. |
| `illness_travel_recovery` | 2 | illness_travel_recovery_approach, jetlag_gradual_shift | **Heuristic-only** (`D_practice`). Safety red flags governed separately by `A_safety` + `safety-triage.md`. |
| `independent_settling` | 12 | bedtime_routine_benefits, graduated_extinction_efficacy, behavioral_interventions_safety, medical_ruleout_before_behavioral, bedtime_fading, consistent_response_settling, independent_settling_readiness, sleep_associations_context, sleep_training_readiness_signals, gentle_settling_approaches, sleep_training_expected_trajectory, sleep_training_method_choice | Strong: behavioral SRs + practice-parameter; method menu and non-judgment framing in `skills/lullsense/references/sleep-training.md`. |
| `is_this_normal` | 14 | total_sleep_4_12_months, total_sleep_1_2_years, total_sleep_2_3_years, night_waking_normal_variability, sleep_consolidation_trajectory, circadian_emergence_infancy, nap_phase_progression, nap_transition_2to1_timing, nap_transition_last_nap_timing, individual_variability_baseline, developmental_context_sleep_shifts, sleep_regression_reframe, bedtime_resistance_toddler_autonomy, short_naps_context | Strongest: `aasm_child_sleep_duration_2016`, `tham_2017`, `spencer_2022` (all verified). |

---

## 3. Table 1b — High-impact recommendation category → backing claims

High-impact categories drawn from spec §11 Step 7 (smallest-useful-experiment options), plus the two highest-value preventable categories (safe sleep, red-flag referral). Acceptance criterion: **each has ≥1 identified evidence or professional-practice source.**

| Recommendation category | Backing `claim_id`s | Backing sources | ≥1 source? |
|---|---|---|---|
| Temporarily earlier bedtime | early_waking_common_causes, split_night_time_in_bed, constraint_first_recommending | `pediatric_sleep_council_sleep_training` + practice | ✅ |
| Bedtime fading (under-tired pattern) | bedtime_fading | `meltzer_mindell_2014_meta_analysis`, `babysleepscience_bedtime_fading_guide` | ✅ |
| Restore consistent routine | bedtime_routine_benefits, consistent_response_settling | `mindell_williamson_2018_bedtime_routine`, `mindell_2006` | ✅ |
| Modify parent response / check-in (family preference) | graduated_extinction_efficacy, consistent_response_settling, independent_settling_readiness, sleep_associations_context | `mindell_2006`, `meltzer_mindell_2014`, `reuter_2020`, `huckleberry_sleep_training_methods` | ✅ |
| Manage non-urgent comfort/environment before bedtime | medical_ruleout_before_behavioral, early_waking_common_causes | `aasm_2006_practice_parameters_bedtime`, `pediatric_sleep_council_sleep_training` | ✅ |
| Stabilize morning/environment cues | early_waking_common_causes, wake_windows_as_heuristic | `pediatric_sleep_council_sleep_training`, `huckleberry_wake_windows_guide` | ✅ |
| Behavioral settling method choice | graduated_extinction_efficacy, bedtime_fading, positive_routines_reinforcement, independent_settling_readiness | behavioral SRs + practice parameter | ✅ |
| Nap-transition guidance | nap_transition_2to1_timing, nap_transition_last_nap_timing, nap_transition_driven_by_maturation, nap_transition_readiness_signs, nap_phase_progression | `spencer_2022_nap_transitions_pnas` (verified) | ✅ |
| Safe-sleep essentials (highest-value preventable) | safe_sleep_back_to_sleep, safe_sleep_firm_flat_surface, safe_sleep_no_bed_sharing, safe_sleep_room_sharing, bed_sharing_harm_reduction, safe_sleep_bare_crib | `aap_safe_sleep_2022` (verified) + AAP HealthyChildren | ✅ |
| Red-flag recognition / referral | fever_under_3mo_urgent, fever_high_or_persistent_contact, fever_with_serious_signs_urgent, infant_dehydration_signs, respiratory_distress_emergency_signs, brue_episode_needs_evaluation | AAP guidelines + HealthyChildren (all verified) | ✅ |
| Sleep-duration context / normalization | total_sleep_4_12_months, total_sleep_1_2_years, total_sleep_2_3_years, individual_variability_baseline | `aasm_child_sleep_duration_2016` (verified) | ✅ |

**All high-impact recommendation categories have ≥1 backing source.** ✅

---

## 4. Table 2a — Unverified sources + confirmation plan

10 sources are `verified: false`. None back an `A_safety` claim (all safety sources are verified). Confirmation = obtain the primary PDF, read it, cross-check the citing claims, then flip `verified: true` with a page-cited `note:` (the reusable PDF-verification loop).

| Source ID | Type | Backs | Confirmation plan |
|---|---|---|---|
| `mindell_2006_behavioral_treatment_review` | systematic_review | graduated_extinction_efficacy, consistent_response_settling, positive_routines_reinforcement, independent_settling_readiness | Obtain PDF (AASM/Sleep 2006); verify extinction/graduated-extinction efficacy + method-consistency findings. **Highest priority** (backs the one `high`-evidence warning). |
| `meltzer_mindell_2014_meta_analysis` | systematic_review | graduated_extinction_efficacy, bedtime_fading | Obtain PDF (J Pediatr Psychol 2014); verify meta-analytic effect + bedtime-fading support. High priority. |
| `reuter_2020_infant_sleep_systematic_review` | systematic_review | graduated_extinction_efficacy, behavioral_interventions_safety | Obtain PDF (Acta Paediatrica 2020); verify efficacy + no-lasting-harm/safety claim. High priority. |
| `aasm_2006_practice_parameters_bedtime` | guideline | medical_ruleout_before_behavioral | Obtain PDF; verify clinical-evaluation-context framing. Medium. |
| `mindell_williamson_2018_bedtime_routine` | review | bedtime_routine_benefits | Obtain PDF (Sleep Med Rev 2018); verify routine-benefit associations. Medium. |
| `aap_healthy_sleep_hours` | review | (none currently — endorses AASM ranges) | Re-access URL; confirm it still endorses AASM bands. Low (duration is already covered by the verified `aasm_child_sleep_duration_2016`). |
| `babysleepscience_bedtime_fading_guide` | consultant_public_material | bedtime_fading | Re-access URL; confirm public content matches the synthesized observation. Low (corroborating only). |
| `huckleberry_sleep_training_methods` | consultant_public_material | consistent_response_settling, sleep_associations_context | Re-access URL; confirm. Low (corroborating). |
| `huckleberry_wake_windows_guide` | consultant_public_material | wake_windows_as_heuristic | Re-access URL; confirm. Low (claim is explicitly heuristic). |
| `pediatric_sleep_council_sleep_training` | consultant_public_material | early_waking_common_causes, independent_settling_readiness | Re-access URL; confirm. Low (corroborating). |

Per `evidence-methodology.md §10`, unverified sources should be verified within 30 days of commit or the claim revisited.

---

## 5. Table 2b — Uncertain / lower-confidence claims + confirmation plan

Two distinct kinds of "not high-confidence" exist here — they must not be conflated:

**(i) Appropriately-calibrated `moderate` claims backed by *verified* sources.** These are not pending verification; their `moderate` level honestly reflects review-level (not guideline-level) evidence. No action needed beyond the normal review cadence.

- All `spencer_2022`- and `tham_2017`-backed `B_developmental` claims (nap transitions, night-waking variability, consolidation, circadian emergence, naps-and-memory, sleep-regression reframe), and `total_sleep_2_3_years` (an honest AASM-band interpolation). Sources verified; level correctly `moderate`.
- *Evidence-type note:* `tham_2017` (narrative review) and `spencer_2022` claims use `evidence_type: primary_research` as the closest enum (the taxonomy lacks a "narrative_review" type); `evidence_level: moderate` carries the real weight. Candidate for a future taxonomy addition.

**(ii) Confidence capped by an unverified source** — resolve via Table 2a:

| Claim | Level | Why capped | Plan |
|---|---|---|---|
| graduated_extinction_efficacy | high (⚠ warns) | 3 SR sources unverified | Verify Mindell 2006 / Meltzer-Mindell 2014 / Reuter 2020 (Table 2a). |
| behavioral_interventions_safety | moderate | reuter_2020 unverified; safety-adjacent | Verify Reuter 2020; keep cautious wording. |
| bedtime_routine_benefits | moderate | mindell_williamson_2018 unverified | Verify PDF. |
| bedtime_fading | moderate | meltzer_mindell_2014 unverified | Verify PDF. |
| positive_routines_reinforcement | moderate | mindell_2006 unverified | Verify PDF. |
| medical_ruleout_before_behavioral | moderate | aasm_2006 unverified | Verify PDF. |
| consistent_response_settling, independent_settling_readiness, sleep_associations_context | moderate/low | mindell_2006 / consultant material unverified | Verify/confirm sources. |

**(iii) Intentional `heuristic` / `low` claims with `sources: []`** — these are honest practice heuristics, *not* pending verification. They are correctly labeled `evidence_level: low` and will always be presented as lower-confidence. No confirmation required by design; revisit only if primary evidence emerges.

- constraint_first_recommending, daycare_schedule_alignment, illness_travel_recovery_approach, jetlag_gradual_shift, split_night_time_in_bed, short_naps_context, nap_transition_readiness_signs, developmental_context_sleep_shifts, bedtime_resistance_toddler_autonomy.

**Thin-coverage flags (honest gaps, within acceptance but noted for Phase 1+):**
- `split_night` rests on a single heuristic claim with no source. Candidate for an evidence-backed claim if literature supports the time-in-bed / circadian explanation.
- `early_waking`, `daycare_schedule_fit`, `illness_travel_recovery` are heuristic-only. Acceptable (the acceptance criterion counts professional-practice sources, and these are logistics/practice problems), but flagged as the weakest-evidenced goals.

---

## 6. Phase 0 acceptance criteria (spec §18 + handoff)

| Criterion | Status | Evidence |
|---|---|---|
| Every high-impact recommendation category has ≥1 evidence/professional-practice source | ✅ | Table 1b — all 11 categories covered. |
| Uncertain areas marked uncertain, not filled with invented certainty | ✅ | Table 2a/2b; heuristics labeled `low`; validator warnings surfaced, not hidden. |
| Safety red-flag list finished (D13), not an outline | ✅ | `skills/lullsense/references/safety-triage.md` (finished) + 12 `A_safety` claims (fever, dehydration, respiratory, BRUE, safe sleep). |
| Newborn safe-sleep essentials present (S3) | ✅ | safe_sleep_* claims [0,12]; `developmental-sleep.md §7`; `safety-triage.md §5`. |
| Age-tiered safety posture present (D12) | ✅ | `<4mo` handling in `safety-triage.md`; `circadian_emergence_infancy` [0,4]; `fever_under_3mo_urgent` [0,3]; consultant-practice-map §5. |
| No fabrication (spec §24) | ✅ | Every A_safety fact page-cited to a verified PDF; unverified sources flagged, not asserted. |
| Parent-goal coverage complete | ✅ | Validator prints no COVERAGE GAP; Table 1a. |

---

## 7. Phase 0 deliverables (spec §18) → artifacts

| Deliverable | Artifact | Status |
|---|---|---|
| Evidence methodology | `skills/lullsense/references/evidence-methodology.md` | ✅ |
| Source inventory | `skills/lullsense/knowledge/sources.yaml` (23) | ✅ |
| Evidence taxonomy | `skills/lullsense/references/evidence-methodology.md §2` + validator enums | ✅ |
| Age/development knowledge map | `skills/lullsense/references/developmental-sleep.md` | ✅ |
| Safety triage (finished, D13) | `skills/lullsense/references/safety-triage.md` + 12 `A_safety` claims | ✅ |
| Consultant practice map | `skills/lullsense/references/consultant-practice-map.md` | ✅ |
| Myths / unsupported-claims list | `skills/lullsense/references/myths-and-overclaims.md` | ✅ |
| Versioned claims (D2/D13) | `skills/lullsense/knowledge/claims.yaml` (45) | ✅ |
| Validator + tests | `scripts/validate_knowledge.py` + `tests/` (9) | ✅ |

---

## 8. Final validation gate

Run from repo root (`. .venv/bin/activate` first):

```
pytest -q                        → 9 passed
python scripts/validate_knowledge.py → exit 0, "Knowledge base is valid.", no COVERAGE GAP
                                       (3 expected warnings on graduated_extinction_efficacy)
ruff check .                     → All checks passed
```

---

## 9. What carries into Phase 1

- **PDF-verify the C-layer behavioral sources** (Table 2a, high priority) — this clears the `graduated_extinction_efficacy` warnings and firms the behavioral spine.
- **Consider evidence-backing the thin goals** (`split_night`, `early_waking`) if the literature supports it.
- **Phase 1 proper** (per D5/D21): canonical data schema + parsers + local experiment store; no vendor field leaks into the reasoning contract; uncertainty metadata on approximate times.
- **Persona consolidation (Phase 4 input ready):** `consultant-practice-map.md` + the two persona memories feed `skills/lullsense/references/consultant-persona.md` and the consultant eval rubric.
