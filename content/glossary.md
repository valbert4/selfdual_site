# Glossary

Short, working definitions for the terms used across the site. Each is the
sense in which this project uses the term, not a full textbook treatment.

- **Type II code** — a binary linear code that is both self-dual and doubly-even.
  Type II codes exist only when the length is a multiple of 8. The target
  `[72,36,16]` is the hypothetical extremal Type II code of length 72.

- **Self-dual code** — a code `C` equal to its own dual, `C = C^⊥`, under the
  standard inner product. A self-dual `[n,k]` code has `k = n/2`.

- **Doubly-even code** — a code in which every codeword has Hamming weight
  divisible by 4. (Doubly-even self-dual = Type II.)

- **Weight enumerator** — the polynomial
  `W_C(x,y) = Σ_{c ∈ C} x^{n - wt(c)} y^{wt(c)}`, recording how many codewords
  have each weight. For an extremal Type II code the weight enumerator is forced
  uniquely (here `A_16 = 249849`, etc.).

- **MacWilliams identities** — the linear relations that determine the weight
  enumerator of the dual `C^⊥` from that of `C`. For a self-dual code they become
  a self-equation the enumerator must satisfy. Higher-genus versions (biweight,
  triweight) constrain the joint enumerators of tuples of codewords.

- **Residual code** — the code obtained by *shortening*: fix the coordinates on
  the support of a chosen codeword (here a weight-16 word), keep the codewords
  that are zero there, and restrict to the complementary coordinates. Anchoring a
  weight-16 word of the `[72,36,16]` code forces a `[56,21,≥16]` residual.

- **Construction A** — the lattice built from a binary code,
  `Λ = (1/√2){x ∈ Z^n : x mod 2 ∈ C}`. It is even unimodular when `C` is
  doubly-even self-dual. Note: its minimum norm is 2, so for length ≥ 24 it is
  *not* extremal (see [Ideas Not Pursued](ideas-not-pursued.md)).

- **CSS code** — a Calderbank–Shor–Steane quantum error-correcting code built
  from classical binary codes with `C_2 ⊆ C_1` (a self-dual classical code gives
  a self-dual CSS package). The exact object obtained from a `[72,36,16]` code is
  a payoff still to be written down precisely.

- **Delsarte LP** — the linear-programming bound on codes and designs, using
  positivity of the dual (Krawtchouk / Eberlein) expansion in an association
  scheme (Hamming or Johnson). The first relaxation layer used here.

- **Terwilliger / Schrijver SDP** — semidefinite-programming strengthenings of
  the Delsarte LP that add 3-point (and higher) configuration constraints via the
  Terwilliger algebra. Tighter than the LP, much heavier to solve exactly.

- **Farkas certificate** — an exact dual vector that, by Farkas' lemma, proves a
  linear system has no nonnegative solution. A proof-grade witness that a
  configuration is impossible — the standard this project requires before a menu
  row is publicly eliminated.

- **Canonical augmentation** — an isomorph-free exhaustive generation method
  (McKay): build objects up one step at a time while rejecting duplicates by
  comparing against a canonical form, so each isomorphism class is produced once.
