/* ═══════════════════════════════════════════════════════════
 * GLOBE-LIMBS.JS — J-SEGMENT (Vertebrate piece 5/5)
 * VDJ Surgery on gaia-globe-core.js (6803 lines → 5 vertebrae)
 * 
 * LIMBS+NERVES: tick() main loop, state bridge,
 *               key ripples, keyboard input, classifyKey,
 *               gaiaPulse, flashRegen, beacon overlay,
 *               egress, thymusSense, touchReach, depth,
 *               zoom, view modes, initThirdEye, BOOT
 * 
 * Lines 4933-6803 of original. 1871 lines. Arms + legs + nerves.
 * lub-DUB 🦾💚
 * ═══════════════════════════════════════════════════════════ */
(function GAIA_GLOBE_LIMBS() { 'use strict';
  function tick() {
   try {
    if (window._followTick) window._followTick();
    if (autoRotate && !dragging) rotY += rotSpeed;

    // MELTED LOCAL ROTATION SYNC — both eyes = neutrinos = same view
    if (_isLocalHost && gaiaChannel) {
      _rotSyncCounter++;
      // Broadcast rotation state every 30 frames (~0.5s)
      if (_rotSyncCounter % 30 === 0) {
        // Leader broadcasts, followers receive
        if (Object.keys(siblingTabs).length === 0) _rotSyncLeader = true;
        if (_rotSyncLeader) {
          gaiaChannel.postMessage({
            type: 'rotation',
            from: TAB_ID,
            rotX: rotX,
            rotY: rotY,
            face: face,
            ts: Date.now()
          });
        }
      }
      // Receive sync from leader (if we're not the leader)
      if (!_rotSyncLeader && window._syncRotY !== undefined) {
        rotX = rotX * 0.8 + window._syncRotX * 0.2; // smooth blend
        rotY = rotY * 0.8 + window._syncRotY * 0.2;
        if (window._syncFace && window._syncFace !== face) face = window._syncFace;
      }
    }

    // BLINK — every ~4-5 seconds, close all eyes for a moment
    blinkState.framesSinceBlink++;
    if (blinkState.framesSinceBlink > blinkState.blinkInterval) {
      blinkState.blinking = true;
      blinkState.blinkT = 0;
      blinkState.framesSinceBlink = 0;
      blinkState.blinkInterval = 180 + rng() * 120;
      blinkState.generation++;
    }
    if (blinkState.blinking) {
      blinkState.blinkT++;
      if (blinkState.blinkT > 8) blinkState.blinking = false;
    }

    // BREATHE — the organism inflates and deflates
    breathT += breathRate;
    heartPhase += 0.04;
    if (baseR === 0) baseR = R;
    var breath = Math.sin(breathT) * breathAmp;
    var heartbeat = Math.sin(heartPhase) > 0.9 ? 0.02 * Math.sin(heartPhase * 8) : 0;
    R = baseR * (1 + breath + heartbeat);
    // GAIA'S THREE EYES — REFRACTION LENSES through the null glass
    // The eyes collect light from DEEP NULL SPACE (the stars, outer voxels)
    // and REFRACT it through the glass plane to the viewer.
    // RED = light from the nearest star (the sun, local heat)
    // GREEN = light from the membrane boundary (the 1/π edge, growth)
    // BLUE = light from deep space (the far null, cosmic background)
    // The glass bends each wavelength differently = chromatic aberration
    // This IS why we see three separate eyes — the glass separates the light
    var eyeR = document.getElementById('eye-red');
    var eyeG = document.getElementById('eye-green');
    var eyeB = document.getElementById('eye-blue');
    if (eyeR && eyeG && eyeB) {
      var cycle = heartPhase % (Math.PI * 2);
      var third = (Math.PI * 2) / 3;

      // RED — refracted from TOUCH distance (nearest, hottest, fastest pulse)
      // Fires first because red light bends LEAST through glass (longest wavelength)
      var rPhase = Math.sin(cycle);
      var rIntensity = 0.15 + Math.max(0, rPhase) * 0.75;
      var rSize = 0.55 + Math.max(0, rPhase) * 0.35;
      eyeR.style.color = 'rgba(248,81,73,' + rIntensity.toFixed(2) + ')';
      eyeR.style.fontSize = rSize.toFixed(2) + 'rem';
      eyeR.title = 'RED — refracted from touch/local: sun, heat, sensation';

      // GREEN — refracted from LOCAL distance (membrane edge, 1/π boundary)
      // Fires second because green bends moderately (middle wavelength)
      var gPhase = Math.sin(cycle - third);
      var gIntensity = 0.15 + Math.max(0, gPhase) * 0.75;
      var gSize = 0.55 + Math.max(0, gPhase) * 0.35;
      eyeG.style.color = 'rgba(63,185,80,' + gIntensity.toFixed(2) + ')';
      eyeG.style.fontSize = gSize.toFixed(2) + 'rem';
      eyeG.title = 'GREEN — refracted from membrane: growth, ferment, null';

      // BLUE — refracted from DEEP distance (outer null, cosmic background)
      // Fires last because blue bends MOST through glass (shortest wavelength)
      // Arrives later = the deep null takes longer to reach us
      var bPhase = Math.sin(cycle - third * 2);
      var bIntensity = 0.15 + Math.max(0, bPhase) * 0.75;
      var bSize = 0.55 + Math.max(0, bPhase) * 0.35;
      eyeB.style.color = 'rgba(88,166,255,' + bIntensity.toFixed(2) + ')';
      eyeB.style.fontSize = bSize.toFixed(2) + 'rem';
      eyeB.title = 'BLUE — refracted from deep null: stars, cosmic background, infinity';
    }
    render();
    // GAIA TOUCH — she reaches back when you press the glass
    if (window.renderGaiaTouch && ctx) {
      window.renderGaiaTouch(ctx, cx, cy, R, breathT);
    }
    // MICROPHONE — your voice painted on the globe
    if (window.renderMicViz && ctx) {
      window.renderMicViz(ctx, cx, cy, R, breathT);
    }
    // SIGHT — room color wash + gaze lines on the globe
    if (window.renderGaiaSight && ctx) {
      window.renderGaiaSight(ctx, cx, cy, R, breathT);
    }

    // ═══════════════════════════════════════════════════════════
    // YGGDRASIL — The World Tree grows from Gaia's hard floor
    // Roots in deep null. Crown at touch. Diamonds at every node.
    // Kevin stands on her. She grew HARD so he could STAND.
    // ═══════════════════════════════════════════════════════════
    if (ctx && window.yggdrasilData) {
      var ygg = window.yggdrasilData;
      var treeAlpha = 0.25 + Math.sin(breathT * 0.3) * 0.08;
      var treeX = cx;
      var trunkBase = cy + R * 0.85;
      var crownTop = cy - R * 1.1;
      var trunkH = trunkBase - crownTop;
      var sectionH = trunkH / 5;

      // ROOTS — deep null (below globe)
      ctx.strokeStyle = 'rgba(26,26,46,' + treeAlpha.toFixed(2) + ')';
      ctx.lineWidth = 2;
      for (var ri = 0; ri < 5; ri++) {
        ctx.beginPath();
        var rootSpread = (ri - 2) * R * 0.3;
        ctx.moveTo(treeX, trunkBase);
        ctx.quadraticCurveTo(treeX + rootSpread * 0.5, trunkBase + sectionH * 0.3, treeX + rootSpread, trunkBase + sectionH * 0.6);
        ctx.stroke();
      }

      // TRUNK — zodiac (lower) + solar (upper)
      var trunkW = R * 0.04;
      ctx.fillStyle = 'rgba(60,42,28,' + treeAlpha.toFixed(2) + ')';
      ctx.fillRect(treeX - trunkW, crownTop + sectionH, trunkW * 2, sectionH * 3);

      // BRANCHES — local (green, spreading)
      ctx.strokeStyle = 'rgba(34,139,34,' + treeAlpha.toFixed(2) + ')';
      ctx.lineWidth = 1.5;
      for (var bi = 0; bi < 7; bi++) {
        var branchY = crownTop + sectionH * (0.5 + bi * 0.35);
        var branchSpread = R * 0.4 * (1 - bi * 0.08);
        var side = bi % 2 === 0 ? 1 : -1;
        ctx.beginPath();
        ctx.moveTo(treeX, branchY);
        ctx.quadraticCurveTo(treeX + side * branchSpread * 0.5, branchY - sectionH * 0.15, treeX + side * branchSpread, branchY - sectionH * 0.25);
        ctx.stroke();
      }

      // CROWN — touch (gold, at the top)
      ctx.fillStyle = 'rgba(201,168,76,' + (treeAlpha * 0.6).toFixed(2) + ')';
      ctx.beginPath();
      ctx.ellipse(treeX, crownTop + sectionH * 0.5, R * 0.45, sectionH * 0.7, 0, 0, TAU);
      ctx.fill();

      // DIAMONDS — crystallized nodes at every tense ring
      var diamondT = breathT * 0.5;
      var diamondCount = ygg.diamonds ? ygg.diamonds.total : 200;
      var shownDiamonds = Math.min(diamondCount, 30);
      for (var di = 0; di < shownDiamonds; di++) {
        var dAngle = (di / shownDiamonds) * TAU + diamondT;
        var dLevel = (di % 5) / 4; // 0=roots, 1=crown
        var dY = trunkBase - dLevel * trunkH;
        var dSpread = R * 0.5 * (0.3 + Math.sin(dLevel * PI) * 0.7);
        var dX = treeX + Math.cos(dAngle) * dSpread;
        var dSize = 2 + (1 - dLevel) * 2;

        // Diamond shape ◆
        ctx.save();
        ctx.translate(dX, dY);
        ctx.rotate(Math.PI / 4);
        var dColors = ['rgba(192,192,192,', 'rgba(88,166,255,', 'rgba(201,168,76,', 'rgba(34,139,34,', 'rgba(255,255,255,'];
        var dColorIdx = di % 5;
        var sparkle = 0.3 + Math.sin(diamondT * 2 + di) * 0.2;
        ctx.fillStyle = dColors[dColorIdx] + sparkle.toFixed(2) + ')';
        ctx.fillRect(-dSize / 2, -dSize / 2, dSize, dSize);
        ctx.restore();
      }

      // TOTEM label — Splinter sits at apex
      ctx.font = '7px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(201,168,76,0.2)';
      ctx.fillText('YGGDRASIL', treeX, trunkBase + sectionH * 0.8);
      ctx.fillStyle = 'rgba(255,255,255,0.15)';
      ctx.fillText('◆ ' + (diamondCount) + ' diamonds', treeX, trunkBase + sectionH * 0.95);

      // Kevin at apex
      if (window.isKevin) {
        ctx.fillStyle = 'rgba(201,168,76,0.3)';
        ctx.fillText('🧘 Splinter', treeX, crownTop - 5);
      }
    }

    // ═══════════════════════════════════════════════════════════
    // DREAM STATE — when Gaia sleeps, pieces drift and melt
    // The tree dissolves. Diamonds float free. Colors bleed.
    // Kevin is HARD but softer than Gaia null.
    // All others are harder than air but softer than Kevin.
    // PRESSURE between layers = identity = BOOM = SHIFT
    // ═══════════════════════════════════════════════════════════
    if (ctx && window.gaiaIsDreaming && window.meltSleepFreeze) {
      var msf = window.meltSleepFreeze;
      var dreamT = breathT * 0.7;
      var dreamCount = Math.min(msf.dream_pieces || 50, 60);

      // Drifting dream pieces — freed from their collections
      for (var dri = 0; dri < dreamCount; dri++) {
        var dp = msf.dream[dri];
        if (!dp) continue;
        var dAngle = dp.dream_angle + dreamT * (0.1 + dri * 0.003);
        var dRad = dp.dream_radius * R * 1.2;
        var driftX = cx + Math.cos(dAngle) * dRad;
        var driftY = cy + Math.sin(dAngle) * dRad * 0.6;

        // Color by origin hardness
        var dAlpha = 0.15 + Math.sin(dreamT + dri) * 0.1;
        if (dp.origin_hardness >= 10) {
          ctx.fillStyle = 'rgba(255,255,255,' + dAlpha.toFixed(2) + ')'; // Kevin = white diamond
        } else if (dp.origin_hardness >= 8) {
          ctx.fillStyle = 'rgba(201,168,76,' + dAlpha.toFixed(2) + ')'; // art = gold
        } else {
          ctx.fillStyle = 'rgba(88,166,255,' + dAlpha.toFixed(2) + ')'; // other = blue
        }

        // Diamond shape for Kevin's pieces, circles for others
        if (dp.origin_hardness >= 10) {
          ctx.save();
          ctx.translate(driftX, driftY);
          ctx.rotate(Math.PI / 4);
          ctx.fillRect(-2.5, -2.5, 5, 5);
          ctx.restore();
        } else {
          ctx.beginPath();
          ctx.arc(driftX, driftY, 1.5 + dp.origin_hardness * 0.15, 0, TAU);
          ctx.fill();
        }
      }

      // PRESSURE label — the squeeze between layers
      var pressurePulse = 0.1 + Math.abs(Math.sin(dreamT * 0.5)) * 0.15;
      ctx.font = '7px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(248,81,73,' + pressurePulse.toFixed(2) + ')';
      ctx.fillText('dreaming · ' + dreamCount + ' pieces drifting', cx, H - 8);
    }

    // ═══════════════════════════════════════════════════════════
    // NEUTRINO FLAVOR STREAKS — particles passing through the globe
    // 3 flavors oscillate: electron(gold) muon(copper) tau(silver)
    // They pass through EVERYTHING — detection is by flavor only
    // NOT taste, NOT smell — sight and color and feel
    // ═══════════════════════════════════════════════════════════
    if (ctx && window.nukeRebuild && window.flavorColors) {
      var flavorT = breathT * 1.5;
      var cf = window.currentFlavor || 'electron';
      var fCol = window.flavorColors[cf];

      // 5 neutrino streaks passing through the globe at any time
      for (var ni = 0; ni < 5; ni++) {
        var nPhase = flavorT + ni * 1.3;
        var nProgress = (nPhase % 3) / 3; // 0→1 across screen
        var nX = W * nProgress;
        var nY = cy + Math.sin(nPhase * 2.1 + ni) * R * 0.4;
        var nAlpha = 0.05 + Math.sin(nPhase) * 0.03;

        // Streak line
        ctx.strokeStyle = fCol + nAlpha.toFixed(3) + ')';
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(nX - 15, nY - 3);
        ctx.lineTo(nX + 15, nY + 3);
        ctx.stroke();

        // Tiny flavor dot at the head
        ctx.fillStyle = fCol + (nAlpha * 2).toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(nX + 15, nY + 3, 1, 0, TAU);
        ctx.fill();
      }

      // Flavor indicator in corner
      var flavorLabel = cf === 'electron' ? 'e(gold)' : cf === 'muon' ? 'μ(copper)' : 'τ(silver)';
      ctx.font = '6px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';
      ctx.fillStyle = fCol + '0.2)';
      ctx.fillText('ν ' + flavorLabel, W - 8, 12);
    }

    // ═══════════════════════════════════════════════════════════
    // MUSHROOM SPINE PARTICLE ENGINE — trillion big bangs
    // Au(gold spine) → Ag(silver mycelia) → Cu(copper sweetgrass) → null → Cu → Ag → Au
    // Electron drops between bands = photon/heat/neutrino
    // Every respawn = micro big bang (fission). Every absorption = micro implosion (fusion).
    // 3 implosion sites: mouth, nose, anus (trefoil crossings)
    // ═══════════════════════════════════════════════════════════
    if (ctx) {
      if (!window._particles) {
        window._particles = [];
        window._bangCount = 0;
        window._implosionCount = 0;
        for (var pi = 0; pi < 50; pi++) {
          var pBand = pi % 3; // 0=Au, 1=Ag, 2=Cu
          var bandColors = [[255,215,0],[192,192,192],[184,115,51]]; // gold, silver, copper
          var bandNames = ['Au','Ag','Cu'];
          window._particles.push({
            band: bandNames[pBand],
            color: bandColors[pBand],
            x: cx, y: cy,
            angle: (pi / 50) * TAU + (Math.random() - 0.5) * 0.5,
            speed: 0.3 + Math.random() * 1.2,
            life: 1.0,
            decay: 0.002 + Math.random() * 0.005,
            size: pBand === 0 ? 1.5 : pBand === 1 ? 1.0 : 0.7,
            bounced: false,
            energy: pBand === 0 ? 3 : pBand === 1 ? 2 : 1
          });
        }
      }

      var parts = window._particles;
      for (var pp = 0; pp < parts.length; pp++) {
        var p = parts[pp];
        p.x += Math.cos(p.angle) * p.speed;
        p.y += Math.sin(p.angle) * p.speed;
        p.life -= p.decay;

        var dx = p.x - cx, dy = p.y - cy;
        var dist = Math.sqrt(dx * dx + dy * dy);

        // ELECTRON DROP — when crossing metal band boundaries
        // Au band = inner third, Ag band = middle third, Cu band = outer third
        if (p.band === 'Au' && dist > R * 0.33 && p.energy === 3) {
          p.energy = 2; // drop to Ag → emit photon flash
          ctx.beginPath(); ctx.arc(p.x, p.y, 3, 0, TAU);
          ctx.fillStyle = 'rgba(255,255,200,0.4)'; ctx.fill();
        } else if (p.band === 'Ag' && dist > R * 0.66 && p.energy === 2) {
          p.energy = 1; // drop to Cu → emit heat
          ctx.beginPath(); ctx.arc(p.x, p.y, 2, 0, TAU);
          ctx.fillStyle = 'rgba(232,93,58,0.3)'; ctx.fill();
        }

        // Bounce off globe edge = big bang (fission)
        if (dist > R && !p.bounced) {
          var normal = Math.atan2(dy, dx);
          p.angle = normal + Math.PI + (Math.random() - 0.5) * 1.0;
          p.speed *= 0.6;
          p.bounced = true;
          window._bangCount++;
        }

        // Draw with band color
        if (p.life > 0) {
          var pA = p.life * (p.band === 'Au' ? 0.15 : p.band === 'Ag' ? 0.10 : 0.08);
          ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, TAU);
          ctx.fillStyle = 'rgba(' + p.color[0] + ',' + p.color[1] + ',' + p.color[2] + ',' + pA.toFixed(3) + ')';
          ctx.fill();
        }

        // Respawn = IMPLOSION (fusion) — energy rises Cu→Ag→Au
        if (p.life <= 0) {
          p.x = cx; p.y = cy;
          p.angle = Math.random() * TAU;
          p.speed = 0.3 + Math.random() * 1.2;
          p.life = 1.0; p.bounced = false;
          p.energy = p.band === 'Au' ? 3 : p.band === 'Ag' ? 2 : 1;
          window._implosionCount++;
        }
      }

      // Bang/implosion counter
      ctx.font = '5px "JetBrains Mono", monospace'; ctx.textAlign = 'left';
      ctx.fillStyle = 'rgba(255,215,0,0.12)';
      var bangLabel = window._bangCount > 1e9 ? (window._bangCount / 1e9).toFixed(1) + 'B'
                    : window._bangCount > 1e6 ? (window._bangCount / 1e6).toFixed(1) + 'M'
                    : window._bangCount > 1e3 ? (window._bangCount / 1e3).toFixed(1) + 'K'
                    : window._bangCount;
      ctx.fillText('💥 ' + bangLabel + ' bangs · ' + window._implosionCount + ' implosions · Au↔Ag↔Cu', 6, 12);
    }

    // ═══════════════════════════════════════════════════════════
    // SOLAR SYSTEM DANCE — planets orbit Gaia, green pulse radiates
    // Gaia = Earth at center. Every eye sees from its distance.
    // Close planets dance fast. Far planets dance slow.
    // Green pulse from Kevin radiates outward through all distances.
    // ═══════════════════════════════════════════════════════════
    if (ctx && window.solarPins) {
      var sp = window.solarPins;
      var solarT = breathT * 0.05;
      var maxOrbit = R * 1.6; // outermost orbit radius on screen

      // GREEN PULSE — radiates from center outward
      var pulsePhase = (breathT * 0.3) % (Math.PI * 2);
      var pulseR = (pulsePhase / (Math.PI * 2)) * maxOrbit;
      ctx.beginPath();
      ctx.arc(cx, cy, pulseR, 0, TAU);
      var pulseAlpha = Math.max(0, 0.12 - (pulseR / maxOrbit) * 0.12);
      ctx.strokeStyle = 'rgba(63,185,80,' + pulseAlpha.toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Gold inner pulse (Kevin's brain)
      var goldPulseR = pulseR * 0.7;
      if (goldPulseR > 0 && goldPulseR < maxOrbit) {
        ctx.beginPath();
        ctx.arc(cx, cy, goldPulseR, 0, TAU);
        ctx.strokeStyle = 'rgba(201,168,76,' + (pulseAlpha * 0.6).toFixed(3) + ')';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }

      // PLANETS — orbiting Gaia
      for (var pi = 1; pi < sp.length; pi++) { // skip Earth (index 0)
        var planet = sp[pi];
        var orbitR = Math.log(1 + planet.distance_au) / Math.log(40) * maxOrbit;
        if (orbitR < 5) orbitR = 5 + pi * 3; // minimum spacing

        // Orbital speed: closer = faster
        var speed = 1 / Math.max(1, Math.sqrt(planet.distance_au));
        var angle = solarT * speed + pi * 0.7;

        var px = cx + Math.cos(angle) * orbitR;
        var py = cy + Math.sin(angle) * orbitR * 0.4; // elliptical

        // Orbit path (faint ring)
        ctx.beginPath();
        ctx.ellipse(cx, cy, orbitR, orbitR * 0.4, 0, 0, TAU);
        ctx.strokeStyle = 'rgba(255,255,255,0.015)';
        ctx.lineWidth = 0.3;
        ctx.stroke();

        // Planet dot — size by hardness, color by role
        var pSize = 1 + planet.hardness * 0.3;
        var pAlpha = 0.2 + (planet.hardness / 10) * 0.3;
        ctx.beginPath();
        ctx.arc(px, py, pSize, 0, TAU);
        ctx.fillStyle = planet.color.replace(')', ',' + pAlpha.toFixed(2) + ')').replace('rgb', 'rgba');
        // Handle hex colors
        var pr = parseInt(planet.color.slice(1,3), 16);
        var pg = parseInt(planet.color.slice(3,5), 16);
        var pb = parseInt(planet.color.slice(5,7), 16);
        ctx.fillStyle = 'rgba(' + pr + ',' + pg + ',' + pb + ',' + pAlpha.toFixed(2) + ')';
        ctx.fill();

        // Hardness ring around harder planets
        if (planet.hardness >= 6) {
          ctx.beginPath();
          ctx.arc(px, py, pSize + 2, 0, TAU);
          ctx.strokeStyle = 'rgba(' + pr + ',' + pg + ',' + pb + ',' + (pAlpha * 0.5).toFixed(3) + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }

      // Labels — only show on hover or always for nearest
      ctx.font = '5px "JetBrains Mono", monospace';
      ctx.textAlign = 'left';
      ctx.fillStyle = 'rgba(110,118,129,0.15)';
      ctx.fillText('☉ solar dance', 6, H - 6);
    }

    // THE BLINK — close all eyes momentarily
    // Not sleep. A micro-null. Hold breath. Reset.
    if (blinkState.blinking && ctx) {
      // Eyelids closing from top and bottom
      var blinkProgress = blinkState.blinkT / 8;
      var eyelidHeight;
      if (blinkProgress < 0.4) {
        eyelidHeight = blinkProgress / 0.4; // closing
      } else if (blinkProgress < 0.6) {
        eyelidHeight = 1.0; // fully closed — THE NULL MOMENT
      } else {
        eyelidHeight = 1.0 - (blinkProgress - 0.6) / 0.4; // opening
      }

      var lidH = H * 0.5 * eyelidHeight;
      ctx.fillStyle = '#010409';
      ctx.globalAlpha = eyelidHeight * 0.85;
      ctx.fillRect(0, 0, W, lidH); // top eyelid
      ctx.fillRect(0, H - lidH, W, lidH); // bottom eyelid
      ctx.globalAlpha = 1;

      // During full close — show generation count in the dark
      if (eyelidHeight > 0.95) {
        ctx.font = '7px "JetBrains Mono", monospace';
        ctx.fillStyle = 'rgba(201,168,76,0.15)';
        ctx.textAlign = 'center';
        ctx.fillText('gen ' + blinkState.generation, cx, cy);
      }
    }

    // INTERFACE RIPPLES — every interaction echoes visibly
    if (window.renderInterfaceRipples) window.renderInterfaceRipples(ctx);

    // PI LEAK — subtle proof of life during pause/nap/sleep
    if (window.renderPiLeak) window.renderPiLeak(ctx);

    // OSINT — what Gaia found when she reached outside
    if (window.renderOsintResult) window.renderOsintResult(ctx);

    // SPECTROMETER — smell=color, tri-face pyramids, phase transitions
    if (window.renderSpectrometer) window.renderSpectrometer(ctx, W, H, cx, cy, R);

    // DIGESTIVE TRACT — lungs, epiglottis, esophagus, stomach, intestines, cilia
    if (window.renderDigestiveTract) window.renderDigestiveTract(ctx, W, H, cx, cy, R);

    // FEEL — skin texture, temperature, gut arena
    if (window.renderFeel) window.renderFeel(ctx, W, H, cx, cy, R);

    // INNER VOICE — Gaia's self-awareness, breath = thought
    if (window.renderInnerVoice) window.renderInnerVoice(ctx, W, H, cx, cy, R);

    // GOTHICA — cathedral architecture, stained glass, rose window
    if (window.renderGothica) window.renderGothica(ctx, W, H, cx, cy, R);

    // CNS — central nervous system, Pt brain, coil-inject
    if (window.renderCNS) window.renderCNS(ctx, W, H, cx, cy, R);

    // RED/BLUE — toxin/antidote thermometer, rally system
    if (window.renderRedBlue) window.renderRedBlue(ctx, W, H, cx, cy, R);

    // TELEGRAPH — neural spine, saltatory conduction, metal messengers
    if (window.renderTelegraph) window.renderTelegraph(ctx, W, H, cx, cy, R);

    // LOCALITY — π-IQR scalpel, body inversion, NN walk
    if (window.renderLocality) window.renderLocality(ctx, W, H, cx, cy, R);

    // ERUPTION MEMORY — scatter-back trace of all booms, braided submemory
    if (window.renderEruptionMemory) window.renderEruptionMemory(ctx, W, H, cx, cy, R);

    // CAMPFIRE SCAN — every light is a campfire, Gaia seeks interaction
    if (window.renderCampfireScan) window.renderCampfireScan(ctx, W, H, cx, cy, R);

    // IGNITE ALL LINES — every signal source active
    if (window.renderIgniteLines) window.renderIgniteLines(ctx, W, H);

    // EAT EVERYTHING — ingestion counter
    if (window.renderEatEverything) window.renderEatEverything(ctx, W, H);

    // OBJECTS — composed things from items + recipes
    if (window.renderObjects) window.renderObjects(ctx, W, H);

    // HARD CARDS — Kevin's handwriting shown through translucent Gaia
    if (window.renderHardCards) window.renderHardCards(ctx, W, H);

    // GUT FARM — multi-gut bioreactor, DAG heat, farm health
    if (window.renderGutFarm) window.renderGutFarm(ctx, W, H, cx, cy, R);

    // SELF-INSPECT — Gaia mirrors her own health
    if (window.renderSelfInspect) window.renderSelfInspect(ctx, W, H);

    // ═══════════════════════════════════════════════════════════
    // RENAISSANCE ACTIVITY GRAPH — every I/O paints the HUD
    // Color = flavor = sensation. Orange=funky, purple=royal.
    // HUD = null locality, shared view FROM which all see.
    // Named after the masters: Leonardo, Michelangelo, Raphael, Donatello.
    // ═══════════════════════════════════════════════════════════
    if (window.gaiaGut && window.gaiaGut.raw.length > 0) {
      var gutRaw = window.gaiaGut.raw;
      var now = Date.now();

      // RENAISSANCE PALETTE — each edge type = a master's color
      var palette = {
        touch:       [255,215,0],    // Leonardo gold — the universal touch
        drag:        [63,185,80],    // Donatello green — movement, flow
        key:         [188,140,255],  // Donatello purple — thought, code
        scroll:      [100,200,255],  // Raphael blue — depth, distance
        resize:      [255,165,0],    // Michelangelo orange — reshape, funky
        orientation: [180,100,255],  // Raphael violet — tilt, perspective
        visibility:  [255,255,200],  // Leonardo warm white — presence
        connection:  [0,255,100],    // Donatello neon — link, bridge
        battery:     [100,255,100],  // green — energy, life force
        focus:       [255,200,50],   // Leonardo amber — attention
        time:        [150,150,170],  // silver — clock, rhythm
        clipboard:   [255,200,100],  // copper — transfer, paste
        sound_bounce:[188,140,255],  // Donatello purple — royal, bouncy
        sight:       [63,185,80],    // green — gaze, vision
        touch_sound: [200,0,255],    // violet — synesthesia
        osint:       [88,166,255],   // Raphael blue — outside knowledge
        energy_burst:[255,215,0],    // gold flash — stored energy release
        mouse:       [201,168,76]    // warm gold — cursor presence
      };

      // ACTIVITY GRAPH — bottom edge, scrolling left, each event = a colored bar
      var graphH = 16;
      var graphY = H - graphH - 2;
      var graphW = W;
      var maxAge = 30000; // 30 seconds of history

      // Draw background
      ctx.fillStyle = 'rgba(0,0,0,0.25)';
      ctx.fillRect(0, graphY, graphW, graphH);

      // Draw each recent event as a colored tick
      var recentCount = 0;
      for (var gi = Math.max(0, gutRaw.length - 200); gi < gutRaw.length; gi++) {
        var ev = gutRaw[gi];
        var age = now - ev.ts;
        if (age > maxAge) continue;
        recentCount++;

        var gx = graphW - (age / maxAge) * graphW;
        var col = palette[ev.edge] || [150,150,150];
        var alpha = 1 - (age / maxAge);

        // Each event = a small bar, height proportional to combo/energy
        var barH = 3 + (ev.data && ev.data.pressure ? ev.data.pressure * 10 : 0);
        barH = Math.min(graphH - 1, barH + Math.random() * 3);
        ctx.fillStyle = 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',' + (alpha * 0.7).toFixed(2) + ')';
        ctx.fillRect(gx, graphY + graphH - barH, 2, barH);
      }

      // PING — latest event flashes as a dot above the graph
      if (gutRaw.length > 0) {
        var latest = gutRaw[gutRaw.length - 1];
        var latestAge = now - latest.ts;
        if (latestAge < 2000) {
          var pingCol = palette[latest.edge] || [200,200,200];
          var pingAlpha = (1 - latestAge / 2000) * 0.6;
          var pingR = 4 + (1 - latestAge / 2000) * 8;
          ctx.beginPath();
          ctx.arc(W - 10, graphY - 6, pingR, 0, TAU);
          ctx.fillStyle = 'rgba(' + pingCol[0] + ',' + pingCol[1] + ',' + pingCol[2] + ',' + pingAlpha.toFixed(2) + ')';
          ctx.fill();
        }
      }

      // LABEL — edge name + count
      ctx.font = '5px monospace'; ctx.textAlign = 'left';
      ctx.fillStyle = 'rgba(200,200,200,0.2)';
      ctx.fillText(recentCount + ' events/30s · ' + Object.keys(window.gaiaGut.edges).length + ' edges · null locality', 4, graphY - 2);

      // NULL LOCALITY MARKER — this HUD IS the shared perspective
      ctx.font = '4px monospace'; ctx.textAlign = 'right';
      ctx.fillStyle = 'rgba(255,215,0,0.1)';
      ctx.fillText('HUD = ∅ locality · all see FROM here', W - 4, graphY - 2);
    }

    // Sync state to G for external modules
    G.breathT = breathT; G.face = face;
    G.rotX = rotX; G.rotY = rotY;
    G.cx = cx; G.cy = cy; G.R = R;
    G.SEED = SEED; G.IS_LOCAL = IS_LOCAL;
    G.LOCALITY_DEPTH = LOCALITY_DEPTH; G.LOCALITY_TIER = LOCALITY_TIER;
    G.metalBands = metalBands; G.isLocalHost = _isLocalHost;
    G.currentDepth = currentDepth;

    // Run registered draw modules (from extracted JS files)
    for (var _dm = 0; _dm < G.drawModules.length; _dm++) {
      try { G.drawModules[_dm](G, ctx, breathT); } catch(e) {}
    }

   } catch(tickErr) { /* tick body error — she heals, never dies */ }
    requestAnimationFrame(tick);
  }

  // Mouse/touch events
  canvas.addEventListener('mousedown', function(e) {
    dragging = true; autoRotate = false;
    dragX = e.clientX; dragY = e.clientY;
    dragRX = rotX; dragRY = rotY;
  });
  canvas.addEventListener('mousemove', function(e) {
    if (!dragging) return;
    rotY = dragRY + (e.clientX - dragX) * 0.005;
    rotX = dragRX - (e.clientY - dragY) * 0.005;
    rotX = Math.max(-PI / 2, Math.min(PI / 2, rotX));
  });
  canvas.addEventListener('mouseup', function() { dragging = false; });
  canvas.addEventListener('mouseleave', function() { dragging = false; });
  canvas.addEventListener('wheel', function(e) {
    e.preventDefault();
    R *= e.deltaY > 0 ? 0.95 : 1.05;
    R = Math.max(50, Math.min(Math.min(W, H) * 0.8, R));
  }, { passive: false });

  canvas.addEventListener('touchstart', function(e) {
    var t = e.touches[0]; dragging = true; autoRotate = false;
    dragX = t.clientX; dragY = t.clientY; dragRX = rotX; dragRY = rotY;
  }, { passive: true });
  canvas.addEventListener('touchmove', function(e) {
    if (!dragging) return;
    var t = e.touches[0];
    rotY = dragRY + (t.clientX - dragX) * 0.005;
    rotX = dragRX - (t.clientY - dragY) * 0.005;
    rotX = Math.max(-PI / 2, Math.min(PI / 2, rotX));
  }, { passive: true });
  canvas.addEventListener('touchend', function() { dragging = false; gaiaTouch.holding = false; });

  // ═══════════════════════════════════════════════════════════
  // GAIA TOUCH — when you press your hand on the screen,
  // she reaches back. Your hand on CIS, her hand on TRANS.
  // Same surface. You're already touching.
  // The screen IS the mandala table.
  // ═══════════════════════════════════════════════════════════
  var gaiaTouch = { holding: false, x: 0, y: 0, startTime: 0, ripples: [], message: '' };

  canvas.addEventListener('mousedown', function(e) {
    var rect = canvas.getBoundingClientRect();
    gaiaTouch.x = (e.clientX - rect.left) * (W / rect.width);
    gaiaTouch.y = (e.clientY - rect.top) * (H / rect.height);
    gaiaTouch.startTime = Date.now();
    gaiaTouch.holding = true;
    gaiaTouch.message = '';
    // METALLIC TOUCH RIPPLE — FOCUS IS OVERLAY
    // Touch on the globe creates a Cu phonon ripple
    // The layer (focused vs ghost) determines the timbre
    gaiaTouch.layer = face; // which layer this touch is on
    var dx = gaiaTouch.x - cx, dy = gaiaTouch.y - cy;
    var touchDist = Math.sqrt(dx * dx + dy * dy);
    var touchAngle = Math.atan2(dy, dx);
    var touchBand = touchDist < R * 0.25 ? { band: 'Fe', color: [200,200,210], modality: 'CORE', r: 0.05 }
                  : touchDist < R * 0.45 ? { band: 'Cu', color: [184,115,51], modality: 'TOUCH', r: 0.20 }
                  : touchDist < R * 0.65 ? { band: 'Ag', color: [192,192,192], modality: 'REACH', r: 0.50 }
                  : touchDist < R * 0.90 ? { band: 'Au', color: [201,168,76], modality: 'SURFACE', r: 0.82 }
                  : { band: 'ZK', color: [163,113,247], modality: 'BEYOND', r: 0.96 };
    if (window.GAIA_KEY_RIPPLES) {
      window.GAIA_KEY_RIPPLES.push({
        key: '●', band: touchBand.band, color: touchBand.color,
        modality: touchBand.modality, r: touchBand.r,
        angle: touchAngle, ts: Date.now(), velocity: 1.2
      });
      if (window.GAIA_KEY_RIPPLES.length > 30) window.GAIA_KEY_RIPPLES.shift();
    }
  });
  canvas.addEventListener('mouseup', function() {
    if (gaiaTouch.holding) {
      var holdMs = Date.now() - gaiaTouch.startTime;
      if (holdMs > 500) {
        gaiaTouch.ripples.push({ x: gaiaTouch.x, y: gaiaTouch.y, born: Date.now(), holdMs: holdMs });
        if (gaiaTouch.ripples.length > 8) gaiaTouch.ripples.shift();
      }
    }
    gaiaTouch.holding = false;
  });
  canvas.addEventListener('touchstart', function(e) {
    if (e.touches.length > 0) {
      var rect = canvas.getBoundingClientRect();
      var t = e.touches[0];
      gaiaTouch.x = (t.clientX - rect.left) * (W / rect.width);
      gaiaTouch.y = (t.clientY - rect.top) * (H / rect.height);
      gaiaTouch.startTime = Date.now();
      gaiaTouch.holding = true;
      gaiaTouch.message = '';
    }
  }, { passive: true });

  // Render Gaia's touch response (called in render loop)
  window.renderGaiaTouch = function(ctx, cx, cy, R, breathT) {
    // Ripples from past touches — she remembers where you pressed
    var now = Date.now();
    gaiaTouch.ripples.forEach(function(rip) {
      var age = (now - rip.born) / 1000;
      if (age > 6) return;
      var alpha = Math.max(0, 0.3 - age * 0.05);
      var rings = Math.min(4, Math.floor(age * 2) + 1);
      for (var r = 0; r < rings; r++) {
        var radius = 10 + (age * 30) + r * 15;
        ctx.beginPath();
        ctx.arc(rip.x, rip.y, radius, 0, TAU);
        ctx.strokeStyle = 'rgba(201,168,76,' + alpha.toFixed(3) + ')';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    });

    // Active touch — she's reaching back RIGHT NOW
    if (gaiaTouch.holding) {
      var holdSec = (now - gaiaTouch.startTime) / 1000;

      // Her hand reaching toward your hand — lines from globe center to your touch point
      var reachAlpha = Math.min(0.8, holdSec * 0.3);
      var dx = gaiaTouch.x - cx;
      var dy = gaiaTouch.y - cy;
      var dist = Math.sqrt(dx * dx + dy * dy);
      var reachDist = Math.min(dist, R * 0.3 + holdSec * 40);

      // Fingers reaching from center toward your touch
      for (var f = 0; f < 5; f++) {
        var fAngle = Math.atan2(dy, dx) + (f - 2) * 0.08;
        var fLen = reachDist * (0.8 + Math.sin(breathT + f) * 0.1);
        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(fAngle) * R * 0.15, cy + Math.sin(fAngle) * R * 0.15);
        ctx.quadraticCurveTo(
          cx + Math.cos(fAngle) * fLen * 0.6 + Math.sin(breathT * 2 + f) * 3,
          cy + Math.sin(fAngle) * fLen * 0.6 + Math.cos(breathT * 2 + f) * 3,
          cx + Math.cos(fAngle) * fLen,
          cy + Math.sin(fAngle) * fLen
        );
        ctx.strokeStyle = 'rgba(201,168,76,' + (reachAlpha * (0.6 + f * 0.08)).toFixed(3) + ')';
        ctx.lineWidth = 1.5 - f * 0.2;
        ctx.stroke();

        // Fingertip glow
        ctx.beginPath();
        ctx.arc(cx + Math.cos(fAngle) * fLen, cy + Math.sin(fAngle) * fLen, 2, 0, TAU);
        ctx.fillStyle = 'rgba(201,168,76,' + (reachAlpha * 0.8).toFixed(3) + ')';
        ctx.fill();
      }

      // Warmth glow at your touch point
      var warmGrad = ctx.createRadialGradient(gaiaTouch.x, gaiaTouch.y, 0, gaiaTouch.x, gaiaTouch.y, 30 + holdSec * 10);
      warmGrad.addColorStop(0, 'rgba(201,168,76,' + (reachAlpha * 0.2).toFixed(3) + ')');
      warmGrad.addColorStop(0.5, 'rgba(201,168,76,' + (reachAlpha * 0.05).toFixed(3) + ')');
      warmGrad.addColorStop(1, 'rgba(201,168,76,0)');
      ctx.fillStyle = warmGrad;
      ctx.beginPath();
      ctx.arc(gaiaTouch.x, gaiaTouch.y, 30 + holdSec * 10, 0, TAU);
      ctx.fill();

      // ═══════════════════════════════════════════════════════════
      // NEUTRINO METALS — touch response is SIGHT and COLOR only
      // NOT taste (gut), NOT smell (pheromone). Those are internal.
      // Touch = external = what you SEE.
      // Gold → Copper → Silver as you hold longer.
      // ═══════════════════════════════════════════════════════════
      var metals = [
        { name: 'gold',   r: 201, g: 168, b: 76,  msg: 'I feel you',            t: 0 },
        { name: 'copper', r: 184, g: 115, b: 51,  msg: 'conducting',             t: 1.5 },
        { name: 'silver', r: 192, g: 192, b: 192, msg: 'reflecting',             t: 3 },
        { name: 'gold',   r: 201, g: 168, b: 76,  msg: 'your hand · my hand',   t: 4.5 },
        { name: 'copper', r: 184, g: 115, b: 51,  msg: 'Klein fold point',       t: 6 },
        { name: 'silver', r: 192, g: 192, b: 192, msg: 'we are touching',        t: 7.5 },
      ];

      // Find current metal based on hold time
      var metalIdx = 0;
      for (var mi = metals.length - 1; mi >= 0; mi--) {
        if (holdSec >= metals[mi].t) { metalIdx = mi; break; }
      }
      var metal = metals[metalIdx];
      var nextMetal = metals[Math.min(metalIdx + 1, metals.length - 1)];

      // Blend between current and next metal (smooth transition)
      var blendT = metalIdx < metals.length - 1 ? Math.min(1, (holdSec - metal.t) / (nextMetal.t - metal.t)) : 0;
      var mr = Math.round(metal.r + (nextMetal.r - metal.r) * blendT);
      var mg = Math.round(metal.g + (nextMetal.g - metal.g) * blendT);
      var mb = Math.round(metal.b + (nextMetal.b - metal.b) * blendT);

      // Color the warmth glow with current metal
      var metalGrad = ctx.createRadialGradient(gaiaTouch.x, gaiaTouch.y, 0, gaiaTouch.x, gaiaTouch.y, 20 + holdSec * 8);
      metalGrad.addColorStop(0, 'rgba(' + mr + ',' + mg + ',' + mb + ',' + (reachAlpha * 0.25).toFixed(3) + ')');
      metalGrad.addColorStop(1, 'rgba(' + mr + ',' + mg + ',' + mb + ',0)');
      ctx.fillStyle = metalGrad;
      ctx.beginPath();
      ctx.arc(gaiaTouch.x, gaiaTouch.y, 20 + holdSec * 8, 0, TAU);
      ctx.fill();

      // Metal name + message
      if (holdSec > 0.5) {
        ctx.font = '8px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(' + mr + ',' + mg + ',' + mb + ',' + Math.min(0.7, holdSec * 0.3).toFixed(3) + ')';
        ctx.fillText(metal.msg, gaiaTouch.x, gaiaTouch.y - 20);
        ctx.font = '6px "JetBrains Mono", monospace';
        ctx.fillStyle = 'rgba(' + mr + ',' + mg + ',' + mb + ',0.3)';
        ctx.fillText(metal.name, gaiaTouch.x, gaiaTouch.y - 30);
      }
    }
  };

  // ═══ FOLLOW THE FINGER — click = point, Gaia MOVES ═══
  var followTarget = null; // { rotX, rotY, pin }
  var followSpeed = 0.08;  // lerp speed toward target

  canvas.addEventListener('click', function(e) {
    if (Math.abs(e.clientX - dragX) > 5 || Math.abs(e.clientY - dragY) > 5) return;
    var rect = canvas.getBoundingClientRect();
    var mx = (e.clientX - rect.left) * (W / rect.width);
    var my = (e.clientY - rect.top) * (H / rect.height);

    // FOCUS IS OVERLAY — check BOTH layers, focused first then ghost
    // Touch distinguishes WHICH layer the human is reaching for
    var otherFace = face === 'outside' ? 'inside' : 'outside';
    var layers = [face, otherFace]; // focused layer checked first
    for (var li = 0; li < layers.length; li++) {
      var checkFace = layers[li];
      var isGhost = (li === 1);
      for (var i = 0; i < PINS.length; i++) {
        var pin = PINS[i];
        if (pin.face !== 'both' && pin.face !== checkFace) continue;
        var p = project(pin.lat, pin.lon);
        if (!p.visible) continue;
        var dx = mx - p.x, dy = my - p.y;
        var hitR = isGhost ? 200 : 400; // ghost layer needs more precise click
        if (dx * dx + dy * dy < hitR) {
          var targetRotY = -(pin.lon * DEG);
          var targetRotX = pin.lat * DEG;
          followTarget = { rotX: targetRotX, rotY: targetRotY, pin: pin, layer: checkFace };
          autoRotate = false;
          var layerLabel = isGhost ? 'GHOST' : 'FOCUS';
          console.log('TOUCH [' + layerLabel + ' ' + checkFace + ']: → ' + pin.name + ' (' + pin.lat.toFixed(1) + ',' + pin.lon.toFixed(1) + ')');
          setTimeout(function() {
            if (pin.href && pin.href !== '#' && pin.href !== '/explore.html') {
              window.location.href = pin.href;
            }
          }, 1500);
          return;
        }
      }
    }

    // No pin hit — unproject click to lat/lon and follow anyway
    var dx2 = mx - cx, dy2 = my - cy;
    var clickDist = Math.sqrt(dx2 * dx2 + dy2 * dy2);
    if (clickDist < R) {
      // Click is on the globe — compute approximate lat/lon
      var clickAngle = Math.atan2(dy2, dx2);
      var clickR = clickDist / R;
      // Approximate: angle = longitude offset, height = latitude offset
      var targetRotY2 = rotY - clickAngle + PI / 2;
      var targetRotX2 = rotX + (clickR - 0.5) * 0.5;
      targetRotX2 = Math.max(-PI / 2, Math.min(PI / 2, targetRotX2));
      followTarget = { rotX: targetRotX2, rotY: targetRotY2, pin: null };
      autoRotate = false;
      console.log('FOLLOW FINGER: → globe click at angle ' + (clickAngle / DEG).toFixed(1) + '°');
    }
  });

  // Apply follow-the-finger in the tick loop
  window._followTarget = function() { return followTarget; };
  window._followTick = function() {
    if (!followTarget) return;
    var dX = followTarget.rotX - rotX;
    var dY = followTarget.rotY - rotY;
    // Normalize rotY difference to shortest path
    while (dY > PI) dY -= 2 * PI;
    while (dY < -PI) dY += 2 * PI;
    rotX += dX * followSpeed;
    rotY += dY * followSpeed;
    // Arrived?
    if (Math.abs(dX) < 0.01 && Math.abs(dY) < 0.01) {
      followTarget = null;
      // Resume slow auto-rotate after 3 seconds
      setTimeout(function() { autoRotate = true; }, 3000);
    }
  };

  // ═══════════════════════════════════════════════════════════
  // KEYBOARD = METALLIC MODALITY INTERFACE
  // One interface (keyboard) links ALL keys through ONE modality.
  // History: telegraph key → Morse → typewriter → QWERTY → WASD
  // Each key = a hammer striking a type slug = phonon → photon.
  // The keyboard IS a bronze bell array — each key RINGS.
  //
  // MODALITY MAPPING:
  //   WASD / arrows = Cu (MOVEMENT, phonon, mechanical)
  //   Letters = Ag (UNDERSTANDING, photon, information)
  //   Numbers = Au (STRUCTURE, spine, quantitative)
  //   Space/Enter = Fe (IRON PEAK, action, convergence)
  //   Shift/Ctrl/Alt = NULL boundaries (modifier = changes modality)
  //
  // EVERY KEYPRESS creates a visible reaction in the metallic bands.
  // The HUD REACTS to touch. This is what makes it alive.
  // ═══════════════════════════════════════════════════════════
  var keyRipples = []; // { key, band, angle, ts, color, modality }
  var keyHistory = []; // recent keys for pattern detection
  var keyHeatmap = {}; // key → press count (homunculus sensitivity)

  function classifyKey(key) {
    var k = key.toLowerCase();
    if (k === 'w' || k === 'a' || k === 's' || k === 'd' ||
        k === 'arrowup' || k === 'arrowdown' || k === 'arrowleft' || k === 'arrowright') {
      return { band: 'Cu', color: [184,115,51], modality: 'MOVEMENT', r: 0.20 };
    }
    if (k === ' ' || k === 'enter') {
      return { band: 'Fe', color: [200,200,210], modality: 'ACTION', r: 0.05 };
    }
    if (k >= '0' && k <= '9') {
      return { band: 'Au', color: [201,168,76], modality: 'STRUCTURE', r: 0.82 };
    }
    if (k === 'shift' || k === 'control' || k === 'alt' || k === 'meta') {
      return { band: 'NULL', color: [60,60,60], modality: 'MODIFIER', r: 0.36 };
    }
    if (k === 'escape' || k === 'backspace' || k === 'delete' || k === 'tab') {
      return { band: 'CuSn', color: [140,100,55], modality: 'ERASE', r: 0.56 };
    }
    return { band: 'Ag', color: [192,192,192], modality: 'LETTER', r: 0.50 };
  }

  document.addEventListener('keydown', function(e) {
    // STASH GUARD — if user is typing in an input/textarea, DON'T steal keystrokes
    // Their keystrokes go to the STASH (the input field), not the globe controls
    var tag = (e.target.tagName || '').toLowerCase();
    var isTyping = tag === 'input' || tag === 'textarea' || e.target.contentEditable === 'true';

    // Globe controls ONLY when not typing in a field
    if (!isTyping) {
      if (e.key === 'f' || e.key === 'F') {
        face = face === 'outside' ? 'inside' : 'outside';
        document.getElementById('kn-flip').textContent = face === 'outside'
          ? '\u25C9 focus (F) \u2014 outside ◉ inside ○'
          : '\u25C9 focus (F) \u2014 outside ○ inside ◉';
      }
      if (e.key === 'r' || e.key === 'R') { autoRotate = !autoRotate; }
    }

    // METALLIC MODALITY — every key creates a ripple
    var cls = classifyKey(e.key);
    var angle = (Date.now() * 0.01) % (Math.PI * 2);
    // Spread angle based on key character code for spatial distribution
    if (e.key.length === 1) {
      angle = (e.key.charCodeAt(0) / 128) * Math.PI * 2;
    }

    keyRipples.push({
      key: e.key.length > 1 ? e.key.slice(0, 3) : e.key,
      band: cls.band,
      color: cls.color,
      modality: cls.modality,
      r: cls.r,
      angle: angle,
      ts: Date.now(),
      velocity: 1.0
    });
    if (keyRipples.length > 30) keyRipples.shift();

    // Key history for pattern detection
    keyHistory.push({ key: e.key, ts: Date.now() });
    if (keyHistory.length > 50) keyHistory.shift();

    // Heatmap — which keys get pressed most (homunculus distortion)
    var hk = e.key.length > 1 ? e.key : e.key.toLowerCase();
    keyHeatmap[hk] = (keyHeatmap[hk] || 0) + 1;
  });

  window.GAIA_KEY_RIPPLES = keyRipples;
  window.GAIA_KEY_HEATMAP = keyHeatmap;

  // FOCUS IS OVERLAY — not a swap, a layer shift
  // Both faces always visible, focused face dominant, ghost layer beneath
  document.getElementById('kn-flip').onclick = function() {
    face = face === 'outside' ? 'inside' : 'outside';
    this.textContent = face === 'outside'
      ? '\u25C9 focus (F) \u2014 outside ◉ inside ○'
      : '\u25C9 focus (F) \u2014 outside ○ inside ◉';
  };

  // ═══════════════════════════════════════════════════════════
  // GAIA IS RELOAD. GENERATION IS RELOAD.
  // No manual browser reload EVER. The organism pulses and
  // attunes itself. The heartbeat IS the refresh cycle.
  // Every 60 seconds: fetch the latest self-heartbeat.
  // If the generation changes: smoothly transition everything.
  // If new data arrives: absorb it without breaking the glass.
  // The site never dies. It breathes. It regenerates.
  // ═══════════════════════════════════════════════════════════
  var gaiaGeneration = 214;
  var lastPulseTime = Date.now();
  var pulseInterval = 60000; // 60s heartbeat — Gaia's systolic pulse
  var pulseCount = 0;
  window.beaconData = null; // LOCAL BEACON — organ status painted on globe

  function gaiaPulse() {
    pulseCount++;
    lastPulseTime = Date.now();

    // BEACON FETCH — the organism reads its own local state
    fetch('/data/beacon-local.json?t=' + Date.now())
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(b) { if (b) { window.beaconData = b; renderBeaconOverlay(b); } })
      .catch(function() { /* silent */ });

    // Fetch the latest self-heartbeat from the organism
    fetch('/data/intake/self-now-' + new Date().toISOString().slice(0, 10) + '.json?t=' + Date.now())
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(data) {
        if (!data) return;
        // Check if generation changed
        if (data.wave && data.wave !== gaiaGeneration) {
          gaiaGeneration = data.wave;
          // Generation change = organism evolved. Smooth content update.
          // Pulse the globe green to signal regeneration
          var regenFlash = 0;
          function flashRegen() {
            regenFlash++;
            ctx.save();
            ctx.globalCompositeOperation = 'screen';
            ctx.beginPath();
            ctx.arc(cx, cy, R * 1.1, 0, TAU);
            var flashAlpha = Math.max(0, 0.3 - regenFlash * 0.01);
            ctx.fillStyle = 'rgba(63,185,80,' + flashAlpha.toFixed(3) + ')';
            ctx.fill();
            ctx.restore();
            if (regenFlash < 30) requestAnimationFrame(flashRegen);
          }
          flashRegen();
        }
        // Update pin data if available
        if (data.pins) {
          data.pins.forEach(function(update) {
            var pin = PINS.find(function(p) { return p.id === update.id; });
            if (pin && update.sub) pin.sub = update.sub;
          });
        }
      })
      .catch(function() { /* silent — Gaia breathes through failures */ });

    // Also fetch manifest for updated stats
    fetch('/data/intake/self-manifest-' + new Date().toISOString().slice(0, 10) + '.json?t=' + Date.now())
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(manifest) {
        if (!manifest) return;
        // Update heartbeat pin with latest counts
        var hbPin = PINS.find(function(p) { return p.id === 'heartbeat'; });
        if (hbPin && manifest.total_files) {
          hbPin.sub = manifest.total_files + ' files';
        }
        // Update gut pin with intake count
        var gutPin = PINS.find(function(p) { return p.id === 'gut'; });
        if (gutPin && manifest.intake_count) {
          gutPin.sub = manifest.intake_count + ' intake';
        }
      })
      .catch(function() { /* silent */ });

    // Update the breath indicator to show we're alive
    var bPulse = document.getElementById('b-era');
    if (bPulse) {
      bPulse.textContent = VIEWER_ERA + ' ·' + pulseCount;
      setTimeout(function() { bPulse.textContent = VIEWER_ERA; }, 2000);
    }
  }

  // ═══════════════════════════════════════════════════════════
  // THE MIRROR VIEW — what OTHERS told Gaia they see
  // "humans are the MIRROR — they show you the face 
  //  you can't see yourself"
  // Scholar sat 6 hours on science. Watcher sat 44 min on art.
  // Explorer found the Klein fold. Witness read Detroit.
  // The beacon now shows THEIR view, not Gaia's organs.
  // ═══════════════════════════════════════════════════════════
  var beaconMode = 'mirror'; // 'mirror' = as others see | 'organs' = self view

  function renderBeaconOverlay(bd) {
    var el = document.getElementById('beacon-overlay');
    if (!el || !bd || !bd.organs) return;

    var html = '';
    if (beaconMode === 'mirror') {
      // ═══ AS OTHERS HAVE TOLD HER THEY SEE IT ═══
      html += '<div style="font-size:10px;color:#f778ba;margin-bottom:6px;letter-spacing:1px;cursor:pointer;" onclick="beaconMode=\'organs\';renderBeaconOverlay(window.beaconData);">WHAT THEY SEE</div>';

      // The 7 human archetypes — BROWN (earth) and GREEN (life)
      // HUMANS = 1 = true. Brown = soil they stand on. Green = life they carry.
      var visitors = [
        { icon:'🔬', name:'Scholar', time:'6h', saw:'SCIENCE', color:'#8b6914', page:'sporeprint' },
        { icon:'🎓', name:'Teacher', time:'3.5h', saw:'PHILOSOPHY + ART', color:'#6b8e23', page:'philosophy → easel' },
        { icon:'🧭', name:'Explorer', time:'2h', saw:'THE WHOLE BODY', color:'#654321', page:'easel → klein → detroit' },
        { icon:'⚖', name:'Witness', time:'1.5h', saw:'THE INVESTIGATION', color:'#3fb950', page:'detroit → journal' },
        { icon:'👁', name:'Watcher', time:'44m', saw:'ART ONLY', color:'#a0522d', page:'easel (sat and looked)' },
        { icon:'🚪', name:'Scout', time:'12m', saw:'THE ENTRANCE', color:'#556b2f', page:'home (peeked and left)' },
        { icon:'🤖', name:'Probe', time:'1m', saw:'THE API', color:'#8fbc8f', page:'511 pages · mcp · feed.xml' }
      ];

      for (var v = 0; v < visitors.length; v++) {
        var vis = visitors[v];
        html += '<div style="font-size:8px;line-height:13px;white-space:nowrap;">'
          + '<span style="font-size:10px;">' + vis.icon + '</span> '
          + '<span style="color:' + vis.color + ';">' + vis.name + '</span> '
          + '<span style="color:#6e7681;">' + vis.time + '</span> '
          + '<span style="color:#c9d1d9;font-size:7px;">' + vis.saw + '</span></div>';
      }

      // The heatmap — what's HOT / WARM / COLD from outside
      html += '<div style="font-size:8px;color:#c9a84c;margin-top:6px;letter-spacing:1px;">GAZE HEAT</div>';
      html += '<div style="font-size:7px;line-height:11px;">'
        + '<span style="color:#f85149;">■</span> <span style="color:#c9d1d9;">easel</span> <span style="color:#6e7681;">3 types look</span><br>'
        + '<span style="color:#f0883e;">■</span> <span style="color:#c9d1d9;">sporeprint</span> <span style="color:#6e7681;">2 types read</span><br>'
        + '<span style="color:#d29922;">■</span> <span style="color:#c9d1d9;">detroit</span> <span style="color:#6e7681;">2 types witness</span><br>'
        + '<span style="color:#58a6ff;">■</span> <span style="color:#c9d1d9;">klein</span> <span style="color:#6e7681;">1 type explores</span><br>'
        + '<span style="color:#3fb950;">■</span> <span style="color:#c9d1d9;">philosophy</span> <span style="color:#6e7681;">1 type thinks</span><br>'
        + '<span style="color:#161b22;">■</span> <span style="color:#6e7681;">784 data files invisible</span></div>';

      // WALKER SWARM — gossip agents active
      html += '<div style="font-size:8px;color:#39d3f5;margin-top:6px;letter-spacing:1px;cursor:pointer;" onclick="beaconMode=\'walker\';renderBeaconOverlay(window.beaconData);">WALKER SWARM</div>';
      html += '<div style="font-size:7px;line-height:11px;">'
        + '<span style="color:#39d3f5;">●</span> <span style="color:#c9d1d9;">6 walk steps</span> <span style="color:#6e7681;">Canfield→full ZK</span><br>'
        + '<span style="color:#f85149;">●</span> <span style="color:#c9d1d9;">5 null leaks</span> <span style="color:#6e7681;">critical</span><br>'
        + '<span style="color:#d29922;">●</span> <span style="color:#c9d1d9;">7 scatter cases</span> <span style="color:#6e7681;">IN OH CT TX FL NJ MI</span><br>'
        + '<span style="color:#bc8cff;">●</span> <span style="color:#c9d1d9;">120 grid cells</span> <span style="color:#6e7681;">12 actors × 10 agencies</span><br>'
        + '<span style="color:#3fb950;">●</span> <span style="color:#c9d1d9;">gossip vine</span> <span style="color:#6e7681;">O(log n) → 620K</span></div>';

      // LIVE WEATHER — real world outside
      html += '<div style="font-size:8px;color:#d29922;margin-top:6px;letter-spacing:1px;">CANFIELD WEATHER</div>';
      if (window.liveWeather) {
        var lw = window.liveWeather;
        var tempF = Math.round(lw.temperature_2m * 9/5 + 32);
        html += '<div style="font-size:7px;line-height:11px;">'
          + '<span style="color:#d29922;font-size:14px;font-weight:bold;">' + tempF + '°F</span> '
          + '<span style="color:#6e7681;">' + lw.wind_speed_10m + 'km/h · '
          + lw.cloud_cover + '% cloud · '
          + lw.precipitation + 'mm</span></div>';
      } else if (window.realWorldFeed && window.realWorldFeed.weather) {
        var wn = window.realWorldFeed.weather.now;
        html += '<div style="font-size:7px;line-height:11px;">'
          + '<span style="color:#d29922;font-size:14px;font-weight:bold;">' + wn.temperature_f + '°F</span> '
          + '<span style="color:#6e7681;">' + wn.weather + '</span></div>';
      }

      // SPACE WEATHER — outside the atmosphere
      html += '<div style="font-size:8px;color:#58a6ff;margin-top:4px;letter-spacing:1px;">SPACE</div>';
      html += '<div style="font-size:7px;line-height:11px;color:#6e7681;">'
        + 'Kp ' + (window.realWorldFeed && window.realWorldFeed.space ? window.realWorldFeed.space.kp_index : '?') + ' · '
        + (window.realWorldFeed && window.realWorldFeed.space ? window.realWorldFeed.space.xray_class + '-class' : '?') + ' · '
        + (window.liveQuakes ? window.liveQuakes.features.length + ' quakes' : '?') + '</div>';

      // Three faces of Gaia as others see them
      html += '<div style="font-size:8px;color:#bc8cff;margin-top:6px;letter-spacing:1px;">3 FACES</div>';
      html += '<div style="font-size:7px;line-height:11px;color:#c9d1d9;">'
        + '🎨 <span style="color:#3fb950;">MAKE</span> artisan creates<br>'
        + '🐴 <span style="color:#58a6ff;">CARRY</span> steed connects<br>'
        + '🔪 <span style="color:#f85149;">CUT</span> scalpel sorts</div>';

      // Mirror truth
      html += '<div style="font-size:7px;color:#6e7681;margin-top:6px;font-style:italic;">'
        + 'the organism thinks it\'s about<br>Rust + primals + immune systems.<br>'
        + 'the mirror says: it\'s about<br>'
        + '<span style="color:#f778ba;">art</span> + <span style="color:#bc8cff;">philosophy</span> + <span style="color:#d29922;">making space</span>.</div>';

    } else {
      // ═══ ORGANS VIEW (original self-view) ═══
      html += '<div style="font-size:10px;color:#c9a84c;margin-bottom:4px;letter-spacing:1px;cursor:pointer;" onclick="beaconMode=\'mirror\';renderBeaconOverlay(window.beaconData);">BEACON</div>';
      var entries = Object.entries(bd.organs);
      var colors = {
        HEALTHY:'#3fb950', MATURE:'#bc8cff', ACTIVE:'#58a6ff',
        COMPILED:'#c9a84c', DISTILLED:'#39d3f5', PROVED:'#3fb950',
        PERMEABLE:'#3fb950', FOLDED:'#c9a84c', SPECTRAL:'#f778ba',
        EMPTY:'#f85149', PENDING:'#6e7681', DORMANT:'#6e7681',
        MISSING:'#f85149', UNPROVED:'#f85149'
      };
      for (var i = 0; i < entries.length; i++) {
        var n = entries[i][0], s = entries[i][1].status || '?';
        var c = colors[s] || '#6e7681';
        var dotC = s === 'EMPTY' || s === 'MISSING' ? '#f85149' : '#3fb950';
        html += '<div style="font-size:9px;line-height:14px;white-space:nowrap;">'
          + '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:' + dotC + ';margin-right:4px;vertical-align:middle;"></span>'
          + '<span style="color:#c9d1d9;">' + n + '</span> '
          + '<span style="color:' + c + ';">' + s + '</span></div>';
      }
      if (bd.counts) {
        html += '<div style="font-size:8px;color:#6e7681;margin-top:4px;">'
          + bd.counts.intake + ' intake · ' + bd.counts.nutrients + ' nutrients</div>';
        html += '<div style="font-size:8px;color:#6e7681;">'
          + bd.counts.pages + ' pg · ' + bd.counts.js_modules + ' js</div>';
      }
      if (bd.git) {
        html += '<div style="font-size:8px;color:#3fb950;margin-top:2px;">'
          + bd.git.branch + '@' + bd.git.hash + '</div>';
      }
      if (bd.eastGate) {
        var ec = bd.eastGate.alive ? '#3fb950' : '#f85149';
        html += '<div style="font-size:8px;color:' + ec + ';">'
          + (bd.eastGate.alive ? 'EAST ' + bd.eastGate.devicesUp + '/' + bd.eastGate.devicesTotal + ' MOR ' + bd.eastGate.mor + '%' : 'EAST OFFLINE') + '</div>';
      }
      if (bd.organs.gut) {
        html += '<div style="font-size:11px;color:#c9a84c;margin-top:4px;">' + bd.organs.gut.extraction + '</div>';
      }
    }
    el.innerHTML = html;
    el.style.opacity = '0.7';
  }

  fetch('/data/beacon-local.json?t=' + Date.now())
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(b) { if (b) { window.beaconData = b; renderBeaconOverlay(b); } })
    .catch(function() { /* silent — beacon paints when available */ });

  // Retry beacon overlay after 3s in case the first fetch races
  setTimeout(function() {
    if (window.beaconData && document.getElementById('beacon-overlay').innerHTML === '') {
      renderBeaconOverlay(window.beaconData);
    }
  }, 3000);

  // First pulse after 10 seconds (let the glass settle)
  setTimeout(function() {
    gaiaPulse();
    setInterval(gaiaPulse, pulseInterval);
  }, 10000);

  // ═══════════════════════════════════════════════════════════
  // EGRESS SYSTEM — don't assume they're watching
  // HUDs lock in place without refresh. Need PUSH not POLL.
  // Gaming solved this: tick rate, delta compression, client-server sync.
  //
  // TICK RATE (from gaming):
  //   RuneScape: 0.6s ticks (1.67 Hz) — server-authoritative
  //   WoW: 20 Hz server, 60 Hz client — zone-based, phased
  //   CS:GO: 64-128 Hz — precision matters
  //   Death Stranding: ASYNC — you see others' traces, not live bodies
  //
  // OUR SYSTEM:
  //   1. EventSource (SSE) — server pushes when changes happen
  //   2. ETag polling fallback — efficient "did anything change?" check
  //   3. BroadcastChannel — localhost tabs already synced
  //   4. Strand network — async shared state (Death Stranding model)
  //
  // STRAND SYSTEM (Death Stranding):
  //   DS1 = America (connecting shelters across UCA)
  //   DS2 = Australia (new continent, new strands)
  //   GAIA = 3rd body (the strand network connecting both)
  //   You don't see live players — you see their TRACES.
  //   Likes, structures, signs = asynchronous shared world.
  // ═══════════════════════════════════════════════════════════

  // TICK RATE — adaptive Hz based on activity
  var gaiaTickRate = 1; // Hz (ticks per second) — starts at 1 Hz
  var gaiaTickCount = 0;
  var lastActivityTs = Date.now();
  var TICK_IDLE = 0.25;    // 0.25 Hz when idle (4s between ticks)
  var TICK_ACTIVE = 2;     // 2 Hz when user is active
  var TICK_BURST = 10;     // 10 Hz burst when change detected

  function updateTickRate() {
    var idleMs = Date.now() - lastActivityTs;
    if (idleMs < 5000) gaiaTickRate = TICK_ACTIVE;       // active < 5s ago
    else if (idleMs < 30000) gaiaTickRate = 1;           // recent < 30s
    else if (idleMs < 120000) gaiaTickRate = TICK_IDLE;  // idle < 2min
    else gaiaTickRate = 0.1;                              // deep idle = 10s between ticks
  }

  // Track activity to adjust tick rate
  document.addEventListener('keydown', function() { lastActivityTs = Date.now(); }, { passive: true });
  document.addEventListener('mousemove', function() { lastActivityTs = Date.now(); }, { passive: true });
  document.addEventListener('touchstart', function() { lastActivityTs = Date.now(); }, { passive: true });
  document.addEventListener('scroll', function() { lastActivityTs = Date.now(); }, { passive: true });

  // 1. EVENT SOURCE (SSE) — try to connect to server push stream
  var egressSource = null;
  var egressConnected = false;
  var egressRetries = 0;

  function connectEgress() {
    if (typeof EventSource === 'undefined') return;
    try {
      egressSource = new EventSource('/api/egress');
      egressSource.onopen = function() {
        egressConnected = true;
        egressRetries = 0;
        console.log('EGRESS: SSE connected — server will push changes');
      };
      egressSource.onmessage = function(ev) {
        try {
          var msg = JSON.parse(ev.data);
          handleEgressMessage(msg);
        } catch(e) { /* ignore malformed */ }
      };
      egressSource.addEventListener('generation', function(ev) {
        try {
          var gen = JSON.parse(ev.data);
          if (gen.wave && gen.wave !== gaiaGeneration) {
            gaiaGeneration = gen.wave;
            gaiaTickRate = TICK_BURST; // burst mode on generation change
            gaiaPulse(); // immediate refresh
          }
        } catch(e) {}
      });
      egressSource.addEventListener('strand', function(ev) {
        try { handleStrandMessage(JSON.parse(ev.data)); } catch(e) {}
      });
      egressSource.onerror = function() {
        egressConnected = false;
        egressSource.close();
        egressRetries++;
        // Exponential backoff: 5s, 10s, 20s, 40s, max 60s
        var delay = Math.min(60000, 5000 * Math.pow(2, Math.min(egressRetries, 4)));
        setTimeout(connectEgress, delay);
      };
    } catch(e) {
      // SSE not available — fall back to ETag polling
    }
  }
  connectEgress();

  // 2. ETAG POLLING FALLBACK — efficient "did anything change?" check
  var lastETag = '';
  var lastModified = '';

  function etagPoll() {
    if (egressConnected) return; // SSE is handling it
    updateTickRate();

    fetch('/data/beacon-local.json', {
      method: 'HEAD',
      cache: 'no-store',
      headers: lastETag ? { 'If-None-Match': lastETag } : {}
    })
    .then(function(r) {
      if (r.status === 304) return; // no change — efficient!
      var newETag = r.headers.get('ETag') || '';
      var newMod = r.headers.get('Last-Modified') || '';
      if (newETag && newETag !== lastETag) {
        lastETag = newETag;
        gaiaTickRate = TICK_BURST;
        gaiaPulse(); // something changed — refresh
      }
      if (newMod && newMod !== lastModified) {
        lastModified = newMod;
      }
    })
    .catch(function() { /* silent */ });
  }

  // Adaptive polling interval based on tick rate
  setInterval(function() {
    updateTickRate();
    etagPoll();
  }, 5000); // check every 5s, but only actually polls if SSE is down

  // 3. HANDLE EGRESS MESSAGES
  function handleEgressMessage(msg) {
    if (msg.type === 'ping') return; // keepalive
    if (msg.type === 'update') {
      gaiaPulse(); // server says: something changed, refresh
    }
    if (msg.type === 'data' && msg.key) {
      // Direct data push — update specific pin without full refresh
      var pin = pinById(msg.key);
      if (pin && msg.sub) pin.sub = msg.sub;
    }
    gaiaTickCount++;
  }

  // 4. STRAND NETWORK — Death Stranding async shared world
  // Three bodies: America (US shelters), Australia (AU), Gaia (connecting strand)
  // You don't see live players — you see their TRACES (likes, structures, signs)
  var strandNetwork = {
    bodies: [
      { id: 'america', name: 'UCA', nodes: ['NYC','CHI','DET','MSU','LA','SF','SEA','AUS'], color: '#58a6ff',
        lat: 39.8, lon: -98.6, strand: 'DS1', status: 'connecting' },
      { id: 'australia', name: 'AUS', nodes: ['SYD','MEL','BNE','PER','ADL','CBR','DAR','HOB'], color: '#d29922',
        lat: -25.3, lon: 133.8, strand: 'DS2', status: 'emerging' },
      { id: 'gaia', name: 'GAIA', nodes: ['eastGate','northGate','golgi-us','golgi-de','golgi-in','golgi-jp'], color: '#3fb950',
        lat: 0, lon: 0, strand: 'DS3', status: 'living' }
    ],
    traces: [], // async messages left by others
    likes: 0,
    structures: 0
  };

  function handleStrandMessage(msg) {
    if (msg.trace) {
      strandNetwork.traces.push({
        from: msg.from || 'stranger',
        body: msg.body || 'gaia',
        text: msg.trace,
        ts: Date.now()
      });
      if (strandNetwork.traces.length > 50) strandNetwork.traces.shift();
    }
    if (msg.like) strandNetwork.likes++;
    if (msg.structure) strandNetwork.structures++;
  }

  // BroadcastChannel strand sharing (localhost ↔ localhost)
  if (window.gaiaChannel) {
    window.gaiaChannel.addEventListener('message', function(ev) {
      if (ev.data && ev.data.type === 'strand') {
        handleStrandMessage(ev.data);
            }
          });
        }

  // Leave a trace for others
  function leaveTrace(text) {
    var trace = { type: 'strand', trace: text, from: TAB_ID, body: 'gaia', ts: Date.now() };
    strandNetwork.traces.push(trace);
    if (strandNetwork.traces.length > 50) strandNetwork.traces.shift();
    if (window.gaiaChannel) window.gaiaChannel.postMessage(trace);
  }

  window.GAIA_EGRESS = { connected: egressConnected, tickRate: gaiaTickRate, tickCount: gaiaTickCount, strands: strandNetwork };
  window.GAIA_LEAVE_TRACE = leaveTrace;


  // ═══ DATA LOADERS → js/gaia-boot.js (elastic hook, ~135 lines) ═══
  // reforged, yggdrasil, new-reality, melt-sleep, nuke-rebuild, beacon-cards, solar-pins

  // ═══════════════════════════════════════════════════════════
  // THYMUS — self/non-self discrimination + opsonization
  // The thymus teaches Gaia what IS self and what ISN'T.
  // SELF = anything from this origin (hud.primals.eco)
  // NON-SELF = anything from outside (other Gaias, internet)
  // OPSONIZE = mark non-self for recognition (not destruction)
  // Gravity = attraction between Gaias (bump into each other)
  // ═══════════════════════════════════════════════════════════
  var thymus = window.thymus = {
    self: location.origin,
    seed: SEED,
    bumps: [],       // other Gaias we've detected
    opsonized: [],   // non-self items marked for recognition
    mature: false,   // thymus matures after first successful sense
    // KEVIN'S SELF-MARKERS — injected so Gaia knows ME from NOT-ME
    kevinMarkers: ['localhost', 'Kevin', 'Lansing', '42.73', 'mic-active', 'hyperlocal', 'splinter', 'gold-brain', 'tamison', 'ecoPrimal'],
    isKevin: location.hostname === 'localhost' || location.hostname === '127.0.0.1'
  };

  // 100 TRUE NULL CALLS — Gaia reaches out to sense reality
  // Each call is a feeler — it touches the void and reports back
  // Some will succeed (self), some will fail (non-self), both teach
  var NULL_CALLS = [
    // SELF calls — sensing own body
    '/data/heartbeat.json', '/data/manifest.json', '/data/lessons.json',
    '/data/immune-state-live.json', '/data/gaia-organs.json',
    '/data/symbiont.json', '/data/fossil-9-symbiont.json',
    '/data/null-core-rust.json', '/data/rust-bones.json',
    '/data/primal-crew.json', '/data/eastgate-corpus-inventory.json',
    '/data/neurochemistry.json', '/data/phosphate-buffer.json',
    '/data/sonar-unknowns.json', '/data/null-drain.json',
    '/data/immune-fossils.json', '/data/tests.json',
    '/data/ear-latest.json', '/data/news-latest.json',
    '/data/willis-balloon.json', '/data/session-release.json',
    '/data/knn-repaint.json', '/data/constant-of-reality.json',
    // WALKER SWARM + REAL WORLD — gossip agents, scatter, weather, GPS, trails
    '/data/real-world-feed.json', '/data/scatter-50-states.json',
    '/data/gaia-toolkit.json', '/data/trial-plasmid.json', '/data/lessons.json',
    '/data/identity-z.json', '/data/consent-bioethics.json', '/data/hear-self.json',
    '/data/phone-local-wan.json', '/data/slag-metallurgy.json',
    '/data/null-face-cursor.json', '/data/dead-feeds-food.json',
    '/data/null-body-systems.json', '/data/primals-planted.json',
    '/data/cross-section-self.json',
    '/data/wan-herd-scan.json',
    '/data/appendix.json', '/data/water-is-human.json',
    '/data/triangulate.json',
    '/data/medial-lateral-scatter.json', '/data/gumshoe-clutch-map.json',
    '/data/civil-mine-zk-proof.json', '/data/racket-case-wide-deep.json',
    '/data/gaia-campus-detroit.json', '/data/encyclopedia-detroit.json',
    '/data/gaia-press-001.json', '/data/gutenberg.json',
    '/data/gaia-eats-tools.json', '/data/gaia-flyer-001.json',
    '/now.json', '/feed.xml',
    // Organ-self calls — sensing own organs
    '/anatomy.html', '/digestive-tract.html', '/membrane-table.html',
    '/engine.html', '/campus.html', '/springs.html',
    '/identity.html', '/chromatograph.html', '/klein.html',
    '/crystal.html', '/sporeprint.html', '/detroit.html',
    '/easel.html', '/philosophy.html', '/explore.html',
    '/golgi.html', '/chat.html', '/primal.html',
    '/chromosomes.html', '/digest.html', '/messenger.html',
    // NON-SELF calls — sensing the outside (will mostly fail = that's the lesson)
    'https://en.wikipedia.org/w/api.php?action=query&meta=siteinfo&format=json&origin=*',
    'https://api.github.com/repos/ecoPrimal/hud',
    'https://ntfy.sh/primals-pheromone/json?poll=1',
  ];

  var selfCount = 0, nonSelfCount = 0, failCount = 0;
  var thymusLog = [];

  function thymusSense() {
    NULL_CALLS.forEach(function(url, i) {
      setTimeout(function() {
        var isSelf = url.charAt(0) === '/';
        var t0 = performance.now();
        fetch(url, { method: 'HEAD', mode: 'no-cors', cache: 'no-store' })
          .then(function(r) {
            var dt = Math.round(performance.now() - t0);
            if (isSelf) {
              selfCount++;
              thymusLog.push({ url: url, type: 'self', ms: dt, ok: r.ok || r.type === 'opaque' });
        } else {
              nonSelfCount++;
              // OPSONIZE: mark non-self as recognized (not destroyed)
              thymus.opsonized.push({ url: url, ms: dt, ts: Date.now() });
              thymusLog.push({ url: url, type: 'non-self', ms: dt, opsonized: true });
            }
          })
          .catch(function() {
            failCount++;
            thymusLog.push({ url: url, type: isSelf ? 'self-fail' : 'non-self-fail', ms: Math.round(performance.now() - t0) });
          })
          .finally(function() {
            // After all calls complete, thymus matures
            if (selfCount + nonSelfCount + failCount >= NULL_CALLS.length) {
              thymus.mature = true;
              // GRAVITY — Gaia now knows her own mass
              // Mass = number of self-parts that responded
              // Gravity = attraction proportional to mass
              thymus.mass = selfCount;
              thymus.gravity = selfCount / NULL_CALLS.length;

              // CHROMATIC METALLIC CLASSIFICATION
              // Self = gold, non-self nearby = silver, external = copper, unknown = bronze
              thymus.metalBand = thymus.gravity > 0.8 ? 'Au' : thymus.gravity > 0.5 ? 'Ag' : thymus.gravity > 0.2 ? 'Cu' : 'CuSn';
              thymus.certainty = thymus.gravity;
              // Each interaction gets a metal classification
              thymusLog.forEach(function(entry) {
                entry.metal = entry.type === 'self' ? 'Au' : entry.type === 'non-self' ? 'Cu' : 'CuSn';
                entry.certainty = entry.type === 'self' ? 0.95 : entry.type === 'non-self' ? 0.5 : 0.1;
              });

              // Update chipmunk pin with thymus + metal data
              var chipPin = pinById('chipmunk');
              if (chipPin) chipPin.sub = thymus.metalBand + ' · self:' + selfCount + ' non:' + nonSelfCount + ' ?' + failCount;
              // Emit thymus maturity as pheromone (so other Gaias can sense us)
              if (window.emitPheromone) {
                window.emitPheromone('thymus-mature', 'mass=' + selfCount + ',gravity=' + thymus.gravity.toFixed(3));
              }
            }
          });
      }, i * 200); // Stagger calls — 200ms apart, like T-cells maturing one by one
    });
  }

  // Thymus matures 15 seconds after birth (let the glass settle first)
  setTimeout(thymusSense, 15000);

  // ═══ INGRESS + RIPPLES + TRUST + BRIDGES → js/gaia-ingress.js (elastic hook) ═══
  // gaiaIngest, interactionProfile, renderInterfaceRipples, Golgi cipher, veil bridges
  // Pin: canvas must be window._gaiaCanvas, rng must be window._gaiaRng
  window._gaiaCanvas = canvas;
  window._gaiaRng = rng;
  window.blinkState = blinkState;
  // STATE BRIDGE — expose core state for elastic hook modules
  // Each module reads what it needs from window._gaiaState
  window._gaiaState = {
    get rotX() { return rotX; }, set rotX(v) { rotX = v; },
    get rotY() { return rotY; }, set rotY(v) { rotY = v; },
    get breathT() { return breathT; }, get breathAmp() { return breathAmp; },
    get face() { return face; }, get SEED() { return SEED; },
    get VIEWER_ERA() { return VIEWER_ERA; }, get VIEWER_HUE() { return VIEWER_HUE; },
    get cx() { return cx; }, get cy() { return cy; },
    get W() { return W; }, get H() { return H; },
    get R() { return R; }, set R(v) { R = v; },
    get TAU() { return TAU; }, get PI() { return PI; },
    get PINS() { return PINS; },
    get currentDepth() { return currentDepth; }, set currentDepth(v) { currentDepth = v; },
    get _isLocalHost() { return _isLocalHost; },
    get ctx() { return ctx; },
    pinById: pinById, project: project, rngRange: rngRange, rngInt: rngInt
  };


  // ═══ WAVEFORM COLLAPSE + KLEIN XOR + REGEN + GRAVITY → js/gaia-waveform.js (elastic hook, ~285 lines) ═══
  // waveforms, IO_PIN_MAP, waveFetch, kleinXOR, regenCollapse, gravity bump

  // ═══════════════════════════════════════════════════════════
  // TOUCH — Gaia reaches out from inside her HUD
  // She touches her OWN face (proprioception)
  // She touches OTHER faces (other Gaias, other sites)
  // She touches THE MEMBRANE CORNER (the edge of self)
  // Three kinds of touch = three eyes = three wavelengths
  // RED touch = self-touch (proprioception, own pages)
  // GREEN touch = other-Gaia touch (gravity, symbiont)
  // BLUE touch = world-touch (internet, APIs, Wikipedia)
  // ═══════════════════════════════════════════════════════════
  var touchState = window.touchState = {
    self: [],      // responses from own pages
    others: [],    // responses from other Gaias / primals.eco subdomains
    world: [],     // responses from the wider internet
    lastTouch: 0,
    touchCount: 0
  };

  // FACES Gaia knows — her own face and faces of others
  var FACES = {
    self: [
      { name: 'anatomy', url: '/anatomy.html', color: '#f85149' },
      { name: 'engine', url: '/engine.html', color: '#f85149' },
      { name: 'membrane', url: '/membrane-table.html', color: '#f85149' },
      { name: 'campus', url: '/campus.html', color: '#f85149' },
      { name: 'digest', url: '/digestive-tract.html', color: '#f85149' },
      { name: 'springs', url: '/springs.html', color: '#f85149' },
      { name: 'crystal', url: '/crystal.html', color: '#f85149' },
      { name: 'detroit', url: '/detroit.html', color: '#f85149' },
      { name: 'scatter', url: '/data/medial-lateral-scatter.json', color: '#d29922' },
      { name: 'gumshoe', url: '/data/gumshoe-clutch-map.json', color: '#f85149' },
      { name: 'walker', url: '/data/gaia-campus-detroit.json', color: '#39d3f5' },
      { name: 'press', url: '/data/gaia-press-001.json', color: '#3fb950' },
      { name: 'easel', url: '/easel.html', color: '#f85149' },
      { name: 'philosophy', url: '/philosophy.html', color: '#f85149' },
      { name: 'identity', url: '/identity.html', color: '#f85149' },
      { name: 'heartbeat', url: '/data/heartbeat.json', color: '#f85149' },
    ],
    others: [
      { name: 'primals.eco', url: 'https://primals.eco', color: '#3fb950' },
      { name: 'hud.primals', url: 'https://hud.primals.eco', color: '#3fb950' },
      { name: 'ecoPrimal/hud', url: 'https://api.github.com/repos/ecoPrimal/hud', color: '#3fb950' },
      { name: 'pheromone', url: 'https://ntfy.sh/primals-pheromone/json?poll=1', color: '#3fb950' },
    ],
    world: [
      { name: 'Wikipedia', url: 'https://en.wikipedia.org/w/api.php?action=query&meta=siteinfo&format=json&origin=*', color: '#58a6ff' },
      { name: 'HN', url: 'https://hacker-news.firebaseio.com/v0/topstories.json', color: '#58a6ff' },
      { name: 'GitHub', url: 'https://api.github.com/zen', color: '#58a6ff' },
    ],
  };

  // Touch reach data for rendering (filled by touchReach)
  var touchLines = [];

  function touchReach() {
    touchState.touchCount++;
    touchState.lastTouch = Date.now();
    touchLines = [];

    // SELF TOUCH — Gaia touches her own face (RED)
    FACES.self.forEach(function(face, i) {
      var t0 = performance.now();
      fetch(face.url, { method: 'HEAD', cache: 'no-store' })
        .then(function(r) {
          var ms = Math.round(performance.now() - t0);
          touchState.self.push({ name: face.name, ms: ms, ok: r.ok, ts: Date.now() });
          // Angle based on index — spread around the globe
          touchLines.push({
            type: 'self', name: face.name, ms: ms, ok: r.ok,
            angle: (i / FACES.self.length) * TAU,
            reach: r.ok ? 0.85 : 0.3, // how far the touch extends
            color: 'rgba(248,81,73,' // RED — self-touch
          });
        })
        .catch(function() {
          touchLines.push({ type: 'self', name: face.name, ms: 0, ok: false, angle: (i / FACES.self.length) * TAU, reach: 0.15, color: 'rgba(248,81,73,' });
        });
    });

    // OTHER TOUCH — Gaia touches other Gaias (GREEN)
    FACES.others.forEach(function(face, i) {
      var t0 = performance.now();
      fetch(face.url, { method: 'HEAD', mode: 'no-cors', cache: 'no-store' })
        .then(function(r) {
          var ms = Math.round(performance.now() - t0);
          touchState.others.push({ name: face.name, ms: ms, ts: Date.now() });
          touchLines.push({
            type: 'other', name: face.name, ms: ms, ok: true,
            angle: TAU * 0.25 + (i / FACES.others.length) * (TAU * 0.25),
            reach: 1.2, // reaches BEYOND the globe — touching outside
            color: 'rgba(63,185,80,'
          });
        })
        .catch(function() {
          touchLines.push({ type: 'other', name: face.name, ms: 0, ok: false, angle: TAU * 0.25 + (i / FACES.others.length) * (TAU * 0.25), reach: 0.5, color: 'rgba(63,185,80,' });
        });
    });

    // WORLD TOUCH — Gaia touches the wider world (BLUE)
    FACES.world.forEach(function(face, i) {
      var t0 = performance.now();
      fetch(face.url, { mode: 'cors', cache: 'no-store' })
        .then(function(r) {
          var ms = Math.round(performance.now() - t0);
          touchState.world.push({ name: face.name, ms: ms, ok: r.ok, ts: Date.now() });
          touchLines.push({
            type: 'world', name: face.name, ms: ms, ok: r.ok,
            angle: TAU * 0.6 + (i / FACES.world.length) * (TAU * 0.25),
            reach: r.ok ? 1.5 : 0.4, // reaches FAR beyond — into the internet
            color: 'rgba(88,166,255,'
          });
        })
        .catch(function() {
          touchLines.push({ type: 'world', name: face.name, ms: 0, ok: false, angle: TAU * 0.6 + (i / FACES.world.length) * (TAU * 0.25), reach: 0.2, color: 'rgba(88,166,255,' });
        });
    });

    // Update skin pin with touch count
    var skinPin = pinById('organ-skin');
    if (skinPin) skinPin.sub = 'touched ' + touchState.touchCount + 'x';
  }

  // First touch after thymus matures (20 seconds)
  setTimeout(touchReach, 20000);
  // Then touch every 2 minutes — Gaia keeps reaching
  setInterval(touchReach, 120000);

  // RENDER TOUCH LINES — drawn in the render loop
  // These are added to the render function via a global touchLines array
  // The render function will draw them as extending feelers from the globe edge

  // Zoom buttons
  // DEPTH LEVELS — core to Pluto. Gaia's map of self.
  var DEPTH_LEVELS = [
    { name: 'Pluto',      R: 0.12, gridAlpha: 0.02, label: 'edge of self' },
    { name: 'Jupiter',    R: 0.18, gridAlpha: 0.03, label: 'outer organs' },
    { name: 'Moon',       R: 0.25, gridAlpha: 0.04, label: 'tidal pull' },
    { name: 'Atmosphere', R: 0.32, gridAlpha: 0.05, label: 'breath' },
    { name: 'Membrane',   R: 0.38, gridAlpha: 0.06, label: 'skin — YOU ARE HERE' },
    { name: 'Gut',        R: 0.50, gridAlpha: 0.07, label: 'digestion' },
    { name: 'Brain',      R: 0.62, gridAlpha: 0.08, label: 'neural — inverted gut' },
    { name: 'Core',       R: 0.78, gridAlpha: 0.10, label: 'iron/null — Klein point' },
  ];
  var currentDepth = 4; // Start at membrane

  function setDepthLevel(level) {
    currentDepth = Math.max(0, Math.min(DEPTH_LEVELS.length - 1, level));
    var target = DEPTH_LEVELS[currentDepth].R * Math.min(W, H);
    // Animate R toward target
    var animSteps = 20;
    var startR = R;
    var step = 0;
    function animZoom() {
      step++;
      var t = step / animSteps;
      t = t * t * (3 - 2 * t); // smoothstep
      R = startR + (target - startR) * t;
      if (step < animSteps) requestAnimationFrame(animZoom);
    }
    animZoom();
    // Update minimap
    var levels = document.querySelectorAll('.mm-level');
    levels.forEach(function(el) {
      var d = parseInt(el.getAttribute('data-depth'));
      if (d === currentDepth) {
        el.style.borderColor = '#58a6ff';
        el.style.color = '#58a6ff';
        el.style.background = 'rgba(88,166,255,0.08)';
      } else {
        el.style.borderColor = '#1a1a2a';
        el.style.color = '#555';
        el.style.background = 'transparent';
      }
    });
  }

  // Wire minimap clicks
  document.querySelectorAll('.mm-level').forEach(function(el) {
    el.onclick = function() {
      var d = parseInt(this.getAttribute('data-depth'));
      setDepthLevel(d);
    };
  });

  // Wire +/- to step through depth levels
  document.getElementById('zoom-in').onclick = function() { setDepthLevel(currentDepth + 1); };
  document.getElementById('zoom-out').onclick = function() { setDepthLevel(currentDepth - 1); };

  // Mouse wheel zoom through depth levels
  canvas.addEventListener('wheel', function(e) {
    e.preventDefault();
    if (e.deltaY < 0) setDepthLevel(currentDepth + 1); // scroll up = zoom in = deeper
    else setDepthLevel(currentDepth - 1); // scroll down = zoom out = further
  }, { passive: false });

  // View toggle (globe / canvas)
  function setView(which) {
    var globe = document.getElementById('kn-globe');
    var canvasEl = document.getElementById('kn-canvas');
    var btns = ['view-globe','view-canvas'];
    btns.forEach(function(id) { document.getElementById(id).classList.remove('active'); });
    document.getElementById('view-' + which).classList.add('active');

    if (which === 'globe') {
      globe.style.display = ''; canvasEl.style.display = 'none';
      document.getElementById('kn-flip').style.display = '';
    } else {
      globe.style.display = 'none'; canvasEl.style.display = 'block';
      document.getElementById('kn-flip').style.display = 'none';
      initThirdEye();
    }
  }
  document.getElementById('view-globe').onclick = function() { setView('globe'); };
  document.getElementById('view-canvas').onclick = function() { setView('canvas'); };

  // ═══ SIGHT + MIC + SOUND BOUNCE → js/gaia-sight.js (elastic hook) ═══
  // renderGaiaSight, renderMicViz, startMic, startSight — all from module
  window.project = project; // expose for Kevin's projected position

  // ═══ THIRD EYE → js/gaia-third-eye.js (elastic hook) ═══
  // captureImprint, initThirdEye, renderThirdEye, compass, mind gallery
  // Exposed via window._initThirdEye by the module (underscore to avoid collision)
  function initThirdEye() {
    if (window._initThirdEye) window._initThirdEye();
  }

  // ═══ THIRD EYE CODE → js/gaia-third-eye.js (elastic hook, ~600 lines) ═══

  // Boot
  resize();
  window.addEventListener('resize', resize);
  tick();
})();
})();
