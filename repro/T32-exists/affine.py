"""affine.py -- shared definitions for the route-3A shape classifier (SCOPE §2F).

A *shape code* of length n, dimension k, target set T is a binary [n,k] code E with
1_n in E, all nonzero codeword weights in T u {n} (=> doubly-even / self-orthogonal /
d >= min(T) when T is a doubly-even window with 0,n excluded).  Fixing g_1 = 1_n makes
every generator column lie in the affine hyperplane {x_1 = 1}, identified with
F_2^m (m = k-1) via the low m bits.  A shape code is then a multiplicity vector

    l : F_2^m -> Z>=0 ,   sum_y l[y] = n ,

with functional sums  V[u'] = sum_{y : <u',y> = 1} l[y]  in T  for every u' != 0
(u' ranges over the nonzero functionals).  Equivalence is AGL(m,2) on F_2^m.

This module is the single source of truth for the parameters, the incidence /
Walsh structure, the l <-> code conversion, the pruning constants, and the
(a,b)-bucket map.  The C++ kernel emits the same constants from here (gen_consts).

Production target:  n=40, T={16,20,24}, k in {6,7,8,9,10}.
The code is fully parameterised in (n,k,T) so the same engine runs the n=8/16/24
validation ladder.
"""

from __future__ import annotations
import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    n: int                      # length
    k: int                      # dimension
    T: tuple                    # allowed nontrivial weights (sorted), e.g. (16,20,24)

    @property
    def m(self) -> int:
        return self.k - 1

    @property
    def npts(self) -> int:
        return 1 << self.m      # |F_2^m| = number of affine points / columns alphabet

    @property
    def nfunc(self) -> int:
        return self.npts - 1    # nonzero functionals u'

    @property
    def Dmax(self) -> int:
        """max |n - 2v| over v in T -- the extreme Walsh deviation (moment cap)."""
        return max(abs(self.n - 2 * v) for v in self.T)

    @property
    def sqcap(self) -> int:
        """Parseval upper bound on sum_y l[y]^2 for the *general* run (all a).

        sum l^2 = (n^2 + sum_{u'!=0} (n-2V[u'])^2) / 2^m,  each term <= Dmax^2.
        """
        return (self.n * self.n + self.nfunc * self.Dmax * self.Dmax) // self.npts

    def validate(self):
        assert self.k >= 2, "k>=2"
        assert self.n % 4 == 0, "n divisible by 4 (doubly-even ambient)"
        assert all(t % 4 == 0 for t in self.T), "T doubly-even"
        assert all(0 < t < self.n for t in self.T), "T strictly between 0 and n"
        assert tuple(sorted(self.T)) == self.T, "T sorted"
        # need n reachable by npts points and the all-ones present
        assert self.npts >= 2
        return self


# Canonical menu parameters (n=40 production) and the small-n validation ladder.
MENU = {kk: Params(40, kk, (16, 20, 24)) for kk in range(6, 11)}
LADDER = {
    ("n8", 4):  Params(8, 4, (4,)),            # e8 = RM(1,3): unique
    ("n16", 4): Params(16, 4, (4, 8, 12)),     # all d>=4 doubly-even, 1 in E
    ("n16", 5): Params(16, 5, (4, 8, 12)),
    ("n16d8", 5): Params(16, 5, (8,)),         # d>=8: RM(1,4) territory
    ("n24", 4): Params(24, 4, (4, 8, 12, 16, 20)),
    ("n24d8", 5): Params(24, 5, (8, 12, 16)),
}


# --------------------------------------------------------------------------- #
#  Incidence / Walsh structure                                                #
# --------------------------------------------------------------------------- #
def parity(x: int) -> int:
    return bin(x).count("1") & 1


def incidence(P: Params):
    """inc[y] = bitmask over functionals u' in 1..npts-1 with <u',y>=1.

    Bit (u'-1) of inc[y] is set iff parity(u' & y) == 1.  Used so a mass update at
    point y touches a fixed mask of functionals.  Also returns, per point y, the
    list form for clarity / the C++ emitter.
    """
    npts = P.npts
    inc = [0] * npts
    for y in range(npts):
        mask = 0
        for up in range(1, npts):
            if parity(up & y):
                mask |= 1 << (up - 1)
        inc[y] = mask
    return inc


def functional_hits(P: Params):
    """For each functional u' (1..npts-1): list of points y with <u',y>=1.

    Used to detect 'dead' functionals (no remaining incident point) during DFS.
    """
    npts = P.npts
    hits = [[] for _ in range(npts)]      # index by u'
    for up in range(1, npts):
        for y in range(npts):
            if parity(up & y):
                hits[up].append(y)
    return hits


def functional_incidence_cols(P: Params):
    """inc_cols[y] = list of nonzero functionals u' with <u',y>=1 (incident to point y)."""
    npts = P.npts
    cols = [[] for _ in range(npts)]
    for y in range(npts):
        for up in range(1, npts):
            if parity(up & y):
                cols[y].append(up)
    return cols


