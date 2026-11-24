"""Pinned Lean replay for an exact type, never an adapter-supplied pass flag."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess

PINNED_VERSION = "4.33.1"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
# This interface accepts proof terms/tactics, not arbitrary Lean commands or
# native computation. It is intentionally narrower than a general Lean project.
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|unsafe|implemented_by|extern|run_tac|"
                       r"elab|macro|set_option|theorem|def|namespace|section|end|import|"
                       r"initialize|native_decide)\b|#")


def local_lean():
    configured = os.environ.get("LEAN_BINARY")
    if configured:
        return configured
    direct = Path.home() / ".elan/toolchains" / ("leanprover--lean4---v" + PINNED_VERSION) / "bin"
    for name in ("lean.exe", "lean"):
        if (direct / name).is_file():
            return str(direct / name)
    candidate = shutil.which("lean")
    # Do not invoke an elan shim that may download a toolchain.
    return candidate if candidate and ".elan" not in str(Path(candidate).parent) else None


def check_proof(project, formal_type, body, lean=None, timeout=30):
    result = {"verified": False, "formal_type": formal_type,
              "scope": "exact elaborated statement; no novelty or global coverage inferred"}
    if not isinstance(formal_type, str) or not isinstance(body, str) or FORBIDDEN.search(formal_type + "\n" + body):
        return dict(result, status="REJECTED_PROOF_LANGUAGE")
    if not 0 < timeout <= 300:
        raise ValueError("Proof timeout must be in (0, 300] seconds")
    executable = lean if lean is not None else local_lean()
    if not executable or not Path(executable).is_file():
        return dict(result, status="CHECKER_UNAVAILABLE")
    core = Path(__file__).with_name("HadamardCore.lean").read_bytes()
    source = core + ("\n theorem Certified : " + formal_type + " :=\n" + body +
                     "\n#print axioms Certified\n").encode("utf-8")
    root = Path(project).resolve()
    evidence = root / "evidence"
    evidence.mkdir(exist_ok=True)
    source_hash = hashlib.sha256(source).hexdigest()
    source_path = evidence / (source_hash + ".lean")
    source_path.write_bytes(source)
    try:
        version = subprocess.run([str(executable), "--version"], capture_output=True,
                                 encoding="utf-8", timeout=min(timeout, 10))
        version_text = version.stdout.strip()
        if version.returncode or not re.search(r"version " + re.escape(PINNED_VERSION) + r"[, )]", version_text):
            return dict(result, status="UNSUPPORTED_CHECKER_VERSION", version=version_text)
        checked = subprocess.run([str(executable), str(source_path)], cwd=root,
                                 capture_output=True, encoding="utf-8", timeout=timeout,
                                 env=dict(os.environ, LEAN_PATH=""))
        output = checked.stdout + checked.stderr
    except subprocess.TimeoutExpired:
        return dict(result, status="CHECKER_TIMEOUT")
    except OSError as error:
        return dict(result, status="CHECKER_UNAVAILABLE", error=str(error))
    output_path = evidence / (source_hash + ".log")
    output_path.write_bytes(output.encode("utf-8"))
    axiom_lists = re.findall(r"'Certified' depends on axioms:\s*\[([^\]]*)\]", output)
    no_axioms = "'Certified' does not depend on any axioms" in output
    axioms = {item.strip() for item in axiom_lists[-1].split(",") if item.strip()} if axiom_lists else set()
    acceptable = no_axioms or bool(axiom_lists) and axioms <= STANDARD_AXIOMS
    verified = checked.returncode == 0 and acceptable and "sorryAx" not in output
    return dict(result, verified=verified, status="VERIFIED" if verified else "PROOF_REJECTED",
                version=version_text, binary_sha256=hashlib.sha256(Path(executable).read_bytes()).hexdigest(),
                binary=str(Path(executable).resolve()),
                trusted_core_sha256=hashlib.sha256(core).hexdigest(), axioms=sorted(axioms),
                source=source_path.relative_to(root).as_posix(), source_sha256=source_hash,
                output=output_path.relative_to(root).as_posix(),
                output_sha256=hashlib.sha256(output_path.read_bytes()).hexdigest(), exit_code=checked.returncode)


def replay_resolution(project, receipt, formal_type):
    """A journal's pass flag is never enough to restore a resolved objective."""
    core = Path(__file__).with_name("HadamardCore.lean").read_bytes()
    path = Path(project) / receipt["source"]
    source = path.read_bytes()
    prefix = core + ("\n theorem Certified : " + formal_type + " :=\n").encode("utf-8")
    suffix = b"\n#print axioms Certified\n"
    if not source.startswith(prefix) or not source.endswith(suffix):
        return False
    binary = receipt.get("binary")
    if not binary or not Path(binary).is_file():
        return False
    if hashlib.sha256(Path(binary).read_bytes()).hexdigest() != receipt["binary_sha256"]:
        return False
    body = source[len(prefix):-len(suffix)].decode("utf-8")
    return check_proof(project, formal_type, body, binary)["verified"]
