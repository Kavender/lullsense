# Evidence Methodology — LullSense

**Status:** Canonical reference — do not rename fields or enum values without updating `scripts/validate_knowledge.py` in the same commit.
**Last updated:** 2026-08-23

---

## 1. Purpose

The knowledge layer of LullSense separates two fundamentally different kinds of statements: **evidence-backed claims** (derived from clinical guidelines, research, or professional consensus) and **heuristics** (derived from practitioner experience or product convention). These two categories carry different epistemic weight and are used in different contexts.

Mixing them without labeling is a common failure mode in parenting advice tools. A fixed wake-window chart is not a clinical standard. A named "four-month sleep regression" is not a medical diagnosis. An observation that "most families find an early bedtime helpful" is not equivalent to the AASM's published recommendation for total sleep duration.

This project makes the distinction explicit and machine-checkable:

- Every claim in `knowledge/claims.yaml` carries an `evidence_type`, an `evidence_level`, and a `layer` field that together describe what kind of knowledge it is and how confident we are in it.
- Every source backing a claim is versioned in `knowledge/sources.yaml` with its own provenance metadata.
- Safety conclusions are drawn exclusively from authoritative sources (AAP, AASM, pediatric sleep medicine). Heuristics may support scheduling suggestions but never safety conclusions.
- Uncertainty is preserved rather than glossed over. When a fact cannot be sourced during content authoring, it is marked `verified: false` or `evidence_level: low` rather than being asserted with false confidence.

The validator (`scripts/validate_knowledge.py`) mechanically enforces this schema. Any drift between this document and the validator is a bug.

---

## 2. Evidence-Type Taxonomy

Each claim must carry exactly one of the following `evidence_type` values. These are the only permitted enum values — the validator rejects any other string.

| `evidence_type` | Definition |
|---|---|
| `guideline` | A formal, named clinical recommendation issued by a recognized professional body (e.g., AAP safe-sleep policy statement, AASM pediatric sleep-duration health advisory). |
| `professional_consensus` | A consensus position endorsed by one or more professional organizations but not issued as a formal named guideline (e.g., a joint society statement, an expert panel summary). |
| `systematic_review` | A synthesis of the primary literature using pre-specified inclusion criteria and, where applicable, meta-analysis (e.g., a Cochrane review of behavioral sleep interventions). |
| `primary_research` | A single peer-reviewed study (RCT, cohort, observational, case series) that provides direct empirical evidence for the claim. |
| `expert_practice` | Widely cited practitioner or consultant practice that lacks formal research backing but is drawn from publicly documented professional advice (e.g., published consultant intake frameworks, professional educational materials). |
| `heuristic` | A product or operational rule of thumb derived from practitioner experience, common industry convention, or internal project convention — not backed by any external source. Heuristics must be `evidence_level: low` and may never be `layer: A_safety`. |

---

## 3. Evidence Level

Each claim carries an `evidence_level` reflecting the overall confidence in the claim given its best available evidence:

| `evidence_level` | Meaning |
|---|---|
| `high` | The claim is supported by a formal guideline, professional consensus, or a well-conducted systematic review with consistent findings. The claim would survive reasonable expert scrutiny and may be stated without major hedging. |
| `moderate` | The claim is supported by one or more primary studies or a professional consensus without the strength of a formal guideline; findings are generally consistent but may have important limitations or gaps. State with appropriate hedging. |
| `low` | The claim is a heuristic, based on limited evidence, or drawn from a single small study or expert opinion only. Must be explicitly labeled as lower-confidence when presented to users. All heuristics must be `low`. |

---

## 4. The Four Knowledge Layers

Claims are assigned to one of four layers that determine how the reasoning workflow uses them. Layer assignment is not just organizational — the safety rule in §8 has different requirements per layer.

### `A_safety`

