with open('/etc/caddy/Caddyfile', 'r') as f:
    content = f.read()

# Fix the broken rewrite-inside-reverse_proxy blocks
# Replace them with proper Caddy v2 syntax: rewrite THEN reverse_proxy

fixes = [
    # Fix /api/pulse
    (
        """\thandle /api/pulse {
\t\treverse_proxy 10.13.37.8:9878 {
\t\t\trewrite /pulse
\t\t}
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}""",
        """\thandle /api/pulse {
\t\trewrite * /pulse
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""
    ),
    # Fix /api/giggles
    (
        """\thandle /api/giggles {
\t\treverse_proxy 10.13.37.8:9878 {
\t\t\trewrite /giggles
\t\t}
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}""",
        """\thandle /api/giggles {
\t\trewrite * /giggles
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""
    ),
    # Fix /api/all
    (
        """\thandle /api/all {
\t\treverse_proxy 10.13.37.8:9878 {
\t\t\trewrite /all
\t\t}
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}""",
        """\thandle /api/all {
\t\trewrite * /all
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t}"""
    ),
    # Fix /spine
    (
        """\thandle /spine {
\t\treverse_proxy 10.13.37.8:9878 {
\t\t\trewrite /all
\t\t}
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel spine
\t}""",
        """\thandle /spine {
\t\trewrite * /all
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel spine
\t}"""
    ),
]

fixed = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        fixed += 1

# Also add /rss (without trailing slash) handler if missing
if 'handle /rss {' not in content:
    # Add it right after the /rss/* handler in the nestgate.io block
    rss_star = """\thandle /rss/* {
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Membrane-Metal gold
\t\theader X-Gaia-Channel rss-spine
\t}"""
    rss_both = rss_star + """
\thandle /rss {
\t\trewrite * /rss
\t\treverse_proxy 10.13.37.8:9878
\t\theader Access-Control-Allow-Origin *
\t\theader X-Gaia-Channel rss-spine
\t}"""
    if rss_star in content:
        content = content.replace(rss_star, rss_both, 1)
        fixed += 1

with open('/etc/caddy/Caddyfile', 'w') as f:
    f.write(content)

print(f'Fixed {fixed} blocks. Reloading Caddy...')
