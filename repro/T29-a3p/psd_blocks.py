#!/usr/bin/env python3
"""Anchored 3-point PSD block assembly.

This is the first PSD layer for the anchored `S_16 x S_56` 3-point program.
It uses the same pair variables `p_i` and normalized triple variables `z_j` as
`linear_gate.py` / `export_linear_gate_lp.py`.

For a fixed codeword `U` in one anchored layer, the Schrijver/A3 singleton
moment matrix has rows and columns indexed by possible second words `V,W`.
After quotienting by the stabilizer of the external anchor and the layer of
`U`, rows become anchored ordered-pair types `(U,V)`.

For pair types `p=(U,V)` and `q=(U,W)`, the compressed entry is

    sum_U sum_{V in p(U)} sum_{W in q(U)} 1_{U,V,W in Y}.

In the normalized variables this is the linear form

    [p == q] * p_p  +  (|Y_B|-2) * sum_o c_o z_o,

where `c_o` counts ordered representatives in triple orbit `o` whose `UV`
projection is `p` and `UW` projection is `q`.

These are quotient/compression PSD constraints.  They are necessary conditions
for a true anchored code and are the natural solver-facing "unblocked" PSD
blocks; further representation-theoretic block diagonalization can be added
later for speed, but is not needed to define the matrices.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from anchored_orbits import (
    LAYERS,
    PROJECTIONS,
    YB_SIZE,
    build_s3_marginal_rows,
    iter_ordered_triple_types,
    pair_type_from_state,
    pair_types,
    s3_canonical,
)

TRIPLE_SCALE = YB_SIZE - 2


LinearKey = tuple[str, int]
LinearForm = dict[LinearKey, int]


def _add_form_term(form: dict[LinearKey, int], key: LinearKey, coeff: int) -> None:
    if coeff:
        form[key] = form.get(key, 0) + int(coeff)
        if form[key] == 0:
            del form[key]


def _form_equal(a: LinearForm, b: LinearForm) -> bool:
    return {k: v for k, v in a.items() if v} == {k: v for k, v in b.items() if v}


def _sum_orbit_rows(rows: Iterable[dict[int, int]]) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for row in rows:
        for orbit_idx, coeff in row.items():
            out[orbit_idx] += int(coeff)
    return {idx: coeff for idx, coeff in out.items() if coeff}


def build_s3_pair_pair_rows():
    """Return pair-pair projection rows for singleton moment matrices.

    The returned `rows[(layer, p_idx, q_idx)]` is a sparse dict from S_3 triple
    orbit index to multiplicity.  `p_idx` is the `UV` pair type, `q_idx` is the
    `UW` pair type, so both have first layer equal to `layer`.
    """

    pairs = pair_types()
    pair_index = {pair: idx for idx, pair in enumerate(pairs)}
    orbit_index: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    orbit_reps: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    rows: dict[tuple[int, int, int], dict[int, int]] = defaultdict(lambda: defaultdict(int))

    for state in iter_ordered_triple_types():
        key = s3_canonical(state)
        orbit_idx = orbit_index.get(key)
        if orbit_idx is None:
            orbit_idx = len(orbit_reps)
            orbit_index[key] = orbit_idx
            orbit_reps.append(key)
        p = pair_type_from_state(state, "UV")
        q = pair_type_from_state(state, "UW")
        p_idx = pair_index[p]
        q_idx = pair_index[q]
        layer = p[0]
        if q[0] != layer:
            raise AssertionError("UV and UW first layers disagree")
        rows[(layer, p_idx, q_idx)][orbit_idx] += 1

    return orbit_reps, {key: dict(value) for key, value in rows.items()}


def build_quotient_psd_blocks():
    """Build exact sparse linear-form PSD blocks.

    Returns a dict with `pairs`, `triple_orbits`, and `blocks`.  Each block is:

        {
          "layer": a,
          "pair_indices": [...],
          "entries": [[{("pair",i): c, ("triple",j): d, ...}, ...], ...],
        }
    """

    pairs = pair_types()
    triple_orbits, pair_pair_rows = build_s3_pair_pair_rows()
    blocks = []
    for layer in LAYERS:
        indices = [idx for idx, pair in enumerate(pairs) if pair[0] == layer]
        entries: list[list[LinearForm]] = []
        for p_idx in indices:
            row = []
            for q_idx in indices:
                form: dict[LinearKey, int] = {}
                if p_idx == q_idx:
                    _add_form_term(form, ("pair", p_idx), 1)
                for orbit_idx, coeff in pair_pair_rows.get((layer, p_idx, q_idx), {}).items():
                    _add_form_term(form, ("triple", orbit_idx), TRIPLE_SCALE * int(coeff))
                row.append(form)
            entries.append(row)
        blocks.append({"layer": layer, "pair_indices": indices, "entries": entries})
    return {
        "pair_types": pairs,
        "triple_orbits": triple_orbits,
        "triple_scale": TRIPLE_SCALE,
        "blocks": blocks,
    }


def validate_blocks(system) -> dict[str, object]:
    """Run structural validations independent of any LP/SDP solution."""

    pairs = system["pair_types"]
    blocks = system["blocks"]
    failures: list[object] = []

    # Symmetry of each quotient moment matrix.
    for block in blocks:
        entries = block["entries"]
        m = len(entries)
        for i in range(m):
            for j in range(i):
                if not _form_equal(entries[i][j], entries[j][i]):
                    failures.append(("asymmetry", block["layer"], i, j))

    # Pair-pair row sums must recover the already-validated UV marginal rows.
    # This confirms that the new pair-pair rows refine the old triple-to-pair
    # bookkeeping rather than changing it.
    _, marginal_rows = build_s3_marginal_rows()
    _, pair_pair_rows = build_s3_pair_pair_rows()
    by_first_layer = {
        layer: [idx for idx, pair in enumerate(pairs) if pair[0] == layer]
        for layer in LAYERS
    }
    for p_idx, pair in enumerate(pairs):
        layer = pair[0]
        summed = _sum_orbit_rows(
            pair_pair_rows.get((layer, p_idx, q_idx), {}) for q_idx in by_first_layer[layer]
        )
        expected = marginal_rows.get(("UV", p_idx), {})
        if summed != expected:
            failures.append(("row_sum_marginal", p_idx, pair, len(summed), len(expected)))

    block_summaries = []
    for block in blocks:
        entries = block["entries"]
        nonzero_entries = 0
        form_terms = 0
        max_abs_coeff = 0
        for row in entries:
            for form in row:
                if form:
                    nonzero_entries += 1
                    form_terms += len(form)
                    if form:
                        max_abs_coeff = max(max_abs_coeff, max(abs(v) for v in form.values()))
        block_summaries.append(
            {
                "layer": block["layer"],
                "size": len(entries),
                "nonzero_entries": nonzero_entries,
                "form_terms": form_terms,
                "max_abs_coeff": max_abs_coeff,
            }
        )

    return {
        "ok": not failures,
        "failures": failures[:20],
        "failure_count": len(failures),
        "blocks": block_summaries,
    }


VAR_RE = re.compile(r"\b(?:dummy|p_\d+|z_\d+)\b")


def variable_order_from_lp(path: Path) -> list[str]:
    """Return GLPK's first-appearance variable order for our CPLEX LP export."""

    seen: set[str] = set()
    order: list[str] = []
    with path.open() as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped or stripped.startswith("\\"):
                continue
            if stripped in {"Minimize", "Subject To", "Bounds", "End"}:
                continue
            for name in VAR_RE.findall(line):
                if name not in seen:
                    seen.add(name)
                    order.append(name)
    return order


