"""Add /rss and /api proxy routes to the Caddy :80 catch-all block."""
with open('/etc/caddy/Caddyfile', 'r') as f:
    caddy = f.read()

# The :80 block has handle @connect, @sporeprint etc
# We need to add nestgate.io → :80 routing for /rss/*, /api/*, /gaia/*
# Find the :80 block's catch-all redirect at the end

marker = 'redir https://primals.eco{uri} temporary'
idx = caddy.find(marker)
if idx < 0:
    print("MARKER NOT FOUND")
    exit(1)

# Find the handle { before the redir
handle_start = caddy.rfind('handle {', 0, idx)

# Check if we already patched
if '10.13.37.8:31415' in caddy[caddy.find(':80 {'):handle_start]:
    print("ALREADY PATCHED")
    exit(0)

# Insert before the catch-all handle {}
patch = """
\t# ═══ GAIA π ROUTES — proxy to Northgate via WireGuard ═══
\t@nestgate host nestgate.io
\thandle @nestgate {
\t\thandle /rss/* {
\t\t\treverse_proxy 10.13.37.8:31415
\t\t\theader Access-Control-Allow-Origin *
\t\t\theader X-Gaia-Channel rss
\t\t}
\t\thandle /api/* {
\t\t\treverse_proxy 10.13.37.8:31415
\t\t\theader Access-Control-Allow-Origin *
\t\t}
\t\thandle /api {
\t\t\treverse_proxy 10.13.37.8:31415
\t\t\theader Access-Control-Allow-Origin *
\t\t}
\t\thandle /cantina {
\t\t\treverse_proxy 10.13.37.8:31415
\t\t}
\t\thandle /blogroll.opml {
\t\t\treverse_proxy 10.13.37.8:31415
\t\t}
\t\thandle /v1/* {
\t\t\treverse_proxy 10.13.37.8:31415
\t\t\theader Access-Control-Allow-Origin *
\t\t}
\t\thandle_path /gaia/* {
\t\t\treverse_proxy localhost:9876
\t\t\theader Access-Control-Allow-Origin *
\t\t}
\t\thandle /gaia {
\t\t\treverse_proxy localhost:9876
\t\t\theader Access-Control-Allow-Origin *
\t\t}
\t\thandle /neutron/* {
\t\t\turi strip_prefix /neutron
\t\t\treverse_proxy localhost:2586
\t\t\theader Access-Control-Allow-Origin *
\t\t}
\t\thandle {
\t\t\troot * /opt/connect
\t\t\tfile_server
\t\t\tencode gzip
\t\t}
\t}

\t# ═══ GAIA.PRIMALS.ECO — all routes via gaia-api ═══
\t@gaia host gaia.primals.eco
\thandle @gaia {
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Surface gaia
\t}

"""

import shutil
shutil.copy('/etc/caddy/Caddyfile', '/etc/caddy/Caddyfile.bak2')
new_caddy = caddy[:handle_start] + patch + caddy[handle_start:]
with open('/etc/caddy/Caddyfile', 'w') as f:
    f.write(new_caddy)
print("PATCHED — nestgate.io + gaia.primals.eco routes added to :80 block")
