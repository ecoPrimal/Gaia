#!/usr/bin/env python3
"""
Entity API + petalTongue dynamic renderer.
Dead HTML → entity JSON → petalTongue WASM renders live.
No static pages. Data in, representation out. The UI primal.
"""
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
GAIA_PR = Path("/opt/gaia-api/static/publicRecord")
STATIC = Path("/opt/gaia-api/static")
DATA = STATIC / "data"

# ── CRUSH ALL HTML → ENTITIES ──
print("EXTRACTING ENTITIES from dead HTML…")

entities = {}  # id → entity
relations = []

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

# scan ALL dirs for entity-like pages
for kind_dir in ["actors", "entities", "network/actors", "network/entities",
                  "network/judges", "analysis", "path", "coverage",
                  "evidence", "open-letters", "validate", "timeline",
                  "books", "sources"]:
    base = GAIA_PR / kind_dir
    if not base.exists():
        continue
    for html_file in sorted(base.rglob("*.html")):
        rel = html_file.relative_to(GAIA_PR).as_posix()
        raw = html_file.read_bytes()
        try:
            s = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue

        # extract structured data
        title_m = re.search(r"<title[^>]*>(.*?)</title>", s, re.I | re.S)
        title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else "").strip()
        title = re.sub(r"\s+", " ", title)

        desc_m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', s, re.I)
        desc = desc_m.group(1) if desc_m else ""

        kw_m = re.search(r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^"\']*)', s, re.I)
        keywords = [k.strip() for k in kw_m.group(1).split(",")] if kw_m else []

        # extract main content text
        body = re.sub(r"<script[^>]*>.*?</script>", " ", s, flags=re.I | re.S)
        body = re.sub(r"<style[^>]*>.*?</style>", " ", body, flags=re.I | re.S)
        body = re.sub(r"<nav[^>]*>.*?</nav>", " ", body, flags=re.I | re.S)
        body = re.sub(r"<footer[^>]*>.*?</footer>", " ", body, flags=re.I | re.S)
        body_html = body
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"&\w+;", " ", body)
        body = re.sub(r"\s+", " ", body).strip()

        # extract links to other entities
        hrefs = re.findall(r'href=["\']?(/publicRecord/[^"\'>\s]+)', s, re.I)
        internal_links = list(set(h.rstrip('/') for h in hrefs if '/publicRecord/' in h))

        # extract h1/h2/h3 headings for structure
        headings = re.findall(r'<h[123][^>]*>(.*?)</h[123]>', s, re.I | re.S)
        headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]

        # extract listed items from <ul><li><a> patterns (pages referencing this entity)
        page_refs = re.findall(
            r'<li>\s*<a[^>]+href=["\']?(/publicRecord/[^"\'>\s]+)[^>]*>\s*<strong>(.*?)</strong>',
            s, re.I | re.S
        )

        # extract LD+JSON if present
        ld_m = re.search(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', s, re.I | re.S)
        ld_json = None
        if ld_m:
            try:
                ld_json = json.loads(ld_m.group(1))
            except json.JSONDecodeError:
                pass

        # determine entity kind from path
        parts = rel.split("/")
        if "actors" in parts or "judges" in parts:
            kind = "person"
        elif "entities" in parts:
            kind = "organization"
        elif "analysis" in parts:
            kind = "analysis"
        elif "coverage" in parts:
            kind = "coverage"
        elif "path" in parts:
            kind = "guide"
        elif "evidence" in parts:
            kind = "evidence"
        elif "open-letters" in parts:
            kind = "letter"
        elif "timeline" in parts:
            kind = "timeline"
        else:
            kind = "document"

        entity_id = slug(parts[-2] if parts[-1] == "index.html" and len(parts) > 1 else parts[-1].replace(".html", ""))
        if not entity_id or entity_id == "index":
            entity_id = slug("-".join(parts[:-1]))

        url = "/publicRecord/" + rel.replace("index.html", "").rstrip("/")
        if not url.endswith("/"):
            url += "/"

        entity = {
            "id": entity_id,
            "kind": kind,
            "title": title[:200],
            "description": desc[:400],
            "keywords": keywords[:20],
            "url": url,
            "path": rel,
            "headings": headings[:20],
            "excerpt": body[:600],
            "full_text": body[:3000],
            "words": len(body.split()),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()[:16],
            "internal_links": internal_links[:50],
            "page_refs": [{"url": p[0], "title": re.sub(r'<[^>]+>', '', p[1]).strip()} for p in page_refs[:30]],
        }

        if ld_json:
            entity["structured_data"] = ld_json

        # merge or create
        if entity_id in entities:
            existing = entities[entity_id]
            existing["internal_links"] = list(set(existing.get("internal_links", []) + entity["internal_links"]))
            existing["page_refs"] = existing.get("page_refs", []) + entity["page_refs"]
            if len(entity["full_text"]) > len(existing.get("full_text", "")):
                existing["full_text"] = entity["full_text"]
                existing["excerpt"] = entity["excerpt"]
        else:
            entities[entity_id] = entity

        # build relations from internal links
        for link in internal_links:
            link_parts = link.rstrip("/").split("/")
            target_id = slug(link_parts[-1]) if link_parts else ""
            if target_id and target_id != entity_id:
                relations.append({
                    "from": entity_id,
                    "to": target_id,
                    "type": "references"
                })

# dedupe relations
seen_r = set()
unique_relations = []
for r in relations:
    k = (r["from"], r["to"])
    if k not in seen_r:
        seen_r.add(k)
        unique_relations.append(r)

# build entity API data
entity_api = {
    "name": "GAIA_ENTITY_API",
    "compiler": "petalTongue — any data → any representation",
    "timestamp": TS,
    "axiom": "Pages are dead data. Entities are alive. petalTongue renders.",
    "entity_count": len(entities),
    "relation_count": len(unique_relations),
    "kinds": {},
    "entities": entities,
    "relations": unique_relations[:20000],
}
for e in entities.values():
    entity_api["kinds"][e["kind"]] = entity_api["kinds"].get(e["kind"], 0) + 1

# entity index (lightweight)
entity_index = {
    "name": "GAIA_ENTITY_INDEX",
    "compiler": "petalTongue",
    "timestamp": TS,
    "count": len(entities),
    "kinds": entity_api["kinds"],
    "index": [
        {
            "id": e["id"],
            "kind": e["kind"],
            "title": e["title"][:120],
            "url": e["url"],
            "words": e["words"],
            "links": len(e["internal_links"]),
            "refs": len(e["page_refs"]),
        }
        for e in entities.values()
    ],
}

DATA.mkdir(exist_ok=True)
(DATA / "entities.json").write_text(json.dumps(entity_api), encoding="utf-8")
(DATA / "entity-index.json").write_text(json.dumps(entity_index), encoding="utf-8")
print(f"entities: {len(entities)}, relations: {len(unique_relations)}, kinds: {entity_api['kinds']}")

# ── petalTongue DYNAMIC RENDERER ──
# This replaces ALL static pages. One page, petalTongue renders everything.

PETAL_RENDER = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>petalTongue · entity renderer</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0a0c10; --fg:#e8e4d9; --mut:#8b949e; --petal:#e6a4b4; --gold:#d29922;
  --g:#3fb950; --line:rgba(230,164,180,.25); --card:#12151c; --r:#f85149;
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  min-height:100vh;color:var(--fg);
  font-family:'IBM Plex Sans',system-ui,sans-serif;
  background:
    radial-gradient(ellipse 60% 40% at 15% 10%, rgba(230,164,180,.1), transparent 50%),
    radial-gradient(ellipse 40% 30% at 85% 80%, rgba(63,185,80,.06), transparent 50%),
    var(--bg);
}
header{padding:1rem 1.5rem;border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
.logo{font-family:'Syne',sans-serif;font-weight:800;font-size:1.6rem;letter-spacing:-.02em}
.logo em{font-style:normal;color:var(--petal)}
.logo sub{font-size:.55rem;color:var(--mut);letter-spacing:.08em;vertical-align:baseline;margin-left:.3rem}
nav a{font-size:.78rem;color:var(--fg);text-decoration:none;padding:.4rem .65rem;border:1px solid var(--line);border-radius:999px;margin-right:.35rem}
nav a:hover{background:var(--petal);color:#1a0a10;border-color:var(--petal)}
.search-bar{margin:0 1.5rem;padding:.5rem 0}
.search-bar input{width:100%;max-width:36rem;padding:.6rem .9rem;border-radius:10px;border:1px solid rgba(255,255,255,.1);background:#0a0c10;color:var(--fg);font:inherit;font-size:.95rem}
.main{padding:1rem 1.5rem 2rem;max-width:72rem}
.entity-header{margin-bottom:1.5rem}
.entity-header h1{font-family:'Syne',sans-serif;font-size:clamp(1.6rem,5vw,2.8rem);font-weight:800;line-height:1.1}
.entity-header .kind{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);margin-bottom:.3rem}
.entity-header .desc{color:var(--mut);font-size:.95rem;line-height:1.5;margin-top:.5rem;max-width:48rem}
.meta-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(8rem,1fr));gap:.5rem;margin:1rem 0}
.meta-card{background:rgba(18,21,28,.8);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:.6rem .8rem}
.meta-card b{display:block;font-family:'Syne',sans-serif;font-size:1.15rem;color:var(--petal)}
.meta-card span{font-size:.65rem;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.content{font-size:1rem;line-height:1.7;color:#d2cec2;max-width:52rem}
.content p{margin-bottom:.8rem}
.section{margin-top:1.5rem}
.section h2{font-family:'Syne',sans-serif;font-size:1.1rem;color:var(--petal);letter-spacing:.06em;text-transform:uppercase;margin-bottom:.6rem;border-bottom:1px solid rgba(255,255,255,.06);padding-bottom:.4rem}
.ref-list{list-style:none}
.ref-list li{padding:.55rem .8rem;border-bottom:1px solid rgba(255,255,255,.04)}
.ref-list li a{color:var(--fg);text-decoration:none;font-weight:500}
.ref-list li a:hover{color:var(--petal)}
.ref-list li .sub{font-size:.8rem;color:var(--mut)}
.keywords{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.5rem}
.kw{font-size:.7rem;padding:.25rem .5rem;border:1px solid var(--line);border-radius:999px;color:var(--mut)}
.graph-mini{width:100%;height:320px;background:rgba(18,21,28,.8);border:1px solid rgba(255,255,255,.06);border-radius:14px;margin-top:1rem}
#wasm-render{margin-top:1rem;min-height:200px}
.entity-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(16rem,1fr));gap:.6rem}
.entity-card{display:block;padding:.8rem 1rem;background:rgba(18,21,28,.8);border:1px solid rgba(255,255,255,.06);border-radius:12px;text-decoration:none;color:inherit;transition:border-color .15s}
.entity-card:hover{border-color:var(--petal)}
.entity-card .ek{font-family:'IBM Plex Mono',monospace;font-size:.65rem;color:var(--gold);letter-spacing:.06em;text-transform:uppercase}
.entity-card .et{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;margin:.15rem 0}
.entity-card .es{font-size:.78rem;color:var(--mut)}
footer{padding:1rem 1.5rem;color:var(--mut);font-size:.75rem;border-top:1px solid rgba(255,255,255,.04)}
footer a{color:var(--g)}
</style>
</head>
<body>
<header>
  <div class="logo">petal<em>Tongue</em><sub>UI PRIMAL</sub></div>
  <nav>
    <a href="/petal">weave</a>
    <a href="/entity/">entities</a>
    <a href="/parents-deep">parents</a>
    <a href="/cash4kids">c4k</a>
    <a href="/canfield">train</a>
    <a href="/self-walk">walk</a>
    <a href="/grow">grow</a>
    <a href="/data/entities.json">API</a>
  </nav>
