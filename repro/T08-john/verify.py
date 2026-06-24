#!/usr/bin/env python3
"""
T08 -- Johnson/Delsarte two-point bound: exact-replayable verifier.

Reproduces, with EXACT rational arithmetic and NO LP solver, the Delsarte
linear-programming upper bound on a = A_16(E) for a length-40 menu code E whose
pairwise weight-16 support intersections are restricted by the code weights.
Kills the menu row (k=9, a=255, b=0): with b=0 the only available intersections
are {4,8}, whose exact Delsarte bound is 247 < 255.

Method
------
Build the second eigenmatrix Q of the Johnson scheme J(40,16) exactly (Eberlein
eigenvalues + an exact rational matrix inverse), then solve the small 2-variable
Delsarte LP by exact vertex enumeration -- every optimum of a 2-D LP is attained
at a vertex (intersection of two constraint lines).  No external solver; only the
Python standard library.

Run:  python3 verify.py
"""
from fractions import Fraction as F
from math import comb
import json
import os

N, W = 40, 16
D = min(W, N - W)  # 16 Johnson classes
HERE = os.path.dirname(os.path.abspath(__file__))


def eberlein(k, j):
    """Eigenvalue of the Johnson-distance-k adjacency matrix on eigenspace V_j."""
    return sum((-1) ** i * comb(j, i) * comb(W - j, k - i) * comb(N - W - j, k - i)
               for i in range(k + 1))


def rational_inverse(M):
    n = len(M)
    A = [[F(M[i][j]) for j in range(n)] + [F(int(i == j)) for j in range(n)]
         for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [A[r][j] - f * A[c][j] for j in range(2 * n)]
    return [[A[i][n + j] for j in range(n)] for i in range(n)]


def second_eigenmatrix():
    P = [[F(eberlein(k, j)) for k in range(D + 1)] for j in range(D + 1)]
    assert all(P[j][0] == 1 for j in range(D + 1)), "column 0 = identity"
    assert all(P[0][k] == comb(W, k) * comb(N - W, k) for k in range(D + 1)), "valencies"
    vtot = comb(N, W)
    Pinv = rational_inverse(P)
    Q = [[vtot * Pinv[i][k] for k in range(D + 1)] for i in range(D + 1)]
    for k in range(D + 1):
        mk = comb(N, k) - (comb(N, k - 1) if k >= 1 else 0)
        assert Q[0][k] == F(mk), ("multiplicity mismatch", k)
    return Q


def delsarte_bound(Q, intersections):
    """Exact Delsarte LP optimum: max size of a constant-weight code in J(40,16)
    whose pairwise support intersections lie in `intersections`.  Two-distance
    case, solved by exact vertex enumeration."""
    dists = [W - t for t in intersections]
    assert len(dists) == 2, "this verifier handles the 2-distance case"
    i1, i2 = dists
    cons = [(Q[0][k], Q[i1][k], Q[i2][k]) for k in range(D + 1)]
    cons.append((F(0), F(1), F(0)))  # a_{i1} >= 0
    cons.append((F(0), F(0), F(1)))  # a_{i2} >= 0
    best = None
    n = len(cons)
    for p in range(n):
        for q in range(p + 1, n):
            c1, a1, b1 = cons[p]
            c2, a2, b2 = cons[q]
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            x = (-c1 * b2 + c2 * b1) / det
            y = (-a1 * c2 + a2 * c1) / det
            if all(c + a * x + b * y >= 0 for (c, a, b) in cons):
                obj = 1 + x + y
                if best is None or obj > best:
                    best = obj
    assert best is not None, "LP infeasible/unbounded -- unexpected"
    return best


def allowed_intersections(a, b):
    """Intersections t available to a code with enumerator 1 + a(y^16+y^24) + b y^20 + y^40."""
    inter = []
    if a > 0:
        inter.append(8)   # wt(u+v) = 16
    if b > 0:
        inter.append(6)   # wt(u+v) = 20
    if a > 0:
        inter.append(4)   # wt(u+v) = 24
    return sorted(inter)


def main():
    Q = second_eigenmatrix()
    b48 = delsarte_bound(Q, [4, 8])
    k, a, b = 9, 255, 0  # the menu row killed by T08 (input: the T01 menu)
    inter = allowed_intersections(a, b)
    assert inter == [4, 8], inter
    killed = F(a) > b48

    print(f"Johnson scheme J(40,16): Delsarte bound for intersections {{4,8}} = {b48}")
    print(f"menu row (k={k}, a={a}, b={b}): b=0 forces intersections {inter}; "
          f"a={a} {'>' if killed else '<='} {b48}  ->  {'KILL' if killed else 'survives'}")

    assert b48 == 247, f"expected exact bound 247, got {b48}"
    assert killed, "row (9,255,0) must be killed"

    json.dump(
        {"scheme": "J(40,16)", "intersections": [4, 8], "delsarte_bound": str(b48),
         "kill_row": [k, a, b], "a": a, "killed": killed, "reason": f"{a} > {b48}"},
        open(os.path.join(HERE, "result.json"), "w"), indent=2,
    )
    print("OK: exact Delsarte bound 247 reproduced; (9,255,0) proof-grade kill confirmed.")


if __name__ == "__main__":
    main()
