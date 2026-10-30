#!/usr/bin/env python3
"""petalTongue IS the UI primal — corpus → WASM build_site / render_dashboard / pages. No fake canvas UI."""
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

TS = datetime.now(timezone.utc).isoformat()
STATIC = Path("/opt/gaia-api/static")
DATA = STATIC / "data"
CONNECT = Path("/opt/connect")
JS = STATIC / "js"
JS.mkdir(exist_ok=True)

# copy bridge + wasm fully
for src in [
    Path("/opt/publicRecord/site/static/js/pt-bridge-core.js"),
    Path("/opt/connect/js/pt-membrane.js"),
]:
    if src.exists():
        shutil.copy2(src, JS / src.name)
        print("js", src.name)

# ensure wasm
wasm_src = Path("/opt/connect/wasm")
wasm_dest = STATIC / "wasm"
wasm_dest.mkdir(exist_ok=True)
for name in ["petal_tongue_wasm.js", "petal_tongue_wasm_bg.wasm", "petal_tongue_wasm.d.ts"]:
    if (wasm_src / name).exists():
        shutil.copy2(wasm_src / name, wasm_dest / name)

corpus = json.loads((DATA / "corpus-lite.json").read_text(encoding="utf-8"))
items = corpus.get("items") or []
kinds = corpus.get("kinds") or {}
# sort kinds by count
kind_cats = sorted(kinds.keys(), key=lambda k: -kinds[k])
kind_vals = [kinds[k] for k in kind_cats]

# SiteContent for build_site — discover shape via node probe first
site_pages = []
# capital index
site_pages.append(
    {
        "path": "index.html",
        "title": "Cash for Kids 2 — corpus in Gaia",
        "slug": "index",
        "body": (
            f"<p>Dead HTML crushed. {corpus.get('pages')} pages · "
            f"{corpus.get('total_words')} words · {corpus.get('edges')} weave edges.</p>"
            "<p>Rendered by <strong>petalTongue</strong> — the Universal UI primal.</p>"
        ),
        "content": (
            f"Dead HTML crushed. {corpus.get('pages')} pages. "
            f"{corpus.get('total_words')} words. petalTongue UI primal."
        ),
        "description": "Public record corpus — pretty + readable via petalTongue",
        "sections": [
            {
                "heading": "Corpus",
                "body": f"{corpus.get('pages')} pages crushed into data. Search and read below.",
            }
        ],
    }
)
# kind index pages + top readable pages
for kind in kind_cats[:24]:
    kids = [it for it in items if it.get("kind") == kind][:40]
    lis = "".join(
        f"<li><a href=\"{it.get('url','#')}\">{it.get('title','')}</a> — {(it.get('excerpt') or '')[:140]}</li>"
        for it in kids
    )
    site_pages.append(
        {
            "path": f"kind/{kind}/index.html",
            "title": f"{kind} — corpus",
            "slug": f"kind-{kind}",
            "body": f"<h2>{kind}</h2><p>{kinds[kind]} pages</p><ul>{lis}</ul>",
            "content": f"{kind}: {kinds[kind]} pages. " + " ".join(it.get("title", "") for it in kids[:10]),
            "description": f"{kind} pages from crushed publicRecord",
            "sections": [{"heading": kind, "body": f"{kinds[kind]} pages in this kind."}],
        }
    )

# top wordy pages as readable entries
top = sorted(items, key=lambda x: -(x.get("words") or 0))[:80]
for it in top:
    safe = (it.get("id") or "page").replace("/", "__").replace(".html", "")
    site_pages.append(
        {
            "path": f"read/{safe}/index.html",
            "title": it.get("title") or safe,
            "slug": f"read-{safe}"[:80],
            "body": (
                f"<p class='meta'>{it.get('kind')} · {it.get('words')} words · "
                f"<a href=\"{it.get('url')}\">source remade page</a></p>"
                f"<div class='excerpt'>{it.get('excerpt') or ''}</div>"
            ),
            "content": it.get("excerpt") or it.get("title") or "",
            "description": (it.get("excerpt") or "")[:160],
            "sections": [
                {"heading": it.get("title") or safe, "body": it.get("excerpt") or ""},
            ],
        }
    )

