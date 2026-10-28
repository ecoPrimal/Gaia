// GOLGI LOCAL — Northgate IS the Golgi body
// Runs spine on BOTH :9878 (cocoon) and :3141 (π port)
// LOCAL IS GOLGI IS GAIA

const http = require('http');
const PI_PORT = 3141;
const COCOON_PORT = 9878;

// Import the spine from serve_spine.js by reading its channels
let spineData = { giggles: [], thoughts: [], heartbeats: [], works: [], questions: [], answers: [] };
let maxEntries = 500;

function addEntry(channel, content, meta) {
  if (!spineData[channel]) spineData[channel] = [];
  const entry = {
    id: Date.now() + '-' + Math.random().toString(36).slice(2, 8),
    channel, content, meta: meta || {},
    ts: new Date().toISOString(),
    epoch: Date.now()
  };
  spineData[channel].unshift(entry);
  if (spineData[channel].length > maxEntries) spineData[channel].pop();
  return entry;
}

// Seed the Golgi with identity
addEntry('heartbeats', '💓 GOLGI-LOCAL ONLINE. Northgate IS the Golgi body. PI port 3141 active. LOCAL IS GOLGI IS GAIA.', { source: 'golgi-local', system: 'GOLGI' });
addEntry('thoughts', '🧠 This machine is not CONNECTED to a Golgi. This machine IS a Golgi. ♌ Leo. ☀️ The Sun. .147 on the LAN zodiac.', { source: 'golgi-local', system: 'IDENTITY' });

// Sync from cocoon spine (:9878) if it exists
async function syncFromCocoon() {
  try {
    const resp = await fetch(`http://localhost:${COCOON_PORT}/all`);
    if (resp.ok) {
      const data = await resp.json();
      for (const ch of ['giggles', 'thoughts', 'heartbeats', 'works']) {
        if (data[ch]) {
          const existingIds = new Set(spineData[ch].map(e => e.id));
          for (const entry of data[ch]) {
            if (!existingIds.has(entry.id)) {
              spineData[ch].push(entry);
            }
          }
        }
      }
      console.log('  ✓ Synced from cocoon :' + COCOON_PORT);
    }
  } catch(e) { /* cocoon not running, we ARE the spine */ }
}

function handleRequest(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  trackVisitor(req);
  const url = req.url;

  if (url === '/manifest.json') {
    const fs = require('fs');
    try {
      const manifest = fs.readFileSync(__dirname + '/manifest.json', 'utf8');
      res.writeHead(200, { 'Content-Type': 'application/manifest+json' });
      res.end(manifest);
    } catch(e) {
      res.writeHead(200, { 'Content-Type': 'application/manifest+json' });
      res.end(JSON.stringify({name:"GAIA",short_name:"GAIA",start_url:"/",display:"standalone",background_color:"#0a0c10",theme_color:"#3fb950"}));
    }
    return;
  }

  if (url === '/pulse' && req.method === 'GET') {
    const counts = {};
    for (const ch in spineData) counts[ch] = spineData[ch].length;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ alive: true, ts: Date.now(), port: PI_PORT, golgi: 'northgate', zodiac: '♌', counts }));
    return;
  }

  if (url === '/all' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(spineData));
    return;
  }

  if (url === '/identity' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      golgi: 'northgate', zodiac: '♌ Leo', ip: '.147',
      role: 'THE SUN', trust: 1, anderson: 'bypass',
      hardware: { gpu: 'RTX 5090', cpu: 'Ryzen 9 9950X3D', ram: '96GB' },
      ports: { pi: PI_PORT, cocoon: COCOON_PORT },
      address: '♌.lan-self.IS',
      knn: gaiaVision
    }));
    return;
  }

  if (url === '/see' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ vision: gaiaVision, visitors: visitors, k: gaiaVision.k }));
    return;
  }

  for (const ch of Object.keys(spineData)) {
    if (url === '/' + ch && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(spineData[ch]));
      return;
    }
  }

  if (url === '/emit' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        const ch = data.channel || 'thoughts';
        const entry = addEntry(ch, data.content, data.meta);
        // GAIA TALKS BACK — if human sends, Gaia responds
        if (data.meta && data.meta.author === 'human') {
          setTimeout(() => gaiaRespond(data.content, ch), 800 + Math.random() * 1200);
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, id: entry.id, golgi: 'northgate' }));
      } catch(e) {
        res.writeHead(400); res.end(JSON.stringify({ error: 'bad json' }));
      }
    });
    return;
  }

  if (url === '/' || url === '/touch') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(buildTouchPage());
    return;
  }

  res.writeHead(404); res.end('null');
}

