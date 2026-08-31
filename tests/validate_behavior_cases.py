from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CASE_FILES = (
    ROOT / "tests" / "behavior-cases" / "routing.md",
    ROOT / "tests" / "behavior-cases" / "decision-and-price.md",
    ROOT / "tests" / "behavior-cases" / "privacy-and-monitoring.md",
)
REQUIRED_FIELDS = {
    "调用方式": ("调用方式",),
    "用户请求": ("用户请求", "在全新对话中使用的用户请求"),
    "必须行为": ("必须行为", "必须观察到的行为"),
    "禁止行为": ("禁止行为", "禁止出现的行为"),
    "停止条件": ("停止条件",),
    "无 Skill 基线": ("无 Skill 基线观察", "未启用 Skill 的基线观察"),
    "启用 Skill 后观察": ("启用 Skill 后观察", "启用 Skill 后的观察"),
}


def case_blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (case-[^\n]+)$", text, flags=re.MULTILINE))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[match.end() : end]))
    return blocks


def is_field_line(line: str, labels: tuple[str, ...]) -> bool:
    prefix = r"^\s*(?:[-*+]\s+|\d+\.\s+)"
    for label in labels:
        escaped = re.escape(label)
        pattern = rf"{prefix}(?:{escaped}|\*\*{escaped}\*\*)\s*(?:：|:)"
        if re.match(pattern, line):
            return True
    return False


def main() -> None:
    total = 0
    for path in CASE_FILES:
        for case_id, block in case_blocks(path):
            total += 1
            for field, labels in REQUIRED_FIELDS.items():
                count = sum(is_field_line(line, labels) for line in block.splitlines())
                assert count == 1, f"{path.name}:{case_id} must contain exactly one {field} field"
    assert total == 14, f"expected 14 behavior cases, found {total}"
    print(f"PASS: {total} behavior case contracts")


if __name__ == "__main__":
    main()
