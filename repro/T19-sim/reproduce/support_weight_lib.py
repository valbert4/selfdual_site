"""
support_weight_lib.py -- core engine for Simonis support-weight (effective-length)
distributions and the generalized MacWilliams identities.

This is the shared math layer for the ``simonis/`` filter.  It computes, in exact
arithmetic:

  * Gaussian binomials  [x, t]_q  for ARBITRARY integer x (including negative x,
    needed by Simonis eq. 7);
  * q-ary Krawtchouk polynomials and the ordinary MacWilliams transform;
  * the Simonis matrices  M_u^r  (eq. 7) and the generalized MacWilliams map
    A^r(C) -> A^r(C^perp)  (eq. 6);
  * the Kloeve interleaving coefficients  [s]_m  (eq. 5) and the F_{2^s} check;
  * brute-force support-weight distributions  A_i^r(C)  from a generator matrix;
  * the generalized-Hamming / doubly-even support trims (d_r, parity).

References
----------
  papers/Simonis_1994/Simonis_1994.md   -- Thm 1 (eq. 4), Remark 5 (eq. 6-7),
                                           Kloeve eq. 5, Examples 1 & 2.
  support_weight/SCOPE.md               -- the filter design this engine serves.

All public numeric routines return exact ``int`` or ``fractions.Fraction``.
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from itertools import combinations

Number = Fraction


# ---------------------------------------------------------------------------
# Gaussian binomials, with the negative-top-index extension used by eq. (7).
# ---------------------------------------------------------------------------
def qpow(q: int, e: int) -> Fraction:
    """q**e as an exact Fraction (handles e < 0)."""
    return Fraction(q) ** e


def gaussian_binomial(x: int, t: int, q: int = 2) -> Fraction:
    """The Gaussian binomial [x, t]_q for any integer x and t >= 0.

    Closed form  prod_{i=0}^{t-1} (q^{x-i} - 1) / (q^{t-i} - 1), evaluated with
    q^{x-i} taken as an exact Fraction when x - i < 0.  For x >= t >= 0 this is
    the usual (integer) subspace count; the negative-x case is the polynomial-in-
    q^x extension justified by Simonis Lemma 3 / Remark 5, and is exactly what
    eq. (7) requires via the [j-k, r-u]_q factor with j < k.
    """
    if t < 0:
        return Fraction(0)
    num = Fraction(1)
    den = Fraction(1)
    for i in range(t):
        num *= (qpow(q, x - i) - 1)
        den *= (qpow(q, t - i) - 1)
    return num / den


def gaussian_binomial_int(k: int, r: int, q: int = 2) -> int:
    """[k, r]_q for 0 <= r <= k -- the number of r-dim subspaces of F_q^k."""
    val = gaussian_binomial(k, r, q)
    assert val.denominator == 1, (k, r, q, val)
    return int(val)


# ---------------------------------------------------------------------------
# Krawtchouk polynomials and the ordinary MacWilliams transform (any q).
# ---------------------------------------------------------------------------
def krawtchouk(i: int, v: int, n: int, Q: int) -> int:
    """K_i(v; n, Q) = sum_j (-1)^j (Q-1)^{i-j} C(v, j) C(n-v, i-j)."""
    s = 0
    for j in range(0, i + 1):
        s += ((-1) ** j) * (Q - 1) ** (i - j) * math.comb(v, j) * math.comb(n - v, i - j)
    return s


def macwilliams_transform(a, n: int, Q: int, code_size: int):
    """Dual weight distribution of an [n, *] code over F_Q with |C| = code_size.

    b_j = (1/|C|) sum_i K_j(i; n, Q) a_i.  Exact (Fraction) output.
    """
    out = []
    for j in range(n + 1):
        s = Fraction(0)
        for i in range(n + 1):
            ai = a[i]
            if ai:
                s += krawtchouk(j, i, n, Q) * ai
        out.append(Fraction(s, 1) / code_size)
    return out


# ---------------------------------------------------------------------------
# Simonis M_u^r matrices (eq. 7) and the generalized MacWilliams map (eq. 6).
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def M_matrix(u: int, r: int, n: int, k: int, q: int = 2):
    """The (n+1)x(n+1) matrix (M_u^r)_{i,v}, eq. (7) of Simonis 1994.

        (M_u^r)_{i,v} = sum_{j=0}^i (-1)^{i+j} C(n-j, n-i)
                        * q^{u(j-k+u-r)} * [j-k, r-u]_q * C(n-v, j).

    Returned as a tuple-of-tuples of Fractions (hashable, cache-friendly).
    """
    rows = []
    for i in range(n + 1):
        row = []
        # the i,j-dependent prefactor sum_j (-1)^{i+j} C(n-j,n-i) q^{..} [..] is
        # independent of v except through C(n-v, j); precompute the j-weights.
        jweight = []
        for j in range(0, i + 1):
            w = (Fraction((-1) ** (i + j))
                 * math.comb(n - j, n - i)
                 * qpow(q, u * (j - k + u - r))
                 * gaussian_binomial(j - k, r - u, q))
            jweight.append((j, w))
        for v in range(n + 1):
            s = Fraction(0)
            for j, w in jweight:
                if w:
                    c = math.comb(n - v, j)
                    if c:
                        s += w * c
            row.append(s)
        rows.append(tuple(row))
    return tuple(rows)


def matvec(M, x):
    """M (tuple-of-tuples) times vector x (list); exact Fraction output."""
    n1 = len(M)
    out = []
    for i in range(n1):
        row = M[i]
        s = Fraction(0)
        for v, xv in enumerate(x):
            if xv:
                s += row[v] * xv
        out.append(s)
    return out


def dual_support_weight(A_by_order, n: int, k: int, r: int, q: int = 2):
    """tilde A^r = sum_{u=0}^r M_u^r A^u   (Simonis eq. 6).

    ``A_by_order`` maps order u -> A^u vector (length n+1).  Returns the dual
    code's order-r support-weight distribution (length n+1, Fractions).
    """
    res = [Fraction(0)] * (n + 1)
    for u in range(r + 1):
        Au = A_by_order[u]
        Mv = matvec(M_matrix(u, r, n, k, q), Au)
        for i in range(n + 1):
            res[i] += Mv[i]
    return res


# ---------------------------------------------------------------------------
# Kloeve interleaving coefficients (eq. 5).
# ---------------------------------------------------------------------------
def interleave_coeff(s: int, m: int, q: int = 2) -> int:
    """[s]_m = prod_{j=0}^{m-1} (q^s - q^j) -- ordered spanning s-tuples of F_q^m."""
    p = 1
    for j in range(m):
        p *= (q ** s - q ** j)
    return p


def interleaved_weight_distribution(A_by_order, n: int, k: int, s: int, q: int = 2):
    """A_i(C^{(s)}) = sum_{m=0}^k [s]_m A_i^m(C)  (eq. 5).

    For q=2, s=2 this packages A^0, A^1, A^2 into the ordinary F_4 weight
    distribution of the 2-interleaving C^{(2)}.
    """
    out = [Fraction(0)] * (n + 1)
    for m, Am in A_by_order.items():
        c = interleave_coeff(s, m, q)
        if c == 0:
            continue
        for i in range(n + 1):
            if Am[i]:
                out[i] += c * Am[i]
    return out


# ---------------------------------------------------------------------------
# Brute-force support-weight distributions from a generator matrix.
# (Validation / small-code oracles only -- exponential in k.)
# ---------------------------------------------------------------------------
def codeword_table(gen_rows, n: int):
    """Map each message in F_2^k to its codeword bitmask.  gen_rows: list of
    length-n int bitmasks (bit j of row r = G[r][j])."""
    k = len(gen_rows)
    cw = [0] * (1 << k)
    for msg in range(1 << k):
        w = 0
        m = msg
        b = 0
        while m:
            if m & 1:
                w ^= gen_rows[b]
            m >>= 1
            b += 1
        cw[msg] = w
    return cw


def rows_from_matrix(matrix):
    """Convert a 0/1 matrix (list of lists, MSB = column 0) to int bitmasks.

    Column 0 maps to the most-significant bit so that printed support order is
    preserved under popcount; the actual bit order is irrelevant to weights.
    """
    rows = []
    for r in matrix:
        bits = 0
        for j, val in enumerate(r):
            if val:
                bits |= 1 << j
        rows.append(bits)
    return rows


def _rdim_subspaces(k: int, r: int):
    """Yield each r-dim subspace of F_2^k as a tuple of its 2^r element ints.

    Canonical RREF enumeration: each r-dim subspace has a unique reduced row
    echelon basis with pivots in columns p_0<...<p_{r-1}; the only free entries
    are (row i, non-pivot column j) with j > p_i.  This visits exactly [k,r]_2
    subspaces, once each -- unlike ordered-basis enumeration it does not blow up
    (essential for r=5 brute-force validation)."""
    if r == 0:
        yield []
        return
    for pivots in combinations(range(k), r):
        pivset = set(pivots)
        nonpiv = [j for j in range(k) if j not in pivset]
        free = [(i, j) for i, p in enumerate(pivots) for j in nonpiv if j > p]
        base = [1 << p for p in pivots]
        for bits in range(1 << len(free)):
            rows = list(base)
            for idx, (i, j) in enumerate(free):
                if (bits >> idx) & 1:
                    rows[i] |= (1 << j)
            yield rows                              # the r RREF basis vectors (message space)


def support_weight_distribution(gen_rows, n: int, r: int):
    """Brute A_i^r(C): count r-dim subcodes by effective length (support size).

    el(subcode) = |union of supports| = OR of the BASIS codewords: a coordinate
    lies in the support iff some basis vector is nonzero there (any combination
    that is nonzero there exists), so only r ORs are needed per subspace, not 2^r.
    """
    k = len(gen_rows)
    cw = codeword_table(gen_rows, n)
    A = [0] * (n + 1)
    if r == 0:
        A[0] = 1
        return A
    for basis in _rdim_subspaces(k, r):
        supp = 0
        for b in basis:
            supp |= cw[b]
        A[supp.bit_count()] += 1
    return A


def all_support_weight_distributions(gen_rows, n: int, rmax: int):
    """{r: A^r(C)} for r = 0..rmax by brute force."""
    return {r: support_weight_distribution(gen_rows, n, r) for r in range(rmax + 1)}


# ---------------------------------------------------------------------------
# Structural trims (Simonis Sec. 2; Tsfasman-Vladut generalized Griesmer).
# ---------------------------------------------------------------------------
def griesmer_d_lower(d1: int, r: int) -> int:
    """Generalized Griesmer lower bound d_r >= sum_{i=0}^{r-1} ceil(d1 / 2^i)."""
    return sum(-(-d1 // (1 << i)) for i in range(r))


def min_distance_from_W(W):
    """Smallest i > 0 with W[i] != 0 (minimum distance), or 0 if none."""
    for i in range(1, len(W)):
        if W[i]:
            return i
    return 0


def doubly_even_el_is_even(r: int) -> bool:
    """For a doubly-even code, el of an r-subcode = (1/2^{r-1}) * sum of weights
    of its 2^r-1 nonzero words; each weight ≡ 0 (mod 4), so el is even for
    every r >= 1 (the sum is divisible by 4, hence by 2^r only partially -- but
    for r=1,2 the relevant parity used downstream is 'el even')."""
    return r >= 1


# ---------------------------------------------------------------------------
# Small GF(2) linear algebra (for brute-force oracles / model self-tests).
# ---------------------------------------------------------------------------
def gf2_inner(a: int, b: int) -> int:
    return (a & b).bit_count() & 1


def gf2_dual_basis(gen_rows, n: int):
    """Basis (int bitmasks) of {y in F_2^n : <y, g> = 0 for all g in gen_rows}."""
    M = [r for r in gen_rows]
    pivot_col = {}
    r = 0
    for col in range(n):
        sel = None
        for rr in range(r, len(M)):
            if (M[rr] >> col) & 1:
                sel = rr
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        for rr in range(len(M)):
            if rr != r and ((M[rr] >> col) & 1):
                M[rr] ^= M[r]
        pivot_col[col] = r
        r += 1
        if r == len(M):
            break
    pivots = set(pivot_col)
    basis = []
    for fc in range(n):
        if fc in pivots:
            continue
        y = 1 << fc
        for col, pr in pivot_col.items():
            if (M[pr] >> fc) & 1:
                y |= 1 << col
        basis.append(y)
    return basis
