"""The portable build and real installer must select the same canonical bytes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import build, package_files, validate


@pytest.mark.parametrize("include_hadamard", [False, True])
def test_portable_build_is_complete_and_installs_identically(tmp_path, include_hadamard):
    output = tmp_path / "portable"
    manifest = build(output, include_hadamard)
    expected = {p.relative_to(ROOT).as_posix() for p in package_files(include_hadamard)}
    assert set(manifest["sources"]) == expected
    assert {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()} == expected | {"manifest.json"}
    if not include_hadamard:
        assert len(expected) == 6
        assert not any(n.startswith(("scripts/", "examples/", "docs/", "research/")) for n in expected)
    for name, record in manifest["sources"].items():
        data = (output / name).read_bytes()
        assert data == (ROOT / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
    profile = tmp_path / "profile"
    argv = ["powershell.exe", "-NoProfile", "-File", str(ROOT / "install.ps1"),
            "-Target", "both", "-UserRoot", str(profile)]
    if include_hadamard:
        argv.append("-IncludeHadamard")
    result = subprocess.run(argv, capture_output=True, encoding="utf-8", timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    for client in (".agents", ".claude"):
        installed = profile / client / "skills/solve-this"
        assert {p.relative_to(installed).as_posix() for p in installed.rglob("*") if p.is_file()} == expected
        for name in expected:
            assert (installed / name).read_bytes() == (output / name).read_bytes()
    if include_hadamard:
        script = profile / ".agents/skills/solve-this/examples/hadamard/scripts/research.py"
        args = [sys.executable, "-B", str(script), "--project", str(tmp_path / "project"), "init"]
        first = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=30)
        assert first.returncode == 0, first.stderr
        assert json.loads(first.stdout)["resolution"] == "UNRESOLVED"
        journal = tmp_path / "project/journal.json"
        before = journal.read_bytes()
        second = subprocess.run(args, capture_output=True, encoding="utf-8", timeout=30)
        assert second.returncode == 0, second.stderr
        assert journal.read_bytes() == before


def test_installer_preview_conflict_and_force_preserve_unrelated_files(tmp_path):
    profile = tmp_path / "profile"
    argv = ["powershell.exe", "-NoProfile", "-File", str(ROOT / "install.ps1"),
            "-Target", "codex", "-UserRoot", str(profile)]
    preview = subprocess.run(argv + ["-WhatIf"], capture_output=True, timeout=30)
    assert preview.returncode == 0 and not profile.exists()
    destination = profile / ".agents/skills/solve-this"
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text("local modification", encoding="utf-8")
    (destination / "notes.txt").write_text("preserve", encoding="utf-8")
    conflict = subprocess.run(argv, capture_output=True, timeout=30)
    assert conflict.returncode != 0
    assert (destination / "SKILL.md").read_text() == "local modification"
    assert not (destination / "agents").exists()
    updated = subprocess.run(argv + ["-Force"], capture_output=True, timeout=30)
    assert updated.returncode == 0
    assert (destination / "SKILL.md").read_bytes() == (ROOT / "SKILL.md").read_bytes()
    assert (destination / "notes.txt").read_text() == "preserve"


def test_existing_builds_and_source_directories_are_never_overwritten(tmp_path):
    output = tmp_path / "existing"
    output.mkdir()
    sentinel = output / "owned.txt"
    sentinel.write_text("preserve")
    for target in (output, ROOT, ROOT / "references/unsafe-output"):
        with pytest.raises(ValueError):
            build(target)
    assert sentinel.read_text() == "preserve"


def test_archived_builds_preserve_exact_historical_bytes():
    history = ROOT / "docs/history"
    records = json.loads((history / "package-builds.sha256.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(history / "package-builds.zip") as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(records)
        for name, digest in records.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest
    assert (history / "original/SKILL.md").is_file()


def test_all_selected_links_resolve():
    validate(package_files())
    validate(package_files(True))
