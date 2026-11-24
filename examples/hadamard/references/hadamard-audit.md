# Hadamard research audit

Audit date: 2026-11-23. This is an active literature audit, not a proof of the
conjecture or a claim that any new construction has been found.

## Immutable objective

For every positive integer k, exhibit a real sign matrix H of order 4k with
HH^T = 4k I, or prove nonexistence at one such order. A failed construction,
restricted-family UNSAT result, finite collection of matrices or exhausted
budget cannot resolve this statement. The earlier small-order experiment is a
KNOWN_RESULT reproduction and remains historical evidence only.

## Literature and version ledger

1. Egan, Kotsireas, London, Ó Catháin, *Recent progress in the construction of
   Hadamard matrices*, [arXiv:2610.27175v2](https://arxiv.org/abs/2610.27175v2),
   revised 3 November 2026. It reports independent verification of the twelve
   previously missing orders below 2000. **Version discrepancy:** the abstract
   lists 85 open orders up to 10000; the retrieved
   [v2 PDF](https://arxiv.org/pdf/2610.27175v2), Table 5, and
   [HTML](https://arxiv.org/html/2610.27175v2) still list 95, starting at 2396.
   Record both; do not publish an exact current gap count as settled. In either
   account, using 668 as the current smallest open case is stale. Reported
   existence is not a local kernel certificate or an exhaustive live survey.
2. Cati and Pasechnik, *A database of constructions of Hadamard matrices*,
   [arXiv:2411.18897v2](https://arxiv.org/abs/2411.18897v2), 30 August 2025.
   Provides a reproducible construction catalogue and identifies a Paley-method
   barrier for orders 2^m·509203. A barrier to a method is not nonexistence of
   Hadamard matrices. Its numerical frontier predates the 2026 results.
3. [SageMath Hadamard documentation](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/matrices/hadamard_matrix.html):
   executable reference for prime-power Paley I/II and other constructions.
   Construction availability in a particular installed version must be checked;
   documentation is not automatically a complete frontier oracle.
4. Williamson, Yacobi, Zinn-Justin, *Generating Hadamard matrices with
   transformers*, [arXiv:2604.11101v2](https://arxiv.org/abs/2604.11101v2),
   11 May 2026. Combines learned proposals with local search in structured
   families. Relevant to candidate generation, not a universal existence proof.
5. Romera-Paredes et al., *FunSearch*, [paper](https://doi.org/10.1038/s41586-023-06924-6),
   [author repository](https://github.com/google-deepmind/funsearch).
   Adopt a persistent diverse candidate archive and a separate exact evaluator.
   The publisher full text was inaccessible in this audit; the author repository
   was inspected. No sample-efficiency or discovery guarantee is transferred.
6. Fawzi et al., *AlphaTensor*, [paper](https://doi.org/10.1038/s41586-022-05172-4),
   [author repository](https://github.com/google-deepmind/alphatensor).
   Algorithm invention can be posed as legal moves on mathematical objects.
   Use typed construction grammars and symmetry-aware proposals; the analogy
   supplies no Hadamard theorem. Publisher full text was inaccessible.
7. Anil et al., *Learning to Give Checkable Answers with Prover-Verifier Games*,
   [arXiv:2108.12099](https://arxiv.org/abs/2108.12099).
   Use an untrusted proposer, an adversarial falsifier and a fixed proof checker
   with different acceptance criteria. A persuasive verifier conversation is
   not kernel certification; equilibrium guarantees need their stated game.
8. Hunicke, LeBlanc, Zubek, *MDA*, [author-hosted paper](https://users.cs.northwestern.edu/~hunicke/pubs/MDA.pdf).
   Adapt mechanics/dynamics/experience to test the research system: legal moves
   and gates, observed selection/repetition behavior, then researcher usefulness.
   This adaptation is a design hypothesis, not evidence that game design solves
   mathematical conjectures.
9. Lean's [proof-validation guidance](https://leanprover-community.github.io/did_you_prove_it.html)
   and [axiom reference](https://lean-lang.org/doc/reference/latest/Axioms):
   verify the exact intended statement, inspect transitive axioms, reject
   `sorryAx` and unintended axioms. Successful elaboration alone is insufficient.

## Construction knowledge and remaining obligations

Baseline symbolic families: H(1), H(2), Sylvester powers of two; Paley I at
q+1 for prime powers q≡3 mod 4; Paley II at 2(q+1) for odd prime powers q≡1
mod 4; and Kronecker product closure. Store these as parameterized rules with
their hypotheses, never as a list of sampled orders. The complement of this
restricted family model is **not** the set of globally unresolved orders.

Useful research interfaces include orthogonal designs, supplementary difference
sets, Goethals–Seidel arrays, Williamson-type matrices, complementary sequences,
bordered arrays, conference matrices and symmetric block designs. Each interface
needs an explicit implication direction and hypotheses. In particular, a
Legendre pair at every odd length would imply the conjecture; existence of a
Hadamard matrix at one order does not imply existence of a Legendre pair of the
corresponding length. Do not silently turn sufficient constructions into
equivalences. The Egan et al. survey and Sage catalogue index these interfaces;
the seed knowledge base records them as literature routes with proof obligations.

## Promising gaps, without a novelty claim

- Parameterized bordered/block constructions: derive Gram conditions before
  numerical search, then distinguish cancellation identities from proofs that
  their parameters exist for every target order.
- Coverage bridges: work backward from all positive multiples of four to a
  sufficient family theorem; use a restricted model's uncovered set to identify
  limitations of that model, not presumed unknown mathematics.
- Obstruction transfer: an obstruction under symmetry/multiplier/ansatz
  restrictions informs other branches but cannot refute unrestricted existence.
- Proof lifting: connect formal polynomial cancellation to signs, dimensions,
  parameter satisfiability and the exact matrix statement. An identity can be
  universally true while its required parameter choices never exist.

## Local capability audit

Python, exact integers, SymPy and NumPy are present. Lean 4.33.1 executes locally;
Z3 and the `z3` Python package are absent. Use the installed pinned Lean binary
without downloading toolchains. No Mathlib availability is assumed. Wilderbeast's
README was inspected: it exposes bounded hypothesis/generalization engines and
replayable SMT receipts, but its guarantees are scoped to their encoded domains.
No Wilderbeast code was changed and no uninspected receipt is trusted here.

Novelty remains unreviewed until a candidate is compared with the updated
construction literature, equivalence transformations, and available artifacts.
This audit establishes a research starting point, not an exhaustive bibliography.
