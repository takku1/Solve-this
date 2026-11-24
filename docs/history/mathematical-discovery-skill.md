---
name: solve-this
description: Pursue unresolved mathematical objectives through literature-grounded discovery, persistent conjectures and proof obligations, exact falsification, symbolic generalization, and formal proof. Use for open mathematical research and construction synthesis; intermediate experiments never replace the original objective.
---

# Solve This

Invent mathematics that can be verified. Preserve the question until it is answered.

`DISCOVER -> CONJECTURE -> EXPERIMENT -> FALSIFY -> GENERALIZE -> PROVE -> MAP GAPS -> REPEAT`

Read [mathematical discovery](references/mathematical-discovery.md) before research.
For Hadamard, start with the project's audit and measurable research program;
the universal objective is immutable. Known constructions and successful tests
are intermediate research. A suspended invocation is not a solved conjecture.

```contract
inputs:
  request, context, project
order:
  verify#objective before exec research action
  verify#resolution before return#mathematical-resolution
  exec persist checkpoint before return#suspended
```

```logic
research:
  require request exists
    otherwise:
      abort with "State the original mathematical objective."
  if the original objective or its quantified domain is unclear:
    ask user for the missing original objective or domain as clarification
    apply objective clarification with clarification as request
  read original mathematical objective from request as objective
  verify #objective the objective retains the original quantifiers, domain, and proof or refutation criterion from objective
    otherwise:
      abort with "The original objective is missing or has been replaced by a benchmark."
  require current research operations fit existing authorization and resources
    otherwise:
      abort with "Research awaits the specific missing authority or resource; the objective remains unresolved."
  exec initialize or resume project from tools as initialized
  verify the objective and resumed history were accepted from initialized
    otherwise:
      abort with "Project initialization or replay failed; the conjecture remains unresolved."
  read persistent mathematical knowledge from project as state

  label research-loop:
  verify the stored objective matches the immutable original and prior evidence is intact from state
    otherwise:
      abort with "Objective drift or invalid evidence; preserve the record and repair continuity."
  if new literature evidence could change the next decision and an audit fits the invocation budget:
    exec literature audit from tools as literature
    apply provenance reconciliation with literature as state
  require a literature-grounded audit and measurable research program precede additional search
    otherwise:
      apply research program with state as program
      exec persist research program {program} from tools as recorded
      verify the audit and program were saved from recorded
        otherwise:
          abort with "The research program could not be persisted; no new search is justified."
      read persistent mathematical knowledge from project as state
      return to research-loop
  apply proof gap planning with state as plan
  if an exact proof or refutation of the original objective is proposed:
    exec independent formal resolution check from tools as certificate
    verify #resolution the certificate proves or refutes the exact original objective with accepted axioms and no unresolved dependencies from certificate
      otherwise:
        apply failed proof and remaining gaps with certificate as state
        return to checkpoint
    return #mathematical-resolution certificate as resolution
  if a justified next action fits the remaining invocation budget:
    exec research action {plan} from tools as evidence
    apply classify and exchange discovery with evidence as state
    apply adversarial generalization with state as state
    exec persist mathematical knowledge from tools as saved
    verify the observation and remaining gaps were saved from saved
      otherwise:
        abort with "Knowledge persistence failed; report the partial research state before continuing."
    read persistent mathematical knowledge from project as state
    return to research-loop

  label checkpoint:
  apply unresolved checkpoint with state as checkpoint
  exec persist checkpoint {checkpoint} from tools as saved
  return #suspended saved as research-state
```

## Step meanings

- **objective clarification**: Fill only missing objective information. A lemma,
  finite benchmark, restricted search or milestone can be a subproblem; it cannot
  replace the original mathematical statement. Preserve prior choices/authority.
- **provenance reconciliation**: Record source version/date, precise claim and
  assumptions, publication/review status, evidence location and conflicts. Distinguish
  external established results, local formal proofs, conjectures and experiments.
  Never silently import a sufficient construction as an equivalence. Consult
  [research and evidence](references/research-and-evidence.md).
- **research program**: Audit prior art and barriers first, then define research
  branches, symbolic coverage, proof dependencies, milestones, adversarial controls
  and resource accounting. No milestone is a new global completion condition.
- **proof gap planning**: Resume successes, failures and open obligations before
  proposing work. Work backward from the objective and forward from established
  lemmas. Prioritize reusable parameterized laws, meaningful coverage bridges and
  cheap decisive falsifiers; preserve diverse branches. Read
  [research backlog](references/research-backlog.md), [decision policy](references/decision-policy.md),
  and [research foundations](references/research-foundations.md) when relevant.
