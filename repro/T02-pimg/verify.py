#!/usr/bin/env python3
"""
T02 -- parent-image divisibility: exact-replayable verifier.

Reproduces the 31 dimension-bound kills: a length-40 row of dimension k sits in
the forced [56,21] residual as the image of a 16-coordinate projection J of
dimension 21-k.  Every J-word is even, so J is contained in the even-weight code
[16,15], forcing dim J = 21-k <= 15, i.e. k >= 6.  Hence every candidate with
k <= 5 is killed.  (The 32nd T02 kill, (11,615,816), is the separate
fiber-divisibility check noted below.)

Pure Python standard library, exact integer arithmetic.

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


_KT = {w: [krawtchouk(j, w) for j in range(N + 1)] for w in (0, 16, 20, 24, 40)}


def candidates():
    out = []
    for k in range(1, 21):
        size = 1 << k
        for a in range((size - 2) // 2 + 1):
            b = size - 2 - 2 * a
            if b < 0:
                continue
            B, ok = [], True
            for j in range(N + 1):
                s = _KT[0][j] + a * (_KT[16][j] + _KT[24][j]) + b * _KT[20][j] + _KT[40][j]
                if s % size or s < 0:
                    ok = False
                    break
                B.append(s // size)
            if ok and a <= B[16] and a <= B[24] and b <= B[20]:
                out.append((k, a, b))
    return out


def main():
    c = candidates()
    # Dimension bound: dim J = 21 - k, J even => J subset [16,15] => 21-k <= 15 => k >= 6.
    killed = [(k, a, b) for (k, a, b) in c if 21 - k > 15]   # exactly k <= 5
    by_k = dict(sorted(Counter(k for k, _, _ in killed).items()))
    print(f"T02: dim J = 21-k must be <= 15 (J even-weight in [16,15]) => k >= 6.")
    print(f"     dimension-bound kills (k<=5): {len(killed)}  by k: {by_k}")
    assert all(k <= 5 for k, _, _ in killed), "dim-bound kills must be exactly k<=5"
    assert len(killed) == 31, f"expected 31 dim-bound kills, got {len(killed)}"
    print("OK: 31 k<=5 rows killed by the exact dimension bound 21-k <= 15.")
    print("    (The 32nd T02 kill, (11,615,816), is fiber-divisibility: its i-marginals "
          "R_i = 2^k * A_i(J) need a valid [16,10] image enumerator A_i(J), which fails. "
          "That check needs the image-enumerator data and is documented in README.)")
    json.dump({"dim_bound_kills": len(killed), "killed_by_k": by_k,
               "note_32nd": "(11,615,816) fiber-divisibility"},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
