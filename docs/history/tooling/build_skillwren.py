"""Check and package the reviewed conversion using a local SkillWren checkout.

No installation, model evaluation, approval recording, or output replacement.
The explicit section and control-flow mappings below are review bookkeeping,
not a semantic-equivalence test.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "solve-this-draft"
REPORTS = ROOT / "skillwren-review"

# Source section -> literal landing anchor(s) in the conversion's step meanings.
SECTIONS = {
    "Rules": ["**evidence assessment**", "**prediction comparison**", "**action plan / basis / repetition**"],
    "Entry and working agreement": ["**working agreement**", "**route selection / reuse assessment**"],
    "Reference routing": ["**discriminating probe plan**", "**research limitation**"],
    "Research-grounded decision policy": ["**matched comparison**", "**strategic and experience lens**", "**metamorphic checks**"],
    "Operating modes": ["**direct solution plan**", "**frame and hypotheses**", "**experimental design**"],
    "Loop": ["**direct solution plan**", "**discriminating probe plan**"],
    "1. Inspect": ["**evidence assessment**", "**inspection limitation / unavailable observation**", "**stabilization plan**"],
    "2. Frame": ["**frame and hypotheses**"],
    "3. Hypothesize": ["**frame and hypotheses**"],
    "4. Discriminate": ["**discriminating probe plan**"],
    "5. Probe": ["**action plan / basis / repetition**", "**unresolved completion / reconciled state**", "**temporary change recovery / recovery action plan**"],
    "6. Verify and update": ["**probe failure classification / missing outcome**", "**prediction comparison**"],
    "Stall, budget, and reframe": ["**progress and stall assessment / reframe**"],
    "Continuity and escalation": ["**continuity compression**", "**authority blocker / verification limitation / blocked resolution**"],
    "Resolution and evidence verdicts": ["**solved resolution / scoped resolution / bounded resolution**"],
    "Converge": ["**route selection / reuse assessment**", "**solved resolution / scoped resolution / bounded resolution**", "**continuity compression**"],
    "Anti-patterns": ["**probe failure classification / missing outcome**", "**progress and stall assessment / reframe**", "**action plan / basis / repetition**"],
    "Supporting material": ["## Supporting material", "**action plan / basis / repetition**"],
}

# Target block boundaries -> quoted source fragment justifying that control flow.
# Every source line is also separately accounted for; these attach exact logic
# statements for SkillWren's reverse check, including owned repair jumps.
TRACE = [
    ("require request exists", "generate investigation state", "Clarify an unclear objective", "input"),
    ("generate investigation state", "label inspect:", "Establish the outcome", "input"),
    ("require the next inspection", "label planning:", "Inspection is not automatically non-invasive", "gate"),
    ("if volatile state", "if an active consequential", "On resumption, revalidate volatile state", "branch"),
    ("if an active consequential", "    if required recovery", "prioritize authorized stabilization", "branch"),
    ("    if required recovery", "    apply route selection", "restore only changes you own", "recovery"),
    ("    apply route selection", "      label choosing:", "Use a reliable procedure when cheaper than discovery", "branch"),
    ("      label choosing:", "        if feasibility", "For capability discovery, candidates may be possible supported routes", "branch"),
    ("        if feasibility", "        if costly noisy", "**Experimental PoC:**", "branch"),
    ("        if costly noisy", "  label action-ready:", "For costly noisy comparisons", "branch"),
    ("  label action-ready:", "  require the next action", "Stop when the objective is verified", "branch"),
    ("  require the next action", "  require the plan changes", "Use explicit user budgets", "gate"),
    ("  require the plan changes", "  generate action plan", "If every plausible result leads to the same action", "gate"),
    ("  generate action plan", "  read relevant target conditions", "Never treat missing authority as a technical obstacle", "gate"),
    ("  read relevant target conditions", "  read prior attempt", "Add a time or attempt limit and recovery plan", "gate"),
    ("  read prior attempt", "  exec planned action", "Reconcile outcome before repeating", "gate"),
    ("  exec planned action", "  require the outcome inspection", "First establish whether the probe executed correctly", "recovery"),
    ("  require the outcome inspection", "  label completion:", "Verify against the original completion condition", "gate"),
    ("  label completion:", "  label reassessing:", "Verify against the original completion condition", "gate"),
    ("  label reassessing:", "```", "On reassessment, choose deliberately", "recovery"),
]


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def inventory():
    sources = {"SKILL.md": (ROOT / "SKILL.md").read_bytes()}
    sources.update({p.relative_to(ROOT).as_posix(): p.read_bytes()
                    for p in sorted((ROOT / "references").glob("*.md"))})
    candidate = (DRAFT / "SKILL.md").read_text(encoding="utf-8")
    requirements, non_requirements = [], []
    by_line = {}
    for name, raw in sources.items():
        lines = raw.decode("utf-8-sig").splitlines()
        section = ""
        for number, line in enumerate(lines, 1):
            text = line.strip()
            if not text:
                continue
            heading = re.match(r"^#{2,3} (.+)$", text)
            if heading:
                section = heading[1]
            if text.startswith(("#", "```")) or text in ("---", "```text"):
                non_requirements.append({"file": name, "lines": [number, number],
                                         "reason": "Heading or Markdown/YAML delimiter; content accounted separately."})
                continue
            if name != "SKILL.md":
                if (DRAFT / name).read_bytes() != raw:
                    raise ValueError(f"Supporting reference changed: {name}")
                lands = [text]
            elif text.startswith(("name:", "description:")):
                lands = [text]
            elif not section:
                lands = ["Find what works. Test what matters. Claim only what the evidence permits.",
                         "Communicate concise findings"]
            else:
                lands = SECTIONS[section]
            item = {"id": f"R{len(requirements) + 1:03}", "kind": "step-meaning",
                    "text": line, "source": [{"file": name, "lines": [number, number]}],
                    "evidence": "none", "lands": list(lands)}
            requirements.append(item)
            by_line[(name, number)] = item

    target_lines = candidate.splitlines()
    logic_start = target_lines.index("```logic")
    source_lines = sources["SKILL.md"].decode("utf-8-sig").splitlines()
    for start, end, quoted, kind in TRACE:
        first = next(i for i in range(logic_start + 1, len(target_lines))
                     if target_lines[i].strip().startswith(start.strip()))
        last = next(i for i in range(first + 1, len(target_lines))
                    if target_lines[i].strip() == end.strip()
                    or target_lines[i].strip().startswith(end.strip()))
        source_number = next(i for i, line in enumerate(source_lines, 1) if quoted in line)
        item = by_line[("SKILL.md", source_number)]
        item["kind"] = kind
        for i in range(first, last):
            text = target_lines[i].strip()
            if text and not text.startswith(("label ", "otherwise:", "else:")):
                item["lands"].append(f"SKILL.md#L{i + 1}")

    orders = [
        ("Method freedom != authority expansion", "verify#authority before exec planned action"),
        ("Confirm evidence belongs to the intended version", "verify#basis before exec planned action"),
        ("Reconcile outcome before repeating", "verify#repetition before exec planned action"),
        ("For a meaningful probe, retain a compact prediction", "generate action plan before verify#basis"),
        ("Verify against the original completion condition", "verify#completion before return#solved"),
    ]
    for quoted, rule in orders:
        number = next(i for i, line in enumerate(source_lines, 1) if quoted in line)
        requirements.append({"id": f"O{len(requirements) + 1:03}", "kind": "order",
                             "text": source_lines[number - 1],
                             "source": [{"file": "SKILL.md", "lines": [number, number]}],
                             "evidence": "none", "lands": [rule],
                             "note": "Explicit ordering lowers the quoted source constraint; no runtime enforcement implied."})

    result = {"format": "skillwren-inventory-1",
              "sources": {name: hashlib.sha256(raw).hexdigest() for name, raw in sources.items()},
              "requirements": requirements, "non_requirements": non_requirements,
              "review_note": "Model-authored line inventory and landing map after user confirmed preservation scope. Supporting references retained byte-for-byte. Presence and traceability do not prove semantic equivalence."}
    REPORTS.mkdir(exist_ok=True)
    write_json(REPORTS / "requirements.json", result)
    rows = ["# Requirement inventory and landing map", "",
            "User confirmed the preservation scope in conversation. This is a model-authored",
            "mapping, not human approval of the converted bytes or proof of semantic parity.", "",
            "Each substantive source line is quoted separately. Formatting is explicitly",
            "accounted for in requirements.json. Supporting references are unchanged.", ""]
    for item in requirements:
        span = item["source"][0]
        rows += [f"## {item['id']} — {span['file']}:{span['lines'][0]}", "",
                 "> " + item["text"], "", "Lands: " + "; ".join(item["lands"]), ""]
    (REPORTS / "requirements.md").write_text("\n".join(rows), encoding="utf-8")
    return list(sources)[1:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skillwren-root", type=Path, default=ROOT.parent / "SkillWren")
    parser.add_argument("--out", type=Path, default=ROOT / "solve-this")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if "name: solve-this" in (ROOT / "SKILL.md").read_text(encoding="utf-8") and (ROOT / "references/mathematical-discovery.md").exists():
        parser.error("This is the archived PoC conversion builder. Use scripts/build_discovery.py for the current mathematical discovery skill; earlier artifacts remain unchanged.")
    launcher = args.skillwren_root.resolve() / "skills/skillwren/scripts/skillwren.py"
    if not launcher.is_file():
        parser.error("Point --skillwren-root at the updated SkillWren checkout.")
    if not args.check_only and args.out.exists():
        parser.error("Output already exists; choose a new --out. Existing builds are never replaced.")
    context = inventory()
    write_json(REPORTS / "toolchain.json", {
        "root": str(args.skillwren_root.resolve()),
        "launcher_sha256": hashlib.sha256(launcher.read_bytes()).hexdigest(),
        "library": {p.relative_to(args.skillwren_root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted((args.skillwren_root / "src/skillwren").rglob("*.py"))},
        "note": "Local toolchain bytes, including tested patches; package version alone does not identify them.",
    })

    def command(report, *arguments):
        proc = subprocess.run([sys.executable, "-B", str(launcher), *map(str, arguments)],
                              cwd=ROOT, capture_output=True, encoding="utf-8", errors="strict")
        (REPORTS / report).write_text(proc.stdout + proc.stderr, encoding="utf-8")
        if proc.returncode:
            raise RuntimeError(f"SkillWren exited {proc.returncode}; see {REPORTS / report}")
        return proc.stdout

    checked = command("check.txt", "check", "--fragment", "--summary", "--audit", DRAFT / "SKILL.md")
    warnings = re.findall(r"warning (\w+):", checked)
    if warnings != ["W15"]:
        raise RuntimeError(f"Expected only the documented planning W15; got {warnings}")
    source_args = ["--source", ROOT / "SKILL.md"]
    for name in context:
        source_args += ["--context", ROOT / name]
    command("inventory-check.json", "inventory", "check", REPORTS / "requirements.json",
            *source_args, "--candidate", DRAFT, "--json")
    findings = json.loads((REPORTS / "inventory-check.json").read_text(encoding="utf-8"))
    if findings["warnings"]:
        raise RuntimeError("Inventory has unexplained warnings; inspect inventory-check.json.")
    command("workflow.txt", "explain-workflow", "--fragment", DRAFT / "SKILL.md")
    command("coverage.txt", "coverage", DRAFT / "SKILL.md")
    command("coverage.json", "coverage", DRAFT / "SKILL.md", "--json")
    if not args.check_only:
        command("build.txt", "build", DRAFT, "--out", args.out.resolve())
        manifest = json.loads((args.out / "manifest.json").read_text(encoding="utf-8"))
        for name, entry in manifest["sources"].items():
            if hashlib.sha256((args.out / name).read_bytes()).hexdigest() != entry["sha256"]:
                raise RuntimeError(f"Built file differs from manifest: {name}")
        print(f"Built and verified {len(manifest['sources'])} files at {args.out.resolve()}")
    else:
        print("Checked draft, inventory, workflow and coverage; existing package untouched.")


if __name__ == "__main__":
    main()
