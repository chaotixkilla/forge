// Reader names for item codes, from the page's praxis-names; the code stays available as a tooltip.
var NAMES = {};
try { NAMES = JSON.parse(document.getElementById("praxis-names").textContent); } catch (e) {}
function NAME(id) { return NAMES[id] || id; }
document.addEventListener("click", function (e) { document.querySelectorAll("details.codes[open]").forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute("open"); }); });
// Filter and sort for interactive views. Pages read completely without it.
(function () {
  document.querySelectorAll("section[data-view]").forEach(function (sec) {
    var input = sec.querySelector("input.filter");
    if (input) {
      input.addEventListener("input", function () {
        var q = input.value.toLowerCase();
        sec.querySelectorAll("tbody tr, .card[data-item], .term, details.req").forEach(function (row) {
          row.hidden = !!q && row.textContent.toLowerCase().indexOf(q) < 0;
        });
      });
    }
    sec.querySelectorAll("table").forEach(function (table) {
      var asc = {};
      table.querySelectorAll("th[data-sortable]").forEach(function (th, i) {
        th.tabIndex = 0;
        function sort() {
          var body = table.tBodies[0];
          if (!body) return;
          asc[i] = !asc[i];
          [].slice.call(body.rows)
            .sort(function (a, b) {
              var x = +a.cells[i].dataset.sort, y = +b.cells[i].dataset.sort;
              return asc[i] ? x - y : y - x;
            })
            .forEach(function (r) { body.appendChild(r); });
        }
        th.addEventListener("click", sort);
        th.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sort(); } });
      });
    });
  });
})();

// Filter chips: each chip group narrows the rows by one data attribute; all groups must match.
(function () {
  var sets = document.querySelectorAll(".chipset");
  if (!sets.length) return;
  function apply() {
    var want = {};
    sets.forEach(function (s) {
      var on = s.querySelector("button[aria-pressed=true]");
      want[s.dataset.filter] = on ? on.dataset.v : "";
    });
    document.querySelectorAll("[data-" + Object.keys(want)[0] + "]:not(.stream)").forEach(function (row) {
      row.hidden = Object.keys(want).some(function (k) { return want[k] && row.dataset[k] !== want[k]; });
    });
    document.querySelectorAll(".stream").forEach(function (sec) {
      if (sec.dataset.decider === "__all") return;
      sec.hidden = !sec.querySelector("[data-" + Object.keys(want)[0] + "]:not([hidden])");
    });
  }
  sets.forEach(function (s) {
    s.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-v]");
      if (!b) return;
      s.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      apply();
    });
  });
})();

// Trace: work -> requirements -> gates. Select anything to see its whole chain and its story.
(function () {
  var host = document.getElementById("trace-graph"), src = document.getElementById("trace-data");
  if (!host || !src) return;
  var d = JSON.parse(src.textContent), panel = document.getElementById("trace-panel");
  var NS = "http://www.w3.org/2000/svg", ROW = 24, TOP = 34;
  var W = Math.max(host.clientWidth - 2, 560), xW = Math.round(W * .2), xR = xW + 60, xG = W - Math.max(150, Math.round(W * .2)), CH = 6.3,
    workChars = Math.floor((xW - 8) / CH), reqChars = Math.floor((xG - 50 - xR - 14) / CH), gateChars = Math.floor((W - xG - 6) / CH);
  var pos = {}, y = TOP, groups = [];
  var byGroup = {};
  d.reqs.forEach(function (r) { (byGroup[r.group] = byGroup[r.group] || []).push(r); });
  Object.keys(byGroup).forEach(function (g) {
    groups.push({ name: g, y: y + 6 }); y += ROW;
    byGroup[g].forEach(function (r) { pos[r.id] = y + 4; y += ROW; });
    y += 8;
  });
  var H = y + 10;
  function spread(list, ideal) {
    list.sort(function (a, b) { return ideal(a) - ideal(b); });
    var last = TOP - ROW;
    list.forEach(function (n) { var v = Math.max(ideal(n), last + ROW); pos[n.id] = v; last = v; });
  }
  var nb = {};
  d.links.forEach(function (l) { (nb[l[0]] = nb[l[0]] || []).push(l[1]); (nb[l[1]] = nb[l[1]] || []).push(l[0]); });
  function avg(id) { var ys = (nb[id] || []).map(function (x) { return pos[x]; }).filter(function (v) { return v != null; });
    return ys.length ? ys.reduce(function (a, b) { return a + b; }, 0) / ys.length : H; }
  spread(d.work.slice(), function (n) { return avg(n.id); });
  d.gates.forEach(function (g, i) { pos[g.id] = TOP + 6 + i * Math.max(ROW, (H - TOP - 20) / Math.max(d.gates.length - 1, 1)); });
  var svg = document.createElementNS(NS, "svg");
  svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("width", W); svg.setAttribute("height", H);
  svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "Work, requirements and gates, linked");
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); (parent || svg).appendChild(e); return e; }
  function text(x, yy, s, cls, anchor, parent) { var t = el("text", { x: x, y: yy, class: cls || "", "text-anchor": anchor || "start", "dominant-baseline": "middle" }, parent); t.textContent = s; return t; }
  [["Work", xW], ["Requirements", xR + 14], ["Gates", xG]].forEach(function (h, i) { text(h[1], 12, h[0].toUpperCase(), "colhead", i === 0 ? "end" : "start"); });
  groups.forEach(function (g) { text(xR + 14, g.y, g.name, "grp"); });
  var xOf = {}; d.work.forEach(function (n) { xOf[n.id] = xW + 10; }); d.reqs.forEach(function (n) { xOf[n.id] = xR; }); d.gates.forEach(function (n) { xOf[n.id] = xG - 12; });
  var linkEls = d.links.map(function (l) {
    var a = l[0], b = l[1], x1 = xOf[a] + (a.indexOf("UNIT") === 0 ? 0 : 6), x2 = xOf[b] - (b.indexOf("GATE") === 0 ? 0 : 6);
    if (a.indexOf("REQ") === 0) { x1 = xG - 44; }
    var mx = (x1 + x2) / 2;
    var p = el("path", { d: "M" + x1 + "," + pos[a] + " C" + mx + "," + pos[a] + " " + mx + "," + pos[b] + " " + x2 + "," + pos[b], class: "lk" });
    p.dataset.a = a; p.dataset.b = b; return p;
  });
  var nodeEls = {};
  function node(id, x, yy, cls, label, anchor, lx) {
    var g = el("g", { class: "nd " + cls, tabindex: "0", role: "button", "aria-label": id + " " + label });
    g.dataset.id = id;
    if (cls.indexOf("oneway") >= 0) el("rect", { x: x - 6, y: yy - 6, width: 12, height: 12, transform: "rotate(45 " + x + " " + yy + ")" }, g);
    else el("circle", { cx: x, cy: yy, r: 6 }, g);
    text(lx, yy, label, "lb", anchor, g);
    nodeEls[id] = g; return g;
  }
  function short(s, n) { return s.length > n ? s.slice(0, n - 1) + "…" : s; }
  d.work.forEach(function (n) { node(n.id, xW + 10, pos[n.id], n.merged ? "w merged" : "w", short(n.label + " " + n.title, workChars), "end", xW); });
  d.reqs.forEach(function (n) { node(n.id, xR, pos[n.id], "r st-" + n.status.replace(" ", ""), short(NAME(n.id) + "  " + n.title, reqChars), "start", xR + 14); });
  d.gates.forEach(function (n) { node(n.id, xG - 12, pos[n.id], "g" + (n.oneway ? " oneway" : "") + (n.ran ? " ran" : ""), short(NAME(n.id) + " · " + n.title, gateChars), "start", xG); });
  host.appendChild(svg);
  var kind = function (id) { return id.split("-")[0]; };
  function chain(id) {
    var on = {}; on[id] = 1;
    var k = kind(id), first = nb[id] || [];
    first.forEach(function (x) { on[x] = 1; });
    if (k !== "REQ") first.forEach(function (r) { (nb[r] || []).forEach(function (x) { if (kind(x) !== k) on[x] = 1; }); });
    return on;
  }
  function esc(s) { return String(s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function link(e) { return e.link ? '<a href="' + esc(e.link) + '">' + esc(e.what || e.link) + "</a>" : esc(e.what); }
  function chips(ids) { return ids.length ? ids.map(function (i) { return '<button class="ref" data-go="' + i + '" title="' + i + '">' + esc(NAME(i)) + "</button>"; }).join(" ") : '<span class="muted">none</span>'; }
  var find = {}; d.work.concat(d.reqs, d.gates).forEach(function (n) { find[n.id] = n; });
  function show(id) {
    var n = find[id], on = chain(id), k = kind(id), h = "";
    svg.classList.add("focus");
    Object.keys(nodeEls).forEach(function (x) { nodeEls[x].classList.toggle("on", !!on[x]); nodeEls[x].classList.toggle("sel", x === id); });
    linkEls.forEach(function (p) { p.classList.toggle("on", !!(on[p.dataset.a] && on[p.dataset.b])); });
    var rel = function (kk) { return Object.keys(on).filter(function (x) { return kind(x) === kk && x !== id; }); };
    if (k === "REQ") {
      var st = { met: "holds", partly: "unsettled" }[n.status] || "unchecked";
      h = '<p class="pk"><span class="id" title="' + n.id + '">' + NAME(n.id) + '</span> ' + esc(n.group) + ' <span class="chip c-' + st + '">' + n.status + "</span></p>" +
        "<h3>" + esc(n.title) + '</h3><p class="shall">' + esc(n.shall) + "</p>" +
        (n.why ? '<p><b>Why.</b> ' + esc(n.why) + "</p>" : "") +
        "<h4>Accepted when</h4><ul class=\"checks-list\">" + (n.accepted.length ? n.accepted.map(function (a) { return '<li class="' + (a.ok ? "ok" : "todo") + '">' + esc(a.text) + "</li>"; }).join("") : '<li class="todo">No criterion yet</li>') + "</ul>" +
        "<h4>Evidence</h4><ul class=\"ev\">" + (n.evidence.length ? n.evidence.map(function (e) { return '<li class="' + e.mark + '">' + link(e) + (e.when ? ' <span class="muted">' + esc(e.when) + "</span>" : "") + "</li>"; }).join("") : '<li class="src muted">None yet</li>') + "</ul>" +
        "<h4>Served by</h4><p>" + chips(rel("UNIT")) + "</p><h4>Opens gates</h4><p>" + chips(rel("GATE")) + "</p>" +
        (n.waits.length ? "<h4>Waits on</h4><p>" + n.waits.map(function (w) { return '<span class="id">' + w + "</span>"; }).join(" ") + "</p>" : "");
    } else if (k === "UNIT") {
      h = '<p class="pk"><span class="id" title="' + n.id + '">' + NAME(n.id) + "</span> " + (n.merged ? '<span class="chip c-holds">merged · ' + esc(n.label) + "</span>" : '<span class="chip c-unchecked">no request yet</span>') + "</p><h3>" + esc(n.title) + "</h3><p>" + esc(n.body) + "</p><h4>Serves</h4><p>" + chips(rel("REQ")) + "</p><h4>Gates it opens</h4><p>" + chips(rel("GATE")) + "</p>";
    } else {
      h = '<p class="pk"><span class="id" title="' + n.id + '">' + NAME(n.id) + "</span> " + (n.oneway ? '<span class="chip c-open">one-way</span> ' : "") + (n.ran ? '<span class="chip c-holds">ran</span>' : '<span class="chip c-unchecked">' + esc(n.when || "undated") + "</span>") + "</p><h3>" + esc(n.title) + "</h3><h4>Requirements it exposes</h4><p>" + chips(rel("REQ")) + "</p><h4>Work it waits on</h4><p>" + chips(rel("UNIT")) + "</p>";
    }
    panel.innerHTML = h + '<p class="muted small">Esc or click the background to clear.</p>';
    try { history.replaceState(null, "", "#" + id); } catch (e) {}
  }
  function clear() { svg.classList.remove("focus"); Object.keys(nodeEls).forEach(function (x) { nodeEls[x].classList.remove("on", "sel"); }); linkEls.forEach(function (p) { p.classList.remove("on"); }); }
  svg.addEventListener("click", function (e) { var g = e.target.closest(".nd"); if (g) show(g.dataset.id); else clear(); });
  svg.addEventListener("keydown", function (e) { var g = e.target.closest(".nd"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); show(g.dataset.id); } });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") clear(); });
  panel.addEventListener("click", function (e) { var b = e.target.closest("[data-go]"); if (b) { show(b.dataset.go); nodeEls[b.dataset.go].focus(); } });
  var start = location.hash.slice(1);
  if (find[start]) show(start);
})();

