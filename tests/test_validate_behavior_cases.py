from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR))
import validate_behavior_cases as validator  # noqa: E402


class BehaviorCaseStructureTests(unittest.TestCase):
    def test_rejects_body_text_that_only_mentions_a_required_field(self) -> None:
        case = """## case-{number}

- 用户请求：请解释“调用方式”字段的含义。
- 必须行为：提供解释。
- 禁止行为：不提供购买建议。
- 停止条件：解释完成后停止。
- 无 Skill 基线观察：待记录/未执行。
- 启用 Skill 后观察：待记录/未执行。
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cases.md"
            path.write_text(
                "# Synthetic behavior cases\n\n"
                + "\n".join(case.format(number=index) for index in range(14)),
                encoding="utf-8",
            )
            original = validator.CASE_FILES
            validator.CASE_FILES = (path,)
            try:
                with self.assertRaisesRegex(AssertionError, "调用方式"):
                    validator.main()
            finally:
                validator.CASE_FILES = original

    def test_accepts_bold_markdown_field_labels(self) -> None:
        case = """## case-{number}

- **调用方式**：自动（隐式）调用。
- **用户请求**：推荐一件商品。
- **必须行为**：提供建议。
- **禁止行为**：不提供购买操作。
- **停止条件**：建议完成后停止。
- **无 Skill 基线观察**：待记录/未执行。
- **启用 Skill 后的观察**：待记录/未执行。
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cases.md"
            path.write_text(
                "# Synthetic behavior cases\n\n"
                + "\n".join(case.format(number=index) for index in range(14)),
                encoding="utf-8",
            )
            original = validator.CASE_FILES
            validator.CASE_FILES = (path,)
            try:
                validator.main()
            finally:
                validator.CASE_FILES = original


if __name__ == "__main__":
    unittest.main()
