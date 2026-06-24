# Extremal 72

**Searching for a binary Type II `[72,36,16]` self-dual code** — an open,
community-verifiable search to decide whether this code exists.

- **Find it**, and we get the next extremal binary Type II code after the
  length-24 Golay and length-48 quadratic-residue codes, with a forced weight
  enumerator (`A_16 = 249849`), a `5-(72,16,78)` design, a code CFT at central
  charge `c = 36`, and a `[[71,1,≥15]]` self-dual CSS code.
- **Rule it out**, and we settle a question open since Sloane raised it in 1973.

The site makes the problem legible and the eliminations *checkable*: every
proof-grade kill ships an exact, independently re-runnable certificate.

## Quick status

`132` length-40 residual candidates `→ 60` eliminated (proof-grade) `→ 72`
surviving; of those, `51` are witnessed nonempty and `21` are unresolved
(not yet exhausted — *not* evidence of emptiness). All `8` proof-grade kills are
reproducible in pure Python with no solver.

## Build and serve

Requirements: Python 3.10+, `pandoc`, and PyYAML.

```sh
pip install -r requirements.txt
sudo apt-get install -y pandoc      # or: brew install pandoc
python build_site.py                # render content/ -> HTML, regenerate data/*.json, package repro bundles
python -m http.server 8000          # http://127.0.0.1:8000/
```

The site is base-path safe (a per-page `<base>` tag is auto-detected), so it
works at a domain root or a project sub-path like `/extremal72/`.

## Publish on GitHub Pages

This repository's CI workflow builds, verifies, link-checks, and deploys the
static site to GitHub Pages on every push to `main`.

One-time GitHub setup: in the repository, go to **Settings -> Pages** and set
**Build and deployment -> Source** to **GitHub Actions**. After the next push to
`main`, the site will publish at `https://valbert4.github.io/selfdual_site/`
unless the repository is renamed or a custom domain is configured.

## Verify the proof-grade results yourself

```sh
python repro/verify_all.py          # exact-replayable bundles, pure Python, no solver
python check_links.py               # internal-link check
```

Each test ships a reproduction bundle under `repro/`. The 🟢 bundles cover all
`8` proof-grade kills plus the menu re-enumeration, each backed by an exact
Farkas/Smith certificate, an exact bound, or an exhaustive witness.

## Layout

| Path | What |
|---|---|
| `index.html`, `prototype/` | the dashboard (tabbed UI + styles + `tabs.js`) |
| `content/` | Markdown pages (rendered to HTML by `build_site.py`) |
| `data/` | structured sources of truth (`*.yml`); the build emits matching `*.json` |
| `repro/` | per-test reproduction bundles + `verify_all.py` |
| `downloads/` | self-contained enumerator / genus-3 / triweight data and bundles |
| `build_site.py`, `check_links.py` | the static build and link checker |

Edit the YAML/Markdown sources, not the generated JSON/HTML.

## Contributing & discussion

See [CONTRIBUTING.md](CONTRIBUTING.md). Discussion happens in the **#extremal72**
channel of the Error Correction Zoo Discord:
<https://discord.gg/gg3pJZNYxQ>.

## License & citation

Code is under the [MIT License](LICENSE); prose and data are additionally
offered under CC-BY-4.0. If you use the project or its certificates, please cite
it (see [CITATION.cff](CITATION.cff)).
