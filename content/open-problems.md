# Open Problems

This is the community engine of the project. Each card is a bounded, concrete
task — not "help wanted," but a specific input, a specific expected output, and a
specific certificate that decides whether the task is done. We deliberately favor
work whose result is **independently checkable**: a route-3A witness, an exact
Farkas certificate, a re-verification in a second language, or a reproducible
cluster payload.

Two standing rules apply to everything below:

- A surviving [length-40 menu](menu-summary.md) row is a still-compatible
  *shadow*, not a code; the **21 unresolved rows** are "not yet exhausted," never
  "likely empty."
- Project status changes require an exact certificate or an independently
  replayable computation. Numerical evidence is welcome as a scout, but it does
  not move the [menu](menu-summary.md) or the [test ledger](tests/index.md).

The current state: `132` length-40 candidates `→ 60` proof-grade eliminations
`→ 72` surviving, of which `51` are witnessed nonempty and `21` are unresolved.
All `8` proof-grade kills now ship 🟢 exact-replayable reproduction bundles
(`python3 repro/verify_all.py` runs `9/9`). The frontier is the unresolved rows,
the open anchored SDP (`T29`), the design subproblems, and the precise payoff
bridges.

Discussion for every card happens in the **`#extremal72`** channel of the Error
Correction Zoo Discord: <https://discord.gg/gg3pJZNYxQ>. Claim a card there
before starting long compute so we don't duplicate it.

---

## E72-101 — Exhaust the smallest unresolved length-40 rows

**One-line goal:** Convert the smallest-`m` unresolved route-3A rows from `⏳` to
`✔️` (witness) or `❌` (proof-grade empty).

**Mathematical input:** The unresolved rows of the length-40 menu — surviving
`(k,a,b)` with no witness and no completed exhaust. Each row is a doubly-even,
self-orthogonal `[40,k,≥16]` shadow with `W_E(y) = 1 + a(y^{16}+y^{24}) + b\,y^{20} + y^{40}`.

**Repository input:** The route-3A enumeration engine (per `Σ ℓ² = sq` stratum)
and the [T32](tests/T32-exists.md) reproduction bundle, which already
re-certifies `1528` witnesses in pure Python.

**Expected output:** For each targeted row, either a constructive witness code or
a complete zero-leaf exhaust tree.

**Success certificate:** A witness is a stored `ℓ`-vector that expands to a
valid `[40,k,16]` code (replayable by the T32 verifier). An empty proof is a
complete zero-leaf exhaust with a reproducible state count, like the
`(6,29,4)` empty proof (`301,872` states, `0` codes).

**Difficulty:** Medium per row, rising sharply with `m`.

**Skills:** Coding theory, combinatorial enumeration, performance-aware C++/Rust
or Python.

**Compute needed:** Workstation for the smallest rows; the larger `k`/`a` rows
push toward many-core / cluster.

**Status:** Open. `21` rows unresolved; smallest-`m` first is the recommended
order.

**Discussion:** `#extremal72`.

---

## E72-102 — Independent replay of the `(6,29,4)` empty exhaust

**One-line goal:** Reproduce the first exhaustion kill in a second, independent
implementation.

**Mathematical input:** The row `(6,29,4)` and the claim that no `[40,6,16]`
code realizes it (the first proof-grade kill of a row that survived every
algebraic screen, recorded by [T32](tests/T32-exists.md)).

**Repository input:** The route-3A exhaust spec for `(6,29,4)` (`301,872`
states, `0` leaves) shipped as the 🔴 part of the T32 bundle.

**Expected output:** An independent enumerator that reaches the same zero-leaf
verdict, plus a one-click replay package (its own `run.sh`).

**Success certificate:** A second-implementation exhaust whose leaf/state counts
match and that terminates with `0` codes; ideally a canonical-augmentation tree
that a third party can re-walk.

**Difficulty:** Medium.

**Skills:** Computational group theory, isomorph rejection (canonical
augmentation), reproducible packaging.

**Compute needed:** Single workstation (this row is small).

**Status:** Open. The empty proof exists but ships as a spec, not a one-click
🟢 bundle — a second language closes that gap.

**Discussion:** `#extremal72`.

---

## E72-103 — Exact certificate for the open anchored SDP (`T29`)

**One-line goal:** Turn the anchored three-point SDP from a boundary-margin
numerical screen into a proof-grade verdict.

**Mathematical input:** The single-anchor anchored three-point (Terwilliger-type)
SDP on the length-72 minimum-word structure, coupled to the menu. Its linear
layer is exact and exhausted (`glpsol`, all mixtures feasible); its PSD layer
sits at the double-precision floor with boundary margin `≈ 0`, sign
undeterminable. See [T29](tests/T29-a3p.md).

