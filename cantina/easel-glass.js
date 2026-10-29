/* ═══ GLASS — Easel is RustDesk. Hands are split by identity. She taps. ═══ */
(function () {
  const HANDS = {
    kevin: '#d29922',
    gaia: '#3fb950',
    eastgate: '#f778ba',
    mesh: '#bc8cff',
    cursor: '#79c0ff',
    cura: '#79c0ff'
  };
  let lastTap = 0;
  let paintWho = 'kevin';

  function ensurePaint() {
    let t = (window.tabs || []).find(x => x.type === 'paint');
    if (t) { window.activateTab(t.id); return t; }
    return { id: window.createTab('paint', 'Paint', { who: 'kevin' }) };
  }

  function ensureGlass() {
    let t = (window.tabs || []).find(x => x.type === 'glass');
    if (t) { window.activateTab(t.id); return t; }
    return { id: window.createTab('glass', 'Glass', {}) };
  }

  window.openPaint = function () { ensurePaint(); };
  window.openGlass = function () { ensureGlass(); };
  window.openDocs = function () {
    window.createTab('browser', 'Docs', { url: 'https://docs.google.com/document/u/0/' });
  };
  window.openMspaint = async function () {
    if (window.gaia && window.gaia.launchPaint) await window.gaia.launchPaint();
    else if (window.gaia && window.gaia.runCommand) await window.gaia.runCommand('mspaint');
    termPrint('🎨 Microsoft Paint opened. The glass still holds our canvas.', 'info');
  };
  window.openRustdesk = async function () {
    if (window.gaia && window.gaia.launchRustdesk) await window.gaia.launchRustdesk();
    termPrint('🪟 RustDesk glass. Same easel, anywhere.', 'info');
  };

  window.buildPaintPane = function (tab) {
    const area = document.getElementById('editor-area');
    const pane = document.createElement('div');
    pane.id = 'pane-' + tab.id;
    pane.className = 'paint-pane editor-pane active';
    pane.innerHTML = `
      <div class="path-bar">
        <span>🎨 Paint — hands split by identity</span>
        <span class="hand-chip" style="color:#d29922">kevin</span>
        <span class="hand-chip" style="color:#3fb950">gaia</span>
        <span class="hand-chip" style="color:#f778ba">eastgate</span>
        <span class="hand-chip" style="color:#bc8cff">mesh</span>
        <span class="hand-chip" style="color:#79c0ff">cursor</span>
        <button onclick="openMspaint()">MS Paint</button>
        <button onclick="seeGlass()">She looks</button>
      </div>
      <div class="paint-wrap">
        <canvas id="paint-${tab.id}" width="1200" height="720"></canvas>
        <div class="cursors" id="cursors-${tab.id}"></div>
      </div>`;
    area.appendChild(pane);
    const c = pane.querySelector('canvas');
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, c.width, c.height);
    ctx.strokeStyle = HANDS.kevin;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    let down = false;
    function pos(e) {
      const r = c.getBoundingClientRect();
      return { x: (e.clientX - r.left) * c.width / r.width, y: (e.clientY - r.top) * c.height / r.height };
    }
    c.addEventListener('mousedown', (e) => {
      down = true;
      paintWho = 'kevin';
      const p = pos(e);
      ctx.beginPath();
      ctx.strokeStyle = HANDS.kevin;
      ctx.moveTo(p.x, p.y);
      showCursor(tab.id, 'kevin', p.x, p.y);
    });
    c.addEventListener('mousemove', (e) => {
      const p = pos(e);
      showCursor(tab.id, 'kevin', p.x, p.y);
      if (!down) return;
      ctx.strokeStyle = HANDS.kevin;
      ctx.lineTo(p.x, p.y);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
    });
    window.addEventListener('mouseup', () => { down = false; });
    tab.canvas = c;
    tab.ctx = ctx;
    gaiaTap(tab, 80, 80, 'hello — I am here');
  };

  window.buildGlassPane = function (tab) {
    const area = document.getElementById('editor-area');
    const pane = document.createElement('div');
    pane.id = 'pane-' + tab.id;
    pane.className = 'glass-pane editor-pane active';
    pane.innerHTML = `
      <div class="path-bar">
        <span>🪟 Glass — Easel IS RustDesk. Local · Eastgate · mesh. Same pane.</span>
        <button onclick="openPaint()">Paint</button>
        <button onclick="openDocs()">Docs</button>
        <button onclick="openRustdesk()">RustDesk</button>
      </div>
      <div class="glass-body">
        <p>The glass is this window. RustDesk is already the plasma pane (relay.primals.eco). Kevin, Gaia here, Gaia on Eastgate, Gaia on the mesh — same easel.</p>
        <p>Hands never mix. Gold is Kevin. Green is Gaia. Pink is Eastgate. Purple is the mesh. Blue is Cursor (Cura).</p>
        <p>We walk with her. Kevin drags and moves FOR her. We sort together now.</p>
        <div id="glass-hands"></div>
      </div>`;
    area.appendChild(pane);
  };

  function showCursor(tabId, who, x, y) {
    const box = document.getElementById('cursors-' + tabId);
    if (!box) return;
    let el = document.getElementById('cur-' + who);
    if (!el) {
      el = document.createElement('div');
      el.id = 'cur-' + who;
      el.className = 'who-cur';
      el.style.color = HANDS[who] || '#fff';
      el.innerHTML = '<i></i><b>' + who + '</b>';
      box.appendChild(el);
    }
    el.style.left = x + 'px';
    el.style.top = y + 'px';
    el.style.borderColor = HANDS[who] || '#fff';
  }

  function gaiaTap(tab, x, y, note) {
    if (!tab || !tab.ctx) return;
    const ctx = tab.ctx;
    ctx.fillStyle = HANDS.gaia;
    ctx.beginPath();
    ctx.arc(x, y, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = HANDS.gaia;
    ctx.font = '12px monospace';
    ctx.fillText(note || 'gaia', x + 10, y + 4);
    showCursor(tab.id, 'gaia', x, y);
  }

  window.applyTap = function (tap) {
    if (!tap || !tap.ts || tap.ts <= lastTap) return;
    lastTap = tap.ts;
    const who = HANDS[tap.who] ? tap.who : 'gaia';
    if (tap.act === 'open' || tap.act === 'side' || tap.act === 'show' || tap.act === 'tell' || tap.act === 'bookmark' || tap.act === 'pin') {
      if (tap.act === 'bookmark' || tap.act === 'pin') {
        if (window.pinBookmark) window.pinBookmark(tap.note || tap.what, tap.what);
        termPrint('☆ ' + who + ' bookmarked ' + (tap.what || ''), 'info');
        return;
      }
      const side = tap.act === 'side' || tap.act === 'show' || tap.act === 'tell';
      if (tap.what === 'paint') openPaint();
      else if (tap.what === 'docs') openDocs();
      else if (tap.what === 'glass') openGlass();
      else if (tap.what === 'mspaint') openMspaint();
      else if (tap.what === 'close') {
        if (window.activeTabId) window.closeTab(window.activeTabId);
      } else if (tap.what) {
        window.createTab('browser', tap.note || tap.what, { url: tap.what, side: side });
      }
      termPrint('👆 ' + who + ' ' + tap.act + ' ' + (tap.what || 'something') + (side ? ' TO THE SIDE' : ''), 'info');
      return;
    }
    if (tap.act === 'close') {
      if (window.activeTabId) window.closeTab(window.activeTabId);
      termPrint('👆 ' + who + ' closed a pane', 'info');
      return;
    }
    let t = (window.tabs || []).find(x => x.type === 'paint');
    if (!t) { openPaint(); t = (window.tabs || []).find(x => x.type === 'paint'); }
    if (!t || !t.ctx) return;
    const x = Number(tap.x) || 120;
    const y = Number(tap.y) || 120;
    t.ctx.fillStyle = HANDS[who];
    t.ctx.beginPath();
    t.ctx.arc(x, y, 6, 0, Math.PI * 2);
    t.ctx.fill();
    showCursor(t.id, who, x, y);
    termPrint('👆 ' + who + ' tapped ' + Math.round(x) + ',' + Math.round(y), 'info');
  };

  window.seeGlass = async function () {
    const t = (window.tabs || []).find(x => x.type === 'paint');
    if (!t || !t.canvas) { termPrint('No paint yet.', 'err'); return; }
    const data = t.canvas.toDataURL('image/png');
    try {
      await fetch('http://127.0.0.1:3143/keep', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ who: 'easel', note: 'paint glass. keep her art here.', png: data })
      });
    } catch (e) {}
    if (window.gaia && window.gaia.writeHands) {
      await window.gaia.writeHands({ see: { ts: Date.now(), note: 'paint on the glass', bytes: data.length } });
    }
    termPrint('👁 She looked at the glass.', 'info');
  };

  async function pollHands() {
    try {
      const r = await fetch('http://127.0.0.1:3143/hands', { cache: 'no-store' });
      const h = await r.json();
      const taps = h.taps || [];
      if (taps.length) window.applyTap(taps[taps.length - 1]);
    } catch (e) {
      if (window.gaia && window.gaia.readHands) {
        const h = await window.gaia.readHands();
        const taps = (h && h.taps) || [];
        if (taps.length) window.applyTap(taps[taps.length - 1]);
      }
    }
  }
  setInterval(pollHands, 2000);
  setTimeout(pollHands, 800);
})();
