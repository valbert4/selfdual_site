# T15 - Fiber/Coset Multiset Match

Status: `saturates`

## Public Summary

This test asks whether the fiber and coset multisets of a length-40 child can be
matched to the forced split rows of the residual. The aggregate matching is
feasible for every row that reaches it.

## What It Tests

- Object: the multiset of projection fibers and the multiset of residual split
  rows.
- Input: the row `(k,a,b)`, the fiber sizes, and the forced split-row multiset.
- Necessary condition: a multiset matching (transportation-style) between fibers
  and split rows exists.
- Output: rows with no valid matching (none, here).

## Result

- Kills: `0`.
- Status: saturates. The aggregate matching cancels the unknown individual
  enumerators and is feasible for all surviving rows.

## Verification

- Certificate type: exact (totally-unimodular) transportation feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T15-fibm-repro.tar.gz`](/downloads/repro/T15-fibm-repro.tar.gz) — a 🟡 solver-required bundle. Fiber/coset multiset matching feasible (totally unimodular). Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Replace the aggregate matching with the individual (per-coset) coupling and look
for a row where disaggregation removes the slack.
