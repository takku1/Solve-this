"""One persistent research iteration with exact evidence and resumable limits."""
import hashlib
import json
from pathlib import Path

from .constructions import synthesize
from .objective import HADAMARD
from .store import Project, ResearchError, canonical, digest


def seed(project):
    data = json.loads(Path(__file__).with_name("seed.json").read_text(encoding="utf-8"))
    for source in data["sources"]:
        project.source(**{("ident" if k == "id" else k): value for k, value in source.items()})
    for item in data["known"]:
        ident = project.claim(kind="known", **{("ident" if k == "id" else k): value for k, value in item.items()})
        if project.snapshot()["claims"][ident]["status"] == "UNRESOLVED":
            project.observe(ident, "KNOWN_RESULT", {"sources": item["sources"], "local_proof": False})
    for item in data["obligations"]:
        ident = project.claim(**{("ident" if k == "id" else k): value for k, value in item.items()})
        project.link(HADAMARD["id"], ident, "may_support")
    project.link("universal-family-coverage", "construction-parameter-existence")
    project.link("universal-legendre-pairs", "legendre-to-hadamard", "may_support")
    references = Path(__file__).resolve().parents[2] / "references"
    project.adopt_program((references / "hadamard-audit.md").read_bytes(),
                          (references / "hadamard-program.md").read_bytes())
    return project.snapshot()


def iterate(project, candidate_budget=256, proof_budget=2, lean=None, fresh_reason=None):
    if type(proof_budget) is not int or not 0 <= proof_budget <= 8:
        raise ResearchError("Proof budget must be an integer between 0 and 8")
    state = project.snapshot()
    if not state["program"]:
        raise ResearchError("Adopt a literature audit and measurable research program before search")
    engine = hashlib.sha256(Path(__file__).with_name("constructions.py").read_bytes()).hexdigest()
    key = digest({"engine": engine, "candidate_budget": candidate_budget, "proof_budget": proof_budget})
    if not fresh_reason:
        for attempt in reversed(state["attempts"]):
            if attempt.get("run_key") == key:
                path = project.root / attempt["artifact"]
                if hashlib.sha256(path.read_bytes()).hexdigest() != attempt["artifact_sha256"]:
                    raise ResearchError("Archived attempt changed; do not silently rediscover it")
                return {"reused": True, "artifact": attempt["artifact"],
                        "resolution": state["resolution"], "session": state["session"]}
    if state["session"] == "BUDGET_EXHAUSTED":
        project.resume()
    report = synthesize(candidate_budget)
    report["objective_hash"] = state["objective_hash"]
    report["engine_sha256"] = engine
    report["fresh_reason"] = fresh_reason
    receipts = []
    for candidate in report["candidates"]:
        ident = "block-" + candidate["id"]
        sources = ["sylvester"] if candidate["novelty"].startswith("KNOWN_RESULT") else []
        # Claim provenance names source records, not theorem ids.
        source_ids = ["sage-hadamard"] if sources else []
        ident = project.claim(ident, "Signed block operator " + canonical(candidate["cells"]),
                              "; ".join(candidate["assumptions"]), sources=source_ids)
        if project.snapshot()["claims"][ident]["status"] == "UNRESOLVED":
            status = "KNOWN_RESULT" if sources else "EMPIRICALLY_SUPPORTED"
            project.observe(ident, status, candidate["experiment"], "constructive-algebra")
        gram = project.claim("gram-" + candidate["id"],
                             "Scalar Gram cancellation for " + canonical(candidate["cells"]),
                             "arbitrary integer Gram entries under the displayed equalities; not a matrix existence theorem",
                             kind="lemma", formal_type=candidate["formal_type"])
        lifting = project.claim("lifting-" + candidate["id"],
                                "Lift the scalar identities for " + canonical(candidate["cells"]) +
                                " to a sign-matrix theorem with exact indices and dimensions",
                                "parameterized matrices of positive equal input order", kind="obligation")
        project.link(ident, gram)
        project.link(ident, lifting)
        project.link(ident, "construction-parameter-existence")
        project.link("universal-family-coverage", ident, "may_support")
        project.link(HADAMARD["id"], ident, "may_support")
        if candidate["experiment"]["assumption_removal_counterexample"]:
            weakened = project.claim("unguarded-" + candidate["id"],
                                      "The same block operator works without amicability: " + canonical(candidate["cells"]),
                                      "all Hadamard A,B of the same order")
            project.observe(weakened, "COUNTEREXAMPLE_FOUND",
                            candidate["experiment"]["assumption_removal_counterexample"], "obstruction-theory")
            old = {"claim": ident, "dependency": weakened, "kind": "generalizes"}
            if old in project.snapshot()["edges"]:
                project.retract_link(ident, weakened, "generalizes",
                                     "Correct direction: removing a hypothesis generalizes the conditional claim")
            project.link(weakened, ident, "generalizes")
        if len(receipts) < proof_budget and project.snapshot()["claims"][gram]["status"] != "LEMMA_PROVEN":
            receipts.append(project.certify(gram, candidate["proof_body"], lean))
    report["formal_lemma_attempts"] = receipts
    report["matrix_family_theorem"] = "UNRESOLVED: scalar cancellation does not discharge lifting or parameter-existence obligations"
    filename = "attempt-" + digest(report) + ".json"
    (project.root / filename).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    project._append("attempt", {"run_key": key, "artifact": filename,
                                "artifact_sha256": hashlib.sha256((project.root / filename).read_bytes()).hexdigest(),
                                "candidate_state": report["state"], "engine_sha256": engine})
    project.checkpoint(["matrix lifting", "parameter existence", "novelty/equivalence review", "global coverage"],
                       "This invocation ended; finite grammar exhaustion is only a branch result")
    return {"reused": False, "artifact": filename, "tested": report["tested"],
            "candidates": len(report["candidates"]), "formal_lemmas_verified": sum(r["verified"] for r in receipts),
            "branch_state": report["state"], "session": "BUDGET_EXHAUSTED", "resolution": "UNRESOLVED"}
