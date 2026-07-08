#!/usr/bin/env python3
"""assemble_moment_matrix.py -- T29 anchored 3-point SDP: exact moment-matrix assembly.

Answers the one reproducibility question the public T29 bundle used to leave open:

    "How do the pair_type keys in triweight_pin.json map to the entries of the
     symmetric moment matrix M(x)?"

This is ground truth, and it is cheap: pure Python + the standard library. There
is no solver, no cluster, and no license involved -- the "cluster/licensed" tier
of T29 refers only to the interior-point SDP *solve* (MOSEK) at the margin, never
to this assembly.  Everything here is the project's own MIT-licensed code:
`anchored_orbits.py` and `psd_blocks.py` are shipped verbatim in this bundle.

--------------------------------------------------------------------------------
The map, in one paragraph
--------------------------------------------------------------------------------
The anchored moment matrix is BLOCK DIAGONAL with one block per anchor layer

    a = |U cap B|  in  {0, 2, 4, 6, 8}.

Block `a` is indexed by exactly the anchored ordered pair types whose first
coordinate equals `a`, listed in increasing *global* pair-type index order
(the order of `anchored_orbits.pair_types()`, which is `sorted(...)`).  For row
`i` and column `j` of block `a`, the exact entry is the linear form

    M_a[i, j]  =  [i == j] * p_{P(i)}  +  (|Y_B| - 2) * sum_o  c^a_{ij,o} * z_o ,

where
  * P(i) is the global pair index of row i (so p_{P(i)} is the pair variable
    whose triweight_pin.json key is pair_type = pairs[P(i)]),
  * z_o are the S_3 triple-orbit variables,
  * c^a_{ij,o} counts ordered triple representatives in orbit o whose UV
    projection is the pair of row i and whose UW projection is the pair of
    column j, and
  * |Y_B| - 2 = 249846  (TRIPLE_SCALE; |Y_B| is the number of weight-16 words
    other than the anchor).

Consequently the triweight_pin.json key `pair_type = tau` appears at exactly one
place in M: on the DIAGONAL of block `tau[0]`, at

    row = col = (position of tau's global index within block tau[0]).

That single (block, row) coordinate per pair_type is what this script emits, as
`t29_moment_matrix_map.json`.

--------------------------------------------------------------------------------
Gotcha: the `col` field of triweight_pin.json is NOT a moment-matrix index
--------------------------------------------------------------------------------
Each triweight_pin.json row also carries an integer `col`.  That is the
AGL(3,2) orbit column of the genus-3 weight enumerator -- an index into the
6 x 4228 exact-V integer matrix N -- and it is used only to PIN the pair
variable to the five genus-3 freedom coordinates a_1..a_5:

    p_tau = (N0 + a_1*N1 + a_2*N2 + a_3*N3 + a_4*N4 + a_5*N5) / (64 * A16),

with A16 = 249849 and 64*A16 = 15990336 = `scale`.  It has nothing to do with
where p_tau sits in M.  (E.g. pair_index 0 = (0,0,0,0) has col=82 but sits at
block 0, row/col 0, with N=[0,64,0,0,0,0], i.e. p_(0,0,0,0) = a_1 / A16.)

The five-parameter pinning above acts on the pair (diagonal) part only.  The z
block -- every off-diagonal entry and the triple part of every diagonal entry --
is the large free block of the SDP; reducing *it* to the same five coordinates
is the separate step you do with triweight_q_constraint.json and the genus-3
exact bases.  This script places every p and z into M exactly so that reduction
lands in the right entries; it does not perform that reduction for you.

--------------------------------------------------------------------------------
Usage
--------------------------------------------------------------------------------
    python3 assemble_moment_matrix.py                 # build, certify, write map
    python3 assemble_moment_matrix.py --full          # also dump the full per-block
                                                       #   symbolic forms (large)
    python3 assemble_moment_matrix.py --pin PATH      # triweight_pin.json location
                                                       #   (default: alongside this file)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from anchored_orbits import LAYERS, YB_SIZE  # noqa: E402
from psd_blocks import build_quotient_psd_blocks, validate_blocks  # noqa: E402

TRIPLE_SCALE = YB_SIZE - 2  # 249846


def build_map(system):
    """Return (map_rows, per_block_meta) describing where each pair_type sits in M.

    map_rows: one dict per pair_type (325 of them), keyed by global pair index.
    per_block_meta: layer -> {size, pair_indices, pair_types}.
    """
    pairs = system["pair_types"]
    blocks = system["blocks"]

    # Position of each global pair index inside its block.
    pos_in_block = {}
    per_block_meta = {}
    for block in blocks:
        layer = block["layer"]
        indices = block["pair_indices"]
        per_block_meta[layer] = {
            "size": len(indices),
            "pair_indices": list(indices),
            "pair_types": [list(pairs[k]) for k in indices],
        }
        for row, gidx in enumerate(indices):
            pos_in_block[gidx] = (layer, row)

    map_rows = []
    for gidx, tau in enumerate(pairs):
        layer, row = pos_in_block[gidx]
        map_rows.append(
            {
                "pair_index": gidx,
                "pair_type": list(tau),
                "block_layer": layer,          # = tau[0]
                "row": row,                    # symmetric: appears on the diagonal
                "col": row,                    # of block `block_layer`
            }
        )
    return map_rows, per_block_meta


def certify_placement(system, map_rows):
    """Independent structural check that the emitted map is exactly the assembly.

    Verifies, directly against the assembled forms:
      1. every pair variable p_k occurs on exactly one entry of M, and it is the
         diagonal (row, row) of block map[k];
      2. that block equals pair_type[0];
      3. no off-diagonal entry, and no *other* diagonal entry, carries a `pair`
         term (i.e. the pair variables live only where the map says).
    Returns a list of failures (empty == certified).
    """
    by_index = {r["pair_index"]: r for r in map_rows}
    seen = {}
    failures = []
    for block in system["blocks"]:
        layer = block["layer"]
        entries = block["entries"]
        for i, row in enumerate(entries):
            for j, form in enumerate(row):
                for (kind, idx), coeff in form.items():
                    if kind != "pair":
                        continue
                    if i != j:
                        failures.append(("pair_off_diagonal", layer, i, j, idx))
                        continue
                    if coeff != 1:
                        failures.append(("pair_coeff_not_1", layer, i, idx, coeff))
                    if idx in seen:
                        failures.append(("pair_seen_twice", idx, seen[idx], (layer, i)))
                    seen[idx] = (layer, i)
                    want = by_index.get(idx)
                    if want is None or (want["block_layer"], want["row"]) != (layer, i):
                        failures.append(("pair_place_mismatch", idx, (layer, i),
                                         None if want is None else (want["block_layer"], want["row"])))
    # every pair index placed, and on its own layer
    for r in map_rows:
        if r["pair_index"] not in seen:
            failures.append(("pair_never_placed", r["pair_index"]))
        if r["block_layer"] != r["pair_type"][0]:
            failures.append(("block_ne_first_layer", r["pair_index"],
                             r["block_layer"], r["pair_type"][0]))
    return failures


def attach_pin(map_rows, pin_path: Path):
    """Attach the triweight_pin.json 5-parameter pinning to each pair_type.

    Adds, per map row, a `pin` field:
      in-support : {"kind": "affine", "N": [N0..N5], "enum_col": col}
                   meaning p_tau = (N0 + sum_i a_i N_i) / scale
      not-in-sup : {"kind": "zero", "reason": ...}
    Returns the pin payload's header fields (A16, den, scale) for the map meta.
    """
    pin = json.loads(pin_path.read_text())
    affine = {r["pair_index"]: r for r in pin["pin_affine"]}
    zero = {r["pair_index"]: r for r in pin["pin_zero"]}
    for r in map_rows:
        gidx = r["pair_index"]
        if gidx in affine:
            a = affine[gidx]
            r["pin"] = {"kind": "affine", "N": a["N"], "enum_col": a["col"]}
        elif gidx in zero:
            z = zero[gidx]
            r["pin"] = {"kind": "zero", "reason": z.get("reason", "not_in_support")}
        else:
            r["pin"] = {"kind": "unpinned"}
    return {"A16": pin["A16"], "den": pin["den"], "scale": pin["scale"],
            "n_pin_affine": len(pin["pin_affine"]), "n_pin_zero": len(pin["pin_zero"])}


def full_forms(system):
    """Full per-block symbolic entries: for each block, a dense list of the upper
    triangle's linear forms, each as {"p": idx or null, "z": [[orbit, count], ...]}.
    Large (hundreds of thousands of z terms); emitted only under --full."""
    pairs = system["pair_types"]
    out = []
    for block in system["blocks"]:
        layer = block["layer"]
        entries = block["entries"]
        d = len(entries)
        tri = []
        for i in range(d):
            for j in range(i, d):
                form = entries[i][j]
                p = None
                zs = []
                for (kind, idx), coeff in sorted(form.items()):
                    if kind == "pair":
                        p = idx
                    else:  # coeff is TRIPLE_SCALE * (raw count); report the raw count
                        zs.append([idx, coeff // TRIPLE_SCALE])
                tri.append({"i": i, "j": j, "p": p, "z": zs})
        out.append({"layer": layer, "size": d, "pair_indices": list(block["pair_indices"]),
                    "pair_types": [list(pairs[k]) for k in block["pair_indices"]],
                    "upper_triangle": tri})
    return out


def assemble(pin_path: Path | None = None):
    """Build the whole thing in-process and return a result dict.

    Deterministic: the returned `text`/`sha256` depend only on the (fixed) pair
    combinatorics and triweight_pin.json, so verify.py can pin the sha256.
    """
    system = build_quotient_psd_blocks()
    val = validate_blocks(system)
    map_rows, per_block_meta = build_map(system)
    fails = certify_placement(system, map_rows)

    pin_meta = None
    if pin_path is not None and Path(pin_path).exists():
        pin_meta = attach_pin(map_rows, Path(pin_path))

    payload = {
        "description": "T29 anchored 3-point SDP: map from triweight_pin.json "
                       "pair_type keys to symmetric moment-matrix (block, row, col).",
        "convention": {
            "block_diagonal_by": "anchor layer a = |U cap B| in {0,2,4,6,8}",
            "block_index_order": "increasing global pair-type index "
                                 "(anchored_orbits.pair_types(), which is sorted)",
            "entry": "M_a[i,j] = [i==j]*p_{P(i)} + (|Y_B|-2)*sum_o c^a_{ij,o} z_o",
            "pair_lives_on": "diagonal (row,row) of block pair_type[0] only",
            "triple_scale": system["triple_scale"],
            "pin_formula": "p_tau = (N0 + a_1*N1 + ... + a_5*N5) / scale, scale=64*A16",
            "col_field_warning": "triweight_pin.json 'col' is the genus-3 enumerator "
                                 "orbit column (index into exact-V N), NOT a matrix index; "
                                 "it is reported here as pin.enum_col",
        },
        "n_pair_types": len(system["pair_types"]),
        "n_triple_orbits": len(system["triple_orbits"]),
        "pin_meta": pin_meta,
        "placement_certified": not fails,
        "blocks": {str(L): per_block_meta[L] for L in LAYERS},
        "map": map_rows,
    }
    text = json.dumps(payload, indent=1, sort_keys=True) + "\n"
    sha = hashlib.sha256(text.encode()).hexdigest()
    return {
        "system": system, "validation": val, "map_rows": map_rows,
        "per_block_meta": per_block_meta, "placement_failures": fails,
        "pin_meta": pin_meta, "payload": payload, "text": text, "sha256": sha,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pin", type=Path, default=HERE / "triweight_pin.json",
                    help="triweight_pin.json (default: alongside this script)")
    ap.add_argument("--out", type=Path, default=HERE / "t29_moment_matrix_map.json")
    ap.add_argument("--full", action="store_true",
                    help="also write t29_moment_matrix_forms.json (the entire M; large)")
    args = ap.parse_args()

    print("T29 anchored 3-point SDP -- exact moment-matrix assembly")
    print("  building quotient PSD blocks (pure Python; no solver, no license) ...")
    res = assemble(args.pin)
    system = res["system"]
    val = res["validation"]
    per_block_meta = res["per_block_meta"]
    map_rows = res["map_rows"]
    fails = res["placement_failures"]
    n_pairs = len(system["pair_types"])
    n_orbits = len(system["triple_orbits"])
    print(f"  pair types (matrix rows total): {n_pairs}")
    print(f"  triple orbits (z variables)   : {n_orbits}")
    print(f"  triple scale (|Y_B|-2)        : {system['triple_scale']}")
    print(f"  psd_blocks.validate_blocks ok : {val['ok']} "
          f"(failures: {val['failure_count']})")
    print("  block sizes (layer: size)     : "
          + ", ".join(f"{L}:{per_block_meta[L]['size']}" for L in LAYERS))
    print(f"  placement certification       : "
          f"{'OK (every p_k is exactly one diagonal, on its own layer)' if not fails else fails[:5]}")
    if res["pin_meta"] is not None:
        n_aff = sum(1 for r in map_rows if r["pin"]["kind"] == "affine")
        n_zero = sum(1 for r in map_rows if r["pin"]["kind"] == "zero")
        print(f"  pinned from triweight_pin.json: {n_aff} affine + {n_zero} zero "
              f"(scale = 64*A16 = {res['pin_meta']['scale']})")
    else:
        print(f"  triweight_pin.json not found at {args.pin} -- map emitted without pinning")

    text, sha = res["text"], res["sha256"]
    args.out.write_text(text)
    print(f"  wrote {args.out.name}  ({len(text)/1e3:.1f} KB)  sha256={sha}")

    # A worked example, printed so run.sh output is self-explanatory.
    r0 = next(r for r in map_rows if r["pair_index"] == 0)
    print("  worked example: pair_type (0,0,0,0) -> "
          f"block {r0['block_layer']}, row/col {r0['row']}; "
          f"pin N={r0.get('pin',{}).get('N')} "
          f"(=> p = N1*a_1/scale = a_1/A16); enum_col={r0.get('pin',{}).get('enum_col')}")

    if args.full:
        forms = full_forms(system)
        fp = HERE / "t29_moment_matrix_forms.json"
        ftext = json.dumps({"triple_scale": system["triple_scale"], "blocks": forms}) + "\n"
        fp.write_text(ftext)
        print(f"  wrote {fp.name}  ({len(ftext)/1e6:.1f} MB)  -- full symbolic M(p,z)")

    print("SUMMARY: "
          f"pairs={n_pairs} orbits={n_orbits} blocks={[per_block_meta[L]['size'] for L in LAYERS]} "
          f"validate_ok={val['ok']} placement_certified={not fails} map_sha256={sha}")


if __name__ == "__main__":
    main()
