# Solve This

An evidence-driven problem-solving and experimental proof-of-concept skill, evolved from [Freestyle](https://github.com/takku1/freestyle).

**Find what works. Test what matters. Claim only what the evidence permits.**

Use `$solve-this` in Codex or `/solve-this` in Claude Code to investigate uncertain problems, research existing solutions, construct bounded tests, and verify outcomes. The skill is not a formal proof engine: a passing PoC supports only its tested scope.

## Workflow

`UNDERSTAND → DISCOVER → HYPOTHESIZE → EXPERIMENT → VERIFY → RESOLVE`

Known solutions take a fast path. Experiments are optional and must be discriminating, safe, and proportionate. A run may end SOLVED, SUPPORTED, REFUTED, INCONCLUSIVE, or BLOCKED.

## Install

Copy this repository's `SKILL.md` and `references/` into `~/.agents/skills/solve-this/` or `~/.claude/skills/solve-this/`, or use `install.ps1` on Windows.

## Evidence

This is a new skill revision, not a validated improvement over Freestyle. Behavioral A/B testing remains to be done.

## Research-informed methods

The skill now conditionally applies active learning, fixed-budget candidate comparison, game-theoretic counterplay, mechanics/dynamics/experience playtesting, and metamorphic testing. See [research foundations](references/research-foundations.md), [game theory and design](references/game-theory-and-design.md), and [decision policy](references/decision-policy.md). These are guidance, not proven improvements in agent performance.
