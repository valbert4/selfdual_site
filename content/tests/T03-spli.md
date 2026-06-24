# T03 - Full Split Integrality

Status: `saturates`

## Public Summary

This test asks whether the first recursive split system around a minimum word has
an integer solution compatible with a menu row. It is a real constraint, but
every row reaching it has enough freedom to satisfy it.

## What It Tests

- Object: the partition-MacWilliams split system of the `[56,21]` residual around
  one weight-16 word.
- Input: the row `(k,a,b)` and the exact split-row equations.
- Necessary condition: the split counts admit a nonnegative integer solution.
- Output: rows with no integral split solution (none, here).

## Result

- Kills: `0`.
- Status: saturates. Tested as an exact MILP / exact-rational feasibility
  problem; all surviving rows pass.

## Verification

- Certificate type: exact integer / PPL feasibility (no floating point).
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T03-spli-repro.tar.gz`](/downloads/repro/T03-spli-repro.tar.gz) — a 🟡 solver-required bundle. First split system is integer-feasible for every surviving row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Look for a strengthening of the split system (extra exact equalities) that turns
this saturated feasibility into a binding obstruction for some surviving row.
