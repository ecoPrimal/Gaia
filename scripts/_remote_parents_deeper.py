#!/usr/bin/env python3
"""Go DEEPER on parents path — resolve links, melt missing, deepen local pack."""
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, unquote

TS = datetime.now(timezone.utc).isoformat()
SRC = Path("/opt/publicRecord/site/public")
GAIA = Path("/opt/gaia-api/static/publicRecord")
NEST = Path("/opt/connect/publicRecord")
CONNECT_CSS = Path("/opt/connect/css")

parents = GAIA / "path/parents/index.html"
t = parents.read_text(encoding="utf-8", errors="replace")
print("parents bytes", len(t))

hrefs = re.findall(r"""href=["']([^"']+)["']""", t)
print("hrefs", len(hrefs))
for h in hrefs:
    if h.startswith(("#", "mailto:", "javascript:")):
        continue
    print(" ", h)

# Map any absolute/relative link into publicRecord relative path
def to_rel(h: str):
    h = h.strip()
    if h.startswith(("http://", "https://")):
        u = urlparse(h)
        path = u.path or "/"
        # strip prefixes
        for pref in ("/publicRecord/", "/"):
            if "publicRecord" in path:
                idx = path.find("/publicRecord/")
                if idx >= 0:
                    path = path[idx + len("/publicRecord/") :]
                    break
            if "defenddetroit.github.io" in (u.netloc or "") and path.startswith("/publicRecord/"):
                path = path[len("/publicRecord/") :]
                break
        if "detroit.primals.eco" in (u.netloc or ""):
            path = path.lstrip("/")
        path = path.lstrip("/")
        return path
    # relative from /publicRecord/path/parents/
    if h.startswith("../"):
        # resolve against path/parents/
        base = Path("path/parents")
        resolved = (base / h).resolve()
        # can't use resolve outside — manual
        parts = ("path/parents/" + h).split("/")
        out = []
        for p in parts:
            if p in ("", "."):
                continue
            if p == "..":
                if out:
                    out.pop()
                continue
            out.append(p)
        return "/".join(out)
    if h.startswith("/publicRecord/"):
        return h[len("/publicRecord/") :]
    if h.startswith("/"):
        return h.lstrip("/")
    return "path/parents/" + h


REWRITE = [
    ("https://defenddetroit.github.io/publicRecord", "/publicRecord"),
    ("http://defenddetroit.github.io/publicRecord", "/publicRecord"),
    ("https://detroit.primals.eco/css/", "/publicRecord/css/"),
    ("https://detroit.primals.eco/", "/publicRecord/"),
    ("https://detroit.primals.eco", "/publicRecord"),
]


def rewrite_bytes(data: bytes, rel: str) -> bytes:
    if not rel.endswith((".html", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".md")):
        return data
    try:
        s = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    for a, b in REWRITE:
        s = s.replace(a, b)
    s = re.sub(
        r"https?://(?:detroit\.primals\.eco|defenddetroit\.github\.io/publicRecord)/css/",
        "/publicRecord/css/",
        s,
    )
    return s.encode("utf-8")


def ensure_page(rel: str):
    """Copy from SRC if missing in GAIA/NEST. Return exists bool."""
    rel = rel.split("#")[0].split("?")[0]
    if not rel:
        return False
    if rel.endswith("/"):
        rel = rel + "index.html"
    elif not rel.endswith((".html", ".css", ".js", ".json", ".txt", ".svg", ".xml", ".md", ".png", ".jpg")):
        # likely a directory page
        if (SRC / rel / "index.html").exists():
            rel = rel.rstrip("/") + "/index.html"
        elif not (SRC / rel).exists():
            return False

    src = SRC / rel
    if not src.exists():
        # try index
        if (SRC / rel / "index.html").exists():
            rel = rel.rstrip("/") + "/index.html"
            src = SRC / rel
        else:
            print("MISSING SRC", rel)
            return False

    data = rewrite_bytes(src.read_bytes(), rel)
    for root in (GAIA, NEST):
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    print("DEEP", rel, len(data))
    return True


