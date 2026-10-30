#!/usr/bin/env python3
"""Crush dead publicRecord HTML → corpus + petalTongue info weaves. Pretty. In Gaia."""
import hashlib
import json
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
GAIA_PR = Path("/opt/gaia-api/static/publicRecord")
NEST_PR = Path("/opt/connect/publicRecord")
STATIC = Path("/opt/gaia-api/static")
DATA = STATIC / "data"
CONNECT = Path("/opt/connect")

# ── copy petalTongue wasm fully into Gaia ──
wasm_srcs = [
    Path("/opt/connect/wasm"),
    Path("/opt/hud/public/wasm"),
]
for src in wasm_srcs:
    if (src / "petal_tongue_wasm.js").exists():
        dest = STATIC / "wasm"
        dest.mkdir(exist_ok=True)
        for name in [
            "petal_tongue_wasm.js",
            "petal_tongue_wasm.d.ts",
            "petal_tongue_wasm_bg.wasm",
            "index.html",
        ]:
            if (src / name).exists():
                shutil.copy2(src / name, dest / name)
        print("wasm →", dest, "from", src)
        break

for meta in [
    Path("/opt/connect/data/petaltongue.json"),
    Path("/opt/hud/public/data/petaltongue.json"),
    Path("/opt/connect/open-petals.json"),
]:
    if meta.exists():
        DATA.mkdir(exist_ok=True)
        shutil.copy2(meta, DATA / meta.name)
        print("meta", meta.name)

