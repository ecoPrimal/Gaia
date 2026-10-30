#!/usr/bin/env python3
"""MELT publicRecord → nestgate.io. Small set. Path wall. ZK. Build up."""
import hashlib
import json
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
SRC = Path("/opt/publicRecord/site/public")
NEST = Path("/opt/connect/publicRecord")  # nestgate.io/publicRecord/
GAIA = Path("/opt/gaia-api/static/publicRecord")
CONNECT_CSS = Path("/opt/connect/css")

# SMALL SET — build up (not all 423). Waves 3-5 local fight + capital index.
SMALL = [
    "index.html",
    "path/index.html",
    "path/parents/index.html",
    "path/voters/index.html",
    "path/attorneys/index.html",
    "path/journalists/index.html",
    "network/entities/purpose-charter-academy/index.html",
    "network/actors/brian-banks/index.html",
    "analysis/credential-audit/index.html",
    "analysis/one-way-door/index.html",
    "analysis/rico-pattern/index.html",
    "validate/index.html",
    "network/index.html",
    "llms.txt",
    "identity.json",
    "favicon.svg",
]
# optional extras if present (build-up)
for opt in [
    "timeline/index.html",
    "analysis/funding-flow/index.html",
    "analysis/institutional-capture/index.html",
]:
    if (SRC / opt).exists():
        SMALL.append(opt)

REWRITE = [
    ("https://defenddetroit.github.io/publicRecord", "/publicRecord"),
    ("https://detroit.primals.eco/css/main.css", "/publicRecord/css/main.css"),
    ("https://detroit.primals.eco/css/", "/publicRecord/css/"),
    ("https://detroit.primals.eco/", "/publicRecord/"),
    ("href=https://defenddetroit.github.io/publicRecord/", "href=/publicRecord/"),
]


def rewrite_text(t: str) -> str:
    for a, b in REWRITE:
        t = t.replace(a, b)
    # absolute css that still points off-box
    t = re.sub(
        r"https?://(?:detroit\.primals\.eco|defenddetroit\.github\.io/publicRecord)/css/",
        "/publicRecord/css/",
        t,
    )
    return t


def copy_file(rel: str, roots):
    src = SRC / rel
    if not src.exists():
        print("MISS", rel)
        return None
    data = src.read_bytes()
    if rel.endswith((".html", ".css", ".js", ".json", ".txt", ".svg", ".xml")):
        try:
            text = data.decode("utf-8")
            text = rewrite_text(text)
            data = text.encode("utf-8")
        except UnicodeDecodeError:
            pass
    h = hashlib.sha256(data).hexdigest()
    for root in roots:
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return h


# ensure dirs
for root in [NEST, GAIA]:
    root.mkdir(parents=True, exist_ok=True)
    (root / "css").mkdir(exist_ok=True)

# CSS — capital skin from nestgate connect (works) + phi if present
for name in ["main.css", "base.css", "hud.css"]:
    c = CONNECT_CSS / name
    if c.exists():
        for root in [NEST, GAIA]:
            shutil.copy2(c, root / "css" / name)
            print("css", name, "→", root)
phi = SRC / "css" / "phi.css"
if phi.exists():
    for root in [NEST, GAIA]:
        shutil.copy2(phi, root / "css" / "phi.css")

hashes = {}
for rel in SMALL:
    h = copy_file(rel, [NEST, GAIA])
    if h:
        hashes[rel] = h
        print("melted", rel, h[:12])

