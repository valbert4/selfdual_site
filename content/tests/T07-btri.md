# T07 - Fixed Three-Anchor Baby-Triweight

Status: `saturates`

## Public Summary

This test refines the two-anchor picture with a small three-anchor (baby
triweight) calculation on the length-72 structure. It is a useful consistency
check but does not bind any surviving row.

## What It Tests

- Object: the genus-3 "baby triweight" slice at three fixed weight-16 anchors.
- Input: the row `(k,a,b)` and the four-block triple-count system.
- Necessary condition: the triple counts admit a nonnegative solution consistent
  with the lower-genus marginals.
- Output: rows with an infeasible baby-triweight slice (none, here).

## Result

- Kills: `0`.
- Status: saturates. It confirms the rigid length-24 bottom column but adds no
  binding obstruction at the current menu level.

## Verification

- Certificate type: exact-rational feasibility of the triple-count system.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T07-btri-repro.tar.gz`](/downloads/repro/T07-btri-repro.tar.gz) — a 🟡 solver-required bundle. Baby-triweight slice feasible at the current menu. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Extend the fixed-anchor slice toward a full triple (joint) enumeration and check
whether the joint constraints bind where the per-pair slice saturates.
