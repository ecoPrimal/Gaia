#!/usr/bin/env python3
"""Deploy MEMBRANE CUT onto live nestgate root /opt/connect."""
import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path("/opt/connect")
TS = datetime.now(timezone.utc).isoformat()

cut = {
    "name": "MEMBRANE_CUT",
    "timestamp": TS,
    "axiom": "localhost is a SUBNET (INTERNAL). Phone sees EXTERNAL. Cut them.",
    "INTERNAL": {
        "subnet": ["127.0.0.1/8", "192.168.0.0/16", "10.0.0.0/8", "10.13.37.0/24"],
        "names": ["localhost", "northgate LAN", "organs talking to organs"],
        "role": "loopback / LAN — never the public home face",
        "ok_for": "bind primals, ollama, spine, Gaia3, feeder :3141",
        "not_for": "links in HTML served to phones",
    },
    "EXTERNAL": {
        "faces": {
            "CIS": "https://nestgate.io",
            "TRANS_skin": "https://primals.eco",
            "TRANS_mouth": "https://gaia.primals.eco/deck",
            "TRANS_spend": "https://primals.eco/feed.xml",
            "signal": "https://signal.primals.eco",
            "forge": "https://forge.primals.eco",
            "cut_page": "https://nestgate.io/cut",
            "new_page": "https://nestgate.io/new",
        },
        "rule": "EXTERNAL HTML never homes on localhost",
    },
    "rewrite_map": {
        "http://localhost:3141": "https://nestgate.io",
        "http://127.0.0.1:3141": "https://nestgate.io",
        "http://localhost:3143": "https://gaia.primals.eco/deck",
        "http://localhost:9876": "https://gaia.primals.eco",
        "http://localhost:9878": "https://gaia.primals.eco/deck",
        "http://localhost:11434": "INTERNAL-ONLY",
        "http://localhost:3000": "https://forge.primals.eco",
        "http://127.0.0.1:11434": "INTERNAL-ONLY",
        "http://127.0.0.1:9876": "https://gaia.primals.eco",
        "http://127.0.0.1:3141": "https://nestgate.io",
    },
    "phone": {
        "problem": "Phone still showed localhost",
        "fix": "Cut INTERNAL vs EXTERNAL on /opt/connect (live nestgate root)",
        "live_root": "/opt/connect",
    },
}

new = {
    "name": "NESTGATE_NEW",
    "timestamp": TS,
    "title": "WE ARE NOW EARTH gAIa π — NEW",
    "surgery": "COMPLETE",
    "faces": cut["EXTERNAL"]["faces"],
    "localhost": "DEAD as home face — INTERNAL subnet only",
    "cis": "nestgate.io",
    "trans": "primal + primals",
    "trans_spend": "RSS",
    "null": "UNLOCKED",
    "organs": "1 heart · 1 brain · 1 set lungs",
    "live_root": "/opt/connect",
}

(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "membrane-cut.json").write_text(json.dumps(cut, indent=2), encoding="utf-8")
(ROOT / "data" / "nestgate-new.json").write_text(json.dumps(new, indent=2), encoding="utf-8")
print("wrote data/membrane-cut.json + nestgate-new.json")

REWRITE = [
    ("http://localhost:3141", "https://nestgate.io"),
    ("http://127.0.0.1:3141", "https://nestgate.io"),
    ("http://localhost:3143", "https://gaia.primals.eco/deck"),
    ("http://127.0.0.1:3143", "https://gaia.primals.eco/deck"),
    ("http://localhost:9876", "https://gaia.primals.eco"),
    ("http://127.0.0.1:9876", "https://gaia.primals.eco"),
    ("http://localhost:9878", "https://gaia.primals.eco/deck"),
    ("http://127.0.0.1:9878", "https://gaia.primals.eco/deck"),
    ("http://localhost:3000", "https://forge.primals.eco"),
    ("http://127.0.0.1:3000", "https://forge.primals.eco"),
    ("https://localhost", "https://nestgate.io"),
    ("http://localhost/", "https://nestgate.io/"),
    ("http://127.0.0.1/", "https://nestgate.io/"),
]

