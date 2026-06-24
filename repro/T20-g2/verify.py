#!/usr/bin/env python3
"""
T20 -- coupled genus-2 biweight feasibility: exact-replayable verifier.

Reproduces the kill of (k=9, a=239, b=32). The closure-tied coupled genus-2
(biweight) family of E <-> E^perp reduces (exact Sage QQ) to an affine family of
dimension 2: every orbit count is

    orbit_value_j  =  particular_j + sum_i Kint[i][j] * z_i        ( >= 0 required )

over the two free kernel coordinates z.  For this row no z makes all 463 orbit
counts nonnegative -- certified by a Farkas vector y_j >= 0 with
    sum_j y_j * Kint[i][j] = 0   (each kernel coord i),
    sum_j y_j * particular_j = -1 < 0,
so  0 <= sum_j y_j * orbit_value_j = sum_j y_j * particular_j = -1, a contradiction.

The certificate (`system.json`) was generated once by the Sage biweight setup
(`the project's solver`); this verifier only CHECKS it.  Pure Python.

Run:  python3 verify.py
"""
from fractions import Fraction as F
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    data = json.load(open(os.path.join(HERE, "system.json")))
    forms = data["forms"]          # forms[j] = [particular_j, Kint[0][j], ..., Kint[dim-1][j]]
    y = data["farkas_y"]           # {j: value}
    dim = data["affine_dim"]
    assert data["row"] == [9, 239, 32]

    s_part = F(0)
    s_kernel = [F(0)] * dim
    for j_str, yv in y.items():
        j = int(j_str)
        yy = F(yv)
        assert yy >= 0, f"y[{j}] = {yy} < 0"
        row = forms[j]
        s_part += yy * F(row[0])
        for i in range(dim):
            s_kernel[i] += yy * F(row[1 + i])

    print(f"T20: coupled genus-2 family, {data['n_vars']} orbit vars, affine dim {dim}; "
          f"Farkas support {len(y)}.")
    print(f"     sum y*Kint[i] = {[str(x) for x in s_kernel]} (must be 0); "
          f"sum y*particular = {s_part} (must be < 0)")
    assert all(x == 0 for x in s_kernel), "Farkas combination of kernel columns is not 0"
    assert s_part < 0, f"sum y*particular = {s_part} is not < 0 (no contradiction)"
    print("OK: (9,239,32) PROVEN infeasible -- the coupled genus-2 family has no "
          "nonnegative point (Farkas-certified, no solver). Reproduces section 27.1.")
    json.dump({"row": [9, 239, 32], "affine_dim": dim, "killed": True},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