def parse_glpk_solution(path: Path, pair_count: int, triple_count: int, lp_path: Path | None = None):
    """Parse GLPK `-w` basic solution into `(p_values, z_values)` floats.

    GLPK numbers columns by first appearance in the LP, not by numeric suffix.
    Pass the LP path to recover the exact name order.  Without it, the function
    falls back to the exporter order and should only be used for quick smoke
    tests on solvers known to preserve that order.
    """

    total = 1 + pair_count + triple_count
    if lp_path is not None:
        names = variable_order_from_lp(lp_path)
        if len(names) != total:
            raise ValueError(f"LP variable count mismatch: saw {len(names)}, expected {total}")
    else:
        names = ["dummy"] + [f"p_{i}" for i in range(pair_count)] + [f"z_{i}" for i in range(triple_count)]

    named_values = {name: 0.0 for name in names}
    with path.open() as fh:
        for line in fh:
            if not line.startswith("j "):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            col = int(parts[1])
            if 1 <= col <= len(names):
                named_values[names[col - 1]] = float(parts[3])

    p_values = [named_values.get(f"p_{i}", 0.0) for i in range(pair_count)]
    z_values = [named_values.get(f"z_{i}", 0.0) for i in range(triple_count)]
    return p_values, z_values


def evaluate_blocks(system, solution_path: Path, lp_path: Path | None = None) -> dict[str, object]:
    """Evaluate PSD blocks on a GLPK linear-gate solution.

    This is a diagnostic only: a random linear feasible point need not satisfy
    the PSD blocks.  Negative eigenvalues here demonstrate that the PSD layer is
    genuinely stronger than the linear gate.
    """

    import numpy as np

    pair_count = len(system["pair_types"])
    triple_count = len(system["triple_orbits"])
    p_values, z_values = parse_glpk_solution(solution_path, pair_count, triple_count, lp_path=lp_path)
    summaries = []
    for block in system["blocks"]:
        m = len(block["entries"])
        mat = np.zeros((m, m), dtype=float)
        for i, row in enumerate(block["entries"]):
            for j, form in enumerate(row):
                val = 0.0
                for key, coeff in form.items():
                    kind, idx = key
                    if kind == "pair":
                        val += coeff * p_values[idx]
                    elif kind == "triple":
                        val += coeff * z_values[idx]
                    else:
                        raise ValueError(f"unknown key kind {kind!r}")
                mat[i, j] = val
        mat = 0.5 * (mat + mat.T)
        eig = np.linalg.eigvalsh(mat)
        diag = np.diag(mat)
        summaries.append(
            {
                "layer": block["layer"],
                "size": m,
                "min_eigenvalue": float(eig[0]),
                "max_eigenvalue": float(eig[-1]),
                "negative_eigenvalues_lt_minus_1e-6": int((eig < -1e-6).sum()),
                "trace": float(np.trace(mat)),
                "min_diagonal": float(diag.min()) if len(diag) else None,
                "max_diagonal": float(diag.max()) if len(diag) else None,
            }
        )
    return {"solution": str(solution_path), "lp": None if lp_path is None else str(lp_path), "blocks": summaries}


