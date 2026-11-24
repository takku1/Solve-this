# Research program and architecture

This program was established after the literature audit and before adding
construction search. The global objective is immutable; milestone completion
never changes it. M0 is an infrastructure milestone, not conjecture resolution.

## Scope, ownership and contracts

| Component | Owned state and contract |
|---|---|
| Knowledge store | Immutable objective, literature provenance, exact typed claims, evidence, failed attempts, branch state and append-only hash-chained journal. Atomic single-writer publication; restart replays the same history. |
| Coverage model | Symbolic family rules and product closure; membership derives a construction route. An uncovered order means only uncovered by enabled rules. No finite scan certifies the infinite complement empty. |
| Planner | Shared claim graph and branch worklist. Backward unresolved obligations and potential generality inform a recorded qualitative priority; empirical hit counts never determine mathematical resolution. |
| Symbolic proposal/evaluation | A bounded signed-block grammar; exact noncommutative Gram residuals, explicit assumptions, experimental counterexamples and symmetry fingerprints. Proposals and numerical witnesses remain distinct from proofs. |
| Generalization | Parameterized statements with quantifiers/domain/hypotheses, validation across diverse cases, then explicit lifting and parameter-existence obligations. No induction from finitely many samples. |
| Proof boundary | Pin the exact statement and local Lean version; generate a fixed wrapper, check the exact theorem type and transitive axioms, retain source/output hashes. Missing checker, timeout or unproved obligations stay unresolved. |
| Research loop | Resume known successes/failures, exchange branch discoveries, select an obligation, propose, falsify, generalize, prove and record gaps. A budget checkpoint suspends work without a solved verdict. |

Keep Python and local files already used by the repository. A versioned JSON
journal avoids a new service or datastore product. Writers use an exclusive lock
and atomic replacement on the same filesystem. This is an application integrity
boundary, not isolation from a malicious same-account process. No network model
API, unattended infinite job, paid run or new tool installation is introduced.
Local proof attempts run only explicitly supplied/generated proof text with a
timeout; arbitrary downloaded code is not executed as literature evidence.

## Seven communicating branches

| Branch | First research target | Useful transferable output |
|---|---|---|
| Constructive algebra | Signed block laws with explicit Gram residuals | Candidate identities, failed cross terms, parameter hypotheses |
| Combinatorial design | Precisely scoped sequence/design implications | Equivalent formulations only with both directions proved |
| Computational search | Counterexamples/structures outside a named ansatz | Exact witnesses and symmetry constraints, never unrestricted nonexistence from restricted UNSAT |
| Recursive composition | New parameterized operators and closure gaps | Symbolic order transforms and proof obligations |
| Number theory | Describe uncovered sets and parameter-existence barriers | Conditional arithmetic lemmas, not finite gap counts as global facts |
| Obstruction theory | Necessary conditions and ansatz-specific impossibility | Scope-tagged obstructions usable by other branches |
| Formal mathematics | Prove cancellation, lifting and objective bridges | Exact certified lemmas and remaining dependencies |

Branches are persistent work records, not a requirement to spawn agents. Link
discoveries to multiple branches and distinguish `requires` proof edges from
`may_support` research edges. Reject proof cycles; allow separate research
feedback records. Inspect unresolved ancestors backward from a target while
reusing established lemmas forward.

## Measurable increments

1. **M0: objective and memory.** Persist the exact quantified objective; prove
   through tests that known constructions, a million hypothetical observations,
   candidate falsification, branch exhaustion and budget exhaustion cannot
   resolve it. Reopen the project in another process without losing prior work.
2. **M1: symbolic construction synthesizer.** Enumerate a declared finite grammar
   of signed 2×2 block expressions, derive Gram residuals under named hypotheses,
   retain candidates and reject degenerate/false ones. Rediscover a classical
   family without putting its complete formula in the proposal generator.
   Compare normalized candidates with known baselines; syntactic difference is
   not mathematical novelty. Record grammar coverage and failed searches.
