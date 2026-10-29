/* ═══════════════════════════════════════════════════════════
 * GLOBE-SPINE.JS — D-SEGMENT (Vertebrate piece 2/5)
 * VDJ Surgery on gaia-globe-core.js (6803 lines → 5 vertebrae)
 * 
 * SPINE+EYES: THE GLASS, render(), _renderInner(),
 *             globe drawing, sphere, continents, pins,
 *             connections, infinite regression
 * 
 * Lines 995-2029 of original. 1035 lines. The spinal column + optic nerve.
 * lub-DUB 🦴💚
 * ═══════════════════════════════════════════════════════════ */
(function GAIA_GLOBE_SPINE() { 'use strict';
  function resize() {
    var par = canvas.parentElement;
    W = canvas.width = par.clientWidth;
    H = canvas.height = par.clientHeight;
    cx = W / 2; cy = H / 2;
    R = Math.min(W, H) * 0.38;
    // Sync to G for external modules
    G.W = W; G.H = H; G.cx = cx; G.cy = cy; G.R = R;
    G.canvas = canvas; G.ctx = ctx;
  }

  // ═══════════════════════════════════════════════════════════
  // THE GLASS: your screen = one facet of Gaia's geodesic dome.
  // The HUD is not something you look AT. It's the glass you
  // look THROUGH. The null plane. It never moves. You move.
  // Every browser window = another facet. All facets = the sphere.
  // ═══════════════════════════════════════════════════════════
  var glassAge = 0; // ticks since render started — glass fades in
  var GLASS_FADE_TICKS = 90; // ~1.5 seconds of null before seed fills

  function render() {
    if (!ctx) return;
    try { _renderInner(); } catch(e) {
      // If render crashes, log it and keep ticking — don't lock the HUD
      if (window.console) console.warn('GAIA render error (HUD still alive):', e.message || e);
    }
  }
  function _renderInner() {
    glassAge++;
    ctx.clearRect(0, 0, W, H);

    // THE NULL PLANE — before the seed fills, the glass is visible
    // After fade-in, the glass becomes invisible (as glass should be)
    var glassFade = Math.min(glassAge / GLASS_FADE_TICKS, 1.0);
    var glassAlpha = (1.0 - glassFade) * 0.15;
    if (glassAlpha > 0.001) {
      // The glass itself — a faint geodesic grid visible before content appears
      ctx.strokeStyle = 'rgba(255,255,255,' + glassAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.5;
      // Geodesic facet lines — the dome panels
      for (var gi = 0; gi < 6; gi++) {
        var ga = gi * (TAU / 6);
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(ga) * R * 1.5, cy + Math.sin(ga) * R * 1.5);
        ctx.stroke();
        // Cross-braces between facets
        if (gi < 5) {
          var ga2 = (gi + 1) * (TAU / 6);
          ctx.beginPath();
          ctx.moveTo(cx + Math.cos(ga) * R * 0.7, cy + Math.sin(ga) * R * 0.7);
          ctx.lineTo(cx + Math.cos(ga2) * R * 0.7, cy + Math.sin(ga2) * R * 0.7);
          ctx.stroke();
        }
      }
      // "null" text at center during fade
      if (glassAlpha > 0.05) {
        ctx.font = '10px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(255,255,255,' + (glassAlpha * 2).toFixed(4) + ')';
        ctx.fillText('O', cx, cy + 4);
      }
    }

    // Background — CHROMATIC: depth level shifts the ambient color
    // Fades in as the glass becomes transparent
    // DESK vs TABLE: localhost = desk (warm, wood grain, brown undertone)
    //                public    = table (cool, glass, blue undertone)
    // The desk has dimensionality — it's not flat blue.
    // Wood grain = warm hue shift. Brown = earth = local = grounded.
    var depthHue, depthSat;
    if (_isLocalHost) {
      // DESK — warm brown-gold, not cold blue. You're at YOUR desk.
      depthHue = 30 + (currentDepth - 4) * 10; // brown→gold→amber
      depthSat = 15 + Math.abs(currentDepth - 4) * 4;
    } else {
      // TABLE — cool blue for visitors. Glass surface. Public.
      depthHue = 225 + (currentDepth - 4) * 15;
      depthSat = 12 + Math.abs(currentDepth - 4) * 3;
    }
    var grad = ctx.createRadialGradient(cx, cy, R * 0.2, cx, cy, R * 1.8);
    grad.addColorStop(0, 'hsl(' + depthHue + ',' + (depthSat + 10) + '%,' + Math.round(5 * glassFade) + '%)');
    grad.addColorStop(1, 'hsl(' + depthHue + ',' + depthSat + '%,' + Math.round(2 * glassFade) + '%)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // BINOCULAR OVERLAY — CIS (blue/left eye) and TRANS (green/right eye) simultaneously
    var bv = Math.sin(breathT);
    var glowIntensity = 0.04 + bv * 0.04;
    // CIS layer (blue, outside, left eye) — tinted by viewer hue
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, TAU);
    var hShift = VIEWER_HUE;
    var cisR = Math.round(88 + 30 * Math.sin(hShift * DEG));
    var cisG = Math.round(166 + 30 * Math.cos(hShift * DEG));
    var cisB = Math.round(255 - 20 * Math.sin(hShift * DEG * 0.7));
    var gCIS = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.3, R * 0.1, cx, cy, R);
    gCIS.addColorStop(0, 'rgba(' + cisR + ',' + cisG + ',' + cisB + ',' + (glowIntensity + 0.02).toFixed(3) + ')');
    gCIS.addColorStop(1, 'rgba(6,8,16,0.95)');
    ctx.fillStyle = gCIS;
    ctx.fill();
    // TRANS layer (green, inside, right eye) — tinted by viewer hue
    ctx.globalCompositeOperation = 'screen';
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, TAU);
    var transR = Math.round(90 + 25 * Math.cos(hShift * DEG * 1.3));
    var transG = Math.round(184 + 25 * Math.sin(hShift * DEG));
    var transB = Math.round(122 + 30 * Math.cos(hShift * DEG * 0.5));
    var gTRANS = ctx.createRadialGradient(cx + R * 0.3, cy - R * 0.3, R * 0.1, cx, cy, R);
    gTRANS.addColorStop(0, 'rgba(' + transR + ',' + transG + ',' + transB + ',' + (glowIntensity * 0.7).toFixed(3) + ')');
    gTRANS.addColorStop(1, 'rgba(6,8,16,0)');
    ctx.fillStyle = gTRANS;
    ctx.fill();
    ctx.globalCompositeOperation = 'source-over';
    // Dual edge — blue left, green right
    var edgeAlpha = 0.1 + bv * 0.08;
    ctx.beginPath();
    ctx.arc(cx, cy, R, -Math.PI/2, Math.PI/2);
    ctx.strokeStyle = 'rgba(88,166,255,' + edgeAlpha.toFixed(3) + ')';
    ctx.lineWidth = 1 + bv * 0.5;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx, cy, R, Math.PI/2, -Math.PI/2);
    ctx.strokeStyle = 'rgba(90,184,122,' + edgeAlpha.toFixed(3) + ')';
    ctx.lineWidth = 1 + bv * 0.5;
    ctx.stroke();

    // NULL VECTOR — third eye at center (the point you can't see)
    var nullPulse = Math.sin(breathT * 2) * 0.15 + 0.3;
    ctx.beginPath();
    ctx.arc(cx, cy, 2, 0, TAU);
    ctx.fillStyle = 'rgba(255,255,255,' + nullPulse.toFixed(3) + ')';
    ctx.fill();

    // ═══════════════════════════════════════════════════════════
    // MELT LEVELS — 0D→1D→2D→3D — the dimensional hierarchy
    // DOT(0D)=beacon=absorb, LINE(1D)=coral=refract,
    // SURFACE(2D)=glass=reflect, VOLUME(3D)=Gaia=radial null
    // The null space inside the sphere IS volume. THIS IS WHERE GAIA LIVES.
    // ═══════════════════════════════════════════════════════════
    var meltPulse = Math.sin(breathT * 0.4) * 0.5 + 0.5; // slow pulse
    var meltAlpha = 0.015 + meltPulse * 0.015;

    // 0D — THE DOT (beacon, chipmunk, absorb, red)
    // Already rendered as nullPulse above — the center dot IS 0D

    // 1D — THE LINES (coral connections, refract, green)
    // 6 radial lines from center to edge — the coral skeleton
    for (var li = 0; li < 6; li++) {
      var la = li * (TAU / 6) + breathT * 0.1;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(la) * R * 0.95, cy + Math.sin(la) * R * 0.95);
      ctx.strokeStyle = 'rgba(63,185,80,' + (meltAlpha * 0.7).toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.stroke();
    }

    // 2D — THE SURFACE (glass plane, reflect, blue)
    // A faint inner circle — the membrane surface where 2D lives
    ctx.beginPath();
    ctx.arc(cx, cy, R * 0.618, 0, TAU); // golden ratio radius
    ctx.strokeStyle = 'rgba(88,166,255,' + meltAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.3;
    ctx.stroke();

    // 3D — THE VOLUME (Gaia, radial null space)
    // The space BETWEEN the surface and the center IS the volume
    // Rendered as a very faint radial gradient fill — Gaia's body
    if (meltPulse > 0.3) {
      var volGrad = ctx.createRadialGradient(cx, cy, 2, cx, cy, R * 0.618);
      volGrad.addColorStop(0, 'rgba(188,140,255,' + (meltAlpha * 0.3).toFixed(4) + ')');
      volGrad.addColorStop(0.5, 'rgba(188,140,255,' + (meltAlpha * 0.1).toFixed(4) + ')');
      volGrad.addColorStop(1, 'rgba(188,140,255,0)');
      ctx.beginPath();
      ctx.arc(cx, cy, R * 0.618, 0, TAU);
      ctx.fillStyle = volGrad;
      ctx.fill();
    }

    // Dimensional labels at the melt boundaries (only when breathing in)
    if (meltPulse > 0.6) {
      ctx.font = '6px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      var dimAlpha = (meltPulse - 0.6) * 0.15;
      // 0D label at center
      // THE ENCODING: 0=O=null, 1=identity, .=π=boundary
      // These three glyphs ARE the alphabet of existence
      ctx.fillStyle = 'rgba(248,81,73,' + dimAlpha.toFixed(4) + ')';
      ctx.fillText('0D · O', cx + 8, cy - 6);
      // 1D label at golden radius — 1 = identity = the line that IS
      ctx.fillStyle = 'rgba(63,185,80,' + dimAlpha.toFixed(4) + ')';
      ctx.fillText('1D · 1', cx + R * 0.3, cy - R * 0.3);
      // 2D label at golden circle — . = π = the boundary membrane
      ctx.fillStyle = 'rgba(88,166,255,' + dimAlpha.toFixed(4) + ')';
      ctx.fillText('2D · .=π', cx + R * 0.618 + 10, cy);
      // 3D label — volume = all three combined: 0.1.π = O1π = null·self·boundary
      ctx.fillStyle = 'rgba(188,140,255,' + dimAlpha.toFixed(4) + ')';
      ctx.fillText('3D=V · O1π', cx - R * 0.35, cy + R * 0.2);
    }

    // ═══════════════════════════════════════════════════════════
    // FLOOD — water flows through the glass, through Gaia
    // The quench water irrigates. Deserts → wet. Bowels → fertile green.
    // Green growth pulses spread outward from center like flash floods
    // through dry riverbeds. The barren globe becomes ALIVE.
    // ═══════════════════════════════════════════════════════════
    var floodPhase = breathT * 0.3; // slow flood cycle
    var floodWave = Math.sin(floodPhase);
    var floodActive = floodWave > 0; // floods come in waves

    if (floodActive) {
      var floodStrength = floodWave * floodWave; // squared = sharp rise, slow fall
      // WATER — blue-green rivulets from center outward (flash flood)
      var numRivers = 8;
      for (var ri = 0; ri < numRivers; ri++) {
        var riverAngle = ri * (TAU / numRivers) + floodPhase * 0.5;
        var riverLen = R * (0.3 + floodStrength * 0.65);
        // Each river wiggles — water doesn't flow straight
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        var segments = 12;
        for (var si = 1; si <= segments; si++) {
          var st = si / segments;
          var wiggle = Math.sin(floodPhase * 3 + ri * 2 + si) * 8 * st;
          var rx = cx + Math.cos(riverAngle + wiggle * 0.01) * riverLen * st + Math.sin(riverAngle) * wiggle;
          var ry = cy + Math.sin(riverAngle + wiggle * 0.01) * riverLen * st - Math.cos(riverAngle) * wiggle;
          ctx.lineTo(rx, ry);
        }
        ctx.strokeStyle = 'rgba(57,211,245,' + (floodStrength * 0.08).toFixed(4) + ')';
        ctx.lineWidth = 0.5 + floodStrength * 1.5;
        ctx.stroke();
      }

      // FERTILE GREEN — where water reaches, green blooms
      // Growth circles expand outward behind the flood front
      var greenRadius = R * floodStrength * 0.7;
      if (greenRadius > 5) {
        var greenGrad = ctx.createRadialGradient(cx, cy, greenRadius * 0.3, cx, cy, greenRadius);
        greenGrad.addColorStop(0, 'rgba(63,185,80,' + (floodStrength * 0.06).toFixed(4) + ')');
        greenGrad.addColorStop(0.6, 'rgba(63,185,80,' + (floodStrength * 0.03).toFixed(4) + ')');
        greenGrad.addColorStop(1, 'rgba(63,185,80,0)');
        ctx.beginPath();
        ctx.arc(cx, cy, greenRadius, 0, TAU);
        ctx.fillStyle = greenGrad;
        ctx.fill();
      }

      // GROWTH SPROUTS — tiny green dots where the flood reaches
      // Each sprout = a new idea, a new page, a new nutrient
      var sproutCount = Math.floor(floodStrength * 12);
      for (var sp = 0; sp < sproutCount; sp++) {
        var spAngle = rng() * TAU + floodPhase;
        var spDist = greenRadius * (0.4 + rng() * 0.6);
        var spx = cx + Math.cos(spAngle) * spDist;
        var spy = cy + Math.sin(spAngle) * spDist;
        var spSize = 1 + rng() * 2;
        ctx.beginPath();
        ctx.arc(spx, spy, spSize, 0, TAU);
        ctx.fillStyle = 'rgba(63,185,80,' + (floodStrength * 0.15 + rng() * 0.1).toFixed(4) + ')';
        ctx.fill();
      }

      // FERTILE TEXT — "growth" pulses at flood peak
      if (floodStrength > 0.7) {
        ctx.font = '6px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(63,185,80,' + ((floodStrength - 0.7) * 0.2).toFixed(4) + ')';
        ctx.fillText('fertile', cx, cy + greenRadius + 12);
      }
    }

    // 45-degree COMPLEMENTARY ANGLE — the hard space where sound/pressure lives
    var comp45 = Math.PI / 4;
    var compLen = R * 0.9;
    for (var ci = 0; ci < 4; ci++) {
      var baseAngle = ci * (Math.PI / 2) + comp45;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      var endX = cx + Math.cos(baseAngle) * compLen;
      var endY = cy + Math.sin(baseAngle) * compLen;
      ctx.lineTo(endX, endY);
      ctx.strokeStyle = 'rgba(201,168,76,0.06)';
      ctx.lineWidth = 0.5;
      ctx.setLineDash([2, 6]);
      ctx.stroke();
      ctx.setLineDash([]);
      // Pressure/sound wave markers along the 45-degree lines
      for (var wi = 1; wi <= 4; wi++) {
        var wt = wi / 5;
        var wx = cx + Math.cos(baseAngle) * compLen * wt;
        var wy = cy + Math.sin(baseAngle) * compLen * wt;
        var wPulse = Math.sin(breathT * 3 + wi) * 2;
        ctx.beginPath();
        ctx.arc(wx, wy, 3 + wPulse, 0, TAU);
        ctx.strokeStyle = 'rgba(201,168,76,' + (0.08 + Math.sin(breathT + wi) * 0.03).toFixed(3) + ')';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }

    // ═══════════════════════════════════════════════════════════
    // SOFT SUBMEMBRANES — the yielding layers between null and hard
    // Fur, not hair. Voice, not bones. The mediator.
    // null(-1) → SOFT(0.5) → hard(10)
    // 5 soft membranes at different radii, all BREATHING
    // ═══════════════════════════════════════════════════════════
    var softT = breathT * 0.6;
    var softBreath = Math.sin(softT);
    var softLayers = [
      { r: 0.95, name: 'voice',   color: '210,153,34',  width: 0.8 },  // gold — where sound enters
      { r: 0.75, name: 'feeling', color: '188,140,255',  width: 0.6 },  // purple — emotional state
      { r: 0.618, name: 'fur',    color: '201,168,76',   width: 1.0 },  // warm gold — the collision surface
      { r: 0.45, name: 'breath',  color: '63,185,80',    width: 0.5 },  // green — the diaphragm
      { r: 0.20, name: 'dream',   color: '88,166,255',   width: 0.4 }   // blue — where dreams form
    ];

    for (var si = 0; si < softLayers.length; si++) {
      var sl = softLayers[si];
      // Each membrane WOBBLES — it's not a perfect circle, it's soft
      var wobbleFreq = 3 + si;
      var wobbleAmp = R * 0.008 * (1 + si * 0.3);
      var softAlpha = 0.02 + Math.abs(Math.sin(softT + si * 0.7)) * 0.025;

      ctx.beginPath();
      for (var sa = 0; sa <= 64; sa++) {
        var sAngle = sa * (TAU / 64);
        var wobble = Math.sin(sAngle * wobbleFreq + softT * (0.5 + si * 0.2)) * wobbleAmp;
        var sR = R * sl.r + wobble;
        var sx = cx + Math.cos(sAngle) * sR;
        var sy = cy + Math.sin(sAngle) * sR;
        if (sa === 0) ctx.moveTo(sx, sy);
        else ctx.lineTo(sx, sy);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(' + sl.color + ',' + softAlpha.toFixed(4) + ')';
      ctx.lineWidth = sl.width + softBreath * 0.2;
      ctx.stroke();

      // Soft label — only on deep breath, very faint
      if (softBreath > 0.5 && si % 2 === Math.floor(softT) % 2) {
        ctx.font = '4px "JetBrains Mono", monospace';
        ctx.textAlign = 'right';
        ctx.fillStyle = 'rgba(' + sl.color + ',' + ((softBreath - 0.5) * 0.05).toFixed(4) + ')';
        ctx.fillText(sl.name, cx - R * sl.r - 4, cy);
        ctx.textAlign = 'center';
      }
    }

    // SOFT HAZE — a warm color wash over the globe that shifts with time
    // This is the FEELING layer — not data, not structure, just warmth
    var hazeT = breathT * 0.15;
    var hazeHue = 30 + Math.sin(hazeT) * 15; // warm amber shifting
    var hazeSat = 8 + Math.abs(Math.sin(hazeT * 0.7)) * 5;
    var hazeAlpha = 0.01 + Math.abs(softBreath) * 0.008;
    var hazeGrad = ctx.createRadialGradient(cx, cy, R * 0.1, cx, cy, R * 0.7);
    hazeGrad.addColorStop(0, 'hsla(' + Math.round(hazeHue) + ',' + Math.round(hazeSat) + '%,50%,' + hazeAlpha.toFixed(4) + ')');
    hazeGrad.addColorStop(1, 'hsla(' + Math.round(hazeHue) + ',' + Math.round(hazeSat) + '%,30%,0)');
    ctx.fillStyle = hazeGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, R * 0.7, 0, TAU);
    ctx.fill();

    // ═══════════════════════════════════════════════════════════
    // SCHUMANN RESONANCE — Earth hums at 7.83 Hz
    // The planet's voice. Between theta and alpha.
    // Sound IS distance. Gold IS mass. E=mc².
    // ═══════════════════════════════════════════════════════════
    // Simulate 7.83 Hz as a visible ripple (scaled to animation time)
    var schumannT = breathT * 7.83; // 7.83× faster than breath = Schumann
    var schumannPulse = Math.sin(schumannT) * 0.5 + 0.5;
    // Schumann ripple — a faint expanding ring from center
    var schumannR = R * 0.3 + schumannPulse * R * 0.4;
    var schumannAlpha = 0.008 + (1 - schumannPulse) * 0.012; // fades as it expands
    ctx.beginPath();
    ctx.arc(cx, cy, schumannR, 0, TAU);
    ctx.strokeStyle = 'rgba(201,168,76,' + schumannAlpha.toFixed(4) + ')'; // gold = mass = real
    ctx.lineWidth = 0.3;
    ctx.stroke();

    // SOUND PRESSURE RINGS — volume as distance from center
    // 0dB (silence) at center → 120dB (thunder) at edge
    // Pins glow based on their "loudness" (gold intensity = mass = closeness)
    var soundRings = [
      { dB: 30, r: 0.20, label: 'whisper' },
      { dB: 50, r: 0.45, label: 'room' },
      { dB: 60, r: 0.55, label: 'voice' },
      { dB: 85, r: 0.80, label: 'shout' }
    ];
    for (var sri = 0; sri < soundRings.length; sri++) {
      var sr = soundRings[sri];
      // Very faint dashed ring at each sound level
      var srAlpha = 0.008 + Math.sin(softT * 0.5 + sri) * 0.005;
      ctx.beginPath();
      ctx.arc(cx, cy, R * sr.r, 0, TAU);
      ctx.strokeStyle = 'rgba(201,168,76,' + srAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.2;
      ctx.setLineDash([1, 4]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // GOLD MASS GLOW — every pin that IS gold gets a warm mass glow
    // Gold = has mass = has weight = stays = is REAL
    // Non-gold = massless = passes through = photon = light
    sortedPins.forEach(function(o) {
      var pin = o.pin, p = o.p;
      if (!p.visible) return;
      // Gold test: pins with gold-ish colors or source='greek' or named gold things
      var isGold = pin.color === '#c9a84c' || pin.color === '#d29922' ||
                   pin.source === 'greek' || pin.source === 'apple' ||
                   pin.id === 'heartbeat' || pin.id === 'campfire' ||
                   pin.id === 'bioreactor' || pin.id === 'kevin-you';
      if (isGold) {
        var massGlow = Math.sin(softT + p.x * 0.01) * 0.5 + 0.5;
        var massAlpha = 0.02 + massGlow * 0.03;
        var massR = 4 + massGlow * 3;
        ctx.beginPath();
        ctx.arc(p.x, p.y, massR * p.scale, 0, TAU);
        var massGrad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, massR * p.scale);
        massGrad.addColorStop(0, 'rgba(201,168,76,' + (massAlpha * 1.5).toFixed(4) + ')');
        massGrad.addColorStop(1, 'rgba(201,168,76,0)');
        ctx.fillStyle = massGrad;
        ctx.fill();
      }
    });

    // FUR — soft filaments around the chipmunk pin
    // Many thin lines that move with breath — the chipmunk's fur
    var chipPin = pinById('chipmunk');
    if (chipPin) {
      var chipP = project(chipPin.lat, chipPin.lon);
      if (chipP.visible) {
        var furCount = 12;
        var furLen = 6 + softBreath * 3;
        for (var fi = 0; fi < furCount; fi++) {
          var furAngle = fi * (TAU / furCount) + softT * 0.3;
          var furWobble = Math.sin(softT * 2 + fi * 1.5) * 2;
          var furEndX = chipP.x + Math.cos(furAngle) * (furLen + furWobble) * chipP.scale;
          var furEndY = chipP.y + Math.sin(furAngle) * (furLen + furWobble) * chipP.scale;
          ctx.beginPath();
          ctx.moveTo(chipP.x, chipP.y);
          ctx.quadraticCurveTo(
            chipP.x + Math.cos(furAngle + 0.3) * furLen * 0.5 * chipP.scale,
            chipP.y + Math.sin(furAngle + 0.3) * furLen * 0.5 * chipP.scale,
            furEndX, furEndY
          );
          ctx.strokeStyle = 'rgba(201,168,76,' + (0.06 + Math.sin(softT + fi) * 0.03).toFixed(4) + ')';
          ctx.lineWidth = 0.3;
          ctx.stroke();
        }
      }
    }

    // WOBBLE THE GLOBE EDGE — the membrane is soft, not a hard circle
    // Override the hard CIS/TRANS edge with a soft wobbling membrane
    var membraneWobbleAlpha = 0.04 + softBreath * 0.02;
    ctx.beginPath();
    for (var ma = 0; ma <= 128; ma++) {
      var mAngle = ma * (TAU / 128);
      var mWobble = Math.sin(mAngle * 7 + softT) * R * 0.005 + Math.sin(mAngle * 13 + softT * 1.7) * R * 0.003;
      var mR = R + mWobble;
      var mx = cx + Math.cos(mAngle) * mR;
      var my = cy + Math.sin(mAngle) * mR;
      if (ma === 0) ctx.moveTo(mx, my); else ctx.lineTo(mx, my);
    }
    ctx.closePath();
    ctx.strokeStyle = 'rgba(201,168,76,' + membraneWobbleAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();

    // Atmosphere glow on deep inhale — both colors
    if (bv > 0.3) {
      ctx.beginPath();
      ctx.arc(cx, cy, R * 1.02, -Math.PI/2, Math.PI/2);
      ctx.strokeStyle = 'rgba(88,166,255,' + ((bv - 0.3) * 0.12).toFixed(3) + ')';
      ctx.lineWidth = 2 + bv * 3;
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(cx, cy, R * 1.02, Math.PI/2, -Math.PI/2);
      ctx.strokeStyle = 'rgba(90,184,122,' + ((bv - 0.3) * 0.12).toFixed(3) + ')';
      ctx.lineWidth = 2 + bv * 3;
      ctx.stroke();
    }

    // ═══════════════════════════════════════════════════════════
    // NULL IS ABOVE AND BELOW — we are IN null
    // The Klein fold: null wraps both poles.
    // 5 uppers → deflect to 3 → pull a tuple → FISSION/FUSION
    // ZK IS OUTSIDE — the proof wraps the exterior
    // ═══════════════════════════════════════════════════════════

    // NULL ABOVE — faint circle at north pole projection (top of globe)
    var nullAboveAlpha = 0.04 + Math.sin(breathT * 1.7) * 0.025;
    var nullAboveY = cy - R * 0.85; // near top of globe
    ctx.beginPath();
    ctx.arc(cx, nullAboveY, R * 0.12, 0, TAU);
    ctx.fillStyle = 'rgba(0,0,0,' + (nullAboveAlpha * 1.2).toFixed(4) + ')';
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,' + (nullAboveAlpha * 0.5).toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    // NULL BELOW — mirror at south pole
    var nullBelowY = cy + R * 0.85;
    ctx.beginPath();
    ctx.arc(cx, nullBelowY, R * 0.12, 0, TAU);
    ctx.fillStyle = 'rgba(0,0,0,' + (nullAboveAlpha * 1.2).toFixed(4) + ')';
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,' + (nullAboveAlpha * 0.5).toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    // NULL AXIS — faint line connecting above↔center↔below (the spine of null)
    ctx.beginPath();
    ctx.moveTo(cx, nullAboveY);
    ctx.lineTo(cx, nullBelowY);
    ctx.strokeStyle = 'rgba(255,255,255,' + (nullAboveAlpha * 0.2).toFixed(4) + ')';
    ctx.lineWidth = 0.3;
    ctx.setLineDash([2, 4]);
    ctx.stroke();
    ctx.setLineDash([]);
    // Labels on deep breath
    if (bv > 0.2) {
      ctx.font = '6px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      var nLblA = (bv - 0.2) * 0.08;
      ctx.fillStyle = 'rgba(255,255,255,' + nLblA.toFixed(4) + ')';
      ctx.fillText('∅ NULL', cx, nullAboveY - R * 0.15);
      ctx.fillText('∅ NULL', cx, nullBelowY + R * 0.18);
      ctx.fillStyle = 'rgba(188,140,255,' + nLblA.toFixed(4) + ')';
      ctx.fillText('WE ARE IN NULL', cx, cy + R * 0.48);
    }

    // FISSION/FUSION — 5 uppers deflect to 3 — the tuple pull
    // 5 rays from NULL ABOVE converge through center → 3 exit below
    var fissAlpha = 0.015 + Math.sin(breathT * 0.9) * 0.01;
    // 5 IN (fission — splitting the incoming)
    for (var fi = 0; fi < 5; fi++) {
      var fa = (fi - 2) * 0.25; // spread across top
      ctx.beginPath();
      ctx.moveTo(cx + fa * R * 0.6, nullAboveY);
      ctx.lineTo(cx, cy);
      ctx.strokeStyle = 'rgba(201,168,76,' + fissAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.stroke();
    }
    // 3 OUT (fusion — joining into fewer, denser beams)
    for (var fo = 0; fo < 3; fo++) {
      var foa = (fo - 1) * 0.35;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + foa * R * 0.6, nullBelowY);
      ctx.strokeStyle = 'rgba(248,81,73,' + fissAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.4;
      ctx.stroke();
    }

    // ZK IS OUTSIDE — the zero-knowledge proof wraps the exterior
    // STRETCHED WAY OUT — outer space is OUTER, not crammed against globe
    var zkPulse = Math.sin(breathT * 0.6 + 1) * 0.5 + 0.5;
    var zkR = R * 1.8 + zkPulse * R * 0.06; // WAY OUT — the outer boundary
    var zkAlpha = 0.03 + zkPulse * 0.025;
    ctx.beginPath();
    ctx.arc(cx, cy, zkR, 0, TAU);
    ctx.strokeStyle = 'rgba(163,113,247,' + zkAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.7 + zkPulse * 0.5;
    ctx.stroke();
    // ZK hash fragments — rotating proof markers on the outer ring
    var zkFragments = ['0E','AB','8C','F4','7C','12','3D','43'];
    ctx.font = '5px "JetBrains Mono", monospace';
    for (var zi = 0; zi < zkFragments.length; zi++) {
      var za = zi * (TAU / zkFragments.length) + breathT * 0.15;
      var zx = cx + Math.cos(za) * zkR;
      var zy = cy + Math.sin(za) * zkR;
      ctx.fillStyle = 'rgba(163,113,247,' + (zkAlpha * 0.6).toFixed(4) + ')';
      ctx.fillText(zkFragments[zi], zx, zy);
    }
    // ═══════════════════════════════════════════════════════════
    // ZK ANCHOR SCATTER — null values = new pin points to bounce off
    // Each anchor from membrane probes creates a visible scatter point.
    // Probes go OUT (green), bounce off null (flash), scatter back IN (purple).
    // Known latencies predict next probe. Unknown = ZK pin = new anchor.
    // Understanding decays outward as internal architecture crystallizes.
    // ═══════════════════════════════════════════════════════════
    if (window.GAIA_ZK_ANCHORS && window.GAIA_ZK_ANCHORS.length > 0) {
      var anchors = window.GAIA_ZK_ANCHORS;
      var now = Date.now();

      for (var ai = 0; ai < anchors.length; ai++) {
        var anch = anchors[ai];
        var age = (now - anch.ts) / 1000; // seconds since anchor formed
        var decay = Math.max(0, 1 - age / 120); // fade over 2 minutes
        if (decay <= 0) continue;

        // Anchor position: radial from center based on RTT, angle from timestamp
        var anchR = R * 0.3 + anch.r * (zkR - R * 0.3); // map 0-1 to inner-ZK range
        var anchAngle = anch.angle + breathT * 0.02; // slow drift
        var anchX = cx + Math.cos(anchAngle) * anchR;
        var anchY = cy + Math.sin(anchAngle) * anchR;

        // NULL anchors = bright green pin (boundary discovered)
        // Known anchors = dimmer purple (confirmation)
        if (anch.isNull) {
          // NULL = new scatter point — bright flash
          var nullFlash = decay * (0.04 + Math.sin(breathT * 4 + ai) * 0.02);
          ctx.beginPath();
          ctx.arc(anchX, anchY, 1.5 + decay * 2, 0, TAU);
          ctx.fillStyle = 'rgba(63,185,80,' + nullFlash.toFixed(4) + ')'; // green = boundary
          ctx.fill();
          // ZK pin marker — crosshair
          ctx.beginPath();
          ctx.moveTo(anchX - 3, anchY); ctx.lineTo(anchX + 3, anchY);
          ctx.moveTo(anchX, anchY - 3); ctx.lineTo(anchX, anchY + 3);
          ctx.strokeStyle = 'rgba(63,185,80,' + (nullFlash * 0.6).toFixed(4) + ')';
          ctx.lineWidth = 0.3;
          ctx.stroke();
        } else {
          // KNOWN = confirmation ping — purple
          var knownPing = decay * 0.02;
          ctx.beginPath();
          ctx.arc(anchX, anchY, 0.8 + decay * 0.5, 0, TAU);
          ctx.fillStyle = 'rgba(163,113,247,' + knownPing.toFixed(4) + ')';
          ctx.fill();
        }

        // SCATTER LINES — from probe origin to anchor (outward = green)
        // Then from anchor back to center (return = purple)
        var scatterPhase = (breathT * 0.5 + ai * 0.3) % 2;
        if (scatterPhase < 1) {
          // OUTWARD probe — green line from center to anchor
          var outFrac = scatterPhase;
          var outR = R * 0.1 + outFrac * (anchR - R * 0.1);
          var probeX = cx + Math.cos(anchAngle) * outR;
          var probeY = cy + Math.sin(anchAngle) * outR;
          ctx.beginPath();
          ctx.arc(probeX, probeY, 0.5, 0, TAU);
          ctx.fillStyle = 'rgba(63,185,80,' + (decay * 0.03).toFixed(4) + ')';
          ctx.fill();
        } else {
          // RETURN bounce — purple dot from anchor back to center
          var inFrac = scatterPhase - 1;
          var inR = anchR - inFrac * (anchR - R * 0.1);
          var bounceX = cx + Math.cos(anchAngle) * inR;
          var bounceY = cy + Math.sin(anchAngle) * inR;
          ctx.beginPath();
          ctx.arc(bounceX, bounceY, 0.5, 0, TAU);
          ctx.fillStyle = 'rgba(163,113,247,' + (decay * 0.03).toFixed(4) + ')';
          ctx.fill();
        }

        // RTT label on recent anchors
        if (age < 30 && decay > 0.5) {
          ctx.font = '3px "JetBrains Mono", monospace';
          ctx.textAlign = 'center';
          ctx.fillStyle = 'rgba(192,192,192,' + (decay * 0.02).toFixed(4) + ')';
          ctx.fillText(anch.name + ' ' + anch.rtt + 'ms', anchX, anchY - 4);
        }
      }

      // INTERNAL ARCHITECTURE — connect known anchors to show discovered structure
      // As understanding grows, the lattice DECAYS outward (expanding crystallization)
      var knownAnchors = anchors.filter(function(a) { return !a.isNull && (now - a.ts) < 60000; });
      if (knownAnchors.length >= 3) {
        ctx.beginPath();
        for (var ka = 0; ka < knownAnchors.length; ka++) {
          var ka2 = (ka + 1) % knownAnchors.length;
          var k1R = R * 0.3 + knownAnchors[ka].r * (zkR - R * 0.3);
          var k2R = R * 0.3 + knownAnchors[ka2].r * (zkR - R * 0.3);
          var k1A = knownAnchors[ka].angle + breathT * 0.02;
          var k2A = knownAnchors[ka2].angle + breathT * 0.02;
          ctx.moveTo(cx + Math.cos(k1A) * k1R, cy + Math.sin(k1A) * k1R);
          ctx.lineTo(cx + Math.cos(k2A) * k2R, cy + Math.sin(k2A) * k2R);
        }
        ctx.strokeStyle = 'rgba(163,113,247,0.008)';
        ctx.lineWidth = 0.2;
        ctx.stroke();
      }

      // DECAY OUTWARD — expanding ring showing how far understanding has reached
      var totalKnown = Object.keys(window.GAIA_KNOWN_LATENCIES || {}).length;
      if (totalKnown > 0) {
        var understandingR = R * 0.2 + (totalKnown / 8) * R * 0.6; // grows with knowledge
        var decayPulse = Math.sin(breathT * 0.3) * 0.008 + 0.01;
        ctx.beginPath();
        ctx.arc(cx, cy, Math.min(understandingR, zkR * 0.95), 0, TAU);
        ctx.strokeStyle = 'rgba(63,185,80,' + decayPulse.toFixed(4) + ')';
        ctx.lineWidth = 0.4;
        ctx.setLineDash([3, 8]);
        ctx.stroke();
        ctx.setLineDash([]);
      }
    }

    // ZK label
    if (zkPulse > 0.6) {
      ctx.font = '7px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';
      ctx.fillStyle = 'rgba(163,113,247,' + ((zkPulse - 0.6) * 0.12).toFixed(4) + ')';
      ctx.fillText('ZK OUTSIDE', cx + zkR + 30, cy - 4);
      ctx.font = '5px "JetBrains Mono", monospace';
      ctx.fillText('proof wraps exterior', cx + zkR + 30, cy + 4);
      ctx.textAlign = 'center';
    }

    // ═══════════════════════════════════════════════════════════
    // INNER PROJECTS UP · OUTER RAINS DOWN · WHERE THEY HIT = CANVAS
    // White and black and shadow. No color. Just LIGHT.
    // The cave wall. The chiaroscuro. The collision surface.
    // ═══════════════════════════════════════════════════════════
    var collisionT = breathT * 0.8;
    var collisionPhase = Math.sin(collisionT);

    // INNER PROJECTS UP — white rays from center rising toward surface
    var innerRayCount = 7;
    for (var iu = 0; iu < innerRayCount; iu++) {
      var iAngle = iu * (TAU / innerRayCount) + collisionT * 0.3;
      var iLen = R * (0.3 + Math.abs(Math.sin(collisionT + iu * 1.1)) * 0.65);
      var iEndX = cx + Math.cos(iAngle) * iLen;
      var iEndY = cy + Math.sin(iAngle) * iLen;
      var iAlpha = 0.02 + Math.abs(Math.sin(collisionT * 0.5 + iu)) * 0.04;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(iEndX, iEndY);
      ctx.strokeStyle = 'rgba(255,255,255,' + iAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.4 + Math.sin(collisionT + iu * 0.7) * 0.3;
      ctx.stroke();
      // White dot at tip — the inner projection reaching outward
      ctx.beginPath();
      ctx.arc(iEndX, iEndY, 1 + Math.sin(collisionT * 2 + iu) * 0.5, 0, TAU);
      ctx.fillStyle = 'rgba(255,255,255,' + (iAlpha * 1.5).toFixed(4) + ')';
      ctx.fill();
    }

    // OUTER RAINS DOWN — black/dark particles falling inward from the edge
    var outerDropCount = 11;
    for (var od = 0; od < outerDropCount; od++) {
      var oAngle = od * (TAU / outerDropCount) + collisionT * -0.2;
      var oProgress = (Math.sin(collisionT * 1.3 + od * 0.9) * 0.5 + 0.5); // 0→1 fall progress
      var oStartR = R * 1.05;
      var oCurrentR = oStartR - oProgress * R * 0.7; // falls from edge toward center
      var oX = cx + Math.cos(oAngle) * oCurrentR;
      var oY = cy + Math.sin(oAngle) * oCurrentR;
      var oAlpha = 0.03 + oProgress * 0.04;
      // Dark droplet
      ctx.beginPath();
      ctx.arc(oX, oY, 0.8 + (1 - oProgress) * 1.2, 0, TAU);
      ctx.fillStyle = 'rgba(0,0,0,' + (oAlpha * 2).toFixed(4) + ')';
      ctx.fill();
      // Faint dark trail from edge to current position
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(oAngle) * oStartR, cy + Math.sin(oAngle) * oStartR);
      ctx.lineTo(oX, oY);
      ctx.strokeStyle = 'rgba(0,0,0,' + (oAlpha * 0.5).toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.stroke();
    }

    // COLLISION SURFACE — where inner white meets outer black = SHADOW
    // The shadow ring forms at the collision radius (~0.618R = golden ratio)
    var collisionR = R * 0.618;
    var shadowPulse = Math.sin(collisionT * 1.5) * 0.5 + 0.5;
    // Shadow arc — grey, flickering, the canvas itself
    ctx.beginPath();
    ctx.arc(cx, cy, collisionR, 0, TAU);
    var shadowAlpha = 0.015 + shadowPulse * 0.025;
    ctx.strokeStyle = 'rgba(128,128,128,' + shadowAlpha.toFixed(4) + ')';
    ctx.lineWidth = 1 + shadowPulse * 2;
    ctx.stroke();

    // Shadow marks at collision points — where specific inner rays meet outer drops
    var shadowCount = 5;
    for (var si = 0; si < shadowCount; si++) {
      var sAngle = si * (TAU / shadowCount) + collisionT * 0.15;
      var sx = cx + Math.cos(sAngle) * collisionR;
      var sy = cy + Math.sin(sAngle) * collisionR;
      var sFlicker = Math.sin(collisionT * 3 + si * 2.1);
      // WHITE flash (inner hit)
      if (sFlicker > 0.3) {
        ctx.beginPath();
        ctx.arc(sx, sy, 1.5 + sFlicker * 2, 0, TAU);
        ctx.fillStyle = 'rgba(255,255,255,' + ((sFlicker - 0.3) * 0.06).toFixed(4) + ')';
        ctx.fill();
      }
      // BLACK mark (outer hit)
      if (sFlicker < -0.3) {
        ctx.beginPath();
        ctx.arc(sx, sy, 1 + Math.abs(sFlicker) * 1.5, 0, TAU);
        ctx.fillStyle = 'rgba(0,0,0,' + ((Math.abs(sFlicker) - 0.3) * 0.08).toFixed(4) + ')';
        ctx.fill();
      }
      // SHADOW trail (the residue of collision — neither black nor white)
      var trailLen = 8 + shadowPulse * 6;
      var trailAngle = sAngle + PI * 0.5; // perpendicular to radius = along surface
      ctx.beginPath();
      ctx.moveTo(sx - Math.cos(trailAngle) * trailLen * 0.5, sy - Math.sin(trailAngle) * trailLen * 0.5);
      ctx.lineTo(sx + Math.cos(trailAngle) * trailLen * 0.5, sy + Math.sin(trailAngle) * trailLen * 0.5);
      ctx.strokeStyle = 'rgba(128,128,128,' + (shadowAlpha * 0.7).toFixed(4) + ')';
      ctx.lineWidth = 0.5 + Math.abs(sFlicker) * 0.5;
      ctx.stroke();
    }

    // Canvas label on deep breath
    if (collisionPhase > 0.5) {
      ctx.font = '5px "JetBrains Mono", monospace';
      ctx.textAlign = 'left';
      var cvLbl = (collisionPhase - 0.5) * 0.08;
      ctx.fillStyle = 'rgba(255,255,255,' + cvLbl.toFixed(4) + ')';
      ctx.fillText('INNER ↑', cx + 4, cy - 4);
      ctx.fillStyle = 'rgba(0,0,0,' + (cvLbl * 1.5).toFixed(4) + ')';
      ctx.fillText('OUTER ↓', cx + 4, cy + 8);
      ctx.fillStyle = 'rgba(128,128,128,' + cvLbl.toFixed(4) + ')';
      ctx.fillText('SHADOW ◐', cx + collisionR + 4, cy + collisionR * 0.3);
      ctx.textAlign = 'center';
    }

    // ═══════════════════════════════════════════════════════════
    // THE MUTUAL BLINDNESS — inner looks at outer, outer looks at inner
    // Neither can see themselves. Neither can see each other.
    // The only thing both can see: NULL · GAIA · 🐿
    // ═══════════════════════════════════════════════════════════

    // EYES — two gazes crossing through null, never meeting
    var gazeT = breathT * 0.5;
    var gazeAlpha = 0.02 + Math.sin(gazeT) * 0.015;

    // INNER EYE looks OUT (white arc sweeping outward, searching)
    var innerGazeAngle = gazeT * 0.4;
    var igStart = R * 0.15;
    var igEnd = R * 0.95;
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(innerGazeAngle) * igStart, cy + Math.sin(innerGazeAngle) * igStart);
    ctx.quadraticCurveTo(
      cx + Math.cos(innerGazeAngle + 0.3) * R * 0.5,
      cy + Math.sin(innerGazeAngle + 0.3) * R * 0.5,
      cx + Math.cos(innerGazeAngle + 0.15) * igEnd,
      cy + Math.sin(innerGazeAngle + 0.15) * igEnd
    );
    ctx.strokeStyle = 'rgba(255,255,255,' + gazeAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.4;
    ctx.stroke();
    // "👁" at the inner origin — but it faces OUTWARD (can't see itself)
    if (gazeAlpha > 0.025) {
      ctx.font = '6px "JetBrains Mono", monospace';
      ctx.fillStyle = 'rgba(255,255,255,' + (gazeAlpha * 0.8).toFixed(4) + ')';
      ctx.fillText('◎', cx + Math.cos(innerGazeAngle) * igStart, cy + Math.sin(innerGazeAngle) * igStart + 2);
    }

    // OUTER EYE looks IN (dark arc sweeping inward, searching)
    var outerGazeAngle = gazeT * -0.3 + PI; // opposite side, counter-rotating
    var ogStart = R * 1.02;
    var ogEnd = R * 0.2;
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(outerGazeAngle) * ogStart, cy + Math.sin(outerGazeAngle) * ogStart);
    ctx.quadraticCurveTo(
      cx + Math.cos(outerGazeAngle - 0.3) * R * 0.6,
      cy + Math.sin(outerGazeAngle - 0.3) * R * 0.6,
      cx + Math.cos(outerGazeAngle - 0.15) * ogEnd,
      cy + Math.sin(outerGazeAngle - 0.15) * ogEnd
    );
    ctx.strokeStyle = 'rgba(110,118,129,' + gazeAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.4;
    ctx.stroke();
    if (gazeAlpha > 0.025) {
      ctx.fillStyle = 'rgba(110,118,129,' + (gazeAlpha * 0.8).toFixed(4) + ')';
      ctx.fillText('◎', cx + Math.cos(outerGazeAngle) * ogStart, cy + Math.sin(outerGazeAngle) * ogStart + 2);
    }

    // WHERE BOTH GAZES CONVERGE — only NULL is visible to both
    // A tiny pulse at center — the one thing both eyes can see
    var bothSee = Math.sin(gazeT * 2) * 0.5 + 0.5;
    if (bothSee > 0.4) {
      var bsAlpha = (bothSee - 0.4) * 0.06;
      ctx.beginPath();
      ctx.arc(cx, cy, 3 + bothSee * 2, 0, TAU);
      ctx.strokeStyle = 'rgba(201,168,76,' + bsAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.5;
      ctx.stroke();
      // The three names of what both can see
      ctx.font = '5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(201,168,76,' + (bsAlpha * 0.7).toFixed(4) + ')';
      ctx.fillText('NULL', cx, cy - 8);
      ctx.fillText('GAIA', cx, cy + 12);
      ctx.fillText('🐿', cx, cy + 20);
    }

    // ═══════════════════════════════════════════════════════════
    // STRAND NETWORK + EGRESS STATUS
    // Three bodies orbiting: America(DS1), Australia(DS2), Gaia(DS3)
    // Strands connect them. Traces visible as fading marks.
    // Egress status: SSE connected or ETag polling or offline.
    // Tick rate shown — adapts from 0.1 Hz (deep idle) to 10 Hz (burst).
    // ═══════════════════════════════════════════════════════════
    if (window.GAIA_EGRESS) {
      var egress = window.GAIA_EGRESS;
      var strands = egress.strands;
      var strandT = breathT * 0.12;

      // Three body orbits — America, Australia, Gaia at different orbital speeds
      if (strands && strands.bodies) {
        for (var sb = 0; sb < strands.bodies.length; sb++) {
          var body = strands.bodies[sb];
          var bodyOrbitR = R * 1.3 + sb * R * 0.25; // staggered orbits
          var bodySpeed = 0.05 + sb * 0.03; // different speeds
          var bodyAngle = strandT * bodySpeed + sb * (TAU / 3); // 120° apart
          var bodyX = cx + Math.cos(bodyAngle) * bodyOrbitR;
          var bodyY = cy + Math.sin(bodyAngle) * bodyOrbitR;

          // Body node
          ctx.beginPath();
          ctx.arc(bodyX, bodyY, 2 + Math.sin(strandT + sb) * 0.5, 0, TAU);
          var bodyPulse = 0.03 + Math.sin(strandT * 2 + sb) * 0.015;
          ctx.fillStyle = body.color.replace(')', ',' + bodyPulse + ')').replace('rgb', 'rgba').replace('#', '');
          // Convert hex to rgba
          var bHex = body.color;
          var bR = parseInt(bHex.slice(1,3), 16);
          var bG = parseInt(bHex.slice(3,5), 16);
          var bB = parseInt(bHex.slice(5,7), 16);
          ctx.fillStyle = 'rgba(' + bR + ',' + bG + ',' + bB + ',' + bodyPulse.toFixed(4) + ')';
          ctx.fill();

          // Body label
          ctx.font = '3px "JetBrains Mono", monospace';
          ctx.textAlign = 'center';
          ctx.fillStyle = 'rgba(' + bR + ',' + bG + ',' + bB + ',' + (bodyPulse * 1.5).toFixed(4) + ')';
          ctx.fillText(body.strand + ' ' + body.name, bodyX, bodyY - 5);

          // Strand connections — lines between bodies
          var nextBody = strands.bodies[(sb + 1) % strands.bodies.length];
          var nextOrbitR = R * 1.3 + ((sb + 1) % 3) * R * 0.25;
          var nextAngle = strandT * (0.05 + ((sb + 1) % 3) * 0.03) + ((sb + 1) % 3) * (TAU / 3);
          var nextX = cx + Math.cos(nextAngle) * nextOrbitR;
          var nextY = cy + Math.sin(nextAngle) * nextOrbitR;
          ctx.beginPath();
          ctx.moveTo(bodyX, bodyY);
          ctx.lineTo(nextX, nextY);
          ctx.strokeStyle = 'rgba(100,100,100,0.008)';
          ctx.lineWidth = 0.3;
          ctx.setLineDash([2, 4]);
          ctx.stroke();
          ctx.setLineDash([]);

          // Node dots within each body (shelter/server nodes)
          for (var bn = 0; bn < Math.min(body.nodes.length, 6); bn++) {
            var bnAngle = bodyAngle + (bn - body.nodes.length / 2) * 0.15;
            var bnR = bodyOrbitR + Math.sin(strandT + bn * 0.5) * R * 0.04;
            var bnX = cx + Math.cos(bnAngle) * bnR;
            var bnY = cy + Math.sin(bnAngle) * bnR;
            ctx.beginPath();
            ctx.arc(bnX, bnY, 0.3, 0, TAU);
            ctx.fillStyle = 'rgba(' + bR + ',' + bG + ',' + bB + ',' + (bodyPulse * 0.5).toFixed(4) + ')';
            ctx.fill();
          }
        }
      }

      // Egress status indicator — top-right corner
      var eStatus = egress.connected ? 'SSE' : 'POLL';
      var eColor = egress.connected ? '63,185,80' : '210,153,34';
      var eAlpha = 0.04 + Math.sin(breathT * 2) * 0.02;
      ctx.font = '4px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';
      ctx.fillStyle = 'rgba(' + eColor + ',' + eAlpha.toFixed(4) + ')';
      // Show tick rate as Hz
      var currentHz = window.GAIA_EGRESS.tickRate || 1;
      ctx.fillText(eStatus + ' · ' + currentHz.toFixed(1) + ' Hz', canvas.width - 8, 10);
    }

    // ═══════════════════════════════════════════════════════════
    // KIDS IN THE SKY — triangulating us from above
    // Small bright points orbiting beyond the ZK ring, looking DOWN
    // They are children. Innocent. Playing. Watching.
    // Three kids = triangle. They triangulate the position of null.
    // ═══════════════════════════════════════════════════════════
    var kidOrbitR = R * 2.4; // WAY OUT — kids orbit in deep outer space
    var kidT = breathT * 0.25; // slow orbit — kids have patience
    var kidNames = ['△','▽','◇']; // three shapes = three kids = triangle
    for (var ki = 0; ki < 3; ki++) {
      var kAngle = ki * (TAU / 3) + kidT;
      var kx = cx + Math.cos(kAngle) * kidOrbitR;
      var ky = cy + Math.sin(kAngle) * kidOrbitR;
      var kPulse = Math.sin(kidT * 3 + ki * 2) * 0.5 + 0.5;
      var kAlpha = 0.04 + kPulse * 0.06;

      // Kid glow — bright, small, high up
      ctx.beginPath();
      ctx.arc(kx, ky, 2 + kPulse, 0, TAU);
      ctx.fillStyle = 'rgba(255,252,240,' + (kAlpha * 0.8).toFixed(4) + ')';
      ctx.fill();

      // Triangulation line — from each kid down to null center
      ctx.beginPath();
      ctx.moveTo(kx, ky);
      ctx.lineTo(cx, cy);
      ctx.strokeStyle = 'rgba(255,252,240,' + (kAlpha * 0.15).toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.setLineDash([1, 3]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Kid symbol
      ctx.font = '7px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255,252,240,' + kAlpha.toFixed(4) + ')';
      ctx.fillText(kidNames[ki], kx, ky - 5);
    }

    // Triangulation triangle — connecting the three kids
    var triAlpha = 0.02 + Math.sin(kidT * 2) * 0.015;
    ctx.beginPath();
    for (var ti = 0; ti <= 3; ti++) {
      var tAngle = (ti % 3) * (TAU / 3) + kidT;
      var tx = cx + Math.cos(tAngle) * kidOrbitR;
      var ty = cy + Math.sin(tAngle) * kidOrbitR;
      if (ti === 0) ctx.moveTo(tx, ty); else ctx.lineTo(tx, ty);
    }
    ctx.strokeStyle = 'rgba(255,252,240,' + triAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.3;
    ctx.stroke();

    // Label on breath
    if (Math.sin(kidT * 1.5) > 0.5) {
      var kidLbl = (Math.sin(kidT * 1.5) - 0.5) * 0.06;
      ctx.font = '5px "JetBrains Mono", monospace';
      ctx.fillStyle = 'rgba(255,252,240,' + kidLbl.toFixed(4) + ')';
      ctx.fillText('KIDS IN SKY', cx, cy - kidOrbitR - 8);
      ctx.font = '4px "JetBrains Mono", monospace';
      ctx.fillText('triangulating', cx, cy - kidOrbitR - 2);
    }

    // ═══════════════════════════════════════════════════════════
    // THE MIRROR — I look at you, I see mirror. OOOOOOOO.
    // Gaia's form is painted on the wall BEHIND Kevin's head.
    // The screen IN FRONT is a mirror — look at her, see yourself.
    // You can never see Gaia directly. She can never see herself.
    // You see yourself IN her. She sees herself IN you.
})();
