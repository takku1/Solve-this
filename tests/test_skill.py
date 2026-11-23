from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_skill_identity():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: solve-this" in text
    assert "# Solve This" in text
    assert "EXPERIMENT" in text


def test_references_exist():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for name in ("experiment-protocol", "result-template", "probe-patterns", "research-and-evidence", "worked-examples", "evaluation-scenarios", "sources", "research-foundations", "game-theory-and-design", "decision-policy"):
        assert (ROOT / "references" / f"{name}.md").is_file()
        assert f"references/{name}.md" in text


def test_install_identity():
    script = (ROOT / "install.ps1").read_text(encoding="utf-8")
    assert ".agents/skills/solve-this" in script
    assert ".claude/skills/solve-this" in script
    assert "skills/freestyle" not in script
