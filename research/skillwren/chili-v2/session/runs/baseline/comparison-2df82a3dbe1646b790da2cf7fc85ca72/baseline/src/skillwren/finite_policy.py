"""Finite Boolean policies: typed validation and an independent exact auditor.

No natural-language interpretation, model-performance or deployment claim is
implied. Enumeration is deliberately bounded and never samples.
"""
import itertools
import json


FORMAT = "skillwren-finite-policy-1"
ROLES = {"obs", "choice", "aux", "param"}
RULES = {"constants", "idempotence", "double-negation", "absorption", "factoring"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def validate(policy, max_worlds=65536):
    required = {"format", "scope", "variables", "constraint", "objective", "rewrite_policy"}
    if not isinstance(policy, dict) or set(policy) != required or policy["format"] != FORMAT:
        raise ValueError("unsupported policy format or fields")
    if not isinstance(policy["scope"], dict) or not policy["scope"]:
        raise ValueError("explicit nonempty scope is required")
    if not isinstance(policy["objective"], dict):
        raise ValueError("objective must be explicit")
    variables = policy["variables"]
    if not isinstance(variables, dict) or not variables:
        raise ValueError("variables must be a nonempty mapping")
    for name, spec in variables.items():
        if not isinstance(name, str) or not name.isidentifier():
            raise ValueError("invalid variable name")
        if not isinstance(spec, dict) or set(spec) != {"role", "type"}:
            raise ValueError("invalid variable declaration")
        if spec["role"] not in ROLES or spec["type"] != "Bool":
            raise ValueError("only declared Boolean variables with typed roles are supported")
    if type(max_worlds) is not int or not 1 <= max_worlds <= 65536:
        raise ValueError("max_worlds must be in 1..65536")
    if 2 ** len(variables) > max_worlds:
        raise ValueError("OPEN: exhaustive world budget exceeded")
    permission = policy["rewrite_policy"]
    if (not isinstance(permission, dict) or set(permission) != {"allowed", "optimize"}
            or permission["optimize"] != ["constraint"]
            or not isinstance(permission["allowed"], list)
            or any(not isinstance(rule, str) or rule not in RULES for rule in permission["allowed"])):
        raise ValueError("unsupported rewrite authorization")
    count = [0]

    def check(expr, depth=0):
        count[0] += 1
        if depth > 64 or count[0] > 10000:
            raise ValueError("expression size/depth budget exceeded")
        if type(expr) is bool:
            return
        if isinstance(expr, str) and expr in variables:
            return
        if not isinstance(expr, list) or not expr or not isinstance(expr[0], str):
            raise ValueError("invalid Boolean expression")
        op = expr[0]
        if op not in {"not", "and", "or"} or (len(expr) != 2 if op == "not" else len(expr) < 3):
            raise ValueError("unsupported operator or arity")
        for part in expr[1:]:
            check(part, depth + 1)
    check(policy["constraint"])
    return policy


def evaluate(expr, world):
    if type(expr) is bool:
        return expr
    if isinstance(expr, str):
        value = world[expr]
        if type(value) is not bool:
            raise ValueError("Boolean assignment required")
        return value
    if expr[0] == "not":
        return not evaluate(expr[1], world)
    values = [evaluate(x, world) for x in expr[1:]]
    return all(values) if expr[0] == "and" else any(values)


def assignments(names):
    names = sorted(names)
    for values in itertools.product((False, True), repeat=len(names)):
        yield dict(zip(names, values))


def audit(source, candidate, max_worlds=65536):
    """Compare complete constraints, a stronger gate than aux projection.

    Equality includes all metadata. Strict inclusion gets an exclusive verdict;
    it is never permission to deploy an equivalent rewrite.
    """
    validate(source, max_worlds)
    validate(candidate, max_worlds)
    metadata = lambda p: {k: v for k, v in p.items() if k != "constraint"}
    if metadata(source) != metadata(candidate):
        return {"verdict": "REDESIGN", "reason": "scope, roles, objective or authority changed"}
    removed, added = [], []
    checked = 0
    for world in assignments(source["variables"]):
        before = evaluate(source["constraint"], world)
        after = evaluate(candidate["constraint"], world)
        checked += 1
        if before and not after and not removed:
            removed.append(world)
        if after and not before and not added:
            added.append(world)
    verdict = ("PROVEN_EQUIVALENT" if not removed and not added else
               "CERTIFIED_TIGHTENING" if removed and not added else
               "CERTIFIED_RELAXATION" if added and not removed else "REFUTED")
    return {"verdict": verdict, "worlds_checked": checked,
            "removed_witness": removed, "added_witness": added,
            "scope": "complete declared finite Boolean relation, not LLM behavior"}


def decisions(policy, observations, max_worlds=65536):
    """Execute the finite policy; existentially quantify aux variables.

    Observed and parameter values must be supplied, never optimized.
    """
    validate(policy, max_worlds)
    variables = policy["variables"]
    fixed = {n for n, s in variables.items() if s["role"] in {"obs", "param"}}
    if set(observations) != fixed or any(type(v) is not bool for v in observations.values()):
        raise ValueError("supply exactly the observed and parameter Boolean values")
    choice = {n for n, s in variables.items() if s["role"] == "choice"}
    auxiliary = {n for n, s in variables.items() if s["role"] == "aux"}
    result = []
    for action in assignments(choice):
        if any(evaluate(policy["constraint"], dict(observations, **action, **extra))
               for extra in assignments(auxiliary)):
            result.append(action)
    return result


def decision_certificate(source, candidate, max_worlds=65536):
    result = audit(source, candidate, max_worlds)
    if result["verdict"] != "PROVEN_EQUIVALENT":
        return {"verdict": "OPEN", "reason": "complete relation equivalence is required"}
    fixed = {n for n, spec in source["variables"].items() if spec["role"] in {"obs", "param"}}
    for world in assignments(fixed):
        if not decisions(source, world, max_worlds):
            return {"verdict": "OPEN", "reason": "an observation has no feasible action; optimal finite risk is undefined",
                    "witness": world}
    return {"verdict": "PROVEN_EQUIVALENT", "deficiency_upper": "0",
            "loss_class": "all finite real losses on identical declared observation/action domains",
            "risk_model": "same feasible decision rules with the same observation distribution",
            "argument": "equal relations imply identical projected feasible actions and decision rules; "
                        "therefore their risk sets and optimal risks coincide",
            "excluded": ["LLM text interpretation", "undeclared actions", "changed observation channels"]}
