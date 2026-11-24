# Game theory and game design lens

Use this reference when the problem involves competing agents, strategic incentives, game rules, player experience, balance, or emergent behavior. Skip for unrelated tasks.

## Strategic-game model

Specify actors, available actions, information/hidden information, payoff objectives, state transitions, and horizon. Ask whether opponents are cooperative, competitive, boundedly rational, scripted, or adaptive. Distinguish what an agent wants from what it can actually observe or execute.

For each candidate solution: identify a best-response or plausible counter-strategy, construct a bounded adversarial test, and record whether it breaks the desired outcome. If comparing strategies, hold opponent policy, seed, budget, and environment constant when possible; test across diverse opponents before claiming robustness. Use minimax regret or exploitability only if the underlying quantities are defined and measured. Do not infer equilibrium from a small tournament.

## Game design evaluation ladder

1. **Rules:** Is the mechanic internally coherent? Check legality, state invariants, termination, edge cases, and interaction order.
2. **Dynamics:** What happens in repeated play? Use toy simulations, strategy comparisons, degenerate-strategy search, and sensitivity tests.
3. **Experience:** Does the intended experience actually occur? Observe playtests, comprehension, perceived agency, pacing, and enjoyment; preserve qualitative contradictions.
4. **Iteration:** Change one major mechanism when possible, rerun matched baselines, and preserve failures.

Example: a racing-card encounter system may obey all rules yet produce permanent stalling. A simulated no-progress policy can falsify a claim that the rules force progression. Human playtests are still needed to assess tension and fun.

## Design cautions

- An optimal strategy under a toy opponent may be exploitable against real players.
- Self-play can hide shared blind spots; include fixed, diverse, and adversarial baselines.
- A statistical win rate is not automatically fun, fair, or understandable.
- Simulated player preferences are hypotheses, not substitutes for human feedback.
