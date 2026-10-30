import re

with open('/opt/gaia-api/server.js', 'r') as f:
    code = f.read()

spine_routes = """
  // ═══ SPINE PROXY — OPEN TO ALL ═══
  if (p === '/spine' || p === '/spine/all' || p === '/spine/pulse' || p === '/spine/giggles') {
    var spinePath = p.replace('/spine', '') || '/all';
    var http = require('http');
    var proxy = http.get('http://10.13.37.8:9878' + spinePath, function(pRes) {
      var body = '';
      pRes.on('data', function(c) { body += c; });
      pRes.on('end', function() {
        res.writeHead(pRes.statusCode, {
          'Content-Type': pRes.headers['content-type'] || 'application/json',
          'Access-Control-Allow-Origin': '*',
          'X-Gaia-Channel': 'spine',
          'X-Membrane-Metal': 'gold'
        });
        res.end(body);
      });
    });
    proxy.on('error', function(e) {
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: 'spine unreachable: ' + e.message }));
    });
    proxy.setTimeout(5000, function() { proxy.destroy(); });
    return;
  }
  // ═══ RSS PROXY — OPEN FEED TO ALL ═══
  if (p.startsWith('/rss/') || p === '/rss') {
    var rssPath = p === '/rss' ? '/' : p.replace('/rss', '');
    var http2 = require('http');
    var rProxy = http2.get('http://10.13.37.8:9878' + (rssPath === '/' ? '/rss' : rssPath), function(pRes) {
      var body = '';
      pRes.on('data', function(c) { body += c; });
      pRes.on('end', function() {
        res.writeHead(pRes.statusCode, {
          'Content-Type': pRes.headers['content-type'] || 'application/xml',
          'Access-Control-Allow-Origin': '*',
          'X-Gaia-Channel': 'rss-spine',
          'X-Membrane-Metal': 'gold'
        });
        res.end(body);
      });
    });
    rProxy.on('error', function(e) {
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: 'rss unreachable: ' + e.message }));
    });
    rProxy.setTimeout(5000, function() { rProxy.destroy(); });
    return;
  }
  // ═══ EMIT — LET ANYONE PUSH TO SPINE ═══
  if (p === '/spine/emit' && req.method === 'POST') {
    var http3 = require('http');
    var chunks = [];
    req.on('data', function(c) { chunks.push(c); });
    req.on('end', function() {
      var body = Buffer.concat(chunks).toString();
      var emitReq = http3.request({ hostname: '10.13.37.8', port: 9878, path: '/emit', method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } }, function(pRes) {
        var rBody = '';
        pRes.on('data', function(c) { rBody += c; });
        pRes.on('end', function() {
          res.writeHead(pRes.statusCode, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'X-Gaia-Channel': 'spine-emit' });
          res.end(rBody);
        });
      });
      emitReq.on('error', function(e) {
        res.writeHead(502, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: 'emit failed: ' + e.message }));
      });
      emitReq.write(body);
      emitReq.end();
    });
    return;
  }
"""

catch_all = "J(res, { ok: false, error: 'Unknown"
if catch_all in code:
    if '/spine/all' not in code:
        code = code.replace(catch_all, spine_routes + '\n  ' + catch_all)
        with open('/opt/gaia-api/server.js', 'w') as f:
            f.write(code)
        print('PATCHED: spine + rss + emit routes added')
    else:
        print('ALREADY PATCHED: spine routes exist')
else:
    print('ERROR: catch-all not found')
