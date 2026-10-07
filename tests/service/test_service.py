"""CAM-12 P1: stateless analysis service — wire contract (P-wire), statelessness (P-state)
and version reporting (P-version)."""
import copy
import importlib.metadata
import json
import os
import subprocess
import sys
from datetime import date, datetime, timedelta

import pytest

from baby_sleep.service import SCHEMA_VERSION, run

SENTINEL = "ZZSENTINELZZ"


def _iso(d: date, h: int, m: int) -> str:
    return datetime(d.year, d.month, d.day, h, m).isoformat() + "+08:00"


def _request(nights: int = 10, op: str = "review", age: int | None = 9) -> dict:
    """``nights`` consecutive Asia/Shanghai nights ending the morning of 2026-10-07,
    each with one afternoon nap the day before."""
    records = []
    last = date(2026, 10, 7)
    for k in range(nights):
        wake_day = last - timedelta(days=nights - 1 - k)
        eve = wake_day - timedelta(days=1)
        records.append({
            "id": f"rec_n{k}", "kind": "night_sleep", "tz": "Asia/Shanghai",
            "start": _iso(eve, 19, 30), "end": _iso(wake_day, 6, 30 + k % 3),
            "startPrecision": "exact", "endPrecision": "exact",
            "wakings": [{"wokeAt": _iso(wake_day, 2, 0), "backAsleepAt": _iso(wake_day, 2, 20),
                         "unresolved": False}],
        })
        records.append({
            "id": f"rec_p{k}", "kind": "nap", "tz": "Asia/Shanghai",
            "start": _iso(eve, 13, 0), "end": _iso(eve, 14, 30),
            "startPrecision": "approx", "endPrecision": "exact", "wakings": [],
        })
    return {
        "schemaVersion": 1, "op": op, "asOf": "2026-10-07T21:30:00+08:00",
        "requestedWindowDays": None, "child": {"ageMonths": age}, "records": records,
    }


def _main(payload: str, cwd=None, env=None, flags=()) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", "-B", "-X", "utf8", *flags, "-m", "baby_sleep.service"],
        input=payload, capture_output=True, text=True, check=False, cwd=cwd, env=env)


# --- P-wire ---------------------------------------------------------------------------

def test_valid_request_computes_review_response():
    out = run(_request())
    assert out["schemaVersion"] == SCHEMA_VERSION == 1
    assert out["status"] == "computed", out.get("reason")
    assert out["status"] == out["review"]["status"]
    assert out["used"]["recordsReceived"] == 20
    # the first evening's nap is its own wake-day (2026-09-27), before the first night
    assert out["used"]["days"] == 11
    assert (out["used"]["firstDay"], out["used"]["lastDay"]) == ("2026-09-27", "2026-10-07")
    assert set(out["summary"]) == {
        "rise_time", "sleep_onset_time", "night_sleep_duration_min",
        "total_24h_sleep_min", "nap_count"}
    assert isinstance(out["baseline"], dict) and isinstance(out["signals"], list)
    assert out["fixes"] == [] and isinstance(out["warnings"], list)


@pytest.mark.parametrize("op, present, absent", [
    ("analyze", set(), {"signals", "review"}),
    ("detect", {"signals"}, {"review"}),
    ("review", {"signals", "review"}, set()),
])
def test_op_selects_sections(op, present, absent):
    out = run(_request(op=op))
    assert present <= out.keys() and not (absent & out.keys())
    assert out["status"] == (out["review"]["status"] if op == "review"
                             else out["baseline"]["status"])


def _mutate(path, value):
    req = _request(nights=2)
    node = req
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    return req


