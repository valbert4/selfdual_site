#!/usr/bin/env python3
"""
T05 -- three-block nonnegativity: exact-replayable verifier.

Reproduces the 7 high-a k=10 kills. At two disjoint weight-16 anchors the
16|16|40 split counts are affine in two free parameters (m, n); a row is
realizable only if all orbit counts can be >= 0 simultaneously. For each of the
7 killed rows that real system is INFEASIBLE, certified by a Farkas vector.

Input (certificate): `system.json` -- for each killed (k,a,b), the orbit affine
forms (alpha + beta*m + gamma*n) and a Farkas certificate y_o >= 0 with
  sum y_o*beta_o = 0,  sum y_o*gamma_o = 0,  sum y_o*alpha_o = -1.
Then  sum_o y_o * (alpha_o + beta_o*m + gamma_o*n) = -1 < 0  for every (m,n),
yet each term is >= 0 under nonnegativity -- a contradiction, so no (m,n) makes
all orbit counts nonnegative. The certificate was generated once by the Sage
three-block setup (`the project's solver`); this verifier only CHECKS it.

Run:  python3 verify.py        (pure Python standard library)
"""
from fractions import Fraction as F
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def check_farkas(forms, y):
    """forms[o] = [alpha,beta,gamma] (strings); y = {orbit: value}. Returns the
    value sum y_o*alpha_o, after asserting y>=0 and sum y_o*(beta,gamma)=(0,0)."""
    sa = sb = sc = F(0)
    for o_str, yv in y.items():
        o = int(o_str)
        yy = F(yv)
        assert yy >= 0, f"y[{o}] = {yy} < 0"
        al, be, ga = (F(forms[o][0]), F(forms[o][1]), F(forms[o][2]))
        sa += yy * al
        sb += yy * be
        sc += yy * ga
    assert sb == 0 and sc == 0, f"Farkas combination of (beta,gamma) is {(sb, sc)}, not 0"
    return sa


def main():
    data = json.load(open(os.path.join(HERE, "system.json")))
    rows = data["rows"]
    killed = []
    for key, row in sorted(rows.items()):
        sa = check_farkas(row["forms"], row["farkas_y"])
        assert sa < 0, f"row {key}: sum y*alpha = {sa} is not < 0 (no contradiction)"
        killed.append((row["k"], row["a"], row["b"]))
        print(f"  ({key}): Farkas valid, sum y*alpha = {sa} < 0  ->  nonnegativity "
              f"INFEASIBLE  ->  KILL")
    expected = [(10, 311, 400), (10, 327, 368), (10, 343, 336), (10, 359, 304),
                (10, 375, 272), (10, 391, 240), (10, 407, 208)]
    assert sorted(killed) == expected, f"killed set mismatch: {sorted(killed)}"
    print(f"OK: all 7 k=10 rows killed by exact three-block nonnegativity "
          f"(Farkas-certified, no solver). Reproduces section 15.1.")
    json.dump({"killed": killed, "n_kills": len(killed)},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
