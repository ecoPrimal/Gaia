with open('/etc/caddy/Caddyfile', 'r') as f:
    content = f.read()

# Replace the /api/pulse, /api/giggles, /api/all, /spine routes in nestgate.io HTTPS block
# Route through localhost:9876 (gaia-api) instead of 10.13.37.8:9878 directly
# gaia-api already has working spine proxy to Northgate

old_pulse = """\thandle /api/pulse {
\t\trewrite * /pulse
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""
new_pulse = """\thandle /api/pulse {
\t\trewrite * /spine/pulse
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""

old_giggles = """\thandle /api/giggles {
\t\trewrite * /giggles
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""
new_giggles = """\thandle /api/giggles {
\t\trewrite * /spine/giggles
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""

old_all = """\thandle /api/all {
\t\trewrite * /all
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""
new_all = """\thandle /api/all {
\t\trewrite * /spine/all
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""

old_spine = """\thandle /spine {
\t\trewrite * /all
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel spine
\t}
\thandle /spine/* {
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel spine
\t}"""
new_spine = """\thandle /spine {
\t\trewrite * /spine
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel spine
\t}
\thandle /spine/* {
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel spine
\t}"""

old_rss = """\thandle /rss/* {
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t\theader X-Gaia-Channel rss-spine
\t}
\thandle /rss {
\t\trewrite * /rss
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel rss-spine
\t}"""
new_rss = """\thandle /rss/* {
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t\theader X-Gaia-Channel rss-spine
\t}
\thandle /rss {
\t\treverse_proxy localhost:9876
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel rss-spine
\t}"""

fixes = [(old_pulse,new_pulse),(old_giggles,new_giggles),(old_all,new_all),(old_spine,new_spine),(old_rss,new_rss)]
count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new, 1)
        count += 1

with open('/etc/caddy/Caddyfile', 'w') as f:
    f.write(content)

print(f'Fixed {count}/5 blocks → all route through localhost:9876 (gaia-api)')
