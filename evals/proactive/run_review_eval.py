"""Deterministic review-level eval. For each case in review_cases/*.yaml, runs
scripts/analyze_sleep.py --review and asserts on the emitted review block.

Supported expect keys:
  status            exact match on review.status
  surfaced          exact list of surfaced signal names (order-insensitive)
  surfaced_contains signal names that MUST be surfaced
  must_not_surface  signal names that must NOT be surfaced
  also_noted_count  exact int
  steady_domains    exact set of steady domain keys (order-insensitive)

Exits 0 iff ALL cases pass.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
ANALYZE = REPO / "scripts" / "analyze_sleep.py"


def _run_case(case_path: Path, cases_dir: Path) -> tuple[bool, str]:
    case = yaml.safe_load(case_path.read_text())
    cid = case["case_id"]
    fixture = cases_dir.parent / case["fixture"]
    cmd = [
        sys.executable, str(ANALYZE),
        "--format", case["format"], "--input", str(fixture),
        "--age-months", str(int(case["age_months"])),
        "--review", "--as-of-date", str(case["as_of_date"]),
    ]
    if "review_window_days" in case:
        cmd += ["--review-window-days", str(int(case["review_window_days"]))]

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return False, f"FAIL [{cid}]: exit {result.returncode}: {result.stderr.strip()}"

    review = json.loads(result.stdout).get("review")
    if review is None:
        return False, f"FAIL [{cid}]: no review block in output"

    exp = case["expect"]
    surfaced = [s["signal"] for s in review.get("surfaced", [])]
    errs = []
    if "status" in exp and review["status"] != exp["status"]:
        errs.append(f"status {review['status']!r} != {exp['status']!r}")
    if "surfaced" in exp and set(surfaced) != set(exp["surfaced"]):
        errs.append(f"surfaced {sorted(surfaced)} != {sorted(exp['surfaced'])}")
    for name in exp.get("surfaced_contains", []):
        if name not in surfaced:
            errs.append(f"expected {name!r} surfaced; got {sorted(surfaced)}")
    for name in exp.get("must_not_surface", []):
        if name in surfaced:
            errs.append(f"{name!r} must not be surfaced")
    if "also_noted_count" in exp and review.get("also_noted_count") != exp["also_noted_count"]:
        errs.append(f"also_noted_count {review.get('also_noted_count')} != {exp['also_noted_count']}")
    if "steady_domains" in exp and set(review.get("steady_domains", [])) != set(exp["steady_domains"]):
        errs.append(f"steady_domains {sorted(review.get('steady_domains', []))} != {sorted(exp['steady_domains'])}")

    if errs:
        return False, f"FAIL [{cid}]:\n  " + "\n  ".join(errs)
    return True, f"PASS [{cid}]"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the review-level eval.")
    parser.add_argument("--cases-dir", type=Path,
                        default=REPO / "evals" / "proactive" / "review_cases")
    args = parser.parse_args(argv)
    cases_dir = args.cases_dir.resolve()
    case_files = sorted(cases_dir.glob("*.yaml"))
    if not case_files:
        print(f"No case files in {cases_dir}", file=sys.stderr)
        return 1
    all_pass = True
    for cf in case_files:
        try:
            ok, msg = _run_case(cf, cases_dir)
        except Exception as exc:  # noqa: BLE001
            ok, msg = False, f"FAIL [{cf.name}]: runner error: {exc}"
        print(msg)
        all_pass = all_pass and ok
    if all_pass:
        print(f"\nAll {len(case_files)} review cases passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
