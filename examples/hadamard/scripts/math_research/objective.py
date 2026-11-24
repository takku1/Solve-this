"""The Hadamard objective is a fixed statement, not a configurable benchmark."""
HADAMARD = {
    "id": "hadamard-conjecture",
    "domain": "k in positive integers; real sign matrices of order 4*k",
    "statement": "forall k in Z_{>0}, exists H in {-1,1}^{4k x 4k}, H*transpose(H) = 4k*I",
    "formal_type": "HadamardConjecture",
    "resolution": ["CONJECTURE_PROVEN", "CONJECTURE_REFUTED"],
    "non_resolutions": ["finite verification", "known constructions", "restricted UNSAT",
                        "candidate counterexample", "branch exhaustion", "budget exhaustion"],
}

RESULT_STATES = frozenset({
    "KNOWN_RESULT", "COUNTEREXAMPLE_FOUND", "EMPIRICALLY_SUPPORTED", "LEMMA_PROVEN",
    "COVERAGE_EXPANDED", "BRANCH_EXHAUSTED", "BUDGET_EXHAUSTED",
    "CONJECTURE_PROVEN", "CONJECTURE_REFUTED",
})
OBSERVATION_STATES = RESULT_STATES - {
    "LEMMA_PROVEN", "COVERAGE_EXPANDED", "CONJECTURE_PROVEN", "CONJECTURE_REFUTED",
}
BRANCHES = {
    "constructive-algebra": "Parameterized block constructions and exact Gram conditions",
    "combinatorial-design": "Scoped difference-set, sequence and design implications",
    "computational-search": "Exact witnesses and counterexamples within declared encodings",
    "recursive-composition": "Parameterized order transforms and composition laws",
    "number-theory": "Symbolic coverage gaps and parameter-existence lemmas",
    "obstruction-theory": "Necessary conditions with explicitly restricted domains",
    "formal-mathematics": "Cancellation, lifting, equivalence and global proof obligations",
}
