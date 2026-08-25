from datetime import date
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
