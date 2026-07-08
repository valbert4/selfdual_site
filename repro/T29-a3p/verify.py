#!/usr/bin/env python3
"""verify.py -- one-click check of the T29 moment-matrix assembly.

Rebuilds the anchored 3-point moment matrix from scratch (pure Python, no solver)
and asserts the published structure:

  * 5 PSD blocks, one per anchor layer, of sizes 25 / 57 / 75 / 83 / 85
    (= 325 anchored pair types total);
  * psd_blocks.validate_blocks passes (block symmetry + marginal row-sum identity);
  * every pair variable p_k sits on exactly one diagonal entry, on its own layer
    (the pair_type -> (block, row, col) placement is certified);
  * triweight_pin.json pins 291 pair types affinely + 34 to zero;
  * the emitted map (t29_moment_matrix_map.json) hashes to the published sha256.

Exit 0 iff every check passes.  This reproduces the ASSEMBLY of T29 exactly; the
final PSD margin verdict at the boundary remains open (that solve is the licensed
MOSEK step, not this).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from assemble_moment_matrix import assemble  # noqa: E402

EXPECT = {
    "n_pair_types": 325,
    "n_triple_orbits": 109684,
    "block_sizes": [25, 57, 75, 83, 85],   # layers 0,2,4,6,8
    "n_pin_affine": 291,
    "n_pin_zero": 34,
    "map_sha256": "ca655e18511c15cbe531267cbe4a144f0a7dcad5a369853e88a464ce1ba5bdcf",
}


def main() -> int:
    res = assemble(HERE / "triweight_pin.json")
    system = res["system"]
    sizes = [res["per_block_meta"][L]["size"] for L in (0, 2, 4, 6, 8)]
    n_aff = sum(1 for r in res["map_rows"] if r["pin"]["kind"] == "affine")
    n_zero = sum(1 for r in res["map_rows"] if r["pin"]["kind"] == "zero")

    checks = [
        ("pair types == 325", len(system["pair_types"]) == EXPECT["n_pair_types"]),
        ("triple orbits == 109684", len(system["triple_orbits"]) == EXPECT["n_triple_orbits"]),
        ("block sizes == 25/57/75/83/85", sizes == EXPECT["block_sizes"]),
        ("validate_blocks ok", bool(res["validation"]["ok"])),
        ("placement certified", res["placement_failures"] == []),
        ("pin affine == 291", n_aff == EXPECT["n_pin_affine"]),
        ("pin zero == 34", n_zero == EXPECT["n_pin_zero"]),
        ("map sha256 matches", res["sha256"] == EXPECT["map_sha256"]),
    ]
    ok = all(v for _, v in checks)
    for name, v in checks:
        print(f"  [{'ok' if v else 'FAIL'}] {name}")
    print(f"RESULT: T29 moment-matrix assembly reproduced "
          f"({'PASS' if ok else 'FAIL'}); map sha256={res['sha256']}")
    if ok:
        # (re)emit the map next to this script so the bundle self-heals if edited
        (HERE / "t29_moment_matrix_map.json").write_text(res["text"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
