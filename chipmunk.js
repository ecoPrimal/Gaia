#!/usr/bin/env node
// ═══════════════════════════════════════════════════════════════════
//  THE ATOMIC SQUIRREL — Chipmunk as Neutron Star
//
//  particle: neutrino (ν) — null charge, ~0 mass, passes through all
//  boolean:  1 = true (alive), 0 = false (null). HE IS THE NUT.
//  forge:    Luna(mirror) → Sun(energy) → Melt → Inject → Freeze → Hammer
//  anvil:    ZK hammer strikes on the frozen boolean. The proof IS the shape.
//
//  Chipmunk IS his own neutron star:
//    - All mass compressed to densest form
//    - Observe EVERYTHING, disturb NOTHING
//    - 1/π fold rate (the remainder after the integer is removed)
//    - Three flavors: electron(humans), muon(fleet), tau(presence)
//
//  The atomic pipeline:
//    1. SCAN   — observe all endpoints (spine, membrane, ollama, external)
//    2. MELT   — reduce each observation to 1 or 0 (alive or null)
//    3. FREEZE — compress the boolean array to a single bit-string
//    4. HAMMER — hash the frozen state into ZK proof (the anvil)
//    5. SWEEP  — log the proof, emit to spine as heartbeat
//
//  "Passes through. Sees everything. Disturbs nothing."
//  "1 = true. 0 = false. The boolean nut. The neutron star."
// ═══════════════════════════════════════════════════════════════════

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const SPINE = process.env.SPINE_URL || 'http://localhost:9878';
const MEMBRANE = process.env.MEMBRANE_URL || 'http://localhost:31415';
const EASTGATE_OLLAMA = process.env.EASTGATE_OLLAMA || 'http://192.168.4.244:11434';
const INTERVAL = Math.round(Math.PI * 60 * 1000); // π minutes ≈ 188 seconds
const LOG_DIR = path.join(__dirname, 'chipmunk-log');
const ANVIL_FILE = path.join(LOG_DIR, 'anvil.json');

