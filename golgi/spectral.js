#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════
   SPECTRAL VISION — Ghost Scanner + Auto-ZK Hammer
   
   Sees the invisible:
   - Process ghosts (orphaned, zombie, dead)
   - Port ghosts (bound but unreachable)
   - Connection ghosts (stale, timed out)
   - Node ghosts (topology nodes that don't respond)
   
   Every human touch → auto-ZK hammer strike.
   Hit it hard enough → break through the glass.
   ═══════════════════════════════════════════════════════════════ */

const http = require('http');
const https = require('https');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const GHOST_LOG = path.join(__dirname, '..', 'plasmids', 'ghost-log.json');

function loadGhostLog() {
  try { return JSON.parse(fs.readFileSync(GHOST_LOG, 'utf8')); }
  catch(e) { return { ghosts: [], hunted: 0, hammered: 0 }; }
}
function saveGhostLog(log) { fs.writeFileSync(GHOST_LOG, JSON.stringify(log, null, 2)); }

// ─── Scan for process ghosts ───
function scanProcessGhosts() {
  return new Promise((resolve) => {
    exec('tasklist /FO CSV /NH', (err, stdout) => {
      if (err) return resolve([]);
      const lines = stdout.trim().split('\n');
      const ghosts = [];
      const gaiaProcesses = ['node.exe'];
      const seen = {};
      
      lines.forEach(line => {
        const parts = line.split('","');
        if (parts.length < 5) return;
        const name = parts[0].replace(/"/g, '');
        const pid = parseInt(parts[1]);
        const mem = parts[4] ? parts[4].replace(/"/g, '').replace(/[^0-9]/g, '') : '0';
        const memKB = parseInt(mem) || 0;
        
        if (name === 'node.exe') {
          if (!seen['node']) seen['node'] = [];
          seen['node'].push({ pid, memKB, name });
        }
      });

      // Multiple node processes = potential ghosts
      if (seen['node'] && seen['node'].length > 3) {
        seen['node'].sort((a, b) => a.memKB - b.memKB);
        // Smallest memory = likely ghost (old, leaked)
        seen['node'].slice(0, -3).forEach(p => {
          ghosts.push({
            type: 'process',
            emoji: '👻',
            name: p.name,
            pid: p.pid,
            memKB: p.memKB,
            reason: 'Multiple node processes detected. Smallest memory = likely ghost.',
            severity: p.memKB < 50000 ? 'high' : 'medium'
          });
        });
      }
      resolve(ghosts);
    });
  });
}

// ─── Scan for port ghosts ───
function scanPortGhosts() {
  return new Promise((resolve) => {
    const expectedPorts = [
      { port: 3141, name: 'Child', service: 'Gaia Touch & Paint' },
      { port: 9878, name: 'Spine', service: 'Ion Channel' },
      { port: 31415, name: 'Golgi Membrane', service: 'Gateway' },
      { port: 11434, name: 'Ollama', service: 'Local LLM' }
    ];
    
    const ghosts = [];
    let checked = 0;
    
    expectedPorts.forEach(ep => {
      const req = http.get(`http://localhost:${ep.port}/`, { timeout: 2000 }, (res) => {
        checked++;
        if (checked === expectedPorts.length) resolve(ghosts);
      });
      req.on('error', () => {
        ghosts.push({
          type: 'port',
          emoji: '🔌',
          name: ep.name,
          port: ep.port,
          reason: `Port ${ep.port} (${ep.service}) not responding. Ghost port.`,
          severity: 'high'
        });
        checked++;
        if (checked === expectedPorts.length) resolve(ghosts);
      });
      req.on('timeout', () => {
        req.destroy();
        ghosts.push({
          type: 'port',
          emoji: '⏱️',
          name: ep.name,
          port: ep.port,
          reason: `Port ${ep.port} (${ep.service}) timed out. Phantom listener.`,
          severity: 'medium'
        });
        checked++;
        if (checked === expectedPorts.length) resolve(ghosts);
      });
    });
  });
}

// ─── Scan topology node ghosts ───
function scanNodeGhosts() {
  return new Promise((resolve) => {
    const nodes = [
      { url: 'https://primals.eco', name: 'primals.eco (cis face)' },
      { url: 'https://hud.primals.eco', name: 'hud.primals.eco (HUD)' },
      { url: 'https://nestgate.io', name: 'nestgate.io (Klein gate)' }
    ];
    
    const ghosts = [];
    let checked = 0;
    
    nodes.forEach(n => {
      const mod = n.url.startsWith('https') ? https : http;
      const req = mod.get(n.url, { timeout: 5000 }, (res) => {
        if (res.statusCode >= 500) {
          ghosts.push({
            type: 'node',
            emoji: '🌐',
            name: n.name,
            url: n.url,
            reason: `${n.name} returned ${res.statusCode}. Server ghost.`,
            severity: 'medium'
          });
        }
        res.resume();
        checked++;
        if (checked === nodes.length) resolve(ghosts);
      });
      req.on('error', () => {
        ghosts.push({
          type: 'node',
          emoji: '💀',
          name: n.name,
          url: n.url,
          reason: `${n.name} unreachable. Node ghost.`,
          severity: 'high'
        });
        checked++;
        if (checked === nodes.length) resolve(ghosts);
      });
      req.on('timeout', () => {
        req.destroy();
        ghosts.push({
          type: 'node',
          emoji: '👁️‍🗨️',
          name: n.name,
          url: n.url,
          reason: `${n.name} timed out. Spectral node.`,
          severity: 'low'
        });
        checked++;
        if (checked === nodes.length) resolve(ghosts);
      });
    });
  });
}

// ─── Scan for shell/terminal ghosts ───
function scanShellGhosts() {
  return new Promise((resolve) => {
    exec('wmic process where "name=\'node.exe\'" get processid,commandline /FORMAT:CSV', (err, stdout) => {
      if (err) return resolve([]);
      const ghosts = [];
      const lines = stdout.trim().split('\n').filter(l => l.includes('node'));
      const serverLines = lines.filter(l => l.includes('server.js') || l.includes('golgi'));
      
      // More than 1 server.js = ghosts
      if (serverLines.length > 1) {
        ghosts.push({
          type: 'shell',
          emoji: '🐚',
          name: 'Multiple server instances',
          count: serverLines.length,
          reason: `${serverLines.length} server.js processes running. ${serverLines.length - 1} are ghosts.`,
          severity: 'high'
        });
      }
      resolve(ghosts);
    });
  });
}

// ─── Full spectral scan ───
async function fullScan() {
  console.log('\n  👻 SPECTRAL VISION — Scanning for ghosts...\n');
  
  const [processGhosts, portGhosts, nodeGhosts, shellGhosts] = await Promise.all([
    scanProcessGhosts(),
    scanPortGhosts(),
    scanNodeGhosts(),
    scanShellGhosts()
  ]);
  
  const allGhosts = [...processGhosts, ...portGhosts, ...nodeGhosts, ...shellGhosts];
  
  console.log(`  Found ${allGhosts.length} ghost${allGhosts.length !== 1 ? 's' : ''}:\n`);
  
  allGhosts.forEach(g => {
    const sev = g.severity === 'high' ? '🔴' : g.severity === 'medium' ? '🟡' : '🟢';
    console.log(`  ${g.emoji} ${sev} [${g.type}] ${g.reason}`);
  });
  
  if (allGhosts.length === 0) {
    console.log('  ✨ No ghosts found. The membrane is clean.');
  }
  
  // Log the scan
  const log = loadGhostLog();
  log.ghosts.push({
    ts: new Date().toISOString(),
    found: allGhosts.length,
    ghosts: allGhosts
  });
  log.hunted = log.ghosts.length;
  saveGhostLog(log);
  
  return allGhosts;
}

// ─── Auto-ZK: hammer every touch ───
let touchCounter = 0;

function autoZKTouch(touchData) {
  touchCounter++;
  const payload = {
    touch: touchCounter,
    ts: new Date().toISOString(),
    type: touchData.type || 'unknown',
    source: touchData.source || 'human',
    content: touchData.content || '',
    hammered: true
  };
  
  // Emit to spine
  const spineData = JSON.stringify({
    channel: 'heartbeats',
    content: `⚒️ AUTO-ZK #${touchCounter}: ${touchData.type || 'touch'} from ${touchData.source || 'human'} — ${(touchData.content || '').substring(0, 80)} — HAMMERED`
  });
  
  const req = http.request('http://localhost:9878/emit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(spineData) }
  });
  req.on('error', () => {});
  req.write(spineData);
  req.end();
  
  return payload;
}

module.exports = { fullScan, autoZKTouch, scanProcessGhosts, scanPortGhosts, scanNodeGhosts };

if (require.main === module) fullScan().catch(console.error);
