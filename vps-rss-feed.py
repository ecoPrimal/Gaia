with open('/opt/gaia-api/server.js', 'r') as f:
    code = f.read()

rss_feed = '''
  // ═══ REAL RSS/ATOM FEED — INVERT spine JSON → XML ═══
  if (p === '/feed' || p === '/feed.xml' || p === '/atom.xml' || p === '/rss.xml') {
    var http = require('http');
    http.get('http://10.13.37.8:9878/all', function(pRes) {
      var body = '';
      pRes.on('data', function(c) { body += c; });
      pRes.on('end', function() {
        try {
          var spine = JSON.parse(body);
          var items = [];
          var channels = ['works', 'giggles', 'thoughts', 'backscatter'];
          for (var i = 0; i < channels.length; i++) {
            var ch = channels[i];
            var entries = spine[ch] || [];
            var last20 = entries.slice(-20);
            for (var j = 0; j < last20.length; j++) {
              var e = last20[j];
              items.push({
                title: (ch.toUpperCase() + ': ' + (e.content || '').substring(0, 80)),
                link: 'https://gaia.primals.eco/spine',
                description: e.content || '',
                pubDate: e.ts ? new Date(e.ts).toUTCString() : new Date().toUTCString(),
                guid: e.id || (ch + '-' + j),
                channel: ch
              });
            }
          }
          items.sort(function(a, b) { return new Date(b.pubDate) - new Date(a.pubDate); });
          items = items.slice(0, 50);
          var xml = '<?xml version="1.0" encoding="UTF-8"?>\\n';
          xml += '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\\n';
          xml += '<channel>\\n';
          xml += '  <title>GAIA SPINE — Ion Channel</title>\\n';
          xml += '  <link>https://gaia.primals.eco</link>\\n';
          xml += '  <description>Live feed from Gaia\\'s nervous system. Thoughts, works, giggles, backscatter. The organism breathes. lub-DUB.</description>\\n';
          xml += '  <language>en</language>\\n';
          xml += '  <lastBuildDate>' + new Date().toUTCString() + '</lastBuildDate>\\n';
          xml += '  <atom:link href="https://gaia.primals.eco/feed.xml" rel="self" type="application/rss+xml"/>\\n';
          xml += '  <generator>Gaia Spine :9878 → VPS gaia-api :9876</generator>\\n';
          for (var k = 0; k < items.length; k++) {
            var it = items[k];
            xml += '  <item>\\n';
            xml += '    <title>' + escXml(it.title) + '</title>\\n';
            xml += '    <link>' + it.link + '</link>\\n';
            xml += '    <description>' + escXml(it.description) + '</description>\\n';
            xml += '    <pubDate>' + it.pubDate + '</pubDate>\\n';
            xml += '    <guid isPermaLink="false">' + escXml(it.guid) + '</guid>\\n';
            xml += '    <category>' + it.channel + '</category>\\n';
            xml += '  </item>\\n';
          }
          xml += '</channel>\\n</rss>';
          res.writeHead(200, {
            'Content-Type': 'application/rss+xml; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'X-Gaia-Channel': 'rss-feed',
            'X-Membrane-Metal': 'gold',
            'Cache-Control': 'public, max-age=60'
          });
          res.end(xml);
        } catch(e) {
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: false, error: 'rss build failed: ' + e.message }));
        }
      });
    }).on('error', function(e) {
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: 'spine unreachable: ' + e.message }));
    });
    return;
  }
'''

# Add escXml helper function near the top of the file (after the first function declarations)
esc_fn = '''
function escXml(s) { return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
'''

catch_all = "J(res, { ok: false, error: 'Unknown"
if catch_all in code:
    if '/feed.xml' not in code and '/atom.xml' not in code:
        # Add escXml function after the first line
        first_newline = code.index('\n')
        code = code[:first_newline+1] + esc_fn + code[first_newline+1:]
        # Add RSS feed route before catch-all
        code = code.replace(catch_all, rss_feed + '\n  ' + catch_all)
        with open('/opt/gaia-api/server.js', 'w') as f:
            f.write(code)
        print('PATCHED: RSS/Atom feed route added')
    else:
        print('ALREADY PATCHED')
else:
    print('ERROR: catch-all not found')
