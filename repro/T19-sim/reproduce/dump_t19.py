# Generate the T19 certificate: the order-4 Farkas vector proving (6,1,60)
# infeasible. Uses Sage/PPL (via certify_kill.find_farkas) to FIND it; writes
# ../cert.json. The verifier re-checks it with no solver.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import support_weight_lib as L, orderk, certify_kill as C
k, a, b, n, r = 6, 1, 60, 40, 4
WE = [0]*(n+1); WE[0]=1; WE[16]+=a; WE[24]+=a; WE[20]+=b; WE[40]+=1
WEp = [int(x) for x in L.macwilliams_transform(WE, n, 2, 2**k)]
variables, eq_rows, ge_rows, _ = orderk.build_order_constraints(n, k, WE, WEp, r, True, True, True)
N, rows = C.ge_form(variables, eq_rows, ge_rows)
cert = C.find_farkas(N, rows)
assert cert and cert.get("found"), "no Farkas certificate found"
json.dump({"k": k, "a": a, "b": b, "n": n, "r": r, "y": cert["y"]},
          open(os.path.join(HERE, "..", "cert.json"), "w"))
print("dumped order-4 Farkas certificate with", len(cert["y"]), "multipliers")
