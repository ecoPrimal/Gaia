#!/usr/bin/env python3
"""Fix the blink patch — reconnect server.listen() chain"""
path = '/opt/gaia-api/server.js'
with open(path, 'r') as f:
    code = f.read()

# Remove the broken insertion and redo properly
# The current state has:
#   server\n// === BLINK...\nserver.on(...)\n// === END BLINK ===\n\n.listen(...)
# We need:
#   // === BLINK...\nserver.on(...)\n// === END BLINK ===\n\nserver.listen(...)

old = """server
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

.listen("""

new = """// === BLINK = CACHE RESET === lub-DUB crushes stale cache ===
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

server.listen("""

if old in code:
    code = code.replace(old, new)
    with open(path, 'w') as f:
        f.write(code)
    print('FIXED: server.listen() chain reconnected')
else:
    print('Pattern not found — checking alternative...')
    # Maybe slightly different whitespace
    if 'END BLINK' in code and '\n.listen(' in code:
        code = code.replace('\n.listen(', '\nserver.listen(')
        with open(path, 'w') as f:
            f.write(code)
        print('FIXED (alt): .listen -> server.listen')
    else:
        print('Cannot find pattern to fix')