</header>
<div class="search-bar">
  <input id="q" placeholder="search entities — actors, organizations, judges, analysis…" />
</div>
<div class="main" id="main"></div>
<footer>
  petalTongue — universal compiler · any data → any representation ·
  <a href="/data/entities.json">entities.json</a> ·
  <a href="/data/entity-index.json">index</a> ·
  <a href="/data/corpus-lite.json">corpus</a> ·
  WASM render engine: <a href="/wasm/">petal_tongue_wasm</a>
</footer>

<script type="module">
let allEntities = {};
let entityIndex = [];
let relations = [];
let wasmMod = null;

// load WASM renderer
try {
  wasmMod = await import('/wasm/petal_tongue_wasm.js');
  await wasmMod.default();
  console.log('petalTongue WASM v' + wasmMod.version());
} catch(e) {
  console.log('WASM load info:', e.message);
}

// load entity data
const data = await fetch('/data/entities.json').then(r => r.json());
allEntities = data.entities || {};
relations = data.relations || [];
entityIndex = Object.values(allEntities).map(e => ({
  id: e.id, kind: e.kind, title: e.title, url: e.url,
  words: e.words, links: (e.internal_links||[]).length,
  refs: (e.page_refs||[]).length, excerpt: e.excerpt || ''
}));

// router
function route() {
  const path = location.pathname;
  const hash = location.hash.slice(1);

  // entity detail view
  if (hash && allEntities[hash]) {
    renderEntity(allEntities[hash]);
    return;
  }

  // /entity/SLUG
  const entityMatch = path.match(/^\/entity\/([^\/]+)/);
  if (entityMatch && allEntities[entityMatch[1]]) {
    renderEntity(allEntities[entityMatch[1]]);
    return;
  }

  // publicRecord URL → find matching entity
  if (path.startsWith('/publicRecord/')) {
    const ent = Object.values(allEntities).find(e => e.url === path || e.url === path + '/');
    if (ent) { renderEntity(ent); return; }
  }

  // default: entity index
  renderIndex(entityIndex);
}

