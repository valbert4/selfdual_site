# Weight Enumerators

This page should be a catalog of downloadable enumerator data, not a second
explanation of the whole search pipeline.

## Public Goal

Make the calculated enumerators available in JSON format:

- one-variable weight enumerators;
- partition and residual biweight data;
- genus-3 / triweight data, including large coefficient objects.
- genus-3 invariant-space and candidate-space artifacts.

Large triweight coefficients should stay machine-readable. The page can show a
compact summary, but the primary public artifact should be JSON.

The Simonis `menu_support_weight_r=*` and `residual_support_weight_r=*` files are
support-weight screening data. They are useful for certificates and tests, but
they should not live on the main enumerator shelf unless the site later creates
a separate "support-weight certificates" catalog.

## Headline Objects

The page can still show the most important small formulas.

```text
A_16 = 249849
```

```text
W_D(y) =
1
+ 5082 y^16
+ 91168 y^20
+ 507045 y^24
+ 890560 y^28
+ 507045 y^32
+ 91168 y^36
+ 5082 y^40
+ y^56.
```

```text
W_E(y; a,b) = 1 + a(y^16 + y^24) + b y^20 + y^40.
```

## Downloads

Each download is a self-contained bundle (every tarball carries its own
`MANIFEST.txt`); nothing points outside the archive.

- **Enumerator data** — `enumerators-json-bundle.tar.gz` (all one-weight,
  biweight and triweight JSON together), plus the individual JSON files and a
  machine-readable `enumerators-index.json` with checksums.
- **Genus-3 invariant spaces** — `genus3-invariant-space-bundle.tar.gz`: AGL/GL
  nullbases, d_n+ atoms, and the n=72 candidate-space artifacts.
- **Triweight routines** — `triweight-routines-source.tar.gz`: the reusable
  genus-3 enumerator tooling as a ready-to-run `extremal72-triweight-routines/`
  tree (sources + README, all paths relative to the bundle).

## Genus-3 Data Now Staged

- n=32 AGL/GL nullbases over p=13 and p=17, with nullity 9.
- n=40 AGL/GL nullbases over p=13 and p=17, with nullity 16, 364 AGL columns,
  and 1700 GL rows.
- n=40 converted G48-coordinate bases over p=13 and p=17.
- d_n+ closed-form genus-3 atoms at n=40 and n=48 over p=13 and p=17.
- n=72 modular candidate spaces for the [72,36,16] support over p=13, p=17,
  and four large primes.
- n=72 char-zero triweight range artifacts: `exact_V`,
  `charzero_cons_basis`, `charzero_integer`, and the 5-design residue-lattice
  extraction output (a lattice of design residues, not a Construction-A
  geometric lattice).

**What `exact_V` is, and is not.** The genus-3 triweight of the `[72,36,16]`
code is **not** uniquely determined by the current constraints. `exact_V` is the
exact 6-dimensional invariant *space* (one forced row plus a 5-dimensional
freedom), recovered and CRT-verified. None of the 5 freedom directions has been
pinned: every computable enumerator-level constraint applied so far leaves the
full freedom intact. So `exact_V` is the pinned-down *space the triweight lives
in*, not the triweight itself. Treat any single point in it as a representative,
not "the" enumerator.

Note: the n=48 data included is the d_48+ closed-form atom, not the full
31-dimensional invariant space (that artifact is not yet computed).

## Triweight Routines

The triweight routines are a separate public service. Prior literature treats
obtaining such enumerators as computationally hard, so the site should make
these routines easy to find.

The public bundle should include:

- row and column symmetrization routines;
- support-pruned transforms;
- different-prime run scripts;
- reconstruction and reconciliation scripts;
- validation scripts and known-code checks;
- short README notes explaining how to rerun or extend the computation.

The public bundle should not include bulky generated caches, private run logs,
or machine-specific scratch output unless those files are deliberately promoted
as public data.

## QR48 Triweight Target

The repo has a generator for the extended quadratic-residue `[48,24,12]` code
(a `qr48_generators()` routine), and the code is the natural
benchmark for the public triweight tools.

However, a direct Golay-style enumeration would involve `2^72` triples. The
site should list the QR48 triweight as a future target for the symmetrized /
modular / reconciliation pipeline, not as an already-computed download.
