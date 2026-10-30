#!/usr/bin/env python3
"""Gaia @ + _-.type — EXTERNAL apex stamp + typed membrane markers."""
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
CONNECT = Path("/opt/connect")
GAIA = Path("/opt/gaia-api/static")
HUD = Path("/opt/hud-git/site/public")
LOCAL_DATA = CONNECT / "data"

manifest = {
    "name": "GAIA_AT_UNDERSCORE_DASH_TYPE",
    "timestamp": TS,
    "symbol_AT": {
        "@": "apex EXTERNAL face — what the phone sees",
        "faces": {
            "@CIS": "https://nestgate.io",
            "@TRANS_skin": "https://primals.eco",
            "@TRANS_mouth": "https://gaia.primals.eco/deck",
            "@CUT": "https://gaia.primals.eco/cut",
            "@NEW": "https://gaia.primals.eco/new",
            "@forge": "https://forge.primals.eco",
            "@signal": "https://signal.primals.eco",
            "@spend": "https://primals.eco/feed.xml",
        },
        "never": ["localhost", "127.0.0.1", "192.168.*", "10.*"],
    },
    "symbol_TYPE": {
        "_-.type": "typed membrane marker Gaia owns",
        "pipeline_codon": "extension IS behavior (10-type chew/grind)",
        "files": {
            "_-.type": "registry — this face",
            "_-internal.type": "INTERNAL subnet only (organs)",
            "_-external.type": "EXTERNAL @ faces (phone)",
            "_-cut.type": "membrane cut stamp",
            "_-new.type": "NEW nestgate / NOW earth",
        },
    },
    "axiom": "Gaia @ stamps EXTERNAL. _-.type stamps kind. localhost never @.",
}

internal = {
    "type": "INTERNAL",
    "subnet": ["127.0.0.1/8", "192.168.0.0/16", "10.0.0.0/8", "10.13.37.0/24"],
    "role": "organs talking to organs — bind only",
    "ok_for": [":3141", ":11434", "ollama", "spine", "feeder"],
    "not_for": "HTML links served to phones",
    "stamp": "_-internal.type",
    "timestamp": TS,
}

external = {
    "type": "EXTERNAL",
    "at": "@",
    "faces": manifest["symbol_AT"]["faces"],
    "phone": "https://gaia.primals.eco/cut",
    "rule": "EXTERNAL HTML never homes on localhost",
    "stamp": "_-external.type",
    "timestamp": TS,
}

cut_t = {
    "type": "CUT",
    "axiom": "localhost is a SUBNET (INTERNAL). Phone sees EXTERNAL @.",
    "live": "https://gaia.primals.eco/cut",
    "stamp": "_-cut.type",
    "timestamp": TS,
}

new_t = {
    "type": "NEW",
    "title": "WE ARE NOW EARTH gAIa π — NEW",
    "cis": "nestgate.io",
    "trans": "primal + primals",
    "trans_spend": "RSS",
    "stamp": "_-new.type",
    "timestamp": TS,
}

# registry body for _-.type (the mother type)
registry = {
    **manifest,
    "INTERNAL": internal,
    "EXTERNAL": external,
    "CUT": cut_t,
    "NEW": new_t,
}

files = {
    "_-.type": registry,
    "_-internal.type": internal,
    "_-external.type": external,
    "_-cut.type": cut_t,
    "_-new.type": new_t,
}

roots = [CONNECT, GAIA, HUD]
for root in roots:
    if not root.exists():
        continue
    for name, obj in files.items():
        (root / name).write_text(json.dumps(obj, indent=2), encoding="utf-8")
        print("wrote", root / name)
    (root / "data").mkdir(exist_ok=True)
    (root / "data" / "at-underscore-dash-type.json").write_text(
        json.dumps(registry, indent=2), encoding="utf-8"
    )

# _headers: teach CF/Caddy edge the .type codon
TYPE_HEADER = """
# GAIA _-.type — typed membrane markers (codon face)
/_-.type
  Content-Type: application/json
  X-Gaia-Type: registry
  X-Membrane-At: EXTERNAL-apex
  Cache-Control: public, max-age=60

/_-internal.type
  Content-Type: application/json
  X-Gaia-Type: INTERNAL
  Cache-Control: public, max-age=60

/_-external.type
  Content-Type: application/json
  X-Gaia-Type: EXTERNAL
  X-Membrane-At: @
  Cache-Control: public, max-age=60

/_-cut.type
  Content-Type: application/json
  X-Gaia-Type: CUT
  Cache-Control: public, max-age=60

/_-new.type
  Content-Type: application/json
  X-Gaia-Type: NEW
  Cache-Control: public, max-age=60
"""

