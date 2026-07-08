# The 72 -> 56 -> 40 -> 24 Hierarchy

The main idea pursued so far is to replace the full `[72,36,16]` search by a
sequence of forced residual shadows.

## Step 1: Anchor at 72

Assume a Type II `[72,36,16]` code `C` exists. It has `249849` weight-16
codewords. Choose one and call its support `B`.

This does not lose generality for a proof attempt: every candidate code has
many such words.

## Step 2: The Forced 56-Point Residual

Shorten on the anchor:

```text
C_B = { x restricted to B^c : x in C and x_B = 0 }.
```

The forced residual is a doubly-even self-orthogonal `[56,21,16]` code
containing the all-ones word, with exactly `5082` weight-16 words.

This residual is the first major narrowing of the problem.

## Step 3: The Length-40 Menu

Choose a residual weight-16 word and shorten again. The resulting length-40
child `E` is a doubly-even self-orthogonal `[40,k,>=16]` code containing the
all-ones word.

Its weight enumerator has the constrained form:

```text
W_E(y; a,b) = 1 + a(y^16 + y^24) + b y^20 + y^40.
```

The repo calls each possible `(k,a,b)` a menu row.

## Step 4: The Rigid 24-Point Bottom Rung

The next residual bottom rung is rigid:

```text
[24,1,24]
```

This is why the hierarchy is finite and why the length-40 menu is such a useful
public artifact.

## What This Means

The project is not a blind search over all length-72 codes. It is an attempt to
force every hypothetical code to cast one of a small number of residual shadows,
then either realize that shadow or prove it impossible.
