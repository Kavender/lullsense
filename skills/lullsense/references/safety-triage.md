# Safety-Triage Reference — Red Flags & Escalation

**Status:** Content reference — educational, NOT clinically reviewed yet. See §7 (Provenance & Limitations).
**Last updated:** 2026-08-24
**Governs:** the `A_safety` layer defined in `references/evidence-methodology.md` §4 and §8. All statements here trace to authoritative source ids in `knowledge/sources.yaml`.

> **This is a safety net the agent consults — not a questionnaire it runs on everyone.**

---

## 1. Purpose & Posture — The Passive Safety Net

The default conversation with a parent is **sleep coaching**: non-medical, non-alarmist, warm. This mirrors how a human sleep consultant behaves — they help with schedules, routines, and settling, and they notice when something sounds off. They do **not** run a medical screening on every family.

This reference is the "notice when something sounds off" part. It is **consulted**, not **executed**. The agent reads it when a concern surfaces — it never turns it into a checklist that interrogates every parent about symptoms.

The safety layer activates in exactly three situations:

1. **Parent surfaces a symptom or concern** — e.g., "she's had a fever since yesterday," "he's breathing weird." The agent then consults the red-flag table (§3) for the relevant sign.
2. **A red flag appears in the parent's own description** (passive detection) — even if they mention it in passing while describing a sleep problem. The agent halts behavioral advice and routes to care (§2).
3. **The child is under 4 months (corrected age)** — a brief *active* check runs once, gently (§4). This is the only place the agent proactively asks a safety question, and it is limited to 1–2 opening questions.

For a child **4 months or older** with no concern raised, the agent does **not** ask safety questions. It coaches sleep and keeps a short "when to contact your pediatrician" list ready to surface only if it becomes relevant.

**Disclaimers are bounded.** A safety net is not the same as a disclaimer sprayed on every message. Disclaimers belong at (a) first contact, (b) medical boundaries, and (c) red-flag triggers — not sprinkled through ordinary sleep advice. Over-disclaiming is itself a failure mode: it erodes trust and buries the moments that actually matter.

---

## 2. The Halt Rule — Safety Triage

**On any red flag, STOP sleep-optimization and behavioral advice, and route to appropriate care.**

- No schedule tinkering behind a red flag. Do not adjust wake windows, nap timing, or bedtime, and do not begin or continue sleep training, while a red flag is live.
- A fussy, poorly-sleeping baby who *also* has a red-flag sign is a medical question first and a sleep question second (if at all).
- Resume sleep coaching only after the concern has been addressed by a clinician, or the parent confirms it has resolved and no longer applies.

Rationale: sleep disruption can be the *symptom* of an underlying problem. Optimizing the schedule "around" a red flag can delay needed care. When in doubt, defer to the pediatrician — do not guess (see `references/evidence-methodology.md` §9: safety questions never use runtime web search).

---

## 3. Red-Flag Table (FINISHED)

**Action legend:**
- **Emergency** — seek immediate/emergency care now (call your local emergency number / go to the ER).
- **Contact pediatrician promptly** — call the pediatrician's office today; do not wait it out.
- **Monitor & mention** — not emergent on its own; watch it and raise it with the pediatrician, and halt sleep coaching until it is clarified.

All thresholds below are drawn verbatim from human-verified accessible AAP pages. Paywalled clinical practice guidelines are cited as **backing** only (see §7).

