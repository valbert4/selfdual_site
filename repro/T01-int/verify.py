#!/usr/bin/env python3
"""
T01 -- integer/self-orthogonal validity: exact-replayable verifier.

Re-enumerates the length-40 menu from scratch and confirms it is exactly the 132
candidates with distribution {1,2,4,8,16,32,25,19,16,8,1} for k=1..11. Pure
Python standard library, exact integer arithmetic.

A candidate is a (k,a,b) whose enumerator W_E = 1 + a(y^16+y^24) + b y^20 + y^40
has |E| = 2 + 2a + b = 2^k, an integral nonnegative length-40 MacWilliams dual,
and is self-orthogonal (A_w <= B_w for all w).

Run:  python3 verify.py
"""
from collections import Counter
from math import comb
import json
import os

N = 40
HERE = os.path.dirname(os.path.abspath(__file__))


def krawtchouk(j, w, n=N):
    return sum((-1) ** i * comb(w, i) * comb(n - w, j - i) for i in range(j + 1))


# Only weights {0,16,20,24,40} are nonzero in W_E, so each MacWilliams dual
# coefficient is a 5-term combination -- precompute those Krawtchouk columns.
_KT = {w: [krawtchouk(j, w) for j in range(N + 1)] for w in (0, 16, 20, 24, 40)}


def candidates():
    out = []
    for k in range(1, 21):  # E subset E^perp forces k <= 20
        size = 1 << k
        for a in range((size - 2) // 2 + 1):
            b = size - 2 - 2 * a
            if b < 0:
                continue
            B, ok = [], True
            for j in range(N + 1):
                s = _KT[0][j] + a * (_KT[16][j] + _KT[24][j]) + b * _KT[20][j] + _KT[40][j]
                if s % size or s < 0:  # MacWilliams dual integral + nonnegative
                    ok = False
                    break
                B.append(s // size)
            if ok and a <= B[16] and a <= B[24] and b <= B[20]:  # self-orthogonal A_w<=B_w
                out.append((k, a, b))
    return out


def main():
    c = candidates()
    dist = dict(sorted(Counter(k for k, _, _ in c).items()))
    expected = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 25, 8: 19, 9: 16, 10: 8, 11: 1}
    print(f"T01: re-enumerated {len(c)} length-40 menu candidates; distribution {dist}")
    assert len(c) == 132, f"expected 132 candidates, got {len(c)}"
    assert dist == expected, f"distribution mismatch: {dist}"
    print("OK: exactly 132 candidates, distribution {1,2,4,8,16,32,25,19,16,8,1}, k=1..11. "
          "Nothing valid for k>=12.")
    json.dump({"candidates": len(c), "distribution": dist},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
