#!/usr/bin/env python3
"""Check how a rendered claude-artifacts site actually draws, in a headless browser.

Usage: check_render.py <out-dir> [--shots <dir>]

Loads every page at a desktop width and the narrowest a headless window opens (500px), and reports:
- a page wider than the screen, so the reader scrolls sideways;
- text cut off by its box;
- labels in a drawing that overlap each other;
- a picture that renders empty;
- a page that opens scrolled past its head, and a script error while it loads.

With --shots, also saves the first screen of each page (1440 by 900) as <dir>/<page path with / as __>.png, for a reader to look at.

Every page is loaded in one headless Chrome, driven over its DevTools pipe, so a run starts one browser process however
many pages the site has.

Needs Chrome or Chromium. Without one it prints {"findings": [], "skipped": "<why>"} and exits 0, so the caller says
the rendering went unchecked rather than passing it.

Prints {"findings": [...]} with {"page", "check", "detail"} each, and exits 1 when there is any.
"""
import base64
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

WIDTHS = {"desktop": 1440, "narrow": 500}  # 500px is the narrowest a headless window opens
SHOT = (1440, 900)

# Evaluated in the page once it has loaded and its own scripts have drawn; returns what it measured.
PROBE = r"""
(function () {
  var out = [], W = window.innerWidth;
  if (window.scrollY > 40) out.push(["opens scrolled", "the page opens " + Math.round(window.scrollY) + "px down, past its head" + (location.hash ? " (address now ends " + location.hash + ")" : "")]);
  function label(el) { var t = (el.textContent || "").trim().replace(/\s+/g, " "); return t.slice(0, 60); }
  if (document.documentElement.scrollWidth > W + 4) {
    var wide = [].filter.call(document.querySelectorAll("main *"), function (e) {
      var r = e.getBoundingClientRect(); return r.right > W + 4 && r.width > 0 && !e.closest(".tbl, .fig, .gaterail, pre, svg");
    }).slice(0, 2).map(function (e) { return e.tagName.toLowerCase() + "." + (e.className || "") + " '" + label(e) + "'"; });
    if (wide.length) out.push(["overflow", "the page is wider than the screen (" + document.documentElement.scrollWidth + "px over " + W + "px), from " + wide.join("; ")]);
  }
  [].forEach.call(document.querySelectorAll("main *"), function (e) {
    var cs = getComputedStyle(e);
    if (e.children.length || !(e.textContent || "").trim()) return;
    if ((cs.overflow === "hidden" || cs.overflowX === "hidden" || cs.textOverflow === "ellipsis") && e.scrollWidth > e.clientWidth + 2)
      out.push(["clipped", "text cut off: '" + label(e) + "'"]);
  });
  [].forEach.call(document.querySelectorAll("main svg"), function (svg, k) {
    var r = svg.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && !svg.querySelector("text, path, rect, circle, line")) out.push(["empty picture", "picture " + (k + 1) + " draws nothing"]);
    var ts = [].map.call(svg.querySelectorAll("text"), function (t) { return [t, t.getBoundingClientRect()]; })
      .filter(function (p) { return p[1].width > 0 && (p[0].textContent || "").trim(); });
    for (var i = 0; i < ts.length; i++) for (var j = i + 1; j < ts.length; j++) {
      var a = ts[i][1], b = ts[j][1];
      var w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (w > 2 && h > 2 && w * h > 0.3 * Math.min(a.width * a.height, b.width * b.height))
        out.push(["overlap", "labels overlap in picture " + (k + 1) + ": '" + label(ts[i][0]) + "' and '" + label(ts[j][0]) + "'"]);
    }
  });
  [].forEach.call(document.querySelectorAll("main .trace-graph, main .map, main [id$='-graph']"), function (e) {
    if (e.getBoundingClientRect().height < 20) out.push(["empty picture", "'" + (e.id || e.className) + "' draws nothing"]);
  });
  return JSON.stringify(out);
})()
"""


