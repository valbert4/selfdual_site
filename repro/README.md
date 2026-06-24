# Reproduction bundles

Each test page links a small archive that re-derives that test's published result
from public data — so a reader can *check the proof*, not just trust the script.

## Standard (per test)

```
T??-name/
  run.sh           # entrypoint; exits 0 iff the published result is reproduced
  verify.py        # the verifier (pure Python where possible, no licensed solver)
  expected.json    # tier + claim + the value(s) to reproduce
  README.md        # what it proves, how to run, inputs
  inputs/          # the published enumerator data it consumes (pinned by sha256)
  reproduce/       # OPTIONAL original solver (may need PPL/Sage/MOSEK/C++)
```

The **verifier** is the part that must run everywhere; the original **solver**
(which *found* the certificate) ships only as optional `reproduce/`.

## Tiers

| Tier | Meaning | CI |
|---|---|---|
| 🟢 `exact-replayable` | pure Python stdlib, exact arithmetic, no solver | every commit |
| 🟡 `solver-required` | needs an exact solver (PPL / Sage / `glpsol --exact`) | nightly, extended image |
| 🔴 `cluster/licensed` | not one-click — anchored SDP (MOSEK), full exhaustion | ship payload + spec only |

## Running

    python3 verify_all.py                 # 🟢 bundles (the public guarantee)
    python3 verify_all.py --all           # attempt every tier

`verify_all.py` runs each `run.sh` and reports PASS/FAIL — the harness that
"makes sure the scripts all run".

## Reusing the published enumerator data

Verifiers consume the same JSON the **Enumerators** tab serves, pinned by sha256,
so "reproduces" means *recomputes `expected.json` from data whose checksum matches
what the site publishes*. This wires Verification ↔ Enumerators and prevents drift.

## Pilot status (this batch)

- 🟢 **T08** — exact Delsarte bound `247` via pure-Python vertex enumeration; kills `(9,255,0)`.
- 🟢 **T32** — re-certifies 1528 route-3A witnesses (the nonempty side) from scratch.
- **T06** — integer Smith-form solvability verifier (pure Python); certificate
  generated once by the Sage three-block script.

The remaining 29 tests follow the same template; T29 (anchored SDP) and the
`(6,29,4)` empty-exhaust are the 🔴 exceptions that ship a spec, not a one-click run.
