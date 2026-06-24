# Theta-visibility splitting of the 5-dim triweight freedom

`splitting_computation.py` — exact char-p computation (two V_play large primes).

## Question

The two remaining unexploited CFT.md constraints — **#6 separating factorization**
and **#7 Fourier–Jacobi boundary membership** — both factor through the genus-3
**partition function** `Z = Theta(W)`.  The theta map `Theta : R_3 -> M_3` is
surjective with kernel the principal ideal `<j_8>` (Runge; HKM: `M_3 = R_3/<j_8>`,
`j_8` degree-16 = weight-8).  Any freedom direction lying in `ker Theta` is
**invisible** to #6/#7 — two enumerators differing by a multiple of `j_8` have the
same `Z`.  So the maximum dimension cut #6+#7 can ever deliver is
`rank(Theta | span(F_1..F_5))`; the rest can only be pinned **code-side**
(positivity / 5-design integrality / anchored SDP).

## Method (exact, large prime)

`ker Theta` is cut out by the single hypersurface `{j_8 = 0}` (Runge: `j_8` is the
ONLY relation among the 8 genus-3 theta constants).  Evaluate each exact freedom
`F_i` (from `exact_V.json.gz`, the char-0 6-prime result) at random `GF(p)`-points
**on** `{j_8 = 0}`:

- `F_i in ker Theta`  =>  `F_i = j_8 * g`  =>  `F_i(x) = 0` at every such point;
- `F_i not in ker`    =>  `F_i(x) != 0` generically.

`visible_dim = rank_GF(p)[ F_i(x_j) ]`,  `kernel_dim = 5 - visible_dim`.
Points are produced by intersecting random lines with the degree-16 hypersurface
and Cantor–Zassenhaus root-finding over `GF(p)`.  Small primes are avoided (they
inflate ranks here); run at `p = 2899999957` and `2899999931`.

`j_8 = enum3(e8(+)e8) - enum3(d16+)`, validated to vanish at genus 1 AND genus 2
(=> in `ker Theta`) and to be nonzero at genus 3.

## Result (both primes agree)

```
visible_dim (rank of Theta on the 5 freedoms)  =  1
kernel_dim  (invisible to #6 / #7)             =  4
rank[F_1..F_5, R_0] = 2     (R_0 genuine row is Theta-visible at all points)
```

Equivalently, of the **6-dim** exact triweight space `V = <R_0, F_1..F_5>`:
- `dim Theta(V) = 2` (the genuine `R_0` + exactly **one** freedom combination);
- `dim (V ∩ ker Theta) = 4`, lying entirely inside the freedom space.

## Consequence

**#6 (factorization) + #7 (Fourier–Jacobi) can pin at most 1 of the 5 freedom
directions.**  The other **4** are pure `j_8`-kernel: identical partition function,
so no CFT degeneration/boundary constraint can ever see them.  Those 4 are
reachable ONLY by code-side levers (positivity, 5-design integrality, anchored
3-point Terwilliger SDP).  This sharply scopes the payoff of building the
genus-2-Jacobi-membership / per-node-factorization machinery: it is a single
linear form on the freedoms, not a multi-dimensional cut.

(The one visible freedom combination — the only one #6/#7 could constrain — is the
row space of the 5×K evaluation matrix; it can be rational-reconstructed from the
two primes if/when that constraint is built.)

## Side finding (repo bug)

`codes.d16plus()` is **not** the indecomposable d16+: its RM(1,4)-based greedy
construction yields a code whose weight-4 graph splits 8+8, i.e. it is equivalent
to `e8(+)e8` (so `enum3` agrees and the difference vanishes).  The genuine
indecomposable d16+ used here is hardcoded as `_D16PLUS_A` in
`splitting_computation.py` (Type II [16,8,4], weight-4 graph = single 16-vertex
component, genus-3 enumerator differs from `e8(+)e8` in 471 monomials).  Worth
fixing `codes.d16plus()` upstream.
