"""Symbolic sufficient families, not an oracle for the mathematical frontier."""
from functools import lru_cache
from math import isqrt

FAMILIES = (
    {"id": "sylvester", "formula": "n = 2^a", "conditions": "integer a >= 0"},
    {"id": "paley-I", "formula": "n = q+1", "conditions": "q prime power, q % 4 == 3"},
    {"id": "paley-II", "formula": "n = 2*(q+1)", "conditions": "q odd prime power, q % 4 == 1"},
    {"id": "kronecker", "formula": "n = a*b", "conditions": "a,b already covered; a,b > 1"},
)
GAP_EXPRESSION = "{4*k : integer k>0} \\ least_closure(Sylvester ∪ PaleyI ∪ PaleyII, Kronecker)"


def prime_power(q):
    if type(q) is not int or q < 2:
        return False
    for p in range(2, isqrt(q) + 1):
        if q % p == 0:
            while q % p == 0:
                q //= p
            return q == 1
    return True


@lru_cache(maxsize=10000)
def derivation(n):
    if type(n) is not int or n <= 0:
        raise ValueError("Order must be a positive integer")
    if n & (n - 1) == 0:
        return {"rule": "sylvester", "order": n, "exponent": n.bit_length() - 1}
    if n > 2 and n % 4:
        return None
    if (n - 1) % 4 == 3 and prime_power(n - 1):
        return {"rule": "paley-I", "order": n, "q": n - 1}
    q = n // 2 - 1
    if n % 2 == 0 and q % 4 == 1 and prime_power(q):
        return {"rule": "paley-II", "order": n, "q": q}
    for a in range(2, isqrt(n) + 1):
        if n % a == 0:
            left, right = derivation(a), derivation(n // a)
            if left and right:
                return {"rule": "kronecker", "order": n, "factors": [left, right]}
    return None


def coverage_report(limit):
    if type(limit) is not int or not 4 <= limit <= 10000:
        raise ValueError("Diagnostic window must be between 4 and 10000")
    gaps = [n for n in range(4, limit + 1, 4) if derivation(n) is None]
    return {"families": FAMILIES, "symbolic_gap": GAP_EXPRESSION,
            "window": {"maximum": limit, "uncovered_by_this_model": gaps},
            "global_conjecture": "UNRESOLVED",
            "limits": "A finite diagnostic window and an incomplete family model do not identify all globally open orders."}
