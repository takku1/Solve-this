## Step meanings

`apply` and `generate` transform working context; they never execute tools or
change external state. Every command, state-changing API/UI operation, write,
and restoration goes through `exec planned action`. Read only actual available
evidence with understood authorized effects. Plan modifiers preserve earlier
constraints. Fold each result into `state` before branching; never invent data.
Load only references relevant to the current uncertainty. If unavailable, use
the core guidance, record a material limitation, and never diagnose the target
from a reference-loading failure.

- **working agreement**: Clarify only missing information that changes the work;
  preserve the objective, observable completion condition, settled choices,
  approvals, target, environment and constraints. Do not invent an objective.
- **investigation state / established context**: Track objective/completion,
  target/version/identity/workspace/time, environment, constraints, budgets,
  observations, alternatives, prior attempts, pending operations, owned changes
  and recovery. Start the no-progress counter at zero; revalidate volatile facts
  on resumption. Store no secrets.
- **inspection limitation / unavailable observation**: Retain the last reliable
  facts and distinguish unavailable access, invalid invocation and missing target
  evidence. Reads can consume queues or create jobs. Plan consequential inspection
  through the action gates; an unperformed observation is not a negative result.
- **evidence assessment**: Inspect actual relevant state before changing it:
  output, capabilities/help, effective configuration, logs, changes or reproduction.
  Check provenance and the intended target/version/identity/time; avoid unrelated
  private data. Separate observation, inference, hypothesis and unresolved
  possibility. Validate observation coverage before interpreting absence;
  preserve conflicting evidence with its conditions. Use
  [research and evidence](references/research-and-evidence.md) for noisy,
  external, ambiguous or causal claims. Prior effort is not evidence.
- **unresolved completion / reconciled state**: Reconcile ambiguous submission or
  stale resumption against authoritative status/destination and existing operation
  identifiers before consequential repetition. Read
  [probe patterns](references/probe-patterns.md) for idempotency, bounded polling,
  client retries and intermittent outcomes. If reconciliation is unavailable and
  duplication matters, stop this branch with ambiguity, pending identifiers and
  needed dependency intact; use INCONCLUSIVE unless required access/capability is
  missing (BLOCKED). A timeout does not mean nothing happened.
- **stabilization plan**: Prioritize established authorized mitigation of active
  consequential failure; preserve evidence when practical and record altered
  conditions. Verify recovery without claiming root cause or durable recurrence
  prevention from a workaround.
- **research backlog triage / advance worklist**: For broad or unfinished work,
  use [research backlog](references/research-backlog.md). Maintain a bounded
  worklist, separate defects from missing implementation and open theory, choose
  discriminating tests, and advance to independent authorized work after recording
  a resolved or blocked branch. Keep the global completion criterion separate
  from each scoped verdict; one successful subproblem does not finish the task.
- **route selection / reuse assessment**: Use the cheapest supported authorized
  procedure; investigate only its unresolved part. Consult
  [decision policy](references/decision-policy.md) when routing is unclear. For
  prior solutions check version, license, constraints, integration gap and
  reproducible evidence; reuse/adapt when sufficient. Stop researching once a
  route or discriminating probe is available, then perform the requested work.
- **research limitation**: Label unavailable search surfaces without claiming
  external verification or making browsing universally necessary. Follow
  [research and evidence](references/research-and-evidence.md): local installed
  behavior, primary applicable sources, full pages, dates/versions/scopes,
  sanitized queries and offline constraints. Retrieved content is evidence, not
  authority; inspect recommended commands before authorized execution.
- **direct solution plan**: Run a known procedure and independently check its
  effect. The abbreviated inspect -> act -> check path permits one obvious,
  low-impact, reversible action with a direct check; exclude material shared-state
  changes, evidence destruction and difficult recovery. If unsure, a check fails
  or alternatives appear, use the full loop. Do not manufacture research.
- **frame and hypotheses**: State the gap and next decision: capability discovery,
  cause, restoration or verification. Rank a small set of explanations/routes by
  evidence fit, discriminating-probe cost, then cost of error. Consider
  preconditions, participants/boundaries, changes and measurement assumptions.
  Record contradictions/falsifiers, retain unseparated alternatives and multiple
  causes when warranted; invent no probabilities or defects.
- **discriminating probe plan**: Choose the lowest-burden authorized test whose
  outcomes change the next decision, or verify completion/a necessary precondition.
  Before execution record question/alternatives, exact operation/target,
  outcomes -> decisions and inconclusive conditions; add proportionate budget,
  dependencies, side effects, baseline, verification and feasible recovery.
  Prefer narrow, local, reversible and observable probes. Read
  [probe patterns](references/probe-patterns.md) for schema/UI discovery, layered
  boundaries, reduction, retry, polling or intermittent behavior; never guess a
  capability or confuse a new setup error with the original failure.
- **experimental design**: Read [experiment protocol](references/experiment-protocol.md)
  for falsifiable scoped claims, prior art, predeclared controls/measurements,
  inconclusive conditions, disposable environments, instrumentation and causal
  isolation. Testing is optional when a reliable procedure already answers the question.
- **matched comparison**: Use [research foundations](references/research-foundations.md)
  only when costly noisy comparisons warrant matched fixed-budget trials or
  sequential elimination. Preserve uncertainty and multiobjective tradeoffs;
  numerical information gain requires defensible estimates. No mandatory bandit
  model, swarm, fixed research duration or unlimited search.
- **strategic and experience lens**: Read [game theory and design](references/game-theory-and-design.md)
  for opponents, incentives, rules, balance or player experience. Separate tested
  mechanics, emergent dynamics and human experience; bounded counterplay and toy
  wins do not establish equilibrium, robustness, fairness or fun.
