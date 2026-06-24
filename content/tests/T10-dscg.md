# T10 - Discriminant-Form and Coset-Weight Gluing

Status: `saturates`

## Summary

For a length-40 child to extend upward into the `[56,21]` residual, its
discriminant form and coset-weight data must match. This test checks that
necessary gluing condition; all current rows pass.

## What It Tests

- Object: the gluing of `E` to the residual through the quotient (discriminant)
  group and coset-weight data.
- Input: the row `(k,a,b)`, the discriminant form, and coset-weight enumerators.
- Necessary condition: the discriminant-form / coset-weight data is consistent
  with an upward extension.
- Output: rows with incompatible gluing data (none, here).

## Result

- Kills: `0`.
- Status: saturates. The discriminant-form conditions are necessary but every
  surviving row has enough slack to satisfy them.

## Verification

- Certificate type: exact coset-weight / discriminant-form consistency.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T10-dscg-repro.tar.gz`](/downloads/repro/T10-dscg-repro.tar.gz) — a 🟡 solver-required bundle. Discriminant-form / coset-weight gluing feasible for every row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Push the gluing condition from the discriminant form to actual coset-weight
coupling (see T23) and look for a row whose coset supply cannot meet the demand.
