def test_package_imports():
    import importlib

    importlib.import_module("baby_sleep")
    importlib.import_module("baby_sleep.contract")
    importlib.import_module("baby_sleep.ingest")
    importlib.import_module("baby_sleep.store")
