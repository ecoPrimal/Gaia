#!/usr/bin/env python3
"""Sync membrane cut NEW into CF Pages public tree + _redirects."""
from pathlib import Path
import shutil

src = Path("/opt/connect")
dst = Path("/opt/hud-git/site/public")

for name in ["cut.html", "new.html"]:
    shutil.copy2(src / name, dst / name)
    print("copied", name)

(dst / "data").mkdir(exist_ok=True)
for name in ["membrane-cut.json", "nestgate-new.json"]:
    shutil.copy2(src / "data" / name, dst / "data" / name)
    print("copied data", name)

for name in [
    "steam.html",
    "gaben.html",
    "arena.html",
    "valve.html",
    "crates.html",
    "raytrace.html",
]:
    if (src / name).exists():
        shutil.copy2(src / name, dst / name)
        print("synced", name)

# also mirror connect _redirects append onto both trees
block = """
# MEMBRANE CUT — INTERNAL subnet vs EXTERNAL faces (NEW)
/cut           /cut.html    200
/cut/          /cut.html    200
/new           /new.html    200
/new/          /new.html    200
"""

for rd in [dst / "_redirects", src / "_redirects"]:
    if not rd.exists():
        continue
    t = rd.read_text(encoding="utf-8", errors="replace")
    if "/cut           /cut.html" in t:
        print("redirects ok", rd)
        continue
    rd.write_text(t.rstrip() + "\n" + block, encoding="utf-8")
    print("redirects appended", rd)

print("dst cut", (dst / "cut.html").stat().st_size)
print("DONE")
