"""Research outcome semantics, persistence, exact experiments and real Lean checks."""
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples/hadamard/scripts"))
from math_research.constructions import (exact_hadamard, sylvester, synthesize,
                                         symmetry_key, instantiate, residuals)
from math_research.coverage import prime_power, derivation, coverage_report
from math_research.formal import check_proof, local_lean
from math_research.objective import HADAMARD, OBSERVATION_STATES
from math_research.planner import plan
from math_research.store import Project, ResearchError, digest
from math_research.workflow import seed, iterate


@pytest.fixture
def project(tmp_path):
    return Project.create(tmp_path / "research")


@pytest.mark.parametrize("state", sorted(OBSERVATION_STATES))
def test_every_intermediate_state_preserves_the_global_objective(project, state):
    project.source("s", "source", "https://example.test", "v1", "2026-11-23")
    claim = project.claim("trial", "candidate law", "bounded specified domain", sources=["s"])
    project.observe(claim, state, {"hypothetical_test_count": 10**9, "actual_execution": False})
    project.checkpoint(["universal existence"])
    snapshot = project.snapshot()
    assert snapshot["objective"] == HADAMARD
    assert snapshot["resolution"] == "UNRESOLVED"
    assert snapshot["session"] == "BUDGET_EXHAUSTED"


def test_observation_cannot_assert_a_proof_or_change_the_root(project):
    claim = project.claim("trial", "candidate law", "bounded domain")
    for state in ("LEMMA_PROVEN", "COVERAGE_EXPANDED", "CONJECTURE_PROVEN", "CONJECTURE_REFUTED"):
        with pytest.raises(ResearchError):
            project.observe(claim, state, {"passed": True})
    with pytest.raises(ResearchError):
        project.observe(HADAMARD["id"], "KNOWN_RESULT", {"examples": "all checked"})
    assert project.snapshot()["resolution"] == "UNRESOLVED"


def test_even_rehashed_initial_objective_drift_is_rejected(project):
    events = json.loads(project.path.read_text())
    events[0]["payload"]["statement"] = "construct H(4)"
    events[0]["hash"] = digest({key: events[0][key] for key in ("number", "previous", "kind", "payload")})
    project.path.write_text(json.dumps(events))
    with pytest.raises(ResearchError, match="immutable"):
        project.snapshot()


def test_claims_and_provenance_survive_restart_and_deduplicate(project):
    project.source("s", "known theorem", "https://example.test", "v1", "2026-11-23")
    first = project.claim("first", "known law", "exact scope", sources=["s"])
    project.observe(first, "KNOWN_RESULT", {"source": "s"})
    assert project.claim("different-id", "known law", "exact scope") == first
    before = project.path.read_bytes()
    reopened = Project.create(project.root)
    assert reopened.snapshot()["claims"][first]["status"] == "KNOWN_RESULT"
    assert reopened.path.read_bytes() == before
    with pytest.raises(ResearchError):
        reopened.claim("first", "a different law", "different scope")


def test_corruption_and_writer_collision_never_silently_restart(project):
    lock = project.root / "writer.lock"
    lock.write_text("another writer")
    with pytest.raises(ResearchError, match="writer"):
        project.checkpoint([])
    lock.unlink()
    events = json.loads(project.path.read_text())
    events[0]["hash"] = "0" * 64
    project.path.write_text(json.dumps(events))
    with pytest.raises(ResearchError, match="integrity"):
        Project.create(project.root)


def test_dangling_pending_write_does_not_replace_last_committed_history(project):
    (project.root / "pending-crashed.json").write_text("incomplete")
    assert Project.create(project.root).snapshot()["objective"] == HADAMARD


def test_dependency_cycles_and_missing_nodes_are_rejected_transactionally(project):
    a = project.claim("a", "law A", "all n")
    b = project.claim("b", "law B", "all n")
    project.link(a, b)
    with pytest.raises(ResearchError, match="Circular"):
        project.link(b, a)
    with pytest.raises(ResearchError, match="unknown"):
        project.link(a, "missing")
    assert project.blocked_dependencies(a) == [b]
    assert len(project.snapshot()["edges"]) == 1
    project.link(b, a, "may_support")  # feedback is not a proof dependency


def test_no_search_before_the_audit_and_program_are_adopted(project):
    with pytest.raises(ResearchError, match="audit"):
        iterate(project, proof_budget=0)
    seed(project)
    assert project.snapshot()["program"]
    assert len(plan(project)["branches"]) == 7
    assert "construction-parameter-existence" in project.blocked_dependencies("universal-family-coverage")


def test_exact_verifier_rejects_overflow_modular_and_non_sign_shortcuts():
    assert exact_hadamard(sylvester(16))
    assert not exact_hadamard(np.ones((256, 256), dtype=np.int8))
    assert not exact_hadamard([[1, 1], [1, 1]])
    assert not exact_hadamard([[1.0]])
    assert not exact_hadamard([[True]])
    assert not exact_hadamard([[1, 1]])


@pytest.mark.parametrize("q,expected", [(2, True), (9, True), (27, True), (12, False), (1, False)])
def test_prime_power_domains(q, expected):
    assert prime_power(q) is expected


