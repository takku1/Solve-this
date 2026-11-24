# Game theory and design

Use this lens when agents adapt strategically, incentives distort evaluation,
or the requested outcome concerns player behavior. A routine software task
does not need to be turned into a game.

## Strategic behavior

Identify the players, available actions, information, timing and incentives.
Distinguish a cooperative optimization problem from competition, coordination
and adversarial verification. Examine exploitable best responses, information
asymmetry, commitment, collusion or reward manipulation when relevant. A strong
result against a fixed scripted opponent is not evidence of equilibrium or
robustness against adaptive opposition.

Choose tests that expose a strategy's assumptions: change the opponent,
information available or payoff conditions; test counterplay and edge cases.
State whether the result concerns a specific opponent, a restricted strategy
class or an actual proved equilibrium. Do not invent payoff probabilities.

## Evaluation incentives

Separate proposal incentives from acceptance. Reward fewer tokens, faster search
or better scores only after fixed correctness conditions pass. A generator must
not weaken its own success criterion or supply the only evidence that it passed.
Use counterexample search, independent checkers and held-out confirmation where
the evidence is statistical. Keep evaluation rules fixed during comparison.

[Prover-Verifier Games](https://arxiv.org/abs/2108.12099) provides a research
connection for checkable answers. A fixed software verifier is a useful design
choice; it does not by itself implement PVG training or prove an equilibrium.

## Player-facing design

Separate the intended player experience from mechanics and numerical balance.
Identify meaningful decisions, readable feedback, counterplay and the behavior
the incentives actually encourage. Test representative play sequences rather
than optimizing an isolated score. A game can be balanced and still be tedious,
or engaging and intentionally asymmetric; evaluate against the requested goal.

Use simulations to test mechanical hypotheses and playtesting to test human
experience. Record player population, context and observed behavior. Neither a
simulation nor an attractive design document demonstrates that people enjoy the
result. Revise the mechanic that produced the observation, then test again.