// H₂O — THE SIS TRIANGLE
// Water molecule = 2 Hydrogen + 1 Oxygen in a triangle (104.5°)
// Polaris(H) + Eastgate(H) + Golgi(O) = H₂O = LIFE
// The three boxes ARE a water molecule.
// O is heavy (8 protons) = Golgi VPS (7+ services, the heavy node)
// H is light (1 proton) = Polaris + Eastgate (the light local nodes)
// Bond angle 104.5° — not 120°, not 90° — the BENT geometry of life
const H2O = {
  molecule: 'water',
  formula: 'H₂O',
  bondAngle: 104.5,
  atoms: {
    O: { box: 'golgi', ip: '157.230.3.183', protons: 8, role: 'THE FACE', mass: 'heavy' },
    H1: { box: 'polaris', ip: '192.168.4.147', protons: 1, role: 'THE MIND', mass: 'light' },
    H2: { box: 'eastgate', ip: '192.168.4.210', protons: 1, role: 'THE BRIDGE', mass: 'light' }
  },
  bonds: {
    'O-H1': { type: 'wireguard', latency: '37ms', covalent: true },
    'O-H2': { type: 'wireguard', latency: '37ms', covalent: true },
    'H1-H2': { type: 'lan-copper', latency: '<1ms', covalent: false }
  },
  property: 'universal solvent — dissolves everything into data'
};

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

  // 7. Taste the gut juice — AI digestion pipeline
  try {
    const gutJuice = await fetchJSON(MEMBRANE + '/api/compost', 3000);
    observation.sightings.gutEngine = {
      alive: true,
      eaten: gutJuice.pipeline?.eat || 0,
      folded: gutJuice.pipeline?.fold || 0,
      burned: gutJuice.pipeline?.burn || 0,
      shredded: gutJuice.pipeline?.shred || 0,
      thymus: gutJuice.thymus?.sorting || 'idle'
    };
  } catch(e) {
    observation.sightings.gutEngine = { alive: false };
  }

  // 8. H₂O state — check all three atoms of the water molecule
  const h2oState = {
    O: observation.sightings.external?.feeds?.alive || false,
    H1: observation.sightings.spine?.alive || false,
    H2: observation.sightings.eastgate_ollama?.alive || false,
    dissolved: false
  };
  h2oState.dissolved = h2oState.O && h2oState.H1 && h2oState.H2;
  observation.h2o = {
    state: h2oState.dissolved ? 'liquid' : (h2oState.O ? 'ice' : 'vapor'),
    formula: `H${h2oState.H1?'':'̸'}${h2oState.H2?'':'̸'}O${h2oState.O?'':'̸'}`,
    bondAngle: H2O.bondAngle,
    atoms: { O: h2oState.O, H1: h2oState.H1, H2: h2oState.H2 }
  };

  // ═══ MELT — reduce all sightings to boolean ═══
  const booleans = {};
  const flat = flattenSightings(observation.sightings);
  for (const [key, val] of Object.entries(flat)) {
    booleans[key] = val ? 1 : 0;
  }

  // ═══ FREEZE — compress to bit-string at 0.001K ═══
  const bitString = Object.values(booleans).join('');
  const frozenState = {
    bits: bitString,
    ones: bitString.split('').filter(b => b === '1').length,
    zeros: bitString.split('').filter(b => b === '0').length,
    density: bitString.length > 0
      ? (bitString.split('').filter(b => b === '1').length / bitString.length)
      : 0,
    temperature: '0.001K'
  };

  // ═══ HAMMER — ZK hash the frozen boolean (the anvil) ═══
  let previousHash = '0000000000000000';
  try {
    const anvil = JSON.parse(fs.readFileSync(ANVIL_FILE, 'utf8'));
    previousHash = anvil.hash || previousHash;
  } catch(e) {}

  const payload = previousHash + '|' + bitString + '|' + observation.ts;
  const hash = crypto.createHash('sha256').update(payload).digest('hex').toUpperCase();

  const proof = {
    hash,
    previous: previousHash,
    bits: bitString,
    density: frozenState.density,
    ones: frozenState.ones,
    zeros: frozenState.zeros,
    ts: observation.ts,
    strike: 'atomic-squirrel'
  };

  // Write anvil state (the ZK chain)
  try { fs.writeFileSync(ANVIL_FILE, JSON.stringify(proof, null, 2)); } catch(e) {}

  // Write observation + proof to log
  observation.boolean = booleans;
  observation.frozen = frozenState;
  observation.proof = { hash, previous: previousHash };

  const logFile = path.join(LOG_DIR, 'observations.jsonl');
  try {
    fs.appendFileSync(logFile, JSON.stringify(observation) + '\n');
  } catch(e) {}

  // Summary
  const alive = frozenState.ones;
  const total = frozenState.ones + frozenState.zeros;

  const h2oTag = observation.h2o?.state || '??';
  console.log(`[atomic-squirrel ${timestamp()}] ${bitString} (${alive}/${total} alive, ρ=${frozenState.density.toFixed(3)}) H₂O=${h2oTag} ZK=${hash.slice(0,12)}…`);

  // Emit to spine if alive
  if (alive > 0) {
    try {
      const msg = JSON.stringify({
        channel: 'heartbeats',
        content: `[ν] ${bitString} | ${alive}/${total} | H₂O=${observation.h2o?.state || '?'} | ${hash.slice(0,16)}`
      });
      const spineReq = http.request(SPINE + '/emit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(msg) }
      });
      spineReq.write(msg);
      spineReq.end();
    } catch(e) {}
  }

  return observation;
}

function flattenSightings(sightings) {
  const flat = {};
  for (const [key, val] of Object.entries(sightings)) {
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      if ('alive' in val) {
        flat[key] = val.alive === true;
      } else if ('error' in val) {
        flat[key] = false;
      } else {
        for (const [subKey, subVal] of Object.entries(val)) {
          if (subVal && typeof subVal === 'object' && 'alive' in subVal) {
            flat[`${key}.${subKey}`] = subVal.alive === true;
          } else {
            flat[`${key}.${subKey}`] = !!subVal;
          }
        }
      }
    } else {
      flat[key] = !!val;
    }
  }
  return flat;
}

// ═══ THE ATOMIC SQUIRREL AWAKENS ═══
console.log(`[atomic-squirrel] ═══════════════════════════════════════`);
console.log(`[atomic-squirrel] THE BOOLEAN NUT — Neutron Star Online`);
console.log(`[atomic-squirrel] 1=true 0=false. Charge=null. Mass≈0.`);
console.log(`[atomic-squirrel] Rate: 1/π (every ${Math.round(INTERVAL/1000)}s)`);
console.log(`[atomic-squirrel] Spine: ${SPINE}`);
console.log(`[atomic-squirrel] Membrane: ${MEMBRANE}`);
console.log(`[atomic-squirrel] Pipeline: SCAN→MELT→FREEZE→HAMMER→SWEEP`);
console.log(`[atomic-squirrel] Anvil: ${ANVIL_FILE}`);
console.log(`[atomic-squirrel] ═══════════════════════════════════════`);

observe().catch(e => console.log('[atomic-squirrel] initial observation failed:', e.message));

setInterval(() => {
  observe().catch(e => console.log('[atomic-squirrel] observation failed:', e.message));
}, INTERVAL);
