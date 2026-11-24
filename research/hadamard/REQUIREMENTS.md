# Requirement inventory and implementation disposition

The user's requested objective and eleven components are the authority for this
redesign. This inventory distinguishes implemented mechanisms from outstanding
mathematics; no item is silently converted into a smaller final objective.

| Requirement | Implementation or evidence | Remaining limitation |
|---|---|---|
| Immutable universal objective | `objective.py`, fixed `HadamardCore.lean`, journal replay and exact resolution wrapper | Final theorem remains unproved |
| 1. Mathematical knowledge base | Versioned sources, scoped immutable claims, known-result provenance, failed attempts and audit/program artifacts | Literature acquisition/interpretation is performed by the agent; no autonomous web crawler |
| 2. Symbolic coverage | Explicit Sylvester/prime-power Paley rules and least product closure, symbolic complement and derivation trees | Partial family model; not the full mathematical frontier |
| 3. Research planner | Seven shared branch records, typed support/required edges, backward unresolved dependencies and diversity ordering | Semantic generality/novelty/test-cost prioritization still needs research judgment |
| 4. Conjecture generator | Signed symbolic block grammar enumerated independently of baseline formula classification | One bounded grammar; additional design/number-theory grammars remain research work |
| 5. Experimental engine | Python integer sign/Gram checks, exact formal symbolic residuals, signed row/column/atom symmetry classes, hypothesis-removal falsifiers | SAT/SMT backend absent because Z3 is unavailable; no fake solver or unrestricted UNSAT claim |
| 6. Generalization engine | Parameterized operators, hypotheses, formal scalar Gram statements, explicit lifting/existence/coverage obligations | Scalar identities do not finish universal matrix construction theorems |
| 7. Adversarial verification | Degenerate/overflow/non-sign controls, removed-hypothesis counterexample, cycle rejection, weak-goal/fake-certificate controls | Literature-equivalence and novelty checks remain human/agent research tasks |
| 8. Formal proof engine | Real pinned Lean process, exact statement wrapper, transitive axiom inspection, artifact/version hashes, independent resolution replay | Restricted proof interface; Mathlib and richer proof backends not silently assumed |
| 9. Proof dependency graph | Persistent claims, required acyclic edges and separate speculative support links | A graph records dependencies; it is not itself a proof |
| 10. Persistent loop | Atomic locked journal, attempt archive/cache, cross-process resume, explicit suspended checkpoints | Manually invoked; not an unattended infinite autonomous service |
| 11. Resolution gate | Only actual proof of `HadamardConjecture` or its negation resolves the root | No proof/refutation currently exists in this project |
| Literature-first program | `AUDIT.md` and `PROGRAM.md` written before construction synthesis; adopted hashes gate search | Source discrepancy is retained; no exhaustive frontier audit claimed |
| Game theory/design addition | Fixed proposer/falsifier/verifier roles, legal grammar moves, independent controls, diversity and anti-gaming rules; MDA evaluation split | No equilibrium or empirical discovery-performance claim |

The first implementation milestone is persistent symbolic discovery with exact
falsification and formal algebra lemmas. Completion of this engineering milestone
must never be reported as completion of the immutable mathematical objective.
