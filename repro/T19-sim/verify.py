#!/usr/bin/env python3
"""
T19 -- Simonis support-weight feasibility: exact-replayable verifier.

Reproduces the kill of (k=6, a=1, b=60). The order-4 Simonis support-weight
system couples the order-4 subcode support distributions of E and E^perp; for
this row it is infeasible, certified by a Farkas vector.

This verifier rebuilds the exact integer order-4 system {G x >= h} in pure Python
(orderk + support_weight_lib use only fractions), loads the stored Farkas vector
`cert.json`, and checks y >= 0, y^T G = 0, y^T h > 0 -- which makes the system
0 = y^T(Gx) >= y^T h > 0, a contradiction.  No solver: the certificate was found
once by Sage/PPL (`the project's solver`); here it is only verified.

Run:  python3 verify.py        (pure Python standard library)
"""
from fractions import Fraction
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "reproduce"))
import support_weight_lib as L      # noqa: E402  (pure Python)
import orderk                       # noqa: E402  (pure Python)
import certify_kill as C            # noqa: E402  (ge_form + verify_farkas; pure)


def main():
    cert = json.load(open(os.path.join(HERE, "cert.json")))
    k, a, b, n, r = cert["k"], cert["a"], cert["b"], cert["n"], cert["r"]
    assert (k, a, b, r) == (6, 1, 60, 4)

    WE = [0] * (n + 1)
    WE[0] = 1
    WE[16] += a
    WE[24] += a
    WE[20] += b
    WE[40] += 1
    WEp = [int(x) for x in L.macwilliams_transform(WE, n, 2, 2 ** k)]

    variables, eq_rows, ge_rows, _ = orderk.build_order_constraints(
        n, k, WE, WEp, r, True, True, True)
    _, rows = C.ge_form(variables, eq_rows, ge_rows)

    y = {int(i): Fraction(s) for i, s in cert["y"].items()}
    ok, detail = C.verify_farkas(rows, y)
    print(f"T19: order-{r} system rebuilt ({len(rows)} integer rows); "
          f"Farkas vector has {len(y)} multipliers.")
    print(f"     exact check: {detail}")
    assert ok, f"Farkas certificate failed verification: {detail}"
    print(f"OK: (k,a,b)=({k},{a},{b}) PROVEN infeasible at order {r} "
          f"(Simonis support-weight), Farkas-certified, no solver. Reproduces section 9.")
    json.dump({"row": [k, a, b], "order": r, "multipliers": len(y), "killed": True},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
