"""Prepare/review or apply only the hash-pinned SkillWren discovery delta."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("Z:/SkillWren")
SOURCE = ROOT / "experiments/skillwren"
EVIDENCE = ROOT / "research/skillwren/change"
FILES = ["README.md", "src/skillwren/cli.py", "src/skillwren/finite_policy.py",
         "src/skillwren/policy_compression.py", "src/skillwren/policy_proof.py",
         "tests/test_policy_compression.py", "docs/current/design/finite-policy-compression.md",
         "examples/optimization/finite-policy.json"]
FILES += ["plugin/skillwren/lib/skillwren/" + name for name in
          ("cli.py", "finite_policy.py", "policy_compression.py", "policy_proof.py")]


def sha(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def read(path):
    return path.read_bytes() if path.exists() else None


def prepare():
    if EVIDENCE.exists():
        raise ValueError("review delta already exists; do not overwrite frozen evidence")
    records, patch = [], []
    for name in FILES:
        before, after = read(TARGET / name), (SOURCE / name).read_bytes()
        expected = None
        if name == "README.md":
            expected = (ROOT / "research/skillwren/README.before.md").read_bytes()
        elif name == "src/skillwren/cli.py":
            expected = (ROOT / "research/skillwren/cli.before.py").read_bytes()
        elif name == "plugin/skillwren/lib/skillwren/cli.py":
            expected = (ROOT / "research/skillwren/cli.before.py").read_bytes().replace(b"\r\n", b"\n")
        if before != expected:
            raise ValueError("target changed or unexpected existing file: " + name)
        records.append({"path": name, "before_sha256": sha(before), "after_sha256": sha(after)})
        patch.extend(difflib.unified_diff((before or b"").decode("utf-8").splitlines(True),
                     after.decode("utf-8").splitlines(True),
                     fromfile="a/" + name if before is not None else "/dev/null", tofile="b/" + name))
    EVIDENCE.mkdir(parents=True)
    for record in records:
        name = record["path"]
        for phase, data in (("after", (SOURCE / name).read_bytes()), ("before", read(TARGET / name))):
            if data is not None:
                destination = EVIDENCE / phase / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
    (EVIDENCE / "manifest.json").write_text(json.dumps({"target": str(TARGET), "files": records}, indent=2), encoding="utf-8")
    (EVIDENCE / "review.patch").write_bytes("".join(patch).encode("utf-8"))
    print(json.dumps({"prepared_files": len(records), "manifest": str(EVIDENCE / "manifest.json")}))


def apply():
    manifest = json.loads((EVIDENCE / "manifest.json").read_text(encoding="utf-8"))
    if manifest["target"] != str(TARGET) or [r["path"] for r in manifest["files"]] != FILES:
        raise ValueError("unexpected manifest scope")
    for record in manifest["files"]:
        path = TARGET / record["path"]
        if not path.resolve().is_relative_to(TARGET.resolve()):
            raise ValueError("path escapes target")
        if sha(read(path)) != record["before_sha256"]:
            raise ValueError("preflight conflict: " + record["path"])
        if sha((EVIDENCE / "after" / record["path"]).read_bytes()) != record["after_sha256"]:
            raise ValueError("review payload changed")
    for record in manifest["files"]:
        path = TARGET / record["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        pending = path.with_name(path.name + ".skillwren-discovery.pending")
        with pending.open("xb") as stream:
            stream.write((EVIDENCE / "after" / record["path"]).read_bytes())
        pending.replace(path)
    for record in manifest["files"]:
        if sha(read(TARGET / record["path"])) != record["after_sha256"]:
            raise ValueError("post-write hash mismatch")
    (EVIDENCE / "applied.json").write_text(json.dumps({"verified_files": manifest["files"]}, indent=2), encoding="utf-8")
    print(json.dumps({"applied_and_hash_verified": len(FILES), "target": str(TARGET)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    apply() if args.apply else prepare()
