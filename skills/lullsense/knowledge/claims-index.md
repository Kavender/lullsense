# Claims Index (generated — do not edit by hand)

Generated from `claims.yaml` by `scripts/build_knowledge_index.py`. One scannable line per
claim so the agent can decide **which** claims to cite without loading the full YAML.

**Retrieval:** pick the 1–3 `claim_id`s you'll actually cite from the table below, then fetch
each full entry with `lullsense-cite <claim_id>` (it also resolves a `<source_id>` from
`sources.yaml`). **Never load `claims.yaml` or `sources.yaml` wholesale in conversation.**
A_safety citations are already embedded inline in `references/safety-triage.md`.

| claim_id | layer | evidence | claim (gist — fetch full text with `lullsense-cite`) |
|---|---|---|---|
| `safe_sleep_back_to_sleep` | A_safety | high | Place a baby on their back for every sleep — naps and night… |
| `safe_sleep_firm_flat_surface` | A_safety | high | A baby should sleep on a firm, flat surface (not inclined m… |
| `safe_sleep_no_bed_sharing` | A_safety | high | A baby should sleep on their own separate sleep surface, no… |
| `safe_sleep_room_sharing` | A_safety | high | Room-sharing (baby on a separate sleep surface in the paren… |
| `bed_sharing_harm_reduction` | A_safety | high | The AAP is unable to recommend bed-sharing under any circum… |
| `safe_sleep_bare_crib` | A_safety | high | Keep soft objects and loose bedding out of the sleep space… |
| `fever_under_3mo_urgent` | A_safety | high | In an infant under 3 months (12 weeks), a temperature of 10… |
| `fever_high_or_persistent_contact` | A_safety | high | Contact the pediatrician if a fever repeatedly rises above… |
| `fever_with_serious_signs_urgent` | A_safety | high | Seek care promptly if a feverish child also looks very ill,… |
| `infant_dehydration_signs` | A_safety | high | Signs of dehydration in an infant include fewer than 6 wet… |
| `respiratory_distress_emergency_signs` | A_safety | high | Labored breathing — fast breathing, nasal flaring, head-bob… |
| `brue_episode_needs_evaluation` | A_safety | high | A brief, now-resolved episode in an infant — a pause in bre… |
| `total_sleep_4_12_months` | B_developmental | high | Infants 4-12 months generally need about 12-16 hours of sle… |
| `total_sleep_1_2_years` | B_developmental | high | Children 1-2 years generally need about 11-14 hours of slee… |
| `total_sleep_2_3_years` | B_developmental | moderate | Between the second and third year, total sleep need continu… |
| `night_waking_normal_variability` | B_developmental | moderate | About 20-30% of infants have night awakenings across the fi… |
| `sleep_consolidation_trajectory` | B_developmental | moderate | Overnight sleep becomes distinct from daytime naps for most… |
| `circadian_emergence_infancy` | B_developmental | moderate | A day-night circadian rhythm is not established at birth; s… |
| `nap_phase_progression` | B_developmental | moderate | Naps reduce gradually over early childhood — from three or… |
| `nap_transition_2to1_timing` | B_developmental | moderate | The transition from two naps to one typically occurs somewh… |
| `nap_transition_last_nap_timing` | B_developmental | moderate | The transition out of the single afternoon nap is highly va… |
| `nap_transition_driven_by_maturation` | B_developmental | moderate | Nap transitions appear to be driven by brain and memory mat… |
| `naps_support_memory` | B_developmental | moderate | Daytime naps support memory consolidation and learning in i… |
| `individual_variability_baseline` | B_developmental | high | Individual sleep need varies with genetic, behavioral, medi… |
| `developmental_context_sleep_shifts` | B_developmental | low | Periods of rapid motor, language, and separation-anxiety de… |
| `separation_anxiety_sleep_disruption` | B_developmental | moderate | Separation and attachment development — the emergence of ob… |
| `sleep_regression_reframe` | B_developmental | moderate | The popular term 'sleep regression' points at real sleep ch… |
| `bedtime_resistance_toddler_autonomy` | B_developmental | low | Bedtime resistance in toddlers is frequently a normal expre… |
| `bedtime_routine_benefits` | C_behavioral | moderate | A consistent, calming bedtime routine is associated with ea… |
| `graduated_extinction_efficacy` | C_behavioral | high | Behavioral interventions, including graduated extinction an… |
| `behavioral_interventions_safety` | C_behavioral | moderate | In studied populations, standard behavioral sleep intervent… |
| `medical_ruleout_before_behavioral` | C_behavioral | moderate | Behavioral sleep approaches are appropriate only after scre… |
| `bedtime_fading` | C_behavioral | moderate | Bedtime fading — temporarily setting bedtime closer to the… |
| `positive_routines_reinforcement` | C_behavioral | moderate | Positive bedtime routines paired with reinforcement (praise… |
| `consistent_response_settling` | C_behavioral | moderate | Consistency of the caregiver's nighttime response across ni… |
| `independent_settling_readiness` | C_behavioral | moderate | Approaches that build independent settling are generally co… |
| `sleep_associations_context` | C_behavioral | low | Sleep-onset associations such as being fed or rocked to sle… |
| `sleep_training_readiness_signals` | C_behavioral | moderate | Beyond simply reaching an age floor, readiness to begin sle… |
| `gentle_settling_approaches` | C_behavioral | low | Responsive, lower-intensity options — pick-up-put-down, the… |
| `sleep_training_expected_trajectory` | C_behavioral | low | Improvement from sleep training is usually non-linear: the… |
| `responding_to_separation_protest` | C_behavioral | moderate | During a separation-anxiety phase, responding to a child's… |
| `comfort_object_safe_sleep_gate` | C_behavioral | moderate | A transitional or comfort object (children commonly attach… |
| `constraint_first_recommending` | D_practice | low | Eliciting a family's fixed constraints (daycare nap schedul… |
| `constraint_driven_structural_debt` | D_practice | low | When an immovable outside constraint (a fixed daycare nap,… |
| `sleep_training_method_choice` | D_practice | moderate | There is no strong evidence that any one sleep-training met… |
| `sleep_training_timing_developmental` | D_practice | moderate | Starting a new extinction-based sleep-training program duri… |
| `wake_windows_as_heuristic` | D_practice | low | Time awake since the last sleep ('wake windows') is a rough… |
| `daycare_schedule_alignment` | D_practice | low | When a child is in daycare, adjusting the home schedule (es… |
| `illness_travel_recovery_approach` | D_practice | low | During illness or travel, prioritizing comfort and adequate… |
| `jetlag_gradual_shift` | D_practice | low | For travel across time zones, gradually shifting sleep and… |
| `early_waking_common_causes` | D_practice | low | Common practical contributors to early-morning waking inclu… |
| `split_night_time_in_bed` | D_practice | low | A 'split night' — a long stretch awake and calm in the midd… |
| `short_naps_context` | D_practice | low | Short naps (often around 30-45 minutes) are common and can… |
| `nap_transition_readiness_signs` | D_practice | low | Signs a child may be ready to drop a nap include consistent… |
| `wake_window_typical_by_age` | D_practice | low | Typical 'wake windows' (awake time between sleeps) lengthen… |
| `sleep_timing_prediction_is_a_range` | D_practice | low | A next-nap/bedtime estimate should be delivered as a time r… |
| `env_light_dim_pre_bed` | E_environment | moderate | A dim, low-light environment in the wind-down before sleep… |
| `env_noise_onset_may_help` | E_environment | low | White noise may help some babies fall asleep faster or slee… |
| `env_noise_efficacy_uncertain` | E_environment | low | The evidence on white noise for sleep is limited and comes… |
| `env_noise_safer_use` | E_environment | moderate | Infant sound machines can produce sound levels above recomm… |
| `env_temperature_preference` | E_environment | low | A comfortable, not-overheated room is a reasonable thing fo… |
| `env_surface_comfort_defers_to_safety` | E_environment | high | Sleep-surface 'comfort' is not an evidence-based sleep leve… |
