# T33-d32 reproduction bundle

**Tier:** 🟡 solver-required

**Result:** D32 is the unique [32,k-4] subcode of RM(1,5) containing 1_32; its enumerator is W = 1 + (2^(k-4)-2) y^16 + y^32. Saturates (no new menu kill).

The classification is exact and pure-Python in the research repo: `classification/d32_sibling/` (`python3 classify_d32.py --selftest`; no Sage/GAP needed).