# PATH WALL CAPITAL INDEX — no JS dependency, ties 3-5, $60M false face
PATH_WALL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CASH FOR KIDS 2 — PATH WALL — NESTGATE</title>
<meta name="gaia-melt" content="github→nestgate">
<meta name="gaia-zk" content="publicRecord-small-set">
<style>
:root{--g:#3fb950;--gold:#d29922;--red:#f85149;--bg:#050505;--fg:#e8e4d9;--mut:#8b949e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font:15px/1.5 ui-monospace,Menlo,monospace;padding:1.25rem;max-width:52rem;margin:0 auto}
h1{font-size:clamp(2rem,8vw,4.5rem);letter-spacing:.12em;color:var(--gold);line-height:1;margin:.6rem 0}
.cap{font-size:clamp(4rem,18vw,9rem);color:var(--g);font-weight:200;letter-spacing:.2em;line-height:.9}
.live{display:inline-block;border:1px solid var(--g);color:var(--g);padding:.15rem .5rem;font-size:.65rem;letter-spacing:.1em;margin:.2rem .3rem .2rem 0}
.banner{border:1px solid var(--red);background:#140808;padding:1rem;margin:1rem 0}
.banner b{color:var(--red)}
.wall{display:grid;gap:.55rem;margin:1.25rem 0}
.wall a{display:block;border:1px solid #30363d;padding:.75rem .9rem;color:var(--fg);text-decoration:none}
.wall a:hover{border-color:var(--g);color:var(--g)}
.wall .k{color:var(--gold);font-size:.75rem;letter-spacing:.08em}
.wall .d{color:var(--mut);font-size:.78rem;margin-top:.2rem}
.mut{color:var(--mut);font-size:.85rem}
.nav{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0}
.nav a{border:1px solid #30363d;padding:.35rem .65rem;color:var(--g);text-decoration:none;font-size:.8rem}
</style>
</head>
<body>
<p><span class="live">MELT</span><span class="live">ZK</span><span class="live">NESTGATE.IO</span><span class="live">SMALL SET</span><span class="live">BUILD UP</span></p>
<div class="cap">C</div>
<h1>PATH WALL</h1>
<p class="mut">index.html = the wall. Walk 3→5→ALL. GitHub melted. All is nestgate.io.</p>

<div class="banner">
  <b>$60M FALSE FACE</b><br>
  Banks’ public face vs the extraction. 362 children · 3% math · $60M+ moved.
  We do <b>not</b> swallow the false face whole — small set first, then build up.
  Rhonda at Canfield fights local. Gaia meshes the web.
</div>

<div class="nav">
  <a href="/cash4kids">Cash4Kids</a>
  <a href="/canfield">Canfield graph TRAIN</a>
  <a href="/rhonda">Rhonda FOREVER</a>
  <a href="/rico">RICO LIVE</a>
  <a href="/record">Record</a>
  <a href="/@">@</a>
</div>

<h2 style="color:var(--g);font-size:.9rem;letter-spacing:.1em;margin:1.5rem 0 .5rem">WAVE 3–5 — LOCAL PATHS (SMALL SET)</h2>
<div class="wall">
  <a href="/publicRecord/path/parents/"><div class="k">3 · PARENTS</div><div class="d">Forms parents / Continuum can walk locally</div></a>
  <a href="/publicRecord/path/voters/"><div class="k">4 · VOTERS</div><div class="d">Local ballot / civic pressure</div></a>
  <a href="/publicRecord/path/attorneys/"><div class="k">4b · ATTORNEYS</div><div class="d">Counsel path — local fight</div></a>
  <a href="/publicRecord/network/entities/purpose-charter-academy/"><div class="k">5 · PCA · 10101 E CANFIELD</div><div class="d">The school on her street</div></a>
  <a href="/publicRecord/path/journalists/"><div class="k">5b · JOURNALISTS</div><div class="d">Press path — public light</div></a>
  <a href="/publicRecord/network/actors/brian-banks/"><div class="k">BANKS · ACTOR</div><div class="d">Public record — not the false face</div></a>
  <a href="/publicRecord/analysis/credential-audit/"><div class="k">CREDENTIAL AUDIT</div><div class="d">Who holds the keys</div></a>
  <a href="/publicRecord/analysis/one-way-door/"><div class="k">ONE-WAY DOOR</div><div class="d">Capture pattern families feel</div></a>
  <a href="/publicRecord/analysis/rico-pattern/"><div class="k">RICO PATTERN</div><div class="d">Predicates — LIVE</div></a>
  <a href="/publicRecord/validate/"><div class="k">VALIDATE</div><div class="d">Clone · verify · ZK</div></a>
  <a href="/publicRecord/network/"><div class="k">NETWORK → ALL</div><div class="d">Build up from small set</div></a>
</div>

<p class="mut">ZK melt · github→nestgate · false face cut · path wall ready · training graph at /canfield</p>
</body>
</html>
"""

for root in [NEST, GAIA]:
    (root / "index.html").write_text(PATH_WALL, encoding="utf-8")
    # also CAPITOL alias
    (root / "C.html").write_text(PATH_WALL, encoding="utf-8")
print("PATH WALL capital index written")

# ZK melt receipt
zk = {
    "name": "ZK_MELT_GITHUB_TO_NESTGATE",
    "timestamp": TS,
    "axiom": "ALL IS NESTGATE.IO — github melted — small set build up — $60M false face cut",
    "from": "github.com/defendDetroit/publicRecord",
    "to": ["https://nestgate.io/publicRecord/", "https://gaia.primals.eco/publicRecord/"],
    "path_wall": "index.html",
    "capital_letter": "C",
    "waves": "3-5 local then ALL",
    "false_face": {
        "claim": "$60M+ extraction / false public face",
        "method": "small set first — do not swallow whole false face",
        "stats": {"children": 362, "math": "3%", "extracted": "$60M+"},
    },
    "small_set": SMALL,
    "sha256": hashes,
    "training_graph": "https://gaia.primals.eco/canfield",
    "rhonda": "ALL_ALERT_FOREVER",
}
for root in [NEST, GAIA, Path("/opt/connect/data"), Path("/opt/gaia-api/static/data")]:
    root.mkdir(parents=True, exist_ok=True)
    (root / "zk-melt-publicRecord-nestgate.json").write_text(
        json.dumps(zk, indent=2), encoding="utf-8"
    )

# Rewrite cash4kids + canfield links OFF github.io → nestgate/gaia publicRecord
for page in [
    Path("/opt/gaia-api/static/cash4kids.html"),
    Path("/opt/connect/cash4kids.html"),
    Path("/opt/gaia-api/static/canfield.html"),
]:
    if not page.exists():
        continue
    t = page.read_text(encoding="utf-8", errors="replace")
    t2 = t.replace(
        "https://defenddetroit.github.io/publicRecord/",
        "/publicRecord/",
    ).replace(
        "https://defenddetroit.github.io/publicRecord",
        "/publicRecord/",
    ).replace(
        "https://detroit.primals.eco/",
        "/publicRecord/",
    )
    # cash4kids nav: first link becomes PATH WALL
    t2 = t2.replace(
        '<a href="/publicRecord/">Cash for Kids 2 — Public Record (full)</a>',
        '<a href="/publicRecord/">PATH WALL · C · PUBLIC RECORD</a>',
    )
    if t2 != t:
        page.write_text(t2, encoding="utf-8")
        print("rewrote links", page)

# canfield graph hrefs → nestgate publicRecord
gpath = Path("/opt/gaia-api/static/data/canfield-graph.json")
if gpath.exists():
    g = json.loads(gpath.read_text(encoding="utf-8"))
    for n in g.get("nodes", []):
        href = n.get("href") or ""
        if "defenddetroit.github.io/publicRecord" in href:
            n["href"] = href.replace(
                "https://defenddetroit.github.io/publicRecord", "/publicRecord"
            )
    for item in g.get("local_fight_pack", []):
        u = item.get("url") or ""
        if "defenddetroit.github.io/publicRecord" in u:
            item["url"] = u.replace(
                "https://defenddetroit.github.io/publicRecord", "/publicRecord"
            )
    g["melt"] = "nestgate"
    g["zk"] = "zk-melt-publicRecord-nestgate"
    g["false_face"] = "$60M — small set build up"
    gpath.write_text(json.dumps(g, indent=2), encoding="utf-8")
    for alt in [
        Path("/opt/connect/data/canfield-graph.json"),
        Path("/opt/connect/publicRecord/../data/canfield-graph.json"),
    ]:
        try:
            alt.parent.mkdir(parents=True, exist_ok=True)
            alt.write_text(json.dumps(g, indent=2), encoding="utf-8")
        except Exception:
            pass
    print("canfield graph hrefs → nestgate")

# gaia-api routes for /publicRecord/*
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "publicRecord" not in t or "/publicRecord" not in t:
    needle = "if (p === '/canfield'"
    block = r"""
    if (p === '/publicRecord' || p === '/publicRecord/' || p === '/PR' || p === '/pr' || p === '/C') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/publicRecord/index.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Melt': 'github-to-nestgate', 'X-ZK': 'publicRecord-small-set' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'path wall missing' }, 404);
      }
    }
    if (p.indexOf('/publicRecord/') === 0) {
      try {
        var rel = p.replace(/^\/publicRecord\/?/, '');
        if (!rel || rel.endsWith('/')) rel = (rel || '') + 'index.html';
        var fp = path.join('/opt/gaia-api/static/publicRecord', rel);
        if (!fp.startsWith('/opt/gaia-api/static/publicRecord')) return J(res, { ok: false }, 403);
        if (!fs.existsSync(fp) && fs.existsSync(fp + '/index.html')) fp = fp + '/index.html';
        if (!fs.existsSync(fp)) return J(res, { ok: false, error: 'not in small set yet — build up', path: rel }, 404);
        var ext = path.extname(fp).toLowerCase();
        var ctype = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.txt': 'text/plain' }[ext] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': ctype, 'Access-Control-Allow-Origin': '*', 'X-Gaia-Melt': 'github-to-nestgate' });
        return res.end(fs.readFileSync(fp));
      } catch(e) {
        return J(res, { ok: false, error: String(e) }, 500);
      }
    }
