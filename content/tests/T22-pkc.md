# T22 - Mode-1 Per-Coset Packing Caps

Status: `saturates`

## Summary

This test adds exact per-coset packing caps to the Mode-1 gluing picture,
limiting how many words each coset can supply. The caps prune the profile pool
but bind no current row.

## What It Tests

- Object: the per-coset profile pool of the upward-glue step, with packing caps.
- Input: the row `(k,a,b)` and exact per-coset capacity bounds.
- Necessary condition: a capped per-coset assignment realizing the row exists.
- Output: rows with no capped assignment (none, here).

## Result

- Kills: `0`.
- Status: saturates. The capped tiling polytopes still admit every aggregate
  mixture.

## Verification

- Certificate type: exact-rational capped feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T22-pkc-repro.tar.gz`](/downloads/repro/T22-pkc-repro.tar.gz) — a 🟡 solver-required bundle. Per-coset packing caps absorbed by aggregate freedom. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Combine the packing caps with pairwise coset coupling (T23) so the capacity
bounds interact, instead of being absorbed by the aggregate freedom.
