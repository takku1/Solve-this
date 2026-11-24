"""Bounded symbolic block-law proposals and exact, scoped falsification.

The grammar contains signed A/B blocks, not a prewritten construction formula.
It is a first synthesis milestone, not a universal Hadamard search algorithm.
"""
from itertools import product, permutations
from numbers import Integral
from .store import digest


def exact_hadamard(matrix):
    rows = [list(row) for row in matrix]
    n = len(rows)
    if not n or any(len(row) != n for row in rows):
        return False
    if any(isinstance(v, bool) or not isinstance(v, Integral) or int(v) not in (-1, 1)
           for row in rows for v in row):
        return False
    return all(sum(int(rows[i][c]) * int(rows[j][c]) for c in range(n)) == (n if i == j else 0)
               for i in range(n) for j in range(i, n))


def sylvester(order):
    if type(order) is not int or order < 1 or order & (order - 1):
        raise ValueError("This control construction requires a power-of-two order")
    h = [[1]]
    while len(h) < order:
        h = [row + row for row in h] + [row + [-x for x in row] for row in h]
    return h


def validate_cells(cells):
    if len(cells) != 4 or any(symbol not in ("A", "B") or type(sign) is not int or sign not in (-1, 1)
                              for symbol, sign in cells):
        raise ValueError("Expected four signed A/B blocks in row-major order")


def gram_terms(cells, r, s):
    validate_cells(cells)
    result = {}
    for c in range(2):
        left, right = cells[2*r+c], cells[2*s+c]
        key = (left[0] + right[0]).lower()
        result[key] = result.get(key, 0) + left[1] * right[1]
    return {key: value for key, value in result.items() if value}


def residuals(cells, amicable=False):
    residual = []
    for r, s in product(range(2), repeat=2):
        values = {}
        for key, coefficient in gram_terms(cells, r, s).items():
            key = "nI" if key in ("aa", "bb") else "cross" if amicable else key
            values[key] = values.get(key, 0) + coefficient
        if r == s:
            values["nI"] = values.get("nI", 0) - 2
        residual.append({key: coefficient for key, coefficient in values.items() if coefficient})
    return residual


def symmetry_key(cells):
    validate_cells(cells)
    variants = []
    for rp, cp in product(permutations(range(2)), repeat=2):
        for signs in product((-1, 1), repeat=4):
            for swap in (False, True):
                transformed = []
                for r, c in product(range(2), repeat=2):
                    symbol, sign = cells[2*rp[r]+cp[c]]
                    if swap:
                        symbol = "B" if symbol == "A" else "A"
                    transformed.append((symbol, sign * signs[r] * signs[2+c]))
                variants.append(tuple(transformed))
    return min(variants)


def instantiate(cells, a, b):
    validate_cells(cells)
    if len(a) != len(b) or not a or any(len(row) != len(a) for row in a+b):
        raise ValueError("Input blocks must have the same positive square order")
    blocks = {"A": a, "B": b}
    result = []
    for r in range(2):
        for i in range(len(a)):
            row = []
            for c in range(2):
                symbol, sign = cells[2*r+c]
                row += [sign * int(x) for x in blocks[symbol][i]]
            result.append(row)
    return result


def experiment(cells, amicable):
    trials = []
    for n in (1, 2, 4, 8):
        a = sylvester(n)
        # Column signs give AB^T = BA^T without forcing B = A.
        b = [[value * (-1 if c % 2 else 1) for c, value in enumerate(row)] for row in a]
        trials.append({"input_order": n, "output_order": 2*n,
                       "valid": exact_hadamard(instantiate(cells, a, b))})
    falsifier = None
    if amicable:
        a = sylvester(4)
        b = a[1:] + a[:1]
        if not exact_hadamard(instantiate(cells, a, b)):
            falsifier = {"scope": "removed amicability hypothesis only; not the Hadamard conjecture",
                         "A": a, "B": b, "output_hadamard": False}
    return {"trials": trials, "all_valid": all(t["valid"] for t in trials),
            "assumption_removal_counterexample": falsifier,
            "limits": "Four exact cases support this parameterized candidate only; they prove no universal family or parameter existence."}


def formal_gram_type(cells, amicable):
    equations = []
    for r, s in product(range(2), repeat=2):
        terms = gram_terms(cells, r, s)
        lhs = " + ".join(f"({value} * {key})" for key, value in sorted(terms.items())) or "0"
        equations.append(f"({lhs} = {'2*n' if r == s else '0'})")
    return ("∀ (n aa bb ab ba : Int), aa = n → bb = n → " +
            ("ab = ba → " if amicable else "") + " ∧ ".join(equations))


def gram_proof_body(amicable):
    return ("by\n  intro n aa bb ab ba haa hbb" + (" hab\n" if amicable else "\n") +
            "  exact ⟨by omega, by omega, by omega, by omega⟩")


def synthesize(budget=256):
    if type(budget) is not int or not 1 <= budget <= 4096:
        raise ValueError("Candidate budget must be between 1 and 4096")
    atoms = tuple(product(("A", "B"), (-1, 1)))
    known = symmetry_key((("A", 1), ("A", 1), ("A", 1), ("A", -1)))
    seen, candidates, rejected, tested = set(), [], [], 0
    for cells in product(atoms, repeat=4):
        if tested >= budget:
            break
        tested += 1
        independent = residuals(cells)
        amicable = any(independent)
        if amicable and any(residuals(cells, amicable=True)):
            rejected.append({"cells": cells, "residuals": residuals(cells, amicable=True),
                             "meaning": "not certified by this reduction; not unrestricted nonexistence"})
            continue
        key = symmetry_key(cells)
        if key in seen:
            continue
        seen.add(key)
        test = experiment(cells, amicable)
        candidates.append({"id": digest({"cells": key, "amicable": amicable})[:16],
                           "cells": cells, "assumptions": ["A,B square Hadamard of same order n"] +
                               (["AB^T = BA^T (amicability)"] if amicable else []),
                           "amicable": amicable, "unreduced_residuals": independent,
                           "reduced_residuals": residuals(cells, amicable),
                           "experiment": test,
                           "novelty": "KNOWN_RESULT: Sylvester up to signed block symmetries" if key == known
                               else "UNREVIEWED: grammar fingerprint is not a literature novelty result",
                           "formal_type": formal_gram_type(cells, amicable),
                           "proof_body": gram_proof_body(amicable),
                           "remaining": ["matrix-index/sign/dimension lifting", "parameter existence over the desired domain",
                                         "literature and equivalence review", "symbolic coverage comparison"]})
    return {"grammar": "signed 2x2 same-order A/B blocks", "total_grammar_size": 256,
            "tested": tested, "not_certified_by_reduction": len(rejected),
            "unsuccessful_candidates": rejected,
            "exhaustive_for_this_grammar": tested == 256,
            "state": "BRANCH_EXHAUSTED" if tested == 256 else "BUDGET_EXHAUSTED",
            "candidates": candidates, "global_resolution": "UNRESOLVED"}
