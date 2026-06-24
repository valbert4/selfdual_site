# Computations and Certificates

This page is about trust. The project lives or dies on whether outsiders can
*check* it, so we hold our own status changes to a standard we want others to
hold us to.

## The public rule

Numerical evidence is welcome. It is how almost every result here started: a
solver returns "infeasible," an LP bottoms out, an SDP sits near a boundary.
That is enough to point effort, and we publish it as such.

But a **status change** — moving a [menu](menu-summary.md) row from *surviving*
to *eliminated*, or calling a branch closed — requires more than a solver's
verdict. It requires at least one of:

- **exact input** — the constraint system reconstructed in exact rational
  arithmetic, with no value rounded on the way in;
- **an independently replayable certificate** — a Farkas vector, a Smith-form
  witness, an exhaustive enumeration — that a second party can re-check without
  re-running our search;
- **a separate verifier** — a short program, ideally in different software from
  the one that found the result, that confirms the claim from public data.

A row is not removed from the public menu unless the obstruction is exact and
independently checkable. We publish corrections as part of the result.

## The three reproduction tiers

Every [test](tests/index.md) ships a reproduction bundle. Each bundle carries a
verifier — the part that must run everywhere — and, optionally, the original
solver that *found* the certificate. Bundles are sorted into three tiers by how
hard they are to re-run.

- 🟢 **exact-replayable** — pure-Python standard library, exact arithmetic, no
  solver, no license. Runs in CI on every commit. The verifier consumes the same
  published enumerator data the site serves, pinned by `sha256`, so
  "reproduces" means *recomputes the claim from data whose checksum matches what
  we publish*. These are the bundles that back our proof-grade kills.
- 🟡 **solver-required** — needs an exact solver (PPL, Sage, or `glpsol --exact`).
  Ships the real solver plus the exact command. Run in extended/nightly CI, not
  on every commit. These are saturation results (LP/SDP screens that did not
  kill a row); they carry **0 kills**, so nothing in the public status depends
  on reproducing them — they are shipped for completeness.
- 🔴 **cluster / licensed or open** — not a one-click run. Ships a *spec* — the
  payload, the memory estimate, the certificate path that *would* close it — not
  a button. The anchored 3-point SDP (`T29`) is the headline example: its linear
  layer gives `0` kills exactly (checkable), but its PSD layer is unresolved at
  the feasibility boundary and needs a licensed solver at cluster scale. The
  full `(6,29,4)` empty-exhaust is the other 🔴 bundle.

## The 9 exact-replayable bundles

These are the bundles behind the project's proof-grade results. All 8 kills plus
the menu re-enumeration are reproduced here with **no floating point, no licensed
solver, and no external service** in the verify path — every certificate is an
exact rational vector, a Farkas/Smith witness, or an exhaustive enumeration.

| Bundle | What it proves | Certificate type | How it is checked |
|---|---|---|---|
| **T01** `int` | The raw menu is exactly the `132` integer, self-orthogonal candidates | exhaustive enumeration | re-enumerate the `132` from the validity filter and compare the set |
| **T02** `pImg` | Parent-image dimension bound `21 − k ≤ 15` (**31 kills**) | exact dimension inequality | recompute the image dimension per row; flag every row that violates the bound |
| **T05** `3bNN` | Three-block (`16∣16∣40`) MacWilliams counts cannot go negative (**7 kills**) | Farkas vector (exact rational) | replay the Farkas certificate against the block system; confirm the forced negative count |
| **T06** `Smth` | Toggle-stabilizer divisibility via integer Smith normal form (**16 kills**) | Smith-form solvability witness | solve the congruence in pure Python; **cross-checked against Sage** |
| **T08** `John` | Exact Delsarte two-point bound `= 247`, by vertex enumeration | exact LP vertex enumeration | enumerate vertices in exact arithmetic; bound `247` kills `(9,255,0)` |
| **T13** `dShr` | Single-distance Johnson bound `7657/67` after forced intersections | exact rational bound | recompute the bound as an exact fraction; it kills `(9,247,16)` |
| **T19** `Sim` | Simonis order-4 support-weight infeasibility | Farkas vector (exact rational) | replay the support-weight Farkas certificate; kills `(6,1,60)` |
| **T20** `g2` | Coupled genus-2 biweight nonnegativity fails | Farkas vector (exact rational) | replay the biweight Farkas certificate; kills `(9,239,32)` |
| **T32** `exists` | The `1528` route-3A nonempty witnesses are genuine | explicit constructive witnesses | re-certify each of the `1528` witnesses from scratch |

`T02`, `T05`, `T06`, `T08`, `T13`, `T19`, `T20`, and `T32` are the **8
proof-grade kills**; `T01` fixes the `132` they all start from. Together they
account for the `60` eliminated menu rows and the witnessed-nonempty side of the
survivors. Each certificate type above is closed under exact re-checking: a
Farkas vector either certifies infeasibility against the exact system or it does
not, with no tolerance to tune.

## The solver-audit lesson

The hardest trust lessons here came from *infeasibility* claims, which are
exactly the claims that change public status. The lesson, stated once:

> An exact simplex does not save you from a constraint that was rounded while the
> LP file was *parsed*.

`glpsol --exact` switches to exact rational arithmetic — but only *after* the
LP/MPS reader has turned the input text into numbers. When coefficients are large
(as they are for high-weight enumerators), a value can be rounded at that parse
step, before exact arithmetic ever sees it. The solver then computes an exact
answer to the wrong problem, and an "infeasible" verdict can be an artifact of
the reader, not a property of the code.

This is not hypothetical: it is why we now require exact input reconstruction,
exact Farkas certificates, or guarded exports (no value passing through a
float-printing reader) before any kill counts — and why a row is reinstated, not
quietly kept, the moment a verdict's input cannot be reconstructed exactly. Past
results have been retracted and later reinstated on exactly this basis; we keep
that history visible on the [Audit Trail](audit-trail.md) as a lesson, not a
footnote.

The same caution applies one floor up, to SDP. A numerical SDP that sits *on*
its feasibility boundary — margin `≈ 0` — is **not proof-grade**. It is a strong
hint that the constraint is tight, and a good reason to invest in an exact
certificate, but on its own it neither kills a row nor closes a branch. `T29` is
in exactly this state: real, suggestive, and explicitly **open**.

## Run it, then argue with it

Reproduce every 🟢 bundle in one command from the reproduction bundle:

```sh
python3 repro/verify_all.py
```

It runs each bundle's verifier and reports `PASS`/`FAIL` (`9/9` reproduced).
Add `--all` to attempt the 🟡 solver tier as well.

Found a rounding hazard, a tighter certificate, or a verifier that disagrees with
us? That is the most valuable kind of contribution. Bring it to the
**#extremal72** channel of the Error Correction Zoo Discord:
<https://discord.gg/gg3pJZNYxQ>.
