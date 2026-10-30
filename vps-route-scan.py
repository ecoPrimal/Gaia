"""Scan VPS gaia-api server.js for all routes and check which HTML files exist."""
import re, os, json
from pathlib import Path

server = open('/opt/gaia-api/server.js').read()

# Find all route patterns: p === '/something'
routes = set(re.findall(r"p === '(/[^']+)'", server))
# Also find p.startsWith patterns
starts = set(re.findall(r"p\.startsWith\('(/[^']+)'\)", server))

# Find all HTML files
static = Path('/opt/gaia-api/static')
html_files = {f.name for f in static.glob('*.html')}
data_files = {f.name for f in (static / 'data').glob('*.json')} if (static / 'data').exists() else set()

# Find all readFileSync references
reads = set(re.findall(r"readFileSync\('([^']+)'\)", server))

# Check which routes point to files that exist vs missing
results = {'alive': [], 'dead': [], 'routes': sorted(routes), 'starts': sorted(starts)}

for read_path in sorted(reads):
    exists = os.path.exists(read_path)
    if exists:
        results['alive'].append(read_path)
    else:
        results['dead'].append(read_path)

print(json.dumps({
    'total_routes': len(routes),
    'total_starts': len(starts),
    'html_files': len(html_files),
    'data_files': len(data_files),
    'alive_files': len(results['alive']),
    'dead_files': len(results['dead']),
    'dead': results['dead'],
    'routes': results['routes'][:40],
    'html_on_disk': sorted(html_files),
    'data_on_disk': sorted(data_files)
}, indent=2))