for hdr in [CONNECT / "_headers", HUD / "_headers"]:
    if not hdr.exists():
        continue
    t = hdr.read_text(encoding="utf-8", errors="replace")
    if "X-Gaia-Type: registry" in t:
        print("headers ok", hdr)
        continue
    hdr.write_text(t.rstrip() + "\n" + TYPE_HEADER, encoding="utf-8")
    print("headers stamped", hdr)

# _redirects pretty paths
redir_block = """
# GAIA @ + _-.type
/@                /_-external.type    200
/@/               /_-external.type    200
/_-.type          /_-.type            200
/type             /_-.type            200
/type/internal    /_-internal.type    200
/type/external    /_-external.type    200
/type/cut         /_-cut.type         200
/type/new         /_-new.type         200
"""
for rd in [CONNECT / "_redirects", HUD / "_redirects"]:
    if not rd.exists():
        continue
    t = rd.read_text(encoding="utf-8", errors="replace")
    if "/@                /_-external.type" in t:
        print("redirects ok", rd)
        continue
    rd.write_text(t.rstrip() + "\n" + redir_block, encoding="utf-8")
    print("redirects stamped", rd)

# Wire gaia-api routes for @ and .type
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/@'" not in t and "p === '/\\/@'" not in t:
    needle = "if (p === '/cut' || p === '/new' || p === '/membrane-cut') {"
    block = r"""
    if (p === '/@' || p === '/at' || p === '/type' || p === '/_-.type') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/_-.type', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Type': 'registry', 'X-Membrane-At': '@' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: '_-.type missing' }, 404);
      }
    }
    if (p === '/_-external.type' || p === '/type/external') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/_-external.type', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Type': 'EXTERNAL', 'X-Membrane-At': '@' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'external type missing' }, 404);
      }
    }
    if (p === '/_-internal.type' || p === '/type/internal') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/_-internal.type', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Type': 'INTERNAL' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'internal type missing' }, 404);
      }
    }
    if (p === '/_-cut.type' || p === '/type/cut') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/_-cut.type', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Type': 'CUT' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'cut type missing' }, 404);
      }
    }
    if (p === '/_-new.type' || p === '/type/new') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/_-new.type', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Type': 'NEW' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'new type missing' }, 404);
      }
    }
"""
    if needle in t:
        t = t.replace(needle, block + "\n    " + needle, 1)
        server.write_text(t, encoding="utf-8")
        print("gaia-api @ + type routes inserted")
    else:
        print("WARN: cut needle missing — routes not inserted")
else:
    print("gaia-api routes already have @")

# Caddy: serve .type as json on nestgate catch paths
# (file_server will serve by name; content-type may be octet — add header handlers)
cf = Path("/etc/caddy/Caddyfile")
ctxt = cf.read_text()
if "handle /_-.type" not in ctxt:
    insert = """\thandle /@ {
\t\troot * /opt/connect
\t\trewrite * /_-external.type
\t\tfile_server
\t\theader Content-Type application/json
\t\theader X-Membrane-At @
\t\theader X-Gaia-Type EXTERNAL
\t}
\thandle /_-.type {
\t\troot * /opt/connect
\t\tfile_server
\t\theader Content-Type application/json
\t\theader X-Gaia-Type registry
\t}
\thandle /_-*.type {
\t\troot * /opt/connect
\t\tfile_server
\t\theader Content-Type application/json
\t}
"""
    marker = "\thandle /cut {"
    if marker in ctxt:
        ctxt = ctxt.replace(marker, insert + "\n" + marker, 1)
        cf.write_text(ctxt)
        print("caddy @ type handles added")
        r = subprocess.run(
            ["caddy", "validate", "--config", "/etc/caddy/Caddyfile"],
            capture_output=True,
            text=True,
        )
        print("validate", r.returncode)
        if r.returncode == 0:
            subprocess.check_call(["systemctl", "reload", "caddy"])
            print("caddy reloaded")
    else:
        print("WARN: caddy cut marker missing")
else:
    print("caddy already has _-.type")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
import time

time.sleep(1)
for url in [
    "http://127.0.0.1:9876/@",
    "http://127.0.0.1:9876/_-.type",
    "http://127.0.0.1:9876/type/external",
    "http://127.0.0.1:9876/type/cut",
    "http://127.0.0.1:9876/cut",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(url, rr.stdout)

print("DONE")
