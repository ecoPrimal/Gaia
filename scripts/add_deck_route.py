with open('/opt/gaia-api/server.js', 'r') as f:
    code = f.read()

deck_route = """if (p === '/deck' || p === '/space' || p === '/dos' || p === '/cmd') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/deck.html', 'utf8');
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
        return res.end(html);
      } catch(e) {
        return J(res, { ok: false, error: 'Deck page not found' }, 404);
      }
    }

    """

anchor = "if (p === '/record'"
if "'/deck'" not in code:
    code = code.replace(anchor, deck_route + anchor)

with open('/opt/gaia-api/server.js', 'w') as f:
    f.write(code)

print('Deck route installed')
