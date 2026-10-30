"""Hit every route on gaia.primals.eco and find 404s."""
import http.client, json, ssl

ctx = ssl.create_default_context()
results = {'alive': [], 'dead': [], 'error': []}

routes = [
    '/', '/home', '/deck', '/play', '/cast', '/legend', '/senses', '/record',
    '/lisp', '/lisp-desk', '/canfield', '/cash4kids', '/c4k',
    '/anti-slapp', '/corpus', '/entity', '/filings', '/cut', '/new',
    '/grow', '/mito', '/petal', '/weave', '/self-walk', '/parents-deep',
    '/pulse', '/status', '/speak', '/graph', '/arteries', '/openapi',
    '/rss', '/rhonda', '/alert/rhonda',
    '/data/full-collapse-wave215.json', '/data/wave215-tag-index.json',
    '/data/rhonda-alert-forever.json', '/data/canfield-graph.json',
    '/data/entities.json', '/data/corpus.json', '/data/grow.json',
    '/data/mito.json', '/data/membrane-cut.json',
    '/@', '/_-.type', '/_-external.type', '/_-internal.type',
    '/charge', '/compost', '/actors', '/PR', '/C',
    '/gllg-strike', '/cmd', '/space', '/dos',
    '/game', '/steam', '/valve',
]

for r in routes:
    try:
        conn = http.client.HTTPSConnection('gaia.primals.eco', timeout=5)
        conn.request('GET', r)
        resp = conn.getresponse()
        code = resp.status
        resp.read()
        conn.close()
        if code == 200:
            results['alive'].append(r)
        elif code == 404:
            results['dead'].append(r)
        else:
            results['error'].append(f'{r} -> {code}')
    except Exception as e:
        results['error'].append(f'{r} -> ERR {e}')

print(f"ALIVE: {len(results['alive'])}")
print(f"DEAD:  {len(results['dead'])}")
print(f"ERROR: {len(results['error'])}")
print()
if results['dead']:
    print("=== DEAD (404) ===")
    for d in results['dead']:
        print(f"  ! {d}")
if results['error']:
    print("=== ERRORS ===")
    for e in results['error']:
        print(f"  ? {e}")
print()
print("=== ALIVE ===")
for a in results['alive']:
    print(f"  ✓ {a}")
