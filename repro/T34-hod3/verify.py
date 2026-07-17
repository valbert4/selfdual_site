#!/usr/bin/env python3
"""
T34 -- higher-order Delsarte LP (level 3, genus-3 / triweight): exact-replayable
verifier of the transform core.

T34's full result -- the level-3 LP saturates (0 kills on the 21 unresolved
menu rows) -- is solver-required (exact PPL feasibility) and lives in the
research repo (`higher_delsarte/level3_model.py --sweep`). This bundle certifies,
with the Python standard library only and no solver, the exact genus-3
machinery that the level-3 model is built on:

  (A) the valid genus-3 column-type count (2593) and its AGL(3,2)-orbit count
      (26) -- the primal variable set of the level-3 LP;
  (B) the genus-3 MacWilliams / Fourier identity, verified end-to-end on the
      self-dual code e8 = RM(1,3): sum_m N_m c_{p,m} == |E|^3 N'_p for every
      dual monomial p (and 0 off-support) -- the coupling the LP imposes;
  (C) the closed-form sparse-point coefficient `sparse_coeff` == the general
      `macwilliams_coeff` (the cheap dual-cut evaluator);
  (D) the coefficient symmetry  c_{p,m} * prod(p!) == c_{m,p} * prod(m!).

Run:  python3 verify.py      (exit 0 iff every check reproduces)
"""
from fractions import Fraction  # noqa: F401  (kept for parity; not needed)
from itertools import product
from math import comb, factorial
import sys

N = 40           # length of the residual child E
NZ = 8           # |F_2^3|
S = (0, 16, 20, 24, 40)     # allowed nonzero weights of E


# --------------------------------------------------------------------------- #
#  Kernel and exact transform coefficient c_{p,m} = [x^p] prod_z L_z^{m_z}     #
# --------------------------------------------------------------------------- #
def sign(z, w):
    return -1 if (bin(z & w).count("1") & 1) else 1


def macwilliams_coeff(m, p, n, g=3):
    """[x^p] prod_z (sum_w sign(z,w) x_w)^{m_z} over F_2^g, exact integer.
    DP over the 2^g columns with suffix-budget pruning."""
    nz = 1 << g
    m = tuple(int(x) for x in m)
    p = tuple(int(x) for x in p)
    if len(m) != nz or len(p) != nz or sum(m) != n or sum(p) != n:
        return 0
    SGN = [[sign(z, w) for w in range(nz)] for z in range(nz)]

    def col_terms(w, r):
        target = p[w]
        res = {}
        suf = [0] * (nz + 1)
        for s in range(nz - 1, -1, -1):
            suf[s] = suf[s + 1] + r[s]
        if target > suf[0]:
            return res

        def rec(slot, rem, coeff, newr):
            if slot == nz:
                if rem == 0:
                    res[newr] = res.get(newr, 0) + coeff
                return
            rz = r[slot]
            s = SGN[slot][w]
            hi = min(rz, rem)
            lo = max(0, rem - suf[slot + 1])
            for a in range(lo, hi + 1):
                c2 = coeff * comb(rz, a)
                if s < 0 and (a & 1):
                    c2 = -c2
                rec(slot + 1, rem - a, c2, newr + (rz - a,))
        rec(0, target, 1, ())
        return res

    states = {m: 1}
    for w in range(nz):
        nxt = {}
        for r, cf in states.items():
            for nr, add in col_terms(w, r).items():
                if add:
                    nxt[nr] = nxt.get(nr, 0) + cf * add
        states = nxt
    return states.get((0,) * nz, 0)


