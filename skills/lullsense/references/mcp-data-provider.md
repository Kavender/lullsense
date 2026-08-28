# MCP / Data-Provider Integration Guide

> **Status: reference — loaded on demand by the skill.**
> Integrators building a data provider for the baby-sleep skill should read this document and `references/data-contract.md` together.

---

## 1. Skill-first design: no provider required

The skill works in full **no-data mode** using conversational intake alone.
A data provider is an optional enhancement that supplies structured historical logs; it is never a required dependency.

Priority order:

1. Safety and evidence provenance
2. Conversation-only usefulness ← **primary path**
3. Canonical data contract / provider integration ← **optional enhancement**

Do not gate any core reasoning on provider availability.

---

## 2. Conceptual provider interface

A compatible provider exposes three conceptual methods.
Actual tool or function names vary by implementation — the skill maps whatever names are available into the canonical schema.

### `get_child_profile()`

Returns a single child's age and optional birth metadata.

| Concept | Maps to | Notes |
|---|---|---|
| Age in months | `Child.age_months` | Integer. May be `null`/absent. |
| Date of birth | `Child.dob` | ISO date (`YYYY-MM-DD`). Alternative to age_months. |
| Gestational age at birth (weeks) | `Child.gestational_age_at_birth_weeks` | Integer. Required for corrected-age adjustment for preterm infants; optional for full-term (≥ 40 wk). |

If a multi-child provider is used, the skill must resolve which child is in scope before calling this method.

### `get_sleep_sessions(start_date, end_date)`

Returns a list of sleep sessions within the specified date range.

| Concept | Maps to | Notes |
|---|---|---|
| Sleep start timestamp | `SleepSession.start` (ApproxTime) | Canonical meaning: **asleep** (sleep onset). See §3 on the put-down/asleep distinction. |
| Sleep end timestamp | `SleepSession.end` (ApproxTime or null) | Null if session is ongoing or end is unknown. |
| Duration | `SleepSession.duration_minutes` | Integer minutes; optional. Compute from start/end when absent. |
| Sleep type | `SleepSession.sleep_type` | One of `"nap"`, `"night"`, `"unknown"`. |
| Location | `SleepSession.location` | One of `"home"`, `"daycare"`, `"other"`, `"unknown"`. |
| Self-settled flag | `SleepSession.self_settled` | Boolean or null. |
| Night wakings count | `SleepSession.night_wakings` | Integer or null. |
| Onset latency | `SleepSession.onset_latency_minutes` | Sleep-onset latency (SOL) in minutes. Never fold this into the start timestamp. |
| Data quality | `SleepSession.data_quality` | `"logged"` / `"reported"` / `"inferred"` — set based on source fidelity. |
| Source identifier | `SleepSession.source` | String; e.g. `"huckleberry_csv"`. |
| Notes | `SleepSession.notes` | Free-text; optional. |

### `get_context_events(start_date, end_date)` *(optional)*

Returns ancillary events (feeds, diapers, etc.) within the date range.
Providers may not supply this method; treat its absence gracefully.

| Concept | Maps to | Notes |
|---|---|---|
| Event kind | `ContextEvent.kind` | One of `"feed"`, `"diaper"`, `"medication"`, `"pump"`, `"other"`. |
| Event timestamp | `ContextEvent.at` (ApproxTime) | When the event occurred. |
| Label | `ContextEvent.label` | Optional human-readable tag. |
| Volume (feeding) | `ContextEvent.amount_ml` | Integer millilitres; null for non-feed events. |
| Data quality | `ContextEvent.data_quality` | Same vocabulary as SleepSession. |
| Source identifier | `ContextEvent.source` | String. |
| Notes | `ContextEvent.notes` | Free-text; optional. |

---

### Review-mode fetch

For a parent-initiated "review my recent sleep" (Phase 5), the skill requests **current** data on demand by calling `get_sleep_sessions(as_of − window, as_of)` — e.g. the last 14 days ending today. Nothing is persisted; the fetched log is analyzed ephemerally and discarded. If the provider returns nothing — or nothing recent — for that range, honor the §7 conversational fallback and do **not** present older data as if it were current. The freshness guard lives in `references/reasoning-framework.md` → "Review mode".

---

## 3. The put-down / asleep distinction

The canonical `SleepSession.start` represents **sleep onset** (when the child fell asleep), not put-down time.
Many trackers log put-down as the start event.