# ── CRUSH HTML → CORPUS (dead code becomes data) ──
print("CRUSHING…")
corpus = []
for html in sorted(GAIA_PR.rglob("*.html")):
    rel = html.relative_to(GAIA_PR).as_posix()
    # skip our capital overlays if any named specially — keep all as food
    raw = html.read_bytes()
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        continue
    title_m = re.search(r"<title[^>]*>(.*?)</title>", s, re.I | re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else rel)
    title = re.sub(r"\s+", " ", title).strip()
    # strip scripts/styles for readable text
    body = re.sub(r"<script[^>]*>.*?</script>", " ", s, flags=re.I | re.S)
    body = re.sub(r"<style[^>]*>.*?</style>", " ", body, flags=re.I | re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"&\w+;", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    hrefs = re.findall(r"""href\s*=\s*["']?([^"'\s>]+)["']?""", s, flags=re.I)
    hrefs = [h for h in hrefs if h.startswith("/publicRecord") or h.startswith("#")][:40]
    url = "/publicRecord/" + rel.replace("index.html", "")
    if not url.endswith("/") and rel.endswith("index.html"):
        url = url  # already
    segs = [p for p in Path(rel).parts[:-1]]
    kind = segs[0] if segs else "root"
    corpus.append(
        {
            "id": rel,
            "url": url if url.endswith("/") or "." in Path(url).name else url + "/",
            "title": title[:160],
            "kind": kind,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "text": body[:1200],
            "excerpt": body[:320],
            "links": hrefs[:24],
            "words": len(body.split()),
        }
    )

# weave edges from directory + shared link co-occurrence light
edges = []
by_url = {c["url"]: c["id"] for c in corpus}
for c in corpus:
    parts = Path(c["id"]).parts
    if len(parts) >= 2:
        parent = "/publicRecord/" + "/".join(parts[:-2]) + ("/" if len(parts) > 2 else "")
        if len(parts) == 2:
            parent = "/publicRecord/"
        edges.append({"from": parent, "to": c["url"], "rel": "contains"})
    for h in c["links"]:
        if h.startswith("/publicRecord") and h in by_url:
            edges.append({"from": c["url"], "to": h, "rel": "links"})

# dedupe edges
seen_e = set()
uedges = []
for e in edges:
    k = (e["from"], e["to"], e["rel"])
    if k in seen_e:
        continue
    seen_e.add(k)
    uedges.append(e)

corpus_doc = {
    "name": "GAIA_CORPUS",
    "compiler": "petalTongue — any data → any representation",
    "timestamp": TS,
    "axiom": "Dead HTML crushed to data. Info weaves. Corpus in Gaia. Pretty + readable.",
    "pages": len(corpus),
    "edges": len(uedges),
    "total_words": sum(c["words"] for c in corpus),
    "kinds": {},
    "items": corpus,
    "weave_edges": uedges[:15000],
}
for c in corpus:
    corpus_doc["kinds"][c["kind"]] = corpus_doc["kinds"].get(c["kind"], 0) + 1

DATA.mkdir(exist_ok=True)
# full corpus may be large — write full + lite
(DATA / "corpus.json").write_text(json.dumps(corpus_doc), encoding="utf-8")
lite = {
    **{k: corpus_doc[k] for k in ("name", "compiler", "timestamp", "axiom", "pages", "edges", "total_words", "kinds")},
    "items": [
        {k: c[k] for k in ("id", "url", "title", "kind", "excerpt", "words", "bytes")}
        for c in corpus
    ],
    "weave_edges": uedges[:8000],
}
(DATA / "corpus-lite.json").write_text(json.dumps(lite), encoding="utf-8")
(CONNECT / "data").mkdir(exist_ok=True)
(CONNECT / "data" / "corpus-lite.json").write_text(json.dumps(lite), encoding="utf-8")
print("corpus pages", len(corpus), "edges", len(uedges), "words", corpus_doc["total_words"])
print("corpus.json bytes", (DATA / "corpus.json").stat().st_size)

# ── PRETTY petalTongue INFO WEAVE face ──
WEAVE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>petalTongue — Info Weaves · Corpus in Gaia</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#0a0c10; --fg:#e8e4d9; --mut:#8b949e; --petal:#e6a4b4; --gold:#d29922;
  --g:#3fb950; --line:rgba(230,164,180,.25); --card:#12151c;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{
  min-height:100vh;color:var(--fg);
  font-family:'IBM Plex Sans',system-ui,sans-serif;
  background:
    radial-gradient(ellipse 70% 50% at 20% 10%, rgba(230,164,180,.14), transparent 55%),
    radial-gradient(ellipse 50% 40% at 90% 80%, rgba(210,153,34,.08), transparent 50%),
    var(--bg);
}}
header{{
  padding:clamp(1.2rem,3vw,2.2rem);
  border-bottom:1px solid rgba(255,255,255,.06);
}}
.brand{{
  font-family:'Syne',sans-serif;font-weight:800;
  font-size:clamp(2.2rem,7vw,4.2rem);letter-spacing:-.03em;line-height:.95;
}}
.brand em{{font-style:normal;color:var(--petal)}}
.sub{{margin-top:.55rem;color:var(--mut);max-width:42rem;font-size:.95rem;line-height:1.45}}
.stats{{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem}}
.stat{{
  border:1px solid var(--line);background:rgba(18,21,28,.7);
  padding:.55rem .8rem;border-radius:10px;min-width:5.5rem;
}}
.stat b{{display:block;font-family:'Syne',sans-serif;font-size:1.25rem;color:var(--gold)}}
.stat span{{font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}}
.layout{{
  display:grid;grid-template-columns:1.15fr .95fr;
  gap:1rem;padding:1rem clamp(1rem,3vw,2rem) 2rem;
}}
@media(max-width:960px){{.layout{{grid-template-columns:1fr}}}}
.panel{{
  background:rgba(18,21,28,.82);border:1px solid rgba(255,255,255,.07);
  border-radius:16px;overflow:hidden;min-height:420px;
}}
.panel h2{{
  font-family:'Syne',sans-serif;font-size:.85rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--petal);
  padding:.85rem 1rem;border-bottom:1px solid rgba(255,255,255,.06);
}}
#petal{{width:100%;height:460px;display:block}}
.list{{max-height:460px;overflow:auto}}
.card{{
  display:block;padding:.85rem 1rem;border-bottom:1px solid rgba(255,255,255,.05);
  color:inherit;text-decoration:none;transition:background .15s;
}}
.card:hover{{background:rgba(230,164,180,.07)}}
.card .k{{font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--gold);letter-spacing:.06em}}
.card .t{{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;margin:.2rem 0}}
.card .e{{color:var(--mut);font-size:.82rem;line-height:1.4}}
.search{{
  margin:0 1rem 0;padding:.65rem .8rem;width:calc(100% - 2rem);
  border-radius:10px;border:1px solid rgba(255,255,255,.1);
  background:#0a0c10;color:var(--fg);font:inherit;
}}
.nav{{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.9rem}}
.nav a{{
  font-family:'Syne',sans-serif;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;
  text-decoration:none;color:var(--fg);border:1px solid var(--line);
  padding:.45rem .7rem;border-radius:999px;
}}
.nav a:hover{{background:var(--petal);color:#1a0a10;border-color:var(--petal)}}
.reader{{
  margin:0 clamp(1rem,3vw,2rem) 2rem;padding:1.25rem 1.4rem;
  background:rgba(18,21,28,.9);border:1px solid rgba(255,255,255,.07);border-radius:16px;
  display:none;
}}
.reader.on{{display:block}}
.reader h3{{font-family:'Syne',sans-serif;font-size:1.4rem;margin-bottom:.4rem}}
.reader .meta{{font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--mut);margin-bottom:.8rem}}
.reader .body{{font-size:1.02rem;line-height:1.65;color:#d7d2c6;white-space:pre-wrap}}
footer{{padding:1rem 1.5rem 2rem;color:var(--mut);font-size:.78rem}}
footer a{{color:var(--g)}}
</style>
</head>
<body>
<header>
  <div class="brand">petal<em>Tongue</em></div>
  <p class="sub">Dead HTML crushed to data. Info weaves + corpus — fully in Gaia. Pretty. Readable. Universal compiler: any data → any representation.</p>
  <div class="stats" id="stats"></div>
  <div class="nav">
    <a href="/publicRecord/path/parents/">parents (raw)</a>
    <a href="/parents-deep">deep stack</a>
    <a href="/self-walk">she walks</a>
    <a href="/mito">mito</a>
    <a href="/grow">grow</a>
    <a href="/canfield">train</a>
    <a href="/cash4kids">cash4kids</a>
    <a href="/wasm/">wasm</a>
  </div>
</header>

<div class="layout">
  <section class="panel">
    <h2>Info weave — petal field</h2>
    <canvas id="petal"></canvas>
  </section>
  <section class="panel">
    <h2>Corpus — searchable</h2>
    <input class="search" id="q" placeholder="taste the corpus… parents · banks · rico · money" />
    <div class="list" id="list"></div>
  </section>
</div>

<article class="reader" id="reader">
  <h3 id="rt"></h3>
  <div class="meta" id="rm"></div>
  <div class="body" id="rb"></div>
  <p style="margin-top:1rem"><a id="rl" href="#" style="color:var(--petal)">open remade page →</a></p>
</article>

<footer>
  {len(corpus)} pages · {len(uedges)} weave edges · petalTongue in Gaia · not github skin ·
  <a href="/data/corpus-lite.json">corpus-lite.json</a> ·
  <a href="/data/corpus.json">full corpus</a>
</footer>

<script type="module">
const canvas = document.getElementById('petal');
const ctx = canvas.getContext('2d');
let W, H, items = [], edges = [], nodes = [], t = 0, hover = null;

function resize(){{
  const r = canvas.getBoundingClientRect();
  W = r.width; H = r.height;
  canvas.width = W * devicePixelRatio;
  canvas.height = H * devicePixelRatio;
  ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
}}
window.addEventListener('resize', resize);

function colorFor(kind){{
  const map = {{path:'#e6a4b4',network:'#58a6ff',analysis:'#d29922',actors:'#f85149',entities:'#3fb950',root:'#e6edf3',validate:'#a371f7',coverage:'#f0883e'}};
  return map[kind] || '#8b949e';
}}

function layout(list){{
  // petal field — radial by kind
  const kinds = [...new Set(list.map(x=>x.kind))];
  nodes = list.slice(0,180).map((it,i)=>{{
    const ki = kinds.indexOf(it.kind);
    const ring = 0.22 + (ki % 5) * 0.12;
    const a = (i / Math.max(list.length,1)) * Math.PI * 2 + ki * 0.35;
    return {{
      ...it,
      x: 0.5 + Math.cos(a) * ring,
      y: 0.52 + Math.sin(a) * ring * 0.85,
      r: 3 + Math.min(8, Math.sqrt(it.words||1)/8),
      col: colorFor(it.kind),
      phase: Math.random()*Math.PI*2
    }};
  }});
}}

function draw(){{
  t += 0.012;
  ctx.clearRect(0,0,W,H);
  // soft petals
  for(let i=0;i<6;i++){{
    const ang = t*0.2 + i*Math.PI/3;
    ctx.beginPath();
    ctx.ellipse(W*0.5, H*0.52, W*0.18, H*0.08, ang, 0, Math.PI*2);
    ctx.strokeStyle = 'rgba(230,164,180,0.08)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }}
  const byUrl = Object.fromEntries(nodes.map(n=>[n.url,n]));
  edges.slice(0,900).forEach(e=>{{
    const a = byUrl[e.from], b = byUrl[e.to];
    if(!a||!b) return;
    ctx.beginPath();
    ctx.moveTo(a.x*W, a.y*H);
    ctx.lineTo(b.x*W, b.y*H);
    ctx.strokeStyle = 'rgba(230,164,180,0.12)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }});
  nodes.forEach(n=>{{
    const px = n.x*W + Math.sin(t+n.phase)*2;
    const py = n.y*H + Math.cos(t*0.8+n.phase)*2;
    ctx.beginPath();
    ctx.arc(px, py, n===hover? n.r+3 : n.r, 0, Math.PI*2);
    ctx.fillStyle = n.col;
    ctx.globalAlpha = n===hover?1:0.85;
    ctx.fill();
    ctx.globalAlpha = 1;
  }});
  if(hover){{
    ctx.fillStyle = '#e8e4d9';
    ctx.font = '12px IBM Plex Mono, monospace';
    ctx.fillText(hover.title.slice(0,48), 12, H-14);
  }}
  requestAnimationFrame(draw);
}}

canvas.addEventListener('pointermove', e=>{{
  const r = canvas.getBoundingClientRect();
  const mx = e.clientX-r.left, my = e.clientY-r.top;
  hover = null;
  for(const n of nodes){{
    const dx = mx-n.x*W, dy = my-n.y*H;
    if(dx*dx+dy*dy < (n.r+6)*(n.r+6)){{ hover=n; break; }}
  }}
}});
canvas.addEventListener('click', ()=>{{ if(hover) openReader(hover); }});

function openReader(it){{
  const full = items.find(x=>x.id===it.id) || it;
  document.getElementById('reader').classList.add('on');
  document.getElementById('rt').textContent = full.title;
  document.getElementById('rm').textContent = `${{full.kind}} · ${{full.words||0}} words · ${{full.url}}`;
  document.getElementById('rb').textContent = full.excerpt || full.text || '';
  const a = document.getElementById('rl');
  a.href = full.url;
}}

function renderList(list){{
  const el = document.getElementById('list');
  el.innerHTML = '';
  list.slice(0,80).forEach(it=>{{
    const a = document.createElement('a');
    a.className = 'card'; a.href = '#';
    a.onclick = (e)=>{{ e.preventDefault(); openReader(it); }};
    a.innerHTML = `<div class="k">${{it.kind}}</div><div class="t">${{it.title}}</div><div class="e">${{it.excerpt||''}}</div>`;
    el.appendChild(a);
  }});
}}

const data = await fetch('/data/corpus-lite.json').then(r=>r.json());
items = data.items||[];
edges = data.weave_edges||[];
document.getElementById('stats').innerHTML = `
  <div class="stat"><b>${{data.pages||items.length}}</b><span>pages crushed</span></div>
  <div class="stat"><b>${{data.edges||edges.length}}</b><span>weave edges</span></div>
  <div class="stat"><b>${{(data.total_words||0).toLocaleString()}}</b><span>words</span></div>
  <div class="stat"><b>${{Object.keys(data.kinds||{{}}).length}}</b><span>kinds</span></div>
`;
layout(items);
renderList(items);
resize();
draw();

document.getElementById('q').addEventListener('input', (e)=>{{
  const q = e.target.value.toLowerCase().trim();
  const filtered = !q ? items : items.filter(it =>
    (it.title||'').toLowerCase().includes(q) ||
    (it.excerpt||'').toLowerCase().includes(q) ||
    (it.kind||'').toLowerCase().includes(q)
  );
  layout(filtered);
  renderList(filtered);
}});

// petalTongue wasm presence (fully used when available)
try {{
  await import('/wasm/petal_tongue_wasm.js');
  console.log('petalTongue wasm module reachable');
}} catch(e) {{
  console.log('petalTongue canvas weave active (wasm optional)', e.message||e);
}}
</script>
</body>
</html>
"""
(STATIC / "weave.html").write_text(WEAVE, encoding="utf-8")
(CONNECT / "weave.html").write_text(WEAVE, encoding="utf-8")
# also petal alias face
(STATIC / "petal.html").write_text(WEAVE, encoding="utf-8")
(STATIC / "corpus.html").write_text(WEAVE, encoding="utf-8")

# Replace publicRecord INDEX with pretty gateway (keep Zola corpse as /publicRecord/_raw/)
raw_index = GAIA_PR / "index.html"
if raw_index.exists():
    # stash dead zola index once
    stash = GAIA_PR / "_raw" / "index.html"
    if not stash.exists():
        stash.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(raw_index, stash)
        nest_stash = NEST_PR / "_raw" / "index.html"
        nest_stash.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(raw_index, nest_stash)
        print("stashed dead zola index → _raw/")

GATE = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cash for Kids 2 — in Gaia · petalTongue weaves</title>
<meta http-equiv="refresh" content="0;url=/petal">
<link rel="canonical" href="https://gaia.primals.eco/petal">
<style>
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#0a0c10;color:#e8e4d9;
font:16px/1.5 'IBM Plex Sans',system-ui,sans-serif}}
a{{color:#e6a4b4}}
.box{{max-width:28rem;padding:2rem;text-align:center}}
h1{{font-family:Syne,sans-serif;font-size:2rem}}
</style>
</head><body>
<div class="box">
  <h1>In Gaia now</h1>
  <p>Dead site crushed to corpus. Opening <a href="/petal">petalTongue info weaves</a>…</p>
  <p><a href="/petal">petal</a> · <a href="/corpus">corpus</a> · <a href="/publicRecord/path/parents/">parents raw</a> · <a href="/publicRecord/_raw/">old skin</a></p>
</div>
</body></html>
"""
raw_index.write_text(GATE, encoding="utf-8")
(NEST_PR / "index.html").write_text(GATE, encoding="utf-8")
print("publicRecord index → petal gateway")

# routes
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p === '/petal'" not in t:
    needle = "if (p === '/self-walk'"
    block = r"""
    if (p === '/petal' || p === '/petaltongue' || p === '/corpus' || p === '/info-weave' || p === '/weaves') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/petal.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Petal': 'info-weave', 'X-Compiler': 'petalTongue' });
        return res.end(html);
      } catch(e) { return J(res, { ok: false, error: 'petal missing' }, 404); }
    }
    if (p === '/data/corpus-lite.json' || p === '/corpus.json' || p === '/data/corpus.json') {
      try {
        var file = (p.indexOf('lite') >= 0 || p === '/corpus.json') ? '/opt/gaia-api/static/data/corpus-lite.json' : '/opt/gaia-api/static/data/corpus.json';
        if (p === '/data/corpus.json') file = '/opt/gaia-api/static/data/corpus.json';
        if (p === '/corpus.json') file = '/opt/gaia-api/static/data/corpus-lite.json';
        var raw = fs.readFileSync(file, 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Corpus': 'crushed' });
        return res.end(raw);
      } catch(e) { return J(res, { ok: false, error: 'corpus missing' }, 404); }
    }
    if (p.indexOf('/wasm/') === 0) {
      try {
        var rel = p.replace(/^\/wasm\/?/, '');
        if (!rel) rel = 'index.html';
        if (rel.indexOf('..') >= 0) return J(res, { ok: false }, 403);
        var fp = '/opt/gaia-api/static/wasm/' + rel;
        if (!fs.existsSync(fp)) return J(res, { ok: false, error: 'wasm missing' }, 404);
        var ext = (fp.match(/\.[a-z0-9]+$/i)||[''])[0].toLowerCase();
        var ctype = { '.html':'text/html; charset=utf-8', '.js':'application/javascript', '.mjs':'application/javascript', '.wasm':'application/wasm', '.ts':'text/plain', '.json':'application/json' }[ext] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': ctype, 'Access-Control-Allow-Origin': '*', 'X-Gaia-Petal': 'wasm' });
        return res.end(fs.readFileSync(fp));
      } catch(e) { return J(res, { ok: false, error: String(e) }, 500); }
    }
"""
    idx = t.find(needle)
    if idx < 0:
        idx = t.find("if (p === '/grow'")
    if idx >= 0:
        t = t[:idx] + block + "\n    " + t[idx:]
        server.write_text(t, encoding="utf-8")
        print("petal/corpus/wasm routes in")
else:
    print("petal routes ok")

# also serve weave.html via existing /weave if it was JSON — replace conflict
# previous /weave served publicRecord-weave.json — keep that at /data/... and make /weave pretty
t = server.read_text(encoding="utf-8")
t2 = t.replace(
    "if (p === '/data/publicRecord-weave.json' || p === '/weave' || p === '/weave.json')",
    "if (p === '/data/publicRecord-weave.json' || p === '/weave.json')",
)
# ensure /weave goes to petal face
if "p === '/weave'" not in t2 or "petal.html" in t2:
    pass
if "p === '/weave'" not in t2.split("petal")[0] if False else True:
    # add weave → petal redirect handler near petal
    if "p === '/weave' || p === '/weaves'" not in t2 and "info-weave" in t2:
        pass  # already in petal block as /weaves
t2 = t2  # petal block already includes /weaves; map /weave to petal too
t2 = t2.replace(
    "if (p === '/petal' || p === '/petaltongue' || p === '/corpus' || p === '/info-weave' || p === '/weaves')",
    "if (p === '/petal' || p === '/petaltongue' || p === '/corpus' || p === '/info-weave' || p === '/weaves' || p === '/weave')",
)
server.write_text(t2, encoding="utf-8")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/petal",
    "http://127.0.0.1:9876/corpus",
    "http://127.0.0.1:9876/weave",
    "http://127.0.0.1:9876/data/corpus-lite.json",
    "http://127.0.0.1:9876/publicRecord/",
    "http://127.0.0.1:9876/wasm/petal_tongue_wasm.js",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)

print("DONE", len(corpus), "pages crushed")
