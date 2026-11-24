# Experimental protocol

In open mathematics an experiment is intermediate research. Use
[mathematical discovery](mathematical-discovery.md): preserve the immutable
objective, domains, symbolic claims and proof obligations, then return results
to the persistent loop. Passing examples, failed searches and restricted UNSAT
cannot resolve a universal existence conjecture.

Use only when a test could change the next decision. Do not build a prototype for a question already answered by a reliable procedure.

## Before running

1. State the objective and a falsifiable, scoped hypothesis. Name the observable outcome that would contradict it.
2. Search local implementations, installed tools, authoritative documentation, and relevant prior work. Prefer reuse or adaptation over reinvention. Label any unavailable search surface.
3. Choose the smallest test that discriminates alternatives. Specify the baseline/control, inputs, variables held constant, measurement method, success criterion, and inconclusive conditions **before** observing results.
4. Check authority, side effects, costs, dependencies, cleanup, and a bounded run budget. Use disposable environments for risky changes.

## Execution

- Preserve the baseline and run exact commands against the intended target.
- Capture raw output, failures, versions, environment, seed and timing where applicable. Do not infer success from exit status alone.
- Repeat only when variability matters; report sample sizes and dispersion rather than inventing precision.
- Verify instrumentation with a known-good control where possible. Differentiate simulation, unit tests, integration, and real deployment evidence.
- When causal claims matter, compare matched conditions and avoid confounding changes. If isolation is impossible, narrow the claim.
- Record failed experiments and tool errors; never silently repair the setup and present the repaired run as the original.

## Conclude

Report SOLVED, SUPPORTED, REFUTED, INCONCLUSIVE, or BLOCKED with evidence scope. A PoC is not a mathematical proof, broad validation, or production readiness. Include reproduction steps and the smallest justified follow-up, if any. Stop when further tests cannot change the decision.
