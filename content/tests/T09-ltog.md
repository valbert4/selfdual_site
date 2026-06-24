# T09 - Local Toggle-Stabilizer Divisibility

Status: `saturates`

## Public Summary

This test applies the toggle-stabilizer divisibility constraints locally, inside
a single `16|24` split around one minimum word. The constraints are valid but
bind no current row.

## What It Tests

- Object: the `16|24` split of the residual around one weight-16 word.
- Input: the row `(k,a,b)` and the local divisibility congruences.
- Necessary condition: the local split counts satisfy the toggle-stabilizer
  congruences.
- Output: rows failing the local congruences (none, here).

## Result

- Kills: `0`.
- Status: saturates. The two-anchor version of this idea (T06) does cut; the
  single-anchor local version does not.

## Verification

- Certificate type: exact integer congruence feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T09-ltog-repro.tar.gz`](/downloads/repro/T09-ltog-repro.tar.gz) — a 🟡 solver-required bundle. Local toggle-stabilizer congruences bind no row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Identify whether a second anchor or an extra coset coordinate makes the local
congruences bind on any surviving row (the bridge from T09 to T06).
