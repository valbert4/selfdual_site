# T32 - Route-3A Direct Existence Exhaust

Status: `active; one proof-grade empty row`

## Public Summary

This test moves beyond algebraic screens and directly tries to build (or
completely exhaust) the actual length-40 codes for each menu row. A witness makes
a row permanently nonempty; a complete zero-leaf exhaust proves a row empty.

## What It Tests

- Object: the actual `[40,k,16]` codes realizing a menu row.
- Input: the row `(k,a,b)` and the route-3A enumeration engine (per
  `Σ ℓ² = sq` stratum).
- Necessary condition: at least one code realizing the row exists.
- Output: `✔️` nonempty (witness found), `❌` empty (complete exhaust, zero
  leaves), or `⏳` unresolved (not yet exhausted).

## Result

- Kills: `1` — `(6,29,4)` is proven empty by a complete exhaust (301,872 states,
  0 codes). This is the first proof-grade kill of a row that survived every
  algebraic screen.
- Status: active. Of the 72 surviving rows, `51` are witnessed nonempty and `21`
  are unresolved (no witness yet, but **not** evidence of emptiness — witnessed
  rows behave identically under the unseeded probe).

## Verification

- Certificate type: exhaustive enumeration (a zero-leaf exhaust is a proof of
  emptiness; a witness is a constructive proof of nonemptiness).
- Reproduce: download the reproduction bundle below and run it.
  count cap quickly, empty rows complete with zero leaves.

## Reproduction bundle

[Download `T32-exists-repro.tar.gz`](/downloads/repro/T32-exists-repro.tar.gz) — a
🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no
solver**) to re-certify all **1528** route-3A witnesses from scratch (expand each
stored `l`-vector to its `2^k` codewords and check the [40,k,16] properties) —
the *nonempty* side of T32. Checksums:
[manifest.json](/downloads/repro/manifest.json). (The *empty* proof for
`(6,29,4)` is the separate cluster-scale exhaustion.)

## How To Help

Package the `(6,29,4)` exhaust for independent replay, and run full exhausts on
the 21 unresolved rows (smallest-`m` first) to convert each `⏳` into `✔️` or `❌`.
