#!/usr/bin/env python3
"""Internal-link checker for the Extremal 72 static site.

Every page sets a <base> to the site root, so internal links are resolved
relative to the site root. This script extracts href/src targets and the
data/*.json link fields, resolves them against the site root, and fails if any
internal target is missing. External (http/https/mailto), in-page (#...), and
the intentional `../` redirect are skipped.

Usage:  python check_links.py        (exit 0 = all internal links resolve)
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
SCRIPT_RE = re.compile(r"<script\b.*?</script>", re.S | re.I)


def is_internal(u):
    return not (u.startswith(("http://", "https://", "//", "#", "mailto:", "data:")))


def resolve(u):
    """Site-root-relative path (links resolve against <base> = site root)."""
    u = u.split("#", 1)[0].split("?", 1)[0]
    u = u.lstrip("/")
    return os.path.normpath(os.path.join(ROOT, u)) if u else ROOT


def check(label, links, missing):
    for u in links:
        if not u or not is_internal(u) or u in ("../", "./", ""):
            continue
        target = resolve(u)
        ok = os.path.exists(target) or (
            os.path.isdir(target) and os.path.exists(os.path.join(target, "index.html")))
        if not ok:
            missing.append((label, u))


def main():
    missing = []
    htmls = ([os.path.join(ROOT, "index.html"), os.path.join(ROOT, "prototype", "index.html")]
             + glob.glob(os.path.join(ROOT, "content", "**", "*.html"), recursive=True))
    for h in htmls:
        if not os.path.exists(h):
            continue
        rel = os.path.relpath(h, ROOT)
        html = SCRIPT_RE.sub("", open(h, encoding="utf-8").read())
        check(rel, LINK_RE.findall(html), missing)

    # data JSON link fields (the dashboard fetches these)
    for name, key, field in [("data/tests.json", "tests", "page"),
                             ("data/enumerators.json", "enumerators", "file")]:
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            rows = json.load(open(p)).get(key, [])
            check(name, [r.get(field, "") for r in rows], missing)

    n = len(htmls)
    if missing:
        print(f"FAIL: {len(missing)} broken internal link(s) across {n} pages:")
        for label, u in missing[:50]:
            print(f"  {label}: {u}")
        sys.exit(1)
    print(f"OK: all internal links resolve ({n} pages checked).")


if __name__ == "__main__":
    main()
