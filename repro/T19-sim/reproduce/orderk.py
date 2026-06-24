"""
orderk.py -- general order-r support-weight feasibility, built on the validated
engine (support_weight_lib).  Handles any order r (r=2, and the r=3
"third support-weight / shortening-dimension" escalation).

For a doubly-even self-orthogonal D = [n,k] with 1_n in D and known W_D, the
unknowns are the support-weight distributions A^2, ..., A^r (A^0, A^1 are known).
For each order u in 2..r the genuine constraints are:

  primal:  A_i^u >= 0;  A_i^u = 0 unless d_u(D) <= i <= n  (Griesmer trim), and
           for u=2, i even (doubly-even);  sum_i A_i^u = [k,u]_2;
           A_n^u >= [k-1, u-1]_2   (u-subcodes spanned together with 1_n).
  dual:    tilde A^u = sum_{w=0}^u M_w^u A^w  must satisfy  tilde A_i^u >= 0;
           tilde A_i^u = 0 for i < d_u(D^perp);  sum_i tilde A_i^u = [n-k,u]_2;
           tilde A_n^u >= [n-k-1, u-1]_2.

All bounds are provable necessary conditions, so an exact-LP INFEASIBLE proves D
cannot exist.  Verdict from `glpsol --exact`; scipy float reported as cross-check.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from fractions import Fraction
from math import lcm

import support_weight_lib as L


@dataclass
class OrderResult:
    n: int
    k: int
    r: int
    label: str
    exact_feasible: bool | None
    float_feasible: bool | None
    nvars: int
    detail: str = ""
    var_orders: dict = field(default_factory=dict)


def _weight_to_A1(W, n):
    A1 = [Fraction(0)] * (n + 1)
    for i in range(1, n + 1):
        A1[i] = Fraction(W[i])
    return A1


def _primal_support(n, u, d_u_lo, doubly_even):
    if u == 2 and doubly_even:
        sup = [i for i in range(d_u_lo, n + 1) if i % 2 == 0]
    else:
        sup = [i for i in range(d_u_lo, n + 1)]
    if n not in sup:
        sup.append(n)
    return sorted(set(sup))


def build_order_constraints(n, k, WD, WDperp, r, doubly_even=True,
                            primal_has_one=True, dual_has_one=True):
    """Build the coupled order-2..r feasibility system.  Returns
    (variables, eq_rows, ge_rows, meta) with variable keys (u, i)."""
    e0 = [Fraction(1)] + [Fraction(0)] * n
    known = {0: e0, 1: _weight_to_A1(WD, n)}

    d1 = L.min_distance_from_W(WD)
    d1p = L.min_distance_from_W(WDperp)

    # primal unknown supports per order
    support = {}
    for u in range(2, r + 1):
        support[u] = _primal_support(n, u, max(u, L.griesmer_d_lower(d1, u)), doubly_even)

    variables = [(u, i) for u in range(2, r + 1) for i in support[u]]

    eq_rows, ge_rows = [], []

    # ---- primal structural constraints, per order ----
    for u in range(2, r + 1):
        Gku = L.gaussian_binomial_int(k, u)
        eq_rows.append(({(u, i): Fraction(1) for i in support[u]}, Fraction(Gku)))
        for i in support[u]:
            ge_rows.append(({(u, i): Fraction(1)}, Fraction(0)))
        if primal_has_one:
            lo = L.gaussian_binomial_int(k - 1, u - 1)   # u-subcodes spanned with 1_n
            ge_rows.append(({(u, n): Fraction(1)}, Fraction(lo)))

    # ---- dual constraints, per order:  tilde A^u = sum_w M_w^u A^w ----
    for u in range(2, r + 1):
        # constant part from known A^0, A^1
        c = [Fraction(0)] * (n + 1)
        for w in (0, 1):
            Mv = L.matvec(L.M_matrix(w, u, n, k, 2), known[w])
            for i in range(n + 1):
                c[i] += Mv[i]
        # coefficient matrices for unknown orders 2..u
        Mcoef = {w: L.M_matrix(w, u, n, k, 2) for w in range(2, u + 1)}

        def tilde_coeffs(i):
            d = {}
            for w in range(2, u + 1):
                Mw = Mcoef[w]
                for j in support[w]:
                    val = Mw[i][j]
                    if val:
                        d[(w, j)] = d.get((w, j), Fraction(0)) + val
            return d

        Gnku = L.gaussian_binomial_int(n - k, u)
        d_up_lo = max(u, L.griesmer_d_lower(d1p, u))

        # dual total: sum_i tilde A_i^u = Gnku
        total = {}
        const_total = Fraction(0)
        for i in range(n + 1):
            const_total += c[i]
            for key, val in tilde_coeffs(i).items():
                total[key] = total.get(key, Fraction(0)) + val
        eq_rows.append((total, Fraction(Gnku) - const_total))

        for i in range(n + 1):
            coeffs = tilde_coeffs(i)
            if i < d_up_lo:
                eq_rows.append((coeffs, -c[i]))          # tilde A_i^u = 0
            else:
                lo = Fraction(0)
                if i == n and dual_has_one:
                    lo = Fraction(L.gaussian_binomial_int(n - k - 1, u - 1))
                ge_rows.append((coeffs, lo - c[i]))      # tilde A_i^u >= lo

    meta = dict(support=support, d1=d1, d1p=d1p)
    return variables, eq_rows, ge_rows, meta


# ---------------------------------------------------------------------------
# Exact LP feasibility (glpsol --exact) with generic variable keys.
# ---------------------------------------------------------------------------
def _scale_int(coeffs, rhs):
    m = 1
    for x in list(coeffs.values()) + [rhs]:
        m = lcm(m, x.denominator)
    return {k: int(c * m) for k, c in coeffs.items()}, int(rhs * m)


def _emit_lp(variables, eq_rows, ge_rows):
    name = {key: f"x{j}" for j, key in enumerate(variables)}
    first = name[variables[0]]
    out = ["Minimize", f" obj: 0 {first}", "Subject To"]
    idx = 0
    for coeffs, rhs in eq_rows:
        ic, ir = _scale_int(coeffs, rhs)
        terms = " ".join(f"{'+' if v >= 0 else '-'} {abs(v)} {name[k]}"
                         for k, v in ic.items() if v != 0)
        out.append(f" e{idx}: {terms if terms else f'+ 0 {first}'} = {ir}")
        idx += 1
    for coeffs, rhs in ge_rows:
        ic, ir = _scale_int(coeffs, rhs)
        terms = " ".join(f"{'+' if v >= 0 else '-'} {abs(v)} {name[k]}"
                         for k, v in ic.items() if v != 0)
        if not terms:
            continue
        out.append(f" g{idx}: {terms} >= {ir}")
        idx += 1
    out.append("Bounds")
    for key in variables:
        out.append(f" {name[key]} >= 0")
    out.append("End")
    return "\n".join(out) + "\n"


def glpsol_exact_feasible(variables, eq_rows, ge_rows, timeout=600):
    """DEPRECATED for n>=~24: GLPK's LP-format reader parses coefficients as C
    doubles, so exact cancellations among >15-digit coefficients are destroyed
    (false infeasibles).  Kept only for small-coefficient cross-checks.  Use
    ppl_feasible for the real runs."""
    lp = _emit_lp(variables, eq_rows, ge_rows)
    with tempfile.TemporaryDirectory() as d:
        lpf = os.path.join(d, "m.lp")
        with open(lpf, "w") as fh:
            fh.write(lp)
        try:
            out = subprocess.run(
                ["glpsol", "--exact", "--lp", lpf, "--output", os.path.join(d, "o.txt")],
                capture_output=True, text=True, timeout=timeout).stdout
        except FileNotFoundError:
            return None, "glpsol not found"
        except subprocess.TimeoutExpired:
            return None, "timeout"
    if re.search(r"NO (PRIMAL )?FEASIBLE SOLUTION|PROBLEM HAS NO", out, re.I):
        return False, "infeasible"
    if re.search(r"OPTIMAL|value =", out, re.I):
        return True, ""
    return None, out.strip()[-200:]


_SAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ppl_solver.sage")


def _ppl_problem(variables, eq_rows, ge_rows):
    """Serialize one LP to the PPL-solver JSON shape with EXACT integer coeffs."""
    name = {key: f"x{j}" for j, key in enumerate(variables)}
    rows = []
    for coeffs, rhs in eq_rows:
        ic, ir = _scale_int(coeffs, rhs)
        rows.append([[[name[k], v] for k, v in ic.items() if v != 0], ir, "eq"])
    for coeffs, rhs in ge_rows:
        ic, ir = _scale_int(coeffs, rhs)
        terms = [[name[k], v] for k, v in ic.items() if v != 0]
        if terms:
            rows.append([terms, ir, "ge"])
    return {"vars": [name[k] for k in variables], "rows": rows}


def _run_sage_chunk(payload, timeout):
    """Solve one chunk of serialized problems in a single Sage process."""
    import json
    with tempfile.TemporaryDirectory() as d:
        inf, outf = os.path.join(d, "in.json"), os.path.join(d, "out.json")
        with open(inf, "w") as fh:
            json.dump(payload, fh)
        try:
            r = subprocess.run(["sage", _SAGE, inf, outf],
                               capture_output=True, text=True, timeout=timeout)
        except FileNotFoundError:
            return [None] * len(payload)
        except subprocess.TimeoutExpired:
            return [None] * len(payload)
        if not os.path.exists(outf):
            raise RuntimeError(f"PPL solver failed:\n{r.stdout[-500:]}\n{r.stderr[-800:]}")
        return json.load(open(outf))


def ppl_feasible_batch(problems, timeout=3600, workers=1):
    """Exact LP feasibility for a batch of (variables, eq_rows, ge_rows) via Sage
    PPL.  Returns list[bool|None].

    workers>1 fans the problems across that many CONCURRENT Sage processes
    (round-robin, so chunks are load-balanced across problem sizes).  Each solve
    is independent, so this is embarrassingly parallel."""
    import json
    from concurrent.futures import ThreadPoolExecutor
    payload = [_ppl_problem(*p) for p in problems]
    nchunks = max(1, min(workers, len(payload)))
    if nchunks == 1:
        return _run_sage_chunk(payload, timeout)
    chunks = [[] for _ in range(nchunks)]
    idxmap = [[] for _ in range(nchunks)]
    for i, p in enumerate(payload):
        chunks[i % nchunks].append(p)
        idxmap[i % nchunks].append(i)
    results = [None] * len(payload)
    with ThreadPoolExecutor(max_workers=nchunks) as ex:          # threads just wait on subprocesses
        futs = {ex.submit(_run_sage_chunk, chunks[c], timeout): c for c in range(nchunks)}
        for fut in futs:
            c = futs[fut]
            res = fut.result()
            for local_i, global_i in enumerate(idxmap[c]):
                results[global_i] = res[local_i] if local_i < len(res) else None
    return results


def ppl_feasible(variables, eq_rows, ge_rows, timeout=3600):
    return ppl_feasible_batch([(variables, eq_rows, ge_rows)], timeout)[0]


def scipy_float_feasible(variables, eq_rows, ge_rows):
    try:
        from scipy.optimize import linprog
    except Exception:
        return None
    idx = {key: j for j, key in enumerate(variables)}
    nv = len(variables)
    A_eq, b_eq, A_ub, b_ub = [], [], [], []
    for coeffs, rhs in eq_rows:
        row = [0.0] * nv
        for k, c in coeffs.items():
            row[idx[k]] = float(c)
        A_eq.append(row); b_eq.append(float(rhs))
    for coeffs, rhs in ge_rows:
        row = [0.0] * nv
        for k, c in coeffs.items():
            row[idx[k]] = -float(c)
        A_ub.append(row); b_ub.append(-float(rhs))
    res = linprog([0.0] * nv, A_ub or None, b_ub or None, A_eq or None, b_eq or None,
                  bounds=[(0, None)] * nv, method="highs")
    return bool(res.success)


def check_order(n, k, WD, WDperp, r, label="", doubly_even=True,
                primal_has_one=True, dual_has_one=True, do_float=False):
    variables, eq_rows, ge_rows, meta = build_order_constraints(
        n, k, WD, WDperp, r, doubly_even, primal_has_one, dual_has_one)
    exact = ppl_feasible(variables, eq_rows, ge_rows)   # EXACT input (PPL), not glpsol
    flt = scipy_float_feasible(variables, eq_rows, ge_rows) if do_float else None
    var_orders = {u: len([1 for (uu, _i) in variables if uu == u]) for u in range(2, r + 1)}
    return OrderResult(n=n, k=k, r=r, label=label, exact_feasible=exact,
                       float_feasible=flt, nvars=len(variables), detail="",
                       var_orders=var_orders)


def _satisfies(variables, eq_rows, ge_rows, assignment):
    val = {key: Fraction(assignment.get(key, 0)) for key in variables}
    for coeffs, rhs in eq_rows:
        if sum(c * val[k] for k, c in coeffs.items()) != rhs:
            return False
    for coeffs, rhs in ge_rows:
        if sum(c * val[k] for k, c in coeffs.items()) < rhs:
            return False
    return True


def _self_test():
    print("orderk model self-test (r=2 and r=3)")
    e8 = L.rows_from_matrix([
        [1, 0, 0, 0, 0, 1, 1, 1], [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 1, 0, 1], [0, 0, 0, 1, 1, 1, 1, 0]])
    c73 = L.rows_from_matrix([
        [1, 0, 0, 1, 1, 0, 1], [0, 1, 0, 1, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1]])

    cases = []
    for gen, n in [(e8, 8), (c73, 7)]:
        k = len(gen)
        dual = L.gf2_dual_basis(gen, n)
        A = L.all_support_weight_distributions(gen, n, 3)
        Ad = L.all_support_weight_distributions(dual, n, 3)
        W = [A[0][i] + A[1][i] for i in range(n + 1)]
        Wd = [Ad[0][i] + Ad[1][i] for i in range(n + 1)]
        allone = (1 << n) - 1
        h1 = any(cw == allone for cw in L.codeword_table(gen, n))
        h2 = any(cw == allone for cw in L.codeword_table(dual, n))
        de = all(i % 4 == 0 for i in range(n + 1) if W[i])   # doubly-even iff all wts ≡ 0 (4)
        cases.append((f"{'e8' if n==8 else 'C73'}[{n},{k}]", n, k, W, Wd, A, de, h1, h2))

    ok_all = True
    for r in (2, 3):
        for label, n, k, W, Wd, A, de, h1, h2 in cases:
            variables, eq, ge, meta = build_order_constraints(
                n, k, W, Wd, r, doubly_even=de, primal_has_one=h1, dual_has_one=h2)
            true_assign = {(u, i): A[u][i] for u in range(2, r + 1)
                           for i in range(n + 1) if (u, i) in set(variables)}
            ok_true = _satisfies(variables, eq, ge, true_assign)
            exact, _ = glpsol_exact_feasible(variables, eq, ge)
            ok = ok_true and exact
            ok_all &= ok
            print(f"  r={r} {label:10s}: true A^* satisfies={ok_true}  glpsol feasible={exact}  "
                  f"vars={len(variables)}  {'OK' if ok else 'FAIL'}")
    assert ok_all, "orderk self-test FAILED"
    print("  orderk self-test PASSED")


if __name__ == "__main__":
    _self_test()