// Cutover: select a gate on the rail to open its card.
(function () {
  var btns = document.querySelectorAll(".gbtn");
  if (!btns.length) return;
  function pick(id, byReader) {
    btns.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.gate === id ? "true" : "false"); });
    document.querySelectorAll(".gpanel").forEach(function (p) { p.hidden = p.dataset.gate !== id; });
    document.querySelectorAll("table.needs td, table.needs th.c").forEach(function (c) {
      var g = c.dataset.gate || (c.querySelector(".gpick") || {}).dataset && c.querySelector(".gpick").dataset.gate;
      c.classList.toggle("sel", g === id);
    });
    if (byReader) { try { history.replaceState(null, "", "#" + id); } catch (e) {} }
  }
  btns.forEach(function (b) { b.addEventListener("click", function () { pick(b.dataset.gate, true); }); });
  document.querySelectorAll(".gpick").forEach(function (b) { b.addEventListener("click", function () { pick(b.dataset.gate, true); }); });

  var h = location.hash.slice(1), pressed = document.querySelector('.gbtn[aria-pressed="true"]');
  if (document.querySelector('.gbtn[data-gate="' + h + '"]')) pick(h); else if (pressed) pick(pressed.dataset.gate);
})();

// Map: what waits on what. Layers by depth; red is the critical path; select a node for its neighbours.
(function () {
  var host = document.getElementById("map-graph"), src = document.getElementById("map-data");
  if (!host || !src) return;
  var d = JSON.parse(src.textContent), panel = document.getElementById("map-panel"), NS = "http://www.w3.org/2000/svg";
  var byId = {}, preds = {}, succs = {}, critSet = {};
  d.nodes.forEach(function (n) { byId[n.id] = n; });
  d.edges.forEach(function (e) { (preds[e[1]] = preds[e[1]] || []).push(e[0]); (succs[e[0]] = succs[e[0]] || []).push(e[1]); });
  d.crit.forEach(function (n) { critSet[n] = 1; });
  var views = host.closest(".views");
  var state = { mode: "all", owner: "", done: true, asks: true, sel: null, layout: (views && views.dataset.layout) || "lanes" };
  if (views) views.addEventListener("praxis:view", function (e) { if (e.detail.layout) { state.layout = e.detail.layout; draw(); } });
  var ownerSel = document.getElementById("map-owner");
  if (ownerSel) {
    var owners = {}; d.nodes.forEach(function (n) { if (n.owner) owners[n.owner] = 1; });
    Object.keys(owners).sort().forEach(function (o) { var op = document.createElement("option"); op.value = o; op.textContent = o; ownerSel.appendChild(op); });
  }
  // Time travel, when set, says whether an item was filed yet and whether it was done on its day; else today's state holds.
  d.nodes.forEach(function (n) { n.doneToday = n.done; });
  function asOf() { d.nodes.forEach(function (n) { n.done = window.praxisDoneAt ? window.praxisDoneAt(n.id, n.doneToday) : n.doneToday; }); }
  document.addEventListener("praxis:travel", function () { draw(); });
  function visible(n) { return (!window.praxisFiledAt || window.praxisFiledAt(n.id)) && (state.done || !n.done) && (state.asks || n.kind !== "ask"); }
  function wrap(s, n) {
    var w = s.split(/\s+/), lines = [""], i = 0;
    w.forEach(function (x) { if ((lines[i] + " " + x).trim().length > n && lines[i]) { if (i === 1) { lines[1] += "…"; i = 2; return; } lines[++i] = x; } else if (i < 2) lines[i] = (lines[i] + " " + x).trim(); });
    return lines.slice(0, 2).map(function (l) { return l.length > n + 1 ? l.slice(0, n) + "…" : l; });
  }
  function esc(s) { return String(s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function stateWord(n) { return n.done ? "done" : n.can ? "can start now" : n.kind === "ask" ? (n.state === "proposed" ? "proposed" : "open") : "waiting on other steps"; }
  var svg, els = {}, links = [];
  function draw() {
    asOf();
    host.innerHTML = ""; els = {}; links = [];
    var shown = d.nodes.filter(visible), maxL = 0, pos = {};
    var LANES = [["ask", "Decisions and outside dependencies"], ["step", "Work"], ["gate", "Gates"]];
    var laneOf = function (n) { return n.kind === "dep" ? "ask" : n.kind; };
    shown.forEach(function (n) { maxL = Math.max(maxL, n.layer); });
    var halos = [];
    if (state.layout === "web") {
    // The web: each gate a hub in opening order, what feeds it clustered around it in rings, the threads between
    // clusters left visible. An item belongs to the first gate it reaches downstream; one reaching none is its own cluster.
    var order = [], seenG = {};
    function placeG(g) { if (seenG[g.id]) return; var p = byId[g.when]; if (p && p.kind === "gate" && visible(p)) placeG(p); seenG[g.id] = 1; order.push(g); }
    shown.filter(function (n) { return n.kind === "gate"; }).forEach(placeG);
    function homeOf(id) {
      var q = [id], seen = {}; seen[id] = 1;
      while (q.length) { var x = q.shift(), ss = succs[x] || [];
        for (var i = 0; i < ss.length; i++) { var y = ss[i]; if (seen[y]) continue; seen[y] = 1; if (byId[y] && byId[y].kind === "gate" && visible(byId[y])) return y; q.push(y); } }
      return null;
    }
    var groups = {}, loose = [];
    order.forEach(function (g) { groups[g.id] = []; });
    shown.forEach(function (n) { if (n.kind === "gate") return; var h = homeOf(n.id); if (h && groups[h]) groups[h].push(n); else loose.push(n); });
    var hubs = order.map(function (g) { return { g: g, items: groups[g.id] }; });
    if (loose.length) hubs.push({ g: null, items: loose });
    // Rings fill outward, each holding as many items as its length gives about 120px of label room.
    var R0 = 92, ringGap = 66, maxN = 1;
    hubs.forEach(function (h) { maxN = Math.max(maxN, h.items.length); });
    function cap(ring) { return Math.max(4, Math.floor(2 * Math.PI * (R0 + ring * ringGap) / 120)); }
    function ringsFor(k) { var r = 0, left = k; while (left > cap(r)) { left -= cap(r); r++; } return r + 1; }
    function radiusFor(k) { return R0 + (ringsFor(k) - 1) * ringGap; }
    var avail = Math.max((host.clientWidth || 1100) - 2, 640), cellH = 2 * radiusFor(maxN) + 110;
    var cols = Math.max(1, Math.min(hubs.length, Math.floor(avail / (2 * radiusFor(maxN) + 80)))), cellW = avail / cols, H = 0;
    pos = {}; laneBox = []; halos = [];
    hubs.forEach(function (h, i) {
      var r = radiusFor(h.items.length), col = i % cols, row = Math.floor(i / cols);
      var cx = cellW * col + cellW / 2, cy = 46 + radiusFor(maxN) + row * cellH + (col % 2 ? 26 : 0);
      if (h.g) pos[h.g.id] = { x: cx, y: cy };
      h.items.sort(function (a, b) { return (critSet[b.id] ? 1 : 0) - (critSet[a.id] ? 1 : 0) || (a.done ? 1 : 0) - (b.done ? 1 : 0); });
      var ring = 0, start = 0;
      h.items.forEach(function (n, k) {
        if (k - start >= cap(ring)) { start = k; ring++; }
        var inRing = Math.min(cap(ring), h.items.length - start), rr = R0 + ring * ringGap;
        var ang = -Math.PI / 2 + (k - start) * 2 * Math.PI / inRing + ring * .35;
        pos[n.id] = { x: cx + rr * Math.cos(ang), y: cy + rr * Math.sin(ang) };
      });
      halos.push({ x: cx, y: cy, r: r + 38, g: h.g });
      H = Math.max(H, cy + r + 70);
    });
    var W = avail, maxL = 0;
    } else if (state.layout === "gates") {
    var maxR = 6; shown.forEach(function (n) { if (!n.done) maxR = Math.max(maxR, Math.min(17, 6 + Math.sqrt(n.down || 0) * 2.4)); });
    var colW = 124, rowH = Math.max(66, Math.round(2 * maxR + 50)), laneGap = 10, labelW = 26, x0 = labelW + 36, laneBox = [];
    // Gates in opening order: a gate that opens on another follows it.
    var order = [], seenG = {};
    function placeG(g) { if (seenG[g.id]) return; var p = byId[g.when]; if (p && p.kind === "gate" && visible(p)) placeG(p); seenG[g.id] = 1; order.push(g); }
    shown.filter(function (n) { return n.kind === "gate"; }).forEach(placeG);
    var rank = function (n) { return (critSet[n.id] ? 0 : 2) + (n.done ? 1 : 0); };
    var groups = order.map(function (g) {
      return { g: g, asks: (preds[g.id] || []).map(function (i) { return byId[i]; })
        .filter(function (n) { return n && n.kind !== "gate" && visible(n); }).sort(function (a, b) { return rank(a) - rank(b); }) };
    });
    var placed = {}; groups.forEach(function (G) { G.asks.forEach(function (n) { placed[n.id] = 1; }); });
    var loose = shown.filter(function (n) { return n.kind !== "gate" && !placed[n.id]; });
    if (loose.length) groups.push({ g: null, asks: loose });
    var avail = Math.max((host.clientWidth || 1100) - 2 - x0 - 24, 560), rowsN = 1, cols;
    function widthFor(r) { return groups.reduce(function (s, G) { return s + Math.max(1, Math.ceil(G.asks.length / r)) * colW; }, 0) + (groups.length - 1) * 18; }
    while (rowsN < 8 && widthFor(rowsN) > avail) rowsN++;
    var askTop = 26, laneH = Math.max(rowsN * rowH + 14, 300), gateY = askTop + laneH + laneGap + 30, xCur = x0, pos = {};
    groups.forEach(function (G) {
      cols = Math.max(1, Math.ceil(G.asks.length / rowsN));
      G.asks.forEach(function (n, i) {
        var below = i + cols < G.asks.length, cx = xCur + (i % cols) * colW + colW / 2;
        pos[n.id] = { x: cx, y: askTop + 20 + Math.floor(i / cols) * rowH, gx: below ? cx + colW / 2 - 4 : 0, yb: askTop + laneH - 10 };
      });
      if (G.g) pos[G.g.id] = { x: xCur + cols * colW / 2, y: gateY };
      xCur += cols * colW + 18;
    });
    if (shown.some(function (n) { return n.kind !== "gate"; })) laneBox.push({ name: "Decisions and outside dependencies", y: askTop - 6, h: laneH });
    laneBox.push({ name: "Gates", y: gateY - 30, h: 84 });
    var W = Math.max(host.clientWidth - 2, xCur + 12), H = gateY + 62;
    } else {
    var colX = [], acc = 0;
    for (var cl = 0; cl <= maxL; cl++) {
      var inCol = shown.filter(function (n) { return n.layer === cl; });
      var narrow = inCol.length && inCol.every(function (n) { return n.done; });
      colX.push(acc); acc += narrow ? 58 : 108;
    }
    var maxR = 6; shown.forEach(function (n) { if (!n.done) maxR = Math.max(maxR, Math.min(17, 6 + Math.sqrt(n.down || 0) * 2.4)); });
    var colW = 108, rowH = Math.max(60, Math.round(2 * maxR + 44)), top = 26, laneGap = 10, labelW = 26, y0 = top, laneBox = [];
    LANES.forEach(function (lane) {
      var cells = {}, rows = 0;
      shown.filter(function (n) { return laneOf(n) === lane[0]; }).forEach(function (n) { (cells[n.layer] = cells[n.layer] || []).push(n); });
      Object.keys(cells).forEach(function (l) {
        cells[l].sort(function (a, b) { return (critSet[b.id] ? 1 : 0) - (critSet[a.id] ? 1 : 0) || (a.done ? 1 : 0) - (b.done ? 1 : 0); });
        cells[l].forEach(function (n, i) { pos[n.id] = { x: labelW + 44 + colX[n.layer], y: y0 + 26 + i * rowH }; });
        rows = Math.max(rows, cells[l].length);
      });
      if (!rows) return;
      laneBox.push({ name: lane[1], y: y0, h: rows * rowH + 14 });
      y0 += rows * rowH + 14 + laneGap;
    });
    var W = Math.max(host.clientWidth - 2, labelW + 44 + acc + 30), H = y0;
    }
    svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("width", W); svg.setAttribute("height", H);
    svg.setAttribute("role", "img"); svg.setAttribute("aria-label", "What waits on what");
    function el(t, a, p) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); (p || svg).appendChild(e); return e; }
    var defs = el("defs", {});
    [["ar", "var(--muted)"], ["arc", "var(--open)"], ["aron", "var(--accent)"]].forEach(function (m) {
      var mk = el("marker", { id: m[0], viewBox: "0 0 8 8", refX: 7, refY: 4, markerWidth: 6, markerHeight: 6, orient: "auto" }, defs);
      el("path", { d: "M0,0 L8,4 L0,8 z", style: "fill:" + m[1] }, mk);
    });
    laneBox.forEach(function (b, i) {
      el("rect", { x: 0, y: b.y - 4, width: W, height: b.h, class: "lane" + (i % 2 ? " alt" : "") });
      var t = el("text", { x: 12, y: b.y + b.h / 2, class: "lanelabel", transform: "rotate(-90 12 " + (b.y + b.h / 2) + ")", "text-anchor": "middle" }); t.textContent = b.name;
    });
    if (state.layout === "lanes") { for (var c = 0; c <= maxL; c++) { var t = el("text", { x: labelW + 44 + colX[c], y: 14, class: "colhead", "text-anchor": "middle" }); t.textContent = String(c + 1); } }
    halos.forEach(function (h) {
      el("circle", { cx: h.x, cy: h.y, r: h.r, class: "halo" + (h.g && critSet[h.g.id] ? " crit" : "") });
      if (!h.g) { var t = el("text", { x: h.x, y: h.y + h.r + 16, "text-anchor": "middle", class: "halolabel" }); t.textContent = "Feeds no gate yet"; }
    });
    function webEdge(a, b) {
      var dx = b.x - a.x, dy = b.y - a.y, len = Math.sqrt(dx * dx + dy * dy) || 1, ux = dx / len, uy = dy / len;
      var mx = (a.x + b.x) / 2 - dy * .16, my = (a.y + b.y) / 2 + dx * .16;
      return "M" + (a.x + ux * 10) + "," + (a.y + uy * 10) + " Q" + mx + "," + my + " " + (b.x - ux * 14) + "," + (b.y - uy * 14);
    }
    d.edges.forEach(function (e) {
      if (window.praxisLinkAt && !window.praxisLinkAt(e[1], e[0])) return;
      if (!pos[e[0]] || !pos[e[1]]) return;
      var a = pos[e[0]], b = pos[e[1]], mx = (a.x + b.x) / 2, crit = critSet[e[0]] && critSet[e[1]];
      var p = el("path", { d: state.layout === "web" ? webEdge(a, b) : (state.layout === "gates" ? (a.gx ? "M" + (a.x + 12) + "," + a.y + " L" + a.gx + "," + a.y + " L" + a.gx + "," + a.yb + " C" + a.gx + "," + ((a.yb + b.y) / 2) + " " + b.x + "," + ((a.yb + b.y) / 2) + " " + b.x + "," + (b.y - 13) : "M" + a.x + "," + (a.y + 10) + " C" + a.x + "," + ((a.y + b.y) / 2) + " " + b.x + "," + ((a.y + b.y) / 2) + " " + b.x + "," + (b.y - 13)) : "M" + (a.x + 9) + "," + a.y + " C" + mx + "," + a.y + " " + mx + "," + b.y + " " + (b.x - 11) + "," + b.y),
        class: "lk" + (crit ? " crit" : "") + (byId[e[0]].kind === "ask" ? " dot" : ""), "marker-end": "url(#" + (crit ? "arc" : "ar") + ")" });
      p.dataset.a = e[0]; p.dataset.b = e[1]; links.push(p);
    });
    shown.forEach(function (n) {
      var P = pos[n.id], cls = "nd " + n.kind + (n.done ? " done" : "") + (n.can ? " can" : "") + (n.tier === "1" ? " t1" : "") + (critSet[n.id] ? " crit" : "");
      var g = el("g", { class: cls, tabindex: "0", role: "button", "aria-label": n.id + " " + n.title }); g.dataset.id = n.id;
      var R = n.done ? 5 : Math.min(17, 6 + Math.sqrt(n.down || 0) * 2.4);
      var tt = document.createElementNS(NS, "title"); tt.textContent = n.id + " · " + n.title + (n.down ? " · " + n.down + " wait on it" : ""); g.appendChild(tt);
      if (n.kind === "ask") el("rect", { x: P.x - R, y: P.y - R, width: R * 2, height: R * 2, transform: "rotate(45 " + P.x + " " + P.y + ")" }, g);
      else if (n.kind === "gate") { el("circle", { cx: P.x, cy: P.y, r: Math.max(9, R) }, g); el("circle", { cx: P.x, cy: P.y, r: 3.5, class: "in" }, g); }
      else el("circle", { cx: P.x, cy: P.y, r: R }, g);
      if (n.down >= 3 && !n.done) { var badge = el("text", { x: P.x, y: P.y + 4, "text-anchor": "middle", class: "dcount" }, g); badge.textContent = n.down; }
      var tag = n.done && n.pr ? n.pr : NAME(n.id) + (n.tier ? " · T" + n.tier : "");
      var t0 = el("text", { x: P.x, y: P.y - R - 7, "text-anchor": "middle", class: "tag" + (n.tier === "1" && !n.done ? " t1" : "") + (n.done && n.pr ? " pr" : "") }, g); t0.textContent = tag;
      if (n.key) wrap(n.title, 17).forEach(function (line, i) { var t = el("text", { x: P.x, y: P.y + R + 12 + i * 12, "text-anchor": "middle", class: "kt" }, g); t.textContent = line; });
      els[n.id] = g;
    });
    host.appendChild(svg);
    apply();
  }
  function apply() {
    var set = null;
    if (state.sel) { set = {}; set[state.sel] = 1; (preds[state.sel] || []).concat(succs[state.sel] || []).forEach(function (k) { set[k] = 1; }); }
    else if (state.mode === "crit") { set = {}; d.crit.forEach(function (k) { set[k] = 1; }); }
    else if (state.mode === "can") { set = {}; d.can.forEach(function (k) { set[k] = 1; }); }
    if (state.owner) { var o = {}; d.nodes.forEach(function (n) { if (n.owner === state.owner && (!set || set[n.id])) o[n.id] = 1; }); set = o; }
    svg.classList.toggle("mode", !!set);
    Object.keys(els).forEach(function (k) { els[k].classList.toggle("on", !!(set && set[k])); els[k].classList.toggle("sel", k === state.sel); });
    links.forEach(function (p) { p.classList.toggle("on", !!(set && set[p.dataset.a] && set[p.dataset.b])); });
  }
  function item(i) { var n = byId[i]; return '<li class="' + (n.done ? "ok" : "todo") + '"><button class="ref" data-go="' + i + '" title="' + i + '">' + esc(NAME(i)) + "</button> " + esc(n.title) + ' <span class="muted">· ' + stateWord(n) + "</span></li>"; }
  function show(id) {
    var n = byId[id]; state.sel = id; apply();
    var kindName = { step: "work", gate: "gate", ask: n.tier ? "tier " + n.tier + " question or decision" : "question or decision", dep: "dependency" }[n.kind];
    var more = n.kind === "gate" ? '<p><a href="' + esc(panel.dataset.cutover || "cutover.html") + "#" + n.id + '">Its card in the cutover plan</a></p>'
      : n.kind === "ask" ? '<p><a href="' + esc(panel.dataset.register || "register.html") + '">In questions and decisions</a></p>' : "";
    panel.innerHTML = '<p class="pk">' + kindName + (critSet[id] ? ' <span class="chip c-open">critical path</span>' : "") + "</p>" +
      '<h3><span class="id" title="' + n.id + '">' + NAME(n.id) + "</span> " + esc(n.title) + '</h3><p class="muted">' + stateWord(n) + (n.owner ? " · " + esc(n.owner) : "") + (n.pr ? " · " + esc(n.pr) : "") + (n.when ? " · " + esc(n.when) : "") + "</p>" + more +
      "<h4>Waits on</h4><ul class=\"checks-list\">" + ((preds[id] || []).map(item).join("") || '<li class="src muted">nothing</li>') + "</ul>" +
      "<h4>Unlocks</h4><ul class=\"checks-list\">" + ((succs[id] || []).map(item).join("") || '<li class="src muted">nothing</li>') + "</ul>";
  }
  function clear() { state.sel = null; apply(); }
  host.addEventListener("click", function (e) { var g = e.target.closest(".nd"); if (g) show(g.dataset.id); else clear(); });
  host.addEventListener("keydown", function (e) { var g = e.target.closest(".nd"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); show(g.dataset.id); } });
  panel.addEventListener("click", function (e) { var b = e.target.closest("[data-go]"); if (b && els[b.dataset.go]) { show(b.dataset.go); els[b.dataset.go].focus(); } });
  document.querySelectorAll("[data-show]").forEach(function (b) { if (!byId[b.dataset.show]) { b.hidden = true; return; } b.addEventListener("click", function () { if (!els[b.dataset.show]) return; show(b.dataset.show); els[b.dataset.show].scrollIntoView({ block: "nearest", inline: "center" }); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") clear(); });
  document.querySelectorAll(".modes button").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".modes button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      state.mode = b.dataset.mode; state.sel = null; apply();
    });
  });
  if (ownerSel) ownerSel.addEventListener("change", function () { state.owner = ownerSel.value; state.sel = null; apply(); });
  [["map-done", "done"], ["map-asks", "asks"]].forEach(function (t) { var c = document.getElementById(t[0]); if (c) c.addEventListener("change", function () { state[t[1]] = c.checked; draw(); }); });
  draw();
})();

