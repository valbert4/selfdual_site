# T08 - Johnson/Delsarte Two-Point Bound

Status: `proof-grade kill`

## Summary

The weight-16 words of a length-40 child form a constant-weight code in the
Johnson scheme. This test applies the exact two-point Delsarte bound to that
constant-weight code; one row needs more weight-16 words than the bound allows.

## What It Tests

- Object: the weight-16 words of `E` as a constant-weight `(40,16)` code.
- Input: the row's required count `a` and the allowed pairwise intersections.
- Necessary condition: `a` is at most the exact Delsarte/Johnson bound for the
  allowed intersection set.
- Output: rows exceeding the bound.

## Result

- Kills: `1` — `(9,255,0)`. With intersections forced to `{4,8}` the exact
  Delsarte bound is `247`, but the row requires `255`.
- Status: proof-grade (exact-rational LP bound).

## Verification

- Certificate type: exact-rational Delsarte LP bound + dual certificate.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T08-john-repro.tar.gz`](/downloads/repro/T08-john-repro.tar.gz) — a
🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no
solver**) to recompute the exact Delsarte bound `247` and confirm the
`(9,255,0)` kill. Checksums in
[manifest.json](/downloads/repro/manifest.json); run every test's bundle with
`python3 verify_all.py`.

## How To Help

Reproduce the exact LP optimum `247` with an independent solver and provide the
dual certificate proving `a <= 247 < 255`.
