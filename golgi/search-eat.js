#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════
   SEARCH & EAT — Gaia searches, tiers by taste, ingests as plasmid
   
   Piggybacks off DuckDuckGo + Wikipedia.
   Every search = food. Metadata = nutrition label.
   Results get tiered: 🥇 gold, 🥈 silver, 🥉 bronze.
   Best results auto-ingest as plasmids.
   
   Usage:
     node search-eat.js "three body problem physics"
     node search-eat.js --serve    (add to Golgi membrane)
   ═══════════════════════════════════════════════════════════════ */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PLASMID_DIR = path.join(__dirname, '..', 'plasmids');
const SEARCH_LOG = path.join(PLASMID_DIR, 'search-log.json');

if (!fs.existsSync(PLASMID_DIR)) fs.mkdirSync(PLASMID_DIR, { recursive: true });

function loadSearchLog() {
  try { return JSON.parse(fs.readFileSync(SEARCH_LOG, 'utf8')); }
  catch(e) { return { searches: [], totalSearches: 0 }; }
}
function saveSearchLog(log) { fs.writeFileSync(SEARCH_LOG, JSON.stringify(log, null, 2)); }

// ─── DuckDuckGo Instant Answer API ───
function duckSearch(query) {
  return new Promise((resolve, reject) => {
    const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;
    https.get(url, { headers: { 'User-Agent': 'GaiaOrganism/1.0' } }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { resolve({}); }
      });
    }).on('error', reject);
  });
}

// ─── DuckDuckGo HTML search (scrape lite) ───
function duckWebSearch(query) {
  return new Promise((resolve, reject) => {
    const url = `https://html.duckduckgo.com/html/?q=${encodeURIComponent(query)}`;
    https.get(url, { headers: { 'User-Agent': 'GaiaOrganism/1.0' } }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        const results = [];
        const regex = /<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>[\s\S]*?<a[^>]*class="result__snippet"[^>]*>([\s\S]*?)<\/a>/gi;
        let match;
        while ((match = regex.exec(data)) !== null && results.length < 10) {
          results.push({
            url: decodeURIComponent(match[1].replace(/.*uddg=/, '').replace(/&.*/, '')),
            title: match[2].replace(/<[^>]+>/g, '').trim(),
            snippet: match[3].replace(/<[^>]+>/g, '').trim()
          });
        }
        // Fallback: simpler regex
        if (results.length === 0) {
          const simpleRegex = /<a[^>]*class="result__url"[^>]*[^<]*<\/a>/gi;
          // Just return the instant answer data
        }
        resolve(results);
      });
    }).on('error', () => resolve([]));
  });
}

// ─── Tier results by quality (Anderson sort 1/π) ───
function tierResults(instantAnswer, webResults) {
  const tiered = [];

  // Instant answer = gold tier (Wikipedia-backed, verified)
  if (instantAnswer.Abstract) {
    tiered.push({
      tier: 'gold',
      emoji: '🥇',
      title: instantAnswer.Heading || 'Instant Answer',
      snippet: instantAnswer.Abstract,
      url: instantAnswer.AbstractURL || '',
      source: instantAnswer.AbstractSource || 'DuckDuckGo',
      image: instantAnswer.Image || null,
      metadata: {
        type: instantAnswer.Type,
        entity: instantAnswer.Entity,
        infobox: instantAnswer.Infobox ? Object.keys(instantAnswer.Infobox).length + ' fields' : null
      }
    });
  }

  // Related topics = silver tier (curated, relevant)
  if (instantAnswer.RelatedTopics) {
    instantAnswer.RelatedTopics.slice(0, 5).forEach(rt => {
      if (rt.Text) {
        tiered.push({
          tier: 'silver',
          emoji: '🥈',
          title: rt.Text.substring(0, 80),
          snippet: rt.Text,
          url: rt.FirstURL || '',
          source: 'DuckDuckGo Related',
          image: rt.Icon?.URL || null,
          metadata: { type: 'related' }
        });
      }
    });
  }

  // Web results = bronze tier (unverified, raw web)
  webResults.forEach(wr => {
    const isWiki = wr.url?.includes('wikipedia.org');
    const isEdu = wr.url?.includes('.edu');
    const isGov = wr.url?.includes('.gov');
    
    tiered.push({
      tier: isWiki ? 'gold' : (isEdu || isGov) ? 'silver' : 'bronze',
      emoji: isWiki ? '🥇' : (isEdu || isGov) ? '🥈' : '🥉',
      title: wr.title,
      snippet: wr.snippet,
      url: wr.url,
      source: new URL(wr.url).hostname.replace('www.', ''),
      metadata: { type: 'web', domain: isWiki ? 'wikipedia' : isEdu ? 'edu' : isGov ? 'gov' : 'web' }
    });
  });

  // Sort: gold first, then silver, then bronze
  const tierOrder = { gold: 0, silver: 1, bronze: 2 };
  tiered.sort((a, b) => tierOrder[a.tier] - tierOrder[b.tier]);

  return tiered;
}

