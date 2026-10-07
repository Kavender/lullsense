"""`python -m baby_sleep.service`: JSON on stdin -> one JSON document on stdout; exit 0 on a
response, 1 on an error document. Nothing else is read, written or logged."""
import json
import sys
import warnings


def main() -> int:
    warnings.simplefilter("ignore")         # stderr stays empty
    try:
        from baby_sleep.service import run
        try:
            request = json.loads(sys.stdin.buffer.read())
        except ValueError:                  # bad JSON or bad UTF-8; message would echo input
            out = {"schemaVersion": 1, "error": "invalid_request", "fields": []}
        else:
            out = run(request)
    except Exception as e:  # noqa: BLE001
        out = {"schemaVersion": 1, "error": "internal", "type": type(e).__name__}
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.flush()
    return 1 if "error" in out else 0


if __name__ == "__main__":
    sys.exit(main())