// Design: select a slice for how it is built and what it carries.
(function () {
  var rows = document.querySelectorAll("tr.srow");
  if (!rows.length) return;
  function pick(id) {
    rows.forEach(function (r) { r.classList.toggle("sel", r.dataset.slice === id); });
    document.querySelectorAll(".spanel").forEach(function (p) { p.hidden = p.dataset.slice !== id; });
    var e = document.querySelector(".sp-empty"); if (e) e.hidden = true;
  }
  rows.forEach(function (r) {
    r.addEventListener("click", function () { pick(r.dataset.slice); });
    r.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(r.dataset.slice); } });
  });
})();

// Reader tools for every list of rows and every plain table on a tab: filter by the tags its rows carry, and sort.
// Pictures, grids and side panels are left alone; a list with fewer than four rows gets nothing.
(function () {
  var SKIP = ".gpanels, .panel, .tabnote, .codes, .scrs, .metrics, .cutover, .trace, .design";
  function tags(row) {
    var cells = row.matches("tr") ? row.querySelectorAll("td .chip") : row.querySelectorAll(":scope > summary .chip");
    return [].map.call(cells, function (c) { return c.textContent.trim().toLowerCase(); }).filter(Boolean);
  }
  function codeNum(row) {
    var id = row.id || (row.querySelector(".id") || {}).textContent || "";
    var m = /(\d+)\s*$/.exec(id); return m ? +m[1] : 1e9;
  }
  function title(row) { var s = row.querySelector(".shall") || row.cells && row.cells[0]; return s ? s.textContent.trim().toLowerCase() : ""; }
  function natural(a, b) {
    var x = parseFloat(a), y = parseFloat(b);
    if (!isNaN(x) && !isNaN(y) && String(x) === a.replace(/[^\d.\-]/g, "") ) return x - y;
    return a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });
  }
  // Tags that never appear on the same row answer one question (agreed / proposed), so they share a chip row; tags that
  // do co-occur (proposed, record written) get separate rows that combine. One choice per row.
  function tagList(row) {
    var cells = row.matches("tr") ? row.querySelectorAll("td .chip") : row.querySelectorAll(":scope > summary .chip");
    return [].map.call(cells, function (c) { return c.textContent.trim().toLowerCase(); }).filter(Boolean);
  }
  function toolbar(host, rows, parent, sorters) {
    rows.forEach(function (r) { r._tags = tagList(r); });
    var all = [];
    rows.forEach(function (r) { r._tags.forEach(function (t) { if (all.indexOf(t) < 0) all.push(t); }); });
    var together = function (x, y) { return rows.some(function (r) { return r._tags.indexOf(x) >= 0 && r._tags.indexOf(y) >= 0; }); };
    var dims = [];
    all.forEach(function (t) {
      var d = dims.find(function (vals) { return vals.every(function (v) { return !together(v, t); }); });
      if (d) d.push(t); else dims.push([t]);
    });
    dims = dims.map(function (vals) { return { vals: vals }; });
    var want = dims.map(function () { return ""; });
    function apply() { rows.forEach(function (r) { r.hidden = want.some(function (w) { return w && r._tags.indexOf(w) < 0; }); }); }
    var bar = document.createElement("div"); bar.className = "tools";
    var groups = document.createElement("div"); groups.className = "tools-groups";
    dims.forEach(function (dim, d) {
      if (dim.vals.length < 2 && rows.every(function (r) { return r._tags.indexOf(dim.vals[0]) >= 0; })) return;
      var show = document.createElement("div"); show.className = "seg"; show.setAttribute("role", "group");
      var LV = ["high", "medium", "low"], lv = function (v) { var i = LV.indexOf(v.split(" ")[0]); return i < 0 ? 9 : i; };
      [""].concat(dim.vals.sort(function (a, b) { return lv(a) - lv(b) || a.localeCompare(b); })).forEach(function (k) {
        var b = document.createElement("button"); b.type = "button";
        b.setAttribute("aria-pressed", k === "" ? "true" : "false");
        b.textContent = k === "" ? "All" : k;
        b.addEventListener("click", function () {
          want[d] = k; show.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); apply();
        });
        show.appendChild(b);
      });
      groups.appendChild(show);
    });
    if (groups.children.length) { var lab0 = document.createElement("span"); lab0.className = "tools-label"; lab0.textContent = "Show"; bar.appendChild(lab0); bar.appendChild(groups); }
    if (sorters) {
      var lab = document.createElement("label"); lab.className = "tools-sort"; lab.innerHTML = "<span class=\"tools-label\">Sort</span>";
      var sel = document.createElement("select");
      Object.keys(sorters).forEach(function (k) { var o = document.createElement("option"); o.value = k; o.textContent = k; sel.appendChild(o); });
      sel.addEventListener("change", function () { rows.slice().sort(sorters[sel.value]).forEach(function (r) { parent.appendChild(r); }); });
      lab.appendChild(sel); bar.appendChild(lab);
    }
    if (bar.children.length) host.parentNode.insertBefore(bar, host);
  }
  document.querySelectorAll("main .reqs").forEach(function (list) {
    if (list.closest(SKIP) || document.querySelector("main .filters") || list.closest("[data-view]") && list.closest("[data-view]").querySelector(".chipset")) return;
    var rows = [].slice.call(list.querySelectorAll(":scope > details.req"));
    if (rows.length < 4) return;
    rows.forEach(function (r, i) { r.dataset.order = i; });
    toolbar(list, rows, list, null);
  });
  document.querySelectorAll("main .tbl > table").forEach(function (table) {
    if (table.closest(SKIP) || table.matches(".dots, .gantt, .tgrid") || !table.tBodies[0]) return;
    var rows = [].slice.call(table.tBodies[0].rows);
    if (rows.length < 4) return;
    var head = table.tHead && table.tHead.rows[0];
    if (head && !head.querySelector("[data-sortable]")) {
      [].forEach.call(head.cells, function (th, i) {
        th.classList.add("sortable"); th.tabIndex = 0; var dir = 0;
        function sort() {
          dir = dir === 1 ? -1 : 1;
          [].forEach.call(head.cells, function (o) { o.removeAttribute("aria-sort"); });
          th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
          rows.slice().sort(function (a, b) {
            var x = a.cells[i] ? (a.cells[i].dataset.sort || a.cells[i].textContent.trim()) : "", y = b.cells[i] ? (b.cells[i].dataset.sort || b.cells[i].textContent.trim()) : "";
            return dir * natural(x, y);
          }).forEach(function (r) { table.tBodies[0].appendChild(r); });
        }
        th.addEventListener("click", sort);
        th.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sort(); } });
      });
    }
    toolbar(table.parentNode, rows, table.tBodies[0], null);
  });
})();

