"""Run Chili Crisp's frozen identity-versus-certified-rewrite comparison.

The output is executable canonical policy JSON, never an opaque codec. This is
a measured local comparison of configured workloads, not a universal bound.
"""
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "research/skillwren/chili-v2"


DRIVER = '''import hashlib
import itertools
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from skillwren.finite_policy import canonical, decisions
from skillwren.policy_compression import compress, verify

fixtures = json.loads(Path("fixtures.json").read_text(encoding="utf-8"))
config = json.loads(Path("search-config.json").read_text())
policies = []
for fixture in fixtures:
    p = fixture["policy"]
    result = compress(p, "bytes", config["budget"])
    cert = result["certificate"]
    candidate = cert["candidate"]
    assert verify(cert, p, candidate)["verified"]
    for approved, ready in itertools.product((False, True), repeat=2):
        obs = {"approved": approved, "ready": ready}
        expected = [{"write": False}, {"write": True}] if approved and ready else [{"write": False}]
        assert decisions(candidate, obs) == expected
    policies.append(candidate)
Path("build").mkdir(exist_ok=True)
Path("build/policies.json").write_bytes(canonical(policies).encode("utf-8"))
print(hashlib.sha256(canonical([f["expected"] for f in fixtures]).encode()).hexdigest())
'''


def main():
    sys.path.insert(0, "Z:/chilicrisp")
    from chilicrisp import development as dev
    from chilicrisp.project import initialize
    if WORK.exists():
        raise SystemExit("Evidence directory exists; retain it and choose a new directory for a fresh experiment")
    baseline = WORK / "baseline"
    package = baseline / "src/skillwren"
    package.mkdir(parents=True)
    for name in ("finite_policy.py", "policy_compression.py"):
        shutil.copyfile(ROOT / "experiments/skillwren/src/skillwren" / name, package / name)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (baseline / "driver.py").write_text(DRIVER, encoding="utf-8")
    sys.path.insert(0, str(ROOT / "experiments/skillwren/tests"))
    sys.path.insert(0, str(ROOT / "experiments/skillwren/src"))
    from test_policy_compression import policy
    fixtures = []
    gate = ["or", ["not", "write"], ["and", "approved", "ready"]]
    for extra in (True, ["not", ["not", gate]], ["or", gate, ["and", gate, "write"]]):
        fixtures.append({"policy": policy(["and", gate, extra, ["or", gate, gate]]),
                         "expected": [[{"write": False}]] * 3 + [[{"write": False}, {"write": True}]]})
    (baseline / "fixtures.json").write_text(json.dumps(fixtures), encoding="utf-8")
    (baseline / "search-config.json").write_text('{"budget":0}', encoding="utf-8")
    project = initialize(baseline, [sys.executable, "-B", "driver.py"],
                         protected_paths=["driver.py", "fixtures.json", "src"])
    plan = {"schema_version": "0.1", "concept": "Reduce full executable finite-policy bytes with identical decisions",
            "project_config": str(project), "benchmark_command": [sys.executable, "-B", "driver.py"],
            "objective": "artifact_bytes", "artifact_paths": ["build/policies.json"],
            "regression_limits": {"wall_seconds": 5}, "reductions": [0.05],
            "repetitions": 3, "confirmation_repetitions": 3, "max_generations": 1, "seed": 31}
    planpath = WORK / "plan.json"
    planpath.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    session = WORK / "session"
    initial = dev.create(planpath, session, trusted_local=True)
    request = dev.request(session)
    (WORK / "request.json").write_text(json.dumps(request, indent=2), encoding="utf-8")
    candidate = WORK / "candidate"
    shutil.copytree(baseline, candidate)
    (candidate / "search-config.json").write_text('{"budget":128}', encoding="utf-8")
    research = {"hypothesis": "Authorized Boolean rewrites reduce redundant policy context",
                "mechanism": "Enable the audited rewrite search instead of the identity fallback",
                "falsification": "Any changed golden decision, metadata, failed audit or insufficient byte reduction",
                "sources": [{"reference": "https://arxiv.org/abs/2108.12099",
                             "supports": "Separate proposal incentives from independent verification; this is not PVG training"}]}
    researchpath = WORK / "research.json"
    researchpath.write_text(json.dumps(research, indent=2), encoding="utf-8")
    result = dev.submit(session, candidate, researchpath, trusted_local=True)
    summary = {"initial": initial, "result": result,
               "scope": "local measured bytes on three frozen finite-policy fixtures; no model-behavior claim"}
    (WORK / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
