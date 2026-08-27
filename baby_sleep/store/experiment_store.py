"""File-backed experiment/constraint store (D5/D21) + ephemeral session memory."""
from __future__ import annotations

import json
from pathlib import Path

from baby_sleep.contract.models import SleepLog
from baby_sleep.store.models import ChildProfile, Experiment, ExperimentStatus, SavedConstraint


class ExperimentStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._experiments = self.path / "experiments.json"
        self._constraints = self.path / "constraints.json"
        self._profile = self.path / "profile.json"

    def _load(self, file: Path) -> list[dict]:
        if not file.exists():
            return []
        return json.loads(file.read_text() or "[]")

    def _dump(self, file: Path, rows: list[dict]) -> None:
        file.write_text(json.dumps(rows, indent=2, default=str))

    # --- experiments ---
    def save_experiment(self, exp: Experiment) -> None:
        rows = [r for r in self._load(self._experiments) if r.get("id") != exp.id]
        rows.append(exp.model_dump(mode="json"))
        self._dump(self._experiments, rows)

    def get_experiment(self, exp_id: str) -> Experiment | None:
        for r in self._load(self._experiments):
            if r.get("id") == exp_id:
                return Experiment.model_validate(r)
        return None

    def list_experiments(self) -> list[Experiment]:
        return [Experiment.model_validate(r) for r in self._load(self._experiments)]

    def update_status(self, exp_id: str, status: ExperimentStatus) -> None:
        exp = self.get_experiment(exp_id)
        if exp is None:
            raise KeyError(exp_id)
        self.save_experiment(exp.model_copy(update={"status": status}))

    # --- constraints ---
    def save_constraint(self, constraint: SavedConstraint) -> None:
        rows = [r for r in self._load(self._constraints) if r.get("key") != constraint.key]
        rows.append(constraint.model_dump(mode="json"))
        self._dump(self._constraints, rows)

    def list_constraints(self) -> list[SavedConstraint]:
        return [SavedConstraint.model_validate(r) for r in self._load(self._constraints)]

    def get_constraint(self, key: str) -> SavedConstraint | None:
        for r in self._load(self._constraints):
            if r.get("key") == key:
                return SavedConstraint.model_validate(r)
        return None

    # --- child profile ---
    def save_profile(self, profile: ChildProfile) -> None:
        # Precedence invariant: an existing exact DOB is authoritative.
        # If a stored profile already has dob_precision == "exact" with a non-null dob,
        # an incoming profile that is missing a dob OR carries only an approximate one
        # must NOT clobber it — we preserve the stored exact dob and dob_precision while
        # still applying all other incoming fields (name, gestational_age_at_birth_weeks, …).
        existing = self.get_profile()
        if (
            existing is not None
            and existing.dob is not None
            and existing.dob_precision == "exact"
            and (profile.dob is None or profile.dob_precision != "exact")
        ):
            profile = profile.model_copy(update={"dob": existing.dob, "dob_precision": existing.dob_precision})
        self._profile.write_text(json.dumps(profile.model_dump(mode="json"), indent=2, default=str))

    def get_profile(self) -> ChildProfile | None:
        if not self._profile.exists():
            return None
        text = self._profile.read_text().strip()
        if not text:
            return None
        return ChildProfile.model_validate(json.loads(text))


class SessionMemory:
    """Holds the current conversation's SleepLog in memory ONLY. No persistence
    method for raw logs — encodes D21 (logs are ephemeral per conversation)."""
    def __init__(self) -> None:
        self._log: SleepLog = SleepLog()

    def set_log(self, log: SleepLog) -> None:
        self._log = log

    def get_log(self) -> SleepLog:
        return self._log
