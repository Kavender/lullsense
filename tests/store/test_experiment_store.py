from datetime import date, datetime

from baby_sleep.contract.models import SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.store.experiment_store import ExperimentStore, SessionMemory
from baby_sleep.store.models import Experiment, ExperimentStatus, SavedConstraint


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


def test_session_memory_is_ephemeral():
    mem = SessionMemory()
    mem.set_log(SleepLog(sessions=[SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 13, 0)))]))
    assert len(mem.get_log().sessions) == 1
    assert not hasattr(mem, "save")   # no persistence path for raw logs (D21)
