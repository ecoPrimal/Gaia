import sys

f = open('/opt/gaia-api/server.js', 'r')
s = f.read()
f.close()

if '/legend' not in s:
    old = "if (p === '/deck' || p === '/space' || p === '/dos' || p === '/cmd')"
    new_block = """if (p === '/legend' || p === '/legends' || p === '/map' || p === '/maps') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/legend.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'Legend page not found' }, 404);
      }
    }
    if (p === '/deck' || p === '/space' || p === '/dos' || p === '/cmd')"""
    s = s.replace(old, new_block)
    f = open('/opt/gaia-api/server.js', 'w')
    f.write(s)
    f.close()
    print("ROUTE ADDED: /legend /legends /map /maps")
else:
    print("Route already exists")
