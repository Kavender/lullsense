# Sleep Training — Options, Choice, and Evidence

**Status:** Content reference — educational, pending maintainer medical review. Anchor every statement to `knowledge/claims.yaml`; cross-check with the sibling `references/*.md` docs listed at the bottom.

---

## Purpose

This is the single navigable place for the "sleep training" topic. It lets the agent answer, from one document: *what are my options, which do I pick, when can I start, what is Ferber vs extinction, I want the gentlest method, is it safe — what about the crying?*

It gathers material that also appears, in narrower form, in `references/interventions.md` (the minimal-experiment menu), `references/reasoning-framework.md` (hypothesis: bedtime association / changed settling pattern), and `references/myths-and-overclaims.md §6` (crying is not automatically behavioral). Where those docs go deeper on a mechanism, this file cross-references rather than restates.

**Framing invariants for every answer here:**

- **Never diagnose.** Present a menu; the family chooses.
- **Method-neutral, non-judgmental.** There is no single "best" method (`sleep_training_method_choice`), and **no obligation to sleep-train at all** (`independent_settling_readiness`). Never evangelize one approach or imply that continuing to settle a child is a failure.
- **Medical-first.** Crying at sleep time is a differential-diagnosis question first and a behavioral one second (`medical_ruleout_before_behavioral`, `references/myths-and-overclaims.md §6`). Nothing in the menu applies until medical and physical causes (illness, pain, reflux, hunger) are screened out.
- **Evidence honesty.** Efficacy is systematic-review-backed for **extinction, graduated extinction, and bedtime fading only**. Gentle/no-cry options, readiness signals, and the improvement trajectory rest on **weaker, practitioner-judgment evidence** — say so plainly (see §6). Never present a heuristic as a systematic-review fact, and never invent statistics, percentages, or night-counts.

---

## 1. When to start

**Age floor (a labeled convention, not a hard rule).** Approaches that build independent settling are generally considered reasonable **from around 4–6 months onward**, once medical causes are excluded and the child is developmentally ready (`independent_settling_readiness`). This ~4–6-month floor is an honestly-labeled clinical-readiness **convention**, not a threshold established by the efficacy sources — the systematic-review evidence is described for infants roughly 5–6 months and up, and the exact lower bound is practitioner judgment (`graduated_extinction_efficacy`, do-not-use-for note in `knowledge/claims.yaml`).

**Under 4 months is out of scope** for behavioral sleep optimization. For younger infants the work is safe sleep and feeding, not settling training (see `circadian_emergence_infancy` and `references/developmental-sleep.md`). Do not offer a settling method for an infant under about 4 months.

**Readiness is more than an age.** Beyond simply clearing the age floor, readiness to begin is usually judged by several signals **together** (`sleep_training_readiness_signals`): the child has been medically cleared, is developmentally settled rather than in the middle of an acute change (illness, travel, a big milestone), feeds and grows well, has a reasonably established sleep and feeding pattern, and **the family itself feels ready to be consistent.** These are practitioner-judgment signals, **not a validated diagnostic checklist** — present them as a way to decide whether *now* is a reasonable time, never as a test the family must pass. Their presence does not obligate anyone to start.

A **peak separation-anxiety phase** (the object-permanence/separation development commonly around 9 months, sometimes recurring in the toddler year — see `references/developmental-sleep.md §6`) is one example of "an acute developmental change" that can make it a harder time to *start* a fresh extinction-based program (`sleep_training_timing_developmental`). Starting mid-phase is often harder, and a temporary worsening during it may reflect the phase rather than method failure; a gentler, more responsive approach or briefly waiting until the phase settles can fit better. This is a timing consideration, not a rule — the family may still choose to start, and whatever is chosen, consistency of application still drives outcomes. Balance it honestly: there is almost always *some* developmental change in progress (teething, a motor or language leap, separation), so waiting for a perfectly disruption-free window can quietly become never starting. Behavioral approaches are supported as effective and safe across these periods (`graduated_extinction_efficacy`, `behavioral_interventions_safety`), so family readiness and consistency matter more than perfect timing — offer the timing point as information, never as a reason the family "should" wait.

**Medical-first gate (hard prerequisite).** Before any method is discussed, screen for illness, pain, reflux, and hunger (`medical_ruleout_before_behavioral`). If a plausible medical or physical cause is present, address it first; if a safety red flag is present, halt and route to care per `references/safety-triage.md`. Crying is not evidence that a behavioral method is warranted.

