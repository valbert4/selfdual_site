# Contributing to Extremal 72

This is a community-verifiable search for a binary Type II `[72,36,16]` code.
The guiding rule: **a status change needs exact input and an independently
checkable certificate.** Numerical evidence is welcome as a scout, but it does
not move the public menu or test ledger by itself.

Discussion happens in the **#extremal72** channel of the Error Correction Zoo
Discord: <https://discord.gg/gg3pJZNYxQ>. Say what you are about to run there so
two people don't exhaust the same row.

## Build the site locally

Requirements: Python 3.10+, `pandoc` (system package), and PyYAML.

```sh
sudo apt-get install -y pandoc      # or: brew install pandoc
pip install -r requirements.txt
python build_site.py                # renders content/ -> HTML, regenerates data/*.json, packages repro bundles
python -m http.server 8000          # serve at http://127.0.0.1:8000/
```

The site is base-path safe (a `<base>` tag is auto-detected per page), so it works
at a domain root or a project sub-path like `/extremal72/`.

## Source of truth

- Page content lives in `content/**/*.md` (rendered by `build_site.py`).
- Structured data lives in `data/*.yml` (`tests.yml`, `enumerators.yml`,
  `references.yml`, `menu-summary.yml`). The build regenerates the matching
  `data/*.json` that the dashboard fetches — **edit the YAML, not the JSON or the
  hardcoded copies.**
- Do not introduce local machine paths (absolute home-directory paths) or
  internal repository directory names into served files; keep public artifacts
  self-contained.

## Reproduction bundles and the certificate standard

Every test ships a bundle under `repro/T??-*/`. A bundle has a `verify.py` (the
part that must run everywhere), an `expected.json` (tier + claim), and optionally
the original solver under `reproduce/`. Tiers:

- 🟢 **exact-replayable** — pure-Python standard library, exact arithmetic, no
  solver. Runs in CI on every commit. All proof-grade kills are here.
- 🟡 **solver-required** — needs an exact solver (PPL / Sage / `glpsol --exact`).
- 🔴 **cluster / open** — ships a spec, not a one-click run (e.g. the anchored SDP `T29`).

Run the green tier:

```sh
python repro/verify_all.py          # 9/9 must pass
```

To add or upgrade a certificate, prefer the certificate-plus-verifier pattern:
generate an exact certificate once with whatever solver you like, then ship a
small pure-Python `verify.py` that re-checks it (a Farkas vector, a Smith-form
witness, an exact bound, or an exhaustive enumeration) against published,
checksum-pinned data. New `T??-*/` bundles are picked up automatically by
`verify_all.py` and the build.

## CI

Pull requests run `.github/workflows/ci.yml`: install deps, `build_site.py`,
`repro/verify_all.py`, and `check_links.py` (internal link check). Keep all three
green.

## Pull-request checklist

- [ ] Edited the YAML/Markdown source, not generated JSON/HTML.
- [ ] `python build_site.py`, `python repro/verify_all.py`, and
      `python check_links.py` all pass.
- [ ] No local paths or internal repo directory names in any served file.
- [ ] Any new elimination ships an independently checkable certificate.
