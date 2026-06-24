# Splitting computation: how much of the genus-3 freedom is Θ-visible?

**Question (CFT.md #6/#7 reachability).** The V_play analysis leaves a
**5-dimensional** freedom in the genus-3 enumerator of the putative [72,36,16]
code. Constraints #6 (separating-degeneration / factorization) and #7
(Fourier–Jacobi boundary) both factor through the CFT partition function
`Z = Θ(W)` — the genus-3 theta map. Because `Θ` has a non-trivial kernel at genus 3
(`ker Θ = ⟨j_8⟩`, Runge; `j_8` degree 16), any freedom direction lying in `ker Θ`
is **invisible** to #6/#7. So: of the 5 freedoms, how many are Θ-visible?

## Result (rigorous, triple-prime verified)

| | dimension |
|---|---|
| genus-3 freedom (V_play) | 5 |
| **Θ-visible** (reachable by factorization #6 + Fourier–Jacobi #7) | **1** |
| **ker Θ = ⟨j_8⟩** (invisible to #6/#7; only code-side levers can pin) | **4** |

The Θ-image of the whole freedom space is **1-dimensional**, spanned by `Θ(F_1)`
(`F_1` = the V pivot orbit `j=82`, the ordered disjoint-weight-16-triple count).
The exact relations (CRT over two primes, then rational reconstruction — tiny
denominators 17/34 confirm correctness) are

```
Θ(F_2) = (921/34) · Θ(F_1)
Θ(F_3) = (42/17)  · Θ(F_1)
Θ(F_4) = (32/17)  · Θ(F_1)
Θ(F_5) = (128/17) · Θ(F_1)
```

equivalently the four explicit **kernel generators** (each `= j_8 · g`, `g ∈ R_3[56]`):

```
34·F_2 − 921·F_1 ,   17·F_3 − 42·F_1 ,   17·F_4 − 32·F_1 ,   17·F_5 − 128·F_1   ∈ ker Θ.
```

These four divisibilities are now backed by a symbolic quotient certificate:
`symbolic_quotient_certificate.json.gz` stores sparse degree-56 quotients for the
primitive generator `J = j_8 / 1344`, with exact identities

```
34·F_2 − 921·F_1 = J · Q_2,
17·F_3 − 42·F_1  = J · Q_3,
17·F_4 − 32·F_1  = J · Q_4,
17·F_5 − 128·F_1 = J · Q_5.
```

All four divisions have zero symbolic remainder over `ZZ`.

## Implication

**Factorization (#6) and Fourier–Jacobi (#7) can cut at most 1 of the 5 freedom
dimensions.** The other **4 dimensions live in the j_8-kernel** and are provably
invisible to any constraint that factors through the partition function `Z=Θ(W)`
— two enumerators differing by an element of `⟨j_8⟩` have identical `Z`. Those 4
can only be pinned by **code-side** levers (positivity, 5-design integrality, the
anchored Terwilliger SDP §19), never by the CFT-degeneration constraints.

This sharply re-prioritises the remaining program: building the #6/#7 machinery
has a hard ceiling of one dimension; the bulk of the freedom is a code-side / SDP
problem. (It is consistent with V_play's own conclusion that no *linear* Siegel
constraint reduces the rational dimension.)

## Method (why it is exact)

`Θ` is a **ring homomorphism** with `Θ(j_8)=0`, so for `F ∈ R_3`:

```
Θ(F) = 0   ⟺   j_8 | F   ⟺   F vanishes on the hypersurface {j_8 = 0}.
```

So `rank` over `GF(p)` of `[ F_i(x_j) ]` at points `x_j ∈ {j_8=0}` equals the
Θ-visible dimension. Points are built exactly: fix random `(x_1..x_7)`, solve the
univariate `j_8(x_0)=0 mod p` (degree ≤16). No theta evaluation, no precision, no
degree-56 basis. **`j_8` is squarefree** (∇`j_8` ≠ 0 at 200/200 generic points of
`{j_8=0}`), so the point test equals `ker Θ` exactly (not merely the radical).

**Validation chain.**
- orbit machinery (exact): `R_0(1,…,1)=2^108=|C|^3`, `F_i(1,…,1)=0`;
- `j_8` is a genuine ker Θ element: self-equation-invariant, AGL-invariant,
  vanishing genus-1 and genus-2 marginals; numerically `j_8(T(Ω))/scale ~ 1e-22`
  at well-conditioned theta points;
- rank consistent across primes `2899999957`, `2899999931`;
- the four exact integer kernel combos verified to vanish on `{j_8=0}` at a
  **third** prime `2899999903` (unused in reconstruction), while `F_1` does not.
- symbolic division over `ZZ` by the primitive generator `J = j_8/1344` gives
  explicit degree-56 quotients and zero remainders for all four kernel combos.

## Files

- `theta_split.py` — direct genus-3 theta evaluation over ℂ (validation +
  cross-check; float64 is precision-limited on the degree-72 dynamic range, so it
  is *not* the system of record — it confirmed `j_8` vanishing and `Θ(F_1)≠0`).
- `exact_split.py` — the exact GF(p) computation on `{j_8=0}` (**system of
  record**); writes `exact_split_verdict.json`.
- `symbolic_quotient.py` — exact multivariate division over `ZZ` for the four
  kernel generators; writes the symbolic quotient certificate.
- `symbolic_quotient_certificate.json.gz` — packed sparse quotients proving the
  four identities above.  Exponents are encoded in base 73.
- `symbolic_quotient_summary.json` — small readable summary of the certificate:
  quotient term counts, coefficient sizes, and hashes.
- `_j8_deg16.json` — the exact degree-16 kernel generator `j_8 = e8² − d16⁺`
  (471 terms), built from `dnplus.dnplus_genus3`.

## Repo bug found

`codes.py:d16plus()` returns a **decomposable** code (its weight-4 support graph
splits 8+8) — i.e. e8⊕e8 in disguise, *not* the indecomposable d16⁺. Its docstring's
"Verified by validate_code / NOT e8⊕e8" is wrong (validate_code only checks
[16,8,4]+Type II). The genuine d16⁺ genus-3 enumerator comes from the Fujii–Oura
closed form `dnplus.dnplus_genus3(16)`; with it, `e8²−d16⁺ = j_8 ≠ 0` (471 terms),
as required. Using the buggy `d16plus()` gives `j_8 = 0` and would silently break
any ker Θ computation.
