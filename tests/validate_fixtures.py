from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "routing-cases.json"
REQUIRED = {"id", "request", "invocation", "should_trigger", "expected_mode", "must_not", "rationale"}
MODES = {"recommend", "evaluate", "compare", "price-timing", "monitor", "none"}


def main() -> None:
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    cases = payload["cases"]
    assert cases, "cases must not be empty"
    ids: set[str] = set()
    covered: set[str] = set()
    has_positive = False
    has_negative = False
    has_explicit = False
    for case in cases:
        missing = REQUIRED - set(case)
        assert not missing, f"{case.get('id', '<unknown>')} missing {sorted(missing)}"
        assert case["id"] not in ids, f"duplicate id: {case['id']}"
        ids.add(case["id"])
        assert case["invocation"] in {"implicit", "explicit"}
        assert isinstance(case["should_trigger"], bool)
        assert case["expected_mode"] in MODES
        assert isinstance(case["must_not"], list)
        assert case["rationale"].strip()
        has_positive |= case["should_trigger"]
        has_negative |= not case["should_trigger"]
        has_explicit |= case["invocation"] == "explicit"
        if case["should_trigger"]:
            assert case["expected_mode"] != "none"
            covered.add(case["expected_mode"])
        else:
            assert case["expected_mode"] == "none"
    assert covered == MODES - {"none"}, f"missing modes: {sorted((MODES - {'none'}) - covered)}"
    assert has_positive and has_negative and has_explicit
    print(f"PASS: {len(cases)} routing cases")


if __name__ == "__main__":
    main()