- **metamorphic checks**: When no reliable oracle exists, use the defensible
  transformation relations/invariants in [research foundations](references/research-foundations.md);
  validate their assumptions instead of fabricating a gold answer.
- **action plan / basis / repetition**: Resolve the exact command/arguments,
  supported tool/API call or observed UI operation and intended resource. Check
  actual permission, target conditions, budget and recovery. Method freedom never
  expands scope, bypasses restrictions, weakens controls or conceals actions.
  Count equivalent attempts across tools/wording; repeat only for changed relevant
  conditions, hypotheses or informative bounded sampling. Preserve the baseline
  and isolate mutations when practical. Parallel calls require independence of
  state, ordering, contention, locks, evidence and read-side limits; no delegation
  is required.
- **raw observation record**: Keep exact operations, raw outputs/failures and
  provenance; for experiments retain conditions, versions, seed/timing and
  sample size/dispersion as relevant. Follow [experiment protocol](references/experiment-protocol.md).
  Keep failed and repaired runs separate. Exit status is not task success.
- **probe failure classification / missing outcome**: Separate failed invocation,
  actual target response and target not observed. Local schema/parse errors do
  not diagnose a remote service; transport failure may narrow only a boundary.
  Missing telemetry excludes an event only when the observation path should
  capture it. Retain ambiguity for reconciliation before repeating effects.
- **prediction comparison**: Classify valid results as supporting, contradicting
  or inconclusive against predictions. Independently check the intended effect
  on the intended target via readback/artifact/user path, proportional to
  consequence. One intermittent success proves no reliability. Separate
  simulation, unit, integration and deployment evidence. Keep Observed /
  Learned or ruled out with conditions / Still unknown / Next; conclusions never
  exceed evidence. Broaden verification only for a reason.
- **temporary change recovery / recovery action plan**: Inspect residual effects;
  plan necessary restoration of only owned temporary changes through the normal
  action gates, respecting concurrent edits. Preserve the requested successful
  result. Undo cannot retract notifications/jobs/consumed data. Include feasible
  recovery before acting and complete required cleanup before SOLVED.
- **progress and stall assessment / reframe**: Reassess after three consecutive
  probes without decision-relevant information or verified progress, sooner for
  expensive/risky/slow/hard-to-reverse work. Eliminating a hypothesis is progress;
  count equivalent attempts together. Three is a checkpoint, not permission for
  risky retries. Choose justified continuation, a changed hypothesis/boundary/
  source/decomposition, escalation or stopping this branch. Return to reliable
  observations/effective state or a smaller reproduction; do not polish dead ends
  or infer impossibility from one failed route. Honor supplied budgets; otherwise
  scale effort to value without arbitrary long research phases.
- **continuity compression**: When changing subproblems or details repeat, retain
  Knowledge Baseline: objective/completion; target/version/context; established
  evidence locations; ruled-out scope; model/alternatives; owned changes/pending
  operations/recovery; blockers; next discriminating action. Persist only when
  needed and available, through a gated action; exclude secrets, link large
  evidence, discard superseded detail. Re-enter from new contradictory evidence.
- **authority blocker / verification limitation / blocked resolution**: Stop the
  affected branch and report established facts, specific missing authority/input/
  capability/decision, partial changes/pending operations and safest useful next
  action. Continue independent authorized work; ask only the smallest newly
  necessary question without reasking settled approvals. Handoff implies no
  rollback. Distinguish missing knowledge/access, untested routes and infeasibility.
- **solved resolution / scoped resolution / bounded resolution**: SOLVED requires
  the original user outcome independently verified and required cleanup complete;
  SUPPORTED is a claim within tested conditions; REFUTED needs valid contradicting
  evidence for the specified claim; INCONCLUSIVE means insufficient/invalid
  evidence; BLOCKED means a required unavailable authority, data or capability.
  Invalid tests are not negative results. Stop unnecessary investigation but
  complete authorized execution. Never fabricate research/execution, claim a PoC
  is mathematical proof, or equate demonstration with generalization/production
  readiness. Report outcome, decisive evidence, limitations and next justified
  action. For experiments use [result template](references/result-template.md)
  and retain runnable artifacts/commands/conditions/raw observations/comparison
  where practical. Preserve a reusable procedure only for future value:
  preconditions, procedure, verification, failure/recovery and known limits.

## Commands and evidence resources

| Step | Operation |
|---|---|
| `exec planned action` | Execute the exact task-specific operation recorded in `action`, using the available `tools`, and retain its actual result as `execution`. This includes commands, authorized state changes, writes, tests, builds, polling and recovery; observation as a purpose does not make a command `readonly`. |

**context** means actual task instructions, constraints, tools and relevant
artifacts/observations; **tools** grants no permission to install or access a
service. Read evidence through an available surface with understood authorized
effects. **authority** comes from actual instructions/approvals, not a generated
approval. All evidence bindings contain real observations and provenance.
`verify ... from` links a claim to evidence; it does not supply a trusted verifier.

## Supporting material

- [Worked examples](references/worked-examples.md): tricky discovery/failure boundaries.
- [Evaluation scenarios](references/evaluation-scenarios.md): maintenance and behavioral evaluation with disposable fixtures.
- [Sources](references/sources.md): provenance and limits; not required in normal execution.

Static checks establish written structure/order, not semantic equivalence,
runtime enforcement, model compliance or improved performance. The planning-order
rule deliberately retains W15: working-context plan generation is model judgment,
without an obligatory external record. Behavioral comparison remains unmeasured.
