#!/usr/bin/env python3
"""GAIA SELF-WALK — her own web DEV. She crawls, sees, melts, rewrites. Not a soft fix."""
import hashlib
import json
import re
import subprocess
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

TS = datetime.now(timezone.utc).isoformat()
SRC = Path("/opt/publicRecord/site/public")
GAIA = Path("/opt/gaia-api/static/publicRecord")
NEST = Path("/opt/connect/publicRecord")
DATA = Path("/opt/gaia-api/static/data")
BASE = "http://127.0.0.1:9876/publicRecord/"

SITE_ROOTS = (
    "network",
    "analysis",
    "path",
    "validate",
    "timeline",
    "evidence",
    "courts",
    "connections",
    "about",
    "actors",
    "entities",
    "coverage",
    "sources",
    "contact",
    "legal",
    "open-letters",
    "books",
    "site-index",
    "docs",
    "api",
    "graph",
    "signal",
    "css",
    "js",
    "img",
)


def normalize_href(href: str, page_url: str) -> str | None:
    if not href or href.startswith(("#", "mailto:", "javascript:", "data:", "tel:")):
        return None
    if href.startswith(("http://", "https://")):
        u = urlparse(href)
        if u.netloc in (
            "127.0.0.1:9876",
            "gaia.primals.eco",
            "nestgate.io",
            "detroit.primals.eco",
            "defenddetroit.github.io",
        ):
            path = u.path or "/"
            if "publicRecord" in path:
                i = path.find("/publicRecord")
                path = path[i + len("/publicRecord") :] or "/"
            elif u.netloc == "defenddetroit.github.io" and path.startswith("/publicRecord"):
                path = path[len("/publicRecord") :] or "/"
            href = path
        else:
            return None  # external — she sees but does not own
    # root-relative site paths
    if href.startswith("/") and not href.startswith("/publicRecord"):
        first = href.strip("/").split("/", 1)[0]
        if first in SITE_ROOTS:
            href = "/publicRecord" + href
        elif href.startswith(("/mito", "/grow", "/canfield", "/cash4kids", "/parents-deep", "/@", "/C")):
            return href  # gaia organs
        else:
            return None
    if href.startswith("/publicRecord"):
        return href
    # relative
    full = urljoin(page_url, href)
    u = urlparse(full)
    path = u.path or "/"
    if path.startswith("/publicRecord"):
        return path
    return None


def path_to_file(url_path: str) -> Path | None:
    """Map /publicRecord/foo/ → GAIA/foo/index.html"""
    if not url_path.startswith("/publicRecord"):
        return None
    rel = url_path[len("/publicRecord") :].lstrip("/")
    if not rel:
        return GAIA / "index.html"
    if rel.endswith("/"):
        rel = rel + "index.html"
    elif "." not in Path(rel).name:
        rel = rel.rstrip("/") + "/index.html"
    return GAIA / rel


def src_file(rel: str) -> Path | None:
    p = SRC / rel
    if p.exists():
        return p
    if (SRC / rel / "index.html").exists():
        return SRC / rel / "index.html"
    return None


def melt_rel(rel: str) -> bool:
    src = src_file(rel)
    if not src:
        return False
    if src.is_dir():
        src = src / "index.html"
        if not src.exists():
            return False
        rel = str(src.relative_to(SRC)).replace("\\", "/")
    data = src.read_bytes()
    if rel.endswith((".html", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".md")):
        s = data.decode("utf-8", errors="replace")
        s = s.replace("https://defenddetroit.github.io/publicRecord", "/publicRecord")
        s = s.replace("https://detroit.primals.eco", "/publicRecord")
        s = s.replace("http://detroit.primals.eco", "/publicRecord")
        s = re.sub(
            r"href=/(?!" + "publicRecord/)(" + "|".join(SITE_ROOTS) + r")(/[^>\s\"']*)",
            r"href=/publicRecord/\1\2",
            s,
        )
        data = s.encode("utf-8")
    for root in (GAIA, NEST):
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return True


def extract_links(html: str, page_url: str):
    hrefs = re.findall(r"""href\s*=\s*["']?([^"'\s>]+)["']?""", html, flags=re.I)
    out = []
    for h in hrefs:
        n = normalize_href(h, page_url)
        if n:
            out.append(n)
    return out


