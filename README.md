# Solve This

One canonical skill for uncertain problems: find an adequate route, run decisive
experiments, pursue open discoveries and verify the original user outcome.

The main [SKILL.md](SKILL.md) uses **SkillWren control-flow notation**. It combines
the original general problem-solving scope with persistent research, exact
claim boundaries and a completion gate. A known solution takes a short path;
open mathematics gets the deeper discovery loop. Hadamard is an optional case
study, not the definition of the skill.

## Package

```text
SKILL.md                 canonical instructions
agents/openai.yaml       discovery and invocation metadata
references/              four focused, conditional references
install.ps1              install only the selected skill files
scripts/build.py         validate and build a portable package
examples/hadamard/       optional specialized runtime and its audit
docs/history/            original skill and archived revisions
research/                retained experiment evidence and open obligations
tests/                   packaging, control-flow and research-runtime checks
```

The default installed skill has six files and no runtime dependency on Python,
Lean, SkillWren or a model provider. The agent uses available tools. SkillWren
is a development-time validator; its syntax does not enforce agent compliance
or prove semantic equivalence. No comparative model-quality gain is claimed.

## Validate, build and install

From the repository, with Python 3.10+ and SkillWren installed:

```powershell
py -3 -B scripts/build.py --check-only
py -3 -B scripts/build.py --out .build/solve-this
py -3 -B -m pytest tests -q
.\install.ps1 -Target codex
```

`-Target claude` or `both` selects other supported destinations. `-UserRoot`
allows an isolated profile, `-WhatIf` previews changes, and `-Force` updates
existing package files. Unrelated files are preserved. Use
`-IncludeHadamard` only when the specialized runtime is wanted; see its
[instructions and limits](examples/hadamard/README.md).

The build contains the canonical files directly; there are no separately
maintained draft, tuned or discovery editions. Generated output stays in
`.build/` or another explicit output directory.

## Preserved history

The [original prose skill](docs/history/original/SKILL.md),
[previous mathematical version](docs/history/mathematical-discovery-skill.md)
and [consolidation notes](docs/history/README.md) explain the lineage. Exact old
package builds and validation artifacts are archived with hashes. They are
historical evidence, not alternative active entrypoints.

The [Hadamard research](research/hadamard/RESULTS.md) and
[SkillWren work](research/skillwren/RESULTS.md) retain their actual results and
unresolved obligations. Passing software tests and known mathematical examples
do not resolve their broader research objectives.
