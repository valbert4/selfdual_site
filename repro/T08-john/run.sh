#!/bin/sh
# T08 reproduction entrypoint. Exits 0 iff the Delsarte bound 247 and the
# (9,255,0) kill are reproduced exactly. Pure Python standard library; no solver.
exec python3 "$(dirname "$0")/verify.py"
