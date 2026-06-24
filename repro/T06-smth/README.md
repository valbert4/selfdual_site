# T06 reproduction bundle — toggle-stabilizer Smith congruence

**Tier:** 🟢 exact-replayable (verifier is pure Python; certificate generated once by Sage)

**Claim reproduced:** at `k = 6`, the three-block toggle-stabilizer congruence
system is integer-**infeasible** exactly when `a` is even — killing the 16 even-a
rows (section 15.1).

**Run**

    sh run.sh        # or: python3 verify.py

`verify.py` reads `system.json` and re-checks integer feasibility of each k=6
system with its own Smith-normal-form solvability test, then asserts the 16
even-a systems are infeasible and the 16 odd-a systems are feasible. Exits `0`
iff so; writes `result.json`. Pure Python standard library — no solver.

**The certificate.** `system.json` holds, for each `a ∈ 0..31`, the
toggle-stabilizer congruence system in the two free counts `(m, n)`:
`B·m + C·n ≡ target (mod mod)` per orbit. It was generated once by the real Sage
three-block setup — `reproduce/dump_t06.py` runs the upstream construction
(`reproduce/three_block_macwilliams.sage.py`) and dumps the integer systems. The
verifier shares **no code** with that construction.

**Independently validated.** The pure-Python solvability test was cross-checked
against Sage's `smith_form` on all 32 systems — **zero mismatches**.

**Regenerate the certificate (optional, needs Sage):**

    sage -python reproduce/dump_t06.py     # rewrites ../system.json

**Inputs:** the systems are derived from the forced n=72 Gleason enumerator and
the three-block split at a disjoint weight-16 pair (the data behind the Menu /
Enumerators tabs).
