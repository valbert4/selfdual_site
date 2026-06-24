# T05 - Three-Block Nonnegativity

Status: `proof-grade kills`

## Summary

Anchor two disjoint weight-16 words and study the induced `16|16|40` split. Some
menu rows force a negative count somewhere in that split, which no real code can
have.

## What It Tests

- Object: the three-block `16|16|40` split of the length-72 code at two disjoint
  anchors.
- Input: the row `(k,a,b)`, the forced length-72 enumerator, and design moments.
- Necessary condition: every count in the exact three-block partition-MacWilliams
  system is nonnegative.
- Output: rows that force a negative block count.

## Result

- Kills: `7` — high-`a` rows at `k=10` (`a = 311..407`).
- Status: proof-grade. The counts are nonnegative integers in any genuine code,
  so infeasibility of the exact-rational system is a true elimination.

## Verification

  `three_block_macwilliams` engine).
- Certificate type: exact-rational (`QQ` / PPL) nonnegativity infeasibility.
- Reproduce: download the reproduction bundle below and run it.

## Reproduction bundle

[Download `T05-3bnn-repro.tar.gz`](/downloads/repro/T05-3bnn-repro.tar.gz) — a 🟢 exact-replayable bundle. Run `sh run.sh` (pure Python standard library, **no solver**) to reproduce: all 7 high-a k=10 rows killed by exact three-block nonnegativity (Farkas-certified). The Farkas certificate was generated once by the solver (`reproduce/`); the verifier only checks it. Checksums: [manifest.json](/downloads/repro/manifest.json); run all with `python3 verify_all.py`.

## How To Help

Replay the seven kills from the exact-rational system and produce a compact
per-row nonnegativity certificate suitable for an independent checker.