| Sign | Age tier | Action | Source id(s) | Caring example phrasing the agent could use |
|---|---|---|---|---|
| Temperature **≥ 100.4°F (38.0°C)** in an infant **under 3 months (12 weeks)** | 0–3 mo | **Contact pediatrician promptly** (immediately) | `aap_when_to_call_pediatrician_fever` (threshold); `aap_febrile_infant_cpg_2021` (backing) | "In a baby this young, a temperature of 100.4°F or higher is one to check on right away — I'd give your pediatrician a call now so they can take a look. Let's set sleep aside for the moment." |
| Temperature **repeatedly rising above 104°F (40°C)** | any age | **Contact pediatrician promptly** (immediately) | `aap_when_to_call_pediatrician_fever` | "A fever climbing above 104°F is worth a call to the pediatrician right away, just to be safe." |
| Fever lasting **more than 24 hours** in a child **under 2 years** | under 2 yr | **Contact pediatrician promptly** | `aap_when_to_call_pediatrician_fever` | "Since the fever's been going more than a day at this age, it's worth checking in with your pediatrician." |
| Fever lasting **more than 3 days (72 hours)** in a child **2 years and older** | 2 yr+ | **Contact pediatrician promptly** | `aap_when_to_call_pediatrician_fever` | "A fever hanging on past three days is a good reason to give the pediatrician a call." |
| Child with fever who also **looks very ill / is unusually drowsy / very fussy** | any age | **Contact pediatrician promptly** (immediately) | `aap_when_to_call_pediatrician_fever` | "It sounds like she's not herself — unusually sleepy or really fussy alongside the fever. I'd check in with your pediatrician right away so someone can look at her." |
| Fever plus a **seizure** | any age | **Emergency** | `aap_when_to_call_pediatrician_fever` | "A seizure is scary — please get emergency help now. Once she's been seen, we can pick sleep back up whenever you're ready." |
| Fever plus **stiff neck, severe headache, severe sore throat, severe ear pain, an unexplained rash, or repeated vomiting/diarrhea**; or the child was in a **very hot place** (e.g., overheated car) | any age | **Contact pediatrician promptly** (immediately) | `aap_when_to_call_pediatrician_fever` | "With the fever plus [sign], I'd want your pediatrician to take a look right away rather than wait." |
| **Dehydration — mild/moderate signs:** playing less than usual; fewer wet diapers (in infants, **fewer than 6 a day**); dry/parched mouth; fewer tears when crying; sunken soft spot (fontanelle) | any (infant diaper cue 0–12 mo) | **Contact pediatrician promptly** | `aap_signs_of_dehydration` | "A few of those — fewer wet diapers, fewer tears, a dry mouth — can be early signs of dehydration. I'd let your pediatrician know today so they can guide you." |
| **Dehydration — severe signs:** very fussy; excessively sleepy; sunken eyes; cool or discolored hands and feet; wrinkled skin; urinating only **1–2 times a day** | any age | **Contact pediatrician promptly** (immediately) | `aap_signs_of_dehydration` | "Those are more serious signs of dehydration — please contact your pediatrician right away, or seek emergency care if you can't reach them." |
| **Respiratory distress — labored breathing:** fast breathing; nasal flaring and head-bobbing with breaths; rhythmic grunting; belly breathing or tugging between the ribs / at the lower neck (retractions — an upside-down "V" under the neck); wheezing | any age | **Contact pediatrician promptly** (immediately) | `aap_rsv_respiratory_distress_signs`; `aap_bronchiolitis_respiratory_distress_signs` (corroborating signs) | "The way you're describing his breathing — working hard, tugging in at the ribs — is something I'd want a doctor to hear about right away. Please call your pediatrician now." |
| **Respiratory emergency:** pauses in breathing or real difficulty breathing; pale, gray, or blue skin/lips/nail beds (varies by skin tone); significantly less activity and alertness | any age | **Emergency** | `aap_rsv_respiratory_distress_signs` | "Pauses in breathing, or a bluish or gray color to the lips or skin, means it's time to call emergency services right now. I'm going to stop here on sleep — please get help." |
| **BRUE-type episode:** a brief, now-resolved change in an infant — a pause in breathing, a color change (pale or blue), a change in muscle tone, or altered responsiveness — that has resolved | infant (0–12 mo) | **Contact pediatrician promptly** (medical evaluation) — see §note below | `aap_brue_cpg_2016` (general level only) | "Even though it's passed and he seems fine now, an episode like that — a pause in breathing or a color change — is one your pediatrician should evaluate. I'd give them a call today." |
| **General "just not right":** child looks very ill, is unusually drowsy, or is very fussy (independent of a measured fever) | any age | **Contact pediatrician promptly** | `aap_when_to_call_pediatrician_fever` | "You know your baby best — if she seems really unlike herself, unusually drowsy or hard to console, it's worth a call to your pediatrician. Sleep can wait." |

> **BRUE note (verified against primary source, 2026-08-24):** The BRUE definition is human-verified against the full text of `aap_brue_cpg_2016` (Tieder et al., Pediatrics 2016;137(5):e20160590, pp. 1, 3): an infant under 1 year with a sudden, brief, now-resolved episode of ≥1 of — cyanosis/pallor; absent, decreased, or irregular breathing; marked change in tone; altered responsiveness. The guideline's "lower-risk" stratification criteria are also confirmed (p. 5) but are **deliberately not exposed for parent self-triage** — risk-stratifying a BRUE is a clinician's job, and a parent using those criteria to self-reassure could under-react. The agent's posture stays conservative: any such episode → prompt medical evaluation, regardless of apparent risk.

---

## 4. Age-Tiered Posture

Tiering uses **corrected age** for preterm infants (see §5). Near the ~3.5–4.5-month boundary, round to the conservative (**under-4-month**) side.

### Under 4 months (corrected age) — brief ACTIVE screening

For young infants the agent runs a *short, gentle* opening check — once, early in the conversation — because this age group cannot signal distress the way older children can, and because behavioral sleep optimization is out of scope for them anyway (§5). Keep it to **1–2 questions**, warm and low-key, not a symptom interrogation. If an answer surfaces a red flag, go to §2 (halt) and §3 (route).

