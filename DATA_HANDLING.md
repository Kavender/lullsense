# Data handling

LullSense is designed to be useful from conversation alone, and to treat a child's
sleep and family details as sensitive. This document explains — plainly, without
reading the source — what the skill reads, what it keeps, where it keeps it, and how
to inspect or delete it.

**Short version:** LullSense keeps a small amount of local state on *your* machine so
it doesn't have to re-ask your child's age and daycare setup every session, and — if
you've connected a sleep-data provider — it can read your recent log to give a better
answer. It stores this locally only, never uploads it anywhere, never stores raw sleep
logs, tells you the first time it saves anything (and whenever it reads a connected
log), and lets you turn memory off at any time.

**Memory is on by default, disclosed, and revocable.** The first time LullSense saves
anything for your child, it tells you in one line — e.g. *"I'll remember her birthday
so you won't have to tell me next time — say the word if you'd rather I didn't."* You
can decline then or later; declining turns memory off, deletes what was saved, and is
remembered so it won't keep asking (see *Turning memory off* below).

---

## What LullSense can read

- **What you type in the conversation.** Your description of the last few nights is the
  primary input; no data source is ever required.
- **A sleep log you provide** — typed notes, a generic CSV/JSON, or an official
  Huckleberry CSV export — when you share one.
- **A connected sleep-data provider / MCP, if one is available.** When structured data
  would sharpen the answer (a review, a prediction, or data-enhanced reasoning) and you
  haven't already pasted a log, LullSense can pull your **recent** sleep itself rather
  than making you export by hand. When it does, **it says so in one short line**
  ("let me check your connected log…"). It detects a provider *by capability*
  (a tool that lists children / returns sleep history) and is **vendor-neutral** — it
  endorses no specific product and uses only official/first-party access, never
  unofficial scraping (see the Huckleberry policy in
  `skills/lullsense/references/mcp-data-provider.md §6`). If you tell it not to use the
  connected data, it stops for the session.

## What is session-only (never written to disk)

- **Raw sleep logs.** A log you paste, or data pulled from a provider, is analyzed
  **in memory for that conversation and then discarded.** LullSense never writes raw
  logs to disk. Baselines and signals are recomputed on demand, not cached.
- **Transient context** — a recent illness, teething, travel, a time-zone change, a
  developmental leap. Used to reason about *this* conversation; never persisted (it
  would go stale exactly like a frozen age).

## What is persisted locally (small, durable, on your machine only)

To avoid re-asking the same things every session, LullSense keeps a tiny per-child
profile:

- **Child profile** — name and a **date of birth** (so age is always derived and never
  goes stale), plus gestational age for preterm corrected-age math. If you only state an
  age ("my 15-month-old"), it anchors an *approximate* DOB; a real birthday you give
  later always supersedes it.
- **Durable constraints** you state — e.g. a fixed daycare nap window, pickup time,
  work start, room-sharing, your put-down-vs-asleep convention.
- **Experiment state** — the one small change you're trying and when to review it.

This is stored as plain JSON files, **on your own machine only**. Nothing is uploaded
to any server. LullSense has no backend.

### Where it's stored

By default, one directory per child under your home directory:

```
~/.lullsense/
    settings.json           # memory on/off preference (non-PII)
    <child-slug>/
        profile.json        # name, dob, dob_precision, gestational age
        constraints.json    # saved durable constraints
        experiments.json    # experiment state
```

A host application may point LullSense at a different location via `--state-dir`. Reading
a child that has no saved state yet creates nothing.

## Turning memory off (and back on)

Memory is on by default. To turn it off, just tell LullSense (e.g. "don't keep her
info"). It will stop saving, delete anything it saved this session, and remember your
choice so it won't ask again. The only thing kept for an opted-out user is a single
non-PII flag: `~/.lullsense/settings.json` → `{"memory": "disabled"}`.

With the optional engine you can also do this directly:

```
lullsense-experiment disable-memory     # turn memory off (remembered across sessions)
lullsense-experiment enable-memory      # turn it back on
lullsense-experiment memory-status      # check current setting
```

Or edit `~/.lullsense/settings.json` by hand. While memory is off, LullSense works
fully — it just re-establishes your child's details from the conversation each time
instead of remembering them.

## How to inspect or delete your data

- **Inspect:** open the JSON files above in any text editor, or run
  `lullsense-experiment --state-dir ~/.lullsense/<child> get-profile` /
  `list-constraints` / `list-experiments` (optional engine).
- **Delete one child:** remove that child's directory —
  `rm -r ~/.lullsense/<child-slug>/`.
- **Delete everything:** `rm -r ~/.lullsense/`.

There is no hidden copy elsewhere; deleting the directory removes the state.

## For contributors

- **Never commit real child data.** Use synthetic fixtures only, in tests, examples, and
  docs. Keep personally identifying details out of tracked files, filenames, commit
  messages, and PRs.
- Raw logs stay ephemeral by design — there is intentionally **no** persistence path for
  a `SleepLog` (see `SessionMemory` in `baby_sleep/store/experiment_store.py`).

---

*Status: public alpha. This describes current behavior; if it ever diverges from the
code, the code is the source of truth — please open an issue.*