// The view picker: a tab drawing more than one eligible visual offers each, the visual-library's first shown first.
// It shows only once this script runs, so a page read without scripts never offers a dead control.
document.documentElement.classList.add("js");
// A deep link (#view=<name>) wins over the reader's last choice on this device, which wins over the default.
(function () {
  document.querySelectorAll(".views").forEach(function (box) {
    var key = "praxis-view:" + location.pathname + ":" + box.dataset.tab, btns = box.querySelectorAll(".picker button");
    function pick(v, keep) {
      var btn = box.querySelector('.picker button[data-v="' + v + '"]');
      if (!btn) return;
      btns.forEach(function (x) { x.setAttribute("aria-pressed", x === btn ? "true" : "false"); });
      var why = box.querySelector(".why");
      if (why) why.hidden = v !== why.dataset.first;
      box.dataset.shown = v; box.dataset.layout = btn.dataset.layout || "";
      box.querySelectorAll(".viewbody").forEach(function (b) { b.hidden = b.dataset.body !== btn.dataset.body; });
      box.dispatchEvent(new CustomEvent("praxis:view", { detail: { view: v, layout: btn.dataset.layout } }));
      if (keep) { try { localStorage.setItem(key, v); } catch (e) {} }
    }
    btns.forEach(function (x) { x.addEventListener("click", function () { pick(x.dataset.v, true); }); });
    function offered(v) { return v && box.querySelector('.picker button[data-v="' + v + '"]') ? v : null; }
    function linked() { var m = /(?:^|[#&])view=([\w-]+)/.exec(location.hash); return offered(m && m[1]); }
    var saved = null;
    try { saved = offered(localStorage.getItem(key)); } catch (e) {}
    var want = linked() || saved;
    if (want && want !== box.dataset.default) pick(want, false);
    window.addEventListener("hashchange", function () { var v = linked(); if (v) pick(v, false); });
  });
})();

// --- visuals: ws1 ---
// Since you last looked: count from the reader's previous visit on this device, kept per site; a visit today keeps the
// one before it, so reloading doesn't empty the list. Without a recorded visit the page keeps the renderer's default week.
(function () {
  document.querySelectorAll(".since-visit").forEach(function (box) {
    var key = "praxis-visit:" + location.pathname.replace(/[^/]*$/, ""), now = new Date(), today = new Date(now - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10), seen = null;
    try { seen = JSON.parse(localStorage.getItem(key) || "null"); } catch (e) {}
    var prev = seen && (seen.last === today ? seen.prev : seen.last);
    try { localStorage.setItem(key, JSON.stringify({ prev: prev || null, last: today })); } catch (e) {}
    if (!prev) return;
    var words = JSON.parse(box.dataset.words), counts = {}, order = [], shown = 0;
    box.querySelectorAll(".sv-list li").forEach(function (li) {
      var on = li.dataset.when > prev, w = li.querySelector(".chip").textContent;
      li.hidden = !on;
      if (on) { shown++; if (!counts[w]) { counts[w] = 0; order.push(w); } counts[w]++; }
    });
    var day = new Date(prev + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short" });
    box.querySelector(".sv-head").textContent = shown ? "Since your last visit, " + day + ": " + order.map(function (w) { return counts[w] + " " + words[w]; }).join(", ") + "." : "Nothing has changed since your last visit, " + day + ".";
    box.querySelector(".sv-note").hidden = true;
  });
})();

// --- reading: ws1 ---
// Hover previews and search, both read from the page's praxis-cards: one card per item, and the tabs it can live on.
// The cards follow this script on the page, so everything here waits for the document to be parsed.
function praxisReady(fn) { if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn); else fn(); }
praxisReady(function () {
  var src = document.getElementById("praxis-cards");
  if (!src) return;
  var D; try { D = JSON.parse(src.textContent); } catch (e) { return; }
  var C = {}; D.cards.forEach(function (c) { C[c[0]] = c; });
  var ID = /^([A-Z][A-Z0-9]*-\d+)$/;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function tone(st) { return /agreed|recorded|holds|met|done|merged|closed|mitigated/.test(st) ? "c-holds" : /open|fails|blocked|late/.test(st) ? "c-open" : /lean|proposed|draft|planned/.test(st) ? "c-unsettled" : "c-unchecked"; }
  function where(c) { return c[9] >= 0 ? D.tabs[c[9]] : null; }
  window.PRAXIS_CARDS = { byId: C, tabs: D.tabs, where: where, esc: esc, tone: tone };

  // The id an element stands for: a data-go or data-show button, an abbr whose title starts with the id, or an id span.
  function idOf(el) {
    if (!el || !el.closest) return null;
    var t = el.closest("abbr[data-pid], abbr[title], .id, button.ref[data-go], [data-show], .tchip, .nd[data-id], .gbtn[data-gate]");
    if (!t || t.closest(".pv")) return null;
    var v = t.dataset.pid || t.dataset.go || t.dataset.show || t.dataset.id || t.dataset.gate || (t.getAttribute("title") || "").split(" · ")[0] || t.textContent.trim();
    if (!ID.test(v)) v = t.textContent.trim();
    return ID.test(v) && C[v] ? { id: v, el: t } : null;
  }
  // An abbr's native tooltip would double the card, so its title moves to data-pid once the page has cards; it stays focusable.
  document.querySelectorAll("abbr[title]").forEach(function (a) {
    var v = a.getAttribute("title").split(" · ")[0];
    if (C[v]) { a.dataset.pid = v; a.setAttribute("aria-label", a.textContent + ", " + a.getAttribute("title")); a.removeAttribute("title"); a.tabIndex = 0; }
  });

  var pv = document.createElement("div"), cur = null, hideT = null;
  pv.className = "pv"; pv.id = "praxis-preview"; pv.setAttribute("role", "tooltip"); pv.hidden = true;
  document.body.appendChild(pv);
  function show(hit) {
    clearTimeout(hideT);
    if (cur === hit.el && !pv.hidden) return;
    cur = hit.el;
    var c = C[hit.id], w = where(c), due = c[5] ? " · due " + esc(ID.test(c[5]) ? NAME(c[5]) : c[5]) : "";
    pv.innerHTML = '<div class="pvhead"><span class="id">' + esc(c[0]) + '</span><span class="chip ' + tone(c[3]) + '">' + esc(c[3] || "—") + "</span>" +
      '<span class="muted">' + esc(c[1]) + (c[4] ? " · " + esc(c[4]) : "") + due + "</span></div>" +
      "<b>" + esc(c[2]) + "</b>" + (c[6] && c[6] !== c[2] ? "<p>" + esc(c[6]) + "</p>" : "") +
      '<div class="pvfoot">' + (w ? '<a href="' + esc(w[1]) + "#sel=" + esc(c[0]) + '">Open on ' + esc(w[0]) + " →</a>" : "") +
      '<span class="muted">' + c[7] + " waits · " + c[8] + " unlocks</span></div>";
    pv.hidden = false;
    hit.el.setAttribute("aria-describedby", "praxis-preview");
    place();
  }
  // The card sits under its id, or above it when there is no room below, and follows it while the page scrolls.
  function place() {
    var r = cur.getBoundingClientRect(), W = Math.min(pv.offsetWidth, innerWidth - 16), H = pv.offsetHeight;
    if (r.bottom < 0 || r.top > innerHeight) { hide(true); return; }
    var x = Math.max(8, Math.min(r.left, innerWidth - W - 8)), y = r.bottom + 8 + H > innerHeight && r.top - 8 - H > 0 ? r.top - 8 - H : r.bottom + 8;
    pv.style.left = x + "px"; pv.style.top = y + "px";
  }
  function hide(now) {
    clearTimeout(hideT);
    hideT = setTimeout(function () { pv.hidden = true; if (cur) cur.removeAttribute("aria-describedby"); cur = null; }, now ? 0 : 180);
  }
  document.addEventListener("mouseover", function (e) { var h = idOf(e.target); if (h) show(h); else if (!e.target.closest(".pv")) hide(); });
  document.addEventListener("focusin", function (e) { var h = idOf(e.target); if (h) show(h); else if (!e.target.closest(".pv")) hide(true); });
  // A tap on an id that does nothing else opens its card; an id that is a control keeps its own action.
  document.addEventListener("click", function (e) {
    var h = idOf(e.target);
    if (h && !h.el.matches("button, a, [role=button]")) { show(h); } else if (!e.target.closest(".pv")) hide(true);
  });
  pv.addEventListener("mouseover", function () { clearTimeout(hideT); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !pv.hidden) { e.stopPropagation(); hide(true); } }, true);
  addEventListener("scroll", function () { if (!pv.hidden && cur) place(); }, { passive: true, capture: true });

  // Search: items, terms and decisions across every tab, opened by the bar's button or Cmd/Ctrl+K.
  var bar = document.querySelector(".bar");
  var dlg = document.createElement("div"), last = null;
  dlg.className = "srch"; dlg.hidden = true; dlg.setAttribute("role", "dialog"); dlg.setAttribute("aria-modal", "true"); dlg.setAttribute("aria-label", "Search the set");
  dlg.innerHTML = '<div class="srbox"><label class="vh" for="praxis-q">Search items, terms and decisions</label>' +
    '<input id="praxis-q" type="search" autocomplete="off" placeholder="Search items, terms and decisions" role="combobox" aria-expanded="true" aria-controls="praxis-hits" aria-autocomplete="list">' +
    '<ul id="praxis-hits" role="listbox" aria-label="Results"></ul><p class="srnote muted"></p></div>';
  document.body.appendChild(dlg);
  var q = dlg.querySelector("input"), list = dlg.querySelector("ul"), note = dlg.querySelector(".srnote"), hits = [], at = 0;
  // Every word must appear in the card's id, title, kind or excerpt. Then: the exact id, a title holding every word with the
  // first word at its start, a title holding every word, anything else; within a tier, the store's order.
  function rank(c, words) {
    var hay = (c[0] + " " + c[2] + " " + c[1] + " " + c[6]).toLowerCase(), t = c[2].toLowerCase();
    for (var i = 0; i < words.length; i++) { if (hay.indexOf(words[i]) < 0) return -1; }
    if (c[0].toLowerCase() === words.join(" ")) return 3;
    if (words.every(function (w) { return t.indexOf(w) >= 0; })) return t.indexOf(words[0]) === 0 ? 2 : 1;
    return 0;
  }
  function paint() {
    list.innerHTML = hits.map(function (c, i) {
      var w = where(c);
      return '<li role="option" id="praxis-hit-' + i + '" aria-selected="' + (i === at) + '"><a href="' + (w ? esc(w[1]) + "#sel=" + esc(c[0]) : "#") + '">' +
        '<span class="id">' + esc(c[0]) + "</span><span>" + esc(c[2]) + '</span><span class="muted">' + esc(w ? w[0] : c[1]) + "</span></a></li>";
    }).join("");
    q.setAttribute("aria-activedescendant", hits.length ? "praxis-hit-" + at : "");
    var sel = list.children[at]; if (sel) sel.scrollIntoView({ block: "nearest" });
  }
  function find() {
    var words = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    hits = !words.length ? [] : D.cards.map(function (c, n) { return [rank(c, words), c, n]; }).filter(function (x) { return x[0] >= 0; })
      .sort(function (a, b) { return b[0] - a[0] || a[2] - b[2]; }).slice(0, 8).map(function (x) { return x[1]; });
    at = 0; paint();
    var held = D.restricted ? " " + D.restricted + " restricted item" + (D.restricted === 1 ? " is" : "s are") + " held apart and not searched." : "";
    note.textContent = (!words.length ? "Type an id, a word from a title, or a term. Keys: 1–9 open a tab, V the next view, arrows walk the map." : hits.length ? "↑ ↓ to move, Enter to open, Esc to close." : "Nothing matches.") + held;
  }
  function open() { last = document.activeElement; dlg.hidden = false; q.value = ""; find(); q.focus(); }
  function close() { dlg.hidden = true; if (last && last.focus) last.focus(); }
  q.addEventListener("input", find);
  q.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); if (hits.length) { at = (at + (e.key === "ArrowDown" ? 1 : hits.length - 1)) % hits.length; paint(); } }
    else if (e.key === "Enter" && hits[at]) { e.preventDefault(); list.children[at].querySelector("a").click(); }
    else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(); }
  });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); else if (e.target.closest("#praxis-hits a")) dlg.hidden = true; });
  document.addEventListener("keydown", function (e) { if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); dlg.hidden ? open() : close(); } });
  var tools = praxisTools(), b = document.createElement("button");
  b.type = "button"; b.className = "sbtn";
  b.innerHTML = 'Search <kbd>' + (/Mac|iP/.test(navigator.platform) ? "⌘" : "Ctrl ") + "K</kbd>";
  b.addEventListener("click", open);
  if (tools) tools.insertBefore(b, tools.firstChild);
});

