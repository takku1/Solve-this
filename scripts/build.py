"""Validate and package the single canonical skill without changing its bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def package_files(include_hadamard=False):
    files = [ROOT / "SKILL.md", ROOT / "agents/openai.yaml"]
    files += sorted((ROOT / "references").glob("*.md"))
    if include_hadamard:
        example = ROOT / "examples/hadamard"
        files += [p for p in sorted(example.rglob("*")) if p.is_file()
                  and "__pycache__" not in p.parts and p.suffix in {".md", ".py", ".json", ".lean"}]
    return files


def validate(files):
    from skillwren.validator.files import validate_fragment
    errors, warnings = validate_fragment(ROOT / "SKILL.md")
    if errors or warnings:
        raise ValueError("SkillWren diagnostics: " + repr(errors + warnings))
    expected = {p.resolve() for p in files}
    for path in files:
        if path.suffix != ".md":
            continue
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            if target not in expected:
                raise ValueError(f"Link outside selected package: {path.relative_to(ROOT)} -> {link}")


def build(out, include_hadamard=False):
    files = package_files(include_hadamard)
    validate(files)
    out = Path(out).resolve()
    # The source tree and existing outputs must never become build destinations.
    if out == ROOT or ROOT.is_relative_to(out) or out.exists():
        raise ValueError("Choose a new output directory outside existing package sources")
    protected = [ROOT / name for name in ("agents", "references", "scripts", "examples", "tests", "docs", "research", "investigations")]
    if any(out.is_relative_to(path) for path in protected):
        raise ValueError("Output must not be inside maintained sources or research evidence")
    out.mkdir(parents=True)
    sources = {}
    for path in files:
        name = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        assert target.read_bytes() == data
        sources[name] = {"sha256": hashlib.sha256(data).hexdigest()}
    manifest = {"format": "solve-this-package-1", "include_hadamard": include_hadamard, "sources": sources}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--include-hadamard", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.check_only:
            files = package_files(args.include_hadamard)
            validate(files)
            print(f"Checked canonical skill and {len(files)} selected files; zero SkillWren diagnostics")
        else:
            if args.out is None:
                parser.error("provide --out or --check-only")
            manifest = build(args.out, args.include_hadamard)
            print(f"Built and verified {len(manifest['sources'])} source files: {args.out.resolve()}")
        return 0
    except (ValueError, OSError, ImportError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
