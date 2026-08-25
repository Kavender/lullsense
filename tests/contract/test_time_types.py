from datetime import datetime
import pytest
from baby_sleep.contract.time_types import ApproxTime, TimePrecision


def test_exact_time_has_zero_window():
    t = ApproxTime(value=datetime(2026, 8, 25, 19, 30))
    assert t.precision is TimePrecision.EXACT
    assert t.uncertainty_minutes == 0
    assert t.earliest == t.value == t.latest


def test_approximate_time_widens_window():
    t = ApproxTime(value=datetime(2026, 8, 25, 19, 0),
                   precision=TimePrecision.APPROXIMATE, uncertainty_minutes=15,
                   raw="around 7pm")
    assert t.earliest == datetime(2026, 8, 25, 18, 45)
    assert t.latest == datetime(2026, 8, 25, 19, 15)
    assert t.raw == "around 7pm"


def test_negative_uncertainty_rejected():
    with pytest.raises(ValueError):
        ApproxTime(value=datetime(2026, 8, 25, 19, 0), uncertainty_minutes=-5)
