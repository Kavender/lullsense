# Canonical Data Contract — `baby_sleep.contract`

> **Status: reference — loaded on demand by the skill.**
> Integrators supplying sleep data to this skill must map their data to this schema.
> The skill's reasoning layer consumes only the canonical contract; no vendor-specific fields cross the boundary.

---

## 1. Overview

The `baby_sleep.contract` package defines the vendor-neutral data shapes that sit between any data provider (CSV, MCP, manual entry) and the sleep-reasoning layer.

All models are **Pydantic v2 `BaseModel`** subclasses.
Fields not marked "required" are optional (default `None` or an enum default).

Machine-readable source of truth — call from Python:

```python
from baby_sleep.contract.schema import export_json_schema

schema = export_json_schema()
# Returns a JSON Schema dict with $defs for every model.
# Root model: SleepLog. All nested types appear under $defs.
```

Or inspect the authoritative source directly:
- `baby_sleep/contract/models.py` — `Child`, `SleepSession`, `ContextEvent`, `SleepLog`
- `baby_sleep/contract/time_types.py` — `ApproxTime`, `TimePrecision`
- `baby_sleep/contract/enums.py` — all controlled vocabularies
- `baby_sleep/contract/schema.py` — `export_json_schema()`

---

## 2. `ApproxTime` — timestamps with uncertainty

All timestamps in the contract use `ApproxTime` rather than a bare `datetime`.
This preserves the distinction between a precisely logged time and an approximate or reconstructed one.

| Field | Type | Default | Description |
|---|---|---|---|
| `value` | `datetime` | required | Best-estimate point in time. Should be timezone-aware. |
| `precision` | `"exact"` \| `"approximate"` | `"exact"` | Whether the time is a precise log or an approximation. |
| `uncertainty_minutes` | `int` (≥ 0) | `0` | Symmetric uncertainty window in minutes. Zero when `precision = "exact"`. |
| `raw` | `str \| null` | `null` | Original string from the data source, for traceability. |

Computed properties (not serialized fields):
- `earliest` → `value − uncertainty_minutes`
- `latest` → `value + uncertainty_minutes`

When constructing `ApproxTime` from provider data, set `precision = "approximate"` and a non-zero `uncertainty_minutes` whenever the time is reconstructed, estimated, or manually entered.

---

## 3. `Child` — child profile

| Field | Type | Default | Description |
|---|---|---|---|
| `age_months` | `int \| null` | `null` | Chronological age in whole months. |
| `dob` | `date \| null` | `null` | Date of birth (`YYYY-MM-DD`). Alternative to `age_months`. |
| `gestational_age_at_birth_weeks` | `int \| null` | `null` | Gestational age at birth in weeks. Required for corrected-age calculation for preterm infants; omit for full-term (≥ 40 wk). |

At least one of `age_months` or `dob` should be populated for age-gated reasoning; all three fields are optional.

Helper method: `child.corrected_age_months()` returns the corrected age (adjusted for prematurity) or `None` if `age_months` is absent. Full-term (≥ 40 wk) or unknown gestation leaves the value unchanged.

---

## 4. `SleepSession` — a single sleep period

| Field | Type | Default | Description |
|---|---|---|---|
| `start` | `ApproxTime` | required | **Sleep onset** — when the child fell asleep. Canonical meaning is *asleep*, not put-down. |
| `end` | `ApproxTime \| null` | `null` | When the child woke. Null if ongoing or unknown. |
| `duration_minutes` | `int \| null` | `null` | Session length in minutes. Compute from start/end when absent. |
| `sleep_type` | `SleepType` | `"unknown"` | `"nap"`, `"night"`, or `"unknown"`. |
| `location` | `Location` | `"unknown"` | `"home"`, `"daycare"`, `"other"`, or `"unknown"`. |
| `start_marks` | `StartMarker` | `"unknown"` | What the logged `start` anchor represents: `"put_down"`, `"asleep"`, or `"unknown"`. |
| `onset_latency_minutes` | `int \| null` | `null` | Sleep-onset latency (SOL) in minutes. **Never** folded into `start`; stored separately. |
| `put_down_at` | `ApproxTime \| null` | `null` | Original put-down time when `start` has been shifted to represent sleep onset. |
| `self_settled` | `bool \| null` | `null` | Whether the child fell asleep without parental intervention. |
| `night_wakings` | `int \| null` | `null` | Count of night wakings during this session. |
| `data_quality` | `DataQuality` | `"logged"` | Fidelity of this record: `"logged"`, `"reported"`, or `"inferred"`. |
| `source` | `str` | `""` | Identifier for the data origin (e.g. `"huckleberry_csv"`, `"manual"`). |
| `notes` | `str \| null` | `null` | Free-text notes. |

### The put-down / asleep distinction

The canonical `start` represents sleep onset. Many trackers log the moment of put-down instead.
Adapters must set `start_marks` to indicate what the source timestamp actually represents.
When shifting the timestamp to represent sleep onset, preserve the original put-down time in `put_down_at` and record the shift in `onset_latency_minutes`.

---

## 5. `ContextEvent` — an ancillary event

Context events record feeds, diapers, medications, and similar events that may correlate with sleep patterns.

| Field | Type | Default | Description |
|---|---|---|---|
| `kind` | `EventKind` | required | `"feed"`, `"diaper"`, `"medication"`, `"pump"`, or `"other"`. |
| `at` | `ApproxTime` | required | When the event occurred. |
| `label` | `str \| null` | `null` | Optional human-readable tag. |
| `amount_ml` | `int \| null` | `null` | Volume in millilitres. Relevant for `"feed"` events; null otherwise. |
| `data_quality` | `DataQuality` | `"logged"` | Same vocabulary as `SleepSession`. |
| `source` | `str` | `""` | Data origin identifier. |
| `notes` | `str \| null` | `null` | Free-text notes. |

