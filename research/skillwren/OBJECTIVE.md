# SkillWren discovery objective

Complete the unfinished compression and certification work without weakening
the original semantics or treating successful examples as universal results.
Baseline: SkillWren 0.13.3 plus the previously tested 14-file repair. Preserve
those changes and all unrelated work in Z:\SkillWren.

The literature-grounded audit is the target's frozen semantic-sufficiency
FORMULATION.md (v23), compact-conversion.md, and its implemented metrics,
selection and certification modules. LLMLingua and LLMLingua-2 demonstrate useful
empirical prompt compression, not universal behavioral equivalence. Blackwell's
comparison of experiments motivates explicitly declaring observations, decisions
and loss classes. Adaptive selection requires independent statistical evidence
unless a complete deterministic equivalence check replaces estimation.

Implementation milestone: a runnable finite typed policy compressor with exact
token measurement, independent exhaustive equivalence checks, persistent search,
adversarial controls, executable policy decisions and replayable certificates.
The original canonical policy is the fallback. All metadata and variable roles
remain fixed. Only explicitly authorized rewrites can be applied.

Acceptance: the complete existing test suite and new adversarial tests pass;
candidate output is strictly smaller in the declared full-serialization metric;
all Boolean observation/choice assignments are checked; corrupted certificates,
changed goals and unsupported policies fail closed. Optional Lean certificates
must execute the kernel on the exact emitted Boolean equivalence theorem.

This milestone does not close arbitrary natural-language semantics, arbitrary
LLM decision risk, infinite domains, host scope classification or the entire
Wilderbeast integration. They remain explicit unresolved dependencies of the
original objective. No finite-policy success may be reported as solving them.