---

## 2. Methods menu

Each method below lists a plain-language procedure, its **evidence strength**, the **crying/protest to expect** (how much crying the family is likely to encounter — this is *not* a measure of how well the method works), and **who it tends to fit**. Efficacy for the extinction family and bedtime fading is anchored to `graduated_extinction_efficacy` and `bedtime_fading`; the gentler options are anchored to `gentle_settling_approaches` and are explicitly **thinner-evidence**. Present as a menu — the family picks (see §3).

### Standard / full extinction ("cry it out")
- **Procedure:** After a consistent bedtime routine and goodbye, the parent puts the child down awake and does not return to actively settle them until the next morning (or the next scheduled feed), barring a genuine need.
- **Evidence:** Systematic-review / meta-analysis supported for reducing bedtime resistance and night wakings, once medical causes are excluded (`graduated_extinction_efficacy`).
- **Crying/protest to expect:** Highest. The most protest up front; often the fastest of the researched methods.
- **Fits:** Families who prefer a clear, brief approach and are comfortable tolerating short-term crying.

### Graduated extinction (Ferber-style check-ins)
- **Procedure:** Parent puts the child down awake and checks in at progressively longer intervals, offering brief reassurance without fully settling the child to sleep.
- **Evidence:** Same systematic-review support as standard extinction (`graduated_extinction_efficacy`); this is the method with the strongest and most-studied backing in the menu.
- **Crying/protest to expect:** High, but graded — check-ins soften it relative to full extinction.
- **Fits:** Families who want an evidence-supported approach but prefer some ongoing contact rather than none. See `references/interventions.md §4` for the check-in spectrum and observation metrics.

### Camping-out / chair method
- **Procedure:** Parent stays in the room but gradually reduces active soothing and, over successive nights, moves their position (e.g., chair) progressively farther from the crib until they are out of the room.
- **Evidence:** Thinner. A responsive, lower-intensity option grounded in `gentle_settling_approaches` (evidence level: low) — plausibly effective but less studied than graduated/standard extinction, so effectiveness and timeline are less predictable.
- **Crying/protest to expect:** Lower-to-moderate; parent stays present.
- **Fits:** Families who want to remain in the room and minimize crying, and who can tolerate a slower, less-predictable timeline.

### Pick-up / put-down
- **Procedure:** When the child protests, the parent picks them up to calm them, then puts them back down drowsy-but-awake, repeating as needed.
- **Evidence:** Thinner — `gentle_settling_approaches` (evidence level: low). Same honesty caveat as above.
- **Crying/protest to expect:** Low; high parental presence and hands-on soothing.
- **Fits:** Younger-end or highly sensitive children and families set on staying present; note it can be physically demanding and slow.

### Bedtime fading
- **Procedure:** Temporarily set bedtime at or near the child's natural sleep-onset time (where they fall asleep without extended protest), then shift it earlier in small increments over a couple of weeks toward the target time.
- **Evidence:** Systematic-review supported for bedtime resistance and prolonged sleep onset (`bedtime_fading`). Targets bedtime **timing**; it does not by itself resolve night waking unrelated to timing.
- **Crying/protest to expect:** Low. Little to no added crying when applied well.
- **Fits:** Families whose problem is a long, contentious sleep-onset battle with an alert child, and who prefer to avoid extinction. Full procedure and reassessment windows: `references/interventions.md §2`.

### Positive routines + reinforcement (older toddlers)
- **Procedure:** A consistent, calming bedtime routine paired with simple reinforcement (praise, a sticker chart) to reduce resistance.
- **Evidence:** Systematic-review supported for reducing bedtime resistance in older toddlers and preschoolers, roughly 18 months and up (`positive_routines_reinforcement`). Requires a child old enough to understand reinforcement.
- **Crying/protest to expect:** Low; collaborative and low-conflict.
- **Fits:** Verbal older toddlers with bedtime resistance (not infants). Pairs with a strong routine — see `bedtime_routine_benefits` and `references/interventions.md §3`.

