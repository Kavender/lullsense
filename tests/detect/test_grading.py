from baby_sleep.analyze.models import Confidence
from baby_sleep.detect.grading import (
    consistency,
    grade_confidence,
    grade_severity,
    grade_status,
)
from baby_sleep.detect.models import Severity, SignalStatus


def test_consistency_counts_direction_hits():
    # baseline 360; direction -1 (earlier). values 300,310,360,400 -> 2 of 4 below
    assert consistency([300.0, 310.0, 360.0, 400.0], 360.0, -1) == 0.5
    assert consistency([], 360.0, -1) == 0.0


def test_grade_severity_buckets():
    assert grade_severity(15, 20, 40) is Severity.MILD
    assert grade_severity(45, 20, 40) is Severity.SIGNIFICANT
    assert grade_severity(30, 20, 40) is Severity.MODERATE


def test_grade_status_threshold():
    assert grade_status(0.8) is SignalStatus.ESTABLISHED
    assert grade_status(0.4) is SignalStatus.EMERGING


def test_grade_confidence_levels():
    # strong magnitude + consistent + good baseline + low approx -> HIGH
    assert grade_confidence(-3.5, 0.9, Confidence.HIGH, 0.0) is Confidence.HIGH
    # moderate magnitude + moderately consistent -> MEDIUM
    assert grade_confidence(-1.8, 0.6, Confidence.MEDIUM, 0.2) is Confidence.MEDIUM
    # weak/inconsistent -> LOW
    assert grade_confidence(-1.6, 0.2, Confidence.LOW, 0.0) is Confidence.LOW
    # cap applies (context detector): HIGH capped down to MEDIUM
    assert grade_confidence(-3.5, 0.9, Confidence.HIGH, 0.0, cap=Confidence.MEDIUM) is Confidence.MEDIUM
    # None deviation_mads (mad==0 stable baseline) still gradable via consistency
    assert grade_confidence(None, 0.9, Confidence.HIGH, 0.0) in (Confidence.MEDIUM, Confidence.HIGH)
