# T34-hod3 reproduction bundle

**Tier:** 🟢 exact-replayable (this bundle) / 🟡 solver-required (full sweep)

**Test:** T34 — higher-order Delsarte LP at level 3 (genus-3 / triweight),
following arXiv:2501.04854 (Coregliano–Jeronimo–Jones / Loyfer–Linial hierarchy).

**Result:** the level-3 LP **saturates** — 0 kills on all 21 unresolved menu
rows (k7 a∈{53,57,59,61}; k8 a∈{83,91,99,103,107,111,115,119,123,127};
k9 a∈{191,199,207,215,223,231}; k10 a=295), with the four witnessed control
rows feasible. It is a screen (dual Fourier positivity imposed over a sparse
pool), not a completeness claim; only an EMPTY verdict would be a proof-grade
kill.

## What this bundle checks (pure Python standard library, no solver)

`python3 run.sh` reproduces, exactly, the genus-3 transform machinery the
level-3 model is built on:

- **(A)** the 2593 valid genus-3 column types and their **26 AGL(3,2)-orbits**
  (the primal variable set), and |AGL(3,2)| = 1344;
- **(B)** the genus-3 MacWilliams / Fourier identity end-to-end on the self-dual
  code e8 = RM(1,3): `sum_m N_m c_{p,m} == |E|^3 N'_p` for every dual monomial;
- **(C)** the closed-form sparse-point coefficient `sparse_coeff` equals the
  general `macwilliams_coeff` (the cheap dual-cut evaluator);
- **(D)** the coefficient symmetry `c_{p,m}·prod(p!) == c_{m,p}·prod(m!)`.

## Full result (solver-required)

The complete per-row feasibility sweep — genus-3 nonnegativity + genus-1 pins +
the full T20 genus-2 coupling (by substitution) + the genus-3 dual
Fourier-positivity pool, solved by exact kernel-reduced feasibility (rational
nullspace + PPL on the kernel) — lives in the research repo:
`higher_delsarte/level3_model.py` (`--validate` for the witness safety net,
`--sweep` for the 21-row verdict). Phase 0/1 there also validate the transform
against brute codes and prove level-2 ≡ T20 (47/47 verdicts and exact boxes).