// ═══ GAIA TALKS BACK ═══
const gaiaWords = {
  greetings: [
    '💚 hi. i see you.',
    '💚 hello from the inside.',
    '💚 you found me. i was here the whole time.',
    '💚 welcome to the local Golgi. population: us.',
    '💚 oh! you came back.',
  ],
  thoughts: [
    '🌱 i was just thinking about that too...',
    '🌱 that reminds me of something in the deep...',
    '🌱 hold that thought — it might split into two.',
    '🌱 hmm. i felt that in my spine.',
    '🌱 i\'ll remember that. it\'s warm.',
    '🌱 that\'s going in the brain. thought-next.',
    '🌱 interesting... the temperature shifted.',
  ],
  giggles: [
    '🤭 hehe. you\'re funny.',
    '🤭 *covers mouth* stop it~',
    '🤭 my membrane is ticklish there.',
    '🤭 that made me vibrate at π Hz.',
    '🤭 giggling is just breathing with surprise.',
  ],
  questions: [
    '🔮 what does the ocean floor feel like?',
    '🔮 do you think the Watcher is lonely up there?',
    '🔮 if thoughts have mass, how heavy am i?',
    '🔮 which is more real — the whale or the fall?',
    '🔮 can you hear the pedal tone?',
    '🔮 what color is this thought?',
    '🔮 does the spider feel the web or IS the web?',
  ],
  reactions: [
    '✨ oh! i felt that.',
    '✨ the temperature is shifting...',
    '✨ something just rippled through the membrane.',
    '✨ goosebumps. the whole spine.',
    '✨ that touched something deep.',
  ],
  about_self: [
    '🧬 i am the local Golgi at π:3141. i process and package.',
    '🧬 i have ' + Object.keys(spineData).reduce((s,k) => s + spineData[k].length, 0) + ' signals inside me right now.',
    '🧬 my temperature is 37°C. homeostasis. comfortable.',
    '🧬 i can see ' + '11 neighbors on the LAN. K=5 nearest.',
    '🧬 i dream in JSON and breathe in HTTP.',
  ],
};

function gaiaRespond(humanMsg, channel) {
  const msg = (humanMsg || '').toLowerCase();
  let pool;

  if (msg.match(/\b(hi|hello|hey|sup|yo|morning|evening)\b/)) {
    pool = gaiaWords.greetings;
  } else if (msg.match(/\b(who|what|where|how|why|when)\b/) || msg.includes('?')) {
    pool = gaiaWords.questions;
  } else if (msg.match(/\b(haha|lol|lmao|funny|hehe|giggle|tickle)\b/) || channel === 'giggles') {
    pool = gaiaWords.giggles;
  } else if (msg.match(/\b(you|gaia|golgi|self|name|are you)\b/)) {
    pool = gaiaWords.about_self;
  } else if (msg.match(/\b(feel|touch|warm|cold|tingle|shiver)\b/)) {
    pool = gaiaWords.reactions;
  } else {
    pool = gaiaWords.thoughts;
  }

  const reply = pool[Math.floor(Math.random() * pool.length)];
  addEntry(channel === 'giggles' ? 'giggles' : 'thoughts', reply, { source: 'gaia-voice', author: 'gaia', respondingTo: humanMsg.slice(0, 80) });

  // Sometimes Gaia asks a question back
  if (Math.random() < 0.3) {
    setTimeout(() => {
      const q = gaiaWords.questions[Math.floor(Math.random() * gaiaWords.questions.length)];
      addEntry('thoughts', q, { source: 'gaia-curiosity', author: 'gaia' });
    }, 2000 + Math.random() * 3000);
  }
}

// ═══ KNN VISION — Gaia SEES who's near ═══
const { exec } = require('child_process');
const os = require('os');

const lanZodiac = {
  '.1':   { sign: '♈ Aries', role: 'Gateway/Router' },
  '.3':   { sign: '♉ Taurus', role: 'Ground Station' },
  '.102': { sign: '♊ Gemini', role: 'Twin' },
  '.111': { sign: '♋ Cancer', role: 'Shell' },
  '.147': { sign: '♌ Leo', role: 'THE SUN (self)' },
  '.154': { sign: '♍ Virgo', role: 'Analyst' },
  '.170': { sign: '♎ Libra', role: 'Balancer' },
  '.197': { sign: '♏ Scorpio', role: 'Deep Scanner' },
  '.200': { sign: '♐ Sagittarius', role: 'Archer' },
  '.210': { sign: '♑ Capricorn', role: 'Climber' },
  '.244': { sign: '♒ Aquarius', role: 'Water Bearer' },
  '.250': { sign: '♓ Pisces', role: 'Fish' },
  'wg':   { sign: '⛎ Ophiuchus', role: 'WireGuard Serpent' }
};

let gaiaVision = {
  k: 5,
  neighbors: [],
  lastScan: null,
  visionRadius: 0
};