def sparse_coeff(m, dirs, masses):
    """c_{p,m} for a sparse dual point p (big mass on slot 0, small `masses` on
    slots `dirs`), in closed form: group m_z by the sign pattern of the dirs and
    extract [prod t_i^{a_i}] prod_group (1 + sum_i (-1)^{pat_i} t_i)^mu."""
    k = len(dirs)
    grp = {}
    for z in range(NZ):
        pat = tuple((bin(z & d).count("1") & 1) for d in dirs)
        grp[pat] = grp.get(pat, 0) + m[z]
    poly = {(0,) * k: 1}
    for pat, mu in grp.items():
        if mu == 0:
            continue
        fac = {}

        def rec(i, rem, exps, mult):
            if i == k:
                fac[tuple(exps)] = fac.get(tuple(exps), 0) + mult
                return
            for e in range(min(masses[i], rem) + 1):
                sgn = -1 if (pat[i] and (e & 1)) else 1
                rec(i + 1, rem - e, exps + [e], mult * comb(rem, e) * sgn)
        rec(0, mu, [], 1)
        nxt = {}
        for ea, ca in poly.items():
            for eb, cb in fac.items():
                ne = tuple(ea[i] + eb[i] for i in range(k))
                if all(ne[i] <= masses[i] for i in range(k)):
                    nxt[ne] = nxt.get(ne, 0) + ca * cb
        poly = nxt
    return poly.get(tuple(masses), 0)


# --------------------------------------------------------------------------- #
#  Valid genus-3 column types + AGL(3,2) orbits                               #
# --------------------------------------------------------------------------- #
def span_weights(m):
    out = []
    for y in range(1, NZ):
        out.append(sum(m[z] for z in range(NZ) if bin(y & z).count("1") & 1))
    return out


