# Certified finite-policy compression

`skillwren compress` completes a restricted, executable compression pipeline:
generate symbolic candidates, test them against every declared Boolean world,
measure the complete serialized artifact, select a strictly smaller equivalent
candidate, retain all attempts, resume and independently replay the certificate.
It does not translate arbitrary prose into formal semantics.

## Run

```text
skillwren compress examples/optimization/finite-policy.json --output out/finite --metric tokens
skillwren compress examples/optimization/finite-policy.json --output out/finite --metric tokens --resume --budget 128
skillwren compress examples/optimization/finite-policy.json --verify out/finite/certificate.json --candidate out/finite/policy.json
```

Use `--lean PATH_TO_LEAN4` on both creation and verification to execute Lean on
the exact equivalence obligation and a general optimal-decision transport
theorem. The verifier selects its trusted executable; certificate data cannot
select one. Checker errors, missing dependencies and exhausted world budgets
produce `OPEN` with exit 2. The Python implementation and prose interpretation
are not formally verified by these theorems.

Tokens use exact `cl100k_base` with the optional `tokens` dependency; there is no
estimated-token fallback. `--metric bytes` uses canonical UTF-8 bytes. Both
baseline and candidate include the same scope, variables, objective and rewrite
authority, with identical canonical JSON formatting. Evidence files are separate
offline audit artifacts, not hidden context needed to execute `policy.json`.
Sending the full certificate to a model would add context and is not counted as
a compressed deployment. No beneficial rewrite means unchanged original output.

## Typed meaning and authorization

The versioned format has Boolean `obs`, `choice`, `aux` and `param` declarations.
Its constraint grammar is Boolean literals, declared variable names, unary
`not`, and n-ary `and`/`or` (at least two operands). There are no binders, textual
macros, untyped substitutions, embedded code or variable elimination. Capture
cannot occur in this grammar. Only the constraint may change and only the
explicitly authorized constant, idempotence, double-negation, absorption and
factoring rules may be applied. Scope, roles, types and objectives remain fixed.

`finite_policy.decisions(policy, observations)` is the executable semantics:
the caller supplies every observation and parameter as a Boolean; the evaluator
returns all feasible choice assignments, existentially projecting auxiliary
variables. Observations and parameters are never optimized. An empty result is
infeasibility, not permission to choose an arbitrary action.

The independent auditor compares the complete relation, stronger than comparing
its auxiliary projection. Exclusive verdicts distinguish equality, strict
tightening, strict relaxation, incompatible redesign and crossing relations
with witnesses. Only equality qualifies for this compressor. Every candidate's
authorized derivation is replayed, not just its final truth table. Whole-domain
checks have a hard ceiling of 65,536 worlds. Adaptive proposal reuse is sound
here because checks are exhaustive, rather than statistical evidence reused as
independent trials.

## Decision-theoretic scope

Equal relations and an unchanged observation/action interface yield identical
feasible decision rules. With the same observation distribution, their risk
sets and optimal risks coincide for every finite real loss on that declared
domain, provided every observation has a feasible action. The implementation
checks that condition; otherwise the risk certificate stays `OPEN` with a
witness, rather than subtracting undefined optimal risks. For a total policy,
the finite-model deficiency bound is exactly zero. This does not
bound the behavior of an LLM interpreting two different text prompts; it is not
an estimator for the general DPCC deployed-model deficiency. `select` and
`certgate` keep their existing model-evidence requirements. This certificate
cannot be substituted for empirical model measurements or host guard wiring.

## Persistence and trust

`search.json` pins the original canonical policy, full metric and engine bytes.
Resumption reconstructs the deterministic attempt sequence and rejects altered
goals, results or engine versions. A changed engine needs an explicit new run.
`policy.json` is the executable output, and `certificate.json` binds source,
candidate, measured sizes, derivation, complete audit and optional Lean receipt.
Per-file atomic replacement writes the checkpoint last. An exclusive sibling
lock prevents concurrent writers. After an interrupted process, an owner may
remove a stale lock only after verifying no writer is alive; incomplete output
without a checkpoint needs a new output directory. These are reproducibility
controls, not a substitute for host-owned deployment storage.

## Research grounding and remaining obligations

[LLMLingua-2](https://arxiv.org/abs/2403.12968) studies learned token pruning and
empirical downstream performance. It does not provide this pipeline's exact
Boolean equivalence guarantee or a universal natural-language guarantee.
[Prover-Verifier Games](https://arxiv.org/abs/2108.12099) motivates separating
proposal incentives from verification. Here that translates into a fixed
independent auditor, counterexample witnesses, immutable correctness fixtures
and a size reward available only after correctness. This implementation does
not train game-theoretic agents or claim an equilibrium result.

The wider semantic-sufficiency program remains unresolved: arbitrary prose
grounding, richer typed domains and capture-avoiding binders, inferred deficiency
bounds for actual model behavior, infinite-family proofs, sequential statistical
certification and deployment scope. Finite-policy success closes none of those
by implication. Original objective preservation remains the resolution gate.
