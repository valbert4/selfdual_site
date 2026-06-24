"""
certify_kill.py -- self-contained exact proof that menu row (k,a,b)=(6,1,60) is
infeasible at order 4.

Builds the exact order-4 system, converts it to uniform '>=' integer form
{G x >= h}, asks Sage/PPL only to FIND a Farkas vector y (y >= 0, y^T G = 0,
y^T h > 0), then VERIFIES that vector in pure Fraction arithmetic.  The proof
does not depend on trusting the solver: if y^T G = 0 (exactly) and y^T h > 0
(exactly) with y >= 0, then G x >= h has no solution, period.

Run:  python3 certify_kill.py            # (6,1,60) by default
      python3 certify_kill.py 6 1 60
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from fractions import Fraction

import support_weight_lib as L
import orderk

FARKAS_SAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ppl_farkas.sage")


def ge_form(variables, eq_rows, ge_rows):
    """Convert (eq, ge) Fraction constraints + x>=0 to integer rows {sum coef*x_j >= rhs}.
    Returns (N, rows) with rows = [ (dict[j->int], int_rhs) ], j indexing variables."""
    idx = {key: j for j, key in enumerate(variables)}
    rows = []
    for coeffs, rhs in eq_rows:
        ic, ir = orderk._scale_int(coeffs, rhs)
        d = {idx[k]: v for k, v in ic.items() if v}
        rows.append((d, ir))                                  # sum >= rhs
        rows.append(({j: -v for j, v in d.items()}, -ir))     # -sum >= -rhs
    for coeffs, rhs in ge_rows:
        ic, ir = orderk._scale_int(coeffs, rhs)
        d = {idx[k]: v for k, v in ic.items() if v}
        if d:
            rows.append((d, ir))
    for j in range(len(variables)):                           # x_j >= 0
        rows.append(({j: 1}, 0))
    return len(variables), rows


def find_farkas(N, rows):
    payload = {"nvars": N, "rows": [[[[j, c] for j, c in d.items()], h] for d, h in rows]}
    with tempfile.TemporaryDirectory() as t:
        inf, outf = os.path.join(t, "in.json"), os.path.join(t, "out.json")
        json.dump(payload, open(inf, "w"))
        subprocess.run(["sage", FARKAS_SAGE, inf, outf], capture_output=True, text=True, timeout=900)
        if not os.path.exists(outf):
            return None
        return json.load(open(outf))


def verify_farkas(rows, y):
    """Exact check: y >= 0, y^T G = 0 (per column), y^T h > 0."""
    N = max((j for d, _ in rows for j in d), default=-1) + 1
    colsum = [Fraction(0)] * N
    hdot = Fraction(0)
    for i, (d, h) in enumerate(rows):
        yi = y.get(i, Fraction(0))
        if yi < 0:
            return False, f"y[{i}]<0"
        if yi == 0:
            continue
        for j, c in d.items():
            colsum[j] += yi * c
        hdot += yi * h
    if any(c != 0 for c in colsum):
        bad = [j for j, c in enumerate(colsum) if c != 0]
        return False, f"y^T G != 0 at columns {bad[:8]}"
    if hdot <= 0:
        return False, f"y^T h = {hdot} (not > 0)"
    return True, f"y^T G = 0 exactly, y^T h = {hdot} > 0"


def certify(n, k, WD, WDperp, r, doubly_even=True, primal_has_one=True, dual_has_one=True):
    """Find + exactly verify a Farkas certificate of order-r infeasibility.
    Returns (proven: bool, n_multipliers: int|None, detail: str).  proven=False
    with n_multipliers=None means the system is feasible (no kill)."""
    variables, eq_rows, ge_rows, _ = orderk.build_order_constraints(
        n, k, WD, WDperp, r, doubly_even, primal_has_one, dual_has_one)
    N, rows = ge_form(variables, eq_rows, ge_rows)
    cert = find_farkas(N, rows)
    if not cert or not cert.get("found"):
        return False, None, "feasible (no Farkas certificate)"
    y = {int(i): Fraction(s) for i, s in cert["y"].items()}
    ok, detail = verify_farkas(rows, y)
    return ok, len(y), detail


def main():
    k, a, b = (int(x) for x in sys.argv[1:4]) if len(sys.argv) >= 4 else (6, 1, 60)
    n = 40
    WE = [0] * (n + 1); WE[0] = 1; WE[16] += a; WE[24] += a; WE[20] += b; WE[40] += 1
    WEp = [int(x) for x in L.macwilliams_transform(WE, n, 2, 2 ** k)]
    print(f"Certifying order-4 infeasibility of (k,a,b)=({k},{a},{b})")
    proven, nmult, detail = certify(n, k, WE, WEp, 4)
    if nmult is None:
        print(f"  {detail} -> NO kill.")
        sys.exit(1)
    print(f"  Farkas vector: {nmult} nonzero multipliers")
    print(f"  EXACT verification: {detail}")
    if proven:
        print(f"  ==> PROVEN: (k,a,b)=({k},{a},{b}) is INFEASIBLE at order 4 (kill certified).")
    else:
        print(f"  ==> certificate FAILED verification: {detail}")
        sys.exit(1)


if __name__ == "__main__":
    main()
