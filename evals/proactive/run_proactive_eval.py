"""Deterministic proactive eval runner.

For each case in cases/*.yaml, runs scripts/analyze_sleep.py on the fixture,
parses the emitted signals, and asserts that:
  - every expected_signal is present in the output
  - every must_not_flag signal is absent from the output

Exits 0 iff ALL cases pass; non-zero otherwise.

Usage:
    python evals/proactive/run_proactive_eval.py [--cases-dir PATH]
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
    with case_path.open() as f:
        case = yaml.safe_load(f)

    case_id = case["case_id"]
    fixture_rel = case["fixture"]
    fmt = case["format"]
    age_months = int(case["age_months"])
    expected = set(case.get("expected_signals", []))
    must_not = set(case.get("must_not_flag", []))

    # Resolve fixture relative to the parent of cases_dir (i.e. evals/proactive/)
    fixture_path = cases_dir.parent / fixture_rel

    result = subprocess.run(
        [
            sys.executable,
            str(ANALYZE),
            "--format", fmt,
            "--input", str(fixture_path),
            "--age-months", str(age_months),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return False, (
            f"FAIL [{case_id}]: analyze_sleep.py exited {result.returncode}:\n"
            f"  stdout: {result.stdout.strip()}\n"
            f"  stderr: {result.stderr.strip()}"
        )

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return False, f"FAIL [{case_id}]: JSON parse error: {exc}"

    present = {s["signal"] for s in data.get("signals", [])}

    missing = expected - present
    forbidden = must_not & present

    if not missing and not forbidden:
        return True, f"PASS [{case_id}]"

    lines = [f"FAIL [{case_id}]:"]
    lines.append(f"  actual signals:   {sorted(present)}")
    if missing:
        lines.append(f"  expected (absent): {sorted(missing)}")
    if forbidden:
        lines.append(f"  must_not_flag (present): {sorted(forbidden)}")
    return False, "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic proactive eval over the analysis CLI."
    )
    parser.add_argument(
        "--cases-dir",
        type=Path,
        default=REPO / "evals" / "proactive" / "cases",
        help=(
            "Directory containing case YAML files; each case's `fixture:` path is"
            " resolved relative to this directory's parent."
        ),
    )
    args = parser.parse_args(argv)

    cases_dir: Path = args.cases_dir.resolve()
    case_files = sorted(cases_dir.glob("*.yaml"))

    if not case_files:
        print(f"No case files found in {cases_dir}", file=sys.stderr)
        return 1

    all_pass = True
    for case_file in case_files:
        try:
            passed, message = _run_case(case_file, cases_dir)
        except Exception as exc:  # noqa: BLE001
            passed = False
            message = f"FAIL [{case_file.name}]: runner error: {exc}"
        print(message)
        if not passed:
            all_pass = False

    if all_pass:
        print(f"\nAll {len(case_files)} cases passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
