"""Emit closed Boolean equivalence obligations and execute a caller-trusted Lean.

The receipt never chooses an executable. The verifier supplies its own Lean
path, regenerates the statement and reruns the kernel. No injected proof text.
"""
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

from .finite_policy import audit, validate


CORE = """import Std

def Optimal {O A L : Type} [LE L] (S : O → A → Prop) (loss : O → A → L)
    (o : O) (a : A) : Prop := S o a ∧ ∀ b, S o b → loss o a ≤ loss o b

theorem sameOptimal {O A L : Type} [LE L] (S T : O → A → Prop)
    (h : ∀ o a, S o a ↔ T o a) (loss : O → A → L) (o : O) (a : A) :
    Optimal S loss o a ↔ Optimal T loss o a := by
  constructor
  · rintro ⟨ha, hm⟩
    exact ⟨(h o a).mp ha, fun b hb => hm b ((h o b).mpr hb)⟩
  · rintro ⟨ha, hm⟩
    exact ⟨(h o a).mpr ha, fun b hb => hm b ((h o b).mp hb)⟩

"""


def obligation(source, candidate, max_worlds=65536):
    validate(source, max_worlds)
    if audit(source, candidate, max_worlds)["verdict"] != "PROVEN_EQUIVALENT":
        raise ValueError("formal proof requires an equivalent typed policy")
    names = {name: "_v" + str(i) for i, name in enumerate(sorted(source["variables"]))}

    def emit(expr):
        if type(expr) is bool:
            return "true" if expr else "false"
        if isinstance(expr, str):
            return names[expr]
        if expr[0] == "not":
            return "(!" + emit(expr[1]) + ")"
        op = " && " if expr[0] == "and" else " || "
        return "(" + op.join(emit(x) for x in expr[1:]) + ")"
    binders = " ".join(names.values())
    return (CORE + "theorem Certified : ∀ (" + binders + " : Bool), "
            + emit(source["constraint"]) + " = " + emit(candidate["constraint"])
            + " := by decide\n\n#print axioms Certified\n#print axioms sameOptimal\n")


def prove(source, candidate, lean, max_worlds=65536):
    lean = Path(lean).resolve(strict=True)
    text = obligation(source, candidate, max_worlds)
    version = subprocess.run([str(lean), "--version"], capture_output=True, text=True,
                             encoding="utf-8", timeout=15, check=True).stdout.strip()
    if not version.startswith("Lean (version 4."):
        raise ValueError("expected Lean 4")
    with tempfile.TemporaryDirectory(prefix="skillwren-policy-proof-") as folder:
        path = Path(folder) / "Proof.lean"
        path.write_text(text, encoding="utf-8")
        result = subprocess.run([str(lean), str(path)], capture_output=True,
                                encoding="utf-8", timeout=60)
    output = result.stdout + result.stderr
    if result.returncode or "sorryAx" in output or "error:" in output:
        raise ValueError("Lean did not certify the obligation: " + output[:2000])
    declarations = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", output)
    empty = output.count("does not depend on any axioms")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    if len(declarations) + empty != 2 or any(
            a.strip() not in allowed for group in declarations for a in group.split(",") if a.strip()):
        raise ValueError("missing or unexpected Lean axiom report")
    return {"checker": "Lean 4 kernel", "version": version,
            "binary_sha256": hashlib.sha256(lean.read_bytes()).hexdigest(),
            "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "source": text, "output": output,
            "scope": "Boolean constraint equivalence and optimal-decision transport theorem"}
