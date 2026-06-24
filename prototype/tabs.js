let tests = [];

let enumerators = [];

const state = {
  filter: "all",
  query: "",
};

function activateMainTab(targetId, updateHash = true) {
  const tabs = document.querySelectorAll("[data-tab-target]");
  const panels = document.querySelectorAll(".panel");

  tabs.forEach((tab) => {
    const isActive = tab.dataset.tabTarget === targetId;
    tab.classList.toggle("is-active", isActive);
    tab.setAttribute("aria-selected", String(isActive));
  });

  panels.forEach((panel) => {
    const isActive = panel.id === targetId;
    panel.classList.toggle("is-active", isActive);
    panel.hidden = !isActive;
  });

  if (updateHash) {
    history.replaceState(null, "", `#${targetId}`);
  }

  if (targetId === "hierarchy") {
    requestAnimationFrame(drawHierarchy);
  }
}

function testKind(test) {
  const status = test.status.toLowerCase();
  const category = test.category.toLowerCase();

  if (status.includes("validation") || category.includes("validation")) return "validation";
  if (status.includes("open") || status.includes("active")) return "open";
  if (test.kills > 0 || status.includes("kill")) return "kills";
  if (status.includes("saturates")) return "saturates";
  return "all";
}

function matchesFilter(test) {
  if (state.filter === "all") return true;
  if (state.filter === "kills") return test.kills > 0 || test.status.includes("kill");
  return testKind(test) === state.filter;
}

function matchesQuery(test) {
  if (!state.query) return true;
  const haystack = [
    test.id,
    test.abbr,
    test.title,
    test.status,
    test.result,
    test.category,
  ]
    .join(" ")
    .toLowerCase();

  return haystack.includes(state.query);
}

function badgeClass(test) {
  const kind = testKind(test);
  if (test.kills > 0) return "kill";
  if (kind === "open") return "open";
  if (kind === "validation") return "validation";
  if (kind === "saturates") return "saturates";
  return "";
}

function renderTests() {
  const grid = document.querySelector("#testGrid");
  const summary = document.querySelector("#testSummary");
  const visible = tests.filter((test) => matchesFilter(test) && matchesQuery(test));
  const totalKills = tests.reduce((sum, test) => sum + test.kills, 0);
  const visibleKills = visible.reduce((sum, test) => sum + test.kills, 0);

  summary.textContent = `${visible.length} of ${tests.length} tests shown; ${visibleKills} of ${totalKills} proof-grade eliminations in view.`;
  grid.replaceChildren(
    ...visible.map((test) => {
      const card = document.createElement("article");
      card.className = "test-card";

      const meta = document.createElement("span");
      meta.className = "meta";
      meta.textContent = `${test.id} ${test.abbr} | ${test.category}`;

      const title = document.createElement("h3");
      title.textContent = test.title;

      const status = document.createElement("p");
      status.textContent = test.status;

      const result = document.createElement("p");
      result.innerHTML = `<strong>Result:</strong> ${test.result}`;

      const link = document.createElement("a");
      link.className = "test-page-link";
      link.href = test.page;
      link.textContent = "Summary";

      const badges = document.createElement("div");
      badges.className = "badge-row";

      const killBadge = document.createElement("span");
      killBadge.className = `badge ${badgeClass(test)}`;
      killBadge.textContent = test.kills === 1 ? "1 elimination" : `${test.kills} eliminations`;

      const statusBadge = document.createElement("span");
      statusBadge.className = `badge ${badgeClass(test)}`;
      statusBadge.textContent = testKind(test);

      badges.append(killBadge, statusBadge);
      card.append(meta, title, status, result, link, badges);
      return card;
    })
  );
}

function renderEnumerators() {
  const grid = document.querySelector("#enumeratorGrid");
  const summary = document.querySelector("#enumeratorSummary");
  if (!grid || !summary) return;

  const kinds = [...new Set(enumerators.map((item) => item.kind))].sort();
  summary.textContent = `${enumerators.length} JSON entries staged across ${kinds.join(", ")} data.`;
  grid.replaceChildren(
    ...enumerators.map((item) => {
      const card = document.createElement("article");
      card.className = "enumerator-card";

      const meta = document.createElement("span");
      meta.className = "meta";
      meta.textContent = item.kind;

      const title = document.createElement("h3");
      title.textContent = item.title;

      const note = document.createElement("p");
      note.textContent = item.note;

      const link = document.createElement("a");
      link.href = item.file;
      link.textContent = "Download JSON";

      card.append(meta, title, note, link);
      return card;
    })
  );
}

const referencesState = { query: "" };
let referencesData = [];