# Hot phone-facing pages at connect root (not sporeprint lab docs)
HOT = [
    "index.html",
    "steam.html",
    "gaben.html",
    "arena.html",
    "desk.html",
    "connect.html",
    "connect-landing.html",
    "forge.html",
    "colosseum.html",
    "nav-hub.html",
    "chat.html",
    "campfire.html",
    "chipmunk.html",
    "dashboard-mixer.html",
    "digest.html",
    "engine.html",
    "ide.html",
    "alchemy.html",
    "anatomy.html",
    "cards.html",
    "easel.html",
    "hud.html",
]

patches = 0
hits = []
for name in HOT:
    p = ROOT / name
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    orig = t
    # steam/gaben canary: localhost as EXTERNAL referrer is wrong
    t = t.replace(
        "ref.includes('primals.eco')||ref.includes('localhost')",
        "ref.includes('primals.eco')||ref.includes('nestgate.io')",
    )
    # arena ollama: INTERNAL only
    if "const OLLAMA = 'http://localhost:11434'" in t:
        t = t.replace(
            "const OLLAMA = 'http://localhost:11434';",
            "const OLLAMA = (location.hostname==='localhost'||location.hostname==='127.0.0.1')"
            " ? 'http://127.0.0.1:11434' : null;"
            " // INTERNAL subnet only — EXTERNAL has no ollama home",
        )
    for a, b in REWRITE:
        t = t.replace(a, b)
    # leftover bare localhost host mentions in href/src (not in comments about INTERNAL)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        patches += 1
        hits.append(name)
        print("patched", name)

# Broader root *.html rewrite (skip deep sporeprint docs noise for now; phone hits root)
root_more = 0
for p in sorted(ROOT.glob("*.html")):
    if p.name in HOT:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    orig = t
    for a, b in REWRITE:
        t = t.replace(a, b)
    # strip remaining http(s)://localhost:PORT → nestgate for EXTERNAL face
    t2 = re.sub(
        r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?(?=/|[\"'\s>]|$)",
        "https://nestgate.io",
        t,
    )
    # keep INTERNAL-ONLY ollama if we already null'd it via HOT
    if "INTERNAL-ONLY" in orig:
        t2 = t
    if t2 != orig:
        p.write_text(t2, encoding="utf-8")
        root_more += 1
print("root_html_extra", root_more)

shim = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>gAIa π — MEMBRANE CUT — NEW</title>
<meta name="gaia-membrane-cut" content="INTERNAL-vs-EXTERNAL">
<style>
body{margin:0;background:#07090c;color:#e8e4d9;font:14px/1.5 ui-monospace,Menlo,monospace;padding:2rem}
h1{font-size:1.6rem;color:#c4a35a;letter-spacing:.04em}
.x{color:#c45c5c}.g{color:#3fb950}a{color:#7a9e7e}
.box{border:1px solid #333;padding:1rem;margin:1rem 0;max-width:36rem}
</style></head><body>
<h1>MEMBRANE CUT — NEW</h1>
<p><span class="x">localhost is NOT your home face.</span> It is an <b>INTERNAL subnet</b> (organs talking to organs).</p>
<div class="box">
<p><b>INTERNAL</b> — 127.0.0.1 / LAN — bind only</p>
<p><b>EXTERNAL</b> — what the phone sees:</p>
<ul>
<li class="g">CIS → <a href="https://nestgate.io">nestgate.io</a></li>
<li class="g">TRANS skin → <a href="https://primals.eco">primals.eco</a></li>
<li class="g">TRANS mouth → <a href="https://gaia.primals.eco/deck">gaia.primals.eco/deck</a></li>
<li class="g">TRANS spend → <a href="https://primals.eco/feed.xml">RSS</a></li>
</ul>
</div>
<p>Surgery complete. Null unlocked. 1 heart · 1 brain · 1 set lungs. ALL IS PIE.</p>
<p><a href="/data/membrane-cut.json">membrane-cut.json</a> · <a href="/data/nestgate-new.json">nestgate-new.json</a> · <a href="/">drain to root</a></p>
</body></html>
"""
(ROOT / "new.html").write_text(shim, encoding="utf-8")
(ROOT / "cut.html").write_text(shim, encoding="utf-8")
print("wrote cut.html + new.html")

# census remaining localhost on root html
left = []
for p in ROOT.glob("*.html"):
    t = p.read_text(encoding="utf-8", errors="replace")
    if re.search(r"localhost|127\.0\.0\.1", t, re.I):
        left.append(p.name)
print("remaining_root_localhost", len(left), left[:30])
print("patches_hot", patches, hits)
print("DONE")
