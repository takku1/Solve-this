# Persistent Hadamard discovery

The objective remains

\[
\forall k\in\mathbb Z_{>0},\quad\exists H\in\{-1,1\}^{4k\times4k}:
HH^\top=4kI.
\]

Only a certified proof of this statement or its negation resolves it. Successful
examples, known constructions, a failed search, finite grammar exhaustion and
resource exhaustion remain intermediate research.

Read [AUDIT.md](AUDIT.md), [PROGRAM.md](PROGRAM.md), and
[REQUIREMENTS.md](REQUIREMENTS.md) for the literature, measurable milestones and
implemented versus outstanding capabilities. The old run under
`experiments/hadamard/` is retained as a historical known-result reproduction.

From the repository root:

```powershell
py -3 -B scripts/research.py --project research/hadamard/session init
py -3 -B scripts/research.py --project research/hadamard/session plan
py -3 -B scripts/research.py --project research/hadamard/session coverage --limit 128
py -3 -B scripts/research.py --project research/hadamard/session iterate --candidates 256 --proofs 2
py -3 -B scripts/research.py --project research/hadamard/session status
py -3 -B scripts/research.py --project research/hadamard/session graph
```

Repeat the same iteration to reuse archived attempts rather than repeat search.
A changed method or hypothesis can justify `--fresh-reason "..."`; retain the
old attempt. `resume` starts another invocation without deleting knowledge.
The default grammar is a bounded first milestone. It is not an implementation
of every research branch or a guarantee of new mathematics.

`session/journal.json` is the persistent single-writer knowledge record. Its
events preserve known results, hypotheses, failures, proof dependencies and
checkpoints. `session/evidence/` contains adopted programs and actual Lean source
and checker logs. Back up the whole directory. A stale writer lock after a crash
requires inspection before removal; the tool never guesses another writer dead.

The local Lean checker certifies exact scalar cancellation lemmas for generated
block operators. Matrix-index lifting, parameter existence and unbounded coverage
remain separate unresolved claims. The formal objective is fixed in
`scripts/math_research/HadamardCore.lean`. To submit a genuinely proposed proof,
provide a proof term/tactic body, not a declaration of a weaker goal:

```powershell
py -3 -B scripts/research.py --project research/hadamard/session resolve prove --proof-body proposed-proof.txt
```

Use `resolve refute` for the negation. The checker rejects missing/unsupported
tools, timeouts, admitted proofs and unintended axioms. A failed attempt is
retained without changing the global status. English claim descriptions and
literature novelty still require independent semantic review.
