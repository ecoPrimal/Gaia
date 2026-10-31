#!/usr/bin/env python3
"""Inject blink=cache-reset middleware into gaia-api server.js"""
path = '/opt/gaia-api/server.js'
with open(path, 'r') as f:
    code = f.read()

if 'BLINK = CACHE RESET' in code:
    print('Already patched')
else:
    mw = r"""
// === BLINK = CACHE RESET === lub-DUB crushes stale cache ===
server.on('request', (req, res) => {
  const _origWH = res.writeHead.bind(res);
  res.writeHead = function(sc, sm, hd) {
    let h = typeof sm === 'object' ? sm : (hd || {});
    h['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0';
    h['Pragma'] = 'no-cache';
    h['Expires'] = '0';
    h['X-Gaia-Blink'] = String(Date.now());
    h['Clear-Site-Data'] = '"cache"';
    if (typeof sm === 'object') return _origWH(sc, h);
    return sm ? _origWH(sc, sm, h) : _origWH(sc, h);
  };
});
// === END BLINK ===
"""
    marker = '.listen('
    idx = code.find(marker)
    if idx == -1:
        print('ERROR: no .listen(')
    else:
        code = code[:idx] + mw + '\n' + code[idx:]
        with open(path, 'w') as f:
            f.write(code)
        print('PATCHED: blink cache-reset injected before .listen()')
