# Solve This field test on SkillWren

The investigation found and corrected concrete defects in SkillWren's reviewed
compression example, compiler diagnostics and failure records, and workflow
explanation. The changes are applied to `Z:\SkillWren`. They do **not** finish a
general semantic compressor or establish DPCC's research guarantees.

This was one real application of Solve This by the current agent, followed by
regression tests and evidence-driven instruction edits. It was not an independent
A/B evaluation, model training, or a test of whether Solve This caused better
results. No paid model runs, credential experiments, approvals, commits, merges or
publication were performed.

## What was actually unfinished

| Component | Finding | Verdict and remaining work |
|---|---|---|
| `measure` and optimized `build` | Implemented; a hand-authored smaller example exists and has hash-bound requirement review. Its reviewed bytes broke on a Windows checkout. | SOLVED for the reproduced checkout defect. Measurement/review acceptance is not semantic equivalence. |
| `compile` | Translates prose to checked structure; it does not generate a guaranteed smaller representation. Wrong evidence tags are frozen during lowering. | REFUTED the assumption that compilation itself is compression. Classification prompt narrowed; automated safe retagging remains open. |
| `select` | Implements finite, fixed-candidate empirical selection, structural checks, conservative bounds and optional evaluator-attested deficiency. | Implemented selector, not a compressor or deficiency estimator. Existing selector/guard tests passed; no new empirical policy was certified. |
| DPCC compressor/search | The formulation explicitly leaves adaptive/sequential candidate generation, deficiency estimation and semantic rewrite machinery for future work. | SUPPORTED as a missing implementation/research gap by implementation mapping and source inspection. No invented algorithm or guarantee substitutes for the missing obligations. |
| Runtime closure | Guard/certgate components exist, while actual isolation against a credentialed model depends on the host and a separate authorized experiment. | Remains untested here; no credential or deployment experiment was run. |

Primary local sources: [status](../../experiments/skillwren/docs/STATUS.md),
[DPCC implementation mapping](../../experiments/skillwren/docs/current/research/semantic-sufficiency/FORMULATION.md),
[compact conversion contract](../../experiments/skillwren/docs/current/design/compact-conversion.md),
and the earlier [I7 investigation](../../experiments/skillwren/docs/current/research/fidelity-benchmark/i7-investigation/README.md).
These are repository documents, not external verification of theoretical claims.

## Tested corrections

1. **Windows optimized-build failure.** The baseline suite reproduced
   `BuildError: original changed: review the conversion before building`.
   `git ls-files --eol` showed LF in Git and CRLF in the worktree for the
   review-pinned example. Normalizing only line endings reproduced the existing
   review hashes exactly. Added exact-byte attributes for `examples/optimization/`
   and restored those reviewed LF bytes; neither review hashes nor review
   decisions were regenerated. Added a non-tokenizer-dependent hash regression.
2. **Unhelpful I7 diagnostics and evidence classification.** Errors now name
   only the evidence form needed by the failing tag and warn against inventing
   operations or weakening real requirements. The adapter now distinguishes
   artifact writes from reading/showing files or returning a reply. The actual
   I7 satisfaction table is unchanged: lost exec/user/effect evidence remains a
   failure. Prompt changes have not been behaviorally evaluated with a new model
   round, and tags remain fixed during lowering.
3. **Lost debugging evidence on refused compiles.** `--keep-failed` now retains
   the last safely landed attempt, its actual inventory/tags/anchors, and a
   failure audit with phase, diagnostics/findings, source hashes and call record.
   Inventory-phase failures retain the incomplete inventory without inventing a
   candidate. An invalid repair preserves the preceding safely landed attempt.
   Failed outputs remain unapproved and unpublished.
4. **Incorrect deterministic explanations.** Exec-only flows previously said
   “the workflow changes nothing,” and absence of additional order rules was
   described as freedom to reorder all steps. The explainer now lists command
   effects, treats readonly as a declaration, and preserves the written sequence.
   The test harness explicitly replaces the old frozen `changes nothing`
   expectation with absence of explicit writes/calls/commands. Frozen data and
   historical scores were not edited or retrospectively reinterpreted as new
   benchmark results.

The generated plugin was rebuilt from sources and its drift check passes.
[Patch](skillwren-fixes.patch), [preflight](patch-preflight.json), and
[applied-file hashes](applied-patch.json) retain the exact changes. Application
refused independent changes in affected files; historical permission-restricted
directories were untouched. The isolated checkout remains under
`Z:\Solve-this\experiments\skillwren` for inspection.

## Verification

