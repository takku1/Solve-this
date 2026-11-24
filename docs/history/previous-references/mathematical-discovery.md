# Persistent mathematical discovery

The original quantified objective is immutable within a research project. Record
it canonically with a stable hash and an exact formal proposition where possible.
Changing that objective requires a distinct, explicitly authorized project/fork;
decomposition, limited compute and convenient benchmarks cannot change it.

## Research cycle

1. Resume known theorems with provenance, conjectures, counterexamples,
   unsuccessful approaches, scope restrictions, branch budgets, source versions,
   proof artifacts and unresolved dependencies.
2. Audit current literature before adding search, checking sufficient conditions
   versus equivalences and original versus later versions. Keep conflicting
   sources rather than guessing the frontier. A catalogue's missing entry is not
   a nonexistence result.
3. Maintain symbolic covered sets and construction hypotheses. A finite window
   reports only gaps in enabled rules; it cannot certify all orders covered or
   identify all globally unresolved cases.
4. Plan independent but communicating branches. Work backward from the objective
   to missing lemmas and forward from established results. Proof dependencies
   are acyclic; speculative support/analogy does not discharge obligations.
5. Generate parameterized laws, block operators, invariants and lemmas with
   explicit domains, quantifiers, shape constraints and hypotheses. Seek structure
   rather than merely larger instances.
6. Derive exact conditions, attempt to solve them and seek counterexamples. Use
   exact arithmetic, symbolic manipulation, available SAT/SMT and justified
   symmetry reduction. Distinguish unsatisfied sufficient conditions from
   impossibility. Restricted UNSAT, UNKNOWN/timeouts and incomplete search never
   establish unrestricted nonexistence.
7. Generalize promising results into universal claims. Prove algebra, signs,
   dimensions, parameter existence, implication directions and coverage separately;
   examples alone never justify an unrestricted law.
8. Challenge degenerate cases, hidden assumptions, circularity, statement drift,
   equivalent published constructions and evaluation leakage. Proof replay and
   informal novelty review are separate.
9. Certify the exact intended formal statement, accepted transitive axioms,
   dependencies, checker version and artifacts. Reject admitted proofs and
   custom axioms assuming the result. SMT facts in an encoded theory do not
   automatically prove unrestricted integer-matrix existence.
10. Persist results and gaps, exchange constraints across branches and reprioritize.
    Budget exhaustion suspends work; resume from evidence, not amnesia.

## Hadamard objective

`forall positive integer k, exists H in {-1,1}^{4k x 4k}: H H^T = 4k I`.

The local Lean core uses positive natural k and total integer-valued functions
restricted to indices below 4k. These encode the same finite real sign matrices;
entries outside the finite square are irrelevant. Review this translation as
part of any final proof. A refutation must establish nonexistence at an admissible
order. Failing to find H, or proving no H exists in an ansatz, is insufficient.

## States and evidence gates

| State | What it establishes |
|---|---|
| KNOWN_RESULT | Existing mathematics with provenance |
| COUNTEREXAMPLE_FOUND | Exact falsification of a specified candidate/domain |
| EMPIRICALLY_SUPPORTED | Bounded experiments survived under recorded conditions |
| LEMMA_PROVEN | Exact intermediate formal proposition certified; English paraphrase review remains separate |
| COVERAGE_EXPANDED | Proven family/witness and valid comparison add orders relative to a declared baseline; novelty is separate |
| BRANCH_EXHAUSTED | One grammar/strategy reached its stated limit |
| BUDGET_EXHAUSTED | Resumable research suspension |
| CONJECTURE_PROVEN | Independently checked proof of the original universal objective |
| CONJECTURE_REFUTED | Independently checked proof of its negation |

UNRESOLVED is the initial/global status. Only the last two result states resolve
the mathematics. Keep novelty, formal proof, empirical support, scope and session
state separate.

## Runnable milestone and limits

The included engine implements journal integrity, objective preservation,
source/claim records, shared proof dependencies, symbolic baseline coverage and a
bounded signed-block synthesizer. Scalar Gram lemmas can be checked with pinned
Lean 4.33.1. They do not discharge full matrix lifting, parameter existence or
novelty. The seven branches are persistent responsibilities, not seven invented
autonomous algorithms or a requirement to delegate. Missing solvers remain
capability gaps; no toolchain installation or model usage is automatic.

The journal shares the user's account and is not isolated from a malicious owner.
The proof gate executes its fixed wrapper and checks exact type/axioms; saved
pass fields cannot substitute for replay at final resolution. Formal proof does
not establish literature novelty or claims outside its exact statement.