Safety and clinical guardrails. Sources must be authoritative (AAP, AASM, pediatric sleep-medicine professional guidance, or high-quality systematic reviews). Content in this layer governs:
- Safe-sleep essentials (sleep surface, position, environment)
- Sleep-duration context used as a health guardrail
- Red-flag symptoms requiring medical escalation
- Statements that override or halt ordinary behavioral sleep coaching

Claims in this layer are never derived from heuristics. If a safety-adjacent question cannot be answered from an authoritative source, the system defers rather than guessing.

### `B_developmental`

The developmental sleep model. Covers circadian and homeostatic sleep maturation, sleep consolidation, nap organization and transitions, individual variability, and developmental context (motor, language, separation-individuation). Age milestones are priors and context, not diagnoses. Variability between healthy children is high and must be stated. Sources should be systematic reviews, primary research, or professional educational materials; heuristics are not preferred for this layer.

### `C_behavioral`

Behavioral sleep medicine. Covers bedtime routines and sleep hygiene, graduated settling approaches, bedtime fading, positive routines and reinforcement, and assessment/monitoring of behavioral interventions. Claims here should distinguish interventions with evidence (e.g., extinction and graduated extinction have systematic-review-level support) from widely used but weakly validated practices (e.g., specific routine durations). Expert-practice sources are acceptable but should be labeled as such.

### `D_practice`

The human consultant playbook. Distilled from public materials published by reputable practitioners and sleep-specialist products: intake strategy, how constraints are elicited, practical troubleshooting, and reassessment craft. Claims in this layer describe how experienced practitioners approach common problems — not clinical standards. `expert_practice` and `heuristic` evidence types are expected here. Content must not reproduce copyrighted proprietary text; it must synthesize observable public practice.

### `E_environment`

