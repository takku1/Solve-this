# Unfinished research and repository work

Start from the implementation, tests, design and recorded results. A TODO or
theoretical formulation is a lead, not a reproduced defect. Preserve unrelated
working changes and frozen evidence.

Classify each material gap before choosing work:

| Gap | Next useful step |
|---|---|
| Reproducible defect | Capture the failure, trace its cause, repair and verify the intended behavior. |
| Missing implementation | Establish inputs, outputs and acceptance conditions; implement and exercise the real path. |
| Open theory | State the missing assumptions or proof obligations; generate and falsify candidate laws. |
| Measurement gap | Establish the oracle, controls or data needed to assess the claim. |
| Historical/deferred work | Check whether it was superseded or explicitly excluded before reopening it. |

For substantial work, maintain a compact worklist:

`Claim/gap | evidence | uncertainty | decisive test | scoped result | next action`

Prioritize by effect on the original objective, the cost of a decisive test and
the consequence of error. Use both forward construction from established facts
and backward planning from missing completion conditions. Keep independent
approaches when they test different assumptions. Exchange useful constraints and
failures across branches; do not duplicate completed investigations.

Persist enough to resume: the original objective and explicit user changes,
source versions, exact claims and hypotheses, failed approaches, evidence
locations, proof dependencies, owned changes and pending operations. Store no
secrets. Revalidate volatile facts on resumption. Missing evidence or corrupted
history is a continuity problem, not permission to invent a successful result.

An engineering milestone can be complete while the research objective remains
open. For example, a finite Boolean policy compressor may prove equivalence in
its typed domain while prose grounding and deployed-model risk remain unresolved.
Record that boundary before the experiment, and retain it in the final report.

Stop a branch when its assumptions fail, its stated budget is exhausted or no
decision-changing action is available. Record why, then continue other authorized
work if useful. A run limit is not a theorem of impossibility. Final reporting
must identify remaining dependencies rather than silently narrowing the task.
