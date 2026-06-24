#!/usr/bin/env python3
"""
verify_all.py -- run every test reproduction bundle and report PASS/FAIL.

This is the CI entrypoint that "makes sure the scripts all run". Each bundle is a
directory `T??-*/` containing a `run.sh` that exits 0 iff that test's published
result is reproduced exactly, and an `expected.json` describing it (tier, claim).

Tiers:
  exact-replayable  -- pure Python, no solver; runs in base CI on every commit
  solver-required   -- needs an exact solver (PPL / Sage / glpsol); extended CI
  cluster/licensed  -- not one-click (e.g. anchored SDP, full exhaustion); skipped

Usage:
  python3 verify_all.py                 # run exact-replayable bundles (default)
  python3 verify_all.py --all           # attempt every tier
  python3 verify_all.py --tier solver-required
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TIERS = {"exact-replayable"}


def bundles():
    out = []
    for d in sorted(os.listdir(HERE)):
        p = os.path.join(HERE, d)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "run.sh")):
            exp = {}
            ep = os.path.join(p, "expected.json")
            if os.path.exists(ep):
                exp = json.load(open(ep))
            out.append((d, p, exp))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="attempt every tier")
    ap.add_argument("--tier", action="append", default=[], help="run only these tiers")
    args = ap.parse_args()
    tiers = set(args.tier) if args.tier else (None if args.all else DEFAULT_TIERS)

    ran, passed, skipped = [], 0, []
    for name, path, exp in bundles():
        tier = exp.get("tier", "exact-replayable")
        if tiers is not None and tier not in tiers:
            skipped.append((name, tier))
            continue
        print(f"=== {name}  [{tier}] ===")
        r = subprocess.run(["sh", "run.sh"], cwd=path, capture_output=True, text=True)
        ok = r.returncode == 0
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print(f"    {'PASS' if ok else 'FAIL'}  (exit {r.returncode})  {tail}")
        if not ok:
            sys.stderr.write(r.stderr[-2000:] + "\n")
        ran.append((name, ok, tier))
        passed += int(ok)

    print()
    for name, tier in skipped:
        print(f"SKIP {name}  [{tier}]")
    print(f"\n{passed}/{len(ran)} bundles reproduced"
          + (f"; {len(skipped)} skipped" if skipped else "") + ".")
    sys.exit(0 if ran and passed == len(ran) else 1)


if __name__ == "__main__":
    main()