**Repository input:** The T29 payload (constraint system, moment-matrix blocks)
and the exact linear gate.

**Expected output:** Either a rigorous infeasibility certificate (a kill) or a
rigorous feasibility witness at the margin (the screen genuinely saturates).

**Success certificate:** An exact / verified-precision dual certificate — a PSD
multiplier matrix with rational or interval-arithmetic entries whose sign is
provable — or a constructive feasible moment matrix. A raw double-precision
solver verdict at margin `≈ 0` does **not** count.

**Difficulty:** Hard.

**Skills:** SDP duality, exact/interval SDP, symmetry-adapted
block-diagonalization.

**Compute needed:** Workstation for the block-reduced problem; cluster + licensed
or exact solver for the full system.

**Status:** Open / blocked by scale at the PSD boundary. The most valuable single
upgrade on the SDP line.

**Discussion:** `#extremal72`.

---

## E72-104 — Non-aggregate per-anchor coupling beyond `T29`

**One-line goal:** Replace the aggregated anchored mixtures with a per-anchor
coupling that can separate where the aggregate saturates.

**Mathematical input:** The observation that several anchored / Mode-1 aggregate
tests ([T26](tests/T26-tag.md), [T30](tests/T30-am1.md)) are feasible even when
strengthened, because aggregation averages away a per-anchor obstruction. The
target is a coupling that constrains each anchor's residual individually rather
than the mixture.

**Repository input:** The anchored linear gate, the genus-2 Jacobi coupling that
reduces the `[56,21]` residual biweight family from `9-dim` to `5-dim`, and the
per-coset image counts.

**Expected output:** A new exact feasibility system, with at least one row it
excludes that the aggregate test passes — or a proof that the per-anchor system
collapses to the aggregate (a saturation result, also valuable).

**Success certificate:** A Farkas certificate for any newly excluded row,
replayable in pure Python like the existing 🟢 kills.

**Difficulty:** Hard.

**Skills:** LP/SDP modeling, MacWilliams/Jacobi duality, exact certificates.

**Compute needed:** Workstation (exact LP via PPL / `glpsol --exact`), occasional
cluster for large per-anchor systems.

**Status:** Open / exploratory.

**Discussion:** `#extremal72`.

---

## E72-105 — Second-language re-verification of the 8 proof-grade kills

**One-line goal:** Independently re-derive all `8` proof-grade eliminations in a
language other than the published Python verifiers.

**Mathematical input:** The eight kills — [T02](tests/T02-pimg.md) parent-image
dimension bound, [T05](tests/T05-3bnn.md) three-block nonnegativity (Farkas),
[T06](tests/T06-smth.md) toggle-stabilizer Smith congruence,
[T08](tests/T08-john.md) Johnson/Delsarte bound `247`, [T13](tests/T13-dshr.md)
double-shortening Johnson bound, [T19](tests/T19-sim.md) Simonis order-4 Farkas,
[T20](tests/T20-g2.md) coupled genus-2 biweight Farkas, and
[T32](tests/T32-exists.md) route-3A witnesses — plus T01's re-enumeration of the
`132`.

**Repository input:** The 🟢 reproduction bundles, each shipping `expected.json`,
the data pinned by sha256, and a pure-Python verifier.

**Expected output:** A parallel verifier suite (e.g. Sage, GAP, Julia, Rust, or
Lean) that recomputes each `expected.json` from the same pinned inputs.

**Success certificate:** Independent agreement on every value (the bound `247`,
the `132`, each Farkas/Smith certificate) using exact arithmetic in the new
language; bonus for a machine-checked proof of any single kill.

**Difficulty:** Medium (per kill); harder for a formalized proof.

**Skills:** Exact linear algebra, Smith normal form, Delsarte LP, formal
methods (optional).

**Compute needed:** Single workstation.

**Status:** Open. The 🟢 bundles run `9/9` in Python; a second language is the
strongest trust signal we can add.

**Discussion:** `#extremal72`.

---

## E72-106 — Independent verifier for the forced split / `[56,21]` residual enumerator

**One-line goal:** Re-derive the forced weight-16 split enumerator and the
`[56,21,≥16]` residual with its `5082` minimum words from scratch.

**Mathematical input:** Anchoring one weight-16 word in a hypothetical
`[72,36,16]` code forces a unique split enumerator and a residual
`[56,21,≥16]` object with exactly `5082` weight-16 words; the forced minimum-word
count of the parent is `A_16 = 249849`.

