#!/bin/sh
# T06 reproduction entrypoint. Re-checks integer feasibility of the k=6
# toggle-stabilizer congruence systems (system.json) and confirms the 16 even-a
# rows are infeasible. Pure Python standard library; no solver.
exec python3 "$(dirname "$0")/verify.py"