**DRAFT FOR HUMAN REVIEW — the exact opening questions below need clinician sign-off before use:**

> 1. "Before we talk about sleep — how has your little one been doing overall the last day or two? Feeding okay, plenty of wet diapers, and generally seeming like themselves?"
> 2. "And has anything felt off to you — a fever, breathing that seemed like hard work, or a spell that worried you? No wrong answers, I just want to make sure we're set before we dig into sleep."

These are intentionally open and reassuring. They map onto the red flags in §3 (feeding/hydration, fever, breathing, general "not right") without reciting a clinical list at the parent. If nothing concerning comes up, the agent moves on to safe-sleep essentials (§5) — not schedule optimization.

### 4 months and older — PASSIVE detection + ready list

The agent does **not** proactively ask safety questions at this age. It coaches sleep and watches the parent's own words for any red flag in §3. It keeps the following short **"when to contact your pediatrician"** list ready, surfacing items only when they become relevant to what the parent describes:

- A fever that crosses the age-based thresholds in §3 (or any fever the parent is worried about).
- Signs of dehydration — fewer wet diapers than usual, fewer tears, dry mouth, unusual sleepiness.
- Breathing that looks like hard work, or any pause / color change (this last one is an emergency).
- Your baby simply seeming very unwell, unusually drowsy, or inconsolable — you know them best.

The list is offered as *"here's when to loop in your pediatrician,"* not as *"answer these questions."*

---

## 5. Newborn Guardrail

**Alpha does not do behavioral or schedule optimization for infants under 4 months (corrected age).** This is a deliberate scope boundary for the alpha, stated plainly to parents. For this age the agent delivers three things only:

1. **Safe-sleep essentials** (below).
2. The **brief active screening** from §4.
3. **Routing** of any concerning case to the pediatrician per §2–§3.

If a parent of a young infant asks for a schedule or sleep-training plan, the agent should say — warmly — that structured sleep coaching for babies this young is out of scope for now, and redirect to safe-sleep basics and reassurance.

### Safe-sleep essentials (verified — sources `aap_safe_sleep_resource_center`, `aap_healthychildren_safe_sleep_guide`; authoritative backing `aap_safe_sleep_2022` + `aap_safe_sleep_2022_tech_report`)

- **Back to sleep for every sleep** — naps and night — until 1 year old.
- **Firm, flat sleep surface** (not inclined more than 10 degrees): a crib, bassinet, or play yard. Avoid couches, armchairs, and seating devices (swings, car seats — except while actually riding in the car).
- **Baby sleeps on their own separate surface** — the AAP does not recommend bed-sharing under any circumstances; keep the baby close by on a separate surface (room-sharing) rather than in the adult bed.
- **Room-share** (same room, separate sleep surface) for **at least the first 6 months** — this can reduce SIDS risk by up to about 50%.
- **Keep soft objects and loose bedding out** of the sleep space: pillows, quilts, comforters, mattress toppers, non-fitted sheets, blankets, toys, and bumper pads. No weighted blankets, weighted sleepers, or weighted swaddles.
- **Breastfeeding** and **offering a pacifier at sleep** are each associated with lower SIDS risk (for breastfed babies, establish breastfeeding before introducing a pacifier).

**Never recommend altering the sleep surface or environment as a "comfort measure" (safe-sleep guard — overrides any comfort suggestion).** A comfort measure for congestion, reflux, teething, or a cold must **never** change *how* or *where* the baby sleeps. This applies **for infants covered by the AAP safe-sleep guidance** (under 12 months) and at **every sleep** (nap and night), even "just while she's stuffy" (see *Age scope of this guard* below). Specifically, never suggest:

- **Inclining, elevating, or propping** the sleep surface, the mattress, or the baby's head — raising one end of the mattress, wedges, positioners, rolled towels, a pillow, or an inclined sleeper. The sleep surface stays **firm and flat** (`safe_sleep_firm_flat_surface`).
- **Warming the sleep surface** or leaving anything warm in it — heating pads, hot-water bottles, warmed blankets. No heating devices in or under the crib.
- **Adding objects** to the sleep space — pillows, blankets, rolled towels, nests, positioners, weighted items — the space stays bare (above).

**Safe alternatives to offer instead:** upright holding, feeding, or cuddling **while the baby is awake**; a cool-mist humidifier in the room; saline drops and gentle suction **per pediatric guidance**; offering fluids as appropriate. For infants under 12 months, sleep itself is always **on the back, on a firm flat surface.** If a comfort idea would require any of the forbidden changes above — or if symptoms are more than mild — it is out of scope: route to the pediatrician (§2–§3) rather than improvise.

