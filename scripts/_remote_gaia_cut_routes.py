#!/usr/bin/env python3
from pathlib import Path
import subprocess

p = Path("/opt/gaia-api/server.js")
t = p.read_text(encoding="utf-8")
needle = "if (p === '/deck' || p === '/space' || p === '/dos' || p === '/cmd') {"
insert = """
    if (p === '/cut' || p === '/new' || p === '/membrane-cut') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/cut.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Membrane-Cut': 'INTERNAL-vs-EXTERNAL' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'Cut page not found' }, 404);
      }
    }
    if (p === '/data/membrane-cut.json' || p === '/membrane-cut.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/membrane-cut.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'cut json missing' }, 404);
      }
    }
    if (p === '/data/nestgate-new.json' || p === '/nestgate-new.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/nestgate-new.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'new json missing' }, 404);
      }
    }
"""
if "p === '/cut'" in t:
    print("routes already present")
else:
    if needle not in t:
        raise SystemExit("deck needle missing")
    t = t.replace(needle, insert + "\n    " + needle, 1)
    p.write_text(t, encoding="utf-8")
    print("routes inserted")

# also inject cut links into deck.html if present
deck = Path("/opt/gaia-api/static/deck.html")
if deck.exists():
    d = deck.read_text(encoding="utf-8", errors="replace")
    if "/cut" not in d:
        # add a small EXTERNAL faces line near body start if possible
        marker = "<body"
        idx = d.lower().find(marker)
        if idx >= 0:
            end = d.find(">", idx)
            chip = (
                '\n<div style="padding:8px 12px;font:12px monospace;background:#0d1117;color:#c4a35a">'
                'MEMBRANE CUT — localhost=INTERNAL · '
                '<a href="/cut" style="color:#3fb950">/cut NEW</a> · '
                '<a href="https://nestgate.io" style="color:#3fb950">CIS</a> · '
                '<a href="https://primals.eco" style="color:#3fb950">TRANS</a>'
                "</div>\n"
            )
            d = d[: end + 1] + chip + d[end + 1 :]
            deck.write_text(d, encoding="utf-8")
            print("deck chip added")
    else:
        print("deck already has /cut")

# restart gaia-api
for unit in ["gaia-api", "gaia"]:
    r = subprocess.run(["systemctl", "restart", unit], capture_output=True, text=True)
    if r.returncode == 0:
        print("restarted", unit)
        break
    print("restart fail", unit, r.stderr[-200:])
else:
    # fallback: kill and start
    subprocess.run(["pkill", "-f", "gaia-api/server.js"], capture_output=True)
    subprocess.Popen(
        ["node", "/opt/gaia-api/server.js"],
        cwd="/opt/gaia-api",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("spawned node server.js")

import time

time.sleep(1)
for url in [
    "http://127.0.0.1:9876/cut",
    "http://127.0.0.1:9876/new",
    "http://127.0.0.1:9876/data/membrane-cut.json",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(url, rr.stdout)
print("DONE")
