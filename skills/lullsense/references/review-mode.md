# Review Mode — parent-initiated "review my recent sleep"

**Loaded on demand** from `SKILL.md` Step 5b (longitudinal review) on a review ask.
Terminating leaf — `mcp-data-provider.md` / `consultant-persona.md §4b` tags are attribution; the calm delivery contract lives in the persona and is pointed to from SKILL.md, not chained from here.

---

## Review mode (parent-initiated "review my recent sleep")

A **review** is the longitudinal counterpart to the problem-driven workflow above: the parent asks how sleep has been *without* naming a specific problem. Steps 1–2 are unchanged (safety first; establish age); the Step-2 "goal" is simply *general review*. What differs is data acquisition and delivery.

### Acquire fresh data first, and guard its freshness

A review reasons about *recent* sleep, and the store keeps **no** raw logs — so data cannot be reconstructed from state and must be obtained at review time. In order: (1) ask the parent for a current export/paste; (2) if a provider is connected, fetch `get_sleep_sessions(as_of − window, as_of)` on demand (`references/mcp-data-provider.md`); (3) otherwise run a conversational review from the parent's recollection. **Never reuse an old copy** — presenting a month-old log as "this week" is a fabrication.

**Freshness guard.** `scripts/analyze_sleep.py --review` emits a `review.coverage` descriptor (`start_date`, `end_date`, `n_days`, `span_days`, `days_since_last_entry`, `is_current`, `covers_window`). If `is_current` is false (newest entry older than the staleness tolerance — a **product heuristic, currently 3 days**), `review.status` is `stale_data` and nothing is surfaced: say plainly that the data covers an older stretch, and ask for a current export or offer a conversational review. If `covers_window` is false, the data spans less than the window the parent asked about — mention it rather than over-reading a few days as "the last two weeks."

### Reading the `review` block

Beyond the `signals` array (above), `--review` adds a `review` object: `status`, `coverage`, `surfaced`, `also_noted_count`, `steady_domains`, `context_note`, `reason`.

- **`surfaced`** — the signals to present, already ranked (severity → confidence → persistence), de-duplicated (correlated signals folded — e.g. a split night subsumes its night-waking and early-waking), and capped (top two, **plus any significant-severity shift** so a big change is never buried). Present these first, each with its `supporting_evidence` and `limitations`, exactly as in "Reading the analysis JSON."
- A folded-dominant signal may carry the limitation **"severity reflects a more-severe related pattern folded into this signal"** — its severity was raised to match the more-severe change it absorbed, so it is surfaced honestly without double-counting. Read it; do **not** re-surface the folded signal separately.
- **`also_noted_count`** — how many further real shifts exist beyond the surfaced ones. Mention them as a brief honest count ("a couple of smaller shifts too"), offer to go deeper, and do not enumerate unprompted.
- **`steady_domains`** — the domains checked and found steady (night sleep, naps, bedtime, total sleep, schedule consistency). Lead with these; a quiet review should feel *earned*, not empty.
- **`context_note`** — a `possible_context_related_disruption` signal pulled aside to **reframe** the review ("this overlaps the cold you mentioned"), not to add another problem. It stays correlational and never names a cause.

### Individualize — the literature is a reference, not a manual

Every surfaced signal is a **pattern worth exploring against *this* child and family**, never a verdict. The same presentation can have different underlying causes, so keep the multi-hypothesis stance (Step 6) and each claim's `individual_variability` front-of-mind rather than applying textbook thresholds mechanically (maintainer's pediatrician, 2026-08-27). A review continues into Steps 6–7 only if the parent wants to act; it can legitimately end at calibrated reassurance.
