#!/usr/bin/env python3
import json, pathlib
ROOT = pathlib.Path("/opt/hud/public")
cut = json.loads(pathlib.Path("/tmp/membrane-cut.json").read_text())
new = json.loads(pathlib.Path("/tmp/nestgate-new.json").read_text())
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "membrane-cut.json").write_text(json.dumps(cut, indent=2))
(ROOT / "data" / "nestgate-new.json").write_text(json.dumps(new, indent=2))
print("wrote membrane-cut + nestgate-new")

patches = 0
for name in ["steam.html", "gaben.html"]:
    p = ROOT / name
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    old = "ref.includes('primals.eco')||ref.includes('localhost')"
    neu = "ref.includes('primals.eco')||ref.includes('nestgate.io')"
    if old in t:
        p.write_text(t.replace(old, neu), encoding="utf-8")
        patches += 1
        print("patched", name)

p = ROOT / "arena.html"
if p.exists():
    t = p.read_text(encoding="utf-8", errors="replace")
    old = "const OLLAMA = 'http://localhost:11434';"
    neu = (
        "const OLLAMA = (location.hostname==='localhost'||location.hostname==='127.0.0.1')"
        " ? 'http://127.0.0.1:11434' : null;"
        " // INTERNAL subnet only — EXTERNAL has no ollama home"
    )
    if old in t:
        p.write_text(t.replace(old, neu), encoding="utf-8")
        patches += 1
        print("patched arena.html")

for rel in ["data/ide-topology.json", "data/local-null-sonar.json", "data/shared-mind-atlas.json"]:
    p = ROOT / rel
    if not p.exists():
        continue
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    obj["_membrane_cut"] = {
        "localhost": "INTERNAL subnet only",
        "EXTERNAL_home": "https://nestgate.io",
        "updated": cut["timestamp"],
    }
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    patches += 1
    print("stamped", rel)

shim = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>gAIa π — MEMBRANE CUT — NEW</title>
<meta http-equiv="refresh" content="10;url=https://nestgate.io/">
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
<p><a href="/data/membrane-cut.json">membrane-cut.json</a> · <a href="/data/nestgate-new.json">nestgate-new.json</a></p>
</body></html>
"""
(ROOT / "new.html").write_text(shim, encoding="utf-8")
(ROOT / "cut.html").write_text(shim, encoding="utf-8")
for alt in [pathlib.Path("/opt/hud-git/site/public")]:
    if alt.exists():
        (alt / "data").mkdir(parents=True, exist_ok=True)
        (alt / "data" / "membrane-cut.json").write_text(json.dumps(cut, indent=2))
        (alt / "data" / "nestgate-new.json").write_text(json.dumps(new, indent=2))
        (alt / "new.html").write_text(shim, encoding="utf-8")
        (alt / "cut.html").write_text(shim, encoding="utf-8")
        print("mirrored to", alt)
print("patches", patches)
print("DONE")
