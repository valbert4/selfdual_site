# Tab-Based GUI Sketch

The site can use a tab-based interface without becoming a heavy web app.

The goal is progressive disclosure:

- first tab: readable public summary;
- second tab: current status and numbers;
- third tab: technical details;
- fourth tab: source/provenance;
- fifth tab: how to help.

This lets specialists reach the ledger quickly while keeping the first screen
usable for a broader mathematical audience.

## 1. Global Top-Level Tabs

Use a persistent top navigation with 6 primary tabs:

```text
Overview | Hierarchy | Menu | Tests | Enumerators | Contribute
```

Recommended mapping:

| Tab | Page | Purpose |
|---|---|---|
| Overview | `index.md` | project statement, stakes, current headline |
| Hierarchy | `hierarchy.md` | the `72 -> 56 -> 40 -> 24` story |
| Menu | `menu-summary.md` | `MENU2` stats and survivor/exhaustion status |
| Tests | `tests/index.md` | T1-T32 ledger and test pages |
| Enumerators | `weight-enumerators-pipeline.md` | data catalog and downloads |
| Contribute | `contribute.md` + `ideas-not-pursued.md` | open tasks, parked ideas, proof standards |

The top tabs should be ordinary links styled as tabs. That keeps the site static,
fast, and easy to host on GitHub Pages.

## 2. Page-Level Tabs

Each complex page should have its own local tabs.

### 2.1 Home / Overview

```text
Snapshot | Why It Matters | How To Help
```

- `Snapshot`: the headline numbers and open status.
- `Why It Matters`: find-it vs rule-it-out stakes.
- `How To Help`: links to open problem cards and test pages.

### 2.2 Hierarchy

```text
72 | 56 | 40 | 24 | Diagram
```

- `72`: Type II code and forced global enumerator.
- `56`: anchored residual and `5082` minimum words.
- `40`: length-40 menu and `(k,a,b)`.
- `24`: rigid bottom rung.
- `Diagram`: visual residual tower.

### 2.3 Menu

```text
Summary | Survivors | Eliminations | Witnesses | Full Ledger
```

- `Summary`: `132 -> 72`, with caveats.
- `Survivors`: public table of surviving rows.
- `Eliminations`: grouped by mathematical idea.
- `Witnesses`: route-3A nonempty rows and unresolved rows.
- `Full Ledger`: link to the generated technical ledger.

### 2.4 Tests

```text
All | Kills | Saturated | Validation | Open
```

Recommended grouping from `tests.yml`:

- `Kills`: T02, T05, T06, T08, T13, T19, T20, T32.
- `Saturated`: T03, T04, T07, T09-T16, T21-T31 except T29 details.
- `Validation`: T17, T18, T23.
- `Open`: T29 PSD status and unresolved T32 rows.

Each test page should then use:

```text
Summary | Result | Verification | Sources | Help
```

### 2.5 Enumerators

```text
Catalog | JSON Bundle | Triweight Routines | Manifest
```

- `Catalog`: all staged one-weight, biweight, support-weight, and triweight data.
- `JSON Bundle`: download all enumerator JSON files at once.
- `Triweight Routines`: full source bundle for row/column symmetrization,
  modular prime runs, and reconciliation.
- `Manifest`: machine-readable file list, provenance, and caveats.

### 2.6 Contribute

```text
Open Tasks | Parked Ideas | Saturated Routes | Validation Policy
```

- `Parked Ideas`: ideas sketched but not built.
- `Saturated Routes`: things that were tried and should not be rebuilt unchanged.
- `Validation Policy`: exact-input and certificate rules.

## 3. Static Implementation Strategy

The first implementation should stay static.

Use one of these:

1. Plain HTML/CSS/JS generated from Markdown.
2. Astro with Markdown content collections.
3. Eleventy with YAML data files.
4. Jekyll if staying close to GitHub Pages defaults.

Best fit for this project:

```text
Astro or Eleventy
```

Reason: both make it easy to read `website/data/tests.yml`, generate one card
per test, and build tabbed pages without turning the site into a client-side app.

## 4. Accessibility Rules

Tabs should be accessible:

- use real links for top-level page tabs;
- for in-page tabs, use buttons with `role="tab"` and panels with
  `role="tabpanel"`;
- keep content reachable if JavaScript is disabled;
- sync tab state to the URL hash, e.g. `#survivors` or `#verification`;
- do not hide essential proof status only inside JavaScript-rendered content.

## 5. Visual Layout

Use a dense, calm interface:

```text
Top tab bar
Status strip
Page title
Local tab bar
Main content panel
Right-side source/provenance rail on desktop
```

On mobile:

```text
Top tabs become horizontal scroll
Local tabs become segmented control or compact dropdown
Source rail moves below content
```

## 6. Concrete First Screen

The home page should look roughly like:

```text
Extremal 72
[Overview] [Hierarchy] [Menu] [Tests] [Enumerators] [Contribute]

Open problem: decide whether a binary Type II [72,36,16] code exists.

[Snapshot] [Why It Matters] [How To Help]

Snapshot
  A_16: 249849
  residual minimum words: 5082
  length-40 menu: 132 raw / 60 eliminated / 72 surviving
  witnessed rows: 51
  unresolved rows: 21
```

## 7. What To Build First

Before creating the separate repo, build a tiny static prototype in this folder:

```text
website/prototype/
  index.html
  styles.css
  tabs.js
```

The prototype should demonstrate:

- top tabs;
- local tabs;
- menu summary cards;
- test-status grouped tabs;
- one sample test page layout.

Once that feels right, start the separate public site repo and move the
prototype into a real static-site framework.
