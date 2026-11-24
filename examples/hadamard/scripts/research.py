"""Persistent mathematical discovery CLI. No observation command can solve Hadamard."""
import argparse
import json
from pathlib import Path
import sys

from math_research.coverage import coverage_report
from math_research.objective import HADAMARD
from math_research.planner import plan
from math_research.store import Project, ResearchError
from math_research.workflow import seed, iterate


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    graph = sub.add_parser("graph")
    graph.add_argument("--mermaid", action="store_true")
    sub.add_parser("plan")
    sub.add_parser("resume")
    coverage = sub.add_parser("coverage")
    coverage.add_argument("--limit", type=int, default=128)
    run = sub.add_parser("iterate")
    run.add_argument("--candidates", type=int, default=256)
    run.add_argument("--proofs", type=int, default=2)
    run.add_argument("--lean")
    run.add_argument("--fresh-reason")
    resolve = sub.add_parser("resolve")
    resolve.add_argument("direction", choices=("prove", "refute"))
    resolve.add_argument("--proof-body", type=Path, required=True)
    resolve.add_argument("--lean")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            project = Project.create(args.project)
            state = seed(project)
            result = {"objective": state["objective"], "resolution": state["resolution"],
                      "claims": len(state["claims"]), "branches": list(state["branches"])}
        else:
            project = Project(args.project)
            state = project.snapshot()
            if args.command == "status":
                result = {"objective": state["objective"], "objective_hash": state["objective_hash"],
                          "resolution": state["resolution"], "session": state["session"],
                          "claims": {key: node["status"] for key, node in state["claims"].items()},
                          "remaining_proof_obligations": [key for key, node in state["claims"].items()
                                                          if node["status"] == "UNRESOLVED"]}
            elif args.command == "graph":
                result = {"nodes": state["claims"], "edges": state["edges"],
                          "objective": HADAMARD["id"], "resolution": state["resolution"]}
                if args.mermaid:
                    ids = {key: f"n{i}" for i, key in enumerate(state["claims"])}
                    print("flowchart TD")
                    for key, node in state["claims"].items():
                        print(f"  {ids[key]}[{json.dumps(key + ' | ' + node['status'])}]")
                    for edge in state["edges"]:
                        connector = " --> " if edge["kind"] == "requires" else f" -. {edge['kind']} .-> "
                        print("  " + ids[edge["dependency"]] + connector + ids[edge["claim"]])
                    return 0
            elif args.command == "plan":
                result = plan(project)
            elif args.command == "coverage":
                result = coverage_report(args.limit)
            elif args.command == "resume":
                project.resume()
                result = plan(project)
            elif args.command == "iterate":
                result = iterate(project, args.candidates, args.proofs, args.lean, args.fresh_reason)
            elif args.command == "resolve":
                result = project.resolve(args.direction, args.proof_body.read_text(encoding="utf-8"), args.lean)
                print(json.dumps(result, indent=2))
                return 0 if result["verified"] else 1
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Research remains unresolved: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