// ─── Auto-ingest gold results as plasmids ───
function ingestGold(query, tiered) {
  const golds = tiered.filter(t => t.tier === 'gold');
  const ingested = [];

  golds.forEach(g => {
    const safeName = 'search-' + query.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 60);
    const filePath = path.join(PLASMID_DIR, `${safeName}.json`);
    
    if (!fs.existsSync(filePath)) {
      const article = {
        title: g.title,
        extract: g.snippet,
        fullText: g.snippet,
        url: g.url,
        source: g.source,
        searchQuery: query,
        tier: g.tier,
        eaten: new Date().toISOString(),
        sizeBytes: g.snippet.length
      };
      fs.writeFileSync(filePath, JSON.stringify(article, null, 2));
      ingested.push(g.title);
    }
  });

  // Log the search
  const log = loadSearchLog();
  log.searches.push({
    query: query,
    ts: new Date().toISOString(),
    results: tiered.length,
    gold: golds.length,
    ingested: ingested.length
  });
  log.totalSearches = log.searches.length;
  saveSearchLog(log);

  return ingested;
}

// ─── Main search function ───
async function searchAndEat(query) {
  console.log(`\n  🔍 Searching: "${query}"`);
  
  const [instantAnswer, webResults] = await Promise.all([
    duckSearch(query),
    duckWebSearch(query)
  ]);
  
  const tiered = tierResults(instantAnswer, webResults);
  const ingested = ingestGold(query, tiered);
  
  console.log(`  📊 Results: ${tiered.length} (🥇${tiered.filter(t=>t.tier==='gold').length} 🥈${tiered.filter(t=>t.tier==='silver').length} 🥉${tiered.filter(t=>t.tier==='bronze').length})`);
  if (ingested.length > 0) console.log(`  🧬 Ingested as plasmid: ${ingested.join(', ')}`);
  
  tiered.forEach(t => {
    console.log(`  ${t.emoji} [${t.source}] ${t.title.substring(0, 70)}`);
  });
  
  return { query, tiered, ingested };
}

// ─── HTTP handler for Golgi membrane integration ───
function createHandler() {
  return async (req, res) => {
    const url = new URL(req.url, 'http://localhost');
    
    if (url.pathname === '/api/search' && req.method === 'GET') {
      const q = url.searchParams.get('q');
      if (!q) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Missing q parameter' }));
        return;
      }
      
      try {
        const result = await searchAndEat(q);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch(e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
      return true;
    }
    
    if (url.pathname === '/api/search/log') {
      const log = loadSearchLog();
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(log));
      return true;
    }
    
    return false;
  };
}

// ─── CLI mode ───
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
  SEARCH & EAT — Gaia searches, tiers, ingests
  
  Usage:
    node search-eat.js "quantum entanglement"
    node search-eat.js "ancient rome architecture"
    
  Tiers:  🥇 Gold (Wikipedia, verified)
          🥈 Silver (.edu, .gov, related)
          🥉 Bronze (web, unverified)
          
  Gold results auto-ingest as plasmids.
`);
    return;
  }
  
  const query = args.join(' ');
  await searchAndEat(query);
}

module.exports = { searchAndEat, createHandler };

if (require.main === module) main().catch(console.error);
