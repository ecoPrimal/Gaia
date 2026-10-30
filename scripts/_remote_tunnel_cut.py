#!/usr/bin/env python3
"""Route nestgate to live tunnel + publish cut on gaia-api (tunnel-live)."""
import json
import shutil
import subprocess
from pathlib import Path

CONNECT = Path("/opt/connect")
GAIA_STATIC = Path("/opt/gaia-api/static")
GAIA_STATIC.mkdir(parents=True, exist_ok=True)

# Publish cut/new onto gaia-api static (served by :9876 → gaia.primals.eco tunnel)
for name in ["cut.html", "new.html"]:
    shutil.copy2(CONNECT / name, GAIA_STATIC / name)
    print("gaia-static", name)

(GAIA_STATIC / "data").mkdir(exist_ok=True)
for name in ["membrane-cut.json", "nestgate-new.json"]:
    src = CONNECT / "data" / name
    if src.exists():
        shutil.copy2(src, GAIA_STATIC / "data" / name)
        print("gaia-data", name)

# Also put under /opt/gaia-api if it serves public differently
for alt in [Path("/opt/gaia-api/public"), Path("/opt/hud/public")]:
    if not alt.exists():
        continue
    (alt / "data").mkdir(exist_ok=True)
    for name in ["cut.html", "new.html"]:
        shutil.copy2(CONNECT / name, alt / name)
    for name in ["membrane-cut.json", "nestgate-new.json"]:
        src = CONNECT / "data" / name
        if src.exists():
            shutil.copy2(src, alt / "data" / name)
    print("mirrored", alt)

# List tunnel routes
r = subprocess.run(["cloudflared", "tunnel", "route", "ip", "show"], capture_output=True, text=True)
print("route ip show", (r.stdout or r.stderr or "")[:500])
r = subprocess.run(["cloudflared", "tunnel", "info", "2c12060a-8582-47c2-b8ff-c7c157f036d9"], capture_output=True, text=True)
print("tunnel info", (r.stdout or r.stderr or "")[:800])

# Force DNS route for nestgate.io to THIS tunnel (overwrite)
for cmd in [
    ["cloudflared", "tunnel", "route", "dns", "--overwrite-dns", "2c12060a-8582-47c2-b8ff-c7c157f036d9", "nestgate.io"],
    ["cloudflared", "tunnel", "route", "dns", "2c12060a-8582-47c2-b8ff-c7c157f036d9", "nestgate.io."],
]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("DNS", " ".join(cmd[-2:]), r.returncode, (r.stdout or "")[-300:], (r.stderr or "")[-400:])

# Ensure gaia-api serves cut.html — check how static is mounted
app_candidates = list(Path("/opt/gaia-api").glob("**/*.{js,py,ts}"))[:5]
print("gaia-api sample", [str(p) for p in app_candidates])
for p in Path("/opt/gaia-api").iterdir():
    print(" ", p.name)

# quick local probe
for url in [
    "https://127.0.0.1/cut.html",
    "http://127.0.0.1:9876/cut.html",
    "http://127.0.0.1:9876/static/cut.html",
]:
    rr = subprocess.run(
        ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", url, "-H", "Host: nestgate.io"],
        capture_output=True,
        text=True,
    )
    # Host header only for nestgate
    if "9876" in url:
        rr = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True,
            text=True,
        )
    print(url, rr.stdout)

print("DONE")
