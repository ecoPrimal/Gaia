#!/usr/bin/env python3
"""Add cache-bust response headers to Caddy for all Gaia domains"""
path = '/etc/caddy/Caddyfile'
with open(path, 'r') as f:
    caddy = f.read()

if 'X-Gaia-Blink' in caddy:
    print('Caddy already has blink headers')
else:
    header_block = '''
    # === BLINK = CACHE RESET ===
    header {
        Cache-Control "no-cache, no-store, must-revalidate, max-age=0"
        Pragma "no-cache"
        Expires "0"
        X-Gaia-Blink "{http.time_now}"
        Clear-Site-Data "\\"cache\\""
        -Server
    }
'''
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
    print('PATCHED: Caddy blink cache-reset headers added')