@pytest.mark.parametrize("req, field", [
    (_mutate(("records", 0, "start"), "2026-10-01T19:42:00"), "records.0.start"),   # naive
    (_mutate(("records", 0, "wakings", 0, "backAsleepAt"), "2026-10-02T02:20:00"),
     "records.0.wakings.0.backAsleepAt"),
    (_mutate(("records", 1, "id"), "rec_n0"), "records"),                            # dup id
    (_mutate(("records", 0, "id"), ""), "records.0.id"),
    (_mutate(("records", 0, "id"), "x" * 65), "records.0.id"),
    (_mutate(("records", 0, "tz"), "Mars/Olympus_Mons"), "records.0.tz"),
    (_mutate(("records", 0, "tz"), "../../etc/passwd"), "records.0.tz"),
    (_mutate(("records", 1, "wakings"),
             [{"wokeAt": "2026-10-05T13:30:00+08:00", "backAsleepAt": None,
               "unresolved": True}]), "records.1"),                                  # nap wakings
    (_mutate(("records", 0, "end"), "2026-10-05T19:30:00+08:00"), "records.0"),       # end == start
    (_mutate(("records", 0, "end"), "2026-10-05T18:00:00+08:00"), "records.0"),       # end < start
    (_mutate(("records", 0, "kind"), "unknown"), "records.0.kind"),
    (_mutate(("requestedWindowDays",), 29), "requestedWindowDays"),
    (_mutate(("child", "ageMonths"), 73), "child.ageMonths"),
    (_mutate(("child", "ageMonths"), True), "child.ageMonths"),
    (_mutate(("asOf",), 1_790_000_000), "asOf"),                                    # not ISO
    (_mutate(("op",), "predict"), "op"),
])
def test_invalid_request_reports_loc_paths_only(req, field):
    out = run(req)
    assert out["error"] == "invalid_request"
    assert field in out["fields"]
    assert set(out) == {"schemaVersion", "error", "fields"}


def test_too_many_records_rejected():
    req = _request(nights=1)
    one = req["records"][0]
    req["records"] = [{**one, "id": f"r{i}"} for i in range(401)]
    out = run(req)
    assert out["error"] == "invalid_request" and "records" in out["fields"]


def test_too_many_wakings_rejected():
    req = _request(nights=1)
    req["records"][0]["wakings"] = req["records"][0]["wakings"] * 21
    assert "records.0.wakings" in run(req)["fields"]


def test_unknown_keys_are_masked_in_loc():
    req = _request(nights=1)
    req["records"][0][SENTINEL] = 1
    req[SENTINEL + "top"] = 1
    out = run(req)
    assert out["error"] == "invalid_request"
    assert set(out["fields"]) == {"records.0.<extra>", "<extra>"}


@pytest.mark.parametrize("version", [2, 0, "1", None])
def test_unknown_schema_version_is_unsupported(version):
    req = _request(nights=1)
    req["schemaVersion"] = version
    assert run(req) == {"schemaVersion": 1, "error": "unsupported_schema"}


def test_non_object_request_is_invalid():
    assert run([1, 2])["error"] == "invalid_request"


def _all_sentinel_request() -> dict:
    s = SENTINEL
    rec = {k: s for k in ("id", "kind", "tz", "start", "end", "startPrecision", "endPrecision")}
    rec["wakings"] = [{"wokeAt": s, "backAsleepAt": s, "unresolved": s, s: s}]
    rec[s + "rec"] = s
    return {"schemaVersion": 1, "op": s, "asOf": s, "requestedWindowDays": s,
            "child": {"ageMonths": s, s + "child": s}, "records": [rec], s + "top": s}


def test_sentinel_in_every_field_never_echoed():
    proc = _main(json.dumps(_all_sentinel_request()))
    assert proc.returncode == 1
    assert SENTINEL not in proc.stdout and proc.stderr == ""
    out = json.loads(proc.stdout)
    assert out["error"] == "invalid_request"
    assert "records.0.<extra>" in out["fields"] and "<extra>" in out["fields"]


def test_main_success_exit_zero_and_quiet():
    proc = _main(json.dumps(_request()))
    assert proc.returncode == 0 and proc.stderr == ""
    assert json.loads(proc.stdout)["status"] == "computed"


