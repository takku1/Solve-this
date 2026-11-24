# Persistent mathematical discovery

Preserve the original quantified statement, domain and proof/refutation criterion
as the project objective. Subproblems, search grammars and computational budgets
cannot replace it. A user-authorized objective change belongs in the record.

## Research loop

1. Resume established theorems with provenance, conjectures, counterexamples,
   failed approaches, hypotheses, source versions and unresolved dependencies.
2. Audit relevant literature and barriers before adding search algorithms.
   Separate sufficient constructions from equivalences and folklore from checked
   statements. Keep conflicting frontier reports with their dates and scope.
3. Describe a measurable program whose milestones reduce proof obligations.
   Work backward from the objective and forward from established results. Maintain
   acyclic proof dependencies; an analogy or speculative edge is not a proof.
4. Generate parameterized constructions, composition laws, invariants and lemmas
   with explicit domains, shapes and assumptions. Prefer a reusable family or
   bridge over accumulating more familiar examples.
5. Derive exact conditions and actively seek falsifiers. Use exact arithmetic,
   symbolic computation and available SAT/SMT or combinatorial search where
   appropriate. An unsuccessful sufficient construction does not prove
   nonexistence. Restricted UNSAT applies only to its encoded domain; timeout or
   UNKNOWN does not establish a theorem.
6. Generalize surviving structure, then prove identities, dimensions, signs,
   parameter existence, implication directions and coverage separately. A valid
   conditional identity does not supply parameters satisfying its conditions.
7. Challenge degenerate cases, hidden hypotheses, circularity, statement drift
   and published equivalents. Independent proof checking and novelty assessment
   are different obligations.
8. Persist the results and remaining gaps; reprioritize instead of starting over.

Represent covered families symbolically when the objective is universal. A
finite diagnostic window reports gaps in enabled rules, not all globally open
cases. Larger verified instances alone do not establish a universal family.

## Claim and resolution states

| State | Meaning |
|---|---|
| KNOWN_RESULT | Established mathematics reproduced with provenance. |
| COUNTEREXAMPLE_FOUND | A specified candidate hypothesis falsified. |
| EMPIRICALLY_SUPPORTED | Bounded experiments survived under recorded conditions. |
| LEMMA_PROVEN | An exact intermediate statement proved; its intended meaning still needs review. |
| COVERAGE_EXPANDED | A proven family or witness adds coverage relative to a declared baseline. |
| BRANCH_EXHAUSTED | A particular strategy or grammar reached its stated limit. |
| BUDGET_EXHAUSTED | Research suspended with a resumable checkpoint. |
| CONJECTURE_PROVEN | Independently checked proof of the original statement. |
| CONJECTURE_REFUTED | Independently checked proof of its negation. |

Only the last two resolve the original conjecture. Keep novelty, empirical
support, proof status and session state separate. A counterexample to a proposed
construction is not automatically a counterexample to the original conjecture.

## Formal verification

Use a suitable proof assistant when it strengthens the claim. Check the exact
intended proposition, transitive assumptions/axioms, prerequisites, checker
version and proof artifacts. Reject placeholders, admitted proofs and unreviewed
new axioms used to manufacture success. Replay decisive certificates rather than
trusting a saved `passed` field. Review the correspondence between informal and
formal statements; the kernel certifies the latter.

Missing tools or failed checker invocations leave claims unresolved. Do not
install toolchains or incur provider usage without the task's authorization.
Application-level journal integrity does not provide host isolation.

The repository includes an optional Hadamard-specific runtime under
`examples/hadamard`; it is a worked case, not a general mathematical discovery
engine. Use it only for its fixed objective. A different conjecture needs its
own reviewed statement and proof adapter. Its bounded signed-block grammar and
scalar Gram lemmas do not resolve Hadamard, full family lifting or novelty.
