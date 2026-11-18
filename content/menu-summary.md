# The Length-40 Menu

The length-40 menu is the public ledger of the residual search.

Every hypothetical `[72,36,16]` Type II code casts one of these length-40
shadows:

```text
E = [40,k,>=16], doubly-even, self-orthogonal, 1_40 in E.
```

The weight enumerator is:

```text
W_E(y; a,b) = 1 + a(y^16 + y^24) + b y^20 + y^40.
```

## Current Counts

```text
132 raw candidates
60 eliminated by exact obstructions
72 surviving at the menu level
52 witnessed nonempty
20 not yet exhausted
```

## How To Read These Numbers

- `132` is the complete arithmetic menu from the current exact validity filter.
- `60` rows have proof-grade eliminations.
- `72` rows remain viable as shadows.
- `52` surviving rows have explicit length-40 witnesses.
- `20` rows are unresolved: not witnessed and not fully exhausted.

A surviving row is not a `[72,36,16]` code. It is a compatible shadow.

## C_5 Sub-Menu (Automorphism-Conditional Tag)

The menu makes **no assumption** about the code's automorphism group. A series of
papers narrows that group to one of five — `C_1` (trivial), `C_2`, `C_3`,
`C_2×C_2`, or `C_5` — but the trivial group `C_1` imposes no structure and is the
hardest case, so every test here must hold for it. (See the Overview for the
exclusion citations.)

One branch still leaves a clean fingerprint on the menu. For `C_5`, orbit
counting (`A_16 = 249849 ≡ 4` and the `5082 ≡ 2 (mod 5)` residual partners) forces
a `σ`-fixed disjoint anchor pair whose length-40 residual carries a
fixed-point-free `C_5` action, so its menu row satisfies **`a ≡ 0 (mod 5)`**.

So a `C_5`-symmetric code must realize one of these **16 surviving rows**
(`a ≡ 0 mod 5`; 14 core rows plus the two reinstated `(7,15,96)`, `(8,55,144)`):

```text
k=6:  (5,52)   (15,32)   (25,12)
k=7:  (15,96)  (25,76)   (35,56)  (45,36)  (55,16)
k=8:  (55,144) (75,104)  (95,64)  (115,24)
k=9:  (135,240)(175,160) (215,80)
k=10: (295,432)
```

**Refinement (2026-11-18).** A computation in the research repository
(`gluing/c5_d56/`, not yet a replayable bundle) narrows this to **4 rows**. A
`C_5`-symmetric code has fixed part `e_8 ⊕ e_8`, so the second residual of a
`σ`-fixed disjoint anchor pair has fixed part `{0, x, y, x+y}` and dimension 6 or
10, and an exhaustive search of the fixed-point-free `C_5` codes leaves only
`(6,5,52)`, `(6,15,32)`, `(6,25,12)` and `(10,295,432)`. All four are witnessed
nonempty as length-40 codes, so eliminating them needs a test that uses the
length-72 parent, not an existence exhaust.

**What the tag means.** If automorphism-agnostic tests eliminate *all* of these,
the `C_5` branch closes with no Hermitian `F_16` search — a far cheaper target
than killing the whole menu. The converse does **not** hold: ruling out `C_5`
does not remove these rows, since a trivial-automorphism code could still cast
any of them. The tag marks where the `C_5` branch overlaps the menu; it is not a
kill.