# ── SELF WALK ──
start = "/publicRecord/path/parents/"
queue = deque([start, "/publicRecord/", "/publicRecord/path/", "/parents-deep"])
seen = set()
seen_pages = []
broken = []
external_seen = []
melted = []
rewrote = 0
max_pages = 250

print("GAIA SELF-WALK begin", start)

while queue and len(seen) < max_pages:
    url = queue.popleft()
    if url in seen:
        continue
    seen.add(url)

    # organ pages
    if url in ("/parents-deep", "/mito", "/grow", "/canfield", "/cash4kids", "/@", "/C"):
        # still record
        seen_pages.append({"url": url, "kind": "organ", "status": "organ"})
        continue

    fp = path_to_file(url)
    if fp is None:
        continue

    rel = str(fp.relative_to(GAIA)).replace("\\", "/") if fp.exists() or True else None
    # try melt if missing
    if not fp.exists():
        guess = url[len("/publicRecord") :].lstrip("/")
        if guess.endswith("/"):
            guess = guess + "index.html"
        elif "." not in Path(guess).name:
            guess = guess.rstrip("/") + "/index.html"
        if melt_rel(guess):
            melted.append(guess)
            fp = GAIA / guess
        else:
            broken.append({"url": url, "error": "missing_after_melt"})
            continue

    if not fp.exists():
        broken.append({"url": url, "error": "missing"})
        continue

    raw = fp.read_bytes()
    # rewrite in place as she walks (her web DEV)
    if fp.suffix == ".html":
        s = raw.decode("utf-8", errors="replace")
        s2 = s.replace("https://defenddetroit.github.io/publicRecord", "/publicRecord")
        s2 = s2.replace("https://detroit.primals.eco", "/publicRecord")
        before = s2
        s2 = re.sub(
            r"href=/(?!" + "publicRecord/)(" + "|".join(SITE_ROOTS) + r")(/[^>\s\"']*)",
            r"href=/publicRecord/\1\2",
            s2,
        )
        s2 = re.sub(
            r"""href=(["'])/(?!publicRecord/)(""" + "|".join(SITE_ROOTS) + r""")(/[^"']*)\1""",
            r"href=\1/publicRecord/\2\3\1",
            s2,
        )
        if s2 != before:
            rewrote += 1
            fp.write_text(s2, encoding="utf-8")
            nest_fp = NEST / fp.relative_to(GAIA)
            nest_fp.parent.mkdir(parents=True, exist_ok=True)
            nest_fp.write_text(s2, encoding="utf-8")
        html = s2
        title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else rel
        page_url = "http://127.0.0.1:9876" + url
        links = extract_links(html, page_url)
        for L in links:
            if L.startswith("/publicRecord") and L not in seen:
                queue.append(L)
            elif L.startswith("http"):
                external_seen.append(L)
        seen_pages.append(
            {
                "url": url,
                "title": title[:120],
                "bytes": len(html.encode("utf-8")),
                "sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
                "links_out": len(links),
                "kind": "page",
                "status": "seen",
            }
        )
    else:
        seen_pages.append({"url": url, "kind": "asset", "bytes": len(raw), "status": "seen"})

# HTTP SEE — she curls herself
http_seen = []
for page in seen_pages[:80]:
    if page.get("kind") != "page":
        continue
    u = "http://127.0.0.1:9876" + page["url"]
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", u],
        capture_output=True,
        text=True,
    )
    code = rr.stdout.strip()
    http_seen.append({"url": page["url"], "http": code})
    if code != "200":
        broken.append({"url": page["url"], "error": f"http_{code}"})

report = {
    "name": "GAIA_SELF_WALK",
    "organ": "webdev",
    "timestamp": TS,
    "axiom": "Not a soft fix. She self-walks. She sees. She DEVs her own web.",
    "start": start,
    "walked": len(seen),
    "pages_seen": len([p for p in seen_pages if p.get("kind") == "page"]),
    "melted_on_walk": melted,
    "rewrote_pages": rewrote,
    "broken": broken[:100],
    "broken_count": len(broken),
    "http_sample": http_seen[:40],
    "seen_sample": seen_pages[:60],
    "queue_remaining": list(queue)[:40],
}

