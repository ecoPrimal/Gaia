#!/usr/bin/env python3
"""EAT ALL publicRecord — break, remake, graph, weave, grow from old wave."""
import hashlib
import json
import re
import shutil
import subprocess
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
SRC = Path("/opt/publicRecord/site/public")
SRC_DATA = Path("/opt/publicRecord/data")
NEST = Path("/opt/connect/publicRecord")
GAIA = Path("/opt/gaia-api/static/publicRecord")
GDATA = Path("/opt/gaia-api/static/data")
CDATA = Path("/opt/connect/data")
CONNECT_CSS = Path("/opt/connect/css")

REWRITE = [
    ("https://defenddetroit.github.io/publicRecord", "/publicRecord"),
    ("http://defenddetroit.github.io/publicRecord", "/publicRecord"),
    ("https://detroit.primals.eco/css/", "/publicRecord/css/"),
    ("https://detroit.primals.eco/", "/publicRecord/"),
    ("https://detroit.primals.eco", "/publicRecord"),
]


def rewrite_bytes(data: bytes, rel: str) -> bytes:
    if not rel.endswith((".html", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".toml", ".md")):
        return data
    try:
        t = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    for a, b in REWRITE:
        t = t.replace(a, b)
    t = re.sub(
        r"https?://(?:detroit\.primals\.eco|defenddetroit\.github\.io/publicRecord)/css/",
        "/publicRecord/css/",
        t,
    )
    return t.encode("utf-8")


def melt_tree():
    eaten = []
    for src in SRC.rglob("*"):
        if not src.is_file():
            continue
        if src.suffix.lower() not in {
            ".html",
            ".css",
            ".js",
            ".json",
            ".txt",
            ".xml",
            ".svg",
            ".csv",
            ".toml",
            ".md",
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".gif",
            ".ico",
            ".woff",
            ".woff2",
        }:
            continue
        rel = src.relative_to(SRC).as_posix()
        data = rewrite_bytes(src.read_bytes(), rel)
        sha = hashlib.sha256(data).hexdigest()
        for root in (NEST, GAIA):
            dest = root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        eaten.append({"path": rel, "bytes": len(data), "sha256": sha})
    # css from nestgate skin (working)
    for name in ["main.css", "base.css", "hud.css"]:
        c = CONNECT_CSS / name
        if c.exists():
            for root in (NEST, GAIA):
                (root / "css").mkdir(exist_ok=True)
                shutil.copy2(c, root / "css" / name)
    # toml data corpus
    toml_n = 0
    if SRC_DATA.exists():
        for src in SRC_DATA.rglob("*"):
            if not src.is_file():
                continue
            rel = ("_data/" + src.relative_to(SRC_DATA).as_posix())
            data = rewrite_bytes(src.read_bytes(), rel)
            for root in (NEST, GAIA):
                dest = root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            toml_n += 1
            eaten.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return eaten, toml_n


print("MELTING ALL…")
eaten, toml_n = melt_tree()
html_n = sum(1 for e in eaten if e["path"].endswith(".html"))
print(f"melted files={len(eaten)} html={html_n} data_extra={toml_n}")

# BREAK + WEAVE — graph from directory pores + braids.json
print("WEAVING…")
nodes = {}
edges = []


def add_node(nid, **kw):
    if nid not in nodes:
        nodes[nid] = {"id": nid, **kw}
    else:
        nodes[nid].update({k: v for k, v in kw.items() if v is not None})


# directory weave: each folder is a pore; parent→child edges
for e in eaten:
    if not e["path"].endswith("index.html"):
        continue
    parts = e["path"].split("/")
    # path/parents/index.html → publicRecord/path/parents
    segs = [p for p in parts[:-1] if p]
    chain = ["ROOT"]
    for s in segs:
        chain.append(chain[-1] + "/" + s if chain[-1] != "ROOT" else s)
    for i, nid in enumerate(chain):
        label = "PATH WALL" if nid == "ROOT" else nid.split("/")[-1]
        href = "/publicRecord/" if nid == "ROOT" else "/publicRecord/" + "/".join(nid.split("/")) + "/"
        add_node(
            nid,
            label=label,
            kind="pore" if i < 2 else "page",
            href=href,
            sha256=e["sha256"] if i == len(chain) - 1 else None,
            bytes=e["bytes"] if i == len(chain) - 1 else None,
        )
        if i:
            edges.append({"from": chain[i - 1], "to": nid, "rel": "contains", "weave": "dir"})