### Gentle / responsive / no-cry approaches (the category)
- **Procedure:** An umbrella for responsive, lower-intensity strategies — camping-out, pick-up/put-down, gradual fading of parental presence — where the parent stays present and works to minimize crying.
- **Evidence:** **Thinner than extinction.** `gentle_settling_approaches` (evidence level: low): reasonable choices, plausibly effective, but the specific evidence base is weaker than for graduated or standard extinction, so effectiveness and timeline are **less predictable**. Being gentler does **not** make them inherently safer — extinction methods have not been shown to cause lasting harm either (§5).
- **Crying/protest to expect:** Low; highest parental presence.
- **Fits:** Families who are uncomfortable with crying and prefer to stay present, and who accept a possibly slower, less-certain result.

**A note on associations.** Being fed or rocked to sleep is common and **not inherently harmful**; it becomes a target for a method only if the family wants to change how the child returns to sleep in the night (`sleep_associations_context`). No family is obligated to eliminate an association.

---

## 3. Choosing a method

There is **no strong evidence that any one method is superior for every child** (`sleep_training_method_choice`). The practical choice is guided by three things:

- **Family comfort / values / crying tolerance** — an approach the family cannot bring themselves to apply consistently is the wrong approach for them.
- **The child** — age (positive routines suit older toddlers; extinction/graduated apply from ~5–6 months), temperament, and sensitivity.
- **The specific goal** — bedtime-onset battles point to fading; association-driven night waking points to a modified parent response; toddler bedtime resistance points to routine + reinforcement.

**Consistency beats method.** How consistently a method is applied across nights matters more than which method is picked (`consistent_response_settling`). Switching methods nightly tends to backfire; a less-optimal method applied consistently usually beats a "better" method applied erratically. Help the family choose something they can actually sustain — do not rank a named method as clinically best. (For how to *say* this warmly, see the persona layer.)

---

## 4. What to expect

Improvement is usually **non-linear** (`sleep_training_expected_trajectory`):

- **The first few nights are commonly the hardest.**
- A temporary increase in protest — an **"extinction burst"** — can occur before things improve.
- It often takes **roughly one to two weeks** of consistent application before a reliable pattern settles.
- **Judge progress over days, not from a single night.** One hard night is not failure.

Set this expectation *before* the family starts, so an early rough night is not misread as the method failing. Do **not** promise a precise number of nights to success — that number varies by child and is not something the evidence supplies.

**Reassessment and stop criteria:**

- Reassess the *method* after about **1–2 weeks** of genuinely consistent application (`sleep_training_expected_trajectory`, `consistent_response_settling`). Two nights of data is not enough to judge.
- If protest is worsening and **coincides with illness, pain, or another medical change, do not dismiss it as a normal "burst" — reassess** and re-screen medically (`medical_ruleout_before_behavioral`).
- A worsening that coincides with a **peak separation-anxiety phase** can reflect development rather than method failure (`sleep_training_timing_developmental`; `references/developmental-sleep.md §6`) — weigh whether this is a good time to be starting fresh, and consider a gentler/responsive approach or briefly waiting, without reading the worsening as proof the method is wrong.
- If the family is **no longer comfortable continuing**, that is a legitimate stop point. Never pressure a family to persist through distress they no longer want to tolerate. Stopping or switching to a gentler approach is always a valid choice.

---

## 5. Non-judgment and a parent-vocabulary map

Parents arrive with their own words. Meet the language they use, then map it to what it means — without correcting them for how they phrased it.

| Parent's term | What it usually maps to | Note |
|---|---|---|
| "Cry it out" / "CIO" | Standard / full extinction | Often used loosely for any crying-tolerant method; clarify which they mean. |
| "Ferber" / "Ferberizing" / "controlled crying" | Graduated extinction (timed check-ins) | The most-studied method (`graduated_extinction_efficacy`). |
| "Gentle" / "no-cry" / "responsive" | Responsive, low-intensity options (camping-out, pick-up/put-down, fading presence) | Thinner evidence base (`gentle_settling_approaches`) — say so honestly. |
| "Chair method" / "camping out" | Gradual fading of parental presence | A gentle/responsive option. |
| "Sleep training" | The category as a whole | Not a single method; open the menu (§2) rather than assuming which one. |
| "Self-soothing" / "independent settling" | The *goal* (child returns to sleep without active parental settling) | A goal, not a method; and an optional one. |