def test_package_import_is_light_so_mains_guard_covers_heavy_imports():
    # `python -m baby_sleep.service` imports the package before __main__ runs; anything
    # it imports at module scope escapes __main__'s warnings filter and error mapping.
    code = ("import sys, baby_sleep.service; "
            "print(sorted(m for m in sys.modules if m.split('.')[0] in "
            "('pydantic', 'pydantic_core') or m.startswith('baby_sleep.') "
            "and m != 'baby_sleep.service'))")
    proc = subprocess.run([sys.executable, "-I", "-c", code],
                          capture_output=True, text=True, check=True)
    assert proc.stdout.strip() == "[]"


def test_main_stays_quiet_when_warnings_are_errors():
    proc = _main(json.dumps(_request()), flags=("-W", "error"))
    assert proc.returncode == 0 and proc.stderr == ""
    assert json.loads(proc.stdout)["status"] == "computed"


@pytest.mark.parametrize("payload, error", [
    ("{not json " + SENTINEL, "invalid_request"),
    ("", "invalid_request"),
    (json.dumps({"schemaVersion": 7, "x": SENTINEL}), "unsupported_schema"),
])
def test_main_handled_errors_exit_one_and_quiet(payload, error):
    proc = _main(payload)
    assert proc.returncode == 1 and proc.stderr == ""
    assert json.loads(proc.stdout)["error"] == error
    assert SENTINEL not in proc.stdout


def test_internal_error_maps_to_type_only(monkeypatch):
    from baby_sleep.service import api

    def boom(*_a, **_k):
        raise RuntimeError(SENTINEL)
    monkeypatch.setattr(api, "build_feature_series", boom)
    out = run(_request())
    assert out == {"schemaVersion": 1, "error": "internal", "type": "RuntimeError"}


# --- P-state --------------------------------------------------------------------------

_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
_FORBIDDEN_PREFIXES = ("os.mkdir", "os.remove", "os.rmdir", "os.rename", "shutil.", "socket.")
_audit = {"on": False, "hits": []}


def _hook(event, args):
    if not _audit["on"]:
        return
    if event == "open":
        mode, flags = args[1], args[2]
        writes = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (
            mode is None and isinstance(flags, int) and flags & _WRITE_FLAGS)
        if writes:
            _audit["hits"].append((event, args))
    elif event.startswith(_FORBIDDEN_PREFIXES):
        _audit["hits"].append((event, args))


sys.addaudithook(_hook)   # cannot be removed; gated by _audit["on"]


def test_run_writes_nothing_and_opens_no_sockets():
    req = _request()
    run(copy.deepcopy(req))          # warm-up: first-use imports may write .pyc files
    _audit["hits"].clear()
    _audit["on"] = True
    try:
        run(req)
        run({"schemaVersion": 1})    # handled-error path too
    finally:
        _audit["on"] = False
    assert _audit["hits"] == []


def test_main_leaves_cwd_home_and_tmpdir_empty(tmp_path):
    dirs = {name: tmp_path / name for name in ("cwd", "home", "tmp")}
    for d in dirs.values():
        d.mkdir()
    env = {"HOME": str(dirs["home"]), "TMPDIR": str(dirs["tmp"])}
    for payload in (json.dumps(_request()), json.dumps({"schemaVersion": 1}), "garbage"):
        proc = _main(payload, cwd=dirs["cwd"], env=env)
        assert proc.stderr == ""
    assert all(list(d.iterdir()) == [] for d in dirs.values())


# --- P-version ------------------------------------------------------------------------

def test_service_version_is_installed_package_version():
    version = run(_request(nights=1))["serviceVersion"]
    assert version == importlib.metadata.version("lullsense")
    assert version.startswith("0.3.")


def test_empty_records_report_null_first_and_last_day():
    req = _request(nights=1)
    req["records"] = []
    used = run(req)["used"]
    assert used == {"recordsReceived": 0, "sessionsAnalyzed": 0, "days": 0,
                    "firstDay": None, "lastDay": None}
