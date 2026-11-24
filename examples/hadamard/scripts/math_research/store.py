"""Atomic single-writer knowledge journal. No model-supplied solved flag exists.

Hash chains detect accidental modification; they are not a security boundary
against an owner who can replace both the journal and its hashes.
"""
from contextlib import contextmanager
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import uuid

from .objective import HADAMARD, OBSERVATION_STATES, BRANCHES


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class ResearchError(ValueError):
    pass


def _acyclic(claims, edges):
    adjacency = {key: [] for key in claims}
    for edge in edges:
        if edge["kind"] == "requires":
            adjacency[edge["claim"]].append(edge["dependency"])
    active, done = set(), set()

    def visit(key):
        if key in active:
            raise ResearchError("Circular proof dependency")
        if key in done:
            return
        active.add(key)
        for dependency in adjacency[key]:
            visit(dependency)
        active.remove(key)
        done.add(key)

    for key in adjacency:
        visit(key)


def _apply(state, kind, payload, event_number=0):
    if kind == "init":
        if state or payload != HADAMARD:
            raise ResearchError("Objective differs from the immutable Hadamard statement")
        state.update(objective=deepcopy(payload), objective_hash=digest(payload),
                     resolution="UNRESOLVED", session="RUNNING", sources={}, claims={},
                     edges=[], observations=[], proofs=[], attempts=[], program=None,
                     branches={key: {"description": value, "attempts": 0, "last_event": 0}
                               for key, value in BRANCHES.items()})
        state["claims"][HADAMARD["id"]] = {
            "id": HADAMARD["id"], "kind": "objective", "statement": HADAMARD["statement"],
            "scope": HADAMARD["domain"], "formal_type": HADAMARD["formal_type"],
            "status": "UNRESOLVED", "sources": [], "novelty": "not_claimed"}
    elif kind == "source":
        if payload["id"] in state["sources"]:
            raise ResearchError("Source versions are immutable; assign a new source id")
        state["sources"][payload["id"]] = deepcopy(payload)
    elif kind == "claim":
        if payload["id"] in state["claims"]:
            raise ResearchError("Claim id already exists; never replace a statement")
        if payload["kind"] == "objective":
            raise ResearchError("A subproblem cannot replace the objective")
        if any(key not in state["sources"] for key in payload["sources"]):
            raise ResearchError("Unknown source id")
        if payload["status"] != "UNRESOLVED":
            raise ResearchError("Claims start unresolved; evidence determines their state")
        state["claims"][payload["id"]] = deepcopy(payload)
    elif kind == "edge":
        if payload["kind"] not in {"requires", "may_support", "generalizes", "falsifies"}:
            raise ResearchError("Unknown edge type")
        if any(payload[k] not in state["claims"] for k in ("claim", "dependency")):
            raise ResearchError("Dependency names an unknown claim")
        if payload in state["edges"]:
            raise ResearchError("Duplicate edge")
        state["edges"].append(deepcopy(payload))
        _acyclic(state["claims"], state["edges"])
    elif kind == "observation":
        claim = state["claims"].get(payload["claim"])
        if not claim or claim["kind"] == "objective":
            raise ResearchError("Experiments never update the global mathematical verdict")
        if payload["state"] not in OBSERVATION_STATES:
            raise ResearchError("That state requires an exact formal proof gate")
        if payload["state"] == "KNOWN_RESULT" and not claim["sources"]:
            raise ResearchError("Known results require literature provenance")
        if claim["status"] in {"LEMMA_PROVEN", "COVERAGE_EXPANDED"}:
            raise ResearchError("Do not overwrite a proof with an observation; record a separate claim")
        claim["status"] = payload["state"]
        state["observations"].append(deepcopy(payload))
        if payload.get("branch"):
            branch = state["branches"][payload["branch"]]
            branch["attempts"] += 1
            branch["last_event"] = payload["event_number"]
    elif kind == "attempt":
        state["attempts"].append(deepcopy(payload))
        if "receipt" in payload:
            state["branches"]["formal-mathematics"]["attempts"] += 1
            state["branches"]["formal-mathematics"]["last_event"] = event_number
    elif kind == "edge-retracted":
        if not payload.get("reason") or payload["edge"] not in state["edges"]:
            raise ResearchError("A relation correction needs the existing edge and a reason")
        state["edges"].remove(payload["edge"])
    elif kind == "proof":
        claim = state["claims"][payload["claim"]]
        if claim["kind"] == "objective" or not payload["receipt"]["verified"]:
            raise ResearchError("Invalid lemma proof event")
        if payload["receipt"]["formal_type"] != claim["formal_type"]:
            raise ResearchError("Proof type differs from the recorded claim")
        claim["status"] = "LEMMA_PROVEN"
        state["proofs"].append(deepcopy(payload))
    elif kind == "resolution":
        wanted = {"prove": "HadamardConjecture", "refute": "Not HadamardConjecture"}
        if (payload["direction"] not in wanted or not payload["receipt"]["verified"]
                or payload["receipt"]["formal_type"] != wanted[payload["direction"]]):
            raise ResearchError("A resolution needs a proof of the exact global statement")
        state["resolution"] = ("CONJECTURE_PROVEN" if payload["direction"] == "prove"
                               else "CONJECTURE_REFUTED")
        state["claims"][HADAMARD["id"]]["status"] = state["resolution"]
        state["proofs"].append({"claim": HADAMARD["id"], **deepcopy(payload)})
    elif kind == "checkpoint":
        if payload["state"] not in {"BUDGET_EXHAUSTED", "RUNNING"}:
            raise ResearchError("Invalid session checkpoint")
        state["session"] = payload["state"]
    elif kind == "program":
        state["program"] = deepcopy(payload)
    else:
        raise ResearchError("Unknown journal event; objective changes are not supported")


