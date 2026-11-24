# Investigating unfinished research or repository work

Use for broad requests such as “find the unfinished compression work and improve
it.” Start from the current implementation, status, tests, design and recorded
results; a TODO or mathematical formulation is a lead, not a demonstrated defect.

Maintain a bounded worklist with one row per distinct claim or gap:

`Claim/gap | implemented evidence | uncertainty | smallest decisive test | verdict | next`

Classify before acting:

- Reproducible defect: a stated supported behavior fails in its intended setup.
  Preserve a failing test, trace cause and verify the correction.
- Missing implementation: a named interface or algorithm is absent; identify its
  inputs, outputs and acceptance conditions before attempting a bounded PoC.
- Open theory: a guarantee requires unresolved assumptions, proofs or evaluation.
  State the missing obligation; a simulation or schema attestation cannot solve it.
- Measurement gap: missing controls/data prevent a conclusion. Distinguish model
  behavior from validity of the procedure, evaluator or execution environment.
- Historical/deferred work: check whether it is already superseded or intentionally
  out of scope. Preserve frozen evidence and other people's working changes.

Prioritize by decision impact, test cost and consequence of error. Test one
explanation at a time; do not replace the task with an unbounded repository audit.
Record a branch's result and advance to independent authorized work when useful.
Keep branch verdicts separate from the global user objective and unfinished items.

For compression, distinguish generation, measurement, selection, preservation
and deployment enforcement. Measure the same declared content and metric on both
sides: entry text, all potentially loaded references, wrapper overhead and any
recovery/retrieval cost relevant to the claim. Label characters separately from
exact tokens and retain tokenizer identity. Moving text to references or retaining
only familiar examples is not automatically compression. Do not compare a full
baseline with a selectively loaded candidate without declaring the policy.

A lossless representation can be validated by round-trip identity. Semantic
rewriting needs requirement/evidence/authority preservation review and appropriate
behavioral evaluation; shorter text and passing static checks alone do not prove
it. Retain failed candidates and source/target hashes. Never invent writes,
approvals, evidence tags, success rates or guarantees to obtain acceptance.

Finish with a tested correction or scoped PoC, exact reproduction evidence, the
remaining backlog, and what would discriminate the next uncertainty. A single
field application is an observation about that run, not an A/B demonstration that
the skill caused an improvement.
