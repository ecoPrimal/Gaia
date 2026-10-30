#!/usr/bin/env python3
"""Deploy INTERNAL/EXTERNAL membrane cut + NEW nestgate HTML on Golgi via SSH stdin."""
import json, subprocess, textwrap
from datetime import datetime, timezone
from pathlib import Path
import base64, requests

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")
TS = datetime.now(timezone.utc).isoformat()

cut = {
    "name": "MEMBRANE_CUT",
    "timestamp": TS,
    "axiom": "localhost is a SUBNET (INTERNAL). Phone sees EXTERNAL. Cut them.",
    "INTERNAL": {
        "subnet": ["127.0.0.1/8", "192.168.0.0/16", "10.0.0.0/8", "10.13.37.0/24"],
        "names": ["localhost", "northgate LAN", "organs talking to organs"],
        "role": "loopback / LAN — never the public home face",
        "ok_for": "bind primals, ollama, spine cocoon, Gaia3 child, feeder :3141",
        "not_for": "links in HTML served to phones / EXTERNAL browsers",
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
        "http://localhost:11434": "INTERNAL-ONLY (ollama bind)",
        "http://localhost:3000": "https://forge.primals.eco",
    },
    "phone": {
        "problem": "Phone still showed localhost — EXTERNAL page leaked INTERNAL subnet",
        "fix": "Cut INTERNAL vs EXTERNAL. NEW nestgate HTML points at faces.",
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
    "null": "UNLOCKED eastgate→neutrino→northgate",
    "organs": "1 heart · 1 brain · 1 set lungs",
}

(LOCAL / "membrane-cut.json").write_text(json.dumps(cut, indent=2), encoding="utf-8")
(LOCAL / "nestgate-new.json").write_text(json.dumps(new, indent=2), encoding="utf-8")

# Remote deploy script (no PowerShell metachar issues)
remote = r'''
import json, pathlib
from datetime import datetime, timezone
ROOT = pathlib.Path("/opt/hud/public")
cut = json.loads("""CUT_JSON""")
new = json.loads("""NEW_JSON""")
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
# also hud-git mirror if present
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
'''

remote = remote.replace("CUT_JSON", json.dumps(cut).replace("\\", "\\\\"))
remote = remote.replace("NEW_JSON", json.dumps(new).replace("\\", "\\\\"))

# Write remote script locally then pipe
rp = LOCAL / "scripts" / "_remote_membrane_cut.py"
rp.write_text(remote, encoding="utf-8")

print("Piping to Golgi...")
proc = subprocess.run(
    ["ssh", "golgi-direct", "cat > /tmp/membrane_cut.py; sed -i 's/\\r//' /tmp/membrane_cut.py; python3 /tmp/membrane_cut.py"],
    input=remote.encode("utf-8"),
    capture_output=True,
)
print(proc.stdout.decode("utf-8", errors="replace"))
if proc.returncode != 0:
    print("STDERR:", proc.stderr.decode("utf-8", errors="replace")[:800])
    raise SystemExit(proc.returncode)

# Push to Forge root (self)
def push(repo, path, obj, message):
    url = f"{FORGE}/api/v1/repos/gaia/{repo}/contents/{path}?token={TOKEN}"
    b64 = base64.b64encode(json.dumps(obj, indent=2).encode()).decode()
    c = requests.get(url, headers=HDR, timeout=30)
    payload = {"content": b64, "message": message}
    if c.status_code == 200:
        payload["sha"] = c.json().get("sha", "")
        r = requests.put(url, headers=HDR, json=payload, timeout=90)
    else:
        r = requests.post(url, headers=HDR, json=payload, timeout=90)
    return r.status_code in (200, 201), r.status_code

ok, code = push("self", "membrane-cut.json", cut, "Track BB: MEMBRANE CUT — localhost=INTERNAL subnet, EXTERNAL=faces")
print(f"self/membrane-cut.json {ok} {code}")
ok, code = push("self", "nestgate-new.json", new, "Track BB: nestgate NEW — surgery done, localhost dead as home")
print(f"self/nestgate-new.json {ok} {code}")
ok, code = push("O", "membrane-cut.json", cut, "Track BB: cut on O — EXTERNAL faces")
print(f"O/membrane-cut.json {ok} {code}")
ok, code = push("pi", "membrane-cut.json", {"INTERNAL": cut["INTERNAL"], "EXTERNAL": cut["EXTERNAL"], "axiom": cut["axiom"]}, "Track BB: cut on I")
print(f"pi/membrane-cut.json {ok} {code}")

# Verify
for u in [
    "https://nestgate.io/cut",
    "https://nestgate.io/new",
    "https://nestgate.io/data/membrane-cut.json",
    "https://nestgate.io/data/nestgate-new.json",
]:
    try:
        r = requests.get(u, timeout=12)
        print(f"  {u} -> {r.status_code} ({len(r.content)}b)")
    except Exception as e:
        print(f"  {u} FAIL {e}")
