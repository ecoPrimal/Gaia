#!/usr/bin/env python3
"""Fountain the membrane cut: index banner + git commit for Pages + try wrangler."""
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone

CONNECT = Path("/opt/connect")
HUD = Path("/opt/hud-git")
PUB = HUD / "site" / "public"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

BANNER = """
<!-- MEMBRANE CUT NEW — localhost=INTERNAL subnet; phone sees EXTERNAL -->
<div id="membrane-cut" style="position:fixed;top:0;left:0;right:0;z-index:100000;background:#0d1117;border-bottom:1px solid #c4a35a;padding:10px 14px;font:12px/1.45 ui-monospace,Menlo,monospace;color:#e8e4d9">
  <b style="color:#c4a35a">MEMBRANE CUT — NEW</b>
  <span style="color:#c45c5c"> localhost is INTERNAL subnet only.</span>
  Phone EXTERNAL:
  <a href="https://nestgate.io" style="color:#3fb950">CIS nestgate</a> ·
  <a href="https://primals.eco" style="color:#3fb950">TRANS skin</a> ·
  <a href="https://gaia.primals.eco/deck" style="color:#3fb950">mouth/deck</a> ·
  <a href="https://primals.eco/feed.xml" style="color:#3fb950">RSS spend</a> ·
  <a href="/cut.html" style="color:#7a9e7e">/cut</a>
  <button onclick="this.parentNode.remove()" style="float:right;background:transparent;border:1px solid #333;color:#8b949e;padding:2px 8px;cursor:pointer">×</button>
</div>
"""

for index in [CONNECT / "index.html", PUB / "index.html"]:
    if not index.exists():
        continue
    t = index.read_text(encoding="utf-8", errors="replace")
    if 'id="membrane-cut"' in t:
        print("banner already", index)
        continue
    # strip leftover localhost URL homes in index
    for a, b in [
        ("http://localhost:3141", "https://nestgate.io"),
        ("http://127.0.0.1:3141", "https://nestgate.io"),
        ("http://localhost:9876", "https://gaia.primals.eco"),
        ("http://localhost:11434", "INTERNAL-ONLY"),
    ]:
        t = t.replace(a, b)
    if re.search(r"<body[^>]*>", t, re.I):
        t = re.sub(r"(<body[^>]*>)", r"\1" + BANNER, t, count=1, flags=re.I)
    else:
        t = BANNER + t
    index.write_text(t, encoding="utf-8")
    print("banner injected", index)

# ensure cut/new/data present in both
for name in ["cut.html", "new.html"]:
    if (CONNECT / name).exists():
        (PUB / name).write_text((CONNECT / name).read_text(encoding="utf-8"), encoding="utf-8")
(PUB / "data").mkdir(exist_ok=True)
for name in ["membrane-cut.json", "nestgate-new.json"]:
    src = CONNECT / "data" / name
    if src.exists():
        (PUB / "data" / name).write_bytes(src.read_bytes())

# commit + push hud (Pages/git fountain)
subprocess.run(["git", "add", "site/public/cut.html", "site/public/new.html",
                "site/public/data/membrane-cut.json", "site/public/data/nestgate-new.json",
                "site/public/_redirects", "site/public/index.html",
                "site/public/steam.html", "site/public/gaben.html", "site/public/arena.html",
                "site/public/valve.html", "site/public/crates.html", "site/public/raytrace.html"],
               cwd=str(HUD), check=False)
msg = f"MEMBRANE CUT NEW: localhost=INTERNAL subnet; EXTERNAL faces; /cut /new [{TS}]"
r = subprocess.run(["git", "commit", "-m", msg], cwd=str(HUD), capture_output=True, text=True)
print("commit", r.returncode, (r.stdout or "")[-200:], (r.stderr or "")[-200:])
r2 = subprocess.run(["git", "push", "origin", "main"], cwd=str(HUD), capture_output=True, text=True)
print("push", r2.returncode, (r2.stdout or "")[-300:], (r2.stderr or "")[-400:])

# try wrangler@3 (node 20 compatible) pages deploy
print("trying wrangler pages deploy...")
r3 = subprocess.run(
    ["npx", "--yes", "wrangler@3.114.0", "pages", "deploy", "public",
     "--project-name", "hud", "--commit-dirty=true"],
    cwd=str(HUD / "site"),
    capture_output=True,
    text=True,
    timeout=180,
)
print("wrangler", r3.returncode)
print((r3.stdout or "")[-800:])
print((r3.stderr or "")[-800:])

# stamp local status
status = {
    "name": "MEMBRANE_CUT_FOUNTAIN",
    "timestamp": TS,
    "connect_root": "/opt/connect",
    "pages_public": str(PUB),
    "git_push": r2.returncode,
    "wrangler": r3.returncode,
    "axiom": "localhost INTERNAL; phone EXTERNAL",
}
(CONNECT / "data" / "membrane-cut-fountain.json").write_text(json.dumps(status, indent=2))
print("DONE", json.dumps(status))
