# Exact rational LP feasibility via PPL, reading EXACT integer coefficients from
# JSON (arbitrary-precision Python ints -> Sage Integer, no double round-trip).
# Usage:  sage ppl_solver.sage  <in.json>  <out.json>
# in.json: [ {"vars":[...], "rows":[ [ [[var,coef],...], rhs, "eq"|"ge" ], ... ]}, ... ]
# out.json: [true|false, ...]   (feasible?)  -- one per problem.
import json, sys

inp, outp = sys.argv[1], sys.argv[2]
problems = json.load(open(inp))
results = []
for prob in problems:
    allvars = list(prob["vars"])
    p = MixedIntegerLinearProgram(solver="PPL")
    x = p.new_variable(nonnegative=True, real=True)
    for key in allvars:
        x[key]                                  # instantiate
    for coeffs, rhs, op in prob["rows"]:
        expr = p.sum(Integer(c) * x[v] for v, c in coeffs)
        if op == "eq":
            p.add_constraint(expr == Integer(rhs))
        else:
            p.add_constraint(expr >= Integer(rhs))
    p.set_objective(None)                       # pure feasibility
    try:
        p.solve()
        results.append(True)
    except Exception:
        results.append(False)
json.dump(results, open(outp, "w"))