def compact_json_summary(system, validation, evaluation=None) -> dict[str, object]:
    return {
        "description": "Anchored singleton quotient PSD block assembly.",
        "anchored_word_count_excluding_anchor": YB_SIZE,
        "triple_scale": TRIPLE_SCALE,
        "pair_types": len(system["pair_types"]),
        "triple_orbits": len(system["triple_orbits"]),
        "blocks": validation["blocks"],
        "validation": {
            "ok": validation["ok"],
            "failure_count": validation["failure_count"],
            "failures": validation["failures"],
        },
        "evaluation": evaluation,
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        type=Path,
        default=here / "psd_blocks_summary.json",
        help="where to write the summary JSON",
    )
    parser.add_argument(
        "--solution",
        type=Path,
        default=None,
        help="optional GLPK .sol file from export_linear_gate_lp.py to evaluate",
    )
    parser.add_argument(
        "--lp",
        type=Path,
        default=None,
        help="LP file used to generate --solution; needed because GLPK reorders columns",
    )
    args = parser.parse_args()

    print("Anchored singleton quotient PSD blocks")
    print("  building pair-pair triple projections ...")
    system = build_quotient_psd_blocks()
    print("  pair types     :", len(system["pair_types"]))
    print("  triple orbits  :", len(system["triple_orbits"]))
    print("  triple scale   :", system["triple_scale"])
    validation = validate_blocks(system)
    print("  validation ok  :", validation["ok"])
    for block in validation["blocks"]:
        print(
            "  block layer {layer}: size={size}, nonzero_entries={nonzero_entries}, "
            "terms={form_terms}, max|coeff|={max_abs_coeff}".format(**block)
        )

    evaluation = None
    if args.solution is not None:
        print("  evaluating solution:", args.solution)
        if args.lp is not None:
            print("  solution LP order :", args.lp)
        evaluation = evaluate_blocks(system, args.solution, lp_path=args.lp)
        for block in evaluation["blocks"]:
            print(
                "    layer {layer}: min_eig={min_eigenvalue:.6e}, "
                "neg={negative_eigenvalues_lt_minus_1e-6}, trace={trace:.6e}".format(**block)
            )

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(compact_json_summary(system, validation, evaluation), indent=2, sort_keys=True) + "\n")
    print("  wrote          :", args.json)


if __name__ == "__main__":
    main()
