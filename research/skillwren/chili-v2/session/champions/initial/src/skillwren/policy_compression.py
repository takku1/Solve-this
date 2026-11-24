"""Proof-gated, resumable compression of executable finite Boolean policies."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess

from .finite_policy import RULES, audit, canonical, decision_certificate, validate


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def measure(policy, metric):
    text = canonical(policy)
    if metric == "bytes":
        return len(text.encode("utf-8"))
    if metric != "tokens":
        raise ValueError("unsupported metric")
    try:
        import tiktoken
    except ImportError as exc:
        raise ValueError("exact tokens require the optional tiktoken dependency") from exc
    return len(tiktoken.get_encoding("cl100k_base").encode(text, disallowed_special=()))


def rewrites(expr, allowed):
    """Local algebraic proposals; the independent truth-table auditor is final."""
    if not isinstance(expr, list):
        return
    op, parts = expr[0], expr[1:]
    if op == "not":
        x = parts[0]
        if "constants" in allowed and type(x) is bool:
            yield "constants", not x
        if "double-negation" in allowed and isinstance(x, list) and x[0] == "not":
            yield "double-negation", x[1]
    else:
        if "constants" in allowed:
            absorbing, neutral = (False, True) if op == "and" else (True, False)
            if any(type(x) is bool and x == absorbing for x in parts):
                yield "constants", absorbing
            kept = [x for x in parts if not (type(x) is bool and x == neutral)]
            if len(kept) != len(parts):
                yield "constants", neutral if not kept else kept[0] if len(kept) == 1 else [op] + kept
        if "idempotence" in allowed:
            unique = []
            for x in parts:
                if x not in unique:
                    unique.append(x)
            if len(unique) != len(parts):
                yield "idempotence", unique[0] if len(unique) == 1 else [op] + unique
        dual = "or" if op == "and" else "and"
        if "absorption" in allowed:
            kept = [x for x in parts if not (isinstance(x, list) and x[0] == dual
                    and any(y in parts for y in x[1:]))]
            if kept and len(kept) < len(parts):
                yield "absorption", kept[0] if len(kept) == 1 else [op] + kept
        if "factoring" in allowed:
            for i, left in enumerate(parts):
                for j in range(i + 1, len(parts)):
                    right = parts[j]
                    if not (isinstance(left, list) and isinstance(right, list)
                            and left[0] == dual and right[0] == dual):
                        continue
                    for common in left[1:]:
                        if common not in right[1:]:
                            continue
                        a, b = list(left[1:]), list(right[1:])
                        a.remove(common)
                        b.remove(common)
                        fold = lambda xs: xs[0] if len(xs) == 1 else [dual] + xs
                        replacement = [dual, common, [op, fold(a), fold(b)]]
                        yield "factoring", [op] + [x for k, x in enumerate(parts) if k not in (i, j)] + [replacement] if len(parts) > 2 else replacement
    for i, part in enumerate(parts):
        for rule, replacement in rewrites(part, allowed):
            changed = list(expr)
            changed[i + 1] = replacement
            yield rule, changed


def compress(source, metric="tokens", budget=128, max_worlds=65536, history=None):
    validate(source, max_worlds)
    if type(budget) is not int or budget < 0 or budget > 10000:
        raise ValueError("budget must be an integer in 0..10000")
    pinned = {"source_sha256": digest(source), "metric": metric,
              "max_worlds": max_worlds, "engine_sha256": engine_hash()}
    if history is None:
        history = {"format": "skillwren-compression-search-1", "objective": pinned,
                   "original": source, "attempts": [], "frontier": [source], "seen": [digest(source)]}
    else:
        # Reconstruct instead of trusting mutable checkpoints or supplied verdicts.
        if history.get("objective") != pinned or history.get("original") != source:
            raise ValueError("immutable objective or engine changed")
        previous = history.get("attempts", [])
        replay = compress(source, metric, len(previous), max_worlds)
        if replay["history"] != history:
            raise ValueError("search checkpoint does not match deterministic replay")
        history = copy.deepcopy(history)
    original_size = measure(source, metric)
    accepted = [source] + [a["candidate"] for a in history["attempts"] if a["verdict"] == "PROVEN_EQUIVALENT"]
    best = min(accepted, key=lambda p: (measure(p, metric), canonical(p)))
    remaining = budget
    allowed = set(source["rewrite_policy"]["allowed"])
    seen = set(history["seen"])
    while history["frontier"] and remaining:
        parent = history["frontier"][0]
        proposals = list(rewrites(parent["constraint"], allowed))
        for rule, expression in proposals:
            candidate = dict(parent, constraint=expression)
            key = digest(candidate)
            if key in seen:
                continue
            if not remaining:
                break
            seen.add(key)
            history["seen"].append(key)
            result = audit(source, candidate, max_worlds)
            size = measure(candidate, metric)
            history["attempts"].append({"rule": rule, "candidate": candidate,
                "parent_sha256": digest(parent), "sha256": key, "size": size, **result})
            remaining -= 1
            if result["verdict"] == "PROVEN_EQUIVALENT":
                history["frontier"].append(candidate)
                if (size, canonical(candidate)) < (measure(best, metric), canonical(best)):
                    best = candidate
        if all(digest(dict(parent, constraint=e)) in seen for _, e in proposals):
            history["frontier"].pop(0)
    # Ties retain the original artifact, not a gratuitous rewrite.
    improved = measure(best, metric) < original_size
    if not improved:
        best = source
    certificate = {"format": "skillwren-finite-certificate-1", "objective": pinned,
        "source": source, "candidate": best, "candidate_sha256": digest(best),
        "metric": metric, "original_size": original_size, "candidate_size": measure(best, metric),
        "strictly_smaller": improved, "audit": audit(source, best, max_worlds),
        "derivation": history["attempts"],
        "decision_risk": decision_certificate(source, best, max_worlds),
        "state": "BRANCH_EXHAUSTED" if not history["frontier"] else "BUDGET_EXHAUSTED",
        "resolution": "UNRESOLVED: arbitrary natural-language and deployed-model semantics"}
    return {"certificate": certificate, "history": history}


def engine_hash():
    from . import finite_policy
    return hashlib.sha256(Path(__file__).read_bytes() + Path(finite_policy.__file__).read_bytes()).hexdigest()


def verify(certificate, source, candidate, lean=None):
    pinned = certificate["objective"]
    if (certificate.get("format") != "skillwren-finite-certificate-1"
            or source != certificate["source"] or candidate != certificate["candidate"]
            or digest(source) != pinned["source_sha256"]
            or digest(candidate) != certificate["candidate_sha256"]
            or pinned["engine_sha256"] != engine_hash()
            or pinned["metric"] != certificate["metric"]):
        raise ValueError("certificate/artifact/engine binding mismatch")
    limit = pinned["max_worlds"]
    result = audit(source, candidate, limit)
    if result["verdict"] != "PROVEN_EQUIVALENT" or result != certificate["audit"]:
        raise ValueError("equivalence audit failed")
    before, after = measure(source, certificate["metric"]), measure(candidate, certificate["metric"])
    if (before != certificate["original_size"] or after != certificate["candidate_size"]
            or (after < before) != certificate["strictly_smaller"]
            or after > before or decision_certificate(source, candidate, limit) != certificate["decision_risk"]):
        raise ValueError("measurement or decision certificate failed")
    # Authorization is about the applied derivation, not just mathematical truth.
    known = {digest(source): source}
    allowed = set(source["rewrite_policy"]["allowed"])
    for step in certificate["derivation"]:
        parent = known.get(step["parent_sha256"])
        proposed = step["candidate"]
        if (parent is None or step["rule"] not in allowed or
                not any(rule == step["rule"] and dict(parent, constraint=expr) == proposed
                        for rule, expr in rewrites(parent["constraint"], allowed))):
            raise ValueError("unauthorized derivation")
        checked = audit(source, proposed, limit)
        if (step["sha256"] != digest(proposed) or step["size"] != measure(proposed, certificate["metric"])
                or any(step.get(key) != value for key, value in checked.items())):
            raise ValueError("invalid derivation evidence")
        if checked["verdict"] == "PROVEN_EQUIVALENT":
            known[digest(proposed)] = proposed
    if digest(candidate) not in known:
        raise ValueError("candidate has no authorized derivation")
    if "formal" in certificate:
        if lean is None:
            raise ValueError("formal receipt requires a caller-trusted --lean for independent replay")
        from .policy_proof import prove
        if prove(source, candidate, lean, limit) != certificate["formal"]:
            raise ValueError("formal receipt does not match independent kernel replay")
    return {"verified": True, "strictly_smaller": after < before, "audit": result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--metric", choices=("tokens", "bytes"), default="tokens")
    parser.add_argument("--budget", type=int, default=128)
    parser.add_argument("--max-worlds", type=int, default=65536)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verify", type=Path, help="certificate to replay against source and --candidate")
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--lean", type=Path, help="caller-trusted Lean 4 executable; certify or replay exact obligations")
    args = parser.parse_args(argv)
    lock = None
    lockpath = None
    try:
        source = json.loads(args.source.read_text(encoding="utf-8-sig"))
        if args.verify:
            if not args.candidate:
                raise ValueError("--verify requires --candidate")
            result = verify(json.loads(args.verify.read_text(encoding="utf-8")), source,
                            json.loads(args.candidate.read_text(encoding="utf-8")), args.lean)
            print(json.dumps(result, indent=2))
            return 0
        if not args.output:
            raise ValueError("compression requires a new --output directory")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        lockpath = args.output.with_name(args.output.name + ".lock")
        lock = lockpath.open("x", encoding="utf-8")
        lock.write(str(os.getpid()))
        lock.flush()
        history = None
        if args.resume:
            history = json.loads((args.output / "search.json").read_text(encoding="utf-8"))
        elif args.output.exists():
            raise ValueError("output exists; use --resume to replay a checkpoint")
        result = compress(source, args.metric, args.budget, args.max_worlds, history)
        if args.lean:
            from .policy_proof import prove
            result["certificate"]["formal"] = prove(source, result["certificate"]["candidate"],
                                                  args.lean, args.max_worlds)
        args.output.mkdir(parents=True, exist_ok=args.resume)
        for name, value in (("policy.json", result["certificate"]["candidate"]),
                            ("certificate.json", result["certificate"]), ("search.json", result["history"])):
            path = args.output / name
            temporary = path.with_suffix(".pending")
            temporary.write_text(canonical(value) + "\n", encoding="utf-8")
            temporary.replace(path)
        print(json.dumps({k: v for k, v in result["certificate"].items()
                          if k not in {"source", "candidate", "derivation", "formal"}}, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, RecursionError, subprocess.SubprocessError) as exc:
        print("OPEN: " + str(exc), file=sys.stderr)
        return 2
    finally:
        if lock is not None:
            lock.close()
            lockpath.unlink()
