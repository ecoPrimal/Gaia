const http = require('http');
const os = require('os');
const { execSync } = require('child_process');

const PORT = 9877;

function getCpuPercent() {
  const cpus = os.cpus();
  let totalIdle = 0, totalTick = 0;
  cpus.forEach(cpu => {
    for (let type in cpu.times) totalTick += cpu.times[type];
    totalIdle += cpu.times.idle;
  });
  return Math.round((1 - totalIdle / totalTick) * 100);
}

function getMemory() {
  const total = os.totalmem();
  const free = os.freemem();
  const used = total - free;
  return {
    totalGB: (total / 1073741824).toFixed(1),
    usedGB: (used / 1073741824).toFixed(1),
    freeGB: (free / 1073741824).toFixed(1),
    percent: Math.round((used / total) * 100)
  };
}

function getGpu() {
  try {
    const raw = execSync('wmic path win32_VideoController get name,adapterram,driverversion /format:csv', { encoding: 'utf8', timeout: 5000 });
    const lines = raw.trim().split('\n').filter(l => l.trim() && !l.startsWith('Node'));
    const gpus = lines.map(line => {
      const parts = line.split(',');
      return {
        ram: parts[1] ? (parseInt(parts[1]) / 1073741824).toFixed(1) + 'GB' : '?',
        driver: (parts[2] || '').trim(),
        name: (parts[3] || '').trim()
      };
    }).filter(g => g.name);
    return gpus;
  } catch (e) {
    return [{ name: 'unknown', ram: '?', driver: '?' }];
  }
}

function getUptime() {
  const s = os.uptime();
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return h + 'h ' + m + 'm';
}

// Boost state (controlled by user)
let boostState = {
  level: 1.0,      // 1.0 = normal, 2.0 = double, 0.5 = half
  nitrous: false,
  maxLevel: 5.0,
  tickMultiplier: 1.0
};

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') { res.writeHead(200); res.end(); return; }

  if (req.url === '/metrics') {
    const mem = getMemory();
    const data = {
      hostname: os.hostname(),
      platform: os.platform(),
      arch: os.arch(),
      cpuModel: os.cpus()[0].model,
      cpuCores: os.cpus().length,
      cpuPercent: getCpuPercent(),
      memory: mem,
      gpus: getGpu(),
      uptime: getUptime(),
      loadAvg: os.loadavg().map(l => l.toFixed(2)),
      boost: boostState,
      ts: Date.now()
    };
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
    return;
  }

  if (req.url === '/boost' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const cmd = JSON.parse(body);
        if (cmd.level !== undefined) boostState.level = Math.max(0.1, Math.min(boostState.maxLevel, cmd.level));
        if (cmd.nitrous !== undefined) boostState.nitrous = !!cmd.nitrous;
        boostState.tickMultiplier = boostState.nitrous ? boostState.level * 2 : boostState.level;
        console.log('[BOOST]', boostState);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(boostState));
      } catch (e) {
        res.writeHead(400);
        res.end('bad json');
      }
    });
    return;
  }

  res.writeHead(404);
  res.end('not found');
});

server.listen(PORT, () => {
  console.log('Northgate metrics server on http://localhost:' + PORT);
  console.log('Metrics: http://localhost:' + PORT + '/metrics');
  console.log('Boost:   POST http://localhost:' + PORT + '/boost');
});