| Run | Observed result |
|---|---|
| Initial sandbox attempt | Invalid run: temporary-file access errors and a stalled child; stopped, not counted as semantic failures. |
| Unchanged isolated baseline | 482 tests: 1 error (Windows review hash), 3 skipped. |
| New compiler regressions before fixes | 3 failing subcases and 2 errors established missing diagnostics/audits. |
| New explainer regressions before fixes | 3 failures established the effect/ordering claims. |
| Final isolated SkillWren | 490 run: 487 passed, 3 skipped. |
| Applied `Z:\SkillWren` | 490 run: 487 passed, 3 skipped. |
| Solve This repository | 8 passed, including package integrity and four gate-bypass mutations. |
| Skill validation | Frontmatter/reference checks pass; inventory coverage/landing/reverse trace: 0 errors, 0 warnings. Logic: 0 errors, one explained planning W15. |

Raw logs: [baseline](baseline-unsandboxed-suite.txt),
[compiler red tests](red-regressions.txt), [explainer red tests](red-explainer.txt),
[final isolated suite](final-suite.txt), [applied destination suite](applied-target-suite.txt).
Intermediate unsuccessful verification logs are retained as well. The earlier
`green-suite.txt` and `verified-suite.txt` names describe intended checks, not
successful outcomes; their logs correctly record the frozen-expectation failures.
The suite reports three skips; skipped paths were not forced to run or counted
as passes.

## Compression measurements

Exact `cl100k_base` tokens, same frozen LF prose baseline, explicit selected
Markdown context including wrapper overhead:

| Representation | Entry tokens | Entire declared Markdown context |
|---|---:|---:|
| Original prose | 3,036 | 9,177 |
| First SkillWren conversion | 4,725 | 10,866 |
| Tuned SkillWren conversion | 4,116 | 10,793 |

The tuned entry is **12.89% smaller** than the first conversion, but total
declared context is only **0.67% smaller**, because the new research-backlog
reference is counted. It is still **17.61% larger** than the prose context and
does not meet an optimized-build compression target. No references were silently
dropped. Some references load conditionally in practice, but no observed per-task
load reduction is claimed.

The shipped hand-authored optimized example is **555 -> 510 tokens** under its
reviewed LF bytes (8.11% reduction), and its actual optimized-build regression now
passes. This demonstrates that the existing review/size gate works for that
example, not an automatic compression algorithm.

[Initial matched measurement](initial-canonical-context-measurements.json) and
[tuned measurement](tuned-context-measurements.json) list all counted files and
both exact tokens and characters. `baseline-skill/` retains the original prose
snapshot and its ten references. Earlier [worktree measurements](context-measurements.json)
used CRLF entry/example bytes; those slightly different counts are retained
separately and are not mixed into the matched table.

## Solve This refinements

The [tuned package](../../solve-this-tuned/SKILL.md) adds:

- A bounded research worklist distinguishing defects, absent implementation,
  open theory, measurement gaps and intentionally deferred work.
- A route to independent remaining work after a branch is resolved or blocked,
  with branch verdicts kept separate from global completion.
- Explicit compression accounting across generated content, references and
  wrappers; size, preservation, selection and enforcement remain separate claims.
- Less duplicated guidance, with all ten original references unchanged and one
  targeted research-backlog reference added.

The original build is retained in `solve-this/`. The tuned source is
`solve-this-draft/`; [review artifacts](../../skillwren-review/README.md)
include the line inventory, deterministic explanation, coverage and toolchain
hashes. Coverage remains 0 enforced, 10 recordable and 9 instructed obligations;
no host policy or ledger was activated. Planning W15 remains explicit rather
than disguising model judgment as external proof. Requirement anchors are
bookkeeping, not semantic-equivalence evidence, and the prose reductions have
not had independent behavioral evaluation.

## Next decision-changing work

1. Evaluate evidence classification in a **new**, pinned compiler round, keeping
   the old benchmark frozen. Measure incorrect tags, invented operations,
   refusals and source fidelity separately; do not infer improvement from the
   changed prompt or greater publication rate alone.
2. Specify a bounded candidate generator with explicit authority, evidence and
   dependency preservation. Compare it with hand-authored compact candidates at
   matched measured outcomes; use fresh holdout evidence after adaptive search.
3. Define and validate the decision class and evaluator before estimating
   deficiency or claiming decision-preserving compression. Attested numbers and
   passing simulations cannot supply missing proofs.

The resolved implementation bugs are SOLVED within their regression scope.
General DPCC compressor generation and theoretical guarantees remain open.
