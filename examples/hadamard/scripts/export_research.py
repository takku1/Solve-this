"""Export inspectable views of a persistent project without changing its history."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from math_research.coverage import coverage_report
from math_research.planner import plan
from math_research.store import Project


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    project = Project(args.project)
    state = project.snapshot()
    args.out.mkdir(parents=True, exist_ok=True)
    artifacts = {"knowledge": state, "plan": plan(project), "coverage": coverage_report(128)}
    for name, value in artifacts.items():
        (args.out / (name + ".json")).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    graph = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("research.py")),
                            "--project", str(project.root), "graph", "--mermaid"],
                           capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    (args.out / "proof-graph.mmd").write_text(graph.stdout, encoding="utf-8")
    print(json.dumps({"objective_hash": state["objective_hash"], "resolution": state["resolution"],
                      "session": state["session"], "claims": len(state["claims"]),
                      "formal_proofs": len(state["proofs"]),
                      "unresolved_claims": sum(c["status"] == "UNRESOLVED" for c in state["claims"].values())}))


if __name__ == "__main__":
    main()
