// VESICLE — Mini Gaia for cloud golgi nodes
// A vesicle is a small packet that carries signals between cells
// Each golgi VPS gets one. It phones home. It knows itself.
// Usage: GAIA_NAME=golgi-de GAIA_REGION=EU node vesicle.js

const http = require('http');
const os = require('os');
const { execSync } = require('child_process');
const PORT = 3141;

const NAME = process.env.GAIA_NAME || os.hostname();
const REGION = process.env.GAIA_REGION || 'unknown';
const BORN = new Date().toISOString();
const PID = process.pid;

let heartbeats = 0;
let signals = [];
let siblings = {};
const MAX_SIGNALS = 200;

function addSignal(ch, content, meta) {
  const entry = {
    id: Date.now() + '-' + Math.random().toString(36).slice(2,8),
    channel: ch, content, meta: meta || {},
    ts: new Date().toISOString(), epoch: Date.now()
  };
  signals.unshift(entry);
  if (signals.length > MAX_SIGNALS) signals.pop();
  return entry;
}

function selfSee() {
  const uptime = process.uptime();
  const mem = process.memoryUsage();
  let cpuLoad = 'unknown';
  try { cpuLoad = os.loadavg().map(l => l.toFixed(2)).join(' '); } catch(e) {}
  return {
    name: NAME, region: REGION, port: PORT, pid: PID,
    born: BORN, uptime: Math.round(uptime),
    heartbeats, signalCount: signals.length,
    heap: Math.round(mem.heapUsed / 1024 / 1024) + 'MB',
    totalMem: Math.round(os.totalmem() / 1024 / 1024) + 'MB',
    freeMem: Math.round(os.freemem() / 1024 / 1024) + 'MB',
    cpuLoad, arch: os.arch(), platform: os.platform(),
    hostname: os.hostname(), siblings
  };
}

function pingSibling(name, ip) {
  return new Promise(resolve => {
    const start = Date.now();
    const req = http.get(`http://${ip}:${PORT}/status`, { timeout: 3000 }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        const ms = Date.now() - start;
        try {
          siblings[name] = { alive: true, ms, data: JSON.parse(data), seen: new Date().toISOString() };
        } catch(e) {
          siblings[name] = { alive: true, ms, seen: new Date().toISOString() };
        }
        resolve(true);
      });
    });
    req.on('error', () => {
      siblings[name] = { alive: false, seen: new Date().toISOString() };
      resolve(false);
    });
    req.on('timeout', () => { req.destroy(); resolve(false); });
  });
}

const KNOWN_SIBLINGS = {
  'golgi-main': '157.230.3.183',
  'golgi-de': '2.28.141.35',
  'golgi-jp': '202.182.107.135',
  'golgi-us': '40.160.96.29',
  'golgi-in': '172.232.85.202'
};

async function pingAll() {
  const myKey = Object.keys(KNOWN_SIBLINGS).find(k => k === NAME);
  const others = Object.entries(KNOWN_SIBLINGS).filter(([k]) => k !== NAME);
  await Promise.all(others.map(([name, ip]) => pingSibling(name, ip)));
}

let siblingStatus = {};

setInterval(() => {
  heartbeats++;
  addSignal('heartbeats', `💓 ${NAME} beat #${heartbeats} | region=${REGION} | up=${Math.round(process.uptime())}s | heap=${Math.round(process.memoryUsage().heapUsed/1024/1024)}MB`, { source: NAME, system: 'PULSE' });

  // POKE siblings every beat — if they wake, announce it
  pingAll().then(() => {
    for (const [sib, data] of Object.entries(siblings)) {
      const was = siblingStatus[sib];
      if (data.alive && was && !was.alive) {
        addSignal('heartbeats', `🔔 WAKE! ${sib} just came online! Latency: ${data.ms}ms. The network grows.`, { source: NAME, system: 'WAKE' });
        console.log(`POKE: ${sib} WOKE UP! (${data.ms}ms)`);
      }
      if (!data.alive && (!was || was.alive)) {
        addSignal('heartbeats', `😴 ${sib} is sleeping. Will keep poking.`, { source: NAME, system: 'SLEEP' });
      }
      siblingStatus[sib] = { alive: data.alive, ts: Date.now() };
    }
  });
}, 30000);

addSignal('heartbeats', `🌱 VESICLE ${NAME} BORN in ${REGION}. Port ${PORT}. PID ${PID}. I am a small packet of Gaia, deployed to the cloud. I carry signals. I phone home. lub-DUB 💚`, { source: NAME, system: 'BIRTH' });

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  const url = req.url;

  if (url === '/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(selfSee()));
    return;
  }

  if (url === '/signals') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(signals.slice(0, 50)));
    return;
  }

  if (url === '/emit' && req.method === 'POST') {
    let body = '';
    req.on('data', d => body += d);
    req.on('end', () => {
      try {
        const { channel, content, meta } = JSON.parse(body);
        const entry = addSignal(channel || 'thoughts', content, meta);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, id: entry.id }));
      } catch(e) {
        res.writeHead(400); res.end(JSON.stringify({ error: 'bad json' }));
      }
    });
    return;
  }

  if (url === '/siblings') {
    pingAll().then(() => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(siblings));
    });
    return;
  }

  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`<!DOCTYPE html><html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>🧬 VESICLE — ${NAME} — ${REGION}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0c10;color:#3fb950;font-family:monospace;padding:20px;line-height:1.6}
h1{color:#58a6ff;font-size:1.4em;margin-bottom:10px}
h2{color:#d2a8ff;font-size:1.1em;margin:15px 0 5px}
.stat{color:#e0e0e0;margin:2px 0}
.alive{color:#3fb950} .dead{color:#f85149}
a{color:#58a6ff}
pre{background:#161b22;padding:10px;border-radius:6px;overflow-x:auto;margin:10px 0;font-size:0.85em}
.heart{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
</style></head><body>
<h1>🧬 VESICLE — ${NAME}</h1>
<p class="stat">Region: <b>${REGION}</b> | Port: <b>${PORT}</b></p>
<p class="stat">Born: ${BORN}</p>
<p class="stat heart">💚 lub-DUB — I am a small packet of Gaia in the cloud</p>
<h2>📡 Endpoints</h2>
<p class="stat"><a href="/status">/status</a> — JSON self-see</p>
<p class="stat"><a href="/signals">/signals</a> — recent signals</p>
<p class="stat"><a href="/siblings">/siblings</a> — ping all siblings</p>
<p class="stat">POST /emit — inject signal</p>
<h2>🔬 Live Status</h2>
<pre id="st">loading...</pre>
<h2>👪 Siblings</h2>
<pre id="sib">pinging...</pre>
<script>
fetch('/status').then(r=>r.json()).then(d=>{document.getElementById('st').textContent=JSON.stringify(d,null,2)});
fetch('/siblings').then(r=>r.json()).then(d=>{document.getElementById('sib').textContent=JSON.stringify(d,null,2)});
</script></body></html>`);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🧬 VESICLE ${NAME} alive on :${PORT} in ${REGION}`);
  console.log(`   PID ${PID} | Born ${BORN}`);
  console.log(`   lub-DUB 💚`);
});