function kindColor(kind) {
  return {person:'#e6a4b4',organization:'#58a6ff',analysis:'#d29922',coverage:'#f0883e',guide:'#3fb950',evidence:'#a371f7',letter:'#f85149',timeline:'#8b949e',document:'#e6edf3'}[kind] || '#8b949e';
}

function renderEntity(e) {
  document.title = e.title + ' · petalTongue';
  const refs = (e.page_refs||[]).map(r =>
    `<li><a href="${r.url}">${r.title}</a></li>`
  ).join('');
  const links = (e.internal_links||[]).slice(0,20).map(l => {
    const parts = l.split('/');
    const name = parts[parts.length-1] || parts[parts.length-2] || l;
    return `<li><a href="${l}/">${name}</a> <span class="sub">${l}</span></li>`;
  }).join('');
  const kws = (e.keywords||[]).map(k => `<span class="kw">${k}</span>`).join('');
  const headings = (e.headings||[]).map(h => `<li>${h}</li>`).join('');

  // petalTongue WASM render
  let wasmSvg = '';
  if (wasmMod && wasmMod.render_scene) {
    try {
      const scene = {
        title: e.title,
        kind: e.kind,
        nodes: [{id: e.id, label: e.title, kind: e.kind, size: 24}],
        edges: []
      };
      const connected = relations.filter(r => r.from === e.id || r.to === e.id);
      connected.slice(0,30).forEach(r => {
        const other = r.from === e.id ? r.to : r.from;
        scene.nodes.push({id: other, label: other, kind: 'related', size: 12});
        scene.edges.push({from: r.from, to: r.to});
      });
      wasmSvg = wasmMod.render_scene(JSON.stringify(scene));
    } catch(ex) { console.log('WASM scene:', ex.message); }
  }

  document.getElementById('main').innerHTML = `
    <div class="entity-header">
      <div class="kind" style="color:${kindColor(e.kind)}">${e.kind}</div>
      <h1>${e.title}</h1>
      <p class="desc">${e.description || ''}</p>
    </div>
    <div class="meta-grid">
      <div class="meta-card"><b>${e.words?.toLocaleString() || 0}</b><span>words</span></div>
      <div class="meta-card"><b>${(e.internal_links||[]).length}</b><span>connections</span></div>
      <div class="meta-card"><b>${(e.page_refs||[]).length}</b><span>references</span></div>
      <div class="meta-card"><b>${e.kind}</b><span>type</span></div>
    </div>
    ${kws ? `<div class="keywords">${kws}</div>` : ''}
    ${wasmSvg ? `<div id="wasm-render">${wasmSvg}</div>` : ''}
    <div class="section">
      <h2>Content</h2>
      <div class="content"><p>${(e.full_text || e.excerpt || '').replace(/\n/g, '</p><p>')}</p></div>
    </div>
    ${headings ? `<div class="section"><h2>Structure</h2><ul class="ref-list">${headings}</ul></div>` : ''}
    ${refs ? `<div class="section"><h2>Referenced in</h2><ul class="ref-list">${refs}</ul></div>` : ''}
    ${links ? `<div class="section"><h2>Links to</h2><ul class="ref-list">${links}</ul></div>` : ''}
    <div class="section">
      <h2>Source</h2>
      <p style="font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:var(--mut)">
        ${e.url} · ${e.bytes?.toLocaleString() || 0} bytes · sha: ${e.sha256 || ''}
      </p>
    </div>
  `;
}

