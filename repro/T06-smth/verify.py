#!/usr/bin/env python3
"""
T06 -- toggle-stabilizer Smith congruence: exact-replayable verifier.

Reproduces, with EXACT integer arithmetic and NO solver, the divisibility kill of
section 15.1: at k=6 the three-block toggle-stabilizer congruence system is
integer-INFEASIBLE exactly when a is even, killing the 16 even-a rows.

Input (certificate): `system.json` -- for each a in 0..31, the toggle-stabilizer
congruence system in the two free counts (m, n):

    B*m + C*n  ==  target   (mod  mod)      for each orbit.

It was generated once by the real Sage three-block setup
(`the project's solver`); this verifier re-checks integer feasibility from
scratch with its own Smith-normal-form solvability test (no shared code).

Decision rule reproduced:  a even  ->  INFEASIBLE (kill);  a odd  ->  feasible.

Run:  python3 verify.py        (pure Python standard library)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def integer_solvable(rows, rhs):
    """True iff the integer system  A x = b  has a solution over Z.

    Diagonalises A by unimodular row/column operations (tracking b under the row
    operations only -- column operations are variable substitutions and preserve
    solvability), then checks the per-row divisibility.  No divisibility chain is
    needed: any unimodular U,V with U A V = D diagonal gives
    A x = b  <=>  D y = U b, solvable iff each (U b)_i is divisible by D_ii
    (or zero where D_ii = 0)."""
    M = [list(map(int, r)) for r in rows]
    if not M:
        return True
    m = len(M)
    n = len(M[0])
    c = list(map(int, rhs))

    def rowswap(i, j):
        M[i], M[j] = M[j], M[i]
        c[i], c[j] = c[j], c[i]

    def rowadd(i, j, f):  # row i += f * row j
        Mi, Mj = M[i], M[j]
        for k in range(n):
            Mi[k] += f * Mj[k]
        c[i] += f * c[j]

    def colswap(i, j):
        for r in range(m):
            M[r][i], M[r][j] = M[r][j], M[r][i]

    def coladd(i, j, f):  # col i += f * col j
        for r in range(m):
            M[r][i] += f * M[r][j]

    t = 0
    while t < min(m, n):
        # pick the smallest-magnitude nonzero entry in the active submatrix
        piv = None
        for i in range(t, m):
            for j in range(t, n):
                if M[i][j] != 0 and (piv is None or abs(M[i][j]) < abs(M[piv[0]][piv[1]])):
                    piv = (i, j)
        if piv is None:
            break
        rowswap(t, piv[0])
        colswap(t, piv[1])
        cleared = False
        while not cleared:
            cleared = True
            for i in range(t + 1, m):
                if M[i][t]:
                    rowadd(i, t, -(M[i][t] // M[t][t]))
                    if M[i][t]:
                        rowswap(t, i)
                        cleared = False
            for j in range(t + 1, n):
                if M[t][j]:
                    coladd(j, t, -(M[t][j] // M[t][t]))
                    if M[t][j]:
                        colswap(t, j)
                        cleared = False
        t += 1

    for i in range(m):
        d = M[i][i] if i < n else 0
        if d:
            if c[i] % d != 0:
                return False
        elif c[i] != 0:
            return False
    return True


def system_matrix(congruences):
    """B*m + C*n == target (mod mod)  ==>  rows  [B, C, ...mod at slack idx...] = target."""
    nc = len(congruences)
    rows, rhs = [], []
    for idx, (B, C, mod, target) in enumerate(congruences):
        row = [B, C] + [0] * nc
        row[2 + idx] = mod
        rows.append(row)
        rhs.append(target)
    return rows, rhs


def main():
    data = json.load(open(os.path.join(HERE, "system.json")))
    systems = data["systems"]
    killed_even, feasible_odd, anomalies = [], [], []
    for a_str, sysd in sorted(systems.items(), key=lambda kv: int(kv[0])):
        a = int(a_str)
        rows, rhs = system_matrix(sysd["congruences"])
        feasible = integer_solvable(rows, rhs)
        if a % 2 == 0:
            (feasible_odd if feasible else killed_even).append(a)  # even should be infeasible
            if feasible:
                anomalies.append(("even-but-feasible", a))
        else:
            if feasible:
                feasible_odd.append(a)
            else:
                anomalies.append(("odd-but-infeasible", a))

    even_killed = sorted(a for a in range(0, 32, 2)
                         if not integer_solvable(*system_matrix(systems[str(a)]["congruences"])))
    odd_feasible = sorted(a for a in range(1, 32, 2)
                          if integer_solvable(*system_matrix(systems[str(a)]["congruences"])))

    print("T06 toggle-stabilizer congruence system, k=6:")
    print(f"  even a INFEASIBLE (killed): {even_killed}")
    print(f"  odd  a feasible (survive) : {odd_feasible}")
    assert even_killed == list(range(0, 32, 2)), "all 16 even-a rows must be infeasible"
    assert odd_feasible == list(range(1, 32, 2)), "all 16 odd-a rows must be feasible"
    assert not anomalies, f"anomalies: {anomalies}"
    print(f"OK: exactly the 16 even-a k=6 rows are killed by toggle-stabilizer divisibility "
          f"({len(even_killed)} kills); odd-a rows survive. Reproduces section 15.1.")
    json.dump({"k": 6, "killed_even_a": even_killed, "survive_odd_a": odd_feasible,
               "n_kills": len(even_killed)},
              open(os.path.join(HERE, "result.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
