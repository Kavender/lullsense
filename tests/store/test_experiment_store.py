from datetime import date, datetime

from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.store.experiment_store import ExperimentStore, SessionMemory
from baby_sleep.store.models import ChildProfile, Experiment, ExperimentStatus, SavedConstraint


def test_experiment_defaults_to_proposed():
    e = Experiment(id="e1", hypothesis="bedtime too late", change="bedtime 30m earlier",
                   metrics=["sleep_onset_latency", "night_wakings"],
                   start_date=date(2026, 8, 25), review_after_days=7)
    assert e.status is ExperimentStatus.PROPOSED
    assert e.outcome is None
    assert "night_wakings" in e.metrics


def test_saved_constraint_roundtrips():
    c = SavedConstraint(key="daycare_nap_window", value="12:30-14:30", note="fixed by center")
    assert SavedConstraint.model_validate(c.model_dump()).value == "12:30-14:30"


def _exp():
    return Experiment(id="e1", hypothesis="h", change="c", metrics=["m"],
                      start_date=date(2026, 8, 25), review_after_days=7)


def test_store_persists_and_reloads(tmp_path):
    store = ExperimentStore(tmp_path / "state")
    store.save_experiment(_exp())
    # a fresh instance over the same path sees the saved data
    reloaded = ExperimentStore(tmp_path / "state")
    assert reloaded.get_experiment("e1").hypothesis == "h"
    assert [e.id for e in reloaded.list_experiments()] == ["e1"]


def test_store_updates_status(tmp_path):
    store = ExperimentStore(tmp_path / "state")
    store.save_experiment(_exp())
    store.update_status("e1", ExperimentStatus.ACTIVE)
    assert store.get_experiment("e1").status is ExperimentStatus.ACTIVE


def test_store_saves_constraints(tmp_path):
    store = ExperimentStore(tmp_path / "state")
    store.save_constraint(SavedConstraint(key="daycare_nap_window", value="12:30-14:30"))
    assert store.list_constraints()[0].key == "daycare_nap_window"


def test_store_reads_sleep_start_convention(tmp_path):
    # the per-family put-down-vs-asleep convention is just a SavedConstraint (D21)
    store = ExperimentStore(tmp_path / "state")
    store.save_constraint(SavedConstraint(key="sleep_start_convention", value="put_down"))
    assert store.get_constraint("sleep_start_convention").value == "put_down"
    assert store.get_constraint("missing") is None


def test_child_profile_roundtrip(tmp_path):
    store = ExperimentStore(tmp_path / "state")
    profile = ChildProfile(name="Ada", dob=date(2025, 2, 26), gestational_age_at_birth_weeks=38)
    store.save_profile(profile)
    # a fresh instance over the same path sees the saved data
    reloaded = ExperimentStore(tmp_path / "state")
    got = reloaded.get_profile()
    assert got is not None
    assert got.name == "Ada"
    assert got.dob == date(2025, 2, 26)
    assert got.gestational_age_at_birth_weeks == 38


def test_get_profile_empty_dir_returns_none(tmp_path):
    store = ExperimentStore(tmp_path / "empty")
    assert store.get_profile() is None


def test_per_child_state_separation(tmp_path):
    store_a = ExperimentStore(tmp_path / "child_a")
    store_b = ExperimentStore(tmp_path / "child_b")
    store_a.save_profile(ChildProfile(name="Alice", dob=date(2024, 1, 1)))
    store_b.save_profile(ChildProfile(name="Bob", dob=date(2023, 6, 15)))
    assert store_a.get_profile().name == "Alice"
    assert store_b.get_profile().name == "Bob"
    assert store_a.get_profile().dob != store_b.get_profile().dob


def test_session_memory_is_ephemeral():
    mem = SessionMemory()
    mem.set_log(SleepLog(sessions=[SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)))]))
    assert len(mem.get_log().sessions) == 1
    assert not hasattr(mem, "save")   # no persistence path for raw logs (D21)
