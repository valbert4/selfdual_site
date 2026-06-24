# T13 - Double-Shortening Forced-Intersection Screen

Status: `proof-grade kill`

## Summary

Shorten on the union of the supports of two weight-16 words and ask which
pairwise intersections remain possible. For one row the intersections are forced
into a single value, and then there is no room for the required number of words.

## What It Tests

- Object: the four-block split on `supp(U) ∪ supp(V)` for a weight-16 pair with
  intersection `t`.
- Input: the row `(k,a,b)` and the per-`t` four-block split tables.
- Necessary condition: some intersection `t` survives whose Johnson bound admits
  the required count `a`.
- Output: rows whose only surviving `t` cannot supply `a` words.

## Result

- Kills: `1` — `(9,247,16)`. The four-block system forces intersections to `{8}`;
  the Johnson bound there is `7657/67 ≈ 114`, far below the required `247`.
- Status: proof-grade.

## Verification

- Certificate type: exact four-block infeasibility (for `t ∈ {4,6}`) plus exact
  Johnson bound on the surviving `t = 8`.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T13-dshr-repro.tar.gz`](/downloads/repro/T13-dshr-repro.tar.gz) — a 🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no solver**) to reproduce: bound 7657/67 < 247 kills (9,247,16). Checksums in [manifest.json](/downloads/repro/manifest.json); run every test's bundle with `python3 verify_all.py`.

## How To Help

Confirm the `t = 4, 6` infeasibility and the `7657/67` Johnson bound
independently, and produce a single combined certificate for the kill.
