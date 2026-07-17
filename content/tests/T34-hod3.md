# T34 - Higher-Order Delsarte LP (Level 3)

Status: `saturates; screen`

## Summary

The Delsarte linear program counts codewords by Hamming weight. Recent work
(Coregliano-Jeronimo-Jones and Loyfer-Linial,
[arXiv:2501.04854](https://arxiv.org/abs/2501.04854)) strengthens it into a
*hierarchy*: at level `l`, the variables count `l`-tuples of codewords by the
weight configuration of the subspace they span. Level 1 is the ordinary Delsarte
LP; **level 2 is exactly the coupled genus-2 biweight model already run as T20**;
this test runs **level 3** - the genus-3 (triweight) feasibility LP - on each
length-40 menu row. It saturates: no unresolved row is eliminated.

## What It Tests

- Object: the genus-3 (triweight) distribution of an ordered triple of codewords
  `(u,v,w)` of the length-40 residual child `E`, recorded as counts `N_m` over
  the `2593` valid column types `m` (which fold under the symmetry group
  `AGL(3,2)` to just **26 orbit variables**).
- Input: the forced menu enumerator `(1,a,b,a,1)`, and the fact that `E` is
  doubly-even self-orthogonal with `1_40 in E`.
- Necessary condition: there exist nonnegative `N_m` with the correct genus-1
  marginals, whose genus-2 marginal satisfies the **full T20 model** (coupled in
  by substitution, so level 3 contains level 2 = T20), and whose genus-3
  **dual Fourier transform** `N'_p = 2^(-3k) sum_m N_m c_{p,m}` is nonnegative on
  the dual code `E^perp` (and zero where `E^perp`, being even, has no words).
- Output: per-row FEASIBLE / EMPTY. An EMPTY row would be a proof-grade kill.

## Result

- Kills: `0` - saturates. All **21 unresolved rows** (the `∃`-column ⏳ rows:
  `k7 a∈{53,57,59,61}`, `k8 a∈{83,91,99,103,107,111,115,119,123,127}`,
  `k9 a∈{191,199,207,215,223,231}`, `k10 a=295`) are **FEASIBLE**, and the four
  witnessed control rows are feasible as required.
- Screen, not completeness: dual Fourier positivity is imposed only over a pool
  of **sparse** dual points (the full dual space has `C(47,7) ~ 6.3·10^7`
  monomials), so a FEASIBLE verdict is *not* a proof of level-3 feasibility -
  only an EMPTY verdict would be proof-grade. The `0/21` result held identically
  at a smaller pool, so it is not an artifact of the particular pool.
- Two facts make the genus-3 dual side tractable: the dual constraint
  `a_o(p) = sum_{m in orbit o} c_{p,m}` is **`AGL(3,2)`-invariant** (one
  representative per orbit collapses hundreds of sparse points to ~19 distinct
  constraints), and a closed-form `sparse_coeff` evaluates `c_{p,m}` for a sparse
  `p` with no large dynamic program.

## Verification

- Certificate type: exact rational feasibility by **kernel reduction** - the
  equality constraints are solved over the rationals (particular solution +
  nullspace) and only the low-dimensional kernel is handed to the exact solver
  PPL. (Float LPs give false infeasibles here: coefficients reach `~10^20` with
  the T20 coupling, a documented pitfall, so the solve is exact.) The pipeline
  was validated end-to-end in two phases before the sweep: the genus-3 transform
  was checked against brute-force enumerators of real codes, and level 2 was
  shown to reproduce T20 exactly on all 47 menu rows (verdicts and exact rational
  boxes). A witness safety net confirms every real code's genus-3 enumerator
  satisfies every generated constraint.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T34-hod3-repro.tar.gz`](/downloads/repro/T34-hod3-repro.tar.gz) - a 🟢
exact-replayable bundle. `python3 run.sh` reproduces, with the Python standard
library only and no solver, the exact genus-3 transform core the level-3 model is
built on: the `2593` valid column types and their `26` `AGL(3,2)` orbits; the
genus-3 MacWilliams / Fourier identity `sum_m N_m c_{p,m} = |E|^3 N'_p`
end-to-end on the self-dual code `e8 = RM(1,3)`; the closed-form `sparse_coeff`
against the general coefficient; and the coefficient symmetry
`c_{p,m} prod(p!) = c_{m,p} prod(m!)`. The full per-row feasibility sweep
(`0` kills) is solver-required (exact PPL) and lives in the research repo
(`higher_delsarte/level3_model.py --sweep`, `--validate`). Checksums:
[manifest.json](/downloads/repro/manifest.json).

## How To Help

The screen can be sharpened without new mathematics. Run a genuine **separation
loop**: given the LP solution for a row, search sparse dual points `p` for the
most negative `N'_p`, add that Fourier-positivity cut, and repeat until the pool
stops finding violations - this is the difference between "feasible on the
current pool" and a real feasibility bound. A single row driven to EMPTY this way
would be the first proof-grade genus-3 kill. Two adjacent levers: the
Loyfer-Linial partial-Fourier level-4 slice on any row that comes close, and the
separate global `n=72` level-2 size-bound LP (a would-be T35) that could rule out
the whole code at once if its optimum falls below `2^36`.