**Families who will not sleep-train.** Many families choose to keep feeding, rocking, or otherwise settling their child, and that is a fully valid choice (`sleep_associations_context`, `independent_settling_readiness`). Sleep training is optional and values-dependent. Acknowledge and support these families; focus on other levers (routine, timing, environment — `references/interventions.md`). Never frame continued parental settling as a failure or a problem to fix.

**Comfort / transitional objects (safe-sleep-gated).** A lovey or comfort object (children commonly attach to one between about 8 and 12 months) can help some children with separation at sleep and be built into a bedtime ritual — but it must **NOT** be placed in the sleep space until the child is past the safe-sleep bare-crib window: soft objects and loose bedding stay out of the crib through the first 12 months (`comfort_object_safe_sleep_gate`, which defers to `safe_sleep_bare_crib` and never softens it). Before then, comfort comes from caregiver continuity and reassurance, not an object in the crib. A comfort object is never required, and a child who does not attach to one does not have a problem.

**Addressing cortisol / attachment fears (handle honestly, never dismissively).**

> Your concern about crying and stress is a real and reasonable one, and it deserves a straight answer rather than reassurance for its own sake. In the populations that have been studied, standard behavioral sleep approaches used appropriately have not been shown to cause lasting harm to the parent–child relationship or to the child's stress regulation. One randomized controlled trial that actually measured infants' salivary cortisol and later mother–child attachment found no adverse stress response and no long-term attachment or behavioral effects for graduated extinction or bedtime fading (Gradisar 2016). A systematic review reached a broadly consistent conclusion (Reuter 2020). I want to be honest about the limits, though: that evidence is "in studied populations," it draws on a single small randomized trial for the cortisol and attachment findings, and it cannot guarantee any particular outcome for your specific child. What it does mean is that there is no good evidence these methods are harmful — but the decision, and how far you are comfortable going, stays entirely with you.

This paragraph is anchored to `behavioral_interventions_safety` (which cites `gradisar_2016_infant_sleep_rct` and `reuter_2020_infant_sleep_systematic_review`). Rules for using it: never dismiss the parent's worry, never guarantee safety or "zero distress," always keep the "in studied populations" and small-single-RCT caveats, and never use it to pressure a hesitant family toward a method (`behavioral_interventions_safety`, do-not-use-for notes).

---

## 6. Evidence transparency

One honest hierarchy, so the agent never overstates:

- **Systematic-review / meta-analysis backed (strongest here):** standard extinction, graduated extinction, and bedtime fading for reducing bedtime resistance and night wakings, after medical causes are excluded — `graduated_extinction_efficacy`, `bedtime_fading` (verified sources: `mindell_2006_behavioral_treatment_review`, `reuter_2020_infant_sleep_systematic_review`; safety: `gradisar_2016_infant_sleep_rct` via `behavioral_interventions_safety`). Positive routines + reinforcement for older toddlers is also review-supported (`positive_routines_reinforcement`).
- **Practitioner-judgment / lower-evidence (say so explicitly):** gentle / responsive / no-cry methods (`gentle_settling_approaches`, level: low), the readiness signals (`sleep_training_readiness_signals`, a judgment cluster, **not** a validated checklist), and the improvement trajectory / extinction-burst / 1–2-week pattern (`sleep_training_expected_trajectory`, level: low). The ~4–6-month age floor is likewise a convention, not a source-established threshold.
- **Where the literature is silent, say so.** There is no evidence base for a precise number of nights to success, for head-to-head superiority of one method over another (`sleep_training_method_choice`), or for exact wake-window charts (`references/myths-and-overclaims.md §1`). Do not fill these gaps with invented numbers.

**Never** present a low-evidence heuristic as a systematic-review fact, and **never** fabricate statistics, percentages, or night-counts. When strength of evidence differs across the menu, name the difference — that honesty is the point of this section.

---

## Cross-references

- Behavioral intervention menu, procedures, observation metrics: `references/interventions.md` (esp. §2 bedtime fading, §3 routine, §4 modified parent response)
- Hypothesis reasoning (bedtime association / changed settling): `references/reasoning-framework.md`
- Medical screening, red flags, halt-and-refer: `references/safety-triage.md`
- Crying is not automatically behavioral; overclaim guardrails: `references/myths-and-overclaims.md §6`
- Developmental norms and the under-4-month scope: `references/developmental-sleep.md`
- All claim IDs and evidence levels: `knowledge/claims.yaml`
