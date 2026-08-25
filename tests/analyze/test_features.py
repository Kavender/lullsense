from baby_sleep.analyze.models import BaselineStatus, Confidence
from baby_sleep.analyze.robust import iqr, mad, median


def test_robust_stats_basic():
    assert median([1, 2, 3, 4]) == 2.5
    assert median([]) is None
    # MAD of [1,2,3,4,100]: median=3, deviations=[2,1,0,1,97] -> median=1
    assert mad([1, 2, 3, 4, 100]) == 1
    assert mad([]) is None
    # IQR of 1..9 (Q3=7, Q1=3) -> 4
    assert iqr([1, 2, 3, 4, 5, 6, 7, 8, 9]) == 4
    assert iqr([]) is None


def test_enum_values_stable():
    assert {c.value for c in Confidence} == {"low", "medium", "high"}
    assert BaselineStatus.BELOW_SUPPORTED_RANGE.value == "below_supported_range"