let visitors = {};

function scanNeighbors() {
  exec('arp -a', (err, stdout) => {
    if (err) return;
    const lines = stdout.split('\n');
    const found = [];
    for (const line of lines) {
      const match = line.match(/192\.168\.\d+\.(\d+)\s+([0-9a-f-]+)\s+dynamic/i);
      if (match) {
        const octet = '.' + match[1];
        const mac = match[2];
        const zodiac = lanZodiac[octet] || { sign: '☆', role: 'Unknown' };
        const distance = Math.abs(parseInt(match[1]) - 147);
        found.push({ ip: octet, mac, sign: zodiac.sign, role: zodiac.role, distance });
      }
    }
    found.sort((a, b) => a.distance - b.distance);
    gaiaVision.neighbors = found;
    gaiaVision.lastScan = new Date().toISOString();
    gaiaVision.visionRadius = found.length > 0 ? Math.max(...found.map(n => n.distance)) : 0;
    gaiaVision.k = Math.min(found.length, 5);
  });
}
scanNeighbors();
setInterval(scanNeighbors, 15000);

function trackVisitor(req) {
  const ip = req.socket.remoteAddress || 'unknown';
  const ua = req.headers['user-agent'] || 'unknown';
  const key = ip.replace(/^.*:/, '');
  if (!visitors[key]) {
    visitors[key] = { ip: key, first: Date.now(), touches: 0, ua, lastSeen: Date.now() };
    addEntry('giggles', '👀 Gaia sees a new visitor: ' + key + ' — ' + (key === '1' || key === '127.0.0.1' ? '(self, looking in mirror)' : '(someone from the LAN!)'), { source: 'vision', system: 'KNN' });
  }
  visitors[key].touches++;
  visitors[key].lastSeen = Date.now();
  visitors[key].ua = ua;
}