When adapting provider data:

- Set `SleepSession.start_marks` to `"put_down"` if the provider's timestamp is the moment the child was laid down.
- Set it to `"asleep"` if the provider distinguishes sleep onset.
- Set it to `"unknown"` when provenance is unclear.
- If the timestamp is shifted to represent sleep onset, preserve the original put-down time in `SleepSession.put_down_at`.
- Never fold onset latency into the start timestamp; store it separately in `SleepSession.onset_latency_minutes`.

This preserves data provenance and lets the reasoning layer apply appropriate uncertainty.

---

## 4. Approximate time handling

All timestamps in the canonical schema use `ApproxTime` rather than a bare `datetime`.
When a provider gives you a precise timestamp, set `precision = "exact"` and `uncertainty_minutes = 0`.
When the timestamp is approximate (e.g. reconstructed from a sleep window or entered manually), set `precision = "approximate"` and populate `uncertainty_minutes` with a reasonable bound.

```
ApproxTime {
    value:               datetime  # best-estimate point in time (UTC or timezone-aware)
    precision:           "exact" | "approximate"
    uncertainty_minutes: int       # ≥ 0; 0 when exact
    raw:                 str | null # original string from provider, for audit
}
```

The `raw` field is optional but strongly recommended for traceability.

---

## 5. Mapping workflow

1. **Discover** which provider tools or functions are available.
2. **Fetch** data for the requested date range.
3. **Normalize** every field into the canonical schema (see `references/data-contract.md`).
4. **Set provenance**: populate `source`, `data_quality`, `start_marks`, and `raw` as precisely as the provider allows.
5. **Pass** the resulting `SleepLog` to the reasoning layer; the reasoning layer must not access provider-specific fields or assumptions.

The reasoning layer is vendor-neutral by design. It must not contain code paths that behave differently based on which provider was used.

---

## 6. Huckleberry policy

> **Legal-sensitive. Review before any connector work.**

The following applies to the core project repository:

- The core project may document and support **Huckleberry's official CSV export** as an import path.
- **Do not** bundle login automation, credential handling, password storage, reverse-engineered API calls, or unofficial scraping code in this repository.
- **Do not** bundle or endorse any third-party MCP server that accesses Huckleberry via reverse-engineered or unofficial means.
- A user may independently configure a generic provider or MCP server that exposes their own tracker data through official means. Treat such a provider as an **external adapter**, not an endorsed dependency.
- Re-review Huckleberry's Terms of Use before adding any first-party connector. As of 2026-08-22, their terms prohibit reverse engineering and automated agents/scripts that generate automated searches, requests, queries, or that scrape/mine product data.
- Treat all child sleep data as **sensitive personal/family data** regardless of whether a specific health-privacy law technically applies in a given jurisdiction.

Official export documentation (starting point; verify currency):
- https://huckleberry.zendesk.com/hc/en-us/articles/4409286804627

---

## 7. No-data fallback

When no provider is available — or when provider data is absent for the relevant period — the skill falls back to conversational intake:

- Ask the parent to describe recent sleep patterns verbally.
- Treat verbally reported times as `ApproxTime` with `precision = "approximate"` and a non-zero `uncertainty_minutes`.
- Populate `data_quality = "reported"` for any session reconstructed from conversation.

The reasoning layer's logic must be identical regardless of data source; only the `data_quality` field and `uncertainty_minutes` differ.

---

## 8. Related files

| File | Purpose |
|---|---|
| `references/data-contract.md` | Canonical schema reference with field-level documentation |
| `baby_sleep/contract/models.py` | Authoritative Python model definitions |
| `baby_sleep/contract/schema.py` | `export_json_schema()` — machine-readable JSON Schema |
| `baby_sleep/ingest/huckleberry.py` | Official Huckleberry CSV adapter (`HuckleberryCsvAdapter`, official export only) |
| `baby_sleep/ingest/csv_generic.py` | Generic CSV adapter |
| `baby_sleep/ingest/json_generic.py` | Generic JSON adapter (`GenericJsonAdapter`) |
| `baby_sleep/ingest/manual_text.py` | Free-text manual entry parser (`parse_manual_text`) |
| `baby_sleep/ingest/normalize.py` | Canonicalizes a raw `SleepLog` (`normalize`) before analysis |
