#!/bin/sh
# T32 reproduction entrypoint. Re-certifies every stored route-3A witness from
# scratch (expand l-vector -> 2^k codewords -> check weights / doubly-even /
# 1_40 in E / full rank / Parseval). Exits 0 iff all witnesses pass. Pure Python.
cd "$(dirname "$0")" && exec python3 verify_witnesses.py
