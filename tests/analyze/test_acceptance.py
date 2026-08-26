"""Phase 2 acceptance (spec §18): deterministic, tz-safe (naive local + midnight),
sparse degrades; age-gated; analyze depends only on contract."""
import ast
from datetime import date, datetime
from pathlib import Path

from baby_sleep.analyze import BaselineStatus, build_baseline, build_feature_series
from baby_sleep.contract.enums import SleepType
from baby_sleep.contract.models import Child, SleepLog, SleepSession
from baby_sleep.contract.time_types import ApproxTime
from baby_sleep.ingest.huckleberry import HuckleberryCsvAdapter
from baby_sleep.ingest.normalize import normalize

FIXTURE = Path(__file__).parent.parent / "fixtures" / "huckleberry_sample.csv"


def test_end_to_end_from_huckleberry_fixture_is_deterministic():
    log, _ = normalize(HuckleberryCsvAdapter().parse(FIXTURE.read_text()))
    s1 = build_feature_series(log)
    s2 = build_feature_series(log)
    assert s1.model_dump() == s2.model_dump()          # deterministic
    # the fixture's midnight-crossing night yields a night with duration preserved
    assert any(d.night_sleep_duration_min for d in s1.days)


def test_midnight_crossing_grouped_into_one_wake_day():
    # a single night 19:36 -> 06:00 next day is ONE wake-day's night, not two
    night = SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 19, 36)),
                         end=ApproxTime(value=datetime(2026, 8, 25, 6, 0)),
                         duration_minutes=624, sleep_type=SleepType.NIGHT)
    series = build_feature_series(SleepLog(sessions=[night]))
    assert len(series.days) == 1
    assert series.days[0].day == date(2026, 8, 25)
    assert series.days[0].night_sleep_duration_min == 624


def test_sparse_data_degrades_to_insufficient():
    night = SleepSession(start=ApproxTime(value=datetime(2026, 8, 24, 19, 36)),
                         end=ApproxTime(value=datetime(2026, 8, 25, 6, 0)),
                         duration_minutes=624, sleep_type=SleepType.NIGHT)
    series = build_feature_series(SleepLog(sessions=[night]))
    b = build_baseline(series, Child(age_months=10))
    assert b.status is BaselineStatus.INSUFFICIENT_DATA


def test_newborn_is_age_gated():
    sessions = [SleepSession(
        start=ApproxTime(value=datetime(2026, 9, 1 + i, 19, 30)),
        end=ApproxTime(value=datetime(2026, 9, 2 + i, 6, 0)),
        duration_minutes=630, sleep_type=SleepType.NIGHT) for i in range(10)]
    series = build_feature_series(SleepLog(sessions=sessions))
    b = build_baseline(series, Child(age_months=3))
    assert b.status is BaselineStatus.BELOW_SUPPORTED_RANGE
    # but descriptive features still computed
    assert len(series.days) == 10 and series.days[0].night_sleep_duration_min == 630


def test_analyze_imports_only_contract():
    root = Path(__file__).parent.parent.parent / "baby_sleep" / "analyze"
    for py in root.glob("*.py"):
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            mod = (node.module if isinstance(node, ast.ImportFrom) else None)
            names = ([a.name for a in node.names] if isinstance(node, ast.Import) else [])
            targets = ([mod] if mod else []) + names
            for t in targets:
                if t and t.startswith("baby_sleep."):
                    assert t.startswith(("baby_sleep.analyze", "baby_sleep.contract")), \
                        f"{py.name} imports {t} — analyze must depend only on contract"
