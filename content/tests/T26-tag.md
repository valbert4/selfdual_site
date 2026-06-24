# T26 - Triweight Aggregate Plus Residual Mode-1

Status: `saturates`

## Summary

This test combines genus-3 triweight aggregate constraints with residual Mode-1
gluing data. The combined aggregate model stays feasible — another sign that
progress needs sharper, non-aggregate structure.

## What It Tests

- Object: the `(16,16,·)` triweight aggregate, coupled to residual Mode-1
  tilings.
- Input: the row `(k,a,b)`, the triweight aggregate, and residual coset data.
- Necessary condition: the coupled aggregate admits the row.
- Output: rows excluded by the coupled aggregate (none, here).

## Result

- Kills: `0`.
- Status: saturates. Both the triweight freedom and the residual biweight family
  retain enough slack to absorb the coupling.

## Verification

- Certificate type: exact-rational aggregate feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T26-tag-repro.tar.gz`](/downloads/repro/T26-tag-repro.tar.gz) — a 🟡 solver-required bundle. Triweight aggregate + residual Mode-1 feasible for every row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

The averaging principle is the wall here. Build the un-averaged anchored coupling
(genus-3 Jacobi at a fixed weight-16 anchor) instead of the aggregate.