# Collect targets from parents + one more hop from each analysis page
targets = []
for h in hrefs:
    if h.startswith(("#", "mailto:", "javascript:")):
        continue
    rel = to_rel(h)
    if rel and not rel.startswith(("http", "data:")):
        targets.append(rel)

# Known deeper stack Rhonda/parents need
DEEPER = [
    "path/parents/index.html",
    "path/voters/index.html",
    "path/attorneys/index.html",
    "path/journalists/index.html",
    "path/index.html",
    "network/entities/purpose-charter-academy/index.html",
    "network/entities/macdowell/index.html",
    "network/entities/purpose-group-llc/index.html",
    "network/actors/brian-banks/index.html",
    "network/actors/joseph-holland-jr/index.html",
    "analysis/credential-audit/index.html",
    "analysis/funding-flow/index.html",
    "analysis/rico-pattern/index.html",
    "analysis/words-vs-numbers/index.html",
    "analysis/institutional-capture/index.html",
    "analysis/corporate-network-lara/index.html",
    "analysis/banks-holland-partnership/index.html",
    "analysis/damages-register/index.html",
    "analysis/education-landscape/index.html",
    "network/index.html",
    "network/judges/index.html",
    "timeline/index.html",
    "validate/index.html",
    "evidence/index.html",
    "courts/index.html",
    "connections/index.html",
    "about/index.html",
]
targets.extend(DEEPER)

# unique preserve order
seen = set()
uniq = []
for x in targets:
    x = x.replace("\\", "/").lstrip("/")
    if x not in seen:
        seen.add(x)
        uniq.append(x)

melted = []
for rel in uniq:
    if ensure_page(rel):
        melted.append(rel)

# second hop: from each melted html, pull more local links one level deeper
hop2 = []
for rel in list(melted):
    if not rel.endswith(".html"):
        continue
    fp = GAIA / rel
    if not fp.exists():
        continue
    html = fp.read_text(encoding="utf-8", errors="replace")
    for h in re.findall(r"""href=["']([^"']+)["']""", html):
        if h.startswith(("#", "mailto:", "javascript:", "http://", "https://")):
            # still convert absolute publicRecord
            if "publicRecord" in h or "detroit.primals.eco" in h or "defenddetroit" in h:
                r = to_rel(h)
                if r and r not in seen:
                    hop2.append(r)
            continue
        # relative from this page's dir
        base = str(Path(rel).parent).replace("\\", "/")
        if h.startswith("/publicRecord/"):
            r = h[len("/publicRecord/") :]
        elif h.startswith("/"):
            r = h.lstrip("/")
        elif h.startswith("../"):
            parts = (base + "/" + h).split("/")
            out = []
            for p in parts:
                if p in ("", "."):
                    continue
                if p == "..":
                    if out:
                        out.pop()
                    continue
                out.append(p)
            r = "/".join(out)
        else:
            r = (base + "/" + h).replace("//", "/")
        r = r.split("#")[0].split("?")[0]
        if r and r not in seen:
            hop2.append(r)

print("hop2 candidates", len(hop2))
for rel in hop2[:120]:
    rel = rel.replace("\\", "/").lstrip("/")
    if rel in seen:
        continue
    seen.add(rel)
    if ensure_page(rel):
        melted.append(rel)

# css
for name in ["main.css", "base.css", "hud.css"]:
    c = CONNECT_CSS / name
    if c.exists():
        for root in (GAIA, NEST):
            (root / "css").mkdir(exist_ok=True)
            shutil.copy2(c, root / "css" / name)

