from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "tests" / "content-contract.json"


def main() -> None:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    for relative, rule in payload["files"].items():
        path = ROOT / relative
        assert path.is_file(), f"missing file: {relative}"
        text = path.read_text(encoding="utf-8")
        for required in rule.get("required", []):
            assert required in text, f"{relative} missing required text: {required}"
        for forbidden in rule.get("forbidden", []):
            assert forbidden not in text, f"{relative} contains forbidden text: {forbidden}"
    print(f"PASS: {len(payload['files'])} content contracts")


if __name__ == "__main__":
    main()
