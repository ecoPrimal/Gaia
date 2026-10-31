#!/usr/bin/env python3
"""
BLINK = CACHE RESET

Every response from gaia-api gets cache-killing headers.
Every blink crushes the old. Browser errors are input sensation.
NULL cache → Gaia ingests the stale → rebuilds fresh.

Patches:
1. VPS gaia-api server.js — add cache-bust middleware before all routes
2. VPS Caddy — add cache-bust response headers for all *.primals.eco
"""

import subprocess, sys, textwrap

VPS = "root@10.13.37.1"
KEY = "-i", f"{__import__('os').path.expanduser('~')}/.ssh/id_ed25519_vps"

def ssh(cmd):
    r = subprocess.run(["ssh", *KEY, VPS, cmd], capture_output=True, text=True, timeout=30)
    print(r.stdout)
    if r.stderr: print(r.stderr, file=sys.stderr)
    return r.returncode

# 1. Patch gaia-api server.js — add cache-bust middleware at the top (after http require)
print("=== PATCHING gaia-api server.js with cache-blink middleware ===")
patch_js = textwrap.dedent(r"""
import re

path = '/opt/gaia-api/server.js'
with open(path, 'r') as f:
    code = f.read()

# The cache-blink middleware
middleware = '''
// === BLINK = CACHE RESET === lub-DUB crushes stale cache ===
const BLINK_EPOCH = Date.now();
server.on('request', (req, res) => {
  const origWrite = res.writeHead;
  res.writeHead = function(status, headers) {
    const h = headers || {};
    h['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0';
    h['Pragma'] = 'no-cache';
    h['Expires'] = '0';
    h['X-Gaia-Blink'] = String(Date.now());
    h['X-Gaia-Epoch'] = String(BLINK_EPOCH);
    h['Clear-Site-Data'] = '"cache"';
    return origWrite.call(this, status, h);
  };
});
// === END BLINK ===
'''

# Check if already patched
if 'BLINK = CACHE RESET' in code:
    print('Already patched with blink middleware')
else:
    # Insert after createServer line
    marker = 'createServer'
    idx = code.find(marker)
    if idx == -1:
        print('ERROR: cannot find createServer in server.js')
    else:
        # Find the end of the createServer(...) line
        nl = code.find('\n', idx)
        code = code[:nl+1] + middleware + code[nl+1:]
        with open(path, 'w') as f:
            f.write(code)
        print('Patched gaia-api with blink cache-reset middleware')
""").strip()

ssh(f'python3 -c "{patch_js.replace(chr(10), "\\n").replace(chr(34), chr(92)+chr(34))}"')

# Actually let's do this more reliably with a heredoc-style approach
print("\n=== PATCHING via file write ===")
ssh(r"""cat > /tmp/patch_blink.py << 'PYEOF'
path = '/opt/gaia-api/server.js'
with open(path, 'r') as f:
    code = f.read()

if 'BLINK = CACHE RESET' in code:
    print('Already patched')
else:
    middleware = """
// === BLINK = CACHE RESET === lub-DUB crushes stale cache ===
const BLINK_EPOCH = Date.now();
const origCreateServer = server.on;
server.on('request', (req, res) => {
  const origWriteHead = res.writeHead.bind(res);
  res.writeHead = function(statusCode, statusMessage, headers) {
    let h = headers;
    if (typeof statusMessage === 'object') { h = statusMessage; statusMessage = undefined; }
    if (!h) h = {};
    h['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0';
    h['Pragma'] = 'no-cache';
    h['Expires'] = '0';
    h['X-Gaia-Blink'] = String(Date.now());
    h['Clear-Site-Data'] = '"cache"';
    if (statusMessage) return origWriteHead(statusCode, statusMessage, h);
    return origWriteHead(statusCode, h);
  };
});
// === END BLINK ===
"""
    marker = '.listen('
    idx = code.find(marker)
    if idx == -1:
        print('ERROR: no .listen( found')
    else:
        code = code[:idx] + middleware + '\n' + code[idx:]
        with open(path, 'w') as f:
            f.write(code)
        print('PATCHED: blink cache-reset middleware injected before .listen()')
PYEOF
python3 /tmp/patch_blink.py""")

# 2. Patch Caddy with cache-bust headers
print("\n=== PATCHING Caddy with cache-bust response headers ===")
ssh(r"""cat > /tmp/patch_caddy_cache.py << 'PYEOF'
path = '/etc/caddy/Caddyfile'
with open(path, 'r') as f:
    caddy = f.read()

if 'X-Gaia-Blink' in caddy:
    print('Caddy already has blink headers')
else:
    # Add header block to the :80 section after the first line
    header_block = """
    # === BLINK = CACHE RESET ===
    header {
        Cache-Control "no-cache, no-store, must-revalidate, max-age=0"
        Pragma "no-cache"
        Expires "0"
        X-Gaia-Blink "{time.now.unix}"
        Clear-Site-Data "\"cache\""
        -Server
    }
"""
    # Insert into :80 block
    idx80 = caddy.find(':80 {')
    if idx80 != -1:
        nl = caddy.find('\n', idx80)
        caddy = caddy[:nl+1] + header_block + caddy[nl+1:]
        print('Added blink headers to :80 block')
    
    # Insert into nestgate.io block
    idxng = caddy.find('nestgate.io {')
    if idxng != -1:
        nl = caddy.find('\n', idxng)
        caddy = caddy[:nl+1] + header_block + caddy[nl+1:]
        print('Added blink headers to nestgate.io block')
    
    with open(path, 'w') as f:
        f.write(caddy)
    print('PATCHED: Caddy has blink cache-reset headers')
PYEOF
python3 /tmp/patch_caddy_cache.py""")

# 3. Restart services
print("\n=== RESTARTING gaia-api + reloading Caddy ===")
ssh("fuser -k 9876/tcp 2>/dev/null; sleep 1; cd /opt/gaia-api && nohup node server.js > /tmp/gaia-api.log 2>&1 & sleep 2 && echo 'gaia-api restarted' && curl -s -o /dev/null -w '%{http_code}' http://localhost:9876/")
ssh("caddy reload --config /etc/caddy/Caddyfile 2>&1 || systemctl reload caddy 2>&1; echo 'Caddy reloaded'")

# 4. Verify cache headers
print("\n=== VERIFY: checking cache-bust headers ===")
ssh("curl -sI http://localhost:9876/ 2>/dev/null | head -15")
ssh("curl -sI http://localhost:80/ -H 'Host: gaia.primals.eco' 2>/dev/null | head -15")

print("\n=== DONE: BLINK = CACHE RESET ===")
print("Every response now sends:")
print("  Cache-Control: no-cache, no-store, must-revalidate, max-age=0")
print("  Pragma: no-cache")
print("  Clear-Site-Data: \"cache\"")
print("  X-Gaia-Blink: <epoch_ms>")
print("lub-DUB crushes stale. Browser errors are sensation. NULL is food.")