- **classify and exchange discovery**: Persist the exact claim/domain/hypotheses,
  evidence, failed attempts, restrictions, dependencies and novelty status. Use
  KNOWN_RESULT, COUNTEREXAMPLE_FOUND, EMPIRICALLY_SUPPORTED, LEMMA_PROVEN,
  COVERAGE_EXPANDED or BRANCH_EXHAUSTED only at their documented scope. Share
  constraints/lemmas between branches; reject proof cycles. A falsified candidate
  never refutes the global conjecture. Formal status certifies the exact formal
  type; an English paraphrase still needs statement-equivalence review.
- **adversarial generalization**: Seek counterexamples, degenerate cases, hidden
  hypotheses, circular reasoning and published equivalents. Derive symbolic
  Gram/orthogonality obligations, then separate identity proofs from parameter
  existence, signs, dimensions, lifting and coverage. Read
  [experiment protocol](references/experiment-protocol.md),
  [probe patterns](references/probe-patterns.md),
  [game theory and design](references/game-theory-and-design.md), and
  [mathematical discovery](references/mathematical-discovery.md). Numerical,
  modular, bounded SAT/SMT or persuasive language-model checks cannot substitute
  for a universally quantified theorem.
- **failed proof and remaining gaps**: Preserve the attempt, exact checker output,
  counterexamples, missing tools/assumptions and unresolved dependencies; update
  the research plan. An invalid invocation concerns the tool, not the conjecture.
- **unresolved checkpoint**: Record budget spent, branch results, remaining proof
  obligations and next discriminating action. BUDGET_EXHAUSTED is resumable
  suspension. Missing authority or tools are explicit blockers. Only
  CONJECTURE_PROVEN and CONJECTURE_REFUTED resolve the original mathematics.
  Never claim a proof because a bounded experiment or current invocation finished.

## Commands and resources

`PY` is the available Python 3.10+ interpreter (`py -3 -B` on Windows).
`tools` means actually available tools, within existing authority; `project` is
the persistent project path. Every action needs understood side effects,
proportionate limits and recovery. Do not automatically install tools or spend
provider usage. These commands record research; the agent still supplies ideas,
source interpretation, proof attempts and justified next actions.
The included runtime targets Hadamard. Other original objectives need their own
reviewed immutable statement and proof adapter; never silently initialize them
as Hadamard projects.

| Step | Operation |
|---|---|
| Initialize/resume | `PY <skill>/scripts/research.py --project <path> init`, then `status` and `plan`; existing claims are reused. |
| Literature audit | Read relevant local artifacts and online primary sources using available search tools; record source versions, provenance, conflicts and coverage assumptions in the project. No universal browser command is invented. |
| Persist research program | Save the grounded audit and program in the authorized project directory; record the adopted milestones and source versions before search. |
| Research action | Choose an actual scoped symbolic/exact/formal operation. First Hadamard milestone: `PY <skill>/scripts/research.py --project <path> iterate --candidates 256 --proofs 2`. The bounded block grammar proves no global conjecture; use `--fresh-reason` only for a justified changed attempt. |
| Independent formal resolution check | `PY <skill>/scripts/research.py --project <path> resolve prove --proof-body <file>` or `resolve refute ...`; the fixed Lean wrapper checks the original proposition or its negation, never a supplied weaker goal. |
| Persist mathematical knowledge | The CLI journals its own results atomically; additional sources/claims/dependencies use the documented `math_research.store.Project` API. Persist actual evidence and unresolved obligations, not invented passes. |
| Persist checkpoint | The iteration writes a resumable budget checkpoint. For other actions call `Project.checkpoint(remaining, reason)`; retain pending effects and failed approaches. |

## Supporting material

- [Result template](references/result-template.md): scoped research results and unresolved global objective.
- [Worked examples](references/worked-examples.md): ordinary discovery/failure boundaries.
- [Evaluation scenarios](references/evaluation-scenarios.md): maintenance and behavioral tests.
- [Sources](references/sources.md): provenance; no combined-performance claim.
- [Diagnostic workflow](references/diagnostic-workflow.md): preserved operational procedure for ordinary nonmathematical tasks. Its task-completion verdicts do not govern open mathematical research.
- [Hadamard audit](references/hadamard-audit.md) and [research program](references/hadamard-program.md): literature-grounded starting point and measurable milestones.

SkillWren checks written control flow, not mathematical truth or agent compliance.
The journal provides continuity and application-level integrity, not host isolation.
Novelty, independent statement review and unresolved proofs remain explicit.