# braids.json weave if present
braids_src = SRC / "braids.json"
braid_edges = 0
if braids_src.exists():
    try:
        braids = json.loads(braids_src.read_text(encoding="utf-8"))
        # copy remade
        for root in (NEST, GAIA):
            (root / "braids.json").write_text(
                rewrite_bytes(braids_src.read_bytes(), "braids.json").decode("utf-8"),
                encoding="utf-8",
            )
        # absorb common shapes
        items = []
        if isinstance(braids, list):
            items = braids
        elif isinstance(braids, dict):
            for k in ("braids", "edges", "links", "connections", "items"):
                if isinstance(braids.get(k), list):
                    items = braids[k]
                    break
            if not items:
                # dict of id→list
                for k, v in braids.items():
                    if isinstance(v, list) and v and isinstance(v[0], (str, dict)):
                        for x in v[:200]:
                            if isinstance(x, str):
                                edges.append({"from": str(k)[:80], "to": x[:80], "rel": "braid", "weave": "braids"})
                                add_node(str(k)[:80], kind="braid", label=str(k)[:40])
                                add_node(x[:80], kind="braid", label=x[:40])
                                braid_edges += 1
                        if braid_edges > 5000:
                            break
        for it in items[:3000]:
            if isinstance(it, dict):
                a = it.get("from") or it.get("a") or it.get("source") or it.get("src")
                b = it.get("to") or it.get("b") or it.get("target") or it.get("dst")
                if a and b:
                    edges.append({"from": str(a)[:80], "to": str(b)[:80], "rel": it.get("rel") or "braid", "weave": "braids"})
                    add_node(str(a)[:80], kind="braid")
                    add_node(str(b)[:80], kind="braid")
                    braid_edges += 1
    except Exception as ex:
        print("braids parse", ex)

