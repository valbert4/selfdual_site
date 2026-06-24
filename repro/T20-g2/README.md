# T20-g2 reproduction bundle

**Tier:** 🟢 exact-replayable (verifier is pure Python; certificate found once by the solver)

**Reproduces:** (9,239,32) proven infeasible — the coupled genus-2 family has no nonnegative point (Farkas-certified).

**Run**

    sh run.sh   # python3 verify.py

`verify.py` checks a Farkas certificate of infeasibility (`y >= 0`, `y^T G = 0`, `y^T h > 0`) against the exact integer system — pure Python, no solver. The certificate in `system.json`/`cert.json` was generated once by the real solver in `reproduce/` (Sage/PPL). Cross-checked against the solver.
