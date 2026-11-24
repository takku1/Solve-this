"""Check ordering invariants; these tests do not establish agent compliance."""
from pathlib import Path

from skillwren.validator.files import validate_fragment

ROOT = Path(__file__).resolve().parents[1]


def test_main_skill_has_zero_static_diagnostics():
    errors, warnings = validate_fragment(ROOT / "SKILL.md")
    assert errors == [] and warnings == []


def assert_rejected(tmp_path, operation, marker, expected):
    original = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert original.count(operation) == 1
    changed = original.replace(operation, "", 1)
    start = changed.index("```logic")
    location = changed.index(marker, start)
    indent = len(marker) - len(marker.lstrip())
    moved = " " * indent + operation.lstrip()
    changed = changed[:location] + moved + changed[location:]
    path = tmp_path / "mutated.md"
    path.write_text(changed, encoding="utf-8")
    errors, _ = validate_fragment(path)
    assert any(e.rule == "P1" and expected in e.msg for e in errors), errors


def test_action_cannot_bypass_original_objective(tmp_path):
    assert_rejected(tmp_path, "    exec perform action {plan} from tools as evidence\n",
                    "  verify #objective ", "verify#objective")


def test_solved_return_cannot_bypass_verification(tmp_path):
    assert_rejected(tmp_path, "    return #solved verification as result\n",
                    "    verify #completion ", "verify#completion")


def test_suspension_cannot_bypass_checkpoint(tmp_path):
    assert_rejected(tmp_path, "  return #unresolved saved as result\n",
                    "  exec persist checkpoint ", "exec persist checkpoint")
