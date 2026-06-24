# Find an exact Farkas certificate of infeasibility for {G x >= h} (all rows >=).
# {G x >= h} is infeasible  iff  exists y >= 0 with y^T G = 0 and y^T h > 0.
# Usage: sage ppl_farkas.sage <in.json> <out.json>
#   in.json: {"nvars": N, "rows": [ [ [[j,coef],...], rhs ], ... ]}   (sum coef*x_j >= rhs)
#   out.json: {"found": bool, "y": {row_index: "p/q", ...}}
import json, sys
from collections import defaultdict

data = json.load(open(sys.argv[1]))
rows, N = data["rows"], data["nvars"]
p = MixedIntegerLinearProgram(solver="PPL")
y = p.new_variable(nonnegative=True, real=True)
for i in range(len(rows)):
    y[i]
col = defaultdict(list)
for i, (coeffs, rhs) in enumerate(rows):
    for j, c in coeffs:
        col[j].append((i, c))
for j in range(N):
    if col[j]:
        p.add_constraint(p.sum(Integer(c) * y[i] for i, c in col[j]) == 0)
p.add_constraint(p.sum(Integer(rhs) * y[i] for i, (coeffs, rhs) in enumerate(rows)) >= 1)
p.set_objective(None)
try:
    p.solve()
    vals = p.get_values(y)
    out = {"found": True, "y": {str(i): str(QQ(v)) for i, v in vals.items() if v != 0}}
except Exception as e:
    out = {"found": False, "err": str(e)}
json.dump(out, open(sys.argv[2], "w"))
