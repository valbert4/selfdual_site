# Contribute

This is an open, community-verifiable search. The job is to decide whether a
binary Type II `[72,36,16]` code exists. Every status change needs exact input
and an independently checkable certificate — numerical evidence is welcome as a
probe, but it does not move the public count by itself.

If you only have a few minutes: pick a lane below, then take one of its first
tasks to the Discord.

## Discussion

Questions, ideas, and progress live in the **#extremal72** channel of the
[Error Correction Zoo Discord](https://discord.gg/gg3pJZNYxQ). That is the place
to ask where to start, claim an [open problem](open-problems.md), say what you
are about to run (so two people do not exhaust the same row), or share a
computation for review.

[**Join the EC Zoo Discord — #extremal72**](https://discord.gg/gg3pJZNYxQ)

## Where the problem stands right now

So you can aim at something real, not a generic "help wanted":

- The search reduces to a finite [length-40 menu](menu-summary.md): `132`
  arithmetic shadows, `60` eliminated proof-grade, `72` still viable.
- Of the `72`, `51` are witnessed nonempty and `21` are **unresolved** — not yet
  exhausted, which is *not* evidence of emptiness. Closing or witnessing any of
  these `21` is the cleanest open prize.
- All `8` proof-grade kills now ship pure-Python verifiers; the open frontier is
  the solver-required saturations, the `3` validation-only tests
  (`T17`/`T18`/`T23`), and the cluster-scale anchored SDP (`T29`).
- The automorphism group is narrowed to one of `{C_1, C_2, C_3, C_2×C_2, C_5}`
  but **nothing is assumed** — every test must hold for the trivial group `C_1`,
  the hardest case. There is a [`C_5` sub-menu](menu-summary.md) of 16 rows with
  `a ≡ 0 (mod 5)`.

---

## "I can prove things"

Coding theory, finite geometry, designs, invariant theory — turn a numerical
screen or a saturated relaxation into a proof-grade obstruction (or a
construction). The highest-value targets are the ones where a continuous
relaxation saturates but an integer/structural argument might still cut.

First tasks:

- **Find a new exact obstruction for an unresolved row.** Pick one of the `21`
  unresolved [menu](menu-summary.md) rows and produce an argument no continuous
  LP/SDP can absorb (integer divisibility, forced intersection, design moment).
  See [Open Problems](open-problems.md).
- **Sharpen the `[56,21]` residual design.** The forced residual has exactly
  `5082` weight-16 words; constant-weight packing is far too loose for that
  target. Tighten it with design-theoretic / intersection structure on the
  minimum words (`5-(72,16,78)` consequences). See [Open Problems](open-problems.md).
- **Close the `C_5` branch on paper.** If automorphism-agnostic tests can
  eliminate all `16` rows with `a ≡ 0 (mod 5)`, the `C_5` case closes with no
  Hermitian `F_16` search. See the [Menu](menu-summary.md).

## "I can code exact algebra / verification"

Re-derive a published result from scratch, in exact arithmetic, with no licensed
solver — this is how a kill earns its place in the public count. Every
proof-grade elimination ships a reproduction bundle whose verifier must run
everywhere.

First tasks:

- **Write an independent split-enumerator verifier.** Reproduce the uniquely
  forced split enumerator (`A_16 = 249849`, residual `5082`) from the partition
  MacWilliams system, in your own code, and compare against the published JSON
  (pinned by sha256). See [Computations and Certificates](computations-and-certificates.md).
- **Package the `T32` direct-existence exhaust for independent replay.** The
  route-3A `(6,29,4)` empty row and the `51` nonempty witnesses should be
  re-checkable from scratch (the `T32` bundle already re-certifies the witness
  side). See the [Tests index](tests/index.md) and `T32`.
- **Convert a solver-required test to a replayable verifier.** Most of the
  saturating tests still depend on a solver; pick one and ship a pure-Python
  `verify.py` that re-checks its published claim against pinned input data. See
  [Computations and Certificates](computations-and-certificates.md).

## "I can run cluster jobs (HPC)"

The remaining open work is partly a scale problem. Run bounded jobs, capture
logs, publish checksums, and turn an "out of local reach" branch into a
reproducible payload.

First tasks:

- **Exhaust an unresolved menu row.** Take one of the `21` unresolved
  [menu](menu-summary.md) rows through a route-3A direct-existence search to a
  definite verdict (witness or empty), and ship the state count plus a
  replayable result. See `T32` in the [Tests index](tests/index.md).
- **Stand up the anchored-SDP cluster payload.** `T29`'s linear layer is exact
  (`0` kills); the PSD layer sits on the feasibility boundary and needs a
  proof-grade, cluster-scale certificate. Run the payload and publish the
  environment + checksums. See [Open Problems](open-problems.md).
- **Package logs to spec.** For any long run, produce the exact command, commit,
  machine, runtime, and output checksum required by
  [Computations and Certificates](computations-and-certificates.md).

## "I know SDP/optimization"

Delsarte/Schrijver/Terwilliger and the anchored Jacobi layers are where the
hardest open test lives. The lesson so far: several natural relaxations
*saturate* (the Polak `B_4` quadruple SDP equals the ordinary Delsarte bound at
length 40), so new leverage must come from exact certificates, not tighter
floats.

First tasks:

- **Upgrade `T29` from linear feasibility to a PSD-certified kill (or prove it
  cannot kill).** The anchored 3-point SDP is OPEN at the boundary, margin ≈ 0;
  a proof-grade dual certificate either closes the row or shows the boundary is
  genuine. See `T29` and [Open Problems](open-problems.md).
- **Promote a validation-only SDP to proof-grade.** `T17` (A3 constant-weight
  SDP) currently has *no* public elimination — it needs an exact SDP certificate
  with a verified constraint system before any row moves. See the
  [Tests index](tests/index.md).
- **Audit float-LP verdicts for rounding.** Large coefficients can be rounded at
  LP/MPS input before exact simplex runs; classify older infeasibility claims by
  whether the input itself was exact. See [Computations and Certificates](computations-and-certificates.md).

## "I know CFT / lattices / quantum codes"

The payoff side. A construction would produce a `5-(72,16,78)` design, a code
CFT at central charge `c = 36`, and a `[[71,1,≥15]]` self-dual CSS code. These
bridges should be stated precisely, with assumptions and references, not as
front-page slogans.

First tasks:

- **Write the precise code-to-CFT bridge note.** State the construction at
  `c = n/2 = 36`, with the genus-`g` partition function as the theta lift of the
  genus-`g` weight enumerator, and what the computed genus-3 Θ-projection does
  and does not pin. See [Open Problems](open-problems.md).
- **Write the self-dual CSS bridge note.** Pin down the `[[71,1,≥15]]` object
  obtained by puncturing and `CSS(C^⊥, C^⊥)`, with the distance bound argued
  exactly. See [Open Problems](open-problems.md).
- **Sanity-check the lattice claim.** Construction A on `[72,36,16]` gives an
  even unimodular lattice with minimum norm `2` — *not* extremal (an extremal
  72-dimensional even unimodular lattice has minimum norm `8`); the link to the
  known extremal lattices is the harder converse question. Verify and sharpen
  this. See [Open Problems](open-problems.md).

## "I can improve the website/data"

Make the work legible and the certificates checkable in a browser. The site is
static Markdown plus small structured `data/` files; keep retractions and audit
notes visible.

First tasks:

- **Rank the `21` unresolved rows by promise and cost.** Turn the menu state
  into a small structured table contributors can claim from. See the
  [Menu](menu-summary.md).
- **Build an exact-certificate browser.** Make the Farkas / verifier artifacts
  inspectable online so a reader checks a kill without cloning anything. See
  [Computations and Certificates](computations-and-certificates.md).
- **Draw the residual-tower diagram.** A clean visual of
  `[72] → [56] → [40] → [24]` for the [Hierarchy](hierarchy.md) page. See
  [Open Problems](open-problems.md).

---

## How to verify a result yourself

Every proof-grade elimination ships a **reproduction bundle**: a small verifier
that re-derives that test's published result from public data (pinned by
sha256), so you can check the proof rather than trust the script.

The `8` proof-grade kills are all 🟢 *exact-replayable* — pure Python standard
library, exact arithmetic, no solver. To re-check all of them at once
(plus the `T01` re-enumeration of the `132`):

```sh
python3 repro/verify_all.py
```

This reports `9/9 bundles reproduced`. The kills it replays:

- `T02` parent-image dimension bound
- `T05` three-block nonnegativity (Farkas)
- `T06` toggle-stabilizer Smith congruence
- `T08` Johnson/Delsarte two-point bound (`247`)
- `T13` double-shortening Johnson bound (`7657/67`)
- `T19` Simonis order-4 Farkas
- `T20` coupled genus-2 biweight Farkas
- `T32` route-3A witnesses

The solver-required saturations (🟡) and the cluster/licensed exceptions
(🔴: `T17`, `T18`, `T23`, `T29`, the empty-exhaust) ship a payload and spec
rather than a one-click run. See [Computations and Certificates](computations-and-certificates.md)
and the [Tests index](tests/index.md).

## How to submit

A result that should change project status needs two things:

1. **Exact input** — the data the claim consumes, with a checksum, so anyone can
   confirm they are checking the same thing (no coefficients rounded at read
   time).
2. **A replayable certificate or an independent verifier** — a Farkas/dual
   certificate, a route-3A witness/exhaust, or a pure-Python `verify.py` that
   re-derives the claim and exits `0` iff it holds. Match the
   [reproduction-bundle](computations-and-certificates.md) format so it slots
   into `verify_all.py`.

Then bring it to **#extremal72** on the
[Discord](https://discord.gg/gg3pJZNYxQ) for review. A row leaves the public
menu only once its obstruction is exact and independently checkable.
