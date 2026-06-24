# T02 - Parent-Image Divisibility

Status: `proof-grade kills`

## Summary

Each length-40 row must sit inside the forced `[56,21]` residual as the image of
a 16-coordinate projection, with fibers of the right size. This test rejects rows
whose required parent image or fiber sizes cannot exist.

## What It Tests

- Object: the 16-coordinate parent image `J` of a row inside the `[56,21]` residual.
- Input: the row `(k,a,b)` and the dimension/fiber arithmetic of the projection.
- Necessary condition: `dim J = 21 - k` and every `J`-word is even, so
  `J ⊆ [16,15]` and `dim J <= 15` (forcing `k >= 6`); each fiber holds exactly
  `2^k` words, so the marginals must be `2^k` times a valid `[16,21-k]` image
  enumerator.
- Output: rows with an impossible image or fiber structure.

## Result

- Kills: `32` — all `k <= 5` rows (31, by the pure dimension bound) plus
  `(11,615,816)` (fiber-divisibility).
- Status: proof-grade. The `k <= 5` kills use only `dim J <= 15` and import no
  image-enumerator assumptions.

## Verification

- Certificate type: exact dimension bound + integer fiber-size divisibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T02-pimg-repro.tar.gz`](/downloads/repro/T02-pimg-repro.tar.gz) — a 🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no solver**) to reproduce: 31 k<=5 rows killed by dim J = 21-k <= 15. Checksums in [manifest.json](/downloads/repro/manifest.json); run every test's bundle with `python3 verify_all.py`.

## How To Help

Confirm the dimension bound `dim J = 21 - k <= 15` independently, and check the
single fiber-divisibility kill `(11,615,816)` against the `[16,10]` image count.