def test_symbolic_coverage_distinguishes_model_gaps_from_mathematical_frontier():
    assert derivation(52)["rule"] == "paley-II"  # q=25, not a prime-only implementation
    report = coverage_report(100)
    assert 92 in report["window"]["uncovered_by_this_model"]  # 92 is known in the literature
    assert "least_closure" in report["symbolic_gap"]
    assert report["global_conjecture"] == "UNRESOLVED"
    with pytest.raises(ValueError):
        derivation(0)


def test_symbolic_grammar_rediscovers_law_and_falsifies_removed_hypothesis():
    result = synthesize(256)
    assert result["tested"] == 256
    assert result["state"] == "BRANCH_EXHAUSTED"
    assert result["global_resolution"] == "UNRESOLVED"
    assert any(c["novelty"].startswith("KNOWN_RESULT") for c in result["candidates"])
    assert all(not any(c["reduced_residuals"]) for c in result["candidates"])
    assert all(c["experiment"]["all_valid"] for c in result["candidates"])
    conditional = next(c for c in result["candidates"] if c["amicable"])
    witness = conditional["experiment"]["assumption_removal_counterexample"]
    assert exact_hadamard(witness["A"]) and exact_hadamard(witness["B"])
    assert not exact_hadamard(instantiate(conditional["cells"], witness["A"], witness["B"]))
    assert any(residuals(conditional["cells"]))


def test_symmetry_reduction_preserves_sylvester_control():
    a = (("A", 1), ("A", 1), ("A", 1), ("A", -1))
    b = (("B", -1), ("B", 1), ("B", -1), ("B", -1))
    assert symmetry_key(a) == symmetry_key(b)


def test_resume_reuses_attempts_in_another_process(project):
    seed(project)
    result = iterate(project, candidate_budget=16, proof_budget=0)
    before = project.path.read_bytes()
    proc = subprocess.run([sys.executable, "-B", str(ROOT / "examples/hadamard/scripts/research.py"),
                           "--project", str(project.root), "iterate", "--candidates", "16", "--proofs", "0"],
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    reopened = json.loads(proc.stdout)
    assert reopened["reused"]
    assert reopened["artifact"] == result["artifact"]
    assert project.path.read_bytes() == before
    assert reopened["resolution"] == "UNRESOLVED"


def test_absent_checker_and_admitted_or_custom_axiom_proofs_are_not_success(project):
    assert check_proof(project.root, "True", "by trivial", lean="not-an-installed-lean")["status"] == "CHECKER_UNAVAILABLE"
    for body in ("by sorry", "by admit", "by native_decide", "by trivial\naxiom invented : False"):
        assert not check_proof(project.root, "True", body)["verified"]
    assert project.snapshot()["resolution"] == "UNRESOLVED"


@pytest.mark.skipif(not local_lean(), reason="Pinned Lean unavailable")
def test_real_lean_proves_an_exact_lemma_but_not_the_hadamard_goal(project):
    node = project.claim("double", "integer doubling identity", "all integers", kind="lemma",
                         formal_type="∀ (n : Int), n+n = 2*n")
    receipt = project.certify(node, "by omega")
    assert receipt["verified"], receipt
    assert project.snapshot()["claims"][node]["status"] == "LEMMA_PROVEN"
    assert not project.resolve("prove", "by trivial")["verified"]
    assert not project.resolve("refute", "by trivial")["verified"]
    assert project.snapshot()["resolution"] == "UNRESOLVED"
    evidence = project.root / receipt["source"]
    evidence.write_text("changed")
    with pytest.raises(ResearchError, match="changed"):
        project.snapshot()


@pytest.mark.skipif(not local_lean(), reason="Pinned Lean unavailable")
def test_fake_global_pass_receipt_fails_independent_exact_statement_replay(project):
    receipt = check_proof(project.root, "True", "by trivial")
    assert receipt["verified"]
    forged = dict(receipt, formal_type="HadamardConjecture")
    project._append("resolution", {"direction": "prove", "receipt": forged})
    with pytest.raises(ResearchError, match="independent proof replay"):
        project.snapshot()


@pytest.mark.skipif(not local_lean(), reason="Pinned Lean unavailable")
def test_generated_conditional_gram_lemma_is_checked_by_real_lean(project):
    candidate = next(c for c in synthesize()["candidates"] if c["amicable"])
    receipt = check_proof(project.root, candidate["formal_type"], candidate["proof_body"])
    assert receipt["verified"], receipt
    assert "ab = ba" in receipt["formal_type"]
    assert project.snapshot()["resolution"] == "UNRESOLVED"


def test_unresolved_prerequisite_blocks_proof_promotion(project):
    prerequisite = project.claim("parameters", "supply all parameters", "universal")
    node = project.claim("family", "conditional identity", "universal", kind="lemma", formal_type="True")
    project.link(node, prerequisite)
    with pytest.raises(ResearchError, match="prerequisites"):
        project.certify(node, "by trivial")


def test_digest_bound_files_keep_exact_bytes_across_git_checkouts():
    paths = ["examples/hadamard/scripts/math_research/HadamardCore.lean", "research/hadamard/session/journal.json",
             "SKILL.md", "examples/hadamard/references/hadamard-program.md"]
    result = subprocess.run(["git", "check-attr", "text", "--", *paths], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    assert len(result.stdout.splitlines()) == len(paths)
    assert all(line.endswith(": text: unset") for line in result.stdout.splitlines())
