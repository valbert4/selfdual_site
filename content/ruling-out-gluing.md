# Ruling out a glue

A construction-side route to settling `[72,36,16]` is to build it *upward* from a
known length-40 code. This is **gluing**. Despite many attempts, no glue has been
built — and, just as importantly, no glue has been proven *impossible*. This page
states the problem precisely, summarizes where the search stands, and lists the
concrete sub-problems whose resolution would rule a glue in or out.

If you want one sharp, self-contained challenge that touches exact algebra, SAT,
and SDP at once, this is a good place to bite in. Bring questions to
[**#extremal72** on the Discord](https://discord.gg/gg3pJZNYxQ).

## The construction (the residual tower, run backwards)

The search normally *descends*

```
[72,36,16]  →  [56,21,≥16]  →  [40,k,≥16]  →  [24, …]
```

by repeatedly shortening at a weight-16 coordinate block. Gluing runs this
*backward*: start from a classified `[40,k,16]` doubly-even self-orthogonal code
`E` (containing the all-ones word) and try to extend it two steps back up to a
`[72,36,16]`. There are two independent lifts:

- **Stage 1:** `[40,k] → [56,21,≥16]`
- **Stage 2:** `[56,21] → [72,36,16]`

Everything below is about **Stage 1** (length 40 → 56). No Stage-1 code has ever
been produced, so Stage 2 — the classical wall — has never been reached.

**Why 56 is pivotal.** `56 = 72 − 16`. If a Type II `[72,36,16]` exists, its
residual at any weight-16 word is forced to be a `[56,21,≥16]` doubly-even
self-orthogonal code containing the all-ones word, with a *unique* forced weight
enumerator — in particular **exactly `A_16 = 5082` minimum words**. So a
length-56 code carrying that exact enumerator is the middle object the whole
construction route turns on.

## The glue map

Fix the length-16 block. A Stage-1 glue is a linear map

```
γ : J → Q_E = E^⊥ / E
```

from an image code `J` (with `dim J = 21 − k`) into the **discriminant form**
`Q_E` — a quadratic space of dimension `40 − 2k`. It must satisfy:

- **kernel = the all-ones word exactly**, so `γ` embeds `J / ⟨1⟩`;
- **it preserves the bilinear and quadratic forms** (this is what makes the
  length-56 code doubly-even and self-orthogonal);
- **the binding condition:** every glued coset has minimum weight high enough to
  hold the distance at `≥ 16`.

Concretely, choosing `γ` means choosing `20 − k` coset images whose *every*
XOR-combination clears its weight threshold — a "deep" packing condition. The
form conditions are easy to satisfy; **the distance condition is the wall.**

## What has been tried — and the two walls

Two structurally *opposite* length-40 families were pushed hard. Each fails for a
different reason, and in each case the failure is a **search/solver limit, not an
impossibility proof.**

### Family A — a highly symmetric "duplicated-point" code (k = 6)

Built from the 32 affine points of a Reed–Muller code plus 8 repeated copies of a
single point. Here `Q_E` factors into a *linear* part and a small
"duplicate-block" part, and the deepness condition splits cleanly:

- The linear/nonlinearity part is **trivially solvable** — a Gold/bent shell
  clears every binding combination instantly.
- The duplicate-block part is the wall: the required weight pattern is realizable
  only if the underlying cubic structure is a very special object (a
  **Delsarte–Goethals / Kerdock shell**), not a generic one. Generic choices pass
  every counting and parity test yet are **unrealizable** as a single linear
  pattern.

This deep-realizability search is *monotone* (a failure at small depth forces
failure at full depth), so it can be searched directly. It has been confirmed
realizable only to a bounded depth; a 64-core, multi-hour cluster search found
**no glue and no proof of impossibility.** Separately, every counting-style
attempt to *kill* this code — exhaustive coset-supply counts, and an exact
forced-enumerator + MacWilliams LP — comes back **feasible** (no obstruction). So
the proof-grade evidence actually leans *toward* this code being glueable; we
simply cannot exhibit the glue or rule it out.

### Family B — "clean" codes with no repeated points (k = 7, 8, 9)

Here `Q_E` is a single quadratic space and the glue is a pure isometry search.
The distinction that matters:

- a **form-isometry** preserves the algebra but ignores distance — one is found
  **instantly**, so there is no algebraic obstruction;
- a **deep isometry** is a form-isometry that *also* keeps every combination
  above threshold — this is what `d ≥ 16` requires.

No deep isometry was found. Minimizing the **leak** (the number of below-threshold
combinations) by every available heuristic **floors at ≈ 10 for k = 9 and ≈ 11
for k = 8**, and never reaches zero. An exact analysis localizes the obstruction
to a specific class of about `30` combinations that cannot all be simultaneously
deep. But that leak floor is a *heuristic minimum*, not a proven one — the true
minimum could in principle be `0` in a basin the search never enters.

## The crux: search-exhaustion is not a proof

This is the single most important point for anyone joining this problem.

- **Proven (proof-grade):** the counting kills *fail*; a form-isometry *exists*;
  the obstruction is *localized*. These are exact statements.
- **Not proven:** that *no* glue exists. Both walls are bounded by **solver time**
  (Family A) or **heuristic search depth** (Family B), not by an impossibility
  certificate.

So the honest status is: **neither family has been glued, and neither has been
provably ruled out.**

## Why ruling one out is hard

The proof-grade verdict reduces to a single large finite **SAT** instance — encode
the binding combinations exactly and solve once. **UNSAT** would prove no glue
exists; **SAT** would hand back an actual `[56,21,16]`. The catch: the instance
sits *exactly* at the SAT/UNSAT phase boundary and carries a quadratic-form
coupling that makes it enormous — encodings with millions of variables have run
for hours without resolving.

The alternative is an exact LP/SDP **infeasibility certificate**, but it needs a
relaxation that can *see that the glued image is closed under addition* (it is a
group). The natural forced-enumerator LP provably cannot see that, which is
exactly why it saturates.

## How you can help

Concrete, self-contained sub-problems — any one of these is a real result:

1. **Finish or shrink the finite SAT.** Drive the exact encoding to a verdict, or
   extract a **minimal unsatisfiable core** from the ~`30`-combination obstruction
   class. A small core is a far cheaper proof of "no glue with this image" than
   the full instance.
2. **Break the quadratic coupling.** Fix one image to automorphism-orbit
   representatives to linearize the dominant coupling that makes the SAT instance
   hard.
3. **Build the special cubic shell (construction route).** For Family A, replace
   the generic cubic extension with the explicit Delsarte–Goethals / Kerdock shell
   so the weight pattern is realizable *by construction*. Success here yields the
   first concrete `[56,21,16]` — settling it by *finding* rather than ruling out.
4. **A group-aware relaxation.** Add linked-triple (subgroup-closure) constraints,
   or a Terwilliger-style PSD layer, to the forced-enumerator LP — the only
   remaining counting-style lever that could produce an exact kill.
5. **A stronger heuristic aimed at leak 0.** For Family B, a deeper
   annealing/restart search that *finds* a deep isometry would resolve the
   "tiny-basin" uncertainty by exhibiting a glue.

## An honest caveat about scope

Ruling out a glue is a sharp and worthwhile sub-problem, but it is **not** how
`[72,36,16]` non-existence would be proven. Non-existence, if true, has to come
from the Delsarte / [menu](menu-summary.md) side of the search; ruling out a glue
for one code — or even every classified code — does not by itself exclude the
`[72,36,16]`. So treat gluing primarily as a **construction** effort (find a real
`[56,21,16]`, then attack the genuine Stage-2 wall), and treat "rule it out" as a
clean, self-contained challenge: *can even a single candidate glue be proven
impossible?*

See also the [Open Problems](open-problems.md) and
[Computations and Certificates](computations-and-certificates.md) pages, and the
[Hierarchy](hierarchy.md) for the `[72] → [56] → [40] → [24]` descent.
