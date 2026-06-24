# T27 - Binary-Rank Incidence Constraints

Status: `saturates`

## Public Summary

This test studies the binary rank spanned by the minimum words of a length-40
child and the incidence structure they force. It yields useful per-row rank
windows but eliminates no current row.

## What It Tests

- Object: the binary rank and incidence structure of the weight-16 words of `E`.
- Input: the row `(k,a,b)` and rank/incidence bounds (notably for `k = 9, 10`).
- Necessary condition: a consistent incidence configuration of the required rank
  exists.
- Output: rows with no consistent configuration (none, here).

## Result

- Kills: `0`.
- Status: saturates. The rank windows are real constraints but do not close on
  any surviving row.

## Verification

- Certificate type: exact rank / incidence feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T27-brk-repro.tar.gz`](/downloads/repro/T27-brk-repro.tar.gz) — a 🟡 solver-required bundle. Binary-rank incidence windows bind no row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Couple the rank windows to the genus-3 triweight support (which lives on
linearly-independent triples) to see whether rank and triweight jointly bind.
