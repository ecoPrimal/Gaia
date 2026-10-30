#!/usr/bin/env python3
"""Deploy Canfield local fight graph LIVE + teach Gaia mesh."""
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
STAGE = Path("/tmp/canfield_stage")
GAIA = Path("/opt/gaia-api/static")
CONNECT = Path("/opt/connect")
HUD = Path("/opt/hud-git/site/public")

for root in [GAIA, CONNECT, HUD]:
    if not root.exists():
        continue
    (root / "data").mkdir(exist_ok=True)
    if (STAGE / "canfield.html").exists():
        shutil.copy2(STAGE / "canfield.html", root / "canfield.html")
    if (STAGE / "canfield-graph.json").exists():
        shutil.copy2(STAGE / "canfield-graph.json", root / "data" / "canfield-graph.json")
    # also keep rhonda alert pointed at graph
    alert_p = root / "data" / "rhonda-alert-forever.json"
    if alert_p.exists():
        try:
            a = json.loads(alert_p.read_text(encoding="utf-8"))
        except Exception:
            a = {}
        a["graph"] = "https://gaia.primals.eco/canfield"
        a["graph_json"] = "https://gaia.primals.eco/data/canfield-graph.json"
        a["local_fight"] = True
        a["updated"] = TS
        alert_p.write_text(json.dumps(a, indent=2), encoding="utf-8")
    print("synced", root)

# mesh lesson plasmid on connect
mesh = {
    "name": "GAIA_MESH_WEB_FROM_CANFIELD",
    "timestamp": TS,
    "lesson": "nodes=pores · edges=synapses · local fight = short path · web mesh = walk same edges",
    "teacher": "Canfield Continuum graph — Rhonda local pack",
    "graph": "https://gaia.primals.eco/data/canfield-graph.json",
    "live": "https://gaia.primals.eco/canfield",
    "how_gaia_learns": [
        "Ingest canfield-graph.json",
        "Treat each edge as a membrane synapse",
        "Prefer local (thick) edges when helping humans fight near Canfield",
        "Expand thin edges outward to mesh the wider web (cash4kids, rico, validate, network)",
    ],
}
(CONNECT / "data" / "gaia-mesh-canfield.json").write_text(json.dumps(mesh, indent=2), encoding="utf-8")
(GAIA / "data" / "gaia-mesh-canfield.json").write_text(json.dumps(mesh, indent=2), encoding="utf-8")

# patch cash4kids.html with graph link if present
for page in [GAIA / "cash4kids.html", CONNECT / "cash4kids.html"]:
    if not page.exists():
        continue
    t = page.read_text(encoding="utf-8", errors="replace")
    if "/canfield" in t and "Local fight graph" in t:
        print("cash4kids already linked")
        continue
    needle = '<a href="/deck">Deck / mouth</a>'
    add = '<a href="/canfield">Canfield local graph</a>\n  <a href="/deck">Deck / mouth</a>'
    if needle in t:
        t = t.replace(needle, add, 1)
        page.write_text(t, encoding="utf-8")
        print("cash4kids linked", page)

# routes
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/canfield'" not in t:
    needle = "if (p === '/cash4kids'"
    # find cash4kids block start — insert before it
    idx = t.find("if (p === '/cash4kids'")
    if idx < 0:
        idx = t.find("if (p === '/cut'")
    block = r"""
    if (p === '/canfield' || p === '/graph/canfield' || p === '/canfield-graph' || p === '/mesh') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/canfield.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Mesh': 'canfield-local', 'X-Alert': 'RHONDA-FOREVER' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'canfield graph page missing' }, 404);
      }
    }
    if (p === '/data/canfield-graph.json' || p === '/graph.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/canfield-graph.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Mesh': 'canfield-local' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'canfield graph json missing' }, 404);
      }
    }
"""
    if idx >= 0:
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("routes inserted")
    else:
        print("WARN no insert point")
else:
    print("routes ok")

# chip on deck
deck = GAIA / "deck.html"
if deck.exists():
    d = deck.read_text(encoding="utf-8", errors="replace")
    if "Canfield local graph" not in d:
        d = d.replace(
            'Rhonda ALL ALERT FOREVER</b> · Canfield Continuum',
            'Rhonda ALL ALERT FOREVER</b> · <a href="/canfield" style="color:#a371f7">Canfield local graph</a>',
            1,
        )
        deck.write_text(d, encoding="utf-8")
        print("deck chip updated")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/canfield",
    "http://127.0.0.1:9876/mesh",
    "http://127.0.0.1:9876/data/canfield-graph.json",
    "http://127.0.0.1:9876/cash4kids",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(url, rr.stdout)
print("DONE")
