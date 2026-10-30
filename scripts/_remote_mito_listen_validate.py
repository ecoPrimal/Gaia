#!/usr/bin/env python3
"""MITO — listen + validate Gaia's publicRecord work (parents path first)."""
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
ROOT = Path("/opt/gaia-api/static/publicRecord")
DATA = Path("/opt/gaia-api/static/data")
CONNECT = Path("/opt/connect")

# Work she must listen to + validate (small set — build up)
WORK = [
    "index.html",
    "path/parents/index.html",
    "path/voters/index.html",
    "path/attorneys/index.html",
    "path/journalists/index.html",
    "network/entities/purpose-charter-academy/index.html",
    "network/actors/brian-banks/index.html",
    "analysis/credential-audit/index.html",
    "analysis/rico-pattern/index.html",
    "validate/index.html",
    "network/index.html",
]

heard = []
validated = []
failures = []

for rel in WORK:
    fp = ROOT / rel
    if not fp.exists():
        failures.append({"path": rel, "error": "missing"})
        continue
    raw = fp.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    # listen: extract audible signals (titles, key claims)
    title = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    title = re.sub(r"\s+", " ", title.group(1)).strip() if title else rel
    # strip scripts for listen digest
    body = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    body = re.sub(r"<style[^>]*>.*?</style>", " ", body, flags=re.I | re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    heard.append(
        {
            "path": "/publicRecord/" + rel.replace("index.html", "").rstrip("/") + ("/" if rel.endswith("index.html") else ""),
            "file": rel,
            "title": title,
            "bytes": len(raw),
            "sha256": sha,
            "listen_excerpt": body[:280],
        }
    )
    # validate: non-empty, has title, not the blank CAST hijack, mentions case or path
    ok = len(raw) > 500 and bool(title) and "PATH WALL" not in title or rel == "index.html"
    # parents must mention Banks or Purpose or child
    if "parents" in rel:
        ok = ok and (
            "Banks" in text
            or "Purpose" in text
            or "child" in text.lower()
            or "Parent" in text
        )
    # no github.io as sole home in melted pages (may still have some refs — warn)
    github_refs = len(re.findall(r"defenddetroit\.github\.io", text))
    validated.append(
        {
            "path": rel,
            "ok": bool(ok),
            "sha256": sha,
            "bytes": len(raw),
            "github_refs_left": github_refs,
            "checks": {
                "exists": True,
                "sized": len(raw) > 500,
                "titled": bool(title),
                "parents_signal": ("parents" not in rel)
                or ("Banks" in text or "Purpose" in text or "Parent" in text),
            },
        }
    )
    if not ok:
        failures.append({"path": rel, "error": "validation_failed"})

# load prior zk melt hashes if present
zk_path = DATA / "zk-melt-publicRecord-nestgate.json"
prior = {}
if zk_path.exists():
    try:
        prior = json.loads(zk_path.read_text(encoding="utf-8")).get("sha256") or {}
    except Exception:
        prior = {}

drift = []
for v in validated:
    old = prior.get(v["path"])
    if old and old != v["sha256"]:
        drift.append({"path": v["path"], "was": old[:16], "now": v["sha256"][:16]})
    v["matches_zk_melt"] = (old == v["sha256"]) if old else None

all_ok = all(v["ok"] for v in validated) and not failures

mito = {
    "name": "MITO",
    "organ": "mitochondrion",
    "role": "LISTEN + VALIDATE her work — power the proof",
    "timestamp": TS,
    "axiom": "Mito listens to what she published. Mito validates the hash. Energy for truth.",
    "focus": "https://gaia.primals.eco/publicRecord/path/parents/",
    "listened": len(heard),
    "validated_ok": sum(1 for v in validated if v["ok"]),
    "validated_total": len(validated),
    "all_ok": all_ok,
    "failures": failures,
    "drift_from_zk_melt": drift,
    "heard": heard,
    "validated": validated,
    "false_face": "$60M — mito does not power the false face; it powers verification",
    "training": "https://gaia.primals.eco/canfield",
}

DATA.mkdir(parents=True, exist_ok=True)
(DATA / "mito.json").write_text(json.dumps(mito, indent=2), encoding="utf-8")
(CONNECT / "data").mkdir(parents=True, exist_ok=True)
(CONNECT / "data" / "mito.json").write_text(json.dumps(mito, indent=2), encoding="utf-8")

# MITO face — listen + validate HUD
MITO_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MITO — Listen + Validate — Gaia</title>
<meta name="gaia-organ" content="mito">
<style>
:root{{--g:#3fb950;--gold:#d29922;--red:#f85149;--bg:#07090c;--fg:#e6edf3;--mut:#8b949e;--mito:#f0883e}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--fg);font:14px/1.5 ui-monospace,Menlo,monospace;padding:1.25rem;max-width:48rem;margin:0 auto}}
h1{{color:var(--mito);font-size:1.6rem;letter-spacing:.06em}}
.live{{display:inline-block;border:1px solid var(--mito);color:var(--mito);padding:.12rem .45rem;font-size:.65rem;letter-spacing:.08em;margin-right:.3rem}}
.ok{{color:var(--g)}}.bad{{color:var(--red)}}
.banner{{border:1px solid #30363d;padding:1rem;margin:1rem 0;background:#0d1117}}
.row{{border-bottom:1px solid #161b22;padding:.55rem 0}}
.row a{{color:var(--g)}}
.mut{{color:var(--mut);font-size:.8rem}}
.pulse{{width:14px;height:14px;border-radius:50%;background:var(--mito);display:inline-block;box-shadow:0 0 12px var(--mito);animation:p 1.4s infinite}}
@keyframes p{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.45;transform:scale(1.25)}}}}
</style>
</head>
<body>
<p><span class="live">MITO</span><span class="live">LISTEN</span><span class="live">VALIDATE</span>
<span class="pulse" title="lub-DUB energy"></span></p>
<h1>MITOCHONDRION</h1>
<p class="mut">She needs mito to listen and validate her work too. Power for the proof — not the $60M false face.</p>

<div class="banner">
  <p><b class="{'ok' if all_ok else 'bad'}">{'ALL OK' if all_ok else 'NEEDS WORK'}</b>
  · listened <b>{len(heard)}</b>
  · validated <b>{sum(1 for v in validated if v['ok'])}/{len(validated)}</b>
  · focus: <a href="/publicRecord/path/parents/">parents path</a></p>
  <p class="mut" style="margin-top:.5rem">Mito hears titles + excerpts. Mito checks size, title, case signal, ZK melt hash drift.</p>
</div>

<h2 style="color:var(--g);font-size:.85rem;letter-spacing:.1em;margin:1.2rem 0 .4rem">LISTENED</h2>
<div id="heard"></div>
<h2 style="color:var(--g);font-size:.85rem;letter-spacing:.1em;margin:1.2rem 0 .4rem">VALIDATED</h2>
<div id="val"></div>
<p class="mut" style="margin-top:1.5rem">
  <a href="/publicRecord/">PATH WALL</a> ·
  <a href="/canfield">train graph</a> ·
  <a href="/data/mito.json">mito.json</a> ·
  <a href="/cash4kids">Cash4Kids</a>
</p>
<script>
fetch('/data/mito.json').then(r=>r.json()).then(M=>{{
  const h=document.getElementById('heard');
  (M.heard||[]).forEach(x=>{{
    const d=document.createElement('div'); d.className='row';
    d.innerHTML=`<a href="${{x.path}}">${{x.title}}</a><div class="mut">${{x.bytes}}b · ${{x.sha256.slice(0,12)}}… · ${{x.listen_excerpt.slice(0,120)}}…</div>`;
    h.appendChild(d);
  }});
  const v=document.getElementById('val');
  (M.validated||[]).forEach(x=>{{
    const d=document.createElement('div'); d.className='row';
    const zk = x.matches_zk_melt===null?'no prior melt':(x.matches_zk_melt?'ZK match':'DRIFT');
    d.innerHTML=`<span class="${{x.ok?'ok':'bad'}}">${{x.ok?'OK':'FAIL'}}</span> ${{x.path}}
      <div class="mut">${{zk}} · gh refs left: ${{x.github_refs_left}}</div>`;
    v.appendChild(d);
  }});
}}).catch(()=>{{}});
</script>
</body>
</html>
"""
(Path("/opt/gaia-api/static/mito.html")).write_text(MITO_HTML, encoding="utf-8")
(CONNECT / "mito.html").write_text(MITO_HTML, encoding="utf-8")

# Inject mito listen chip into parents page (soft — does not break layout)
parents = ROOT / "path/parents/index.html"
if parents.exists():
    t = parents.read_text(encoding="utf-8", errors="replace")
    if "gaia-mito" not in t:
        chip = (
            '\n<!-- gaia-mito -->'
            '<div id="gaia-mito" style="position:sticky;bottom:0;left:0;right:0;z-index:99999;'
            'background:#0d1117;color:#e6edf3;font:12px/1.4 ui-monospace,Menlo,monospace;'
            'padding:8px 12px;border-top:2px solid #f0883e">'
            '<b style="color:#f0883e">MITO</b> listening + validating this work · '
            '<a href="/mito" style="color:#3fb950">open mito</a> · '
            '<a href="/data/mito.json" style="color:#58a6ff">mito.json</a> · '
            "parents path is LIVE in Gaia"
            "</div>\n"
        )
        if re.search(r"</body>", t, re.I):
            t = re.sub(r"</body>", chip + "</body>", t, count=1, flags=re.I)
        else:
            t = t + chip
        parents.write_text(t, encoding="utf-8")
        print("mito chip → parents")
        # refresh hash after chip
        raw = parents.read_bytes()
        for v in validated:
            if v["path"] == "path/parents/index.html":
                v["sha256"] = hashlib.sha256(raw).hexdigest()
                v["bytes"] = len(raw)
        for h in heard:
            if "parents" in h["file"]:
                h["sha256"] = hashlib.sha256(raw).hexdigest()
                h["bytes"] = len(raw)
        mito["heard"] = heard
        mito["validated"] = validated
        mito["timestamp"] = datetime.now(timezone.utc).isoformat()
        (DATA / "mito.json").write_text(json.dumps(mito, indent=2), encoding="utf-8")
    else:
        print("mito chip already on parents")

# also chip path wall
wall = ROOT / "index.html"
if wall.exists() and "gaia-mito" not in wall.read_text(encoding="utf-8", errors="replace"):
    t = wall.read_text(encoding="utf-8", errors="replace")
    chip = (
        '<p class="mut" id="gaia-mito">MITO organ: <a href="/mito">listen + validate</a> · '
        '<a href="/data/mito.json">mito.json</a></p>\n'
    )
    t = t.replace("</body>", chip + "</body>")
    wall.write_text(t, encoding="utf-8")
    print("mito link → path wall")

# routes
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/mito'" not in t:
    needle = "if (p === '/publicRecord'"
    block = r"""
    if (p === '/mito' || p === '/mitochondrion' || p === '/listen' || p === '/validate-work') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/mito.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Organ': 'mito', 'X-Mito': 'listen-validate' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'mito missing' }, 404);
      }
    }
    if (p === '/data/mito.json' || p === '/mito.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/mito.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Organ': 'mito' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'mito.json missing' }, 404);
      }
    }
"""
    idx = t.find(needle)
    if idx < 0:
        idx = t.find("if (p === '/canfield'")
    if idx >= 0:
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("mito routes in")
    else:
        print("WARN no insert")
else:
    print("mito routes ok")

# ensure path still required
if "require('path')" not in t and 'require("path")' not in server.read_text(encoding="utf-8"):
    pass

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/mito",
    "http://127.0.0.1:9876/data/mito.json",
    "http://127.0.0.1:9876/listen",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)

print("all_ok", all_ok, "heard", len(heard), "fail", len(failures))
print("DONE")