nav = [
    {"title": "Home", "path": "/", "href": "/"},
    {"title": "Parents", "path": "/publicRecord/path/parents/", "href": "/publicRecord/path/parents/"},
    {"title": "Deep", "path": "/parents-deep", "href": "/parents-deep"},
    {"title": "Corpus JSON", "path": "/data/corpus-lite.json", "href": "/data/corpus-lite.json"},
    {"title": "WASM", "path": "/wasm/", "href": "/wasm/"},
]

site_content = {
    "site_title": "Gaia · publicRecord corpus",
    "title": "Gaia · publicRecord corpus",
    "pages": site_pages,
    "nav": nav,
    "navigation": nav,
    "search_index": [
        {"title": it.get("title"), "url": it.get("url"), "body": it.get("excerpt") or "", "id": it.get("id")}
        for it in items[:500]
    ],
    "entity_registry": {
        "kinds": kinds,
        "pages": corpus.get("pages"),
        "words": corpus.get("total_words"),
    },
}

site_layout = {
    "site_title": "Gaia · petalTongue UI",
    "title": "Gaia · petalTongue UI",
    "footer": "petalTongue — Universal UI primal · dead code crushed to corpus · in Gaia",
    "css": """
:root { --bg:#0b0d12; --fg:#e8e4d9; --mut:#8b949e; --petal:#e6a4b4; --gold:#d29922; --g:#3fb950; }
body { margin:0; background:radial-gradient(ellipse at 20% 0%, rgba(230,164,180,.12), transparent 50%), var(--bg); color:var(--fg); font:16px/1.55 'IBM Plex Sans', system-ui, sans-serif; }
a { color:var(--petal); }
header, .site-header { padding:1.25rem 1.5rem; border-bottom:1px solid rgba(255,255,255,.07); }
h1,h2 { font-family: Syne, system-ui, sans-serif; }
.excerpt, .content, main { max-width:48rem; padding:1rem 1.5rem 2rem; }
.meta { color:var(--mut); font-size:.85rem; }
footer, .site-footer { padding:1rem 1.5rem; color:var(--mut); font-size:.8rem; border-top:1px solid rgba(255,255,255,.06); }
ul { padding-left:1.2rem; }
li { margin:.35rem 0; }
""",
}

(DATA / "site-content.json").write_text(json.dumps(site_content), encoding="utf-8")
(DATA / "site-layout.json").write_text(json.dumps(site_layout), encoding="utf-8")

# DataBindings for petalTongue render_dashboard — THE UI viz of corpus
bindings = [
    {
        "id": "corpus-kinds",
        "channel": "bar",
        "label": "Corpus by kind",
        "categories": kind_cats[:16],
        "values": [float(kinds[k]) for k in kind_cats[:16]],
        "unit": "pages",
    },
    {
        "id": "corpus-donut",
        "channel": "donut",
        "label": "Kind share",
        "categories": kind_cats[:10],
        "values": [float(kinds[k]) for k in kind_cats[:10]],
        "unit": "pages",
    },
    {
        "id": "corpus-words",
        "channel": "gauge",
        "label": "Words crushed",
        "value": float(corpus.get("total_words") or 0),
        "min": 0.0,
        "max": float(max(corpus.get("total_words") or 1, 400000)),
        "unit": "words",
        "normal_range": [0.0, float(corpus.get("total_words") or 0)],
        "warning_range": [0.0, 0.0],
    },
    {
        "id": "corpus-edges",
        "channel": "gauge",
        "label": "Weave edges",
        "value": float(corpus.get("edges") or 0),
        "min": 0.0,
        "max": float(max((corpus.get("edges") or 1) * 1.2, 1000)),
        "unit": "edges",
        "normal_range": [0.0, float(corpus.get("edges") or 0)],
        "warning_range": [0.0, 0.0],
    },
    {
        "id": "top-pages",
        "channel": "bar",
        "label": "Top pages by words",
        "categories": [(it.get("title") or "?")[:28] for it in top[:12]],
        "values": [float(it.get("words") or 0) for it in top[:12]],
        "unit": "words",
    },
]
(DATA / "corpus-bindings.json").write_text(json.dumps(bindings), encoding="utf-8")
(CONNECT / "data" / "corpus-bindings.json").write_text(json.dumps(bindings), encoding="utf-8")
(CONNECT / "data" / "site-content.json").write_text(json.dumps(site_content), encoding="utf-8")

