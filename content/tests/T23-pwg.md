# T23 - Mode-1 Pairwise/Subgroup Coset Coupling

Status: `diagnostic consistency check; no public elimination`

## Public Summary

This test couples pairs (and subgroups) of cosets and checks an overcode-style
consistency condition on the upward glue. Its current value is as a consistency
layer; this page states what it would need to become an eliminator.

## What It Tests

- Object: pairs / subgroups of cosets in the upward-glue step.
- Input: the row `(k,a,b)` and the pairwise/subgroup coupling constraints.
- Necessary condition: the coupled counts are consistent with a `[40,k+2]`-valid
  overcode structure.
- Output: rows with inconsistent coupling (subject to the requirements below).

## Result

- Kills: `0` (no public elimination).
- Status: diagnostic / validation target.

## Verification

Requirements for a pairwise-coupling elimination to count publicly:

- pairwise and subgroup counts reconcile exactly with the row-level coset
  normalization;
- the coupling uses the exact subgroup structure of the image, not an
  approximation;
- any constructive witness for the row is excluded under the exact hypothesis.

- Certificate type: exact pairwise/subgroup reconciliation (required).

## Reproduction bundle

[Download `T23-pwg-repro.tar.gz`](/downloads/repro/T23-pwg-repro.tar.gz) — a 🔴 bundle. This test is open / validation-only: pairwise coupling needs exact subgroup reconciliation to count. The archive ships a spec and the source path, not a one-click run. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Lift the per-coset coupling to exact pairwise `E + ⟨y_j, y_{j'}⟩` validity using
the image subgroup, and look for a row where the coupled supply is exhausted.