---

## 6. `SleepLog` — the top-level container

`SleepLog` is the root object passed to the reasoning layer. A provider returns (or the skill constructs) one `SleepLog`.

| Field | Type | Default | Description |
|---|---|---|---|
| `child` | `Child` | `Child()` | Child profile. An empty `Child()` is valid when no profile is available. |
| `sessions` | `list[SleepSession]` | `[]` | All sleep sessions in scope, ordered by `start`. |
| `events` | `list[ContextEvent]` | `[]` | All context events in scope. Empty list is valid. |
| `source` | `str` | `""` | Top-level data origin label. |
| `parsed_at` | `datetime \| null` | `null` | When this log was constructed or last updated. |

An empty `SleepLog()` (no sessions, no profile) is valid and represents the no-data starting point. The reasoning layer must handle it gracefully.

---

## 7. Controlled vocabularies

### `SleepType`
| Value | Meaning |
|---|---|
| `"nap"` | Daytime sleep |
| `"night"` | Overnight sleep |
| `"unknown"` | Not determined |

### `Location`
| Value | Meaning |
|---|---|
| `"home"` | Home environment |
| `"daycare"` | Childcare setting |
| `"other"` | Any other location |
| `"unknown"` | Not determined |

### `EventKind`
| Value | Meaning |
|---|---|
| `"feed"` | Feeding event |
| `"diaper"` | Diaper change |
| `"medication"` | Medication given |
| `"pump"` | Pumping session |
| `"other"` | Any other event kind |

### `DataQuality`
| Value | Meaning |
|---|---|
| `"logged"` | Recorded at the time by an app or device |
| `"reported"` | Recalled or estimated by a parent after the fact |
| `"inferred"` | Derived or **repaired** by the skill (e.g. a forgot-to-stop night truncated to the typical wake) — see "Data quality & repair" below |

### `StartMarker`
| Value | Meaning |
|---|---|
| `"put_down"` | The `start` timestamp is when the child was laid down |
| `"asleep"` | The `start` timestamp is actual sleep onset |
| `"unknown"` | Provenance not determined |

### `TimePrecision`
| Value | Meaning |
|---|---|
| `"exact"` | Precisely recorded timestamp |
| `"approximate"` | Estimated or reconstructed timestamp |

### Data quality & repair (D15)

Real logs are messy. The ingest layer (`normalize`) repairs the common defects **before**
analysis so they don't silently poison the per-child baseline — and **nothing is silent**:
every repair or drop is appended to the analyzer's `warnings` list, and repaired sessions
are re-marked `data_quality: "inferred"`.

| Defect | What the parent did | Repair | Marked |
|---|---|---|---|
| **No end & no duration** | Started a session, never recorded its length | Dropped (not analyzable) | warning |
| **Overlapping sessions** | Double-logged the same sleep | Contained one dropped; a partial overlap has its start trimmed to the earlier end | warning + `inferred` on the trimmed one |
| **Forgot-to-stop night** | Left a bedtime timer running past the real morning wake (a >13h "night") | End truncated to the child's typical morning wake (median of clean nights); if too few clean nights exist, the night is dropped instead of guessed | warning + `inferred` |

Two honesty consequences flow downstream:

- A session marked `inferred` is a **repair, not a measurement** — treat it as softer evidence.
- When more than ~25% of the **baseline** window is repaired, every emitted signal is capped
  at `medium` confidence with a "baseline includes repaired sessions" limitation. Do not
  present such signals as firm.

**Explaining a repair to a parent** (only if it's decision-relevant, and in plain language):
*"One night looked like the timer was left running — about 14 hours — so I treated it as a
normal night for her instead, which is why it's not throwing off the picture."* Never scold the
logging; the repair is a courtesy, not a correction of the parent. Thresholds here (13h, 25%,
≥3 clean nights) are **product heuristics**, not clinical rules.

---

## 8. Vendor-neutral boundary

The reasoning layer receives a `SleepLog` and must not depend on:

- Which data provider produced it.
- Vendor-specific field names, IDs, or terminology.
- Provider availability (the reasoning layer must handle an empty `SleepLog`).

Adapters (in `baby_sleep/ingest/`) are responsible for all normalization before the `SleepLog` is passed onward.
The reasoning layer's behavior must be identical regardless of data source; only `data_quality`, `uncertainty_minutes`, `source`, and `start_marks` differ by provenance.

---

## 9. Privacy note

Child sleep data is sensitive personal/family data.
Handle it accordingly even where a specific health-privacy law may not technically apply.
Do not log raw `SleepLog` payloads to unprotected outputs, and do not include real child data in fixtures or examples — use synthetic data.

---

## 10. Related files

| File | Purpose |
|---|---|
| `references/mcp-data-provider.md` | Provider integration guide: conceptual interface and mapping workflow |
| `baby_sleep/contract/models.py` | Authoritative model definitions (`Child`, `SleepSession`, `ContextEvent`, `SleepLog`) |
| `baby_sleep/contract/time_types.py` | `ApproxTime` and `TimePrecision` |
| `baby_sleep/contract/enums.py` | All controlled-vocabulary enums |
| `baby_sleep/contract/schema.py` | `export_json_schema()` — machine-readable JSON Schema |
| `baby_sleep/ingest/huckleberry.py` | Official Huckleberry CSV adapter (`HuckleberryCsvAdapter`, official export path only) |
| `baby_sleep/ingest/` | Generic CSV/JSON/manual-text adapters + `normalize()` |
