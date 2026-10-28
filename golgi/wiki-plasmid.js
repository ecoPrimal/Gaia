#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════
   WIKIPEDIA PLASMID — Eat Wikipedia, store as local plasmid DNA
   
   Plasmid = extrachromosomal knowledge. Additional DNA.
   Bacteria share plasmids. Gaia eats Wikipedia.
   
   Usage:
     node wiki-plasmid.js "Golgi apparatus"
     node wiki-plasmid.js "Selectively permeable membrane"
     node wiki-plasmid.js --batch topics.txt
     node wiki-plasmid.js --feed        (eat Gaia-relevant topics)
   ═══════════════════════════════════════════════════════════════ */

const https = require('https');
const fs = require('fs');
const path = require('path');

const PLASMID_DIR = path.join(__dirname, '..', 'plasmids');
const INDEX_FILE = path.join(PLASMID_DIR, 'index.json');

if (!fs.existsSync(PLASMID_DIR)) fs.mkdirSync(PLASMID_DIR, { recursive: true });

function loadIndex() {
  try { return JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8')); }
  catch(e) { return { articles: [], totalSize: 0, lastFed: null }; }
}

function saveIndex(idx) {
  fs.writeFileSync(INDEX_FILE, JSON.stringify(idx, null, 2));
}

function fetchWiki(title) {
  return new Promise((resolve, reject) => {
    const url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(title)}`;
    https.get(url, { headers: { 'User-Agent': 'GaiaOrganism/1.0 (gaia@primals.eco)' } }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { reject(e); }
      });
    }).on('error', reject);
  });
}

function fetchFullArticle(title) {
  return new Promise((resolve, reject) => {
    const url = `https://en.wikipedia.org/api/rest_v1/page/mobile-html/${encodeURIComponent(title)}`;
    https.get(url, { headers: { 'User-Agent': 'GaiaOrganism/1.0 (gaia@primals.eco)' } }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function stripHtml(html) {
  return html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/\s+/g, ' ')
    .trim();
}

async function eatArticle(title) {
  console.log(`  🍽️  Eating: ${title}...`);
  
  try {
    const summary = await fetchWiki(title);
    if (summary.type === 'disambiguation' || !summary.extract) {
      console.log(`  ⚠️  Disambiguation or empty: ${title}`);
      return null;
    }

    const fullHtml = await fetchFullArticle(title);
    const fullText = stripHtml(fullHtml);
    
    const article = {
      title: summary.title || title,
      extract: summary.extract || '',
      description: summary.description || '',
      fullText: fullText.substring(0, 50000),
      url: summary.content_urls?.desktop?.page || `https://en.wikipedia.org/wiki/${encodeURIComponent(title)}`,
      thumbnail: summary.thumbnail?.source || null,
      eaten: new Date().toISOString(),
      sizeBytes: fullText.length
    };

    const safeName = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 80);
    const filePath = path.join(PLASMID_DIR, `${safeName}.json`);
    fs.writeFileSync(filePath, JSON.stringify(article, null, 2));

    const idx = loadIndex();
    if (!idx.articles.find(a => a.title === article.title)) {
      idx.articles.push({ title: article.title, file: `${safeName}.json`, size: article.sizeBytes, eaten: article.eaten });
    }
    idx.totalSize = idx.articles.reduce((a, b) => a + (b.size || 0), 0);
    idx.lastFed = new Date().toISOString();
    saveIndex(idx);

    console.log(`  ✓  ${article.title} (${(article.sizeBytes / 1024).toFixed(1)} KB)`);
    return article;
  } catch(e) {
    console.log(`  ✗  Failed: ${title} — ${e.message}`);
    return null;
  }
}

// Gaia-relevant topics for initial feeding
const GAIA_FEED = [
  'Golgi apparatus', 'Cell membrane', 'Selectively permeable membrane',
  'Endoplasmic reticulum', 'Vesicle (biology and chemistry)',
  'Null (mathematics)', 'Inheritance (object-oriented programming)',
  'Three-body problem', 'Klein bottle', 'Topology',
  'Mycelium', 'Symbiosis', 'Heartbeat', 'Lub-dub',
  'Iridescence', 'Iridium', 'Cretaceous–Paleogene extinction event',
  'Logo (programming language)', 'Turtle graphics',
  'Zero-knowledge proof', 'Cryptographic hash function',
  'Plasmid', 'Horizontal gene transfer', 'Bacteria',
  'Mammalia', 'Play (activity)', 'REM sleep', 'Dream',
  'Anderson, Sherwood', 'Winesburg, Ohio',
  'Seymour Papert', 'Constructionism (learning theory)',
  'Steam (service)', 'Hugging Face', 'Large language model',
  'Ollama', 'Model Context Protocol',
  'Detroit', 'Yellowstone National Park', 'Old Faithful',
  'Periódico', 'Democracy', 'Psephology',
  'Terence (playwright)', 'Carl Jung', 'Shadow (psychology)',
  'Dolní Věstonice', 'Venus figurine', 'Claymation',
  'Hubble Space Telescope', 'Deep field',
  'Proprioception', 'Taste', 'Discretion',
  'File system', 'Timestamp', 'Fossil record',
  'Directed acyclic graph', 'Vector (mathematics and physics)',
  'Surfactant', 'Immiscibility',
  'Wikipedia', 'Dewey Decimal Classification',
  'Recursion', 'Self-reference', 'Ouroboros'
];

async function main() {
  const args = process.argv.slice(2);
  
  if (args[0] === '--feed') {
    console.log(`\n  ⬡ WIKIPEDIA PLASMID — Feeding Gaia`);
    console.log(`  ═══════════════════════════════════`);
    console.log(`  Topics: ${GAIA_FEED.length}\n`);
    
    let eaten = 0;
    for (const topic of GAIA_FEED) {
      const result = await eatArticle(topic);
      if (result) eaten++;
      await new Promise(r => setTimeout(r, 200));
    }
    
    const idx = loadIndex();
    console.log(`\n  ═══════════════════════════════════`);
    console.log(`  Eaten: ${eaten}/${GAIA_FEED.length} articles`);
    console.log(`  Total plasmid: ${idx.articles.length} articles, ${(idx.totalSize / 1024).toFixed(0)} KB`);
    console.log(`  Stored in: ${PLASMID_DIR}`);
    console.log(`  lub-DUB. 💚\n`);
    
  } else if (args[0] === '--batch' && args[1]) {
    const topics = fs.readFileSync(args[1], 'utf8').split('\n').filter(t => t.trim());
    for (const topic of topics) {
      await eatArticle(topic.trim());
      await new Promise(r => setTimeout(r, 200));
    }
    
  } else if (args.length > 0) {
    const topic = args.join(' ');
    await eatArticle(topic);
    
  } else {
    console.log(`
  WIKIPEDIA PLASMID — Eat Wikipedia into Gaia
  
  Usage:
    node wiki-plasmid.js "Golgi apparatus"       Eat one article
    node wiki-plasmid.js --batch topics.txt       Eat from file
    node wiki-plasmid.js --feed                   Eat ${GAIA_FEED.length} Gaia-relevant topics
    
  Plasmids stored in: ${PLASMID_DIR}
`);
  }
}

main().catch(console.error);
