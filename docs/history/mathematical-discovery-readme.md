# Solve This

A persistent mathematical discovery skill: generate laws and conjectures,
falsify them, generalize surviving structure, certify exact claims, and retain
the remaining proof gaps across research sessions.

**The original mathematical objective stays immutable.** Reproducing known
mathematics, verifying examples and completing engineering milestones do not
resolve a conjecture. Only an independently checked proof or refutation of its
original statement does. Exhausted budgets produce resumable unresolved states.

`DISCOVER -> CONJECTURE -> EXPERIMENT -> FALSIFY -> GENERALIZE -> PROVE -> MAP GAPS -> REPEAT`

## Hadamard research project

[Research audit](research/hadamard/AUDIT.md) ·
[Measurable program](research/hadamard/PROGRAM.md) ·
[Implementation scope](research/hadamard/REQUIREMENTS.md) ·
[Run and resume](research/hadamard/README.md)

The initial executable milestone includes a persistent knowledge journal, seven
communicating research branches, a proof dependency graph, symbolic coverage,
signed-block construction proposals, exact counterexamples and real Lean checks
of generated scalar Gram lemmas. Full family lifting, parameter-existence proofs,
novelty and the universal Hadamard conjecture remain unresolved.

The online audit includes primary Hadamard literature, construction catalogues,
FunSearch/AlphaTensor, prover-verifier games, game design and Lean proof validation.
Game scores guide exploration; proof acceptance remains fixed and independent.

```powershell
py -3 -B scripts/research.py --project research/hadamard/session init
py -3 -B scripts/research.py --project research/hadamard/session iterate --candidates 256 --proofs 2
py -3 -B scripts/research.py --project research/hadamard/session status
```

The helper runtime targets Hadamard. Other mathematical objectives require their
own reviewed immutable statement and proof adapter. This is an early discovery
system, not a claim of autonomous general mathematical invention.

## Install and validate

Use `install.ps1` to copy the current skill, references, research runtime and
trusted Lean core into the selected skills directory. It preserves the existing
overwrite checks and supports `-WhatIf`; installation is not automatic.
Python 3.10+ runs the research infrastructure. The narrow formal backend uses
an already installed Lean 4.33.1; absence or failure leaves claims unresolved.
No provider usage or toolchain download is automatic.

```powershell
py -3 -B scripts/build_discovery.py --check-only
py -3 -B -m pytest tests -q
```

The current portable SkillWren package is [solve-this-discovery](solve-this-discovery/SKILL.md).
`solve-this/` and `solve-this-tuned/` retain the earlier PoC-oriented revisions;
their completion rules do not govern this research architecture.
The older [SkillWren investigation](investigations/skillwren/RESULTS.md) remains
historical evidence. Ordinary nonmathematical diagnosis is preserved in
[diagnostic workflow](references/diagnostic-workflow.md).

Static control-flow validation and software tests do not prove semantic
equivalence, mathematical novelty, model compliance or the conjecture. Formal
certificates apply only to their exact types. No controlled behavioral gain from
this combined skill has been established.
