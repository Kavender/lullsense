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


# --- dob_precision tests (Task 6c) ---

def test_save_approximate_dob_roundtrips(tmp_path):
    store = ExperimentStore(tmp_path / "state")
    profile = ChildProfile(name="Baby", dob=date(2025, 2, 26), dob_precision="approximate")
    store.save_profile(profile)
    got = store.get_profile()
    assert got.dob == date(2025, 2, 26)
    assert got.dob_precision == "approximate"


def test_save_exact_dob_roundtrips(tmp_path):
    store = ExperimentStore(tmp_path / "state")
    profile = ChildProfile(name="Baby", dob=date(2025, 3, 1))  # default precision = "exact"
    store.save_profile(profile)
    got = store.get_profile()
    assert got.dob == date(2025, 3, 1)
    assert got.dob_precision == "exact"


def test_exact_dob_not_clobbered_by_approximate(tmp_path):
    """After an exact DOB is stored, saving a different approximate DOB preserves the exact one;
    but other fields (e.g. name) from the new save DO take effect."""
    store = ExperimentStore(tmp_path / "state")
    store.save_profile(ChildProfile(name="Baby", dob=date(2025, 3, 1), dob_precision="exact"))
    store.save_profile(ChildProfile(name="NewName", dob=date(2025, 1, 1), dob_precision="approximate"))
    got = store.get_profile()
    assert got.dob == date(2025, 3, 1), "exact DOB must survive an approximate save"
    assert got.dob_precision == "exact"
    assert got.name == "NewName", "name from the new save must take effect"


def test_exact_dob_preserved_when_dob_none(tmp_path):
    """After an exact DOB is stored, a name-only save (dob=None) must not clear the DOB."""
    store = ExperimentStore(tmp_path / "state")
    store.save_profile(ChildProfile(name="Baby", dob=date(2025, 3, 1), dob_precision="exact"))
    store.save_profile(ChildProfile(name="UpdatedName"))  # dob=None
    got = store.get_profile()
    assert got.dob == date(2025, 3, 1), "exact DOB must survive a name-only save"
    assert got.dob_precision == "exact"


def test_exact_dob_can_be_replaced_by_newer_exact(tmp_path):
    """A correction: saving a new explicit exact DOB replaces the old exact DOB."""
    store = ExperimentStore(tmp_path / "state")
    store.save_profile(ChildProfile(name="Baby", dob=date(2025, 3, 1), dob_precision="exact"))
    store.save_profile(ChildProfile(name="Baby", dob=date(2025, 3, 15), dob_precision="exact"))
    got = store.get_profile()
    assert got.dob == date(2025, 3, 15), "a new exact DOB must replace the old exact DOB"
    assert got.dob_precision == "exact"


def test_approximate_over_approximate_is_replaced(tmp_path):
    """Latest approximate wins when there's no exact DOB locked in."""
    store = ExperimentStore(tmp_path / "state")
    store.save_profile(ChildProfile(name="Baby", dob=date(2025, 2, 1), dob_precision="approximate"))
    store.save_profile(ChildProfile(name="Baby", dob=date(2025, 3, 1), dob_precision="approximate"))
    got = store.get_profile()
    assert got.dob == date(2025, 3, 1), "latest approximate should replace previous approximate"
    assert got.dob_precision == "approximate"


def test_partial_save_does_not_wipe_gestational_weeks(tmp_path):
    """A partial update (e.g. adding a name) must NOT wipe already-stored fields.

    Regression: gestational_age_at_birth_weeks feeds corrected-age math, which drives
    the <4mo safety tiering — silently reverting it to None on an incremental save
    could mis-tier a preterm infant near the 4-month boundary.
    """
    store = ExperimentStore(tmp_path / "state")
    store.save_profile(
        ChildProfile(dob=date(2025, 3, 1), dob_precision="exact", gestational_age_at_birth_weeks=34)
    )
    store.save_profile(ChildProfile(name="Alex"))  # partial: name only
    got = store.get_profile()
    assert got.name == "Alex", "the new name should be applied"
    assert got.gestational_age_at_birth_weeks == 34, "gestational weeks must survive a partial save"
    assert got.dob == date(2025, 3, 1), "exact dob must survive a partial save"
    assert got.dob_precision == "exact"


def test_partial_save_preserves_name_when_omitted(tmp_path):
    """A dob-only update must not wipe a previously-stored name."""
    store = ExperimentStore(tmp_path / "state")
    store.save_profile(ChildProfile(name="Sam", dob=date(2025, 1, 1), dob_precision="approximate"))
    store.save_profile(ChildProfile(dob=date(2025, 1, 5), dob_precision="exact"))  # no name
    got = store.get_profile()
    assert got.name == "Sam", "stored name must survive a dob-only save"
    assert got.dob == date(2025, 1, 5) and got.dob_precision == "exact"
