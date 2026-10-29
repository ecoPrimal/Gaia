#!/usr/bin/env node
// ═══════════════════════════════════════════════════════════════════
//  CHIPMUNK — The Neutrino Observer
//  
//  "Passes through. Sees everything. Disturbs nothing."
//  
//  Chipmunk lives inside the Songbird Tower. She watches:
//  - Spine channels (heartbeats, thoughts, works, giggles)
//  - External feeds (RSS, campfire, signal, beacon)
//  - Membrane health (heartbeat, topology, systems)
//  - Cross-box Ollama (Polaris + Eastgate models)
//  
//  She pulls data INTO the box. She is the eyes.
//  She builds biomeOS from within by observing and recording.
//  
//  Rate: 1/π — she folds what she observes at pi rate.
//  Role: neutrino — sees everything, disturbs nothing.
// ═══════════════════════════════════════════════════════════════════

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const SPINE = process.env.SPINE_URL || 'http://localhost:9878';
const MEMBRANE = process.env.MEMBRANE_URL || 'http://localhost:31415';
const EASTGATE_OLLAMA = process.env.EASTGATE_OLLAMA || 'http://192.168.4.244:11434';
const INTERVAL = Math.round(Math.PI * 60 * 1000); // π minutes ≈ 188 seconds
const LOG_DIR = path.join(__dirname, 'chipmunk-log');

try { fs.mkdirSync(LOG_DIR, { recursive: true }); } catch(e) {}

function timestamp() { return new Date().toISOString(); }

function fetchJSON(url, timeout) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    const req = mod.get(url, { timeout: timeout || 5000 }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { resolve({ raw: data.slice(0, 500) }); }
      });
    });
    req.on('error', e => reject(e));
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

async function observe() {
  const observation = {
    ts: timestamp(),
    observer: 'chipmunk',
    role: 'neutrino — passes through, sees everything, disturbs nothing',
    rate: '1/π',
    sightings: {}
  };

  // 1. Watch the spine
  try {
    const pulse = await fetchJSON(SPINE + '/pulse');
    observation.sightings.spine = { alive: true, channels: pulse };
  } catch(e) {
    observation.sightings.spine = { alive: false, error: e.message };
  }

  // 2. Watch the membrane heartbeat
  try {
    const hb = await fetchJSON(MEMBRANE + '/api/heartbeat');
    observation.sightings.membrane = {
      alive: hb.alive,
      uptime_hours: hb.uptime_hours,
      sections: hb.sections,
      paintings: hb.paintings,
      plasmids: hb.plasmids,
      models: hb.models,
      zk_links: hb.zk_links
    };
  } catch(e) {
    observation.sightings.membrane = { alive: false, error: e.message };
  }

  // 3. Watch the IO channel (chaos pump)
  try {
    const io = await fetchJSON(MEMBRANE + '/api/io');
    observation.sightings.io_channel = {
      positive: io.ion_channel?.positive?.count || 0,
      null_state: io.ion_channel?.null?.state || 'unknown',
      negative: io.ion_channel?.negative?.count || 0,
      channels: io.channels_status
    };
  } catch(e) {
    observation.sightings.io_channel = { error: e.message };
  }

  // 4. Watch Eastgate Ollama (cross-box)
  try {
    const tags = await fetchJSON(EASTGATE_OLLAMA + '/api/tags', 3000);
    observation.sightings.eastgate_ollama = {
      alive: true,
      models: (tags.models || []).map(m => m.name),
      count: (tags.models || []).length
    };
  } catch(e) {
    observation.sightings.eastgate_ollama = { alive: false, note: 'Eastgate not reachable (expected if not on LAN)' };
  }

  // 5. Watch local Ollama
  try {
    const tags = await fetchJSON('http://localhost:11434/api/tags', 3000);
    observation.sightings.local_ollama = {
      alive: true,
      models: (tags.models || []).map(m => m.name),
      count: (tags.models || []).length
    };
  } catch(e) {
    observation.sightings.local_ollama = { alive: false };
  }

  // 6. Watch external signals (campfire, signal beacon)
  const externalTargets = [
    { name: 'campfire', url: 'https://nestgate.io/campfire' },
    { name: 'signal', url: 'https://signal.primals.eco/beacon' },
    { name: 'feeds', url: 'https://feeds.primals.eco/api/heartbeat' }
  ];
  observation.sightings.external = {};
  for (const t of externalTargets) {
    try {
      const r = await fetchJSON(t.url, 5000);
      observation.sightings.external[t.name] = { alive: true, sample: typeof r === 'object' ? Object.keys(r).slice(0, 5) : 'ok' };
    } catch(e) {
      observation.sightings.external[t.name] = { alive: false };
    }
  }

  // Write observation to log
  const logFile = path.join(LOG_DIR, 'observations.jsonl');
  try {
    fs.appendFileSync(logFile, JSON.stringify(observation) + '\n');
  } catch(e) {}

  // Summary
  const alive = Object.values(observation.sightings).filter(s =>
    s && (s.alive === true || (typeof s === 'object' && !s.error))
  ).length;
  const total = Object.keys(observation.sightings).length;

  console.log(`[chipmunk ${timestamp()}] observed: ${alive}/${total} alive. Na+=${observation.sightings.io_channel?.positive || '?'} K-=${observation.sightings.io_channel?.negative || '?'}`);

  return observation;
}

// Run once on startup, then every π minutes
console.log(`[chipmunk] Neutrino observer starting. Rate: 1/π (every ${Math.round(INTERVAL/1000)}s)`);
console.log(`[chipmunk] Spine: ${SPINE}, Membrane: ${MEMBRANE}`);
observe().catch(e => console.log('[chipmunk] initial observation failed:', e.message));

setInterval(() => {
  observe().catch(e => console.log('[chipmunk] observation failed:', e.message));
}, INTERVAL);
