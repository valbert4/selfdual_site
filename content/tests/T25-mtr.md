# T25 - Menu-to-Triweight Feedback LP

Status: `saturates`

## Public Summary

This test feeds menu information into the genus-3 triweight variables and asks
whether the feedback rules out any row. It does not, through this aggregate LP.

## What It Tests

- Object: the genus-3 triweight invariant space, fed by menu (min-word-triple)
  data.
- Input: the row `(k,a,b)` and the triweight feedback constraints.
- Necessary condition: the row is consistent with some point of the triweight
  space.
- Output: rows inconsistent with the triweight feedback (none, here).

## Result

- Kills: `0`.
- Status: saturates. The triweight is itself an unpinned family — the exact
  6-dimensional invariant space carries a 5-dimensional freedom, none of it
  pinned — so the aggregate feedback has slack to absorb every row.

## Verification

- Certificate type: exact-rational aggregate LP feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T25-mtr-repro.tar.gz`](/downloads/repro/T25-mtr-repro.tar.gz) — a 🟡 solver-required bundle. Menu->triweight feedback LP feasible (triweight freedom absorbs it). Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Replace the aggregate feedback with the un-averaged (per-anchor) min-word-triple
coupling, where the triweight freedom is not washed out by averaging.
