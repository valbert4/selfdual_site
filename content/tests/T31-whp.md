# T31 - Wei-Duality Weight-Hierarchy Partition

Status: `saturates but non-vacuous`

## Public Summary

This test applies Wei duality and generalized-Hamming-weight (GHW) bounds to the
length-40 child and its dual. It has real teeth — it would kill anomalous
dual-minimum-distance rows — but every surviving row falls inside the allowed
windows.

## What It Tests

- Object: the weight hierarchy (generalized Hamming weights) of `E` and `E^⊥`.
- Input: the row `(k,a,b)` and the GHW partition windows.
- Necessary condition: the row's dual minimum distance `d_1(E^⊥)` lies in the
  admissible window.
- Output: rows with an anomalous dual minimum distance.

## Result

- Kills: `0`, but non-vacuous: the screen kills `m = 1` for every `k` and kills
  large `m`; admissible windows are narrow. All surviving rows have
  `d_1(E^⊥) ∈ {2, 4}`, inside their windows.
- Status: saturates but non-vacuous (a candidate with anomalous dual distance
  would die; none do).

## Verification

- Certificate type: exact GHW-theorem bounds (no `E`-projectivity assumed).
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T31-whp-repro.tar.gz`](/downloads/repro/T31-whp-repro.tar.gz) — a 🟡 solver-required bundle. Wei-duality windows admit every survivor (kills anomalous dual distance, none occur). Reproduce in the research repo (the bundle ships the source script and the exact command); for the proof-grade kills a one-click pure-Python verifier is the next upgrade. Checksums: [manifest.json](/downloads/repro/manifest.json).

## How To Help

Combine the GHW windows with the binary-rank incidence data (T27): both touch the
subcode structure, and a joint constraint may be sharper than either alone.
