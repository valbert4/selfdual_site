#!/bin/sh
# Tier "solver-required": not a one-click pure-Python check in this bundle.
# The classification itself is exact and pure-Python in the research repo.
echo "Result: D32 is the unique [32,k-4] sibling (subcode of RM(1,5) containing 1_32); W = 1 + (2^(k-4)-2) y^16 + y^32; saturates (no new menu kill)"
echo "Reproduce: research repo classification/d32_sibling/ -- python3 classify_d32.py --selftest (pure Python; no Sage/GAP)"
