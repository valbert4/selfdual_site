#!/usr/bin/env python3
"""Render the Extremal 72 Markdown content to a static HTML site.

Uses pandoc (GFM -> html5). Writes a .html next to every content/*.md, rewrites
internal .md links to .html, and generates a landing index.html at the site root.
The existing `python3 -m http.server` rooted at website/ then serves it.
"""
import glob
import gzip
import hashlib
import os
import re
import subprocess
import tarfile

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")

# Paths are base-relative (no leading slash); a per-page <base> tag (injected by
# page() below) makes them resolve against the site root, so the site works at a
# domain root OR a project sub-path (e.g. /extremal72/).
NAV = [
    ("Dashboard", "index.html"),
    ("Current Map", "content/current-map.html"),
    ("Hierarchy", "content/hierarchy.html"),
    ("Menu", "content/menu-summary.html"),
    ("Tests", "content/tests/index.html"),
    ("Enumerators", "content/weight-enumerators-pipeline.html"),
    ("Validation", "content/audit-trail.html"),
    ("Ideas", "content/ideas-not-pursued.html"),
    ("Glossary", "content/glossary.html"),
]

LINK_RE = re.compile(r'href="(?!https?:|/|#|mailto:)([^"]+?)\.md(#[^"]*)?"')
H1_RE = re.compile(r"^#\s+(.*)$", re.M)
STATUS_RE = re.compile(r"^Status:\s*`([^`]*)`", re.M)


def navbar():
    links = "".join(f'<a href="{href}">{name}</a>' for name, href in NAV)
    return (
        '<header class="topbar"><div class="brand">'
        '<span class="brand-mark" aria-hidden="true">72</span>'
        '<div><p class="eyebrow">Extremal 72</p><h1>Research dossier</h1></div>'
        f'</div><nav class="docnav">{links}</nav></header>'
    )


def base_tag(depth):
    """First <head> element: auto-detect the site root from this page's location
    (which is `depth` directory levels below root) and write a <base>, so every
    relative URL resolves against the site root at any deploy path."""
    return (
        "<script>(function(){var d=%d,p=location.pathname.split(\"/\");"
        "p=p.slice(0,p.length-1-d);"
        "document.write('<base href=\"'+p.join(\"/\")+'/\">');})();</script>"
    ) % depth


def page(title, body, depth=1):
    return (
        "<!doctype html><html lang=en><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width, initial-scale=1">'
        + base_tag(depth)
        + f"<title>{title} - Extremal 72</title>"
        '<link rel=stylesheet href="prototype/styles.css?v=3">'
        '<link rel=stylesheet href="prototype/dark-skin.css?v=3">'
        '<link rel=stylesheet href="site.css?v=3"></head><body>'
        f'{navbar()}<main class="app-shell"><article class="doc">{body}</article></main>'
        '<footer class="doc-footer">Extremal 72 - static site. '
        "Status numbers mirror <code>data/menu-summary.yml</code>.</footer>"
        "</body></html>"
    )


ANY_LINK_RE = re.compile(r'((?:href|src)=)"([^"]+)"')
_EXTERNAL = ("http://", "https://", "//", "#", "mailto:", "data:")


def _to_site_root_relative(html, pagedir):
    """Make every in-content link site-root-relative so it resolves against the
    per-page <base> at any deploy path: page-directory-relative links get the
    page dir prefixed; leading-slash links lose the slash; externals untouched."""
    def repl(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(_EXTERNAL) or not url:
            return m.group(0)
        frag = ""
        if "#" in url:
            url, frag = url.split("#", 1)
            frag = "#" + frag
        if url.startswith("/"):
            new = url.lstrip("/")
        else:
            new = os.path.normpath(os.path.join(pagedir, url)).replace(os.sep, "/")
        return f'{attr}"{new}{frag}"'
    return ANY_LINK_RE.sub(repl, html)


def render_md(md_path, pagedir):
    out = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5", md_path],
        capture_output=True, text=True, check=True,
    ).stdout
    out = LINK_RE.sub(r'href="\1.html\2"', out)
    return _to_site_root_relative(out, pagedir)


