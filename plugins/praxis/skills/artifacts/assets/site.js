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
  var state = { mode: "all", owner: "", done: true, asks: true, sel: null };
  var ownerSel = document.getElementById("map-owner");
  if (ownerSel) {
    var owners = {}; d.nodes.forEach(function (n) { if (n.owner) owners[n.owner] = 1; });
    Object.keys(owners).sort().forEach(function (o) { var op = document.createElement("option"); op.value = o; op.textContent = o; ownerSel.appendChild(op); });
  }
  function visible(n) { return (state.done || !n.done) && (state.asks || n.kind !== "ask"); }
  function wrap(s, n) {
    var w = s.split(/\s+/), lines = [""], i = 0;
    w.forEach(function (x) { if ((lines[i] + " " + x).trim().length > n && lines[i]) { if (i === 1) { lines[1] += "…"; i = 2; return; } lines[++i] = x; } else if (i < 2) lines[i] = (lines[i] + " " + x).trim(); });
    return lines.slice(0, 2).map(function (l) { return l.length > n + 1 ? l.slice(0, n) + "…" : l; });
  }
  function esc(s) { return String(s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function stateWord(n) { return n.done ? "done" : n.can ? "can start now" : n.kind === "ask" ? (n.state === "proposed" ? "proposed" : "open") : "waiting on other steps"; }
  var svg, els = {}, links = [];
  function draw() {
    host.innerHTML = ""; els = {}; links = [];
    var shown = d.nodes.filter(visible), maxL = 0, pos = {};
    var LANES = [["ask", "Decisions and outside dependencies"], ["step", "Work"], ["gate", "Gates"]];
    var laneOf = function (n) { return n.kind === "dep" ? "ask" : n.kind; };
    shown.forEach(function (n) { maxL = Math.max(maxL, n.layer); });
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
    for (var c = 0; c <= maxL; c++) { var t = el("text", { x: labelW + 44 + colX[c], y: 14, class: "colhead", "text-anchor": "middle" }); t.textContent = String(c + 1); }
    d.edges.forEach(function (e) {
      if (!pos[e[0]] || !pos[e[1]]) return;
      var a = pos[e[0]], b = pos[e[1]], mx = (a.x + b.x) / 2, crit = critSet[e[0]] && critSet[e[1]];
      var p = el("path", { d: "M" + (a.x + 9) + "," + a.y + " C" + mx + "," + a.y + " " + mx + "," + b.y + " " + (b.x - 11) + "," + b.y,
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