The sleep-environment / comfort differential (Hypothesis #8; `references/environment-comfort-factors.md`). Covers light, noise, and temperature as *things to observe and rule out conversationally* — not a checklist. Evidence here is **deliberately mixed and labeled honestly rather than dropped**: light is mechanistic + preschool-aged (melatonin markers, not measured infant sleep), noise efficacy and temperature are low/preference-level, and noise safer-use (sound-machine output limits) is documented. The **sleep surface itself is not in this layer as a lever** — surface "comfort" is safety-governed and defers to `A_safety` (`safe_sleep_firm_flat_surface`); the boundary claim `env_surface_comfort_defers_to_safety` records that deferral. `<4 mo` is out of scope for this layer, as for the rest of the behavioral content.

---

## 5. Claim Schema

All claims in `knowledge/claims.yaml` must conform to this schema. Field names and allowed values are exact — the validator enforces them literally.

```yaml
- claim_id: <snake_case_unique>
  layer: A_safety | B_developmental | C_behavioral | D_practice
  topic: <short_snake_case_topic>
  parent_goals: [ ... ]        # subset of the controlled goal list in §6; may be []
  age_range_months: [<min>, <max>]   # ints, 0 <= min <= max
  evidence_type: guideline | professional_consensus | systematic_review | primary_research | expert_practice | heuristic
  evidence_level: high | moderate | low
  claim: "<one plain-language sentence>"
  sources: [<source_id>, ...]  # each must exist in sources.yaml; may be [] ONLY for heuristics
  use_for: [ ... ]
  do_not_use_for: [ ... ]
  individual_variability: high | moderate | low
  last_reviewed: YYYY-MM-DD
```

### Field definitions

**`claim_id`** — Unique snake_case identifier for this claim. Used by the validator, tests, and cross-references. Never reuse a retired ID; deprecate instead.

**`layer`** — One of the four layer values in §4. Governs which safety rules apply (see §8).

**`topic`** — Short snake_case label grouping related claims (e.g., `safe_sleep_surface`, `sleep_duration`, `nap_transition`). Not a controlled vocabulary, but should be consistent within the file.

**`parent_goals`** — Zero or more values from the controlled goal vocabulary in §6. Declares which user-facing goals this claim is relevant to. May be an empty list `[]` if the claim is background context rather than directly goal-targeted.

**`age_range_months`** — A two-element list of non-negative integers `[min, max]` with `min <= max`. Specifies the age range to which the claim applies. Use `[0, 0]` only if truly age-independent and min equals max is meaningful; otherwise express the full applicable range (e.g., `[0, 4]` for newborn-specific guidance). Age `0` means birth.

**`evidence_type`** — One of the six enum values in §2. Describes the best-available source type for this claim.

**`evidence_level`** — One of `high`, `moderate`, `low` as defined in §3.

**`claim`** — A single plain-language sentence stating what the claim asserts. Should be comprehensible to a non-specialist parent. Do not embed citations or jargon here.

**`sources`** — A list of source ID strings, each corresponding to an entry in `knowledge/sources.yaml`. Must be non-empty for all claims except those with `evidence_type: heuristic`. For heuristics, `[]` is permitted and expected.

**`use_for`** — A list of strings describing contexts where this claim appropriately applies. Helps the reasoning layer select claims accurately.

**`do_not_use_for`** — A list of strings describing contexts where this claim must not be applied, even if superficially relevant. Prevents the system from misapplying valid evidence (e.g., a population sleep-duration reference must not be used to prescribe an exact bedtime for a specific child).

**`individual_variability`** — One of `high`, `moderate`, `low`. Describes how much individual variation exists around the stated claim. A `high` value means the claim describes a population central tendency and will not hold for many healthy children — the reasoning layer must communicate this to parents.

**`last_reviewed`** — ISO 8601 date (`YYYY-MM-DD`) on which a human last verified this claim against its sources and confirmed it remains current. See §10 for review discipline.

---

## 6. Controlled Parent-Goal Vocabulary

The `parent_goals` field in every claim must be drawn exclusively from this list. There are exactly 10 allowed values:

1. `early_waking`
2. `bedtime_resistance`
3. `night_waking`
4. `split_night`
5. `short_naps`
6. `nap_transition`
7. `daycare_schedule_fit`
8. `illness_travel_recovery`
9. `independent_settling`
10. `is_this_normal`

No other values are permitted. If a new goal is needed, it must be added to this list in this document and in the validator in the same commit.

---

## 7. Source Schema

All sources backing claims must be declared in `knowledge/sources.yaml`. Each entry must conform to this schema. Field names and allowed values are exact.

```yaml
- id: <snake_case_unique>
  organization: <string>
  title: <string>
  url: <https url>
  source_type: guideline | consensus_statement | systematic_review | primary_research | review | consultant_public_material
  verified: true | false      # false until a human confirms URL + content
  last_accessed: YYYY-MM-DD
```

### Field definitions

**`id`** — Unique snake_case identifier referenced by `claim.sources` lists. Never reuse a retired ID.

**`organization`** — The issuing or publishing organization (e.g., `American Academy of Pediatrics`, `American Academy of Sleep Medicine`, `Cochrane Collaboration`).

**`title`** — The full title of the document, guideline, or article as published.

**`url`** — A fully qualified HTTPS URL pointing to the source. Must begin with `https://`. Do not fabricate URLs. If a source is not freely accessible online, use the DOI URL or the publisher's landing page.

**`source_type`** — One of the following values:

| `source_type` | Meaning |
|---|---|
| `guideline` | A formal named clinical recommendation from a professional body. |
| `consensus_statement` | A joint or expert-panel consensus position, not a formal guideline. |
| `systematic_review` | A systematic literature review or meta-analysis. |
| `primary_research` | A single peer-reviewed study. |
| `review` | A narrative review, professional educational article, or evidence summary that does not meet systematic-review criteria. |
| `consultant_public_material` | Publicly available material from a named sleep consultant, practitioner organization, or sleep-specialist product (e.g., a published protocol, a public blog post with professional authorship). |

**`verified`** — Boolean. Set to `false` at initial entry. A human contributor must access the URL, confirm the content matches the claim it is cited for, and change this to `true`. Automated agents must not set `verified: true` unless they can confirm the current content at the URL. The validator will warn (not fail) when unverified sources back `evidence_level: high` claims.

**`last_accessed`** — ISO 8601 date (`YYYY-MM-DD`) on which the URL was last confirmed to be accessible and to contain the expected content.

---

## 8. Hard Safety Rule

This rule is enforced mechanically by `scripts/validate_knowledge.py`. Any claim that violates this rule must be rejected by the validator before the claim can be committed.

**The rule states:**

A claim with `layer: A_safety` **MUST**:
- have `evidence_type` drawn from exactly: `{guideline, professional_consensus, systematic_review}`
- have `evidence_level: high`
- have a non-empty `sources` list (i.e., `sources` must contain at least one source ID)

Additionally:
- `evidence_type: heuristic` **MAY NEVER** be assigned `layer: A_safety`. This is an absolute prohibition.
- `evidence_type: heuristic` **MUST** always be `evidence_level: low`. A heuristic with `evidence_level: moderate` or `evidence_level: high` is invalid.

These constraints encode the principle that safety guidance must be grounded in authoritative sources and that practitioner conventions or product heuristics — however useful for scheduling — cannot stand alone as safety claims.

**Rationale:** A parent following safety guidance trusts that it reflects professional medical consensus. Presenting a heuristic alongside AAP-level guidance without distinction violates that trust and creates liability risk. The machine check exists because human reviewers miss this under time pressure.

---

## 9. Runtime Web-Search Fallback

For non-safety questions, the agent may answer gaps not covered by `knowledge/claims.yaml` by querying publicly available information at runtime. When this fallback is used:

- The response must be labeled as **not versioned** and **lower-confidence** than claim-backed answers.
- Queries must be de-identified: use only high-level sleep-science terms (e.g., "AAP safe sleep 2022 recommendations"), never any child's identifying details.
- The agent must distinguish clearly in its response between answers derived from `claims.yaml` (versioned, source-backed) and answers derived from runtime search (current but unreviewed).

When a non-safety gap is encountered repeatedly through runtime search, it becomes a candidate for the next `claims.yaml` revision. Contributors should open a tracking issue or note describing the gap, the sources that would support it, and the proposed claim. This closes the loop between runtime knowledge and the versioned knowledge base.

**Safety questions NEVER use runtime search.** If a safety question cannot be answered from an authoritative source in `claims.yaml`, the system must:
1. State that it cannot provide a confident safety answer.
2. Direct the parent to their pediatrician or appropriate emergency resource.
3. Not attempt to answer from a search result.

---

## 10. Review Discipline

### `last_reviewed` semantics

The `last_reviewed` date on a claim records when a human contributor last read both the claim text and the source(s) it cites, confirmed that the source URL is accessible, confirmed that the source content still supports the claim as written, and updated the claim if the source had changed.

Automated agents setting `last_reviewed` to the current date without performing this check must set the associated source's `verified: false`. The date alone is not sufficient to certify correctness.

### Versioning and re-checking

Claims are not deleted; they are deprecated by adding a `deprecated: true` field and a `deprecated_reason: <string>`. The validator will warn about deprecated claims appearing in active use-for contexts.

When a source issues an update (e.g., the AAP revises its safe-sleep policy), every claim citing that source must be re-reviewed before the source's `last_accessed` date is updated. The claim's `last_reviewed` date must be updated simultaneously.

### Suggested review cadence

- `A_safety` and `B_developmental` claims: annual review minimum, or on publication of a major guideline update from AAP/AASM or equivalent authority.
- `C_behavioral` and `D_practice` claims: biannual review minimum.
- Any claim where the source's `verified` field is `false`: must be verified within 30 days of initial commit or removed from the knowledge base.

The phase-0 coverage matrix (`docs/phase-0-coverage-matrix.md`) tracks which parent goals have at least one `A_safety`- or `B_developmental`-layer claim and serves as the starting point for coverage gap analysis during each review cycle.
