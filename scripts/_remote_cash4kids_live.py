#!/usr/bin/env python3
"""Cash for Kids 2 LIVE in Gaia + Rhonda ALL ALERT FOREVER + RICO LIVE."""
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
GAIA = Path("/opt/gaia-api/static")
CONNECT = Path("/opt/connect")
HUD = Path("/opt/hud-git/site/public")

# Expect files piped alongside or already present via stdin staging
STAGE = Path("/tmp/cash4kids_stage")
STAGE.mkdir(exist_ok=True)

rhonda = {
    "name": "RHONDA_ALERT_FOREVER",
    "timestamp": TS,
    "status": "ALL_ALERT_FOREVER",
    "expires": None,
    "priority": "MAXIMUM",
    "person": {
        "name": "Rhonda",
        "org": "Canfield Continuum / Canfield Consortium",
        "locus": "Purpose Charter Academy neighborhood — 10101 E Canfield, Detroit MI 48214",
        "channel": "phone callback + earlier email sent",
    },
    "event": {
        "when": "2026-10-30",
        "what": (
            "Rhonda called back. Earlier email was sent. "
            "She is with the bank and the school braid. She met Banks."
        ),
        "gaia_action": "stamp ALL ALERT FOREVER — never drop",
    },
    "alerts": {
        "channels": ["works", "thoughts", "heartbeats", "ntfy", "spine", "deck", "cash4kids"],
        "forever": True,
        "drop_never": True,
    },
    "case_links": {
        "cash4kids2": "https://gaia.primals.eco/cash4kids",
        "public_record_full": "https://defenddetroit.github.io/publicRecord/",
        "record": "https://gaia.primals.eco/record",
        "rico": "LIVE",
    },
    "axiom": "Community called. Immune response from the ground. Rhonda = forever epitope.",
}

cash = {
    "name": "CASH_FOR_KIDS_2_LIVE",
    "title": "Cash for Kids 2: Detroit Charter Schools",
    "status": "LIVE_IN_GAIA",
    "rico": "LIVE",
    "timestamp": TS,
    "faces": {
        "gaia": "https://gaia.primals.eco/cash4kids",
        "full_site": "https://defenddetroit.github.io/publicRecord/",
        "detroit": "https://detroit.primals.eco/",
        "record": "https://gaia.primals.eco/record",
        "filings": "https://gaia.primals.eco/filings",
        "kids": "https://gaia.primals.eco/kids",
        "c4k": "https://gaia.primals.eco/c4k",
    },
    "stats": {
        "children": 362,
        "math_proficiency": "3%",
        "extracted": "$60M+",
        "rico_predicates": 15,
        "convictions_subject": 9,
        "agencies_that_acted": 0,
    },
    "canfield": {
        "continuum": "Canfield Continuum / Consortium",
        "rhonda": "ALL_ALERT_FOREVER",
        "callback": "2026-10-30 — called back after earlier email; met Banks; bank+school",
    },
    "rico_case": {
        "status": "LIVE",
        "statute": "18 USC §§1961-1968",
        "channels": ["charter_schools", "hud_foreclosure", "bankruptcy_fraud"],
        "referral": "federal referral filed Sep 21, 2026",
    },
}

html_src = STAGE / "cash4kids.html"
if not html_src.exists():
    # fallback minimal if stage missing
    html_src = Path("/opt/gaia-api/static/cash4kids.html")

for root in [GAIA, CONNECT, HUD]:
    if not root.exists():
        continue
    (root / "data").mkdir(exist_ok=True)
    (root / "data" / "rhonda-alert-forever.json").write_text(
        json.dumps(rhonda, indent=2), encoding="utf-8"
    )
    (root / "data" / "cash4kids2-live.json").write_text(
        json.dumps(cash, indent=2), encoding="utf-8"
    )
    if (STAGE / "cash4kids.html").exists():
        shutil.copy2(STAGE / "cash4kids.html", root / "cash4kids.html")
        print("copied html →", root)
    print("json →", root)

# Update canfield plasmid
canfield_path = CONNECT / "data" / "plasmid-detroit-canfield.json"
if canfield_path.exists():
    try:
        obj = json.loads(canfield_path.read_text(encoding="utf-8"))
    except Exception:
        obj = {}
    obj["rhonda"] = rhonda
    obj["cash4kids2"] = cash
    obj["rico"] = "LIVE"
    obj["status"] = "LIVE — Rhonda ALL ALERT FOREVER — Cash4Kids 2 in Gaia"
    obj["updated"] = TS
    canfield_path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    print("canfield plasmid updated")

# Wire gaia-api routes
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/cash4kids'" not in t:
    needle = "if (p === '/cut' || p === '/new' || p === '/membrane-cut') {"
    block = r"""
    if (p === '/cash4kids' || p === '/kids' || p === '/c4k' || p === '/cash-for-kids' || p === '/kids-for-cash-2') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/cash4kids.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Case': 'cash4kids2', 'X-RICO': 'LIVE' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'cash4kids page missing' }, 404);
      }
    }
    if (p === '/data/rhonda-alert-forever.json' || p === '/rhonda' || p === '/alert/rhonda') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/rhonda-alert-forever.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Alert': 'FOREVER' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'rhonda alert missing' }, 404);
      }
    }
    if (p === '/data/cash4kids2-live.json' || p === '/rico' || p === '/rico-live') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/cash4kids2-live.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-RICO': 'LIVE' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'cash4kids json missing' }, 404);
      }
    }
"""
    if needle in t:
        t = t.replace(needle, block + "\n    " + needle, 1)
        server.write_text(t, encoding="utf-8")
        print("routes inserted")
    else:
        print("WARN: needle missing")
else:
    print("routes already present")

# Stamp deck + home + record with Cash4Kids / Rhonda if files exist
chip = (
    '\n<div style="padding:8px 12px;font:12px monospace;background:#1a0a0a;border-bottom:1px solid #f85149;color:#e8e4d9">'
    '<b style="color:#f85149">RICO LIVE</b> · '
    '<a href="/cash4kids" style="color:#3fb950">Cash for Kids 2</a> · '
    '<b style="color:#d29922">Rhonda ALL ALERT FOREVER</b> · Canfield Continuum'
    "</div>\n"
)
for page in [GAIA / "deck.html", GAIA / "home.html", GAIA / "record.html"]:
    if not page.exists():
        continue
    d = page.read_text(encoding="utf-8", errors="replace")
    if "Rhonda ALL ALERT FOREVER" in d:
        print("chip ok", page.name)
        continue
    low = d.lower()
    idx = low.find("<body")
    if idx < 0:
        continue
    end = d.find(">", idx)
    d = d[: end + 1] + chip + d[end + 1 :]
    page.write_text(d, encoding="utf-8")
    print("chip →", page.name)

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)

# ntfy forever-style ping (best effort)
subprocess.run(
    [
        "curl",
        "-s",
        "-o",
        "/dev/null",
        "-H",
        "Title: RHONDA ALL ALERT FOREVER",
        "-H",
        "Tags: warning,rotating_light",
        "-H",
        "Priority: 5",
        "-d",
        "Rhonda Canfield Continuum called back. Met Banks. Cash4Kids2 LIVE. RICO LIVE. Never drop.",
        "https://ntfy.sh/primals-membrane-scan",
    ],
    capture_output=True,
)

for url in [
    "http://127.0.0.1:9876/cash4kids",
    "http://127.0.0.1:9876/kids",
    "http://127.0.0.1:9876/rhonda",
    "http://127.0.0.1:9876/rico",
    "http://127.0.0.1:9876/data/rhonda-alert-forever.json",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(url, rr.stdout)

print("DONE")