// The reader's tools in the top row, before the Sources and Codes keys: search, the link to this view, the theme.
function praxisTools() {
  var t = document.querySelector(".rtools"), row = document.querySelector(".bar .toprow");
  if (t || !row) return t;
  t = document.createElement("div"); t.className = "rtools";
  row.insertBefore(t, row.querySelector("details"));
  return t;
}

// Theme: the reader's system until they choose, then their choice, kept on this device. Set before anything draws. The
// control is a small menu button at the end of the top row, beside Sources and Codes; cobalt stays for content choices.
(function () {
  var KEY = "praxis-theme", root = document.documentElement, pick = "system";
  try { pick = localStorage.getItem(KEY) || "system"; } catch (e) {}
  function set(v) { if (v === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", v); pick = v; }
  set(pick);
  var SVG = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">';
  var ICON = {
    system: SVG + '<circle cx="8" cy="8" r="6"/><path d="M8 2a6 6 0 0 1 0 12z" fill="currentColor" stroke="none"/></svg>',
    dark: SVG + '<path d="M13.2 9.6A5.6 5.6 0 1 1 6.4 2.8a4.4 4.4 0 0 0 6.8 6.8z"/></svg>',
    light: SVG + '<circle cx="8" cy="8" r="2.8"/><path d="M8 1.2v1.6M8 13.2v1.6M1.2 8h1.6M13.2 8h1.6M3.2 3.2l1.1 1.1M11.7 11.7l1.1 1.1M3.2 12.8l1.1-1.1M11.7 4.3l1.1-1.1"/></svg>'
  };
  var NAMES = [["system", "System"], ["dark", "Dark"], ["light", "Light"]];
  praxisReady(function () {
    var row = document.querySelector(".bar .toprow");
    if (!row) return;
    var wrap = document.createElement("div");
    wrap.className = "tmenu";
    wrap.innerHTML = '<button type="button" class="tbtn" aria-haspopup="menu" aria-expanded="false" aria-controls="praxis-theme-menu"></button>' +
      '<div class="tlist" id="praxis-theme-menu" role="menu" aria-label="Theme" hidden>' +
      NAMES.map(function (n) { return '<button type="button" role="menuitemradio" data-theme="' + n[0] + '">' + ICON[n[0]] + "<span>" + n[1] + '</span><i class="tchk" aria-hidden="true">✓</i></button>'; }).join("") + "</div>";
    row.appendChild(wrap);
    var btn = wrap.querySelector(".tbtn"), menu = wrap.querySelector(".tlist"), items = Array.prototype.slice.call(menu.querySelectorAll("[role=menuitemradio]"));
    function paint() {
      var label = NAMES.filter(function (n) { return n[0] === pick; })[0][1];
      btn.innerHTML = ICON[pick]; btn.setAttribute("aria-label", "Theme: " + label); btn.title = "Theme: " + label;
      items.forEach(function (x) { x.setAttribute("aria-checked", x.dataset.theme === pick ? "true" : "false"); });
    }
    function open(focusAt) {
      menu.hidden = false; btn.setAttribute("aria-expanded", "true");
      var k = items.findIndex(function (x) { return x.dataset.theme === pick; });
      items[focusAt === "last" ? items.length - 1 : focusAt === "first" ? 0 : Math.max(0, k)].focus();
    }
    function close(back) { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); if (back) btn.focus(); }
    function choose(x) { set(x.dataset.theme); try { localStorage.setItem(KEY, pick); } catch (e) {} paint(); close(true); }
    btn.addEventListener("click", function () { menu.hidden ? open() : close(false); });
    btn.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); open(e.key === "ArrowDown" ? "first" : "last"); }
    });
    menu.addEventListener("click", function (e) { var x = e.target.closest("[role=menuitemradio]"); if (x) choose(x); });
    menu.addEventListener("keydown", function (e) {
      var k = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); items[(k + (e.key === "ArrowDown" ? 1 : items.length - 1)) % items.length].focus(); }
      else if (e.key === "Home" || e.key === "End") { e.preventDefault(); items[e.key === "Home" ? 0 : items.length - 1].focus(); }
      else if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(true); }
      else if (e.key === "Tab") close(false);
    });
    document.addEventListener("click", function (e) { if (!menu.hidden && !wrap.contains(e.target)) close(false); });
    paint();
  });
})();

