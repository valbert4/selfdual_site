# T05-3bnn reproduction bundle

**Tier:** 🟢 exact-replayable (verifier is pure Python; certificate found once by the solver)

**Reproduces:** all 7 high-a k=10 rows killed by exact three-block nonnegativity (Farkas-certified).

**Run**

    sh run.sh   # python3 verify.py

`verify.py` checks a Farkas certificate of infeasibility (`y >= 0`, `y^T G = 0`, `y^T h > 0`) against the exact integer system — pure Python, no solver. The certificate in `system.json`/`cert.json` was generated once by the real solver in `reproduce/` (Sage/PPL). Cross-checked against the solver.