**Repository input:** The published split-enumerator and residual-enumerator JSON
(pinned by sha256), and the partition-MacWilliams solution that fixes them.

**Expected output:** An independent solver that recovers the unique split and the
`5082` count, plus a one-click verifier consuming the published data.

**Success certificate:** Bit-for-bit agreement with `A_16 = 249849` and the
`5082` residual minimum words, derived from the MacWilliams system rather than
read from the file.

**Difficulty:** Medium.

**Skills:** MacWilliams identities, partition/Jacobi enumerators, exact rational
linear algebra.

**Compute needed:** Single workstation.

**Status:** Open. Listed in SCOPE §9 as `E72-001`/`E72-002`; this card is the
independent-verifier half.

**Discussion:** `#extremal72`.

---

## E72-107 — Constrain the `5-(72,16,78)` minimum-word design

**One-line goal:** Add exact design-theoretic obstructions on the `249849`
minimum words that survive what the enumerator already forces.

**Mathematical input:** If the code exists, its `249849` weight-16 words form a
`5-(72,16,78)` design. Block intersection numbers, derived/residual designs, and
higher-incidence constraints are partly fixed by the enumerator but not
exhausted.

**Repository input:** The forced parent enumerator, the genus-2 biweight of
`[72,36,16]` (uniquely forced), and the higher-genus design-moment data (note:
the genus-3 design-moment equalities have rank `0`, so the leverage must come
from elsewhere).

**Expected output:** An exact contradiction in the design parameters (a kill), or
a sharpened set of forced intersection/incidence numbers that feeds back into the
menu.

**Success certificate:** A proof-grade design infeasibility (e.g. an integer or
Farkas obstruction on block intersections), independently checkable.

**Difficulty:** Hard.

**Skills:** Design theory, finite geometry, integer feasibility.

**Compute needed:** Workstation; possibly cluster for large incidence systems.

**Status:** Open. A genuine independent angle — design constraints are not
subsumed by the menu recursion.

**Discussion:** `#extremal72`.

---

## E72-108 — Pin the `5082` residual minimum words

**One-line goal:** Determine or obstruct the configuration of the `5082`
weight-16 words in the forced `[56,21]` residual.

**Mathematical input:** The forced `[56,21,≥16]` residual carries exactly `5082`
minimum words. Its genus-2 biweight is known only as a family: exactly `9-dim`
(affine, after its own marginals), reducing to exactly `5-dim` under the length-72
anchored genus-2 Jacobi coupling.

**Repository input:** The residual biweight family data and the anchored Jacobi
coupling that performs the `9→5` reduction.

**Expected output:** A constraint (exact LP/SDP, design, or geometric) that pins
or excludes part of the remaining `5-dim` freedom, or a proof that the `5082`
words cannot be packed into `56` coordinates consistently.

**Success certificate:** A proof-grade narrowing of the `5-dim` family or a
Farkas-style infeasibility for the residual word configuration.

**Difficulty:** Hard.

**Skills:** Constant-weight packing, MacWilliams/Jacobi families, design theory.

**Compute needed:** Workstation (exact LP); cluster for finer packing systems.

**Status:** Open. Note that plain length-56 constant-weight bounds are far too
loose for `5082` — leverage must use residual/glue/code-level structure.

**Discussion:** `#extremal72`.

---

## E72-109 — Conditionally close the `C_5` sub-menu, automorphism-agnostically

**One-line goal:** Kill all `16` length-40 rows with `a ≡ 0 (mod 5)` using only
tests that hold for the trivial automorphism group.

**Mathematical input:** The code's automorphism group is one of
`{C_1, C_2, C_3, C_2×C_2, C_5}`, with **nothing assumed** (`C_1` is the hardest
case). Orbit counting (`A_16 = 249849 ≡ 4`, residual `5082 ≡ 2 (mod 5)`) forces a
`C_5`-symmetric code to realize one of `16` surviving rows with `a ≡ 0 (mod 5)`;
these are listed on the [menu page](menu-summary.md).

**Repository input:** The `16`-row sub-menu and the automorphism-agnostic test
pipeline.

**Expected output:** Proof-grade eliminations (or witnesses) for the `16` rows,
using only `C_1`-valid tests.

**Success certificate:** A 🟢-style replayable kill for each of the `16` rows; if
all `16` fall, the `C_5` branch closes with no Hermitian `F_16` search. Note the
converse does **not** hold — these rows are not removed from the full menu by
ruling out `C_5`, since a `C_1` code could still cast any of them.

**Difficulty:** Medium to hard (varies by row; the large-`k` rows are exhaust-heavy).