def chrome():
    for c in ("google-chrome", "chromium", "chromium-browser", "chrome",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        p = shutil.which(c) or (c if os.path.exists(c) else None)
        if p:
            return p
    return None


class Browser:
    """One headless Chrome, spoken to over --remote-debugging-pipe: requests on fd 3, replies and events on fd 4."""

    def __init__(self, exe, profile):
        to_r, self._to_w = os.pipe()
        self._from_r, from_w = os.pipe()

        def fds():  # the pipe ends land on 3 and 4 in the child, whatever numbers they had here
            a, b = os.dup(to_r), os.dup(from_w)
            os.dup2(a, 3)
            os.dup2(b, 4)
        self.proc = subprocess.Popen(
            [exe, "--headless=new", "--remote-debugging-pipe", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
             "--no-default-browser-check", "--disable-extensions", "--mute-audio", f"--user-data-dir={profile}", "about:blank"],
            pass_fds=(3, 4, to_r, from_w), preexec_fn=fds, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.close(to_r)
        os.close(from_w)
        self._buf, self._id, self.events = b"", 0, []
        target = self.call("Target.createTarget", {"url": "about:blank"})["targetId"]
        self.session = self.call("Target.attachToTarget", {"targetId": target, "flatten": True})["sessionId"]
        for m in ("Page.enable", "Runtime.enable"):
            self.call(m, session=True)

    def _read(self, timeout):
        end = time.time() + timeout
        while b"\0" not in self._buf:
            if time.time() > end:
                raise TimeoutError("the browser stopped answering")
            chunk = os.read(self._from_r, 1 << 16)
            if not chunk:
                raise RuntimeError("the browser closed")
            self._buf += chunk
        msg, self._buf = self._buf.split(b"\0", 1)
        return json.loads(msg)

    def call(self, method, params=None, session=False, timeout=60):
        self._id += 1
        msg = {"id": self._id, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = self.session
        os.write(self._to_w, json.dumps(msg).encode() + b"\0")
        while True:
            m = self._read(timeout)
            if m.get("id") == self._id:
                if "error" in m:
                    raise RuntimeError(f'{method}: {m["error"].get("message")}')
                return m.get("result", {})
            self.events.append(m)

    def wait_for(self, method, timeout=30):
        for k, e in enumerate(self.events):
            if e.get("method") == method:
                del self.events[: k + 1]
                return e
        end = time.time() + timeout
        while time.time() < end:
            m = self._read(end - time.time())
            if m.get("method") == method:
                return m
            self.events.append(m)
        raise TimeoutError(f"no {method}")

    def load(self, url, width, height):
        self.call("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False}, session=True)
        self.events.clear()
        self.call("Page.navigate", {"url": url}, session=True)
        self.wait_for("Page.loadEventFired")
        time.sleep(0.4)  # the page's own scripts draw after load
        errors = [e["params"]["exceptionDetails"].get("exception", {}).get("description") or e["params"]["exceptionDetails"].get("text", "")
                  for e in self.events if e.get("method") == "Runtime.exceptionThrown"]
        return [str(x).splitlines()[0] for x in errors if x]

    def evaluate(self, expr):
        r = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True}, session=True)
        return r.get("result", {}).get("value")

    def screenshot(self, path):
        data = self.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False}, session=True)["data"]
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(data))

    def close(self):
        try:
            self.call("Browser.close", timeout=5)
        except Exception:
            pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def main(argv):
    if len(argv) not in (2, 4) or (len(argv) == 4 and argv[2] != "--shots"):
        print(__doc__, file=sys.stderr)
        return 2
    out = os.path.abspath(argv[1])
    shots = os.path.abspath(argv[3]) if len(argv) == 4 else None
    exe = chrome()
    if not exe:
        print(json.dumps({"findings": [], "skipped": "no Chrome or Chromium found, so the rendering went unchecked"}, indent=2))
        return 0
    pages = sorted(os.path.relpath(os.path.join(d, f), out).replace(os.sep, "/")
                   for d, _, fs in os.walk(out) for f in fs if f.endswith(".html"))
    findings, seen = [], set()
    if shots:
        os.makedirs(shots, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        b = Browser(exe, profile)
        try:
            for rel in pages:
                url = pathlib.Path(os.path.join(out, rel)).as_uri()
                for name, w in WIDTHS.items():
                    try:
                        errors = b.load(url, w, 1200)
                        got = json.loads(b.evaluate(PROBE) or "[]")
                    except (TimeoutError, RuntimeError) as e:
                        findings.append({"page": rel, "check": "load", "detail": f"{e} at {name} width"})
                        continue
                    for check, detail in [("script error", m) for m in errors] + [tuple(x) for x in got]:
                        if (rel, check, detail) not in seen:
                            seen.add((rel, check, detail))
                            findings.append({"page": rel, "check": check, "detail": f"{detail} ({name})"})
                if shots:
                    # The first screen of the page, at a normal window.
                    try:
                        b.load(url, *SHOT)
                        b.screenshot(os.path.join(shots, rel.replace("/", "__")[:-5] + ".png"))
                    except (TimeoutError, RuntimeError) as e:
                        findings.append({"page": rel, "check": "load", "detail": f"{e} while taking its screenshot"})
        finally:
            b.close()
    print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
