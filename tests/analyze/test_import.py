import importlib


def test_analyze_package_imports():
    importlib.import_module("baby_sleep.analyze")


def test_public_surface_exports():
    from baby_sleep.analyze import (
        build_baseline,
        segment_days,
    )
    assert callable(segment_days) and callable(build_baseline)
