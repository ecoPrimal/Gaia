#!/usr/bin/env python3
"""Fix Gaia self-walk melt + re-walk until she SEES."""
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

SITE_ROOTS = (
    "network", "analysis", "path", "validate", "timeline", "evidence", "courts",
    "connections", "about", "actors", "entities", "coverage", "sources", "contact",
    "legal", "open-letters", "books", "site-index", "docs", "api", "graph", "signal",
    "css", "js", "img", "favicon.svg", "llms.txt", "identity.json", "atom.xml",
    "braids.json", "weave.json", "sitemap.xml", "robots.txt",
)


def url_to_rel(url: str) -> str:
    path = url
    if path.startswith("/publicRecord"):
        path = path[len("/publicRecord"):]
    path = path.split("?")[0].split("#")[0]
    path = path.lstrip("/")
    if not path or path.endswith("/"):
        path = (path or "") + "index.html"
    elif "." not in Path(path).name:
        path = path + "/index.html"
    return path


def find_src(rel: str) -> Path | None:
    candidates = [
        SRC / rel,
        SRC / rel.replace("index.html", "") / "index.html" if rel.endswith("index.html") else None,
    ]
    # also try without network/ prefix duplicates (actors vs network/actors)
    if rel.startswith("network/actors/"):
        candidates.append(SRC / rel.replace("network/actors/", "actors/", 1))
    if rel.startswith("network/entities/"):
        candidates.append(SRC / rel.replace("network/entities/", "entities/", 1))
    if rel.startswith("actors/"):
        candidates.append(SRC / ("network/" + rel))
    if rel.startswith("entities/"):
        candidates.append(SRC / ("network/" + rel))
    for c in candidates:
        if c and c.is_file():
            return c
        if c and c.is_dir() and (c / "index.html").is_file():
            return c / "index.html"
    # fuzzy: search by last two segments
    parts = Path(rel).parts
    if len(parts) >= 2:
        leaf = parts[-2] if parts[-1] == "index.html" else parts[-1]
        for hit in SRC.rglob(leaf):
            if hit.is_dir() and (hit / "index.html").exists():
                return hit / "index.html"
            if hit.name == "index.html" and hit.parent.name == leaf:
                return hit
    return None


def melt_url(url: str) -> tuple[bool, str]:
    rel = url_to_rel(url)
    src = find_src(rel)
    if not src:
        return False, rel
    # destination rel under GAIA prefers the URL path structure
    dest_rel = rel
    data = src.read_bytes()
    if dest_rel.endswith((".html", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".md")):
        s = data.decode("utf-8", errors="replace")
        s = s.replace("https://defenddetroit.github.io/publicRecord", "/publicRecord")
        s = s.replace("https://detroit.primals.eco", "/publicRecord")
        s = s.replace("http://detroit.primals.eco", "/publicRecord")
        s = re.sub(
            r"href=/(?!publicRecord/)(" + "|".join(SITE_ROOTS) + r")(/[^>\s\"']*)",
            r"href=/publicRecord/\1\2",
            s,
        )
        data = s.encode("utf-8")
    for root in (GAIA, NEST):
        dest = root / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return True, dest_rel


def normalize_href(href: str, page_url: str):
    if not href or href.startswith(("#", "mailto:", "javascript:", "data:", "tel:")):
        return None
    if href.startswith(("http://", "https://")):
        u = urlparse(href)
        if u.netloc not in (
            "127.0.0.1:9876",
            "gaia.primals.eco",
            "nestgate.io",
            "detroit.primals.eco",
            "defenddetroit.github.io",
        ):
            return None
        path = u.path or "/"
        if "/publicRecord" in path:
            path = path[path.find("/publicRecord") :]
        elif u.netloc == "detroit.primals.eco":
            path = "/publicRecord" + (path if path.startswith("/") else "/" + path)
        href = path
    if href.startswith("/") and not href.startswith("/publicRecord"):
        first = href.strip("/").split("/", 1)[0]
        if first in SITE_ROOTS:
            href = "/publicRecord" + href
        else:
            return None
    if href.startswith("/publicRecord"):
        # normalize trailing
        if not href.endswith("/") and "." not in Path(href).name:
            href = href + "/"
        return href
    full = urljoin(page_url, href)
    path = urlparse(full).path or "/"
    if path.startswith("/publicRecord"):
        if not path.endswith("/") and "." not in Path(path).name:
            path = path + "/"
        return path
    return None


# Load prior broken list and melt them
prior = {}
pj = DATA / "gaia-self-walk.json"
if pj.exists():
    prior = json.loads(pj.read_text(encoding="utf-8"))

melted = []
still_missing = []
for b in (prior.get("broken") or []) + [{"url": x} for x in (prior.get("queue_remaining") or [])]:
    url = b.get("url") if isinstance(b, dict) else b
    if not url or not str(url).startswith("/publicRecord"):
        continue
    ok, rel = melt_url(url)
    if ok:
        melted.append({"url": url, "rel": rel})
    else:
        still_missing.append(url)

print("melted from prior broken", len(melted), "still missing", len(still_missing))

# Fresh walk from parents — she SEES
start = "/publicRecord/path/parents/"
queue = deque([start, "/publicRecord/", "/publicRecord/path/", "/publicRecord/network/", "/publicRecord/analysis/"])
seen = set()
pages = []
broken = []
rewrote = 0
max_pages = 400