// Deep links: the address holds what the reader sees (view, map mode and owner, a tab's filters, the selection and the
// lens) and follows it as they change it, so a pasted link opens the same. A bare #<id>, the older form, is a selection.
praxisReady(function () {
  var main = document.querySelector("main");
  if (!main) return;
  function parse() {
    var h = location.hash.slice(1), o = {};
    if (/^[A-Z][A-Z0-9]*-\d+$/.test(h)) return { sel: h };
    h.split("&").forEach(function (kv) { var i = kv.indexOf("="); if (i > 0) o[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1)); });
    return o;
  }
  function q(sel) { return document.querySelector(sel); }
  var keepView = false;  // a link that names its view keeps it: a selection hidden there stays unshown
  function seen(sel) {
    var all = Array.prototype.slice.call(document.querySelectorAll(sel)), vis = all.filter(function (x) { return x.getClientRects().length; });
    if (vis.length || !all.length || keepView) return vis[0] || null;
    var body = all[0].closest(".viewbody[hidden]"), box = body && body.closest(".views");
    var btn = box && box.querySelector('.picker button[data-body="' + body.dataset.body + '"]');
    if (btn) { btn.click(); return all[0].getClientRects().length ? all[0] : null; }
    return null;
  }
  function select(id) {
    var esc = window.CSS && CSS.escape ? CSS.escape(id) : id, t = seen('.nd[data-id="' + esc + '"]') || seen('.gbtn[data-gate="' + esc + '"]');
    if (t) { t.dispatchEvent(new MouseEvent("click", { bubbles: true })); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest", inline: "center" }); return; }
    t = seen("#" + esc) || seen('[data-item="' + esc + '"]') || seen('abbr[data-pid="' + esc + '"]');
    if (t) { t.scrollIntoView({ block: "center" }); t.classList.add("hit"); setTimeout(function () { t.classList.remove("hit"); }, 2400); }
  }
  function apply(o) {
    if (o.mode) { var m = q('.modes button[data-mode="' + o.mode + '"]'); if (m) m.click(); }
    if (o.owner) { var ow = q("#map-owner"); if (ow) { ow.value = o.owner; ow.dispatchEvent(new Event("change")); } }
    Object.keys(o).forEach(function (k) {
      if (k.indexOf("f-") === 0) { var f = q('[data-filter="' + k.slice(2) + '"] [data-v="' + o[k] + '"]'); if (f) f.click(); }
    });
    if (window.praxisTravel) window.praxisTravel(o.at || "");
    if (window.praxisLens) window.praxisLens(o.lens || "");  // set before selecting, so a selection lands on what the lens shows
    keepView = !!o.view;
    if (o.sel) select(o.sel);
  }
  function state() {
    var o = [], box = q(".views[data-shown]"), m = q('.modes button[aria-pressed="true"]'), ow = q("#map-owner"), s = q(".nd.sel") || q('.gbtn[aria-pressed="true"]');
    if (box && box.dataset.shown !== box.dataset.default) o.push(["view", box.dataset.shown]);
    if (m && m.dataset.mode !== "all") o.push(["mode", m.dataset.mode]);
    if (ow && ow.value) o.push(["owner", ow.value]);
    document.querySelectorAll("[data-filter]").forEach(function (g) {
      var b = g.querySelector('[data-v][aria-pressed="true"]'); if (b && b.dataset.v) o.push(["f-" + g.dataset.filter, b.dataset.v]);
    });
    if (s) o.push(["sel", s.dataset.id || s.dataset.gate]);
    if (document.documentElement.dataset.lens) o.push(["lens", document.documentElement.dataset.lens]);
    if (document.documentElement.dataset.at) o.push(["at", document.documentElement.dataset.at]);
    return o.map(function (kv) { return encodeURIComponent(kv[0]) + "=" + encodeURIComponent(kv[1]); }).join("&");
  }
  var t = null;
  function follow() { clearTimeout(t); t = setTimeout(function () { var h = state(); try { history.replaceState(null, "", h ? "#" + h : location.pathname + location.search); } catch (e) {} }, 60); }
  window.praxisFollow = follow;
  window.praxisSelect = select;
  ["click", "change", "keyup", "praxis:view"].forEach(function (ev) { document.addEventListener(ev, follow, true); });
  if (location.hash) { apply(parse()); follow(); }
  window.addEventListener("hashchange", function () { apply(parse()); });

  var tools = praxisTools();
  if (tools) {
    var c = document.createElement("button");
    c.type = "button"; c.className = "sbtn copy"; c.textContent = "Copy link to this view";
    c.addEventListener("click", function () {
      var url = location.href, done = function () { c.textContent = "Link copied"; c.classList.add("ok"); setTimeout(function () { c.textContent = "Copy link to this view"; c.classList.remove("ok"); }, 2000); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { prompt("Copy this link", url); });
      else prompt("Copy this link", url);
    });
    tools.appendChild(c);
  }
});

