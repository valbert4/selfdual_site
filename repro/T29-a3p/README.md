# T29-a3p reproduction bundle — anchored 3-point moment-matrix assembly

**Tier:** 🟢 exact-replayable (pure Python standard library; no solver, no license)

**What this bundle reproduces:** the exact assembly of the anchored 3-point SDP
moment matrix, and the map from the `pair_type` keys in `triweight_pin.json` to
the entries of that symmetric matrix.

> The final PSD-margin verdict for T29 (kill vs. saturation at the boundary) is
> **still open** — that is the licensed/high-precision SDP *solve*, not this. What
> was previously missing from the public bundle, and is now here, is the
> **construction**: how the pinned pair variables land in `M`.

Run it:

```sh
sh run.sh        # ~30–60 s; enumerates the 109684 S₃ triple orbits, exit 0 on match
```

## The map, exactly

The anchored moment matrix is **block diagonal**, one block per anchor layer

```
a = |U ∩ B|  ∈  {0, 2, 4, 6, 8}          (B is the fixed weight-16 anchor)
```

Block `a` is indexed by exactly the anchored ordered pair types whose **first
coordinate equals `a`**, listed in increasing global pair-type index order
(the order of `anchored_orbits.pair_types()`, which is `sorted(...)`). The block
sizes are

```
layer 0: 25   layer 2: 57   layer 4: 75   layer 6: 83   layer 8: 85   (Σ = 325)
```

For row `i`, column `j` of block `a`, the exact entry is the linear form

```
M_a[i,j] = [i == j] · p_{P(i)}  +  (|Y_B| − 2) · Σ_o  c^a_{ij,o} · z_o
```

where `P(i)` is the global pair index of row `i`, `p_·` are the anchored pair
variables (the `triweight_pin.json` keys), `z_o` are the S₃ triple-orbit
variables, `c^a_{ij,o}` counts ordered triple representatives in orbit `o` whose
`UV` projection is the pair of row `i` and `UW` projection is the pair of column
`j`, and `|Y_B| − 2 = 249846` (`TRIPLE_SCALE`; `|Y_B|` is the number of weight-16
words other than the anchor).

**Therefore** the `triweight_pin.json` key `pair_type = τ` appears at exactly one
place in `M`: on the **diagonal of block `τ[0]`**, at

```
row = col = (position of τ's global index within block τ[0]).
```

That single `(block, row)` coordinate for every one of the 325 pair types is
emitted, together with the pinning, as **`t29_moment_matrix_map.json`**.

## The gotcha: `col` in `triweight_pin.json` is *not* a matrix index

Each `triweight_pin.json` row carries an integer `col`. That is the **AGL(3,2)
orbit column of the genus-3 weight enumerator** — an index into the `6 × 4228`
exact-V integer matrix `N` — and it is used only to *pin* the pair variable to the
five genus-3 freedom coordinates `a₁…a₅`:

```
p_τ = ( N0 + a₁·N1 + a₂·N2 + a₃·N3 + a₄·N4 + a₅·N5 ) / (64 · A16),
      A16 = 249849,   64·A16 = 15990336 = "scale".
```

It says nothing about where `p_τ` sits in `M`. Concretely:

```
pair_type (0,0,0,0):  col = 82   (enumerator orbit column)
                      → block 0, row/col 0   (moment-matrix position)
                      N = [0, 64, 0, 0, 0, 0]  ⇒  p_(0,0,0,0) = a₁ / A16
```

In `t29_moment_matrix_map.json` the enumerator column is reported as
`pin.enum_col` precisely so it is never confused with `row`/`col`.

## Where the 5 parameters do and do not act

The five-parameter pinning above acts on the **pair (diagonal) part only**. The
`z` block — every off-diagonal entry, and the triple part of every diagonal
entry — is the large *free* block of the SDP (109684 orbit variables). Reducing
*that* to the same five coordinates is the **separate** step you already rebuilt
with `triweight_q_constraint.json` and the genus-3 exact bases. This bundle places
every `p` and `z` into `M` exactly, so your reduction lands in the right entries;
it does **not** perform that reduction, and `M` is *not* a 5-parameter matrix until
you do (it is affine in `(p, z)`, with `p` pinned to `a₁…a₅` and `z` free here).

## Files

| file | what it is |
|------|-----------|
| `anchored_orbits.py`        | orbit bookkeeping (S₁₆×S₅₆ pair/triple types). MIT, project code, verbatim. |
| `psd_blocks.py`             | the assembly: `build_quotient_psd_blocks()` builds the 5 blocks; `validate_blocks()` checks symmetry + the marginal row-sum identity. MIT, project code, verbatim. |
| `assemble_moment_matrix.py` | driver: builds the map, attaches the pin, certifies placement, writes `t29_moment_matrix_map.json`. `--full` also dumps the entire symbolic `M(p,z)` (≈4 MB). |
| `verify.py` / `run.sh`      | one-click check (rebuilds and compares to the published sha256). |
| `triweight_pin.json`        | the public pinning payload (identical math to `/downloads/enumerators/triweight_pin.json`; cluster paths scrubbed). |
| `t29_moment_matrix_map.json`| precomputed output: the 325-entry `pair_type → (block,row,col)` map + pin. |
| `expected.json`             | the claim + expected `map_sha256`. |

## Getting the whole matrix symbolically

```sh
python3 assemble_moment_matrix.py --full   # writes t29_moment_matrix_forms.json
```

`t29_moment_matrix_forms.json` gives, per block, the upper triangle of `M` as
`{i, j, p, z:[[orbit, count], …]}`, i.e. every `p` and `z` term of every entry
(the `count` is `c^a_{ij,o}`; multiply by `triple_scale = 249846`). Substitute
your pinned `p_τ(a)` on the diagonals and your `z`-reduction to obtain
`M(a₁,…,a₅)` and take the PSD margin.

## License

Code (`*.py`) is MIT; data/prose are CC-BY-4.0. See the repository `LICENSE`.
This is the project's own code — none of the assembly is licensed third-party
software; the "cluster/licensed" label on T29 refers only to the MOSEK *solve*.
