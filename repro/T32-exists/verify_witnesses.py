"""verify_witnesses.py -- re-verify EVERY saved shape-code witness from scratch.

Walks results/witness_l/*.txt (l-vectors; filename gives k via k{K}_...) plus the
canonical single witnesses (k9_unfold/leaves.txt, witness_k8.json), and for each:
expand l -> all 2^k codewords -> check  (i) weights subset of {0,16,20,24,40},
(ii) doubly-even => self-orthogonal, (iii) 1_40 in E, (iv) full rank k,
(v) A16 = A24 = a, 2 + 2a + b = 2^k, (vi) Parseval  sum l^2 = (a+25)/2^{k-7}.
This is the independent certification path (no engine code shared beyond affine.py).

Writes results/verified_witnesses.json: per file, k, (a,b), sum l^2.
Run:  /usr/bin/python3 verify_witnesses.py
"""

from __future__ import annotations
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import affine as A


def verify(k, l):
    P = A.Params(40, k, (16, 20, 24))
    assert len(l) == P.npts, (len(l), P.npts)
    assert sum(l) == 40 and all(x >= 0 for x in l)
    words = A.l_to_codewords(P, l)
    assert len(set(words)) == 1 << k, "full rank"
    we = Counter(bin(w).count("1") for w in words)
    assert set(we) <= {0, 16, 20, 24, 40}, dict(we)
    assert all(v % 4 == 0 for v in we), "doubly-even"
    assert ((1 << 40) - 1) in words, "1_40 in E"
    a, b = we[16], we[20]
    assert we[24] == a and 2 + 2 * a + b == (1 << k)
    sq = sum(x * x for x in l)
    # Parseval: sq * 2^(k-7) - 25 == a.  Cleared of the negative shift (k<7) by
    # multiplying through by 2^7 so it is integer-exact for every k:
    #   sq * 2^k == (a + 25) * 128.
    assert sq * (1 << k) == (a + 25) * 128, "Parseval"
    return a, b, sq


def main():
    out = {}
    nfail = 0
    # canonical single witnesses
    l9 = list(map(int, open(os.path.join(HERE, "results/k9_unfold/leaves.txt")).read().split()))
    out["k9_unfold/leaves.txt"] = dict(zip(("a", "b", "sq"), verify(9, l9)))
    wj = json.load(open(os.path.join(HERE, "results/witness_k8.json")))
    for idx in ("2", "3"):
        out[f"witness_k8.json#{idx}"] = dict(zip(("a", "b", "sq"),
                                                 verify(8, wj["witnesses"][idx]["l"])))
    # the probe/grid witness files
    for path in sorted(glob.glob(os.path.join(HERE, "results/witness_l/*.txt"))):
        base = os.path.basename(path)
        m = re.match(r"k(\d+)_", base)
        if not m:
            continue
        k = int(m.group(1))
        txt = open(path).read().split()
        if not txt:
            continue                                  # empty file (no leaf found)
        npts = 1 << (k - 1)
        for off in range(0, len(txt), npts):          # files may hold several leaves
            l = list(map(int, txt[off:off + npts]))
            if len(l) < npts:
                break
            try:
                a, b, sq = verify(k, l)
                key = base if off == 0 else f"{base}+{off // npts}"
                out[key] = {"a": a, "b": b, "sq": sq}
            except AssertionError as e:
                nfail += 1
                print(f"FAIL {base}@{off // npts}: {e}")
    rows = Counter()
    for rec in out.values():
        k = None
    # summarize realized rows per k
    byk = {}
    for name, rec in out.items():
        mk = re.search(r"k(\d+)", name)
        kk = int(mk.group(1))
        byk.setdefault(kk, set()).add((rec["a"], rec["b"]))
    summary = {f"k{kk}": sorted(v) for kk, v in sorted(byk.items())}
    with open(os.path.join(HERE, "results/verified_witnesses.json"), "w") as f:
        json.dump({"witnesses": out, "realized_rows": {k: [list(t) for t in v]
                                                       for k, v in summary.items()}},
                  f, indent=1)
    print(f"{len(out)} witnesses verified, {nfail} failures")
    for kk, v in summary.items():
        print(f"  {kk}: realized rows {v}")


if __name__ == "__main__":
    main()
