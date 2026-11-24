"""One-time consolidation; archive exact bytes before retiring duplicate builds."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    history = ROOT / "docs/history"
    if history.exists():
        raise SystemExit("History already exists; this migration is one-time")
    history.mkdir(parents=True)
    original = history / "original"
    for name in subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=ROOT, text=True).splitlines():
        if name in {"SKILL.md", "README.md"} or name.startswith("references/"):
            target = original / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(subprocess.check_output(["git", "show", "HEAD:" + name], cwd=ROOT))
    shutil.copyfile(ROOT / "SKILL.md", history / "mathematical-discovery-skill.md")
    shutil.copyfile(ROOT / "README.md", history / "mathematical-discovery-readme.md")
    shutil.copytree(ROOT / "references", history / "previous-references")
    names = ["solve-this", "solve-this-tuned", "solve-this-draft", "solve-this-discovery", "solve-this-discovery-draft",
             "discovery-review", "skillwren-review"]
    records = {}
    with zipfile.ZipFile(history / "package-builds.zip", "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            source = ROOT / name
            if not source.resolve().is_relative_to(ROOT) or source.is_symlink():
                raise ValueError("Unsafe migration source")
            for path in sorted(source.rglob("*")):
                if path.is_file():
                    relative = path.relative_to(ROOT).as_posix()
                    data = path.read_bytes()
                    archive.writestr(relative, data)
                    records[relative] = hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(history / "package-builds.zip") as archive:
        assert archive.testzip() is None
        for name, digest in records.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest
    (history / "package-builds.sha256.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    # Every recursive removal below is a named workspace directory whose exact
    # file bytes were just archived and read back successfully.
    for name in names:
        source = (ROOT / name).resolve()
        assert source.is_relative_to(ROOT) and source != ROOT
        shutil.rmtree(source)
    retired = history / "tooling"
    retired.mkdir()
    for name in ("build_discovery.py", "build_skillwren.py", "smoke_research_install.py",
                 "benchmark_skillwren_compression.py", "apply_skillwren_fixes.py",
                 "apply_skillwren_discovery.py", "check_skillwren_discovery.py"):
        shutil.move(str(ROOT / "scripts" / name), str(retired / name))
    example = ROOT / "examples/hadamard"
    (example / "scripts").mkdir(parents=True)
    (example / "references").mkdir()
    for name in ("research.py", "math_research", "export_research.py"):
        shutil.move(str(ROOT / "scripts" / name), str(example / "scripts" / name))
    for name in ("hadamard-audit.md", "hadamard-program.md"):
        shutil.move(str(ROOT / "references" / name), str(example / "references" / name))
    # The full previous reference set is retained in readable history above.
    for path in (ROOT / "references").glob("*.md"):
        path.unlink()
    print(json.dumps({"archived_build_files": len(records), "canonical_skill": "SKILL.md",
                      "optional_runtime": "examples/hadamard"}))


if __name__ == "__main__":
    main()
