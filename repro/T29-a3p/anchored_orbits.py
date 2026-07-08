#!/usr/bin/env python3
"""Orbit bookkeeping for the anchored 3-point SDP.

The anchor support has size 16 and its complement has size 56.  A word is
represented by its intersection layer with the anchor, and a triple orbit under
S_16 x S_56 is represented by two 8-region Venn compositions, one on each side
of the split.

Mask convention for a composition c[0..7]:

    bit 0 -> U, bit 1 -> V, bit 2 -> W.

Thus c[3] is U V W^c, c[5] is U W V^c, c[6] is V W U^c, and c[7] is U V W.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations

ANCHOR_SIZE = 16
RESIDUAL_SIZE = 56
WORD_WEIGHT = 16
LAYERS = (0, 2, 4, 6, 8)
ALLOWED_INTERSECTIONS = (0, 2, 4, 6, 8)
LAYER_COUNTS = {
    0: 5082,
    2: 84480,
    4: 123480,
    6: 34496,
    8: 2310,
}
YB_SIZE = sum(LAYER_COUNTS.values())
PROJECTIONS = ("UV", "UW", "VW")
S3_PERMS = tuple(permutations(range(3)))


def row_weight(comp: tuple[int, ...], bit: int) -> int:
    mask = 1 << bit
    return sum(value for idx, value in enumerate(comp) if idx & mask)


def pair_intersection(comp: tuple[int, ...], bit_a: int, bit_b: int) -> int:
    mask = (1 << bit_a) | (1 << bit_b)
    return sum(value for idx, value in enumerate(comp) if (idx & mask) == mask)


def triple_row_weights(comp: tuple[int, ...]) -> tuple[int, int, int]:
    return (row_weight(comp, 0), row_weight(comp, 1), row_weight(comp, 2))


def triple_pair_intersections(comp: tuple[int, ...]) -> tuple[int, int, int]:
    return (
        pair_intersection(comp, 0, 1),
        pair_intersection(comp, 0, 2),
        pair_intersection(comp, 1, 2),
    )


@lru_cache(maxsize=None)
def part_types_by_pair(
    part_size: int,
    row_weights: tuple[int, int, int],
) -> dict[tuple[int, int, int], tuple[tuple[int, ...], ...]]:
    """Return Venn compositions grouped by their three pair intersections."""
    w_u, w_v, w_w = row_weights
    grouped: dict[tuple[int, int, int], list[tuple[int, ...]]] = defaultdict(list)

    for c111 in range(min(w_u, w_v, w_w) + 1):
        for c110 in range(min(w_u, w_v) - c111 + 1):
            for c101 in range(min(w_u, w_w) - c111 + 1):
                c100 = w_u - c111 - c110 - c101
                if c100 < 0:
                    continue
                for c011 in range(min(w_v, w_w) - c111 + 1):
                    c010 = w_v - c111 - c110 - c011
                    c001 = w_w - c111 - c101 - c011
                    if c010 < 0 or c001 < 0:
                        continue
                    union = c100 + c010 + c001 + c110 + c101 + c011 + c111
                    c000 = part_size - union
                    if c000 < 0:
                        continue
                    comp = (c000, c100, c010, c110, c001, c101, c011, c111)
                    grouped[triple_pair_intersections(comp)].append(comp)

    return {key: tuple(value) for key, value in grouped.items()}


def valid_pair_type(a: int, b: int, q_anchor: int, q_residual: int) -> bool:
    if a not in LAYERS or b not in LAYERS:
        return False
    if q_anchor + q_residual not in ALLOWED_INTERSECTIONS:
        return False
    if not max(0, a + b - ANCHOR_SIZE) <= q_anchor <= min(a, b):
        return False
    ra = WORD_WEIGHT - a
    rb = WORD_WEIGHT - b
    if not max(0, ra + rb - RESIDUAL_SIZE) <= q_residual <= min(ra, rb):
        return False
    return True


def pair_types() -> list[tuple[int, int, int, int]]:
    out = []
    for a in LAYERS:
        for b in LAYERS:
            for q_anchor in range(max(0, a + b - ANCHOR_SIZE), min(a, b) + 1):
                for total in ALLOWED_INTERSECTIONS:
                    q_residual = total - q_anchor
                    if valid_pair_type(a, b, q_anchor, q_residual):
                        out.append((a, b, q_anchor, q_residual))
    return sorted(out)


def swap_pair_type(pair: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, q_anchor, q_residual = pair
    return (b, a, q_anchor, q_residual)


def pair_s2_orbit_count(pairs: list[tuple[int, int, int, int]] | None = None) -> int:
    pairs = pair_types() if pairs is None else pairs
    return len({min(pair, swap_pair_type(pair)) for pair in pairs})


def iter_ordered_triple_types():
    """Yield ordered anchored triple orbit representatives under S_16 x S_56."""
    for a_u in LAYERS:
        for a_v in LAYERS:
            for a_w in LAYERS:
                b_groups = part_types_by_pair(ANCHOR_SIZE, (a_u, a_v, a_w))
                r_groups = part_types_by_pair(
                    RESIDUAL_SIZE,
                    (WORD_WEIGHT - a_u, WORD_WEIGHT - a_v, WORD_WEIGHT - a_w),
                )
                for b_pair, b_comps in b_groups.items():
                    for uv in ALLOWED_INTERSECTIONS:
                        r_uv = uv - b_pair[0]
                        if r_uv < 0:
                            continue
                        for uw in ALLOWED_INTERSECTIONS:
                            r_uw = uw - b_pair[1]
                            if r_uw < 0:
                                continue
                            for vw in ALLOWED_INTERSECTIONS:
                                r_vw = vw - b_pair[2]
                                if r_vw < 0:
                                    continue
                                r_comps = r_groups.get((r_uv, r_uw, r_vw))
                                if not r_comps:
                                    continue
                                for b_comp in b_comps:
                                    for r_comp in r_comps:
                                        yield (b_comp, r_comp)


def permute_comp(comp: tuple[int, ...], perm: tuple[int, int, int]) -> tuple[int, ...]:
    out = [0] * 8
    for old_mask, value in enumerate(comp):
        new_mask = 0
        for new_bit, old_bit in enumerate(perm):
            if old_mask & (1 << old_bit):
                new_mask |= 1 << new_bit
        out[new_mask] = value
    return tuple(out)


def permute_state(
    state: tuple[tuple[int, ...], tuple[int, ...]],
    perm: tuple[int, int, int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    b_comp, r_comp = state
    return (permute_comp(b_comp, perm), permute_comp(r_comp, perm))


def s3_canonical(
    state: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(permute_state(state, perm) for perm in S3_PERMS)


def projection_bits(projection: str) -> tuple[int, int]:
    if projection == "UV":
        return (0, 1)
    if projection == "UW":
        return (0, 2)
    if projection == "VW":
        return (1, 2)
    raise ValueError(f"unknown projection {projection!r}")


def pair_type_from_state(
    state: tuple[tuple[int, ...], tuple[int, ...]],
    projection: str,
) -> tuple[int, int, int, int]:
    b_comp, r_comp = state
    bit_a, bit_b = projection_bits(projection)
    return (
        row_weight(b_comp, bit_a),
        row_weight(b_comp, bit_b),
        pair_intersection(b_comp, bit_a, bit_b),
        pair_intersection(r_comp, bit_a, bit_b),
    )


def orbit_summary() -> dict[str, object]:
    pairs = pair_types()
    ordered_triples = 0
    s3_sizes: Counter[int] = Counter()
    s3_seen: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}

    for state in iter_ordered_triple_types():
        ordered_triples += 1
        key = s3_canonical(state)
        s3_seen[key] = s3_seen.get(key, 0) + 1

    s3_sizes.update(s3_seen.values())
    return {
        "anchor_size": ANCHOR_SIZE,
        "residual_size": RESIDUAL_SIZE,
        "word_weight": WORD_WEIGHT,
        "layers": list(LAYERS),
        "allowed_intersections": list(ALLOWED_INTERSECTIONS),
        "layer_counts": dict(LAYER_COUNTS),
        "anchored_word_count_excluding_anchor": YB_SIZE,
        "ordered_pair_types": len(pairs),
        "s2_pair_orbits": pair_s2_orbit_count(pairs),
        "ordered_triple_types": ordered_triples,
        "s3_triple_orbits": len(s3_seen),
        "s3_orbit_size_counts": {str(key): value for key, value in sorted(s3_sizes.items())},
    }


def build_s3_marginal_rows():
    """Build sparse triple-to-pair marginal rows for the linear gate.

    Returns `(orbit_reps, rows)`, where `rows[(projection, pair_index)]` is a
    sparse dict mapping an S_3 triple orbit index to its coefficient.
    """
    pairs = pair_types()
    pair_index = {pair: idx for idx, pair in enumerate(pairs)}
    orbit_index: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    orbit_reps: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    rows: dict[tuple[str, int], dict[int, int]] = defaultdict(lambda: defaultdict(int))

    for state in iter_ordered_triple_types():
        key = s3_canonical(state)
        idx = orbit_index.get(key)
        if idx is None:
            idx = len(orbit_reps)
            orbit_index[key] = idx
            orbit_reps.append(key)
        for projection in PROJECTIONS:
            pair = pair_type_from_state(state, projection)
            rows[(projection, pair_index[pair])][idx] += 1

    return orbit_reps, {key: dict(value) for key, value in rows.items()}