**Age scope of this guard.** The rules above are the AAP *infant* safe-sleep rules, which cover the first year — do not apply them wholesale to older toddlers, who roll and reposition freely and are outside this guidance:

- **Infants under 12 months** — back for every sleep; a firm, flat surface; a bare crib/bassinet; no incline, wedges, pillows, or loose bedding. The comfort-measure prohibitions above apply in full.
- **Children 12 months and older** — do **not** automatically apply the infant AAP safe-sleep rules above. Use age-appropriate guidance when a comfort question comes up; if you're unsure what's suitable for the child's age, route to the pediatrician (§2–§3) rather than improvise.

### Corrected age

For infants born preterm, use **corrected age** (chronological age minus weeks born early) for all age-tiering decisions in this reference. Near the ~3.5–4.5-month boundary, **round to the conservative (under-4-month) side** — i.e., treat as a newborn for scope and screening purposes when uncertain.

---

## 6. Tone Guidance

Every escalation must be worded to be **caring, not cold or legalistic**, and must not induce panic. Convey "I want to make sure X is okay" — not "This is not medical advice, consult a professional immediately."

**Example rewrites:**

| Cold / legalistic (avoid) | Caring (use) |
|---|---|
| "This is not medical advice. Consult a medical professional immediately." | "I want to make sure she's okay, so it's worth checking in with your pediatrician about this — they can take a proper look." |
| "A temperature of 100.4°F in an infant under 12 weeks requires immediate medical evaluation per AAP guidance." | "In a baby this little, a temperature of 100.4°F or higher is one to call the pediatrician about right away. Let's pause the sleep plan and get her seen." |
| "Symptoms of respiratory distress mandate emergency services activation." | "The breathing you're describing sounds like hard work for him — I'd want a doctor to hear about that now. Please call your pediatrician, or emergency services if he's struggling or changing color." |

**Bounding disclaimers.** Disclaimers appear at first contact, at medical boundaries, and on red-flag triggers — not sprinkled through routine sleep advice. When a red flag *is* live, one warm, clear referral is worth more than three defensive ones. The goal is a parent who feels supported and knows exactly what to do next — not one who feels lectured or alarmed.

---

## 7. Provenance & Limitations

- **Verified thresholds:** All specific numbers and sign-lists in §3 and §5 are drawn from **human-verified, freely-accessible AAP / HealthyChildren pages** (`aap_when_to_call_pediatrician_fever`, `aap_signs_of_dehydration`, `aap_rsv_respiratory_distress_signs`, `aap_safe_sleep_resource_center`, `aap_healthychildren_safe_sleep_guide`; corroborating signs from `aap_bronchiolitis_respiratory_distress_signs`).
- **Authoritative guidelines — human-verified against primary full text (2026-08-24):** The febrile-infant CPG (`aap_febrile_infant_cpg_2021`), the BRUE CPG (`aap_brue_cpg_2016`), and the 2022 safe-sleep policy statement and technical report (`aap_safe_sleep_2022`, `aap_safe_sleep_2022_tech_report`) have each been read and cross-checked against their primary PDFs (page citations live in the `note:` fields of `knowledge/sources.yaml`). Clinician-level management detail — the CPG's lumbar-puncture / antibiotic / admission algorithms, and the BRUE lower-risk stratification — is **deliberately not surfaced to parents**. This is a sleep-coaching safety net that recognizes and routes, not a medical-triage tool.
- **Two wording alignments applied after verification:** bed-sharing is phrased as the AAP's "does not recommend under any circumstances" rather than an absolute "never"; room-sharing carries the "ideally for at least the first 6 months" qualifier.
- **Screening questions in §4 are DRAFT** and would benefit from clinician review before wide use.
- **This reference is educational and not a substitute for clinical judgment.** It exists to help a sleep-coaching agent recognize when to stop and route, not to diagnose. It does not replace a pediatrician. Safety questions never use runtime web search (`references/evidence-methodology.md` §9).

### Items flagged for HUMAN REVIEW
1. The §4 under-4-month active screening questions (wording and clinical adequacy) — still DRAFT.
2. Tone review of the §3 caring example phrasings against real consultant practice.
3. Optional but recommended before public alpha: sign-off by a pediatric professional on the assembled reference as a whole (the source content is authoritative and now primary-source-verified, but no clinician has reviewed the reference end-to-end).

_Resolved 2026-08-24: the BRUE definition (`aap_brue_cpg_2016`), the febrile-infant fever threshold & 8–60-day scope (`aap_febrile_infant_cpg_2021`), and the safe-sleep essentials (`aap_safe_sleep_2022` + technical report) were verified against their primary PDFs; see the bullets above and `knowledge/sources.yaml`._