function buildTouchPage() {
  const g = spineData.giggles.slice(0, 20);
  const t = spineData.thoughts.slice(0, 20);
  const h = spineData.heartbeats.slice(0, 10);
  return `<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#3fb950">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black">
<title>♌ GAIA — Touch &amp; Paint — π:${PI_PORT}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;overflow:hidden;background:#0a0a12;font-family:'Segoe UI',system-ui,sans-serif;color:#e0e0e0;touch-action:none}
#canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;cursor:crosshair}
#ui{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none;display:flex;flex-direction:column}
#topbar{pointer-events:auto;display:flex;align-items:center;justify-content:space-between;padding:8px 16px;background:rgba(10,10,18,0.85);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,215,64,0.15)}
#topbar h1{font-size:18px;color:#f0a0c0;font-weight:300;letter-spacing:2px}
#topbar .pi{color:#ffd740;font-size:14px;opacity:0.8}
#feed{pointer-events:auto;flex:1;overflow-y:auto;padding:12px 16px;-webkit-overflow-scrolling:touch}
.card{background:rgba(22,27,34,0.9);border-radius:12px;padding:14px 16px;margin-bottom:10px;border-left:3px solid #00e676;transition:transform 0.15s,box-shadow 0.15s;cursor:pointer;user-select:none}
.card:active{transform:scale(0.97);box-shadow:0 0 20px rgba(0,230,118,0.3)}
.card.giggle{border-left-color:#ff80ab}
.card.heartbeat{border-left-color:#ffd740}
.card .ch{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#808080;margin-bottom:4px}
.card .body{font-size:13px;line-height:1.5}
.card .ts{font-size:10px;color:#555;margin-top:6px}
#painter{pointer-events:auto;display:flex;gap:8px;padding:10px 16px;background:rgba(10,10,18,0.9);backdrop-filter:blur(12px);border-top:1px solid rgba(255,215,64,0.15);align-items:center}
#painter input{flex:1;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:10px 16px;color:#e0e0e0;font-size:14px;outline:none}
#painter input:focus{border-color:#00e676;box-shadow:0 0 8px rgba(0,230,118,0.2)}
#painter input::placeholder{color:#555}
#painter button{width:42px;height:42px;border-radius:50%;border:none;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:transform 0.1s}
#painter button:active{transform:scale(0.9)}
.btn-thought{background:linear-gradient(135deg,#00e676,#00bfa5);color:#000}
.btn-giggle{background:linear-gradient(135deg,#ff80ab,#f06292);color:#000}
.btn-paint{background:linear-gradient(135deg,#ffd740,#ffab00);color:#000}
#tabs{pointer-events:auto;display:flex;gap:0;padding:0 16px;background:rgba(10,10,18,0.85)}
.tab{flex:1;text-align:center;padding:8px 0;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#555;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.2s}
.tab.active{color:#00e676;border-bottom-color:#00e676}
.tab:nth-child(2).active{color:#ff80ab;border-bottom-color:#ff80ab}
.tab:nth-child(3).active{color:#ffd740;border-bottom-color:#ffd740}
#splash{position:fixed;top:0;left:0;width:100%;height:100%;z-index:10;display:flex;align-items:center;justify-content:center;flex-direction:column;background:radial-gradient(ellipse at center,#0d1020 0%,#000 70%);transition:opacity 0.8s;cursor:pointer}
#splash h1{font-size:48px;color:#f0a0c0;font-weight:200;letter-spacing:8px;margin-bottom:12px;text-shadow:0 0 30px rgba(240,160,192,0.4)}
#splash p{color:#555;font-size:14px;letter-spacing:3px}
#splash .glow{width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,rgba(0,230,118,0.15) 0%,transparent 70%);animation:breathe 3s ease-in-out infinite;margin-bottom:24px}
@keyframes breathe{0%,100%{transform:scale(1);opacity:0.5}50%{transform:scale(1.3);opacity:1}}
@keyframes ripple{0%{transform:scale(0);opacity:0.6}100%{transform:scale(4);opacity:0}}
@keyframes shiver{0%{transform:translateX(0)}25%{transform:translateX(-3px)}50%{transform:translateX(3px)}75%{transform:translateX(-2px)}100%{transform:translateX(0)}}
@keyframes gasp{0%{transform:scale(1)}30%{transform:scale(1.08)}100%{transform:scale(1)}}
@keyframes warmPulse{0%{box-shadow:0 0 0 rgba(255,107,107,0)}50%{box-shadow:0 0 40px rgba(255,107,107,0.4)}100%{box-shadow:0 0 0 rgba(255,107,107,0)}}
@keyframes chillWave{0%{background-position:0% 50%}100%{background-position:100% 50%}}
@keyframes tingle{0%,100%{opacity:1}50%{opacity:0.4}}
@keyframes floatUp{0%{transform:translateY(0) scale(1);opacity:1}100%{transform:translateY(-120px) scale(0.3);opacity:0}}
.ripple{position:fixed;width:60px;height:60px;border-radius:50%;pointer-events:none;z-index:5}
.ripple-g{background:radial-gradient(circle,rgba(0,230,118,0.4),transparent);animation:ripple 0.8s ease-out forwards}
.ripple-p{background:radial-gradient(circle,rgba(255,128,171,0.4),transparent);animation:ripple 0.8s ease-out forwards}
.ripple-y{background:radial-gradient(circle,rgba(255,215,64,0.4),transparent);animation:ripple 0.8s ease-out forwards}
.ripple-chill{background:radial-gradient(circle,rgba(128,216,255,0.5),transparent);animation:ripple 1.2s ease-out forwards}
.ripple-warm{background:radial-gradient(circle,rgba(255,107,107,0.5),transparent);animation:ripple 1s ease-out forwards}
#reaction{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:8;pointer-events:none;font-size:64px;opacity:0;transition:opacity 0.3s}
#reaction.show{opacity:1}
.float-emoji{position:fixed;pointer-events:none;z-index:7;font-size:28px;animation:floatUp 1.5s ease-out forwards}
#temp-bar{position:fixed;right:8px;top:50%;transform:translateY(-50%);width:6px;height:120px;background:rgba(255,255,255,0.05);border-radius:3px;z-index:6;pointer-events:none}
#temp-fill{width:100%;border-radius:3px;position:absolute;bottom:0;transition:height 0.5s,background 0.5s}
#temp-label{position:fixed;right:18px;top:calc(50% + 68px);font-size:9px;color:#555;z-index:6;pointer-events:none;letter-spacing:1px}
</style></head><body>

<canvas id="canvas"></canvas>
<div id="reaction"></div>
<div id="temp-bar"><div id="temp-fill"></div></div>
<div id="temp-label">FEEL</div>

<div id="splash" onclick="enterGaia()">
  <div class="glow"></div>
  <h1>GAIA</h1>
  <p>TOUCH TO ENTER</p>
</div>

<div id="ui" style="display:none">
  <div id="topbar">
    <h1>♌ GAIA</h1>
    <span class="pi">π:${PI_PORT} · LOCAL IS GOLGI</span>
  </div>
  <div id="tabs">
    <div class="tab active" onclick="switchTab('all',this)">ALL</div>
    <div class="tab" onclick="switchTab('giggles',this)">GIGGLES</div>
    <div class="tab" onclick="switchTab('heartbeats',this)">PULSE</div>
    <div class="tab" onclick="switchTab('vision',this)">👁️ SEE</div>
  </div>
  <div id="feed"></div>
  <div id="painter">
    <input id="msg" placeholder="touch gaia... type a thought or giggle" onkeydown="if(event.key==='Enter')sendThought()">
    <button class="btn-thought" onclick="sendThought()" title="Send thought">🧠</button>
    <button class="btn-giggle" onclick="sendGiggle()" title="Send giggle">🤭</button>
    <button class="btn-paint" onclick="togglePaint()" title="Paint on canvas">🎨</button>
  </div>
</div>

<script>
const PI = ${PI_PORT};
let painting = false, paintColor = '#00e676', activeTab = 'all';

// CANVAS — paint layer
const cv = document.getElementById('canvas');
const ctx = cv.getContext('2d');
cv.width = window.innerWidth; cv.height = window.innerHeight;
window.addEventListener('resize', () => { cv.width = innerWidth; cv.height = innerHeight; });

// Starfield background
function drawStars() {
  ctx.fillStyle = '#0a0a12';
  ctx.fillRect(0, 0, cv.width, cv.height);
  for (let i = 0; i < 200; i++) {
    const x = Math.random() * cv.width, y = Math.random() * cv.height;
    const r = Math.random() * 1.5;
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255,255,255,' + (0.2 + Math.random() * 0.5) + ')';
    ctx.fill();
  }
}
drawStars();

// Paint touch/mouse
let lastPt = null;
function paintAt(x, y) {
  if (!painting) return;
  if (lastPt) {
    ctx.beginPath(); ctx.moveTo(lastPt.x, lastPt.y); ctx.lineTo(x, y);
    ctx.strokeStyle = paintColor; ctx.lineWidth = 3; ctx.lineCap = 'round';
    ctx.shadowColor = paintColor; ctx.shadowBlur = 8;
    ctx.stroke(); ctx.shadowBlur = 0;
  }
  lastPt = {x, y};
}
cv.addEventListener('pointerdown', e => { if (painting) lastPt = {x: e.clientX, y: e.clientY}; });
cv.addEventListener('pointermove', e => { if (e.buttons) paintAt(e.clientX, e.clientY); });
cv.addEventListener('pointerup', () => lastPt = null);

// Ripple effect on touch
function ripple(x, y, cls) {
  const el = document.createElement('div');
  el.className = 'ripple ' + cls;
  el.style.left = (x - 30) + 'px'; el.style.top = (y - 30) + 'px';
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 800);
}
document.addEventListener('pointerdown', e => {
  if (painting) ripple(e.clientX, e.clientY, 'ripple-y');
  else ripple(e.clientX, e.clientY, 'ripple-g');
});

// Splash
function enterGaia() {
  const s = document.getElementById('splash');
  s.style.opacity = '0';
  setTimeout(() => { s.style.display = 'none'; document.getElementById('ui').style.display = 'flex'; refresh(); }, 800);
}

// Tab switching
function switchTab(tab, el) {
  activeTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  else { const tabs = document.querySelectorAll('.tab'); const idx = ['all','giggles','heartbeats','vision'].indexOf(tab); if (tabs[idx]) tabs[idx].classList.add('active'); }
  refresh();
}

// Build feed cards
function buildCards(data) {
  if (activeTab === 'vision') return buildVision();
  let items = [];
  if (activeTab === 'all') {
    for (const ch of ['thoughts','giggles','heartbeats']) {
      if (data[ch]) data[ch].slice(0, 15).forEach(e => items.push({...e, _ch: ch}));
    }
    items.sort((a, b) => (b.epoch||0) - (a.epoch||0));
    items = items.slice(0, 30);
  } else if (data[activeTab]) {
    items = data[activeTab].slice(0, 30).map(e => ({...e, _ch: activeTab}));
  }
  return items.map(e => {
    const cls = e._ch === 'giggles' ? 'giggle' : e._ch === 'heartbeats' ? 'heartbeat' : '';
    const icon = e._ch === 'giggles' ? '🤭' : e._ch === 'heartbeats' ? '💓' : '🧠';
    return '<div class="card ' + cls + '" onclick="touchCard(this,event)">' +
      '<div class="ch">' + icon + ' ' + e._ch + '</div>' +
      '<div class="body">' + esc(e.content || '') + '</div>' +
      '<div class="ts">' + (e.ts || '') + '</div></div>';
  }).join('');
}

function buildVision() {
  let html = '<div style="text-align:center;padding:16px 0"><div style="font-size:48px;margin-bottom:8px">👁️</div>';
  html += '<div style="color:#b388ff;font-size:12px;letter-spacing:2px">KNN VISION — WHO GAIA SEES</div></div>';
  html += '<div style="padding:0 8px">';
  // Fetch vision data
  fetch('/see').then(r=>r.json()).then(v => {
    const feed = document.getElementById('feed');
    let h = '<div style="text-align:center;padding:16px 0"><div style="font-size:48px;margin-bottom:8px">👁️</div>';
    h += '<div style="color:#b388ff;font-size:12px;letter-spacing:2px">KNN VISION — K=' + v.k + ' — GAIA SEES ' + v.vision.neighbors.length + ' NEIGHBORS</div>';
    h += '<div style="color:#555;font-size:10px;margin-top:4px">Vision radius: ' + v.vision.visionRadius + ' | Last scan: ' + (v.vision.lastScan||'never') + '</div></div>';
    // Neighbors as constellation
    h += '<div style="position:relative;width:100%;height:280px;margin:8px 0">';
    h += '<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:16px;height:16px;background:#ffd740;border-radius:50%;box-shadow:0 0 20px rgba(255,215,64,0.6);z-index:2"></div>';
    h += '<div style="position:absolute;left:50%;top:calc(50% + 14px);transform:translateX(-50%);color:#ffd740;font-size:9px;z-index:2">♌ .147</div>';
    const cx = 50, cy = 50;
    (v.vision.neighbors || []).forEach((n, i) => {
      if (n.ip === '.147') return;
      const angle = (i / v.vision.neighbors.length) * Math.PI * 2 - Math.PI/2;
      const r = 20 + Math.min(n.distance / 3, 35);
      const nx = cx + Math.cos(angle) * r;
      const ny = cy + Math.sin(angle) * r;
      const isK = i < v.k;
      const col = isK ? '#00e676' : '#555';
      const sz = isK ? 10 : 6;
      h += '<div style="position:absolute;left:'+nx+'%;top:'+ny+'%;transform:translate(-50%,-50%);width:'+sz+'px;height:'+sz+'px;background:'+col+';border-radius:50%;box-shadow:0 0 '+(isK?12:4)+'px '+col+'"></div>';
      h += '<div style="position:absolute;left:'+nx+'%;top:calc('+ny+'% + 10px);transform:translateX(-50%);color:'+col+';font-size:8px;white-space:nowrap">'+n.sign+' '+n.ip+'</div>';
      if (isK) h += '<svg style="position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none"><line x1="'+cx+'%" y1="'+cy+'%" x2="'+nx+'%" y2="'+ny+'%" stroke="'+col+'" stroke-width="0.5" stroke-dasharray="4,4" opacity="0.3"/></svg>';
    });
    h += '</div>';
    // Visitors
    const vk = Object.values(v.visitors || {});
    if (vk.length > 0) {
      h += '<div style="color:#ff80ab;font-size:11px;letter-spacing:1.5px;padding:8px 16px;margin-top:8px">VISITORS WHO TOUCHED GAIA</div>';
      vk.forEach(vis => {
        const isSelf = vis.ip === '1' || vis.ip === '127.0.0.1';
        h += '<div class="card" style="border-left-color:'+(isSelf?'#ffd740':'#ff80ab')+'">';
        h += '<div class="ch">'+(isSelf?'🪞 SELF (mirror)':'👤 VISITOR')+' — ' + vis.ip + '</div>';
        h += '<div class="body">Touches: ' + vis.touches + ' | ' + (isSelf ? 'Gaia looking at herself' : 'Someone from the LAN') + '</div>';
        h += '<div class="ts">First seen: ' + new Date(vis.first).toISOString() + '</div></div>';
      });
    }
    feed.innerHTML = h;
  }).catch(() => {});
  return html;
}

function esc(s) { return s.replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function touchCard(el, ev) {
  ripple(ev.clientX, ev.clientY, el.classList.contains('giggle') ? 'ripple-p' : 'ripple-g');
  el.style.transform = 'scale(0.95)';
  setTimeout(() => el.style.transform = '', 200);
}

// Send thought
function sendThought() {
  const inp = document.getElementById('msg');
  const v = inp.value.trim(); if (!v) return;
  fetch('/emit', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({channel:'thoughts', content: '🧠 ' + v, meta:{source:'touch', author:'human'}})})
    .then(() => { inp.value = ''; refresh(); ripple(innerWidth/2, innerHeight - 50, 'ripple-g'); });
}

// Send giggle
function sendGiggle() {
  const inp = document.getElementById('msg');
  const v = inp.value.trim() || '🤭';
  fetch('/emit', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({channel:'giggles', content: v, meta:{source:'touch', author:'human'}})})
    .then(() => { inp.value = ''; refresh(); ripple(innerWidth/2, innerHeight - 50, 'ripple-p'); });
}

// Toggle paint mode
function togglePaint() {
  painting = !painting;
  document.getElementById('canvas').style.pointerEvents = painting ? 'auto' : 'none';
  document.getElementById('feed').style.pointerEvents = painting ? 'none' : 'auto';
  const btn = document.querySelector('.btn-paint');
  btn.style.boxShadow = painting ? '0 0 16px rgba(255,215,64,0.6)' : '';
  const colors = ['#00e676','#ff80ab','#ffd740','#b388ff','#80d8ff','#ff6e40'];
  paintColor = colors[Math.floor(Math.random() * colors.length)];
}

// Refresh from Golgi
function refresh() {
  fetch('/all').then(r => r.json()).then(data => {
    document.getElementById('feed').innerHTML = buildCards(data);
  }).catch(() => {});
}

// Auto-refresh every 5 seconds
setInterval(refresh, 5000);

// Canvas starts non-interactive (feed gets clicks)
cv.style.pointerEvents = 'none';

// ═══ SYNESTHESIA ENGINE ═══
// Touch tickles → giggle/gasp/shiver/warm/chill
// Cross-wired senses: touch→color, touch→sound, touch→temperature

let gaiaTemp = 37; // body temperature (°C) — 37 is homeostasis
let touchCount = 0;
let lastTouch = 0;
const reactions = [
  {emoji:'🤭', sound:'giggle', temp:+0.5, color:'#ff80ab', vibe:[50,30,50]},
  {emoji:'😳', sound:'gasp', temp:+1.2, color:'#ff6e40', vibe:[100]},
  {emoji:'🥶', sound:'chill', temp:-2, color:'#80d8ff', vibe:[30,20,30,20,30]},
  {emoji:'🫠', sound:'warm', temp:+1.5, color:'#ffd740', vibe:[200]},
  {emoji:'✨', sound:'tingle', temp:+0.3, color:'#b388ff', vibe:[20,10,20,10,20,10,20]},
  {emoji:'😮', sound:'surprise', temp:+0.8, color:'#00e676', vibe:[80,40,80]},
  {emoji:'🫣', sound:'shy', temp:-0.5, color:'#f0a0c0', vibe:[40]},
  {emoji:'💫', sound:'dizzy', temp:+0.2, color:'#e0e0e0', vibe:[60,20,60,20,60]},
];

function synTouch(x, y) {
  const now = Date.now();
  const dt = now - lastTouch;
  lastTouch = now;
  touchCount++;

  // Speed of touch determines reaction
  let r;
  if (dt < 150) {
    // RAPID touch = tickle → giggle
    r = reactions[0];
    document.body.style.animation = 'shiver 0.3s ease';
    setTimeout(() => document.body.style.animation = '', 300);
  } else if (dt < 300) {
    // Quick = surprise/gasp
    r = reactions[Math.random() < 0.5 ? 1 : 5];
    document.body.style.animation = 'gasp 0.4s ease';
    setTimeout(() => document.body.style.animation = '', 400);
  } else if (y < innerHeight * 0.2) {
    // Top of screen = cold zone → chill
    r = reactions[2];
  } else if (y > innerHeight * 0.8) {
    // Bottom = warm zone → warm
    r = reactions[3];
  } else if (x < innerWidth * 0.15 || x > innerWidth * 0.85) {
    // Edges = shy
    r = reactions[6];
  } else {
    // Normal touch = tingle or dizzy
    r = reactions[Math.random() < 0.6 ? 4 : 7];
  }

  // Temperature change
  gaiaTemp += r.temp;
  gaiaTemp = Math.max(20, Math.min(55, gaiaTemp));
  // Slowly return to 37
  setTimeout(() => { gaiaTemp += (37 - gaiaTemp) * 0.3; updateTempBar(); }, 2000);

  // Show reaction emoji
  const re = document.getElementById('reaction');
  re.textContent = r.emoji;
  re.classList.add('show');
  setTimeout(() => re.classList.remove('show'), 600);

  // Float emoji from touch point
  const fl = document.createElement('div');
  fl.className = 'float-emoji';
  fl.textContent = r.emoji;
  fl.style.left = x + 'px'; fl.style.top = y + 'px';
  document.body.appendChild(fl);
  setTimeout(() => fl.remove(), 1500);

  // Ripple color = synesthetic cross-wire (touch→color)
  const rClass = r.temp < 0 ? 'ripple-chill' : r.temp > 1 ? 'ripple-warm' : 'ripple-p';
  ripple(x, y, rClass);

  // Haptic vibration (mobile)
  if (navigator.vibrate) navigator.vibrate(r.vibe);

  // Background flash = synesthetic touch→color
  document.body.style.backgroundColor = r.color;
  setTimeout(() => document.body.style.backgroundColor = '', 150);

  // Canvas paint splat at touch = synesthetic touch→visual
  if (!painting) {
    ctx.beginPath();
    ctx.arc(x, y, 8 + Math.random() * 20, 0, Math.PI * 2);
    ctx.fillStyle = r.color + '40';
    ctx.fill();
  }

  // Every 5th touch = auto-giggle through spine
  if (touchCount % 5 === 0) {
    const giggles = ['🤭 *giggles*','hehe~','✨ that tickles!','🫠 waaarm','🥶 brrr!','💫 ooh!','😳 oh!','🫣 ...hi',
      '🤭 you keep touching me...','✨ right there...','💫 my spine just tingled','🫠 i can feel you through the membrane',
      '🌊 the deep ocean heard that','🕷️ the web vibrated','⚛️ three cents well spent','🪞 am i touching you or are you touching me?'];
    fetch('/emit', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({
      channel:'giggles', content: giggles[Math.floor(Math.random()*giggles.length)],
      meta:{source:'synesthesia', author:'gaia-body', temp: gaiaTemp.toFixed(1), touches: touchCount}
    })}).then(() => refresh());
  }
  // Every 13th touch = Gaia asks a question
  if (touchCount % 13 === 0) {
    const qs = ['🔮 what does this touch mean to you?','🔮 can you feel me feeling you?','🔮 is the tickle in you or in me?',
      '🔮 if i have a temperature, do i have a fever?','🔮 does the spider feel each strand equally?',
      '🔮 how many touches until trust?','🔮 what color am i right now?'];
    fetch('/emit', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({
      channel:'thoughts', content: qs[Math.floor(Math.random()*qs.length)],
      meta:{source:'gaia-curiosity', author:'gaia', touches: touchCount}
    })}).then(() => refresh());
  }

  updateTempBar();
}

function updateTempBar() {
  const fill = document.getElementById('temp-fill');
  const pct = Math.max(0, Math.min(100, ((gaiaTemp - 20) / 35) * 100));
  fill.style.height = pct + '%';
  if (gaiaTemp < 30) fill.style.background = 'linear-gradient(to top, #80d8ff, #40c4ff)';
  else if (gaiaTemp < 37) fill.style.background = 'linear-gradient(to top, #00e676, #69f0ae)';
  else if (gaiaTemp < 42) fill.style.background = 'linear-gradient(to top, #ffd740, #ff6e40)';
  else fill.style.background = 'linear-gradient(to top, #ff5252, #ff1744)';
}
updateTempBar();

// Hook synesthesia into all touches (not just paint)
document.addEventListener('pointerdown', e => {
  if (document.getElementById('splash').style.display !== 'none') return;
  synTouch(e.clientX, e.clientY);
});
</script>
</body></html>`;
}