// Keyboard: 1–9 open the tabs in the bar's order, V the next view, arrows walk the map from a node to those it links.
praxisReady(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".bar nav a"));
  var md = document.getElementById("map-data"), preds = {}, succs = {};
  if (md) { try { JSON.parse(md.textContent).edges.forEach(function (e) { (preds[e[1]] = preds[e[1]] || []).push(e[0]); (succs[e[0]] = succs[e[0]] || []).push(e[1]); }); } catch (e) {} }
  var walk = { from: null, k: 0 };
  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey || e.target.closest("input, textarea, select, [contenteditable]")) return;
    var nd = e.target.closest && e.target.closest("#map-graph .nd");
    if (nd && /^Arrow/.test(e.key)) {
      var id = nd.dataset.id, base = walk.from && walk.from !== id && (preds[walk.from] || []).concat(succs[walk.from] || []).indexOf(id) >= 0 ? walk.from : id;
      var list = e.key === "ArrowRight" ? succs[id] : e.key === "ArrowLeft" ? preds[id] : (preds[base] || []).concat(succs[base] || []);
      if (!list || !list.length) return;
      e.preventDefault();
      var at = list.indexOf(id), next = e.key === "ArrowRight" || e.key === "ArrowLeft" ? list[0]
        : at < 0 ? list[e.key === "ArrowDown" ? 0 : list.length - 1] : list[(at + (e.key === "ArrowDown" ? 1 : list.length - 1)) % list.length];
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") walk.from = id; else walk.from = base;
      var g = document.querySelector('#map-graph .nd[data-id="' + next + '"]');
      if (g) { g.focus(); g.dispatchEvent(new MouseEvent("click", { bubbles: true })); }
      return;
    }
    if (/^[1-9]$/.test(e.key) && tabs[+e.key - 1]) { e.preventDefault(); tabs[+e.key - 1].click(); return; }
    if (e.key === "v" || e.key === "V") {
      var btns = Array.prototype.slice.call(document.querySelectorAll(".views .picker button"));
      if (!btns.length) return;
      e.preventDefault();
      var on = btns.findIndex(function (b) { return b.getAttribute("aria-pressed") === "true"; });
      btns[(on + 1) % btns.length].click(); btns[(on + 1) % btns.length].focus();
    }
  });
});

// Motion: a view the picker shows comes in with a short fade; the reader's reduced-motion setting turns it off (in the CSS).
praxisReady(function () {
  document.querySelectorAll(".views").forEach(function (box) {
    box.addEventListener("praxis:view", function () {
      box.querySelectorAll(".viewbody:not([hidden])").forEach(function (b) { b.classList.remove("enter"); void b.offsetWidth; b.classList.add("enter"); });
    });
  });
});

// The one-page brief: the status tab offers it, and the print stylesheet shows it alone, in the light palette.
praxisReady(function () {
  var brief = document.querySelector(".brief"), hero = document.querySelector(".hero");
  if (!brief || !hero) return;
  var b = document.createElement("button");
  b.type = "button"; b.className = "sbtn"; b.textContent = "Print the one-page brief";
  b.addEventListener("click", function () { window.print(); });
  hero.appendChild(b);
});

