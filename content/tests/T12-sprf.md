# T12 - Weight-16 Shortening Profiles

Status: `saturates`

## Summary

This test enumerates all weight-16 shortening profiles attached to a menu row and
checks them for consistency. The profiles are a useful invariant but bind no
current row.

## What It Tests

- Object: the multiset of shortening profiles obtained by deleting the support of
  each weight-16 word.
- Input: the row `(k,a,b)` and the allowed profile types.
- Necessary condition: a consistent assignment of shortening profiles exists.
- Output: rows with no consistent profile assignment (none, here).

## Result

- Kills: `0`.
- Status: saturates.

## Verification

- Certificate type: exact profile-consistency feasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T12-sprf-repro.tar.gz`](/downloads/repro/T12-sprf-repro.tar.gz) — a 🟡 solver-required bundle. Weight-16 shortening profiles consistent for every row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Tie the shortening profiles to the forced intersection data of T13 to see whether
the profile multiset becomes binding for a surviving row.
