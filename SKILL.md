---
name: solve-this
description: Solve uncertain problems through existing-solution research, discriminating experiments, persistent discovery, and independent verification. Use when the right approach, cause, feasibility, or proof is unclear; apply a reliable known procedure directly when one exists.
---

# Solve This

Find what works. Test what matters. Preserve the question until it is answered.

Use the shortest justified route: **inspect → act → verify** for a known solution;
**discover → conjecture → experiment → falsify → generalize → prove** for open
research. A successful subproblem never replaces the user's original objective.

## Checked workflow

```contract
inputs:
  request, context, tools
order:
  verify#objective before exec perform action
  verify#completion before return#solved
  exec persist checkpoint before return#unresolved
```

```logic
solve:
  read original objective and completion criterion from request as objective
  verify #objective the objective preserves the user's target, scope, constraints and original success criterion from objective
    otherwise:
      abort with "Clarify the missing objective; do not substitute an easier task."
  read relevant evidence and prior attempts from context as state
  apply route selection with state as plan

  label investigate:
  if a solution or resolution of the original objective is proposed:
    exec independent verification from tools as verification
    verify #completion the verification satisfies the original objective at the claimed scope from verification
      otherwise:
        apply failed verification and remaining gaps with verification as state
        apply route selection with state as plan
        if a justified recovery or independent action remains:
          return to investigate
        return to checkpoint
    return #solved verification as result
  if a justified action fits existing authority and the available resources:
    exec perform action {plan} from tools as evidence
    apply evidence assessment with evidence as state
    apply route selection with state as plan
    if a solution or resolution of the original objective is proposed:
      return to investigate
    if the result warrants another discriminating action:
      return to investigate

  label checkpoint:
  exec persist checkpoint {state} from tools as saved
  return #unresolved saved as result
```

## What the steps require

**Objective.** Recover settled decisions and authorization before asking for
missing information. For an engineering task, define the observable user outcome.
For mathematics, retain the exact domain, quantifiers and proof/refutation
criterion. A benchmark, restricted model or milestone is a subordinate target.
The user can change the objective; record that change explicitly.

**Route selection.** Inspect the actual target and resume prior evidence first.
Use or adapt an adequate existing solution before inventing another. Research
the uncertain part, then act when a supported route is available. For competing
explanations, choose a cheap test whose outcomes change the next decision.
Do not assign invented probabilities or keep a failed branch alive because of
prior effort. Continue independent useful work when one branch is blocked.

**Evidence assessment.** State the prediction, acceptance condition and relevant
limits before a consequential experiment. Separate observation, interpretation,
empirical support and proof. A failed invocation is not a negative result;
missing telemetry is not proof of absence. After an ambiguous submission,
reconcile authoritative status before repeating an action that could duplicate
effects. Preserve unsuccessful approaches when they will prevent rediscovery.

**Verification.** Check the intended effect on the intended target using evidence
independent of the action's success message. Match checks to the claim: a saved
artifact or exercised user path for implementation; controlled measurements for
performance; a proof of the exact statement for universal mathematics. Search
for counterexamples, hidden assumptions, degenerate cases and published
equivalents. Static validation does not prove truth, compliance or novelty.

**Failed verification and remaining gaps.** Reject the failed completion claim,
retain the counterexample or missing evidence, and choose a justified recovery
or independent action. Suspend only when no useful authorized action remains.

**Checkpoint.** For continuing work, persist the original objective, current
evidence, source/version, failures, dependencies, owned changes, pending effects
and next discriminating action in the authorized project. For a small task,
the response can be the checkpoint; do not create a research database by default.
Resource exhaustion suspends research. It does not establish impossibility or
resolve the original objective.

Report the outcome, decisive evidence, changes, remaining gaps and next action.
Use **SOLVED** only when the original completion condition is verified. Otherwise
distinguish **SUPPORTED**, **REFUTED** (the specified claim), **INCONCLUSIVE** and
**BLOCKED**. Keep branch results separate from global resolution.

## Load only the relevant detail

- [Evidence and experiments](references/evidence-and-experiments.md): research
  sources, discriminating tests, noisy measurements and independent verification.
- [Unfinished research and repository work](references/research-work.md): classify
  defects, missing implementations, theory and measurement gaps; preserve progress.
- [Mathematical discovery](references/mathematical-discovery.md): persistent claims,
  symbolic laws, proof dependencies and the exact resolution gate.
- [Game theory and design](references/game-theory-and-design.md): strategic agents,
  counterplay, evaluation incentives and player-facing mechanics when relevant.

The logic blocks make ordering reviewable with SkillWren. They do not execute
the task or enforce the agent's behavior. Use actually available tools and the
user's authorization; the skill does not grant additional permissions.