function renderReferences() {
  const grid = document.querySelector("#referenceGrid");
  const summary = document.querySelector("#referenceSummary");
  if (!grid || !summary) return;
  const q = referencesState.query.toLowerCase();
  const items = referencesData.filter((r) => {
    if (!q) return true;
    return [
      r.id, r.title, r.authors, r.year, r.category, r.provides,
      (r.relevant_tests || []).join(" "),
      (r.relevant_enumerators || []).join(" "),
    ].join(" ").toLowerCase().includes(q);
  });
  summary.textContent =
    `${items.length} of ${referencesData.length} references` +
    (q ? ` matching "${q}"` : "") + ".";
  grid.replaceChildren(
    ...items.map((r) => {
      const card = document.createElement("article");
      card.className = "enumerator-card";

      const meta = document.createElement("span");
      meta.className = "meta";
      meta.textContent = r.category;

      const title = document.createElement("h3");
      title.textContent = r.title;

      const auth = document.createElement("p");
      auth.innerHTML = `<strong>${r.authors}</strong> &middot; ${r.year}`;

      const prov = document.createElement("p");
      prov.textContent = r.provides;

      const tags = document.createElement("p");
      const t = r.relevant_tests || [];
      const e = r.relevant_enumerators || [];
      tags.innerHTML =
        ((t.length ? `<strong>Tests:</strong> ${t.join(", ")}<br>` : "") +
          (e.length ? `<strong>Enumerators:</strong> ${e.join(", ")}` : "")) ||
        "<em>background / no test or enumerator tag</em>";

      const m = String(r.source || "").match(/arXiv:\s*([0-9.]+)/i);
      const link = document.createElement("a");
      if (m) link.href = `https://arxiv.org/abs/${m[1]}`;
      link.textContent = r.source || "";

      card.append(meta, title, auth, prov, tags, link);
      return card;
    })
  );
}

function setFilter(filter) {
  state.filter = filter;
  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.filter === filter);
  });
  renderTests();
}

function drawHierarchy() {
  const canvas = document.querySelector("#hierarchyCanvas");
  if (!canvas) return;

  const parent = canvas.parentElement;
  const rect = parent.getBoundingClientRect();
  const ratio = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * ratio));
  canvas.height = Math.max(1, Math.floor(rect.height * ratio));
  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;

  const ctx = canvas.getContext("2d");
  ctx.scale(ratio, ratio);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const points =
    rect.width < 680
      ? [
          [rect.width / 2, 88],
          [rect.width / 2, 232],
          [rect.width / 2, 376],
          [rect.width / 2, 520],
        ]
      : [
          [rect.width * 0.16, 118],
          [rect.width * 0.4, 242],
          [rect.width * 0.64, 118],
          [rect.width * 0.86, 242],
        ];

  ctx.lineWidth = 4;
  ctx.strokeStyle = "#315f8a";
  ctx.fillStyle = "#315f8a";
  ctx.setLineDash([8, 8]);

  for (let index = 0; index < points.length - 1; index += 1) {
    const [x1, y1] = points[index];
    const [x2, y2] = points[index + 1];
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.bezierCurveTo(x1 + 90, y1, x2 - 90, y2, x2, y2);
    ctx.stroke();
    drawArrow(ctx, x1, y1, x2, y2);
  }

  ctx.setLineDash([]);
  points.forEach(([x, y], index) => {
    const colors = ["#202124", "#0f766e", "#a15c00", "#a23b3b"];
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, Math.PI * 2);
    ctx.fillStyle = colors[index];
    ctx.fill();
  });
}

function drawArrow(ctx, x1, y1, x2, y2) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const size = 10;
  ctx.save();
  ctx.translate(x2, y2);
  ctx.rotate(angle);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-size, -size * 0.55);
  ctx.lineTo(-size, size * 0.55);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

document.querySelectorAll("[data-tab-target]").forEach((button) => {
  button.addEventListener("click", () => activateMainTab(button.dataset.tabTarget));
});

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => setFilter(button.dataset.filter));
});

document.querySelector("#testSearch").addEventListener("input", (event) => {
  state.query = event.target.value.trim().toLowerCase();
  renderTests();
});

window.addEventListener("resize", () => {
  if (!document.querySelector("#hierarchy").hidden) {
    drawHierarchy();
  }
});

const hashTarget = window.location.hash.replace("#", "");
if (hashTarget && document.getElementById(hashTarget)) {
  activateMainTab(hashTarget, false);
}

function loadJSON(url) {
  return fetch(url).then((r) => (r.ok ? r.json() : null)).catch(() => null);
}

// Single source of truth: the dashboard data is fetched from the generated
// JSON (built from data/*.yml), not hardcoded. Paths are base-relative so the
// site works at a domain root or a project sub-path.
Promise.all([
  loadJSON("data/tests.json"),
  loadJSON("data/enumerators.json"),
  loadJSON("data/references.json"),
]).then(([t, e, r]) => {
  tests = (t && t.tests) || [];
  enumerators = (e && e.enumerators) || [];
  referencesData = (r && r.references) || [];
  renderTests();
  renderEnumerators();
  renderReferences();
});

const refSearchEl = document.querySelector("#refSearch");
if (refSearchEl) {
  refSearchEl.addEventListener("input", (event) => {
    referencesState.query = event.target.value.trim();
    renderReferences();
  });
}