DATA.mkdir(parents=True, exist_ok=True)
(DATA / "gaia-self-walk.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
Path("/opt/connect/data/gaia-self-walk.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

# SELF-WALK face
ok_http = sum(1 for h in http_seen if h["http"] == "200")
WALK_HTML = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GAIA SELF-WALK — her own web DEV</title>
<style>
body{{margin:0;background:#050505;color:#e6edf3;font:14px/1.5 ui-monospace,Menlo,monospace;padding:1.25rem;max-width:48rem}}
h1{{color:#58a6ff;letter-spacing:.08em}}
.live{{border:1px solid #58a6ff;color:#58a6ff;padding:.1rem .45rem;font-size:.65rem;margin-right:.3rem;display:inline-block}}
.ok{{color:#3fb950}}.bad{{color:#f85149}}
.row{{border-bottom:1px solid #161b22;padding:.45rem 0}}
a{{color:#3fb950}}
.mut{{color:#8b949e;font-size:.8rem}}
.box{{border:1px solid #30363d;padding:1rem;margin:1rem 0}}
</style></head><body>
<p><span class="live">SELF-WALK</span><span class="live">WEB DEV</span><span class="live">NOT SOFT FIX</span></p>
<h1>She walks her own web</h1>
<p class="mut">Gaia crawls /publicRecord, sees pages, melts missing, rewrites links. Her DEV — not ours.</p>
<div class="box">
  <p>Walked <b>{len(seen)}</b> · Pages seen <b class="ok">{len([p for p in seen_pages if p.get('kind')=='page'])}</b></p>
  <p>Rewrote <b>{rewrote}</b> · Melted on walk <b>{len(melted)}</b> · Broken <b class="{'ok' if not broken else 'bad'}">{len(broken)}</b></p>
  <p>HTTP sample OK <b class="ok">{ok_http}/{len(http_seen)}</b></p>
  <p><a href="/publicRecord/path/parents/">parents</a> · <a href="/parents-deep">deep stack</a> · <a href="/data/gaia-self-walk.json">walk JSON</a> · <a href="/mito">MITO</a></p>
</div>
<h2 style="color:#58a6ff;font-size:.85rem;letter-spacing:.1em">SHE SAW</h2>
<div id="saw"></div>
<script>
fetch('/data/gaia-self-walk.json').then(r=>r.json()).then(W=>{{
  const el=document.getElementById('saw');
  (W.seen_sample||[]).filter(x=>x.kind==='page').forEach(p=>{{
    const d=document.createElement('div'); d.className='row';
    d.innerHTML=`<a href="${{p.url}}">${{p.title||p.url}}</a><div class="mut">${{p.url}} · ${{p.bytes||0}}b · links ${{p.links_out||0}}</div>`;
    el.appendChild(d);
  }});
}});
</script>
</body></html>
"""
Path("/opt/gaia-api/static/self-walk.html").write_text(WALK_HTML, encoding="utf-8")
Path("/opt/connect/self-walk.html").write_text(WALK_HTML, encoding="utf-8")

# routes
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/self-walk'" not in t:
    needle = "if (p === '/parents-deep'"
    block = r"""
    if (p === '/self-walk' || p === '/walk' || p === '/webdev' || p === '/she-walks') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/self-walk.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-WebDev': 'self-walk' });
        return res.end(html);
      } catch(e) { return J(res, { ok: false, error: 'self-walk missing' }, 404); }
    }
    if (p === '/data/gaia-self-walk.json' || p === '/self-walk.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/gaia-self-walk.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-WebDev': 'self-walk' });
        return res.end(raw);
      } catch(e) { return J(res, { ok: false }, 404); }
    }
"""
    idx = t.find(needle)
    if idx < 0:
        idx = t.find("if (p === '/grow'")
    if idx >= 0:
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("self-walk routes in")
else:
    print("routes ok")

# chip on parents — she walks
parents = GAIA / "path/parents/index.html"
if parents.exists():
    s = parents.read_text(encoding="utf-8", errors="replace")
    if "self-walk" not in s:
        s = s.replace(
            'OPEN DEEP STACK</a>',
            'OPEN DEEP STACK</a> · <a href="/self-walk" style="color:#58a6ff;font-weight:bold">SHE WALKS</a>',
            1,
        )
        parents.write_text(s, encoding="utf-8")
        (NEST / "path/parents/index.html").write_text(s, encoding="utf-8")
        print("parents chip → SHE WALKS")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/self-walk",
    "http://127.0.0.1:9876/walk",
    "http://127.0.0.1:9876/data/gaia-self-walk.json",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)

print(
    "WALKED",
    len(seen),
    "REWROTE",
    rewrote,
    "MELTED",
    len(melted),
    "BROKEN",
    len(broken),
)
print("DONE")