class Project:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.path = self.root / "journal.json"

    @classmethod
    def create(cls, root):
        project = cls(root)
        project.root.mkdir(parents=True, exist_ok=True)
        if not project.path.exists():
            project._append("init", HADAMARD)
        project.snapshot()
        return project

    def _load(self):
        if not self.path.exists():
            return [], {}
        events = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(events, list) or not events:
            raise ResearchError("Journal is empty or malformed")
        state, previous = {}, "0" * 64
        for index, event in enumerate(events):
            body = {key: event[key] for key in ("number", "previous", "kind", "payload")}
            if body["number"] != index or body["previous"] != previous or digest(body) != event["hash"]:
                raise ResearchError("Journal integrity or sequence failure")
            _apply(state, body["kind"], body["payload"], index)
            previous = event["hash"]
        if state["objective_hash"] != digest(HADAMARD):
            raise ResearchError("Objective drift")
        return events, state

    def snapshot(self):
        _, state = self._load()
        if not state:
            raise ResearchError("Initialize a project first")
        for proof in state["proofs"]:
            receipt = proof["receipt"]
            for key in ("source", "output"):
                path = self.root / receipt[key]
                if not path.is_relative_to(self.root) or not path.is_file():
                    raise ResearchError("Missing proof evidence")
                if hashlib.sha256(path.read_bytes()).hexdigest() != receipt[key + "_sha256"]:
                    raise ResearchError("Proof evidence changed; reverify before reuse")
        if state["program"]:
            for name in ("audit", "program"):
                artifact = self.root / state["program"][name]
                if not artifact.is_relative_to(self.root) or not artifact.is_file():
                    raise ResearchError("Missing adopted research program")
                if hashlib.sha256(artifact.read_bytes()).hexdigest() != state["program"][name + "_sha256"]:
                    raise ResearchError("Adopted research program changed")
        if state["resolution"] != "UNRESOLVED":
            from .formal import replay_resolution
            receipt = state["proofs"][-1]["receipt"]
            formal_type = ("HadamardConjecture" if state["resolution"] == "CONJECTURE_PROVEN"
                           else "Not HadamardConjecture")
            if not replay_resolution(self.root, receipt, formal_type):
                raise ResearchError("Stored resolution failed independent proof replay; conjecture is unresolved")
        return deepcopy(state)

    @contextmanager
    def _lock(self):
        path = self.root / "writer.lock"
        token = f"{os.getpid()}:{uuid.uuid4().hex}"
        try:
            with path.open("x", encoding="utf-8") as stream:
                stream.write(token)
        except FileExistsError as error:
            raise ResearchError("Another writer or a stale crash lock exists; inspect it before recovery") from error
        try:
            yield
        finally:
            if path.read_text(encoding="utf-8") == token:
                path.unlink()

    def _append(self, kind, payload):
        with self._lock():
            events, state = self._load()
            _apply(state, kind, payload, len(events))
            body = {"number": len(events), "previous": events[-1]["hash"] if events else "0" * 64,
                    "kind": kind, "payload": deepcopy(payload)}
            events.append({**body, "hash": digest(body)})
            temporary = self.root / ("pending-" + uuid.uuid4().hex + ".json")
            try:
                with temporary.open("x", encoding="utf-8", newline="\n") as stream:
                    stream.write(json.dumps(events, indent=2) + "\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, self.path)
            finally:
                if temporary.exists():
                    temporary.unlink()

    def source(self, ident, title, url, version, accessed, status="literature"):
        if not all(isinstance(x, str) and x for x in (ident, title, url, version, accessed)):
            raise ResearchError("A source needs identity, provenance, version and access date")
        item = dict(id=ident, title=title, url=url, version=version, accessed=accessed, status=status)
        existing = self.snapshot()["sources"].get(ident)
        if existing == item:
            return ident
        self._append("source", item)
        return ident

    def claim(self, ident, statement, scope, kind="candidate", sources=(), formal_type=None):
        if kind not in {"candidate", "lemma", "coverage", "known", "obligation"}:
            raise ResearchError("Invalid claim kind")
        if not all(isinstance(x, str) and x.strip() for x in (ident, statement, scope)):
            raise ResearchError("A claim requires a statement and explicit scope")
        state = self.snapshot()
        for claim in state["claims"].values():
            if (claim["statement"], claim["scope"], claim["formal_type"]) == (statement, scope, formal_type):
                return claim["id"]
        self._append("claim", dict(id=ident, statement=statement, scope=scope, kind=kind,
                                   sources=list(sources), formal_type=formal_type,
                                   status="UNRESOLVED", novelty="UNREVIEWED"))
        return ident

    def link(self, claim, dependency, kind="requires"):
        item = dict(claim=claim, dependency=dependency, kind=kind)
        if item not in self.snapshot()["edges"]:
            self._append("edge", item)

    def observe(self, claim, state, evidence, branch=None):
        snapshot = self.snapshot()
        if branch is not None and branch not in snapshot["branches"]:
            raise ResearchError("Unknown research branch")
        if not evidence:
            raise ResearchError("An observation needs evidence, including failed conditions")
        events, _ = self._load()
        self._append("observation", dict(claim=claim, state=state, evidence=evidence,
                                         branch=branch, event_number=len(events)))

    def retract_link(self, claim, dependency, kind, reason):
        self._append("edge-retracted", {"edge": {"claim": claim, "dependency": dependency, "kind": kind},
                                        "reason": reason})

    def checkpoint(self, remaining, reason="budget or invocation ended"):
        self._append("checkpoint", dict(state="BUDGET_EXHAUSTED", remaining=remaining, reason=reason))

    def adopt_program(self, audit, program):
        payload = {}
        folder = self.root / "evidence"
        folder.mkdir(exist_ok=True)
        for name, data in (("audit", audit), ("program", program)):
            raw = data.encode("utf-8") if isinstance(data, str) else data
            if not raw:
                raise ResearchError("An adopted audit/program cannot be empty")
            checksum = hashlib.sha256(raw).hexdigest()
            path = folder / (name + "-" + checksum + ".md")
            path.write_bytes(raw)
            payload[name] = path.relative_to(self.root).as_posix()
            payload[name + "_sha256"] = checksum
        if self.snapshot()["program"] != payload:
            self._append("program", payload)

    def resume(self):
        self._append("checkpoint", dict(state="RUNNING"))

    def blocked_dependencies(self, claim):
        state = self.snapshot()
        pending, visited, stack = [], set(), [claim]
        while stack:
            current = stack.pop()
            for edge in state["edges"]:
                if edge["claim"] == current and edge["kind"] == "requires":
                    dep = edge["dependency"]
                    if dep not in visited:
                        visited.add(dep)
                        if state["claims"][dep]["status"] not in {"LEMMA_PROVEN", "KNOWN_RESULT", "COVERAGE_EXPANDED"}:
                            pending.append(dep)
                        stack.append(dep)
        return sorted(pending)

    def certify(self, claim, body, lean=None, timeout=30):
        from .formal import check_proof
        state = self.snapshot()
        node = state["claims"][claim]
        if node["kind"] == "objective" or not node["formal_type"]:
            raise ResearchError("Use the exact global resolution gate for the objective")
        if self.blocked_dependencies(claim):
            raise ResearchError("Unresolved proof prerequisites")
        receipt = check_proof(self.root, node["formal_type"], body, lean, timeout)
        self._append("attempt", dict(claim=claim, receipt=receipt))
        if receipt["verified"]:
            self._append("proof", dict(claim=claim, receipt=receipt))
        return receipt

    def resolve(self, direction, body, lean=None, timeout=30):
        from .formal import check_proof
        if direction not in {"prove", "refute"}:
            raise ResearchError("Resolution direction must be prove or refute")
        if self.blocked_dependencies(HADAMARD["id"]):
            raise ResearchError("Unresolved global proof prerequisites")
        formal_type = "HadamardConjecture" if direction == "prove" else "Not HadamardConjecture"
        receipt = check_proof(self.root, formal_type, body, lean, timeout)
        self._append("attempt", dict(claim=HADAMARD["id"], receipt=receipt))
        if receipt["verified"]:
            self._append("resolution", dict(direction=direction, receipt=receipt))
        return receipt