def reference_frame(P: Params):
    """A fixed affine basis prefix (0, e_1, e_2) used for sound symmetry breaking.

    AGL(m,2) is 3-transitive on F_2^m (m>=2), so every orbit of l has a rep whose
    three largest multiplicities sit on a fixed affinely-independent triple; we fix
    that triple to (0, 1, 2) and require l[0] >= l[1] >= l[2] >= l[y] (y>=3).
    For m == 1 (k=2) there is no triple; frame = the 2 points, no constraint beyond
    l[0] >= l[1].
    """
    m = P.m
    if m >= 2:
        return [0, 1, 2]                  # 0, e_1, e_2  (affinely independent)
    return list(range(P.npts))


def point_order(P: Params):
    """DFS assignment order: reference frame first, then the rest ascending.

    Frame-first lets the non-increasing cap chain (l[0]>=l[1]>=l[2]>= rest) be
    enforced incrementally and soundly.
    """
    frame = reference_frame(P)
    rest = [y for y in range(P.npts) if y not in frame]
    return frame + rest


# --------------------------------------------------------------------------- #
#  l  <->  code  /  weights  /  (a,b) bucket                                   #
# --------------------------------------------------------------------------- #
def column_int(P: Params, y: int) -> int:
    """k-bit column for point y: bit 0 = the x_1=1 coordinate, bits 1..m = y."""
    return 1 | (y << 1)


def l_to_columns(P: Params, l):
    """Expand multiplicity vector l into the list of n columns (k-bit ints)."""
    cols = []
    for y, mult in enumerate(l):
        if mult:
            cols.extend([column_int(P, y)] * mult)
    assert len(cols) == P.n, (len(cols), P.n)
    return cols


def _codewords_from_cols(P: Params, cols):
    """Codeword set (r-bit ints) for a generator whose columns are `cols` (len r)."""
    words = []
    for msg in range(1 << P.k):
        w = 0
        for c, col in enumerate(cols):
            if parity(msg & col):
                w |= 1 << c
        words.append(w)
    return words


def l_to_codewords(P: Params, l):
    """All 2^k codewords (n-bit ints) of the FULL (length-n) code generated by l."""
    cols = l_to_columns(P, l)
    return _codewords_from_cols(P, cols)


def l_to_columns_partial(P: Params, l):
    """Columns (k-bit ints) of the partial code l, in point-expansion order (len sum l)."""
    cols = []
    for y, mult in enumerate(l):
        cols.extend([column_int(P, y)] * mult)
    return cols


def l_to_codewords_partial(P: Params, l):
    """Codewords of the PARTIAL code (length r = sum l <= n) for canonicalisation.

    Allows rank-deficient partials (dim < k); dreadnaut canon() dedups codewords.
    """
    cols = []
    for y, mult in enumerate(l):
        if mult:
            cols.extend([column_int(P, y)] * mult)
    return _codewords_from_cols(P, cols)


def functional_sums(P: Params, l):
    """V[u'] for u' in 0..npts-1 (V[0]=0); V[u'] = sum_{y:<u',y>=1} l[y]."""
    npts = P.npts
    V = [0] * npts
    for y, mult in enumerate(l):
        if not mult:
            continue
        for up in range(1, npts):
            if parity(up & y):
                V[up] += mult
    return V


def ab_bucket(P: Params, l):
    """(a, b) of the shape code for l, computed from functional sums.

    a = A_16-analog = #{u'!=0 : V[u'] != mid},   b = 2 * #{u'!=0 : V[u'] = mid},
    where 'mid' = n/2 is the self-paired weight (20 for n=40).  Returns None if l
    is not a valid shape code (some V[u'] not in T).
    """
    V = functional_sums(P, l)
    mid = P.n // 2
    z = 0
    for up in range(1, P.npts):
        if V[up] not in P.T:
            return None
        if V[up] == mid:
            z += 1
    a = (P.npts - 1) - z
    b = 2 * z
    return (a, b)


def is_valid_shape(P: Params, l) -> bool:
    return ab_bucket(P, l) is not None and sum(l) == P.n


def aut_closed_form(P: Params, l, stab_agl_order: int) -> int:
    """|Aut(E)| = |Stab_AGL(l)| * prod_y l[y]!  (SCOPE §2F).  Needs |Stab_AGL(l)|."""
    import math
    prod = 1
    for mult in l:
        prod *= math.factorial(mult)
    return stab_agl_order * prod


if __name__ == "__main__":
    # smoke: e8 unique l == 1 on 8 points, (a,b)=(7,0)-analog, sqcap sanity
    P = LADDER[("n8", 4)].validate()
    l = [1] * P.npts
    assert is_valid_shape(P, l), functional_sums(P, l)
    print("e8:", "valid", "V=", functional_sums(P, l)[1:], "bucket(a,b)=", ab_bucket(P, l))
    for kk in (6, 7, 8, 9, 10):
        Q = MENU[kk].validate()
        print(f"k={kk}: m={Q.m} npts={Q.npts} nfunc={Q.nfunc} Dmax={Q.Dmax} sqcap={Q.sqcap}")
    # sqcap must match the SCOPE §2H values 112/88/76 at a-max
    assert MENU[6].sqcap == 112 and MENU[7].sqcap == 88 and MENU[8].sqcap == 76
    print("affine.py OK")