while queue and len(seen) < max_pages:
    url = queue.popleft()
    if url in seen:
        continue
    seen.add(url)
    if not url.startswith("/publicRecord"):
        continue

    rel = url_to_rel(url)
    fp = GAIA / rel
    if not fp.exists():
        ok, rel2 = melt_url(url)
        if ok:
            melted.append({"url": url, "rel": rel2})
            fp = GAIA / rel2
        else:
            broken.append({"url": url, "error": "cannot_melt"})
            continue

    if fp.suffix != ".html":
        continue

    s = fp.read_text(encoding="utf-8", errors="replace")
    s2 = s
    s2 = s2.replace("https://defenddetroit.github.io/publicRecord", "/publicRecord")
    s2 = s2.replace("https://detroit.primals.eco", "/publicRecord")
    before = s2
    s2 = re.sub(
        r"href=/(?!publicRecord/)(" + "|".join(SITE_ROOTS) + r")(/[^>\s\"']*)",
        r"href=/publicRecord/\1\2",
        s2,
    )
    if s2 != before:
        rewrote += 1
        fp.write_text(s2, encoding="utf-8")
        nest = NEST / rel
        nest.parent.mkdir(parents=True, exist_ok=True)
        nest.write_text(s2, encoding="utf-8")

    title_m = re.search(r"<title[^>]*>(.*?)</title>", s2, re.I | re.S)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else rel
    page_url = "http://127.0.0.1:9876" + url
    hrefs = re.findall(r"""href\s*=\s*["']?([^"'\s>]+)["']?""", s2, flags=re.I)
    outs = []
    for h in hrefs:
        n = normalize_href(h, page_url)
        if n and n.startswith("/publicRecord"):
            outs.append(n)
            if n not in seen:
                queue.append(n)

    pages.append(
        {
            "url": url,
            "title": title[:140],
            "bytes": len(s2.encode("utf-8")),
            "links_out": len(outs),
            "status": "seen",
        }
    )

# HTTP verify sample of what she walked
http_ok = 0
http_bad = []
for p in pages[:100]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:9876" + p["url"]],
        capture_output=True,
        text=True,
    )
    code = rr.stdout.strip()
    p["http"] = code
    if code == "200":
        http_ok += 1
    else:
        http_bad.append({"url": p["url"], "http": code})

report = {
    "name": "GAIA_SELF_WALK",
    "organ": "webdev",
    "timestamp": TS,
    "axiom": "Not a soft fix. She self-walks. She sees. She melts. She DEVs her own web.",
    "start": start,
    "walked_urls": len(seen),
    "pages_seen": len(pages),
    "melted": len(melted),
    "melted_sample": melted[:40],
    "rewrote_pages": rewrote,
    "broken": broken[:80],
    "broken_count": len(broken),
    "still_missing_from_prior": still_missing[:40],
    "http_ok": http_ok,
    "http_checked": min(100, len(pages)),
    "http_bad": http_bad[:30],
    "seen_sample": pages[:80],
}

(DATA / "gaia-self-walk.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
Path("/opt/connect/data/gaia-self-walk.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

# refresh self-walk face
WALK = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GAIA SELF-WALK — her own web DEV</title>
<style>
body{{margin:0;background:#050505;color:#e6edf3;font:14px/1.5 ui-monospace,Menlo,monospace;padding:1.25rem;max-width:52rem}}
h1{{color:#58a6ff}} .live{{border:1px solid #58a6ff;color:#58a6ff;padding:.1rem .4rem;font-size:.65rem;margin-right:.25rem;display:inline-block}}
.ok{{color:#3fb950}} .bad{{color:#f85149}} a{{color:#3fb950}} .mut{{color:#8b949e;font-size:.8rem}}
.box{{border:1px solid #30363d;padding:1rem;margin:1rem 0}} .row{{border-bottom:1px solid #161b22;padding:.4rem 0}}
</style></head><body>
<p><span class="live">SELF-WALK</span><span class="live">WEB DEV</span><span class="live">SHE SEES</span></p>
<h1>Gaia walks her own web</h1>
<p class="mut">Not our soft fix. She crawls, melts missing pores, rewrites, HTTP-sees.</p>
<div class="box">
<p>Pages she saw: <b class="ok">{len(pages)}</b> · Melted: <b>{len(melted)}</b> · Rewrote: <b>{rewrote}</b></p>
<p>HTTP OK: <b class="ok">{http_ok}/{min(100,len(pages))}</b> · Broken: <b class="{'bad' if broken else 'ok'}">{len(broken)}</b></p>
<p><a href="/publicRecord/path/parents/">parents</a> · <a href="/parents-deep">deep</a> · <a href="/data/gaia-self-walk.json">JSON</a> · <a href="/mito">MITO</a></p>
</div>
<h2 style="color:#58a6ff;font-size:.85rem">SHE SAW</h2>
<div id="saw"></div>
<script>
fetch('/data/gaia-self-walk.json').then(r=>r.json()).then(W=>{{
  const el=document.getElementById('saw');
  (W.seen_sample||[]).forEach(p=>{{
    const d=document.createElement('div'); d.className='row';
    const st=(p.http==='200'||!p.http)?'ok':'bad';
    d.innerHTML=`<span class="${{st}}">${{p.http||'seen'}}</span> <a href="${{p.url}}">${{p.title||p.url}}</a>
      <div class="mut">${{p.url}} · ${{p.bytes||0}}b · out ${{p.links_out||0}}</div>`;
    el.appendChild(d);
  }});
}});
</script>
</body></html>
"""
Path("/opt/gaia-api/static/self-walk.html").write_text(WALK, encoding="utf-8")
Path("/opt/connect/self-walk.html").write_text(WALK, encoding="utf-8")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
print("pages", len(pages), "melted", len(melted), "broken", len(broken), "http_ok", http_ok)
print("DONE")
