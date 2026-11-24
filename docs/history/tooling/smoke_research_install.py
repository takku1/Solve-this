"""Exercise the real installer into a workspace-only profile, then run its CLI."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    profile = ROOT / "research/hadamard/install-smoke"
    project = ROOT / "research/hadamard/install-project"
    subprocess.run(["powershell.exe", "-NoProfile", "-File", str(ROOT / "install.ps1"),
                    "-Target", "codex", "-UserRoot", str(profile)], check=True, timeout=60)
    installed = profile / ".agents/skills/solve-this"
    expected = json.loads((ROOT / "discovery-review/source-hashes.json").read_text(encoding="utf-8"))
    for name, checksum in expected.items():
        assert hashlib.sha256((installed / name).read_bytes()).hexdigest() == checksum, name
    result = subprocess.run([sys.executable, "-B", str(installed / "scripts/research.py"),
                             "--project", str(project), "init"], capture_output=True,
                            encoding="utf-8", check=True, timeout=30)
    state = json.loads(result.stdout)
    assert state["resolution"] == "UNRESOLVED"
    history = (project / "journal.json").read_bytes()
    subprocess.run([sys.executable, "-B", str(installed / "scripts/research.py"),
                    "--project", str(project), "init"], capture_output=True,
                   encoding="utf-8", check=True, timeout=30)
    assert (project / "journal.json").read_bytes() == history
    record = {"profile": str(profile), "files_verified": len(expected),
              "installed_cli": "initialized and resumed knowledge successfully",
              "resolution": state["resolution"], "claims": state["claims"]}
    (ROOT / "research/hadamard/install-smoke.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