def first_title(text, fallback):
    m = H1_RE.search(text)
    return m.group(1).strip() if m else fallback


def build_content():
    md_files = glob.glob(os.path.join(CONTENT, "**", "*.md"), recursive=True)
    for md in sorted(md_files):
        text = open(md, encoding="utf-8").read()
        title = first_title(text, os.path.basename(md))
        html_path = md[:-3] + ".html"
        rel = os.path.relpath(html_path, ROOT)
        # depth = directory levels below the site root (content/foo.html -> 1,
        # content/tests/Txx.html -> 2); pagedir = the page's dir relative to root.
        depth = len(rel.split(os.sep)) - 1
        pagedir = os.path.dirname(rel).replace(os.sep, "/")
        open(html_path, "w", encoding="utf-8").write(
            page(title, render_md(md, pagedir), depth))
    return md_files


def build_landing():
    start = [
        ("Current Map", "/content/current-map.html", "The short status view."),
        ("The Hierarchy", "/content/hierarchy.html", "72 - 56 - 40 - 24 descent."),
        ("Length-40 Menu", "/content/menu-summary.html", "The finite menu and counts."),
        ("Tests T01-T32", "/content/tests/index.html", "One page per exact test."),
        ("Weight Enumerators", "/content/weight-enumerators-pipeline.html", "Downloadable data."),
        ("Validation Standards", "/content/audit-trail.html", "What counts as proof-grade."),
        ("Ideas Not Pursued", "/content/ideas-not-pursued.html", "Parked and closed routes."),
        ("Interactive Dashboard", "/prototype/index.html", "The tabbed prototype UI."),
    ]
    cards = "".join(
        f'<a class="card" href="{h}"><div class="t">{t}</div><div class="d">{d}</div></a>'
        for t, h, d in start
    )

    # Test grid from the test markdown files.
    tcards = []
    for md in sorted(glob.glob(os.path.join(CONTENT, "tests", "T*.md"))):
        text = open(md, encoding="utf-8").read()
        tid_title = first_title(text, os.path.basename(md))
        sm = STATUS_RE.search(text)
        status = sm.group(1) if sm else ""
        href = "/content/tests/" + os.path.basename(md)[:-3] + ".html"
        cls = "tcard"
        if "kill" in status:
            cls += " kill"
        elif "open" in status or "critical" in status:
            cls += " open"
        # split "T01 - Title" into id + title
        parts = tid_title.split(" - ", 1)
        tid = parts[0]
        ti = parts[1] if len(parts) > 1 else ""
        tcards.append(
            f'<a class="{cls}" href="{href}"><span class="id">{tid}</span> '
            f'<span class="ti">{ti}</span><div class="st">{status}</div></a>'
        )
    tgrid = '<div class="testgrid">' + "".join(tcards) + "</div>"

    stats = (
        '<div class="statrow">'
        '<div class="stat"><b>132</b><span>raw shadows</span></div>'
        '<div class="stat"><b>60</b><span>eliminated</span></div>'
        '<div class="stat green"><b>72</b><span>surviving</span></div>'
        '<div class="stat"><b>51</b><span>witnessed</span></div>'
        '<div class="stat gold"><b>21</b><span>unresolved</span></div>'
        "</div>"
    )

    body = (
        "<h1>Extremal 72</h1>"
        '<p class="lede">A community search to decide whether a binary Type II '
        "<code>[72,36,16]</code> code exists - find it, or prove it cannot.</p>"
        + stats
        + "<h2>Start here</h2>"
        + f'<div class="cards">{cards}</div>'
        + "<h2>Tests T01-T32</h2>"
        + '<p class="lede">Every exact filter applied to the length-40 menu, '
        "one checkable page each.</p>"
        + tgrid
    )
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
        page("Home", body)
    )


