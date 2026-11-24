"""Backward obligations plus diversity, not success-count rewards."""
from .objective import HADAMARD


def plan(project, target=None):
    state = project.snapshot()
    target = target or HADAMARD["id"]
    if target not in state["claims"]:
        raise ValueError("Unknown planning target")
    unresolved = project.blocked_dependencies(target)
    support = [e["dependency"] for e in state["edges"]
               if e["claim"] == target and e["kind"] == "may_support"]
    ranking = sorted(state["branches"].items(),
                     key=lambda pair: (pair[1]["attempts"] > 0, pair[1]["last_event"], pair[0]))
    return {"objective_hash": state["objective_hash"], "target": target,
            "unresolved_prerequisites": unresolved, "possible_support": support,
            "branches": [{"id": name, **data} for name, data in ranking],
            "decision_policy": "First attack unresolved prerequisites; among viable scoped tests preserve branch diversity and revisit least-recently explored branches. Generality, novelty review and exact test cost are qualitative judgments, not invented probabilities.",
            "resolution": state["resolution"], "session": state["session"]}
