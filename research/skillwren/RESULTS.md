# SkillWren discovery run

Implemented, tested and applied a complete **finite Boolean policy compression
pipeline** to `Z:\SkillWren`. The original broad research objective remains
**UNRESOLVED**. This is an engineering completion with a stated mathematical
domain, not a solution to arbitrary natural-language compression or Hadamard.

## Delivered behavior

`py -3 -m skillwren compress` now generates authorized symbolic rewrites,
independently checks the complete finite relation, measures full canonical JSON
using exact tokens or bytes, selects a strictly smaller equivalent policy and
keeps the original as fallback. It records unsuccessful proposals and supports
deterministic replay and resumption with the original objective and engine
pinned. Source, candidate, derivation, roles, scope, metric and optional proof
receipt are checked again by the verifier. The evaluator executes policies with
fixed observed/parameter values and existential auxiliary variables.

An optional caller-trusted Lean 4 executable certifies the emitted concrete
Boolean equivalence and a general theorem transporting optimal decisions
across equal feasible relations. Both checked declarations use **no axioms**.
This proves the emitted statements, not correctness of every Python function or
the fidelity of a prose-to-policy translation.

The package, generated plugin and installed editable package are updated. The
installed module now resolves to `Z:\SkillWren\src\skillwren`. The previous
14-file repair and unrelated target changes were preserved. The reviewed delta
contains 12 files, with original/updated bytes and hashes in
[change/manifest.json](change/manifest.json). Installation needed no dependency
downloads; the existing exact tokenizer and local Lean were used.

## Measured results and verification

| Check | Result | Evidence |
|---|---|---|
| Full example, exact cl100k_base tokens | 183 → 116 (36.61% smaller) | [certificate](demo-v2/certificate.json) |
| Three frozen fixtures, complete canonical bytes | 1,941 → 1,402 (27.77% smaller) | [Chili comparison](chili-v2/summary.json) |
| Chili exploration and fresh confirmation | 3 paired repetitions each; accepted experimental candidate | [session](chili-v2/session/state.json) |
| Complete target regression suite | 507 passed, 3 skipped | [target log](target-tests.txt) |
| Solve-this regression suite | 37 passed | [log](solve-this-regressions.txt) |
| Installed package and bundled plugin replay | Both passed, including fresh Lean execution | [installed](installed-replay.txt), [plugin](plugin-replay.txt) |

The benchmark compares a frozen identity baseline against enabling the existing
audited rewrite engine. It measures configured finite fixtures, not novel law
discovery, production acceptance, universal compression or model quality. Both
versions use identical canonical formatting and complete metadata. Offline
certificates are separate audit evidence; sending them to a model adds context.

## Falsification retained

An adversarial review exposed an invalid risk inference in the first version:
equal relations can both have observations with no feasible action, so their
optimal-risk difference is not defined. The fix explicitly checks every context
for feasibility. Otherwise the risk claim remains `OPEN` with a witness. The
regression test covers this case. The corrected demonstration includes an
explicit refusal action and its scoped finite-model deficiency bound is zero.

`demo/` and `chili/` preserve the earlier run. Their zero-risk assertions for
infeasible policies are **withdrawn**; use `demo-v2/` and `chili-v2/`. The earlier
byte measurements do not establish those withdrawn risk claims. Failed packaging
and stale-installed-package replay logs are retained alongside their passing
replacements. No failed approach was silently erased.

## Research grounding

The audit started with SkillWren's frozen v23 semantic-sufficiency formulation,
its explicit future Wilderbeast interface, compact-conversion design and the
implemented metrics/selection/certgate boundaries. Sources and the measurable
program were recorded in [OBJECTIVE.md](OBJECTIVE.md) before implementation.

[LLMLingua-2](https://arxiv.org/abs/2403.12968) supports empirical learned prompt
compression as a useful comparison, not a universal semantic guarantee.
[Prover-Verifier Games](https://arxiv.org/abs/2108.12099) informed the design of
fixed verification gates and separate size incentives: the proposal generator
cannot reward itself for skipping correctness. This implementation does not
train PVG agents or claim a game-theoretic equilibrium.

The current discovery instructions were applied as an agent workflow. The
Hadamard-specific `research.py` was not misused to label SkillWren as a Hadamard
project. The retained implementation checkpoints are target-native; the broader
proof obligations are recorded separately below.

## Remaining proof obligations

| Obligation | State |
|---|---|
| Exact equality and authorized compression of supported finite Boolean policies | Implemented, exhaustive checks and optional kernel certification |
| Decision-risk transport in identical total finite decision models | Established under explicit assumptions; known mathematics |
| Ground arbitrary prose into a complete typed semantics | OPEN |
| Infer deficiency bounds for actual LLM behavior over a declared loss class | OPEN; finite relation certificates cannot replace model data |
| Richer domains, binders and capture-avoiding alpha conversion | OPEN; unsupported syntax rejected |
| Unbounded/adaptive statistical certification and infinite-family guarantees | OPEN |
| Host scope classification and full Wilderbeast integration | OPEN |

These dependencies prevent a solved verdict for the original broad objective.
They require additional semantics, implementations and evidence, rather than
more redundant matrix orders or additional finite examples.
