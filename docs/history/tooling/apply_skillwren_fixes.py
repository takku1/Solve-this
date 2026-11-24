"""Preflight or apply the exact tested SkillWren field-investigation patch."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "investigations/skillwren"
CLONE = ROOT / "experiments/skillwren"
BASE = "a5d7d40fab57b90bad0d07bf736479ff23b70808"


def git(folder, *args):
    return subprocess.check_output(["git", "-C", str(folder), *map(str, args)])


def normalize(raw):
    return raw.replace(b"\r\n", b"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    if git(target, "rev-parse", "HEAD").decode().strip() != BASE:
        parser.error("Target HEAD differs from the tested baseline; review before applying.")
    names = git(CLONE, "diff", "--name-only", "HEAD").decode().splitlines()
    if not names:
        parser.error("No isolated changes to apply.")
    entries = {}
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            parser.error("Unexpected patch path.")
        baseline = git(CLONE, "show", f"{BASE}:{name}")
        current = (target / name).read_bytes()
        if normalize(current) != normalize(baseline):
            parser.error(f"Target has independent changes in {name}; leaving it untouched.")
        entries[name] = {"before_sha256": hashlib.sha256(current).hexdigest(),
                         "candidate_sha256": hashlib.sha256((CLONE / name).read_bytes()).hexdigest()}
    # Exact reviewed example bytes are restored only when normalization matches
    # the existing review. No digests or review decisions are regenerated.
    example = target / "examples/optimization"
    review = json.loads((example / "review.json").read_text(encoding="utf-8"))
    example_bytes = {}
    for name, key in (("original.md", "original_sha256"), ("SKILL.md", "logic_sha256")):
        raw = normalize((example / name).read_bytes())
        if hashlib.sha256(raw).hexdigest() != review[key]:
            parser.error(f"Reviewed example {name} has independent changes; refusing normalization.")
        example_bytes[name] = raw
    patch = REVIEW / "skillwren-fixes.patch"
    patch.write_bytes(git(CLONE, "diff", "--binary", "HEAD"))
    subprocess.run(["git", "-C", str(target), "apply", "--check", str(patch)], check=True)
    manifest = {"base": BASE, "target": str(target), "files": entries,
                "patch_sha256": hashlib.sha256(patch.read_bytes()).hexdigest(),
                "applied": False}
    if args.apply:
        subprocess.run(["git", "-C", str(target), "apply", str(patch)], check=True)
        for name, raw in example_bytes.items():
            (example / name).write_bytes(raw)
        for name, entry in entries.items():
            raw = (target / name).read_bytes()
            candidate = (CLONE / name).read_bytes()
            if normalize(raw) != normalize(candidate):
                raise RuntimeError(f"Readback differs from tested candidate: {name}")
            entry["after_sha256"] = hashlib.sha256(raw).hexdigest()
        manifest["applied"] = True
    path = REVIEW / ("applied-patch.json" if args.apply else "patch-preflight.json")
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"{'Applied and verified' if args.apply else 'Preflight passed for'} {len(entries)} files; "
          "reviewed LF example hashes preserved.")


if __name__ == "__main__":
    main()
