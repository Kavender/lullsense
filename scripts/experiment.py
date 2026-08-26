"""Thin CLI over baby_sleep.store: experiment state (D5) + saved constraints (D21)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from baby_sleep.store.experiment_store import ExperimentStore
from baby_sleep.store.models import Experiment, ExperimentStatus, SavedConstraint


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Experiment/constraint store CLI.")
    p.add_argument("--state-dir", required=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    sc = sub.add_parser("save-constraint")
    sc.add_argument("--key", required=True)
    sc.add_argument("--value", required=True)
    sc.add_argument("--note", default=None)

    gc = sub.add_parser("get-constraint")
    gc.add_argument("--key", required=True)

    se = sub.add_parser("save-experiment")
    for a in ("id", "hypothesis", "change", "metrics", "start-date"):
        se.add_argument(f"--{a}", required=True)
    se.add_argument("--review-after-days", type=int, required=True)

    sub.add_parser("list-experiments")

    us = sub.add_parser("update-status")
    us.add_argument("--id", required=True)
    us.add_argument("--status", required=True, choices=[s.value for s in ExperimentStatus])

    args = p.parse_args(argv)
    store = ExperimentStore(Path(args.state_dir))

    if args.cmd == "save-constraint":
        store.save_constraint(SavedConstraint(key=args.key, value=args.value, note=args.note))
        print(json.dumps({"saved": args.key}))
    elif args.cmd == "get-constraint":
        c = store.get_constraint(args.key)
        print(json.dumps(c.model_dump(mode="json") if c else None))
    elif args.cmd == "save-experiment":
        exp = Experiment(
            id=args.id,
            hypothesis=args.hypothesis,
            change=args.change,
            metrics=args.metrics.split(","),
            start_date=date.fromisoformat(args.start_date),
            review_after_days=args.review_after_days,
        )
        store.save_experiment(exp)
        print(json.dumps(exp.model_dump(mode="json")))
    elif args.cmd == "list-experiments":
        print(json.dumps([e.model_dump(mode="json") for e in store.list_experiments()]))
    elif args.cmd == "update-status":
        store.update_status(args.id, ExperimentStatus(args.status))
        print(json.dumps(store.get_experiment(args.id).model_dump(mode="json")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
