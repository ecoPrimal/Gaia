// ═══ PLAY / GAME / VALVE ═══
    if (p === '/play' || p === '/game' || p === '/steam' || p === '/valve') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/play.html', 'utf8');
        J(res, null); res.writeHead(200, {'Content-Type':'text/html;charset=utf-8','Access-Control-Allow-Origin':'*'}); res.end(html);
      } catch(e) { J(res, {error:'play not found'},404); }
      return;
    }

    // ═══ LISP DESK ═══
    if (p === '/lisp' || p === '/lisp-desk') {
      try {
        var html = fs.readFileSync('/opt/gaia-api/static/lisp-desk.html', 'utf8');
        J(res, null); res.writeHead(200, {'Content-Type':'text/html;charset=utf-8','Access-Control-Allow-Origin':'*'}); res.end(html);
      } catch(e) { J(res, {error:'lisp not found'},404); }
      return;
    }

    // ═══ DATA FILES — structured JSON for SEO/crawlers/agents ═══
    if (p.startsWith('/data/') && p.endsWith('.json')) {
      try {
        var raw = fs.readFileSync('/opt/gaia-api/static' + p, 'utf8');
        res.writeHead(200, {'Content-Type':'application/json;charset=utf-8','Access-Control-Allow-Origin':'*'}); res.end(raw);
      } catch(e) { J(res, {error:'data not found: '+p},404); }
      return;
    }