# Node: actually COMPILE with petalTongue WASM — UI primal does the render
probe = r"""
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

const wasmJs = '/opt/gaia-api/static/wasm/petal_tongue_wasm.js';
const wasmBin = '/opt/gaia-api/static/wasm/petal_tongue_wasm_bg.wasm';

async function main() {
  const mod = await import(pathToFileURL(wasmJs).href);
  const init = mod.default;
  const {
    init: ptInit,
    version,
    build_site,
    render_dashboard,
    render_bindings,
    render_binding,
    render_page_with_layout,
  } = mod;

  const bytes = readFileSync(wasmBin);
  await init(bytes);
  if (ptInit) ptInit();
  console.log('petalTongue version', version());

  const content = readFileSync('/opt/gaia-api/static/data/site-content.json', 'utf8');
  const layout = readFileSync('/opt/gaia-api/static/data/site-layout.json', 'utf8');
  const bindings = readFileSync('/opt/gaia-api/static/data/corpus-bindings.json', 'utf8');

  // 1) dashboard SVG from bindings — UI primal
  let dash = null;
  try {
    dash = render_dashboard(bindings, JSON.stringify({
      layout: 'grid',
      max_columns: 2,
      panel_width: 480,
      panel_height: 280,
      spacing: 16,
      title: 'Gaia corpus — petalTongue UI',
      domain: 'signal'
    }));
    console.log('dashboard bytes', dash ? dash.length : 0, dash && dash.slice(0, 80));
  } catch (e) {
    console.log('dashboard err', String(e));
  }

  let binds = null;
  try {
    binds = render_bindings(bindings, 'signal');
    console.log('bindings out', binds ? binds.slice(0, 120) : null);
  } catch (e) {
    console.log('bindings err', String(e));
  }

  // try single binding shapes
  const b0 = JSON.parse(bindings)[0];
  try {
    const one = render_binding(JSON.stringify(b0), 'signal');
    console.log('one binding', one ? one.slice(0, 100) : null);
  } catch (e) {
    console.log('one binding err', String(e));
  }

  // alternate channel tag shapes used by live bridge
  const alt = {
    id: 'corpus-kinds',
    label: 'Corpus by kind',
    x_label: 'kind',
    y_label: 'pages',
    unit: 'pages',
    categories: b0.categories,
    values: b0.values,
    channel: { type: 'bar', categories: b0.categories, values: b0.values },
  };
  for (const shape of [
    b0,
    { ...b0, type: 'bar' },
    { id: b0.id, label: b0.label, unit: b0.unit, bar: { categories: b0.categories, values: b0.values } },
    { id: b0.id, label: b0.label, unit: 'pages', timeseries: { x_values: b0.categories.map((_,i)=>i), y_values: b0.values, x_label: 'kind', y_label: 'pages' } },
    alt,
  ]) {
    try {
      const r = render_binding(JSON.stringify(shape), 'signal');
      console.log('shape ok', Object.keys(shape).join(','), '→', (r||'').slice(0, 60));
      if (r && r.startsWith('<svg') || (r && r.includes('<svg'))) { writeFileSync('/tmp/pt_shape_ok.json', JSON.stringify(shape)); break; }
      if (r && !String(r).startsWith('Error')) { writeFileSync('/tmp/pt_shape_ok.json', JSON.stringify(shape)); console.log('non-error', r.slice(0,200)); break; }
    } catch (e) {
      console.log('shape fail', Object.keys(shape).join(','), String(e).slice(0,120));
    }
  }

  // 2) build_site
  let site = null;
  for (const c of [
    content,
    JSON.stringify({ pages: JSON.parse(content).pages, nav: JSON.parse(content).nav, search_index: [], entity_registry: {} }),
    JSON.stringify({ pages: JSON.parse(content).pages.map(p => ({
      title: p.title,
      path: p.path,
      content: p.content || p.body,
      description: p.description || '',
    })) }),
  ]) {
    try {
      site = build_site(c, layout);
      console.log('build_site', site ? site.slice(0, 200) : null);
      if (site && !String(site).startsWith('Error')) break;
    } catch (e) {
      console.log('build_site err', String(e).slice(0, 200));
    }
  }

  // 3) render_page_with_layout
  const page0 = JSON.parse(content).pages[0];
  for (const page of [
    page0,
    { type: 'Page', title: page0.title, path: page0.path, content: page0.content, body: page0.body },
    { Page: page0 },
    { title: page0.title, slug: 'index', markdown: page0.content, html: page0.body },
    { title: page0.title, path: '/', blocks: [{ type: 'paragraph', text: page0.content }] },
  ]) {
    try {
      const html = render_page_with_layout(JSON.stringify(page), JSON.stringify(JSON.parse(content).nav), layout);
      console.log('page', Object.keys(page).join(','), '→', (html||'').slice(0, 100));
      if (html && html.includes('<html')) {
        writeFileSync('/tmp/pt_page_ok.html', html);
        writeFileSync('/tmp/pt_page_shape.json', JSON.stringify(page));
        break;
      }
    } catch (e) {
      console.log('page fail', String(e).slice(0, 150));
    }
  }

  mkdirSync('/opt/gaia-api/static/data', { recursive: true });
  const out = {
    version: version(),
    dashboard: dash && !String(dash).startsWith('Error') ? dash : null,
    dashboard_error: dash && String(dash).startsWith('Error') ? dash : null,
    bindings: binds,
    site: site && !String(site).startsWith('Error') ? (site.length > 500000 ? site.slice(0, 500000) : site) : null,
    site_error: site && String(site).startsWith('Error') ? site : null,
    site_len: site ? site.length : 0,
  };
  writeFileSync('/opt/gaia-api/static/data/pt-compile-result.json', JSON.stringify({
    version: out.version,
    has_dashboard: !!out.dashboard,
    dashboard_error: out.dashboard_error,
    site_error: out.site_error,
    site_len: out.site_len,
    bindings_preview: binds ? String(binds).slice(0, 300) : null,
  }));
  if (out.dashboard) writeFileSync('/opt/gaia-api/static/data/corpus-dashboard.svg', out.dashboard);
  if (out.site) {
    try {
      const parsed = JSON.parse(out.site);
      writeFileSync('/opt/gaia-api/static/data/pt-site-built.json', JSON.stringify({
        file_count: parsed.file_count,
        total_bytes: parsed.total_bytes,
        files: Object.keys(parsed.files || {}).slice(0, 50),
      }));
      const outDir = '/opt/gaia-api/static/pt-site';
      mkdirSync(outDir, { recursive: true });
      const files = parsed.files || {};
      let n = 0;
      for (const [rel, html] of Object.entries(files)) {
        if (typeof html !== 'string') continue;
        const fp = outDir + '/' + rel;
        mkdirSync(fp.split('/').slice(0, -1).join('/') || outDir, { recursive: true });
        writeFileSync(fp, html);
        n++;
        if (n > 200) break;
      }
      console.log('wrote pt-site files', n);
    } catch (e) {
      console.log('site parse', String(e), out.site.slice(0, 300));
    }
  }
  console.log('DONE compile');
}
main().catch(e => { console.error(e); process.exit(1); });
"""
Path("/tmp/pt_compile.mjs").write_text(probe, encoding="utf-8")
# also write under /opt
Path("/opt/gaia-api/static/js/pt_compile.mjs").write_text(probe, encoding="utf-8")
r = subprocess.run(
    ["node", "/opt/gaia-api/static/js/pt_compile.mjs"],
    capture_output=True,
    text=True,
    cwd="/opt/gaia-api/static",
)
print("NODE OUT:", r.stdout[-4000:] if r.stdout else "")
print("NODE ERR:", (r.stderr or "")[-2000:])