def build_repro_bundles():
    """Tar each repro/T??-*/ bundle into downloads/repro/ with a sha256 manifest.

    Deterministic (mtime/uid zeroed, sorted entries, gzip mtime=0) so the
    checksum is stable across builds; generated outputs and caches are excluded.
    """
    import json as _json
    repro = os.path.join(ROOT, "repro")
    if not os.path.isdir(repro):
        return {}
    outdir = os.path.join(ROOT, "downloads", "repro")
    os.makedirs(outdir, exist_ok=True)
    skip_names = {"result.json", "verified_witnesses.json"}

    def keep(path):
        base = os.path.basename(path)
        return not ("__pycache__" in path or base in skip_names or base.endswith(".pyc"))

    manifest = {}
    for d in sorted(os.listdir(repro)):
        p = os.path.join(repro, d)
        if not (os.path.isdir(p) and os.path.exists(os.path.join(p, "run.sh"))):
            continue
        files = sorted(fp for fp in glob.glob(os.path.join(p, "**", "*"), recursive=True)
                       if os.path.isfile(fp) and keep(fp))
        tarpath = os.path.join(outdir, f"{d}-repro.tar.gz")
        with open(tarpath, "wb") as raw, \
                gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as gz, \
                tarfile.open(fileobj=gz, mode="w") as tf:
            for fp in files:
                ti = tf.gettarinfo(fp, arcname=os.path.join(d, os.path.relpath(fp, p)))
                ti.mtime = 0
                ti.uid = ti.gid = 0
                ti.uname = ti.gname = ""
                with open(fp, "rb") as fh:
                    tf.addfile(ti, fh)
        sha = hashlib.sha256(open(tarpath, "rb").read()).hexdigest()
        manifest[d] = {"file": f"downloads/repro/{d}-repro.tar.gz",
                       "sha256": sha, "files": len(files)}
    _json.dump(manifest, open(os.path.join(outdir, "manifest.json"), "w"), indent=2)
    print(f"packaged {len(manifest)} reproduction bundles -> downloads/repro/")
    return manifest


if __name__ == "__main__":
    # Note: the site root index.html is the card-based dashboard (a copy of
    # prototype/index.html with absolute asset paths), NOT generated here, so it
    # is never overwritten by a rebuild. This script only renders the Markdown
    # detail pages that the dashboard's cards link into.
    files = build_content()
    # The References tab fetches data/references.json (browsers can't parse YAML);
    # regenerate it from the YAML source of truth on every build.
    # The dashboard (tabs.js) fetches these JSON files; they are the single
    # source of truth's machine-readable form. Browsers can't parse YAML, so the
    # build regenerates JSON from the YAML/structured sources on every run.
    try:
        import yaml
        import json as _json

        def dump(obj, name):
            _json.dump(obj, open(os.path.join(ROOT, "data", name), "w"),
                       ensure_ascii=False, indent=0)

        refs = yaml.safe_load(open(os.path.join(ROOT, "data", "references.yml")))
        dump(refs, "references.json")

        ts = yaml.safe_load(open(os.path.join(ROOT, "data", "tests.yml")))["tests"]
        dump({"tests": [{
            "id": t["id"], "abbr": t["abbr"], "title": t["title"],
            "status": t["status"], "kills": t["kills"], "result": t["result"],
            "category": t.get("public_category", ""),
            "page": "content/tests/%s.html" % t["slug"],
        } for t in ts]}, "tests.json")

        ens = yaml.safe_load(open(os.path.join(ROOT, "data", "enumerators.yml")))
        dump(ens, "enumerators.json")
        print(f"wrote data/{{references,tests,enumerators}}.json "
              f"({len(refs['references'])} refs, {len(ts)} tests, "
              f"{len(ens['enumerators'])} enumerators)")
    except Exception as exc:  # noqa: BLE001
        print("data json generation skipped:", exc)
    build_repro_bundles()
    print(f"rendered {len(files)} content detail pages")
