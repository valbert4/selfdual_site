# T08 reproduction bundle — Johnson/Delsarte two-point bound

**Tier:** 🟢 exact-replayable (pure Python standard library, no solver)

**Claim reproduced:** the length-40 menu row `(k=9, a=255, b=0)` is empty. With
`b = 0` the weight-16 supports form a 2-distance constant-weight code in the
Johnson scheme `J(40,16)` (intersections `{4,8}`), whose exact Delsarte LP bound
is `247`. Since the row needs `a = 255 > 247`, no such code exists.

**Run**

    sh run.sh        # or: python3 verify.py

Exits `0` iff the exact bound `247` and the kill are reproduced; writes
`result.json`.

**How it is exact without an LP solver.** `verify.py` builds the second
eigenmatrix `Q` of `J(40,16)` from the Eberlein eigenvalues with an exact
rational matrix inverse, then solves the 2-variable Delsarte LP by exact vertex
enumeration (every optimum of a 2-D LP is a vertex). The arithmetic is
`fractions.Fraction` throughout, so the bound `247` is exact, not numerical.

**Original solver (optional):** the reproduction bundle computes the
same bound with Sage + PPL. This bundle does not need it.

**Inputs:** the kill row `(9,255,0)` is one of the 132 length-40 menu candidates
from T01 (see the Enumerators / Menu tabs). The scheme `J(40,16)` is fixed by the
problem (length 40, weight 16).
