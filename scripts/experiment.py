"""Thin CLI over baby_sleep.store: experiment state (D5) + saved constraints (D21)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from baby_sleep.store import settings as memory_settings
from baby_sleep.store.experiment_store import ExperimentStore
from baby_sleep.store.models import ChildProfile, Experiment, ExperimentStatus, SavedConstraint

# Commands that operate on the global memory preference (state root), not a child dir.
MEMORY_CMDS = {"memory-status", "enable-memory", "disable-memory"}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Experiment/constraint store CLI.")
    # Required for per-child commands; memory-* commands use --root instead.
    p.add_argument("--state-dir", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    sc = sub.add_parser("save-constraint")
    sc.add_argument("--key", required=True)
    sc.add_argument("--value", required=True)
    sc.add_argument("--note", default=None)

    gc = sub.add_parser("get-constraint")
    gc.add_argument("--key", required=True)

    sub.add_parser("list-constraints")

    se = sub.add_parser("save-experiment")
    for a in ("id", "hypothesis", "change", "metrics", "start-date"):
        se.add_argument(f"--{a}", required=True)
    se.add_argument("--review-after-days", type=int, required=True)

    sub.add_parser("list-experiments")

    us = sub.add_parser("update-status")
    us.add_argument("--id", required=True)
    us.add_argument("--status", required=True, choices=[s.value for s in ExperimentStatus])

    sp = sub.add_parser("save-profile")
    sp.add_argument("--name", default=None)
    sp.add_argument("--dob", default=None, metavar="YYYY-MM-DD")
    sp.add_argument("--dob-precision", default="exact", choices=["exact", "approximate"])
    sp.add_argument("--gestational-weeks", type=int, default=None)

    sub.add_parser("get-profile")

    sub.add_parser("clear-profile")
    sub.add_parser("clear-constraints")
    sub.add_parser("clear-experiments")
    sub.add_parser("clear-all")

    for mem_cmd in ("memory-status", "enable-memory", "disable-memory"):
        mp = sub.add_parser(mem_cmd)
        mp.add_argument("--root", default=None,
                        help="state root holding settings.json (default: ~/.lullsense)")

    args = p.parse_args(argv)

    # Memory preference commands operate on the state root, not a child dir.
    if args.cmd in MEMORY_CMDS:
        root = args.root  # None → module default (~/.lullsense)
        if args.cmd == "enable-memory":
            memory_settings.set_memory(True, root)
        elif args.cmd == "disable-memory":
            memory_settings.set_memory(False, root)
        print(json.dumps({"memory": "enabled" if memory_settings.memory_enabled(root) else "disabled"}))
        return 0

    if args.state_dir is None:
        print(json.dumps({"error": "--state-dir is required for this command"}), file=sys.stderr)
        return 1
    store = ExperimentStore(Path(args.state_dir))

    if args.cmd == "save-constraint":
        store.save_constraint(SavedConstraint(key=args.key, value=args.value, note=args.note))
        print(json.dumps({"saved": args.key}))
    elif args.cmd == "get-constraint":
        c = store.get_constraint(args.key)
        print(json.dumps(c.model_dump(mode="json") if c else None))
    elif args.cmd == "list-constraints":
        print(json.dumps([c.model_dump(mode="json") for c in store.list_constraints()]))
    elif args.cmd == "save-experiment":
        try:
            start = date.fromisoformat(args.start_date)
        except ValueError:
            print(json.dumps({"error": f"invalid --start-date: {args.start_date!r}, expected YYYY-MM-DD"}), file=sys.stderr)
            return 1
        exp = Experiment(id=args.id, hypothesis=args.hypothesis, change=args.change,
                         metrics=[m.strip() for m in args.metrics.split(",") if m.strip()],
                         start_date=start, review_after_days=args.review_after_days)
        store.save_experiment(exp)
        print(json.dumps(exp.model_dump(mode="json")))
    elif args.cmd == "list-experiments":
        print(json.dumps([e.model_dump(mode="json") for e in store.list_experiments()]))
    elif args.cmd == "update-status":
        try:
            store.update_status(args.id, ExperimentStatus(args.status))
        except KeyError:
            print(json.dumps({"error": f"experiment not found: {args.id}"}), file=sys.stderr)
            return 1
        print(json.dumps(store.get_experiment(args.id).model_dump(mode="json")))
    elif args.cmd == "save-profile":
        dob = None
        if args.dob is not None:
            try:
                dob = date.fromisoformat(args.dob)
            except ValueError:
                print(json.dumps({"error": f"invalid --dob: {args.dob!r}, expected YYYY-MM-DD"}), file=sys.stderr)
                return 1
        profile = ChildProfile(
            name=args.name,
            dob=dob,
            dob_precision=args.dob_precision,
            gestational_age_at_birth_weeks=args.gestational_weeks,
        )
        store.save_profile(profile)
        saved = store.get_profile()
        print(json.dumps(saved.model_dump(mode="json") if saved else None))
    elif args.cmd == "get-profile":
        profile = store.get_profile()
        print(json.dumps(profile.model_dump(mode="json") if profile is not None else None))
    elif args.cmd == "clear-profile":
        print(json.dumps({"cleared": {"profile": store.clear_profile()}}))
    elif args.cmd == "clear-constraints":
        print(json.dumps({"cleared": {"constraints": store.clear_constraints()}}))
    elif args.cmd == "clear-experiments":
        print(json.dumps({"cleared": {"experiments": store.clear_experiments()}}))
    elif args.cmd == "clear-all":
        print(json.dumps({"cleared": store.clear_all()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
