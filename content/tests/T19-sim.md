# T19 - Simonis Support-Weight Feasibility

Status: `proof-grade kill`

## Summary

This test uses generalized (Simonis) support-weight identities, which couple the
support distributions of order-`r` subcodes of `E` to those of its dual. One row
fails the order-4 system.

## What It Tests

- Object: the order-`r` support-weight distributions of `E` and `E^⊥`,
  `r = 2..7`.
- Input: the row `(k,a,b)` and the coupled support-weight identities.
- Necessary condition: a nonnegative solution to the coupled order-`r` system
  exists for every `r`.
- Output: rows infeasible at some order.

## Result

- Kills: `1` — `(6,1,60)`, infeasible at order `r = 4` (its dual would need no
  4-dimensional subcode of effective length 2 or 3). Orders `r = 2, 3` saturate.
- Status: proof-grade (exact Farkas certificate at `r = 4`).

## Verification

- Certificate type: exact-rational Farkas certificate of the order-4 system.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T19-sim-repro.tar.gz`](/downloads/repro/T19-sim-repro.tar.gz) — a 🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no solver**) to reproduce: (6,1,60) proven infeasible at order 4, Farkas-certified. The Farkas certificate was generated once by the solver (`reproduce/`); the verifier only checks it. Checksums: [manifest.json](/downloads/repro/manifest.json); run all with `python3 verify_all.py`.

## How To Help

Confirm the order-4 Farkas certificate for `(6,1,60)` independently, and check
whether any other low-`a` row fails at order 5–7.