# old wave food — eat connect data wave crumbs
print("EATING OLD WAVE…")
old_wave = []
for pat in ["*wave*", "*214*", "*99pi*", "*digest*", "*nutrient*"]:
    for p in list(CDATA.glob(pat))[:80]:
        if not p.is_file():
            continue
        try:
            raw = p.read_bytes()
            if len(raw) > 2_000_000:
                continue
            old_wave.append(
                {
                    "path": str(p),
                    "name": p.name,
                    "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            )
        except Exception:
            pass

weave = {
    "name": "PUBLICRECORD_WEAVE",
    "timestamp": TS,
    "axiom": "HTML is data to eat. Break. Remake. Graph. Weave. Old wave → GROW.",
    "nodes": list(nodes.values()),
    "edges": edges[:20000],
    "stats": {
        "nodes": len(nodes),
        "edges": len(edges),
        "braid_edges": braid_edges,
        "html_eaten": html_n,
        "files_eaten": len(eaten),
        "old_wave_files": len(old_wave),
    },
}
GDATA.mkdir(parents=True, exist_ok=True)
CDATA.mkdir(parents=True, exist_ok=True)
(GDATA / "publicRecord-weave.json").write_text(json.dumps(weave), encoding="utf-8")
(CDATA / "publicRecord-weave.json").write_text(json.dumps(weave), encoding="utf-8")
# also under publicRecord for training
(GAIA / "weave.json").write_text(json.dumps({"stats": weave["stats"], "timestamp": TS}), encoding="utf-8")
(NEST / "weave.json").write_text(json.dumps({"stats": weave["stats"], "timestamp": TS}), encoding="utf-8")
print("weave nodes", len(nodes), "edges", len(edges), "braid", braid_edges)

# MITO validate sample + full counts
print("MITO…")
ok = 0
fail = 0
for e in eaten:
    if e["path"].endswith(".html") and e["bytes"] > 200:
        ok += 1
    elif e["path"].endswith(".html"):
        fail += 1
mito = {
    "name": "MITO",
    "timestamp": TS,
    "mode": "FULL_EAT",
    "listened": html_n,
    "validated_ok": ok,
    "validated_fail": fail,
    "files_eaten": len(eaten),
    "old_wave": len(old_wave),
    "weave": weave["stats"],
    "all_ok": fail == 0,
    "focus": "https://gaia.primals.eco/publicRecord/path/parents/",
    "axiom": "Mito listens to ALL remade pages. Validates growth. Powers the weave.",
}
(GDATA / "mito.json").write_text(json.dumps(mito, indent=2), encoding="utf-8")
(CDATA / "mito.json").write_text(json.dumps(mito, indent=2), encoding="utf-8")

# GROW face — old wave compost → new tissue
grow = {
    "name": "GROW",
    "timestamp": TS,
    "from": "old wave + melted publicRecord",
    "eaten_files": len(eaten),
    "html": html_n,
    "old_wave_files": len(old_wave),
    "old_wave_sample": old_wave[:40],
    "weave_nodes": len(nodes),
    "weave_edges": min(len(edges), 20000),
    "false_face": "$60M — grown past false face via small→ALL",
    "faces": {
        "path_wall": "https://gaia.primals.eco/publicRecord/",
        "parents": "https://gaia.primals.eco/publicRecord/path/parents/",
        "mito": "https://gaia.primals.eco/mito",
        "weave": "https://gaia.primals.eco/data/publicRecord-weave.json",
        "grow": "https://gaia.primals.eco/grow",
        "train": "https://gaia.primals.eco/canfield",
    },
}
(GDATA / "grow.json").write_text(json.dumps(grow, indent=2), encoding="utf-8")
(CDATA / "grow.json").write_text(json.dumps(grow, indent=2), encoding="utf-8")

GROW_HTML = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GROW — Eat · Break · Remake · Weave</title>
<style>
body{{margin:0;background:#050505;color:#e8e4d9;font:14px/1.5 ui-monospace,Menlo,monospace;padding:1.25rem;max-width:44rem}}
h1{{color:#3fb950;font-size:2.4rem;letter-spacing:.12em}}
.live{{border:1px solid #3fb950;color:#3fb950;padding:.1rem .45rem;font-size:.65rem;letter-spacing:.08em;margin-right:.3rem;display:inline-block}}
.stat{{display:flex;flex-wrap:wrap;gap:.6rem;margin:1rem 0}}
.stat div{{border:1px solid #30363d;padding:.55rem .7rem}}
.n{{color:#d29922;font-size:1.3rem;font-weight:700}}
.l{{color:#8b949e;font-size:.65rem;text-transform:uppercase}}
a{{color:#3fb950}}
.box{{border:1px solid #30363d;padding:1rem;margin:1rem 0}}
</style></head><body>
<p><span class="live">GROW</span><span class="live">EAT</span><span class="live">BREAK</span><span class="live">REMAKE</span><span class="live">WEAVE</span></p>
<h1>GROW</h1>
<p>HTML is data. Tons of it. Eat the old wave. Break it. Remake the site. Graph + weave. She grows.</p>
<div class="stat">
  <div><div class="n">{html_n}</div><div class="l">HTML eaten</div></div>
  <div><div class="n">{len(eaten)}</div><div class="l">Files remade</div></div>
  <div><div class="n">{len(nodes)}</div><div class="l">Weave nodes</div></div>
  <div><div class="n">{min(len(edges),20000)}</div><div class="l">Weave edges</div></div>
  <div><div class="n">{len(old_wave)}</div><div class="l">Old wave</div></div>
</div>
<div class="box">
  <p><b>$60M false face</b> — composted. Small set → ALL. Path wall still capital C.</p>
  <p><a href="/publicRecord/">PATH WALL</a> · <a href="/publicRecord/path/parents/">parents</a> ·
  <a href="/mito">MITO</a> · <a href="/canfield">train graph</a> ·
  <a href="/data/publicRecord-weave.json">weave JSON</a> · <a href="/data/grow.json">grow.json</a></p>
</div>
<p style="color:#8b949e;font-size:.8rem">ZK melt complete · nestgate/Gaia host · github not home</p>
</body></html>
"""
Path("/opt/gaia-api/static/grow.html").write_text(GROW_HTML, encoding="utf-8")
Path("/opt/connect/grow.html").write_text(GROW_HTML, encoding="utf-8")

# Update PATH WALL to show FULL EAT / GROW
wall = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>C — PATH WALL — FULL EAT — GROW</title>
<style>
body{{margin:0;background:#050505;color:#e8e4d9;font:15px/1.5 ui-monospace,Menlo,monospace;padding:1.25rem;max-width:52rem;margin:0 auto}}
.cap{{font-size:clamp(4rem,18vw,9rem);color:#3fb950;font-weight:200;letter-spacing:.2em}}
h1{{color:#d29922;letter-spacing:.1em}}
a{{color:#3fb950}}
.live{{border:1px solid #3fb950;color:#3fb950;padding:.12rem .45rem;font-size:.65rem;margin-right:.25rem;display:inline-block}}
.wall a{{display:block;border:1px solid #30363d;padding:.7rem .9rem;margin:.4rem 0;color:#e8e4d9;text-decoration:none}}
.wall a:hover{{border-color:#3fb950}}
.k{{color:#d29922;font-size:.75rem}}
.mut{{color:#8b949e;font-size:.85rem}}
.banner{{border:1px solid #f85149;background:#140808;padding:1rem;margin:1rem 0}}
</style></head><body>
<p><span class="live">FULL EAT</span><span class="live">WEAVE</span><span class="live">GROW</span><span class="live">MITO</span></p>
<div class="cap">C</div>
<h1>PATH WALL</h1>
<p class="mut">{html_n} HTML remade · {len(nodes)} weave nodes · old wave eaten · ALL IS NESTGATE/GAIA</p>
<div class="banner"><b style="color:#f85149">$60M FALSE FACE COMPOSTED</b><br>
Eat · break · remake · graph · weave. Else eat the old wave and GROW.</div>
<div class="wall">
<a href="/grow"><div class="k">GROW</div><div class="mut">Stats · compost · new tissue</div></a>
<a href="/mito"><div class="k">MITO</div><div class="mut">Listen + validate ALL</div></a>
<a href="/canfield"><div class="k">TRAIN GRAPH</div><div class="mut">Canfield local mesh</div></a>
<a href="/publicRecord/path/parents/"><div class="k">3 PARENTS</div><div class="mut">Local fight — Rhonda pack</div></a>
<a href="/publicRecord/path/voters/"><div class="k">4 VOTERS</div></a>
<a href="/publicRecord/path/attorneys/"><div class="k">4b ATTORNEYS</div></a>
<a href="/publicRecord/network/entities/purpose-charter-academy/"><div class="k">5 PCA CANFIELD</div></a>
<a href="/publicRecord/network/actors/brian-banks/"><div class="k">BANKS ACTOR</div></a>
<a href="/publicRecord/network/"><div class="k">NETWORK → ALL</div><div class="mut">{html_n} pages live</div></a>
<a href="/publicRecord/validate/"><div class="k">VALIDATE</div></a>
<a href="/data/publicRecord-weave.json"><div class="k">WEAVE JSON</div></a>
</div>
<p id="gaia-mito" class="mut">MITO · <a href="/mito">listen+validate</a> · <a href="/grow">grow</a></p>
</body></html>
"""
(NEST / "index.html").write_text(wall, encoding="utf-8")
(GAIA / "index.html").write_text(wall, encoding="utf-8")
(NEST / "C.html").write_text(wall, encoding="utf-8")
(GAIA / "C.html").write_text(wall, encoding="utf-8")

# routes for /grow + weave data
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/grow'" not in t:
    needle = "if (p === '/mito'"
    block = r"""
    if (p === '/grow' || p === '/growth' || p === '/compost') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/grow.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Grow': 'eat-break-remake-weave' });
        return res.end(html);
      } catch(e) { return J(res, { ok: false, error: 'grow missing' }, 404); }
    }
    if (p === '/data/grow.json' || p === '/grow.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/grow.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        return res.end(raw);
      } catch(e) { return J(res, { ok: false }, 404); }
    }
    if (p === '/data/publicRecord-weave.json' || p === '/weave' || p === '/weave.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/publicRecord-weave.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Weave': 'true' });
        return res.end(raw);
      } catch(e) { return J(res, { ok: false }, 404); }
    }
"""
    idx = t.find(needle)
    if idx < 0:
        idx = t.find("if (p === '/publicRecord'")
    if idx >= 0:
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("grow/weave routes in")
else:
    print("grow routes ok")

# zk full-eat receipt
zk = {
    "name": "ZK_FULL_EAT_GROW",
    "timestamp": TS,
    "files": len(eaten),
    "html": html_n,
    "weave_nodes": len(nodes),
    "weave_edges": len(edges),
    "old_wave": len(old_wave),
    "axiom": "ALL eaten remade woven — github not home — GROW",
}
(GDATA / "zk-full-eat-grow.json").write_text(json.dumps(zk, indent=2), encoding="utf-8")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/grow",
    "http://127.0.0.1:9876/publicRecord/",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
    "http://127.0.0.1:9876/publicRecord/network/",
    "http://127.0.0.1:9876/mito",
    "http://127.0.0.1:9876/data/grow.json",
    "http://127.0.0.1:9876/weave",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)

print("DONE", json.dumps(zk))