function renderIndex(items) {
  document.title = 'Entity Index · petalTongue';
  const kinds = {};
  items.forEach(e => { kinds[e.kind] = (kinds[e.kind]||0) + 1; });
  const kindStats = Object.entries(kinds).map(([k,v]) =>
    `<div class="meta-card"><b>${v}</b><span>${k}</span></div>`
  ).join('');

  const cards = items.slice(0,200).map(e => `
    <a class="entity-card" href="#${e.id}" onclick="location.hash='${e.id}';route();return false;">
      <div class="ek" style="color:${kindColor(e.kind)}">${e.kind}</div>
      <div class="et">${e.title.split('—')[0].trim()}</div>
      <div class="es">${e.words} words · ${e.links} links</div>
    </a>
  `).join('');

  document.getElementById('main').innerHTML = `
    <div class="entity-header">
      <h1>Entity Index</h1>
      <p class="desc">${items.length} entities extracted from dead HTML. petalTongue renders. Data is alive.</p>
    </div>
    <div class="meta-grid">${kindStats}</div>
    <div class="entity-list">${cards}</div>
  `;
}

// search
document.getElementById('q').addEventListener('input', (ev) => {
  const q = ev.target.value.toLowerCase().trim();
  if (!q) { renderIndex(entityIndex); return; }
  const filtered = entityIndex.filter(e =>
    e.title.toLowerCase().includes(q) ||
    e.kind.toLowerCase().includes(q) ||
    e.id.includes(q) ||
    (e.excerpt||'').toLowerCase().includes(q)
  );
  renderIndex(filtered);
});

