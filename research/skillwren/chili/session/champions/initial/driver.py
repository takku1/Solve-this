import hashlib
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
        expected = [{"write": True}] if approved and ready else []
        assert decisions(candidate, obs) == expected
    policies.append(candidate)
Path("build").mkdir(exist_ok=True)
Path("build/policies.json").write_bytes(canonical(policies).encode("utf-8"))
print(hashlib.sha256(canonical([f["expected"] for f in fixtures]).encode()).hexdigest())