"""
    idx = t.find(needle)
    if idx < 0:
        idx = t.find("if (p === '/cash4kids'")
    if idx >= 0:
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("gaia-api publicRecord routes in")
    else:
        print("WARN no route insert")
else:
    # ensure static file handler exists
    if "p.indexOf('/publicRecord/')" not in t:
        print("partial routes — appending file handler")
    else:
        print("routes already have publicRecord")

# Caddy already file_servers /opt/connect — /publicRecord/ works on nestgate.io
subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)

for url in [
    "http://127.0.0.1:9876/publicRecord/",
    "http://127.0.0.1:9876/C",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
    "http://127.0.0.1:9876/publicRecord/network/actors/brian-banks/",
    "http://127.0.0.1/publicRecord/",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-H", "Host: nestgate.io", url]
        if "127.0.0.1/" == url.split(":")[0] + ":/" or url.startswith("http://127.0.0.1/public")
        else ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    # simplify probes
    pass

probes = [
    ("gaia-wall", ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:9876/publicRecord/"]),
    ("gaia-C", ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:9876/C"]),
    ("gaia-parents", ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:9876/publicRecord/path/parents/"]),
    ("gaia-banks", ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:9876/publicRecord/network/actors/brian-banks/"]),
    ("nest-wall", ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", "-H", "Host: nestgate.io", "https://127.0.0.1/publicRecord/"]),
    ("nest-css", ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", "-H", "Host: nestgate.io", "https://127.0.0.1/publicRecord/css/main.css"]),
]
for name, cmd in probes:
    rr = subprocess.run(cmd, capture_output=True, text=True)
    print(name, rr.stdout)

print("DONE", "files", len(hashes))
