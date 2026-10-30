#!/usr/bin/env python3
"""Discover exact petalTongue WASM DataBinding + DocumentNode shapes, then compile corpus UI."""
import json
import subprocess
from pathlib import Path

STATIC = Path("/opt/gaia-api/static")
DATA = STATIC / "data"
corpus = json.loads((DATA / "corpus-lite.json").read_text())
items = corpus["items"]
kinds = corpus["kinds"]
kind_cats = sorted(kinds.keys(), key=lambda k: -kinds[k])
top = sorted(items, key=lambda x: -(x.get("words") or 0))[:80]

mjs = r'''
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { pathToFileURL } from 'url';
const mod = await import(pathToFileURL('/opt/gaia-api/static/wasm/petal_tongue_wasm.js').href);
const init = mod.default;
const { init: ptInit, version, build_site, render_dashboard, render_bindings, render_binding, render_page_with_layout } = mod;
await init({ module_or_path: readFileSync('/opt/gaia-api/static/wasm/petal_tongue_wasm_bg.wasm') });
if (ptInit) ptInit();
console.log('v', version());

function tryBind(label, shape) {
  try {
    const r = render_binding(JSON.stringify(shape), 'signal');
    const ok = r && !String(r).startsWith('Error') && String(r).includes('<svg');
    console.log(ok ? 'OK' : 'NO', label, (r||'').slice(0, 140).replace(/\n/g,' '));
    if (ok) writeFileSync('/tmp/ok_bind.json', JSON.stringify(shape, null, 2));
    return ok ? r : null;
  } catch (e) {
    console.log('EX', label, String(e).slice(0, 140));
    return null;
  }
}

const cats = ['path','network','analysis','actors','entities','validate'];
const vals = [120,80,60,40,30,20];

const candidates = [
  { id:'k', label:'Kinds', channel_type:'bar', categories:cats, values:vals, unit:'pages' },
  { id:'k', label:'Kinds', channel_type:'Bar', categories:cats, values:vals, unit:'pages' },
  { id:'k', label:'Kinds', channel_type:'bar', unit:'pages', categories:cats, values:vals, x_label:'kind', y_label:'n' },
  { id:'k', label:'Kinds', channel_type:{ type:'bar' }, categories:cats, values:vals, unit:'pages' },
  { id:'k', label:'Kinds', channel_type:'bar', data:{ categories:cats, values:vals }, unit:'pages' },
  // externally tagged
  { Bar: { id:'k', label:'Kinds', categories:cats, values:vals, unit:'pages' } },
  { channel_type: 'bar', Bar: { id:'k', label:'Kinds', categories:cats, values:vals, unit:'pages' } },
  { id:'k', label:'Kinds', unit:'pages', channel_type:'bar', bar:{ categories:cats, values:vals } },
  { id:'g', label:'Words', channel_type:'gauge', value:325065, min:0, max:400000, unit:'words', normal_range:[0,325065], warning_range:[0,0] },
  { id:'d', label:'Share', channel_type:'donut', categories:cats, values:vals, unit:'pages' },
  { id:'t', label:'TS', channel_type:'timeseries', x_label:'i', y_label:'n', unit:'pages', x_values:[0,1,2,3,4,5], y_values:vals },
  { id:'s', label:'SC', channel_type:'scatter', x:vals, y:vals.map(v=>v/2), unit:'u', label_x:'x', label_y:'y' },
  { id:'s', label:'SC', channel_type:'scatter', unit:'u', x:vals, y:vals.map(v=>v/2) },
];

let good = null;
for (const c of candidates) {
  const r = tryBind(JSON.stringify(c).slice(0,80), c);
  if (r) { good = c; break; }
}

// more systematic: channel_type enum strings
if (!good) {
  for (const ct of ['bar','Bar','BAR','bars','histogram','category_bar','BarChart']) {
    const s = { id:'k', label:'Kinds', channel_type:ct, categories:cats, values:vals, unit:'pages' };
    const r = tryBind('ct='+ct, s);
    if (r) { good = s; break; }
  }
}

function tryPage(label, page, nav, layout) {
  try {
    const r = render_page_with_layout(JSON.stringify(page), JSON.stringify(nav), JSON.stringify(layout));
    const ok = r && !String(r).startsWith('Error') && String(r).includes('<');
    console.log(ok ? 'PAGE OK' : 'PAGE NO', label, (r||'').slice(0, 160).replace(/\n/g,' '));
    if (ok) {
      writeFileSync('/tmp/ok_page.json', JSON.stringify(page, null, 2));
      writeFileSync('/tmp/ok_page.html', r);
    }
    return ok;
  } catch (e) {
    console.log('PAGE EX', label, String(e).slice(0, 160));
    return false;
  }
}

const layout = { site_title: 'Gaia', footer: 'petalTongue UI', css: 'body{font-family:sans-serif}' };
const nav = [{ title: 'Home', path: '/' }, { NavLink: { title: 'Home', href: '/' } }];

const pageCands = [
  { Page: { title: 'Home', path: 'index.html', children: [ { Paragraph: { text: 'Hello corpus' } } ] } },
  { Page: { title: 'Home', slug: 'index', body: [ { Paragraph: 'Hello' } ] } },
  { Page: { title: 'Home', path: '/', content: [ { Paragraph: { text: 'Hello' } } ] } },
  { Page: { title: 'Home', blocks: [ { Paragraph: { text: 'Hello' } } ] } },
  { Page: { title: 'Home', children: [ { Paragraph: { text: 'Hello' } } ] } },
  { Page: { title: 'Home', children: [ { Heading: { level: 1, text: 'Corpus' } }, { Paragraph: { text: '438 pages crushed' } } ] } },
  { Page: { title: 'Home', markdown: '# Hi\n\n438 pages' } },
  { Page: { title: 'Home', html: '<p>438 pages</p>' } },
  { Page: { title: 'Home', text: '438 pages' } },
  { Page: { title: 'Home', path: 'index.html', nodes: [ { Paragraph: { text: 'Hi' } } ] } },
  // internally tagged
  { type: 'Page', title: 'Home', children: [{ type: 'Paragraph', text: 'Hi' }] },
  { type: 'Page', title: 'Home', content: 'Hi there' },
];

let pageOk = false;
for (const p of pageCands) {
  if (tryPage(JSON.stringify(p).slice(0,100), p, [{title:'Home',path:'/'}], layout)) { pageOk = true; break; }
}

// build_site shapes
function trySite(label, content) {
  try {
    const r = build_site(JSON.stringify(content), JSON.stringify(layout));
    console.log('SITE', label, (r||'').slice(0, 200).replace(/\n/g,' '));
    if (r && !String(r).startsWith('Error') && !String(r).includes('"error"')) {
      writeFileSync('/tmp/ok_site.json', r.slice(0, 50) === '{' ? r : JSON.stringify({raw:r.slice(0,500)}));
      try {
        const parsed = JSON.parse(r);
        writeFileSync('/opt/gaia-api/static/data/pt-site-meta.json', JSON.stringify({
          file_count: parsed.file_count, total_bytes: parsed.total_bytes,
          files: Object.keys(parsed.files||{}).slice(0,30)
        }));
        const outDir = '/opt/gaia-api/static/pt-site';
        mkdirSync(outDir, { recursive: true });
        let n = 0;
        for (const [rel, html] of Object.entries(parsed.files || {})) {
          const fp = outDir + '/' + rel;
          mkdirSync(fp.split('/').slice(0,-1).join('/') || outDir, { recursive: true });
          writeFileSync(fp, html);
          n++;
        }
        console.log('WROTE', n, 'files');
      } catch(e) { console.log('parse site', e); }
      return true;
    }
    return false;
  } catch (e) {
    console.log('SITE EX', label, String(e).slice(0, 200));
    return false;
  }
}

const para = { Paragraph: { text: 'Dead HTML crushed into corpus. petalTongue is the UI primal.' } };
const homePage = {
  Page: {
    title: 'Cash for Kids 2 — in Gaia',
    path: 'index.html',
    children: [
      { Heading: { level: 1, text: 'Corpus' } },
      para,
      { Paragraph: { text: '438 pages · 325065 words · 5534 weave edges.' } },
    ]
  }
};

for (const content of [
  { pages: [homePage], nav: [{ title:'Home', path:'/' }], search_index: [], entity_registry: {} },
  { pages: [homePage], navigation: [], search_index: [], entity_registry: {} },
  { pages: [homePage] },
  { documents: [homePage] },
  { root: homePage },
  { tree: [homePage] },
  { content: [homePage] },
  { nodes: [homePage] },
  { pages: [ { Page: { title:'Home', path:'index.html', children:[para] } } ], nav_sections: [] },
  { pages: [ { Page: { title:'Home', path:'index.html', children:[para] } } ],
    nav: [ { NavSection: { title: 'Main', links: [ { title:'Home', path:'/' } ] } } ] },
]) {
  if (trySite(JSON.stringify(Object.keys(content)), content)) break;
}

console.log('GOOD_BIND', good ? JSON.stringify(good).slice(0,200) : null);
'''

Path("/opt/gaia-api/static/js/pt_shape_fix.mjs").write_text(mjs, encoding="utf-8")
r = subprocess.run(
    ["node", "/opt/gaia-api/static/js/pt_shape_fix.mjs"],
    capture_output=True,
    text=True,
    cwd="/opt/gaia-api/static",
)
print(r.stdout[-8000:] if r.stdout else "")
print("ERR", (r.stderr or "")[-1500:])

# show ok shapes
for p in ["/tmp/ok_bind.json", "/tmp/ok_page.json", "/tmp/ok_page.html", "/opt/gaia-api/static/data/pt-site-meta.json"]:
    pp = Path(p)
    if pp.exists():
        print("====", p)
        print(pp.read_text()[:1200])
