# T32 reproduction bundle — route-3A direct existence (witness side)

**Tier:** 🟢 exact-replayable (pure Python standard library, no solver)

**Claim reproduced:** the menu rows recorded as *nonempty* genuinely are — each
is realized by an explicit `[40,k,16]` doubly-even self-orthogonal code
containing `1₄₀`. This is the constructive (`✔️`) side of T32.

**Run**

    sh run.sh        # or: python3 verify_witnesses.py

Walks every stored witness (`results/witness_l/*.txt`, `results/witness_k8.json`,
`results/k9_unfold/leaves.txt`), expands each `l`-vector to its `2^k` codewords,
and checks: weights ⊆ `{0,16,20,24,40}`, doubly-even ⟹ self-orthogonal,
`1₄₀ ∈ E`, full rank `k`, `A₁₆ = A₂₄ = a`, `2 + 2a + b = 2^k`, and the Parseval
identity `sq·2^k = (a+25)·128`. Exits `0` iff all pass; writes
`results/verified_witnesses.json`. Expected: **1528 witnesses, 0 failures, 27
distinct realized rows**.

**Independence.** The verifier shares no code with the search engine beyond
`affine.py` (the `l`-vector → codeword expansion). It is the independent
certification path.

**Note on the bug fix.** The upstream `verify_witnesses.py` used
`sq * (1 << (k-7))`, which raises `negative shift count` on the `k=6` witnesses.
This bundle clears the shift by checking `sq·2^k == (a+25)·128`, exact for all
`k`. (Worth upstreaming.)

**Inputs:** the witness `l`-vectors in `results/` are the actual codes found by
the route-3A engine — the constructive data behind the "51 witnessed nonempty"
count on the Menu tab.

**Out of scope here:** the *empty* proof for `(6,29,4)` is a ~68-billion-node
exhaustion (the C++ `unfold` engine), not a one-click reproduction; it ships
separately with a seed + leaf-count certificate.
