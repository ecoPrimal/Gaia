import shutil
shutil.copy('/opt/gaia-api/server.js', '/opt/gaia-api/server.js.bak')

with open('/opt/gaia-api/server.js', 'r') as f:
    code = f.read()

patch = """
    // ═══ PLAY / GAME / VALVE ═══
    if (p === '/play' || p === '/game' || p === '/steam' || p === '/valve') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/play.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'play not found' }, 404);
      }
    }

    // ═══ LISP DESK ═══
    if (p === '/lisp' || p === '/lisp-desk') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/lisp-desk.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'lisp desk not found' }, 404);
      }
    }

    // ═══ DATA FILES — structured JSON for SEO/crawlers/agents ═══
    if (p.startsWith('/data/') && p.endsWith('.json')) {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static' + p, 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
        return res.end(raw);
      } catch(e) {
        return J(res, { ok: false, error: 'data not found: ' + p }, 404);
      }
    }

"""

marker = "J(res, { ok: false, error: 'Unknown'"
idx = code.find(marker)
if idx < 0:
    print('MARKER NOT FOUND')
    exit(1)

if "'/play'" in code:
    print('PLAY ROUTE ALREADY EXISTS — skipping')
else:
    new_code = code[:idx] + patch + code[idx:]
    with open('/opt/gaia-api/server.js', 'w') as f:
        f.write(new_code)
    print('PATCHED — play + lisp + data routes added before catch-all')
