# T04 - Image-Code Classification

Status: `saturates`

## Summary

This test pins down the 16-coordinate image code `J` attached to a length-40
child and checks consistency. It is useful bookkeeping but eliminates no
additional rows at the current menu level.

## What It Tests

- Object: the image code `J = ρ(D)` of the `[56,21]` residual on 16 coordinates.
- Input: the row `(k,a,b)` and the candidate `[16,21-k]` image enumerators.
- Necessary condition: a valid `J` of the required dimension exists and is
  consistent with the split engine.
- Output: rows with no consistent image code (none, here).

## Result

- Kills: `0`.
- Status: saturates. The split engine consumes only the forced `[56,21]`
  enumerator, never the image enumerator, so this layer is consistent for every
  surviving row.

## Verification

- Certificate type: exact image-enumerator consistency check.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T04-imgc-repro.tar.gz`](/downloads/repro/T04-imgc-repro.tar.gz) — a 🟡 solver-required bundle. A consistent 16-coordinate image code exists for every row. Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Classify the actual image codes `J` per `k` and check whether any forced
image structure (beyond the enumerator) contradicts a surviving row.