# DEEPER parents portal — Gaia overlay that drills into remade stack
DEEP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PARENTS — DEEPER — Canfield local stack</title>
<meta name="gaia-depth" content="parents-deep">
<style>
:root{--g:#3fb950;--gold:#d29922;--red:#f85149;--bg:#07090c;--fg:#e6edf3;--mut:#8b949e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--fg);font:14px/1.5 ui-monospace,Menlo,monospace}
header{padding:1rem 1.2rem;border-bottom:1px solid #21262d}
h1{color:var(--gold);font-size:1.35rem;letter-spacing:.06em}
.live{display:inline-block;border:1px solid var(--g);color:var(--g);padding:.1rem .4rem;font-size:.65rem;letter-spacing:.08em;margin-right:.3rem}
.mut{color:var(--mut);font-size:.85rem}
.grid{display:grid;grid-template-columns:1fr 1.4fr;min-height:70vh}
@media(max-width:900px){.grid{grid-template-columns:1fr}}
.rail{border-right:1px solid #21262d;padding:.8rem;overflow:auto;max-height:80vh}
.rail a{display:block;padding:.55rem .65rem;border:1px solid #21262d;margin:.35rem 0;color:var(--fg);text-decoration:none;font-size:.8rem}
.rail a:hover,.rail a.on{border-color:var(--g);color:var(--g)}
.rail .k{color:var(--gold);font-size:.68rem;letter-spacing:.06em}
.view{display:flex;flex-direction:column}
.view iframe{flex:1;width:100%;min-height:75vh;border:0;background:#fff}
.banner{margin:0;padding:.7rem 1rem;background:#140808;border-bottom:1px solid var(--red);font-size:.8rem}
.banner b{color:var(--red)}
.top{display:flex;flex-wrap:wrap;gap:.4rem;padding:.6rem 1rem;border-bottom:1px solid #21262d}
.top a{color:var(--g);font-size:.75rem}
</style>
</head>
<body>
<header>
  <p><span class="live">DEEPER</span><span class="live">PARENTS</span><span class="live">CANFIELD</span></p>
  <h1>For Parents — drill the stack</h1>
  <p class="mut">Not the surface card. Open each layer. MITO listens. Rhonda forever.</p>
</header>
<div class="banner"><b>$60M FALSE FACE</b> — go deeper: schools → money → credentials → RICO → validate. All remade in Gaia.</div>
<div class="top">
  <a href="/publicRecord/path/parents/" target="deepframe">original parents page</a>
  <a href="/mito">MITO</a>
  <a href="/canfield">train graph</a>
  <a href="/grow">GROW</a>
  <a href="/publicRecord/">PATH WALL</a>
</div>
<div class="grid">
  <nav class="rail" id="rail"></nav>
  <div class="view">
    <iframe name="deepframe" id="frame" src="/publicRecord/path/parents/" title="parents deep"></iframe>
  </div>
</div>
<script>
const LAYERS = [
  {k:'1 SURFACE', t:'Parents path', u:'/publicRecord/path/parents/'},
  {k:'2 SCHOOL', t:'Purpose Charter Academy', u:'/publicRecord/network/entities/purpose-charter-academy/'},
  {k:'2 SCHOOL', t:'MacDowell Preparatory', u:'/publicRecord/network/entities/macdowell/'},
  {k:'3 MONEY', t:'Funding flow', u:'/publicRecord/analysis/funding-flow/'},
  {k:'3 MONEY', t:'Words vs Numbers', u:'/publicRecord/analysis/words-vs-numbers/'},
  {k:'3 MONEY', t:'Purpose Group LLC', u:'/publicRecord/network/entities/purpose-group-llc/'},
  {k:'4 PEOPLE', t:'Brian Banks', u:'/publicRecord/network/actors/brian-banks/'},
  {k:'4 PEOPLE', t:'Joseph Holland Jr', u:'/publicRecord/network/actors/joseph-holland-jr/'},
  {k:'4 PEOPLE', t:'Banks–Holland partnership', u:'/publicRecord/analysis/banks-holland-partnership/'},
  {k:'5 KEYS', t:'Credential audit', u:'/publicRecord/analysis/credential-audit/'},
  {k:'6 PATTERN', t:'RICO pattern', u:'/publicRecord/analysis/rico-pattern/'},
  {k:'6 PATTERN', t:'Institutional capture', u:'/publicRecord/analysis/institutional-capture/'},
  {k:'7 LOCAL', t:'Voters path', u:'/publicRecord/path/voters/'},
  {k:'7 LOCAL', t:'Attorneys path', u:'/publicRecord/path/attorneys/'},
  {k:'7 LOCAL', t:'Journalists path', u:'/publicRecord/path/journalists/'},
  {k:'8 MESH', t:'Full network', u:'/publicRecord/network/'},
  {k:'8 MESH', t:'Judges', u:'/publicRecord/network/judges/'},
  {k:'8 MESH', t:'Timeline', u:'/publicRecord/timeline/'},
  {k:'9 PROOF', t:'Validate', u:'/publicRecord/validate/'},
  {k:'9 PROOF', t:'Evidence', u:'/publicRecord/evidence/'},
];
const rail=document.getElementById('rail');
const frame=document.getElementById('frame');
LAYERS.forEach((L,i)=>{
  const a=document.createElement('a');
  a.href=L.u; a.target='deepframe';
  a.innerHTML=`<div class="k">${L.k}</div>${L.t}`;
  a.onclick=()=>{ [...rail.querySelectorAll('a')].forEach(x=>x.classList.remove('on')); a.classList.add('on'); };
  if(i===0) a.classList.add('on');
  rail.appendChild(a);
});
</script>
</body>
</html>
"""

Path("/opt/gaia-api/static/parents-deep.html").write_text(DEEP_HTML, encoding="utf-8")
Path("/opt/connect/parents-deep.html").write_text(DEEP_HTML, encoding="utf-8")

# rewrite parents page links to /publicRecord/... and add DEEPER banner
t = parents.read_text(encoding="utf-8", errors="replace")
for a, b in REWRITE:
    t = t.replace(a, b)
# relative ../analysis → /publicRecord/analysis etc.
t = re.sub(r'href="\.\./\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/', r'href="/publicRecord/\1/', t)
t = re.sub(r"href='\.\./\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/", r"href='/publicRecord/\1/", t)
t = re.sub(r'href="\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/', r'href="/publicRecord/\1/', t)

if "parents-deep" not in t:
    banner = (
        '\n<div id="gaia-deeper" style="position:sticky;top:0;z-index:100000;background:#140808;'
        'border-bottom:2px solid #f85149;padding:10px 12px;font:13px/1.4 ui-monospace,Menlo,monospace;color:#e6edf3">'
        '<b style="color:#f85149">DEEPER</b> — surface is not enough · '
        '<a href="/parents-deep" style="color:#3fb950;font-weight:bold">OPEN DEEP STACK</a> · '
        '<a href="/publicRecord/analysis/funding-flow/" style="color:#58a6ff">money</a> · '
        '<a href="/publicRecord/analysis/credential-audit/" style="color:#58a6ff">creds</a> · '
        '<a href="/publicRecord/analysis/rico-pattern/" style="color:#58a6ff">RICO</a> · '
        '<a href="/mito" style="color:#f0883e">MITO</a>'
        "</div>\n"
    )
    if re.search(r"<body[^>]*>", t, re.I):
        t = re.sub(r"(<body[^>]*>)", r"\1" + banner, t, count=1, flags=re.I)
    # keep mito chip
parents.write_text(t, encoding="utf-8")
# mirror nest
(NEST / "path/parents/index.html").write_bytes(parents.read_bytes())

# routes
server = Path("/opt/gaia-api/server.js")
st = server.read_text(encoding="utf-8")
if "p === '/parents-deep'" not in st:
    needle = "if (p === '/grow'"
    block = r"""
    if (p === '/parents-deep' || p === '/deep' || p === '/parents/deep' || p === '/publicRecord/path/parents/deep') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/parents-deep.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Depth': 'parents-deep' });
        return res.end(html);
      } catch(e) { return J(res, { ok: false, error: 'parents-deep missing' }, 404); }
    }
"""
    idx = st.find(needle)
    if idx < 0:
        idx = st.find("if (p === '/mito'")
    if idx >= 0:
        st = st[:idx] + block + "\n    " + st[idx:]
        server.write_text(st, encoding="utf-8")
        print("parents-deep route in")
else:
    print("route ok")

meta = {
    "name": "PARENTS_DEEPER",
    "timestamp": TS,
    "melted": melted,
    "count": len(melted),
    "face": "https://gaia.primals.eco/parents-deep",
    "surface": "https://gaia.primals.eco/publicRecord/path/parents/",
}
Path("/opt/gaia-api/static/data/parents-deeper.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
print("DEEPER melted", len(melted))
print("DONE")
