# Optional Hadamard research runtime

This worked case preserves the existing journal, symbolic coverage, signed-block
synthesizer, proof dependencies and Lean proof gates. It is not a general-purpose
discovery engine and does not resolve the Hadamard conjecture.

From the repository root:

```powershell
py -3 -B examples/hadamard/scripts/research.py --project .build/hadamard init
py -3 -B examples/hadamard/scripts/research.py --project .build/hadamard iterate --candidates 256 --proofs 2
py -3 -B examples/hadamard/scripts/research.py --project .build/hadamard status
```

Use Python 3.10+ and, for formal checks, an already installed Lean 4.33.1.
Missing checkers leave claims unresolved. Initialization is persistent and
resuming the same configuration reuses prior results. `resolve prove` or
`resolve refute` accepts a proof body only inside the fixed original-proposition
wrapper; it never accepts a substituted weaker objective.

Read the [audit](references/hadamard-audit.md) and
[program](references/hadamard-program.md) before additional search. The runtime
adopts their exact bytes. The moved implementation is unchanged; previous
sessions and proof receipts remain in `research/hadamard` in the source checkout.
Their historical paths and reports describe the earlier layout.

Install the optional files with `install.ps1 -IncludeHadamard` or build them with
`scripts/build.py --include-hadamard`. The default skill does not include them.
The research profile preserves the original universal conjecture: reproducing
Sylvester/Paley or proving a scalar Gram identity cannot satisfy it. Full matrix
lifting, parameter existence, universal coverage and novelty remain open.