3. **M2: exact verification and formal obligations.** Verify matrix witnesses
   with Python integers; certify generated scalar Gram-cancellation lemmas with
   Lean; expose the separate matrix-lifting and parameter-existence obligations.
   An algebra lemma is not a universally proved matrix construction. A final
   proof must inhabit the trusted Hadamard statement or its negation.
4. **M3: genuine new family.** Expand the grammar only after M1/M2 evidence.
   Require literature/equivalence review, a full formal family theorem, and
   symbolic coverage comparison. A rediscovered law is KNOWN_RESULT; an
   unreviewed one is not labeled new. This milestone may remain unresolved.
5. **Global resolution.** Only an independently replayed proof/refutation of
   the immutable original objective can yield CONJECTURE_PROVEN or
   CONJECTURE_REFUTED. Implementing M0–M2 is never reported as solving Hadamard.

## Game theory and game design

Define proposer moves as typed symbolic edits; falsifier moves as exact
counterexamples, assumption removal tests and equivalence challenges; verifier
moves as fixed proof checks. The proposer cannot edit the objective, acceptance
predicate or verifier. Reward verified reusable structure and eliminated proof
obligations; retain failures. Never reward matrix count, output length,
unreviewed novelty, or persuading a second language model.

This is a protocol inspired by prover-verifier games, not a proved Nash/minimax
solution. Use diverse fixed controls as well as adaptive opponents; self-play
can share blind spots. Branch selection uses transparent evidence and resource
cost, with no invented success probabilities. Preserve a diversity archive so
the cheapest known construction cannot monopolize the search.

MDA adaptation: **mechanics** are legal grammar moves, exact domains and gates;
**dynamics** are measured branch starvation, rediscovery loops, evidence leakage
and reward gaming across resumed runs; **experience** is whether researchers can
inspect, reproduce and redirect the work. Human usefulness is evaluated
separately from mathematical correctness. A game score never proves a theorem.

## Assurance and checks

| Claim | Failure | Owner/control | Acceptance evidence |
|---|---|---|---|
| Objective preserved | Benchmarks replace the conjecture | Immutable canonical objective plus event validation | Drift and fake-success tests |
| Durable knowledge | Crash/restart loses or duplicates evidence | Journal lock, sequence/hash chain, atomic replace | Replay, corruption and writer-collision tests |
| Proof graph sound as bookkeeping | Circular or missing prerequisites | Typed edges and cycle rejection | Missing-node, cycle and blocked-prerequisite tests |
| Exact experiments | Floating overflow or modular equality accepted | Arbitrary-precision sign/Gram checker | Non-sign, overflow and modular-only controls |
| Proof scope retained | Scalar identity promoted to global existence | Fixed statement wrappers and separate claim kinds | Weak-theorem, custom-axiom, sorry and unresolved-dependency tests |
| Honest capability status | Missing solver treated as failed conjecture | Capability discovery and suspended state | Absent-checker/timeout paths |
| Reuse without amnesia | Known constructions repeatedly called novel | Stable claim fingerprints, persistent attempts and branch sharing | Duplicate, resume and novelty-state tests |

Raised disciplines: verification, reliability, operations, maintainability and
CLI usability. The implementation is local and manually invoked; external
literature retrieval is separate from proof execution. No deployment or service
availability target. Work is unguarded by full-stack's run_guard; scope will be
checked with Git status/diff and actual test logs. Existing unrelated changes and
the archived SkillWren investigation remain intact.

## Remaining blockers and honest limits

New mathematical theorems, a complete family lifting proof and mathematical
novelty are research outcomes, not implementation promises. SAT/SMT adapters
remain conditional on an available solver and proof-producing encoding; there
is no benefit in a fake backend. Imported literature is labeled by provenance,
and uncertain frontier versions remain disputed. The journal does not provide
host isolation, autonomous online retrieval, or distributed concurrent writers.
