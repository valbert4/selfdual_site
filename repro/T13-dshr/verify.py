#!/usr/bin/env python3
"""
T13 -- double-shortening forced-intersection screen: exact-replayable verifier.

Reproduces the kill of (k=9, a=247, b=16). Double-shortening on the union of two
weight-16 supports forces (for this row) the pairwise intersection to the single
value t=8; the weight-16 supports are then a one-distance constant-weight code in
J(40,16), whose exact Delsarte/Johnson bound is 7657/67 ~ 114.3 < 247.

This verifier reproduces the bound 7657/67 exactly (Eberlein eigenvalues + exact
rational matrix inverse + a one-variable Delsarte LP), with no solver. The
combinatorial forcing of t=8 (ruling out t=4,6 via the four-block split) is in
the upstream verify_t13_doubleshorten.py; this bundle certifies the binding bound.

Run:  python3 verify.py
"""
from fractions import Fraction as F
from math import comb
import json
import os

N, W = 40, 16
D = min(W, N - W)
HERE = os.path.dirname(os.path.abspath(__file__))


def eberlein(k, j):
    return sum((-1) ** i * comb(j, i) * comb(W - j, k - i) * comb(N - W - j, k - i)
               for i in range(k + 1))


def rational_inverse(M):
    n = len(M)
    A = [[F(M[i][j]) for j in range(n)] + [F(int(i == j)) for j in range(n)] for i in range(n)]
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
    assert all(P[0][k] == comb(W, k) * comb(N - W, k) for k in range(D + 1))
    vtot = comb(N, W)
    Pinv = rational_inverse(P)
    return [[vtot * Pinv[i][k] for k in range(D + 1)] for i in range(D + 1)]


def one_distance_bound(Q, intersection):
    """max 1 + x  s.t.  Q[0][k] + x*Q[i][k] >= 0 for all k, x >= 0, i = W - t."""
    i = W - intersection
    xmax = None
    for k in range(D + 1):
        if Q[i][k] < 0:
            cap = -Q[0][k] / Q[i][k]
            if xmax is None or cap < xmax:
                xmax = cap
    assert xmax is not None, "unbounded -- unexpected"
    return 1 + xmax


def main():
    Q = second_eigenmatrix()
    bound = one_distance_bound(Q, 8)
    k, a, b = 9, 247, 16
    killed = F(a) > bound
    print(f"T13: intersections forced to {{8}}; Johnson/Delsarte bound = {bound} (~{float(bound):.3f})")
    print(f"     row (k={k}, a={a}, b={b}): a={a} {'>' if killed else '<='} {bound}  "
          f"->  {'KILL' if killed else 'survives'}")
    assert bound == F(7657, 67), f"expected 7657/67, got {bound}"
    assert killed, "row (9,247,16) must be killed"
    print("OK: exact bound 7657/67 reproduced; (9,247,16) proof-grade kill confirmed.")
    json.dump({"scheme": "J(40,16)", "intersections": [8], "bound": str(bound),
               "kill_row": [k, a, b], "killed": killed},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
