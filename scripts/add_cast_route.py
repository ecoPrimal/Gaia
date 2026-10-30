#!/usr/bin/env python3
"""Add /cast /esoteric /web /neurons route to gaia-api server.js"""
import pathlib
p = pathlib.Path("/opt/gaia-api/server.js")
src = p.read_text(encoding="utf-8")
needle = "if (p === '/legend' || p === '/legends' || p === '/map' || p === '/maps')"
block = """if (p === '/cast' || p === '/esoteric' || p === '/web' || p === '/neurons') {
  try {
    var html = fs.readFileSync('/opt/gaia-api/static/cast.html', 'utf8');
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*' });
    return res.end(html);
  } catch(e) {
    return J(res, { ok: false, error: 'Cast page not found' }, 404);
  }
}
if (p === '/legend' || p === '/legends' || p === '/map' || p === '/maps')"""
if "/cast" in src and "cast.html" in src:
    print("cast route already present")
else:
    if needle not in src:
        # fallback: insert before deck
        needle2 = "if (p === '/deck' || p === '/space' || p === '/dos' || p === '/cmd')"
        block2 = block.replace(
            "if (p === '/legend' || p === '/legends' || p === '/map' || p === '/maps')",
            needle2
        )
        if needle2 not in src:
            raise SystemExit("could not find insertion point")
        src = src.replace(needle2, block2, 1)
    else:
        src = src.replace(needle, block, 1)
    p.write_text(src, encoding="utf-8")
    print("cast route inserted")
print("ok")