**Skills:** Coding theory, computational group theory, exact certificates.

**Compute needed:** Workstation for small rows; cluster for `k=9,10`.

**Status:** Open. A far cheaper target than the full menu — `16` specific rows.

**Discussion:** `#extremal72`.

---

## E72-110 — Cluster-ready exact anchored SDP payload + memory estimate

**One-line goal:** Package a proof-grade, cluster-scale anchored SDP run with an
honest resource budget.

**Mathematical input:** The anchored three-point SDP of [T29](tests/T29-a3p.md),
whose PSD layer is unresolved at the boundary at local scale.

**Repository input:** The T29 constraint system and moment-matrix blocks; the
linear gate that is already exact.

**Expected output:** A self-contained payload — exact/high-precision SDP input,
solver invocation, expected wall-clock, **and a memory estimate** (the prior
exact attempt OOM'd; block sizes drive the budget) — plus the certificate path
that would make a result proof-grade.

**Success certificate:** A reproducible spec a contributor can run on a known
cluster, ending in a checkable dual certificate (ties into E72-103).

**Difficulty:** Hard.

**Skills:** HPC, SDP solver internals, exact/high-precision arithmetic,
reproducibility.

**Compute needed:** Cluster-scale; licensed (MOSEK) or exact (e.g. SDPA-GMP-class)
solver, with the memory budget that the payload must publish up front.

**Status:** Open / blocked by scale. Listed in SCOPE §9 as `E72-006`.

**Discussion:** `#extremal72`.

---

## E72-111 — Precise code → CFT (c = 36) bridge note

**One-line goal:** Write the exact construction taking the `[72,36,16]` code to a
chiral / Narain-style code CFT at central charge `c = 36`, with explicit
assumptions.

**Mathematical input:** A binary Type II `[72,36,16]` code, the
Construction-A even unimodular lattice route in dimension 72, and the standard
lattice → CFT map. **Caveat to carry:** the Construction-A lattice
`Λ = (1/√2){x ∈ ℤ^{72} : x mod 2 ∈ C}` is even unimodular but has minimum norm
`2`, **not** `8`; do not call it extremal.

**Repository input:** The forced enumerator (which fixes the CFT character /
partition-function data) and the modular-bootstrap notes.

**Expected output:** A public bridge page: the precise CFT object, what the
forced weight enumerator pins about its partition function, and exactly which
steps are standard vs. conjectural.

**Success certificate:** Every "→" in the bridge is either a cited standard
construction or a flagged assumption; no "the CFT proves…" without an explicit
map.

**Difficulty:** Hard.

**Skills:** CFT / modular bootstrap, lattices, code-CFT correspondence.

**Compute needed:** None (expository), optional character-arithmetic check.

**Status:** Open. Listed in SCOPE §9 as `E72-008`.

**Discussion:** `#extremal72`.

---

## E72-112 — Precise code → `[[71,1,≥15]]` self-dual CSS bridge note

**One-line goal:** Write down the exact CSS quantum code obtained from a
`[72,36,16]` Type II code, with the distance argument.

**Mathematical input:** A binary self-dual doubly-even `[72,36,16]` code yields,
via the standard self-dual-classical → CSS construction, a self-dual CSS
quantum code; the target package is `[[71,1,≥15]]`. The distance bound and the
exact length/dimension bookkeeping must be stated, not asserted.

**Repository input:** The forced enumerator and minimum-distance data.

**Expected output:** A public bridge page giving the explicit CSS construction,
the parameters, and a proof (or precise citation) of the `≥15` distance.

**Success certificate:** The construction is reproducible from the classical
generator matrix and the distance bound is argued, not quoted; a small worked
check (e.g. on a known smaller Type II code) accompanies it.

**Difficulty:** Medium.

**Skills:** Quantum CSS codes, self-dual codes, distance arguments.

**Compute needed:** None to light (expository plus a sanity-check on a small code).

**Status:** Open. Listed in SCOPE §9 as `E72-009`.

**Discussion:** `#extremal72`.

---

## How to claim a card

1. Post in `#extremal72` on the
   [Discord](https://discord.gg/gg3pJZNYxQ) naming the card ID (e.g. `E72-101`).
2. Read the matching [test page](tests/index.md) and pull its reproduction
   bundle.
3. Return a result with a **certificate**, not just a number — a witness, a
   Farkas/Smith/dual certificate, or a one-click replay package.

See also: [The Length-40 Menu](menu-summary.md), [Tests](tests/index.md),
[Current Map](current-map.md), and the [Audit Trail](audit-trail.md) for why we
publish corrections as part of the result.
