"""Replay the retained engineering evidence without changing research claims."""
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "research/skillwren"


def main():
    manifest = json.loads((WORK / "change/manifest.json").read_text(encoding="utf-8"))
    for record in manifest["files"]:
        for path in (Path(manifest["target"]) / record["path"], WORK / "change/after" / record["path"]):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["after_sha256"], path
    from skillwren.policy_compression import verify
    source = json.loads((Path(manifest["target"]) / "examples/optimization/finite-policy.json").read_text(encoding="utf-8"))
    candidate = json.loads((WORK / "demo-v2/policy.json").read_text(encoding="utf-8"))
    certificate = json.loads((WORK / "demo-v2/certificate.json").read_text(encoding="utf-8"))
    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.33.1/bin/lean.exe"
    result = verify(certificate, source, candidate, lean)
    assert result["verified"] and result["strictly_smaller"]
    for name in ("target-tests", "installed-replay", "plugin-replay", "solve-this-regressions", "chili-v2-run"):
        assert json.loads((WORK / (name + ".txt.json")).read_text(encoding="utf-8"))["returncode"] == 0, name
    study = json.loads((WORK / "chili-v2/summary.json").read_text(encoding="utf-8"))
    assert study["result"]["generations"][0]["decision"] == "accepted_experimental"
    graph = json.loads((WORK / "proof-graph.json").read_text(encoding="utf-8"))
    assert graph["objective_sha256"] == hashlib.sha256((WORK / "OBJECTIVE.md").read_bytes()).hexdigest()
    assert graph["resolution"] == "UNRESOLVED"
    assert all(graph["nodes"][name]["status"] == "OPEN" for name in graph["required_open_dependencies"])
    print(json.dumps({"verified_applied_files": len(manifest["files"]), "certificate": result,
                      "original_objective": "UNRESOLVED"}, indent=2))


if __name__ == "__main__":
    main()