// Explain this: ask Claude, on the viewer's own account and only for them, to explain the instrument in view. It shows only
// where the artifact runtime offers sampling; the first ask in a view asks the viewer's consent.
praxisReady(function () {
  var hosts = document.querySelectorAll(".xhost");
  if (!hosts.length || !window.claude || !claude.use) return;
  var HIDE = ["not_granted", "sampling_disabled", "not_declared", "capability_disabled", "capability_removed"];
  var ID = /\b[A-Z][A-Z0-9]*-\d+\b/g;
  function hideAll() { hosts.forEach(function (h) { h.querySelector(".xbtn").hidden = true; }); }
  function idsInto(el, text) {  // ids in the answer become previewable, the text itself set as text
    el.textContent = "";
    var at = 0, m, C = (window.PRAXIS_CARDS || {}).byId || {};
    ID.lastIndex = 0;
    while ((m = ID.exec(text))) {
      el.appendChild(document.createTextNode(text.slice(at, m.index)));
      if (C[m[0]]) { var a = document.createElement("abbr"); a.dataset.pid = m[0]; a.tabIndex = 0; a.textContent = m[0]; el.appendChild(a); }
      else el.appendChild(document.createTextNode(m[0]));
      at = m.index + m[0].length;
    }
    el.appendChild(document.createTextNode(text.slice(at)));
  }
  // The instrument's own text (the view shown, never the button or an answer), its named items' cards, and the tab's
  // context, trimmed to stay under the 64 KiB a sample may carry; the prompt says when it was cut.
  function data(host) {
    var shown = host.querySelector(".viewbody:not([hidden])"), box = host.querySelector(".views"), pick = box && box.querySelector('.picker button[aria-pressed="true"]');
    var text = shown ? shown.innerText : Array.prototype.filter.call(host.children, function (c) { return !c.matches(".xbar, .xout"); }).map(function (c) { return c.innerText; }).join("\n");
    text = (text || "").replace(/\n{3,}/g, "\n\n");
    var C = (window.PRAXIS_CARDS || {}).byId || {}, ids = {}, cards = [];
    (text.match(ID) || []).forEach(function (i) { if (C[i] && !ids[i]) { ids[i] = 1; var c = C[i]; cards.push([c[0], c[1], c[2], c[3], c[4], c[10] || ""].join(" | ")); } });
    var h1 = document.querySelector(".hero h1"), tab = document.querySelector('.bar nav a[aria-current="page"]');
    var head = "Explain one chart on a project's documentation page to the reader looking at it.\n" +
      "Write plain prose, at most 150 words: what the chart shows, what it concludes, and what the reader might do next. " +
      "Cite every item you mention by its id exactly as written (such as Q-4). Use only the data below; where it doesn't say, say that it doesn't. No headings, no lists.\n\n" +
      "Tab: " + (tab ? tab.textContent : document.title) + "\nPage headline: " + (h1 ? h1.innerText : "") + "\nView: " + (pick ? pick.textContent : host.dataset.instrument);
    var size = function (x) { return new TextEncoder().encode(x).length; }, nText = text.length, nCards = cards.length, out;
    for (;;) {
      var cut = (nText < text.length ? "\n(The chart's text was cut short here.)" : "") + (nCards < cards.length ? "\n(" + (cards.length - nCards) + " more items it names were not sent.)" : "");
      out = head + "\n\nWhat the chart shows, as text:\n" + text.slice(0, nText) + "\n\nThe items it names (id | kind | title | state | who decides or owns it | due date):\n" + cards.slice(0, nCards).join("\n") + cut;
      if (size(out) < 60000) return out;
      if (nCards > 20) nCards = Math.floor(nCards / 2); else nText = Math.floor(nText * 0.8);
    }
  }
  claude.use("sample").then(function (sample) {
    if (!sample) return;
    hosts.forEach(function (host) {
      var btn = host.querySelector(".xbtn"), out = host.querySelector(".xout"), ctl = null;
      btn.hidden = false;
      function reset() { ctl = null; btn.textContent = "Explain this"; }
      btn.addEventListener("click", function () {
        if (ctl) { ctl.abort(); return; }
        ctl = new AbortController();
        btn.textContent = "Stop"; out.hidden = false;
        out.innerHTML = '<p class="xtext">Thinking…</p><p class="xnote muted">Only you see this answer; it runs on your own Claude account.</p>';
        var p = out.querySelector(".xtext");
        var call;
        try { call = sample(data(host), { signal: ctl.signal, modelTier: "quick", onText: function (u) { p.textContent = u.text; } }); }
        catch (err) { p.textContent = "The answer was interrupted; try again."; reset(); return; }
        call
          .then(function (r) { idsInto(p, r.text + (r.truncated ? " …(cut short)" : "")); })
          .catch(function (e) {
            e = e && typeof e === "object" ? e : { code: "upstream_error" };
            if (e.code === "cancelled") { if (e.text) idsInto(p, e.text); else out.hidden = true; return; }
            if (HIDE.indexOf(e.code) >= 0) { out.hidden = true; hideAll(); return; }
            if (e.code === "refused") { p.textContent = "Claude didn't answer this one."; return; }
            p.textContent = (e.text ? e.text + "\n\n" : "") + (e.code === "rate_limited" ? "Too many questions just now; try again in a minute."
              : e.code === "session_expired" ? "Sign in to Claude again to ask." : e.code === "prompt_too_large" ? "This view holds too much to send; narrow it with a filter."
              : "The answer was interrupted; try again.");
          })
          .then(reset, reset);
      });
    });
  }, function () {});
});

// Reader lenses: on the status tab, "Reading as" re-ranks the tab for one kind of reader; Everyone is the whole tab.
praxisReady(function () {
  var panels = document.querySelectorAll(".lens[data-lens]"), hero = document.querySelector(".hero"), main = document.querySelector("main");
  if (!panels.length || !hero) return;
  var g = document.createElement("div"), names = [["", "Everyone"]];
  panels.forEach(function (p) { names.push([p.dataset.lens, p.dataset.lens.charAt(0).toUpperCase() + p.dataset.lens.slice(1)]); });
  g.className = "lensrow";
  g.innerHTML = '<span class="muted">Reading as</span><div class="picker" role="group" aria-label="Reader lens">' +
    names.map(function (n) { return '<button type="button" data-l="' + n[0] + '" aria-pressed="' + (n[0] === "") + '">' + n[1] + "</button>"; }).join("") + "</div>";
  hero.appendChild(g);
  function set(name) {
    var on = null;
    panels.forEach(function (p) { p.hidden = p.dataset.lens !== name; if (!p.hidden) on = p; });
    if (!on) name = "";
    main.classList.toggle("lensing", !!on);
    if (name) document.documentElement.dataset.lens = name; else delete document.documentElement.dataset.lens;
    g.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.l === name ? "true" : "false"); });
    if (window.praxisFollow) window.praxisFollow();
  }
  window.praxisLens = set;
  g.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) set(b.dataset.l); });
  document.querySelectorAll(".lall").forEach(function (b) { b.addEventListener("click", function () { set(""); }); });
  var m = /(?:^|[#&])lens=(\w+)/.exec(location.hash);
  if (m) set(m[1]);
});

// Time travel on the map: a date control redraws the map as it stood on a day the store dates something. An item
// appears on the day it was filed, and turns done on the day its kind's own event dates it; links, wording and positions
// stay as they are today. The map asks praxisFiledAt and praxisDoneAt on each draw.
praxisReady(function () {
  var host = document.getElementById("map-graph"), C = (window.PRAXIS_CARDS || {}).byId, md = document.getElementById("map-data");
  if (!host || !C || !md) return;
  var onMap = {}; try { JSON.parse(md.textContent).nodes.forEach(function (n) { onMap[n.id] = 1; }); } catch (e) { return; }
  var today = new Date(), iso = new Date(today - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10), days = {};
  var undatedLinks = false;
  Object.keys(C).forEach(function (k) {
    C[k].slice(11, 15).forEach(function (d) { if (d && d <= iso) days[d] = 1; });
    Object.keys(C[k][15] || {}).forEach(function (e) { if (C[k][15][e] <= iso) days[C[k][15][e]] = 1; });
  });
  try { JSON.parse(md.textContent).edges.forEach(function (e) { var c = C[e[1]]; if (!(c && c[15] && c[15][e[1] + ">" + e[0]])) undatedLinks = true; }); } catch (e) {}
  var dates = Object.keys(days).sort();
  if (dates.length < 2) return;  // one dated day gives nothing to travel between
  if (dates[dates.length - 1] !== iso) dates.push(iso);
  var row = document.createElement("div"), at = "";
  row.className = "tt";
  var NOTE = undatedLinks
    ? "Only when items were filed and when they were agreed, merged or run go back, and links that carry the day they were filed. Other links, wording and places on the map are today's, so an item filed later leaves a gap, and an item done with no date stays done."
    : "Items and links go back as the store dates them, and today's done items turn done on their dated day. Wording and places on the map are today's, so an item filed later leaves a gap.";
  row.innerHTML = '<label for="praxis-at">As it stood on</label><input id="praxis-at" type="range" min="0" max="' + (dates.length - 1) + '" step="1" value="' + (dates.length - 1) + '">' +
    '<output for="praxis-at"></output><button type="button" class="sbtn ttnow" hidden>Back to today</button>' +
    '<span class="muted small ttnote"></span><details class="ttwhy"><summary aria-label="What goes back in time">?</summary><p></p></details>';
  var slot = document.querySelector(".mapctl .ttslot"), anchor = host.closest(".trace") || host;
  if (slot) slot.appendChild(row); else anchor.parentNode.insertBefore(row, anchor);
  row.querySelector(".ttwhy p").textContent = NOTE;
  var input = row.querySelector("input"), out = row.querySelector("output"), now = row.querySelector(".ttnow"), note = row.querySelector(".ttnote");
  function fmt(d) { return new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }); }
  // An item with no card (restricted) or no filed date is taken as always there.
  window.praxisFiledAt = function (id) { var c = C[id]; return !at || !c || !c[11] || c[11] <= at; };
  // A blocked-by link is stored on the waiting item; one with a since after the day isn't drawn.
  window.praxisLinkAt = function (from, to) { var c = C[from], d = c && c[15] && c[15][from + ">" + to]; return !at || !d || d <= at; };
  window.praxisDoneAt = function (id, doneToday) {
    var c = C[id], on = c && [c[12], c[13], c[14]].filter(Boolean).sort()[0];
    return !doneToday ? false : !at || !on || on <= at;
  };
  var firstOnMap = Object.keys(onMap).map(function (k) { return C[k] && C[k][11]; }).filter(Boolean).sort()[0];
  function set(d) {
    var k = d ? dates.indexOf(d) : dates.length - 1;
    if (k < 0) { k = 0; for (var j = 0; j < dates.length; j++) { if (dates[j] <= d) k = j; } }
    at = k === dates.length - 1 ? "" : dates[k];
    input.value = k; out.textContent = at ? fmt(at) : "today";
    now.hidden = !at; row.classList.toggle("past", !!at);
    if (at) document.documentElement.dataset.at = at; else delete document.documentElement.dataset.at;
    document.dispatchEvent(new CustomEvent("praxis:travel"));
    var empty = at && !host.querySelector(".nd");
    note.textContent = empty ? "Nothing on the map was filed yet; the first was filed on " + (firstOnMap ? fmt(firstOnMap) : "a later day") + "."
      : at ? (undatedLinks ? "Links and wording are today's." : "Wording and places are today's.") : "";
    if (window.praxisFollow) window.praxisFollow();
  }
  window.praxisTravel = set;
  input.addEventListener("input", function () { set(dates[+input.value]); });
  now.addEventListener("click", function () { set(""); });
  var m = /(?:^|[#&])at=(\d{4}-\d\d-\d\d)/.exec(location.hash), s = /(?:^|[#&])sel=([\w-]+)/.exec(location.hash);
  set(m ? m[1] : "");
  if (m && s && window.praxisSelect) window.praxisSelect(s[1]);  // the link's selection, once its day is drawn
});
