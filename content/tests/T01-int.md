# T01 - Integer and Self-Orthogonal Validity

Status: `defines raw menu`

## Summary

This test generates the length-40 menu. It enumerates every weight enumerator a
doubly-even self-orthogonal `[40,k,>=16]` code containing the all-ones word could
have, and keeps the ones that pass the basic arithmetic. Its output is the
universe of "shadows" every later test works on.

## What It Tests

- Object: a hypothetical length-40 residual child `E`.
- Input: the constrained enumerator `W_E(y; a,b) = 1 + a(y^16 + y^24) + b y^20 + y^40`.
- Necessary condition: `|E| = 2 + 2a + b` is a power of two; the length-40
  MacWilliams dual is nonnegative and integral; `E` is self-orthogonal
  (`A_w <= B_w`).
- Output: the complete list of valid `(k,a,b)`.

## Result

- Kills: `0` (this test defines the menu rather than pruning it).
- Status: produces exactly `132` raw candidates, `k = 1..11`, distribution
  `{1,2,4,8,16,32,25,19,16,8,1}`. Exhaustive over the full self-orthogonal range
  (`k <= 20`); nothing valid exists outside the 132.

## Verification

- Certificate type: exact integer enumeration (power-of-two size, exact
  MacWilliams transform, self-orthogonality).
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T01-int-repro.tar.gz`](/downloads/repro/T01-int-repro.tar.gz) — a 🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no solver**) to reproduce: re-enumerates exactly 132 candidates. Checksums in [manifest.json](/downloads/repro/manifest.json); run every test's bundle with `python3 verify_all.py`.

## How To Help

Provide an independent re-enumeration (different language or method) that
reproduces exactly the same 132 `(k,a,b)` and confirms none are missed.
