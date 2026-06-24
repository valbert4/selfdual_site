# T11 - Local 16/24 Split Table

Status: `saturates`

## Summary

This test builds the local `16|24` split table around a minimum word and checks
that the counts are realizable. Every row that reaches it is consistent.

## What It Tests

- Object: the local `16|24` split table of the residual at one weight-16 word.
- Input: the row `(k,a,b)` and the split-table equations.
- Necessary condition: a nonnegative integer split table exists.
- Output: rows with no realizable local split table (none, here).

## Result

- Kills: `0`.
- Status: saturates.

## Verification

- Certificate type: exact-rational / integer feasibility of the split table.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T11-lspl-repro.tar.gz`](/downloads/repro/T11-lspl-repro.tar.gz) — a 🟡 solver-required bundle. Local 16|24 split table realizable for every row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Combine the local split table with a second weight-16 word to reach the
three-block setting (T05), where the same data does cut.
