import copy
import itertools
import json

import pytest

from skillwren.finite_policy import FORMAT, RULES, audit, decisions, decision_certificate, evaluate, validate
from skillwren.policy_compression import compress, verify, rewrites


def policy(expr):
    return {"format": FORMAT, "scope": {"regime": "offline-test", "authority": "owner"},
            "variables": {name: {"type": "Bool", "role": role}
                          for name, role in (("approved", "obs"), ("write", "choice"), ("ready", "param"))},
            "constraint": expr, "objective": {"loss_domain": "declared actions only"},
            "rewrite_policy": {"allowed": sorted(RULES), "optimize": ["constraint"]}}


def test_compression_replays_and_executes():
    p = policy(["and", ["or", "approved", ["and", "approved", "write"]], True,
                ["not", ["not", "ready"]], ["or", "write", "write"]])
    result = compress(p, "bytes")
    c = result["certificate"]
    assert c["strictly_smaller"] and c["candidate_size"] < c["original_size"]
    assert verify(c, p, c["candidate"])["verified"]
    for approved, ready in itertools.product((False, True), repeat=2):
        obs = {"approved": approved, "ready": ready}
        assert decisions(p, obs) == decisions(c["candidate"], obs)
    assert c["decision_risk"]["verdict"] == "OPEN"


def test_roles_scope_objective_are_immutable():
    p = policy("approved")
    for key, value in (("scope", {}), ("objective", {"new": "goal"}),
                       ("variables", dict(p["variables"], write={"role": "obs", "type": "Bool"}))):
        q = copy.deepcopy(p)
        q[key] = value or {"changed": True}
        assert audit(p, q)["verdict"] == "REDESIGN"


def test_exclusive_inclusion_and_counterexample():
    p = policy("approved")
    assert audit(p, policy(["and", "approved", "write"]))["verdict"] == "CERTIFIED_TIGHTENING"
    assert audit(p, policy(["or", "approved", "write"]))["verdict"] == "CERTIFIED_RELAXATION"
    assert audit(p, policy(["not", "approved"]))["verdict"] == "REFUTED"
    assert audit(p, p)["verdict"] == "PROVEN_EQUIVALENT"
    assert decision_certificate(p, policy(True))["verdict"] == "OPEN"


def test_bounded_checks_never_sample_or_optimize_observations():
    p = policy("approved")
    with pytest.raises(ValueError, match="budget"):
        audit(p, p, max_worlds=4)
    for obs in ({"ready": True}, {"approved": 1, "ready": True},
                {"approved": True, "ready": True, "write": False}):
        with pytest.raises(ValueError):
            decisions(p, obs)


@pytest.mark.parametrize("expr", [["or"], ["eq", True, True], ["not", True, False], "missing", 1,
                                  {"let": "capture"}, ["and", "approved", {"python": "exec"}]])
def test_unsupported_expressions_fail_closed(expr):
    with pytest.raises(ValueError):
        validate(policy(expr))


def test_resume_is_exact_and_detects_tampering():
    p = policy(["and", ["not", ["not", "approved"]], True, True, "write"])
    first = compress(p, "bytes", 1)
    resumed = compress(p, "bytes", 10, history=first["history"])
    full = compress(p, "bytes", 11)
    assert resumed == full
    changed = copy.deepcopy(first["history"])
    changed["attempts"][0]["size"] = 0
    with pytest.raises(ValueError, match="replay"):
        compress(p, "bytes", history=changed)
    with pytest.raises(ValueError, match="objective"):
        compress(policy(False), "bytes", history=first["history"])


def test_fallback_and_denied_rewrites():
    p = policy(["and", "approved", "approved"])
    p["rewrite_policy"]["allowed"] = []
    c = compress(p, "bytes")["certificate"]
    assert not c["strictly_smaller"] and c["candidate"] == p
    assert verify(c, p, p)["verified"]


def test_certificate_cannot_attest_its_own_success():
    p = policy(["or", "approved", "approved"])
    c = compress(p, "bytes")["certificate"]
    for field, value in (("candidate_size", 0), ("derivation", []), ("candidate_sha256", "fake")):
        bad = copy.deepcopy(c)
        bad[field] = value
        with pytest.raises(ValueError):
            verify(bad, p, c["candidate"])
    bad = copy.deepcopy(c)
    bad["candidate"]["constraint"] = True
    with pytest.raises(ValueError):
        verify(bad, p, bad["candidate"])


def test_all_local_rules_against_independent_worlds():
    atoms = [True, False, "approved", "write", "ready"]
    inner = [[op, a, b] for op in ("and", "or") for a in atoms for b in atoms]
    expressions = [[op, a, b] for op in ("and", "or") for a in atoms + inner for b in atoms]
    expressions += [["not", ["not", x]] for x in atoms + inner]
    expressions += [["or", ["and", "approved", "write"], ["and", "approved", "ready"]]]
    for expr in expressions:
        for rule, changed in rewrites(expr, RULES):
            assert audit(policy(expr), policy(changed))["verdict"] == "PROVEN_EQUIVALENT", (rule, expr, changed)


def test_auxiliary_is_existential_and_parameters_fixed():
    p = policy(["and", "ready", ["or", "write", "approved"]])
    p["variables"]["approved"]["role"] = "aux"
    assert decisions(p, {"ready": True}) == [{"write": False}, {"write": True}]
    assert decisions(p, {"ready": False}) == []


def test_risk_bound_requires_feasible_decisions_in_every_context():
    total = policy(["or", ["not", "write"], ["and", "approved", "ready"]])
    assert decision_certificate(total, total)["deficiency_upper"] == "0"
    infeasible = policy(["and", "approved", "write"])
    assert decision_certificate(infeasible, infeasible)["verdict"] == "OPEN"


def test_cli_and_mutated_artifact(tmp_path):
    from skillwren.cli import dispatch
    p = policy(["and", "approved", "approved"])
    source, output = tmp_path / "source.json", tmp_path / "out"
    source.write_text(json.dumps(p), encoding="utf-8")
    assert dispatch(["skillwren", "compress", str(source), "--metric", "bytes", "--output", str(output)]) == 0
    argv = ["skillwren", "compress", str(source), "--verify", str(output / "certificate.json"),
            "--candidate", str(output / "policy.json")]
    assert dispatch(argv) == 0
    altered = json.loads((output / "policy.json").read_text())
    altered["constraint"] = False
    (output / "policy.json").write_text(json.dumps(altered))
    assert dispatch(argv) == 2


def test_formal_obligation_is_closed_and_injection_free():
    from skillwren.policy_proof import obligation
    p = policy(["and", "approved", "approved"])
    text = obligation(p, policy("approved"))
    assert "∀ (_v0 _v1 _v2 : Bool)" in text and "by decide" in text
    assert "sorry" not in text and "axiom " not in text
    with pytest.raises(ValueError):
        obligation(p, policy(False))


def test_real_lean_and_independent_receipt_replay():
    from pathlib import Path
    from skillwren.policy_proof import prove
    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.33.1/bin/lean.exe"
    if not lean.is_file():
        pytest.skip("pinned local Lean is unavailable")
    p = policy(["and", "approved", "approved"])
    c = compress(p, "bytes")["certificate"]
    c["formal"] = prove(p, c["candidate"], lean)
    assert verify(c, p, c["candidate"], lean)["verified"]
    with pytest.raises(ValueError, match="caller-trusted"):
        verify(c, p, c["candidate"])
    c["formal"]["source"] += "\n-- tampered"
    with pytest.raises(ValueError, match="replay"):
        verify(c, p, c["candidate"], lean)