def valid_types():
    """Genus-3 monomials (sum N) whose 7 nonzero span weights all lie in S, via
    Walsh inversion (5^7 assignments)."""
    out = []
    for ws in product(S, repeat=NZ - 1):
        D = [N] + [N - 2 * w for w in ws]
        m = []
        ok = True
        for z in range(NZ):
            t = sum(D[y] * (-1 if (bin(y & z).count("1") & 1) else 1)
                    for y in range(NZ))
            if t % NZ or t < 0:
                ok = False
                break
            m.append(t // NZ)
        if ok:
            out.append(tuple(m))
    return out


def _gl3():
    mats = []
    for bits in range(1 << 9):
        col = [(bits >> (3 * c)) & 7 for c in range(3)]
        c0, c1, c2 = col
        if 0 in col or c1 == c0 or c2 == c0 or c2 == c1 or c2 == (c0 ^ c1):
            continue
        perm = []
        for z in range(8):
            r = 0
            if z & 1:
                r ^= c0
            if z & 2:
                r ^= c1
            if z & 4:
                r ^= c2
            perm.append(r)
        mats.append(tuple(perm))
    return mats


def agl_perms():
    perms = set()
    for A in _gl3():
        for c in range(8):
            perms.add(tuple(A[z] ^ c for z in range(8)))
    return [list(p) for p in perms]


def orbit_count(types):
    tset = set(types)
    AGL = agl_perms()
    seen = set()
    n = 0
    for m in types:
        if m in seen:
            continue
        n += 1
        for perm in AGL:
            out = [0] * NZ
            for z in range(NZ):
                out[perm[z]] += m[z]
            t = tuple(out)
            if t in tset:
                seen.add(t)
    return n, len(AGL)


# --------------------------------------------------------------------------- #
#  e8 = RM(1,3) genus-3 MacWilliams end-to-end check                          #
# --------------------------------------------------------------------------- #
def e8_codewords():
    """RM(1,3) = [8,4,4], self-dual doubly-even: generator = all-ones + the 3
    coordinate bits over F_2^3."""
    n, k = 8, 4
    cols = []
    for j in range(n):
        c = 1
        for b in range(3):
            if (j >> b) & 1:
                c |= 1 << (b + 1)
        cols.append(c)
    words = []
    for msg in range(1 << k):
        w = 0
        for pos, col in enumerate(cols):
            if bin(msg & col).count("1") & 1:
                w |= 1 << pos
        words.append(w)
    return words, n, k


def genus3_enum(words, n):
    """Brute complete genus-3 enumerator {m: count} over ordered triples."""
    enum = {}
    for u in words:
        for v in words:
            for w in words:
                m = [0] * NZ
                for j in range(n):
                    z = ((u >> j) & 1) + 2 * ((v >> j) & 1) + 4 * ((w >> j) & 1)
                    m[z] += 1
                key = tuple(m)
                enum[key] = enum.get(key, 0) + 1
    return enum


# --------------------------------------------------------------------------- #
def main():
    ok = True

    # (A) primal variable set
    T = valid_types()
    nvalid = len(T)
    norb, nagl = orbit_count(T)
    a_ok = (nvalid == 2593 and norb == 26 and nagl == 1344)
    print(f"(A) valid genus-3 types = {nvalid} (want 2593); "
          f"AGL(3,2) orbits = {norb} (want 26); |AGL| = {nagl} (want 1344): "
          f"{'OK' if a_ok else 'FAIL'}")
    ok &= a_ok

    # (B) genus-3 MacWilliams on e8 (self-dual): sum_m N_m c_{p,m} == 2^{3k} N_p
    w8, n8, k8 = e8_codewords()
    from collections import Counter
    assert Counter(bin(x).count("1") for x in w8) == Counter({0: 1, 4: 14, 8: 1})
    Ne = genus3_enum(w8, n8)
    scale = 1 << (3 * k8)          # |E|^3 = 2^12
    supp = list(Ne)
    b_ok = True
    for p in supp:
        s = sum(Ne[m] * macwilliams_coeff(m, p, n8) for m in Ne)
        if s != scale * Ne[p]:
            b_ok = False
            break
    # off-support: a few sparse p not in support must transform to 0
    off = 0
    for z in range(8):
        for aa in (2, 4, n8):
            p = [0] * 8
            p[z] = aa
            p = tuple(p)
            if sum(p) != n8 or p in Ne:
                continue
            if sum(Ne[m] * macwilliams_coeff(m, p, n8) for m in Ne) != 0:
                b_ok = False
            off += 1
    print(f"(B) e8=RM(1,3) genus-3 MacWilliams: sum_m N_m c_{{p,m}} == 2^12 N_p "
          f"over all {len(supp)} support pts + {off} off-support: "
          f"{'OK' if b_ok else 'FAIL'}")
    ok &= b_ok

    # (C) sparse_coeff == macwilliams_coeff on a sample
    c_ok = True
    tried = 0
    cases = [(0, [(1,)], [(2,)]), (0, [(1, 2)], [(2, 3)]),
             (0, [(1, 2, 4)], [(1, 2, 1)]), (0, [(3, 5, 6)], [(2, 1, 2)])]
    idx = 0
    for m in T[::137]:                 # a spread-out sample of valid types
        for _, dirs_l, masses_l in cases:
            dirs, masses = dirs_l[0], masses_l[0]
            p = [0] * 8
            p[0] = N - sum(masses)
            for d, aa in zip(dirs, masses):
                p[d] += aa
            if macwilliams_coeff(m, tuple(p), N) != sparse_coeff(m, dirs, masses):
                c_ok = False
            tried += 1
    print(f"(C) sparse_coeff == macwilliams_coeff over {tried} cases: "
          f"{'OK' if c_ok else 'FAIL'}")
    ok &= c_ok

    # (D) coefficient symmetry  c_{p,m} prod(p!) == c_{m,p} prod(m!)
    d_ok = True
    dtried = 0
    for m in T[:20]:
        for z1, z2 in [(1, 2), (3, 5)]:
            p = [0] * 8
            p[0] = N - 4
            p[z1] += 2
            p[z2] += 2
            p = tuple(p)
            cpm = macwilliams_coeff(m, p, N)
            cmp_ = macwilliams_coeff(p, m, N)
            pm = 1
            pp = 1
            for x in m:
                pm *= factorial(x)
            for x in p:
                pp *= factorial(x)
            if cpm * pp != cmp_ * pm:
                d_ok = False
            dtried += 1
    print(f"(D) c_{{p,m}} prod(p!) == c_{{m,p}} prod(m!) over {dtried} cases: "
          f"{'OK' if d_ok else 'FAIL'}")
    ok &= d_ok

    print()
    print("Result: T34 genus-3 transform core reproduced exactly." if ok
          else "Result: FAILED")
    print("Full level-3 sweep (0 kills / 21 unresolved rows) is solver-required: "
          "research repo higher_delsarte/level3_model.py --sweep (exact PPL).")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
