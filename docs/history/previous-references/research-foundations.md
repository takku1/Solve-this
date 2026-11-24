# Research foundations and adoption decisions (2026-11-23)

This is a design synthesis, not a claim that Solve This is empirically validated. Source results are scoped to their original settings. Use methods conditionally, not as a checklist.

## 1. Sequential experimental design / active learning

Research: Di Fiore et al. (2024), https://doi.org/10.1007/s11831-024-10064-z ; Zhang et al. (2023), https://www.nature.com/articles/s42256-023-00719-0 .

Adopt: choose experiments for **decision-changing information**, not maximum data collection. When candidates are costly and measurements comparable, use sequential selection. Define what each possible result would change before executing. Do not invent posterior probabilities or expected information gain numbers without a calibrated model.

## 2. Fixed-budget best-arm identification

Research: Barrier et al. (2023), https://proceedings.mlr.press/v201/barrier23a ; Kone et al. (2024), https://proceedings.mlr.press/v238/kone24a.html .

Adopt: when comparing alternative implementations with stochastic outcomes, define a shared budget, matched trials, a baseline, and an elimination rule. Retain uncertainty and Pareto tradeoffs for multiobjective comparisons. Do not force bandit algorithms onto deterministic one-off tasks.

## 3. Game theory and adversarial robustness

Adopt conditionally when success depends on another agent's choices, incentives, or counter-strategy. Model players, feasible actions, information, payoffs, and time horizon. Ask what a rational or adversarial responder could do to defeat the candidate. Test exploitable strategies with counterplay, not only a cooperative opponent. Equilibrium or minimax analysis requires an actual defined game and assumptions; do not assert Nash equilibrium from a few simulations. Safety and authorization remain binding.

## 4. Game design / playtesting

Research: Hunicke, LeBlanc, Zubek, *MDA*, https://game-developers.org/info/uploads/2022/09/MDA.pdf ; critique and extension https://www.mdpi.com/2078-2489/12/10/395 .

Adopt: distinguish **mechanics** (implemented rules), **dynamics** (emergent interaction), and **experience** (player-perceived outcome). Separate deterministic rule checks from simulations, counterplay, and human playtests. A mechanically correct system may still be unbalanced, unfun, unclear, or fail the target experience. Declare intended player behavior and experience before testing; collect qualitative feedback without treating it as objective proof. Use paper prototypes where cheaper than code.

## 5. Metamorphic testing and oracle problems

Research: https://pmc.ncbi.nlm.nih.gov/articles/PMC7252536/ .

Adopt: when expected output is unknown, define relationships that should hold under controlled input transformations (e.g., invariance, monotonicity, symmetry, conservation). Check the relation, not a fabricated gold answer. Relations themselves may be wrong; validate their assumptions.

## 6. Causal identification and adversarial evaluation

Research: https://www.nature.com/articles/s42256-023-00719-0 ; https://www.nist.gov/system/files/documents/2024/02/15/ID034%20-%202024-02-02%2C%20Microsoft%2C%20Comments%20on%20AI%20EO%20RFI.pdf .

Adopt: identify confounders and matched controls before attributing improvements. Adversarial probes supplement rather than replace systematic evaluation. A counterexample refutes only the properly quantified claim it contradicts.

## Non-adoptions

- No mandatory Bayesian posterior, numerical scoring formula, autonomous infinite search, self-play engine, or LLM swarm.
- No ungrounded claims of optimality, Nash equilibrium, generalization, or production readiness.
- No fixed research duration; choose the cheapest reliable evidence that changes the next decision.
