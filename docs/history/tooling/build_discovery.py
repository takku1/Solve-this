"""Package the discovery skill after checking its actual control flow and links."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skillwren-root", type=Path, default=ROOT.parent / "SkillWren")
    parser.add_argument("--out", type=Path, default=ROOT / "solve-this-discovery")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.out.exists() and not args.check_only:
        parser.error("Choose a new output directory; previous builds are retained.")
    launcher = args.skillwren_root / "skills/skillwren/scripts/skillwren.py"
    if not launcher.is_file():
        parser.error("Point --skillwren-root at the checked SkillWren source.")
    files = [ROOT / "SKILL.md", ROOT / "agents/openai.yaml", ROOT / "scripts/research.py"]
    files += sorted((ROOT / "references").glob("*.md"))
    files += [p for p in sorted((ROOT / "scripts/math_research").glob("*"))
              if p.suffix in {".py", ".lean", ".json"}]
    draft = ROOT / "solve-this-discovery-draft"
    draft.mkdir(exist_ok=True)
    expected = {p.relative_to(ROOT).as_posix() for p in files}
    for path in files:
        target = draft / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
    extras = [p for p in draft.rglob("*") if p.is_file() and ".skillwren" not in p.parts
              and "__pycache__" not in p.parts and p.relative_to(draft).as_posix() not in expected]
    if extras:
        raise ValueError(f"Unexpected draft files, inspect before packaging: {extras}")
    for path in draft.rglob("*.md"):
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" not in link and not link.startswith("#"):
                target = (path.parent / link.split("#")[0]).resolve()
                if not target.is_relative_to(draft) or not target.is_file():
                    raise ValueError(f"Unresolved package link in {path.name}: {link}")
    review = ROOT / "discovery-review"
    review.mkdir(exist_ok=True)

    def command(name, *arguments):
        result = subprocess.run([sys.executable, "-B", str(launcher.resolve()), *map(str, arguments)],
                                capture_output=True, encoding="utf-8", cwd=ROOT)
        (review / name).write_text(result.stdout + result.stderr, encoding="utf-8")
        if result.returncode:
            raise RuntimeError(f"SkillWren exited {result.returncode}: {review / name}")
        return result.stdout

    check = command("check.txt", "check", "--fragment", "--summary", "--audit", draft / "SKILL.md")
    if " warning " in check:
        raise RuntimeError("Inspect warnings before packaging")
    command("workflow.txt", "explain-workflow", "--fragment", draft / "SKILL.md")
    command("coverage.txt", "coverage", draft / "SKILL.md")
    command("coverage.json", "coverage", draft / "SKILL.md", "--json")
    (review / "source-hashes.json").write_text(json.dumps(
        {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        indent=2) + "\n", encoding="utf-8")
    if not args.check_only:
        command("build.txt", "build", draft, "--out", args.out.resolve())
        manifest = json.loads((args.out / "manifest.json").read_text(encoding="utf-8"))
        for name, item in manifest["sources"].items():
            assert hashlib.sha256((args.out / name).read_bytes()).hexdigest() == item["sha256"], name
        print(f"Built and read back {len(manifest['sources'])} files: {args.out.resolve()}")
    else:
        print("Discovery logic, links, workflow and coverage checked; no output replaced.")


if __name__ == "__main__":
    main()