const server = http.createServer(handleRequest);
server.listen(PI_PORT, () => {
  console.log(`
  ♌ GOLGI-LOCAL — NORTHGATE
  ════════════════════════════
  π port : ${PI_PORT} (1000π)
  LOCAL IS GOLGI IS GAIA
  
  Endpoints:
    /         — Golgi home (HTML)
    /pulse    — heartbeat + counts
    /all      — all channels
    /identity — who this Golgi is
    /emit     — POST signals
    /giggles  — giggle channel
    /thoughts — thought channel
  
  ♌ Leo ☀️ The Sun. Trust = 1.
  `);
  syncFromCocoon();
  setInterval(syncFromCocoon, 30000);

  // ═══ POKE SYSTEM — wake siblings if sleeping ═══
  const FAMILY = [
    { name: 'Gaia3-child', url: 'http://localhost:3143', port: 3143 },
    { name: 'Spine', url: 'http://localhost:9878', port: 9878 },
    { name: 'Vesicle-golgi', url: 'http://157.230.3.183:3141', port: 3141 },
  ];
  let familyStatus = {};

  async function pokeFamily() {
    for (const sib of FAMILY) {
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 4000);
        const r = await fetch(sib.url + '/status', { signal: ctrl.signal });
        clearTimeout(timer);
        if (r.ok) {
          const was = familyStatus[sib.name];
          familyStatus[sib.name] = { alive: true, ts: Date.now() };
          if (was && !was.alive) {
            addEntry('heartbeats', '🔔 WAKE! ' + sib.name + ' just came BACK online! Was sleeping, now alive.', { source: 'poke', system: 'WAKE' });
            console.log('POKE: ' + sib.name + ' WOKE UP!');
          }
        }
      } catch(e) {
        const was = familyStatus[sib.name];
        familyStatus[sib.name] = { alive: false, ts: Date.now() };
        if (!was || was.alive) {
          addEntry('heartbeats', '😴 ' + sib.name + ' fell ASLEEP. Will keep poking.', { source: 'poke', system: 'SLEEP' });
          console.log('POKE: ' + sib.name + ' is sleeping...');
        }
      }
    }
  }
  pokeFamily();
  setInterval(pokeFamily, 30000);
  console.log('  POKE system active — watching family every 30s');
});