// hash navigation
window.addEventListener('hashchange', route);
window.route = route;
route();
</script>
</body>
</html>
"""

# write the petalTongue entity renderer
(STATIC / "entity.html").write_text(PETAL_RENDER, encoding="utf-8")
print("entity.html → petalTongue dynamic renderer")

# ── WIRE ROUTES ──
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")

if "p === '/entity'" not in t:
    # find insertion point
    needle = "if (p === '/petal'"
    idx = t.find(needle)
    if idx >= 0:
        block = """
    if (p === '/entity' || p === '/entity/' || p.indexOf('/entity/') === 0) {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/entity.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Petal': 'entity-renderer', 'X-Compiler': 'petalTongue' });
        return res.end(html);
      } catch(e) { return J(res, { ok: false, error: 'entity renderer missing' }, 404); }
    }
    if (p === '/data/entities.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/entities.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Entity': 'api' });
        return res.end(raw);
      } catch(e) { return J(res, { ok: false, error: 'entities missing' }, 404); }
    }
    if (p === '/data/entity-index.json') {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static/data/entity-index.json', 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Entity': 'index' });
        return res.end(raw);
      } catch(e) { return J(res, { ok: false, error: 'entity index missing' }, 404); }
    }
"""
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("entity/API routes wired")
else:
    print("entity routes already present")

# ── Make publicRecord entity URLs route through petalTongue ──
# Instead of serving dead HTML, intercept actor/entity URLs → entity renderer
t = server.read_text(encoding="utf-8")
if "X-Petal-Override" not in t:
    # find the static file serving section for publicRecord
    # add intercept before static fallback for known entity paths
    needle = "if (p.indexOf('/publicRecord/') === 0"
    idx = t.find(needle)
    if idx < 0:
        # try alternate pattern
        needle = "publicRecord"
        candidates = [i for i in range(len(t)) if t[i:].startswith("if (p.indexOf('/publicRecord/") or t[i:].startswith("if (p === '/publicRecord")]
        if candidates:
            idx = candidates[0]
    
    if idx >= 0:
        override_block = """
    // petalTongue entity override: actor/entity URLs → dynamic renderer
    if (p.indexOf('/publicRecord/actors/') === 0 || p.indexOf('/publicRecord/network/actors/') === 0 ||
        p.indexOf('/publicRecord/entities/') === 0 || p.indexOf('/publicRecord/network/entities/') === 0 ||
        p.indexOf('/publicRecord/network/judges/') === 0 || p.indexOf('/publicRecord/analysis/') === 0) {
      if (p !== '/publicRecord/actors/' && p !== '/publicRecord/entities/' &&
          p !== '/publicRecord/network/' && p !== '/publicRecord/analysis/') {
        try {
          var html = fs.readFileSync('/opt/gaia-api/static/entity.html', 'utf8');
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Petal-Override': 'entity', 'X-Compiler': 'petalTongue' });
          return res.end(html);
        } catch(e) { /* fall through to static */ }
      }
    }
"""
        t = t[:idx] + override_block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("publicRecord entity override → petalTongue")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1.5)

# verify
for url in [
    "http://127.0.0.1:9876/entity/",
    "http://127.0.0.1:9876/data/entities.json",
    "http://127.0.0.1:9876/data/entity-index.json",
    "http://127.0.0.1:9876/publicRecord/actors/johnson-l/",
    "http://127.0.0.1:9876/publicRecord/network/actors/brian-banks/",
    "http://127.0.0.1:9876/publicRecord/analysis/damages-calculator/",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code} %{header:x-compiler} %{header:x-petal-override}", url],
        capture_output=True, text=True,
    )
    out = rr.stdout.strip()
    print(out, url.replace("http://127.0.0.1:9876", ""))

print(f"\nDONE: {len(entities)} entities, {len(unique_relations)} relations")
print("petalTongue IS the UI. Dead HTML → entity API → WASM renders.")
