# T14 - Coset Minimum and Congruence Prefilter

Status: `saturates`

## Public Summary

This test applies minimum-weight and congruence constraints to the cosets used in
the `40 -> 56` upward direction. It is a fast prefilter; all current rows pass.

## What It Tests

- Object: the cosets of `E` in `E^⊥` used to build the `[56,21]` residual.
- Input: the row `(k,a,b)` and per-coset minimum-weight / congruence bounds.
- Necessary condition: enough cosets of the right minimum weight and congruence
  class exist to supply the upward gluing.
- Output: rows with insufficient coset supply (none, here).

## Result

- Kills: `0`.
- Status: saturates. The current rows all have ample coset supply.

## Verification

- Certificate type: exact per-coset minimum-weight / congruence feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T14-cmin-repro.tar.gz`](/downloads/repro/T14-cmin-repro.tar.gz) — a 🟡 solver-required bundle. Coset minimum / congruence prefilter binds no row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Tighten the prefilter with exact per-coset packing caps (see T22) and test
whether the combined supply bound binds anywhere.
