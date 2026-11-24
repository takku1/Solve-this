"""Measure explicitly selected skill context; no model calls or pruning."""
import json
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "experiments/skillwren"
sys.path.insert(0, str(TARGET / "src"))
from skillwren.metrics import MeasurementError, compare


def expanded_selected(folder, names):
    pieces = []
    for name in sorted(names):
        raw = (folder / name).read_bytes()
        pieces += [b"<!-- file: " + name.encode() + b" -->\n", raw]
        if not raw.endswith(b"\n"):
            pieces.append(b"\n")
    return b"".join(pieces)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=ROOT / "solve-this")
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("context-measurements.json"))
    args = parser.parse_args()
    baseline = Path(__file__).with_name("baseline-skill")
    names = ["SKILL.md"] + [p.relative_to(baseline).as_posix()
                            for p in sorted((baseline / "references").glob("*.md"))]
    candidate_names = ["SKILL.md"] + [p.relative_to(args.candidate).as_posix()
                                      for p in sorted((args.candidate / "references").glob("*.md"))]
    pairs = {
        "solve_this_entry": ((baseline / "SKILL.md").read_bytes(),
                             (args.candidate / "SKILL.md").read_bytes()),
        "solve_this_declared_context": (expanded_selected(baseline, names),
                                       expanded_selected(args.candidate, candidate_names)),
        "shipped_optimization_example": ((TARGET / "examples/optimization/original.md").read_bytes(),
                                         (TARGET / "examples/optimization/SKILL.md").read_bytes()),
    }
    reports = {"source_commit": "a5d7d40fab57b90bad0d07bf736479ff23b70808",
               "selected_baseline_files": names,
               "selected_candidate_files": candidate_names,
               "candidate": str(args.candidate),
               "limits": "Size only. No semantic equivalence or behavioral preservation inferred.",
               "measurements": {}}
    for name, (original, candidate) in pairs.items():
        reports["measurements"][name] = {}
        for metric in ("characters", "tokens"):
            try:
                result = compare([original], candidate, metric=metric)
            except MeasurementError as error:
                result = {"unavailable": str(error)}
            reports["measurements"][name][metric] = result
    path = args.out
    path.write_text(json.dumps(reports, indent=2) + "\n", encoding="utf-8")
    for name, metrics in reports["measurements"].items():
        print(name)
        for metric, result in metrics.items():
            if "unavailable" in result:
                print(f"  {metric}: unavailable")
            else:
                print(f"  {metric}: {result['original']['count']} -> "
                      f"{result['compiled']['count']}; ratio {result['ratio']:.3f}")


if __name__ == "__main__":
    main()