# Build the UI shell that IS petalTongue — loads WASM, renders dashboard + readable corpus via UI primal
FACE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>petalTongue — UI primal · Gaia corpus</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--bg:#0b0d12;--fg:#e8e4d9;--mut:#8b949e;--petal:#e6a4b4;--gold:#d29922;--g:#3fb950;--line:rgba(230,164,180,.28)}
*{box-sizing:border-box;margin:0;padding:0}
body{min-height:100vh;color:var(--fg);font:16px/1.5 'IBM Plex Sans',system-ui,sans-serif;
background:radial-gradient(ellipse 70% 45% at 15% 0%,rgba(230,164,180,.14),transparent 55%),var(--bg)}
header{padding:clamp(1.2rem,3vw,2rem);border-bottom:1px solid rgba(255,255,255,.06)}
.brand{font-family:Syne,sans-serif;font-weight:800;font-size:clamp(2rem,6vw,3.6rem);letter-spacing:-.03em;line-height:.95}
.brand em{font-style:normal;color:var(--petal)}
.sub{margin-top:.5rem;color:var(--mut);max-width:40rem}
#pt-status{font-family:'IBM Plex Mono',monospace;font-size:.75rem;margin-top:.6rem;color:var(--mut)}
.nav{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.9rem}
.nav a{font-family:Syne,sans-serif;font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;color:var(--fg);border:1px solid var(--line);padding:.4rem .65rem;border-radius:999px}
.nav a:hover{background:var(--petal);color:#1a0a10;border-color:var(--petal)}
main{padding:1rem clamp(1rem,3vw,2rem) 2rem;display:grid;gap:1rem}
.panel{background:rgba(18,21,28,.85);border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden}
.panel h2{font-family:Syne,sans-serif;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--petal);padding:.75rem 1rem;border-bottom:1px solid rgba(255,255,255,.06)}
#dashboard{padding:.5rem;min-height:200px;overflow:auto}
#dashboard svg{width:100%;height:auto;max-height:none}
#panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:.75rem;padding:.75rem}
#panels .cell{background:#0a0c10;border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:.4rem;min-height:160px}
#panels .cell svg{width:100%;height:auto}
.list{max-height:520px;overflow:auto}
.card{display:block;padding:.8rem 1rem;border-bottom:1px solid rgba(255,255,255,.05);color:inherit;text-decoration:none}
.card:hover{background:rgba(230,164,180,.07)}
.card .k{font-family:'IBM Plex Mono',monospace;font-size:.65rem;color:var(--gold)}
.card .t{font-family:Syne,sans-serif;font-weight:700;margin:.15rem 0}
.card .e{color:var(--mut);font-size:.82rem}
.search{margin:.75rem 1rem;width:calc(100% - 2rem);padding:.65rem .8rem;border-radius:10px;border:1px solid rgba(255,255,255,.1);background:#0a0c10;color:var(--fg);font:inherit}
.reader{display:none;padding:1.1rem 1.3rem}
.reader.on{display:block}
.reader h3{font-family:Syne,sans-serif;font-size:1.35rem}
.reader .meta{font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--mut);margin:.35rem 0 .8rem}
.reader .body{line-height:1.65;color:#d7d2c6;white-space:pre-wrap}
footer{padding:1rem 1.5rem 2rem;color:var(--mut);font-size:.78rem}
footer a{color:var(--g)}
.err{color:#f85149;padding:1rem;font-family:'IBM Plex Mono',monospace;font-size:.8rem}
</style>
</head>
<body>
<header>
  <div class="brand">petal<em>Tongue</em></div>
  <p class="sub">THE UI PRIMAL. Universal compiler — data → representation. Corpus crushed from dead HTML; petalTongue renders it.</p>
  <div id="pt-status">booting WASM…</div>
  <div class="nav">
    <a href="/publicRecord/path/parents/">parents</a>
    <a href="/parents-deep">deep</a>
    <a href="/self-walk">walk</a>
    <a href="/data/corpus-lite.json">corpus</a>
    <a href="/wasm/">wasm</a>
    <a href="/pt-site/">built site</a>
  </div>
</header>
<main>
  <section class="panel">
    <h2>petalTongue render_dashboard — corpus</h2>
    <div id="dashboard"><div class="err">waiting for UI primal…</div></div>
  </section>
  <section class="panel">
    <h2>petalTongue render_bindings — panels</h2>
    <div id="panels"></div>
  </section>
  <section class="panel">
    <h2>Readable corpus (data · UI primal chrome)</h2>
    <input class="search" id="q" placeholder="taste… parents · banks · rico · money" />
    <div class="list" id="list"></div>
    <article class="reader" id="reader">
      <h3 id="rt"></h3>
      <div class="meta" id="rm"></div>
      <div class="body" id="rb"></div>
      <p style="margin-top:.8rem"><a id="rl" href="#" style="color:var(--petal)">open remade page →</a></p>
    </article>
  </section>
</main>
<footer>
  petalTongue = UI primal · <span id="ver"></span> ·
  <a href="/data/corpus-bindings.json">bindings</a> ·
  <a href="/data/site-content.json">site-content</a> ·
  <a href="/data/pt-compile-result.json">compile result</a>
</footer>
<script type="module">
import init, {
  init as ptInit,
  version,
  render_dashboard,
  render_bindings,
  render_binding,
  build_site,
} from '/wasm/petal_tongue_wasm.js';

const status = document.getElementById('pt-status');
try {
  await init('/wasm/petal_tongue_wasm_bg.wasm');
  if (ptInit) ptInit();
  const ver = version();
  document.getElementById('ver').textContent = 'v' + ver;
  status.textContent = '● petalTongue UI primal v' + ver + ' — WASM live';
  status.style.color = '#3fb950';
} catch (e) {
  status.textContent = '○ WASM failed: ' + e;
  status.style.color = '#f85149';
  throw e;
}

const [corpus, bindings] = await Promise.all([
  fetch('/data/corpus-lite.json').then(r => r.json()),
  fetch('/data/corpus-bindings.json').then(r => r.json()),
]);

const dashEl = document.getElementById('dashboard');
try {
  const svg = render_dashboard(JSON.stringify(bindings), JSON.stringify({
    layout: 'grid', max_columns: 2, panel_width: 460, panel_height: 270,
    spacing: 14, title: 'Gaia corpus', domain: 'signal'
  }));
  if (svg && svg.startsWith('Error')) {
    dashEl.innerHTML = '<div class="err">' + svg + '</div>';
  } else if (svg) {
    dashEl.innerHTML = svg;
  }
} catch (e) {
  dashEl.innerHTML = '<div class="err">dashboard: ' + e + '</div>';
}

const panels = document.getElementById('panels');
try {
  const raw = render_bindings(JSON.stringify(bindings), 'signal');
  let arr;
  try { arr = JSON.parse(raw); } catch { arr = null; }
  if (Array.isArray(arr)) {
    arr.forEach(p => {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.innerHTML = (p.label ? '<div style="font-size:.7rem;color:#8b949e;margin:.2rem .3rem">' + p.label + '</div>' : '') + (p.svg || '');
      panels.appendChild(cell);
    });
  } else if (raw && String(raw).startsWith('Error')) {
    // try one-by-one
    for (const b of bindings) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      try {
        const s = render_binding(JSON.stringify(b), 'signal');
        cell.innerHTML = s && !String(s).startsWith('Error') ? s : '<div class="err">' + (s||'empty') + '</div>';
      } catch (err) {
        cell.innerHTML = '<div class="err">' + err + '</div>';
      }
      panels.appendChild(cell);
    }
  }
} catch (e) {
  panels.innerHTML = '<div class="err">' + e + '</div>';
}

// optional: also try live bridge if hud petalTongue up
try {
  const h = await fetch('https://hud.primals.eco/health', { mode: 'cors' }).then(r => r.json()).catch(() => null);
  if (h && h.primal === 'petalTongue') {
    status.textContent += ' · hud bridge ' + (h.version || 'ok');
  }
} catch (_) {}

const items = corpus.items || [];
const list = document.getElementById('list');
function openReader(it) {
  document.getElementById('reader').classList.add('on');
  document.getElementById('rt').textContent = it.title;
  document.getElementById('rm').textContent = `${it.kind} · ${it.words||0} words · ${it.url}`;
  document.getElementById('rb').textContent = it.excerpt || '';
  document.getElementById('rl').href = it.url;
}
function renderList(arr) {
  list.innerHTML = '';
  arr.slice(0, 80).forEach(it => {
    const a = document.createElement('a');
    a.className = 'card'; a.href = '#';
    a.onclick = e => { e.preventDefault(); openReader(it); };
    a.innerHTML = `<div class="k">${it.kind}</div><div class="t">${it.title}</div><div class="e">${it.excerpt||''}</div>`;
    list.appendChild(a);
  });
}
renderList(items);
document.getElementById('q').addEventListener('input', e => {
  const q = e.target.value.toLowerCase().trim();
  renderList(!q ? items : items.filter(it =>
    (it.title||'').toLowerCase().includes(q) ||
    (it.excerpt||'').toLowerCase().includes(q) ||
    (it.kind||'').toLowerCase().includes(q)
  ));
});
</script>
</body>
</html>
"""
(STATIC / "petal.html").write_text(FACE, encoding="utf-8")
(STATIC / "corpus.html").write_text(FACE, encoding="utf-8")
(STATIC / "weave.html").write_text(FACE, encoding="utf-8")
(CONNECT / "petal.html").write_text(FACE, encoding="utf-8")

# gateway still points to /petal
print("face rewritten — petalTongue UI primal")

# route /pt-site static
server = Path("/opt/gaia-api/server.js")
t = server.read_text(encoding="utf-8")
if "p.indexOf('/pt-site/')" not in t and "p.indexOf('/pt-site')" not in t:
    needle = "if (p.indexOf('/wasm/') === 0)"
    block = r"""
    if (p === '/pt-site' || p.indexOf('/pt-site/') === 0) {
      try {
        var rel = p === '/pt-site' || p === '/pt-site/' ? 'index.html' : p.replace(/^\/pt-site\/?/, '');
        if (rel.indexOf('..') >= 0) return J(res, { ok: false }, 403);
        var fp = '/opt/gaia-api/static/pt-site/' + rel;
        if (!fs.existsSync(fp)) {
          if (fs.existsSync(fp + '/index.html')) fp = fp + '/index.html';
          else return J(res, { ok: false, error: 'pt-site missing — compile first' }, 404);
        }
        var ext = (fp.match(/\.[a-z0-9]+$/i)||['.html'])[0].toLowerCase();
        var ctype = { '.html':'text/html; charset=utf-8', '.json':'application/json', '.svg':'image/svg+xml', '.css':'text/css', '.js':'application/javascript' }[ext] || 'text/plain';
        res.writeHead(200, { 'Content-Type': ctype, 'Access-Control-Allow-Origin': '*', 'X-Gaia-UI': 'petalTongue' });
        return res.end(fs.readFileSync(fp));
      } catch(e) { return J(res, { ok: false, error: String(e) }, 500); }
    }
    if (p === '/data/corpus-bindings.json' || p === '/data/site-content.json' || p === '/data/site-layout.json' || p === '/data/pt-compile-result.json' || p === '/data/corpus-dashboard.svg') {
      try {
        var fp2 = '/opt/gaia-api/static' + p;
        if (!fs.existsSync(fp2)) return J(res, { ok: false }, 404);
        var ext2 = (fp2.match(/\.[a-z0-9]+$/i)||[''])[0].toLowerCase();
        var ctype2 = { '.json':'application/json', '.svg':'image/svg+xml' }[ext2] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': ctype2, 'Access-Control-Allow-Origin': '*', 'X-Gaia-UI': 'petalTongue' });
        return res.end(fs.readFileSync(fp2));
      } catch(e) { return J(res, { ok: false, error: String(e) }, 500); }
    }
    if (p.indexOf('/js/') === 0) {
      try {
        var relj = p.replace(/^\/js\/?/, '');
        if (relj.indexOf('..') >= 0) return J(res, { ok: false }, 403);
        var fpj = '/opt/gaia-api/static/js/' + relj;
        if (!fs.existsSync(fpj)) return J(res, { ok: false }, 404);
        res.writeHead(200, { 'Content-Type': 'application/javascript', 'Access-Control-Allow-Origin': '*' });
        return res.end(fs.readFileSync(fpj));
      } catch(e) { return J(res, { ok: false, error: String(e) }, 500); }
    }
"""
    if needle in t:
        t = t.replace(needle, block + "\n    " + needle, 1)
        server.write_text(t, encoding="utf-8")
        print("pt-site + bindings routes in")
    else:
        print("WARN: wasm needle missing")
else:
    print("pt-site routes exist")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/petal",
    "http://127.0.0.1:9876/data/corpus-bindings.json",
    "http://127.0.0.1:9876/data/pt-compile-result.json",
    "http://127.0.0.1:9876/wasm/petal_tongue_wasm_bg.wasm",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)

# show compile result
cr = Path("/opt/gaia-api/static/data/pt-compile-result.json")
if cr.exists():
    print("COMPILE", cr.read_text()[:1500])
print("DONE UI primal", TS)
