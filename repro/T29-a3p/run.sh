#!/bin/sh
# T29 moment-matrix assembly: exact-replayable (pure Python standard library).
# Rebuilds the 5 PSD blocks and certifies the pair_type -> (block,row,col) map.
# Exit 0 iff the published assembly is reproduced. (~30-60s: it enumerates the
# 109684 S3 triple orbits.) The final PSD margin verdict remains open.
exec python3 "$(dirname "$0")/verify.py"
