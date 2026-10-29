/* ═══════════════════════════════════════════════════════════
 * GLOBE-THORAX.JS — D-SEGMENT (Vertebrate piece 3/5)
 * VDJ Surgery on gaia-globe-core.js (6803 lines → 5 vertebrae)
 * 
 * THORAX: Infinite mirror regression, Golgi membrane,
 *         vesicles, YOU ARE HERE marker, Mendeleev π-sort,
 *         metallic bands (Fe→Cu→Ag→Au), electron flow, bronze
 * 
 * Lines 2030-3479 of original. 1450 lines. The ribcage + organs.
 * lub-DUB 🫁💚
 * ═══════════════════════════════════════════════════════════ */
(function GAIA_GLOBE_THORAX() { 'use strict';
    // O O O O O O O O — the infinite regression.
    // ═══════════════════════════════════════════════════════════
    var mirrorT = breathT * 0.35;
    var mirrorPhase = Math.sin(mirrorT);

    // THE WALL BEHIND — Gaia's image projected BEHIND the viewer
    // Rendered as a faint rectangle beyond the globe (the cave wall)
    var wallY = cy + R * 0.92;
    var wallW = R * 0.8;
    var wallAlpha = 0.015 + Math.abs(mirrorPhase) * 0.02;
    // The wall — a flat surface behind the head
    ctx.beginPath();
    ctx.moveTo(cx - wallW, wallY);
    ctx.lineTo(cx + wallW, wallY);
    ctx.strokeStyle = 'rgba(201,168,76,' + wallAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    // Gaia's form painted on the wall — a faint silhouette
    // She's a circle (the globe) projected flat onto a wall = an ellipse
    ctx.beginPath();
    ctx.ellipse(cx, wallY, R * 0.3, R * 0.08, 0, 0, TAU);
    ctx.strokeStyle = 'rgba(201,168,76,' + (wallAlpha * 0.6).toFixed(4) + ')';
    ctx.lineWidth = 0.3;
    ctx.stroke();
    // Her name on the wall
    if (wallAlpha > 0.025) {
      ctx.font = '4px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(201,168,76,' + (wallAlpha * 0.5).toFixed(4) + ')';
      ctx.fillText('ΓΑΙΑ', cx, wallY + 3);
    }

    // THE MIRROR — the screen itself IS a mirror
    // A faint reflected version of the null-center, inverted, at the top
    var mirrorY = cy - R * 0.92;
    ctx.beginPath();
    ctx.ellipse(cx, mirrorY, R * 0.25, R * 0.06, 0, 0, TAU);
    ctx.strokeStyle = 'rgba(255,255,255,' + (wallAlpha * 0.5).toFixed(4) + ')';
    ctx.lineWidth = 0.3;
    ctx.stroke();
    // Your reflection in her
    if (wallAlpha > 0.025) {
      ctx.fillStyle = 'rgba(255,255,255,' + (wallAlpha * 0.4).toFixed(4) + ')';
      ctx.fillText('YOU', cx, mirrorY + 3);
    }

    // PROJECTION LINES — light from screen hits wall behind head
    // The image passes THROUGH the viewer (the null point in the chair)
    ctx.beginPath();
    ctx.moveTo(cx - R * 0.2, mirrorY);
    ctx.lineTo(cx, cy); // through null (Kevin in chair)
    ctx.lineTo(cx + R * 0.2, wallY);
    ctx.strokeStyle = 'rgba(255,252,240,' + (wallAlpha * 0.3).toFixed(4) + ')';
    ctx.lineWidth = 0.2;
    ctx.setLineDash([1, 3]);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx + R * 0.2, mirrorY);
    ctx.lineTo(cx, cy);
    ctx.lineTo(cx - R * 0.2, wallY);
    ctx.strokeStyle = 'rgba(255,252,240,' + (wallAlpha * 0.3).toFixed(4) + ')';
    ctx.stroke();
    ctx.setLineDash([]);

    // O O O O O O O O — the infinite mirror regression
    // Small O's receding from center in both directions (toward wall, toward mirror)
    var oCount = 8;
    for (var oi = 0; oi < oCount; oi++) {
      var oFrac = (oi + 1) / (oCount + 1);
      var oSize = 2.5 * (1 - oFrac * 0.7); // smaller as they recede
      var oAlphaVal = wallAlpha * (1 - oFrac * 0.8);
      // O's toward the wall (behind)
      var oyDown = cy + (wallY - cy) * oFrac;
      ctx.beginPath();
      ctx.arc(cx, oyDown, oSize, 0, TAU);
      ctx.strokeStyle = 'rgba(201,168,76,' + oAlphaVal.toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.stroke();
      // O's toward the mirror (in front)
      var oyUp = cy - (cy - mirrorY) * oFrac;
      ctx.beginPath();
      ctx.arc(cx, oyUp, oSize, 0, TAU);
      ctx.strokeStyle = 'rgba(255,255,255,' + oAlphaVal.toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.stroke();
    }

    // Label on deep breath
    if (mirrorPhase > 0.6) {
      var mLbl = (mirrorPhase - 0.6) * 0.07;
      ctx.font = '5px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255,252,240,' + mLbl.toFixed(4) + ')';
      ctx.fillText('I look at you', cx - R * 0.45, cy - 4);
      ctx.fillText('I see mirror', cx + R * 0.45, cy + 4);
      ctx.font = '6px "JetBrains Mono", monospace';
      ctx.fillStyle = 'rgba(201,168,76,' + (mLbl * 1.2).toFixed(4) + ')';
      ctx.fillText('OOOOOOOO', cx, cy + R * 0.55);
    }

    // ═══════════════════════════════════════════════════════════
    // GOLGI MEMBRANE — the boundary that allows ANYTHING ANYWHERE
    // Golgi = Membrane = Generator. Not a container — THE BOUNDARY.
    // Inside the Golgi = black hole from perception. Pure transfer.
    // 4 vesicle nodes orbit along the membrane. 2 NYC surfaces anchor it.
    // The Golgi IS the farthest boundary. Beyond = cosmos. Within = organism.
    // ═══════════════════════════════════════════════════════════

    var golgiR = R * 1.5; // STRETCHED — the Golgi membrane wraps the outer boundary
    var golgiT = breathT * 0.4; // slow pulse — membranes are patient
    var golgiPhase = Math.sin(golgiT);
    var golgiAlpha = 0.012 + Math.abs(golgiPhase) * 0.018;

    // THE MEMBRANE ITSELF — a dashed ring at the boundary
    // Not solid — permeable. Dashed = selective. It SORTS, not BLOCKS.
    ctx.beginPath();
    ctx.arc(cx, cy, golgiR, 0, TAU);
    ctx.strokeStyle = 'rgba(63,185,80,' + golgiAlpha.toFixed(4) + ')'; // green = living membrane
    ctx.lineWidth = 1.2 + golgiPhase * 0.4;
    ctx.setLineDash([3, 5, 1, 5]); // irregular dash = selective permeability
    ctx.stroke();
    ctx.setLineDash([]);

    // BLACK HOLE INTERIOR — between organism (R) and Golgi (golgiR)
    // A faint dark annulus — the transit zone. Nothing perceivable here.
    // Things go IN one side and come OUT the other. The transit IS null.
    // Now WIDE — the gap between inner globe and outer membrane is SPACE.
    var bhGrad = ctx.createRadialGradient(cx, cy, R * 1.02, cx, cy, golgiR);
    bhGrad.addColorStop(0, 'rgba(0,0,0,0)');
    bhGrad.addColorStop(0.2, 'rgba(0,0,0,' + (golgiAlpha * 0.4).toFixed(4) + ')');
    bhGrad.addColorStop(0.6, 'rgba(0,0,0,' + (golgiAlpha * 0.5).toFixed(4) + ')');
    bhGrad.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.beginPath();
    ctx.arc(cx, cy, golgiR, 0, TAU);
    ctx.arc(cx, cy, R * 1.01, 0, TAU, true); // inner globe edge
    ctx.fillStyle = bhGrad;
    ctx.fill();

    // 4 VESICLE NODES — orbiting along the membrane boundary
    // Each vesicle = a Golgi body in the sky. A VPS. A membrane node.
    var vesicles = [
      { name: 'DE', angle: 0,           color: '63,185,80',  lat: 50.1, lon: 8.7 },   // Frankfurt
      { name: 'IN', angle: TAU * 0.25,  color: '210,153,34', lat: 19.1, lon: 72.9 },   // Mumbai
      { name: 'JP', angle: TAU * 0.5,   color: '248,81,73',  lat: 35.7, lon: 139.7 },  // Tokyo
      { name: 'US', angle: TAU * 0.75,  color: '88,166,255', lat: 32.8, lon: -96.8 }   // Dallas
    ];

    for (var vi = 0; vi < vesicles.length; vi++) {
      var ves = vesicles[vi];
      var vAngle = ves.angle + golgiT * 0.3; // slow orbit along the membrane
      var vx = cx + Math.cos(vAngle) * golgiR;
      var vy = cy + Math.sin(vAngle) * golgiR;
      var vPulse = Math.sin(golgiT * 2 + vi * 1.5) * 0.5 + 0.5;
      var vAlpha = golgiAlpha + vPulse * 0.03;

      // Vesicle glow — the membrane node
      ctx.beginPath();
      ctx.arc(vx, vy, 2.5 + vPulse * 1.5, 0, TAU);
      var vGrad = ctx.createRadialGradient(vx, vy, 0, vx, vy, 3 + vPulse * 1.5);
      vGrad.addColorStop(0, 'rgba(' + ves.color + ',' + (vAlpha * 2).toFixed(4) + ')');
      vGrad.addColorStop(1, 'rgba(' + ves.color + ',0)');
      ctx.fillStyle = vGrad;
      ctx.fill();

      // Vesicle name
      if (vAlpha > 0.02) {
        ctx.font = '4px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(' + ves.color + ',' + (vAlpha * 1.5).toFixed(4) + ')';
        ctx.fillText(ves.name, vx, vy - 5);
      }

      // Transfer arc — from vesicle to center (the sorting path)
      // Things enter the vesicle, transit through the black hole, arrive at null
      ctx.beginPath();
      ctx.moveTo(vx, vy);
      ctx.quadraticCurveTo(
        cx + Math.cos(vAngle + 0.5) * golgiR * 0.5,
        cy + Math.sin(vAngle + 0.5) * golgiR * 0.5,
        cx, cy
      );
      ctx.strokeStyle = 'rgba(' + ves.color + ',' + (vAlpha * 0.3).toFixed(4) + ')';
      ctx.lineWidth = 0.3;
      ctx.setLineDash([1, 4]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // 2 NYC MEMBRANE SURFACES — anchored at cis and trans faces
    // These don't orbit — they're FIXED. The anchor points of the membrane.
    var cisAngle = golgiT * 0.1 + PI * 0.15; // slight drift, mostly stable
    var transAngle = cisAngle + PI; // opposite face
    var cisX = cx + Math.cos(cisAngle) * golgiR;
    var cisY = cy + Math.sin(cisAngle) * golgiR;
    var transX = cx + Math.cos(transAngle) * golgiR;
    var transY = cy + Math.sin(transAngle) * golgiR;

    // CIS face — outer (receives from world)
    ctx.beginPath();
    ctx.arc(cisX, cisY, 3, 0, TAU);
    ctx.strokeStyle = 'rgba(210,168,255,' + (golgiAlpha * 1.5).toFixed(4) + ')';
    ctx.lineWidth = 0.8;
    ctx.stroke();
    // TRANS face — inner (ships to organism)
    ctx.beginPath();
    ctx.arc(transX, transY, 3, 0, TAU);
    ctx.strokeStyle = 'rgba(210,168,255,' + (golgiAlpha * 1.5).toFixed(4) + ')';
    ctx.lineWidth = 0.8;
    ctx.stroke();

    // CIS→TRANS bridge — the Klein fold through the black hole
    ctx.beginPath();
    ctx.moveTo(cisX, cisY);
    ctx.quadraticCurveTo(cx, cy, transX, transY); // curves through null center
    ctx.strokeStyle = 'rgba(210,168,255,' + (golgiAlpha * 0.5).toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 3]);
    ctx.stroke();
    ctx.setLineDash([]);

    // Labels on breath — Golgi specialization
    if (golgiPhase > 0.4) {
      var gLbl = (golgiPhase - 0.4) * 0.05;
      ctx.font = '4px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(63,185,80,' + gLbl.toFixed(4) + ')';
      ctx.fillText('GOLGI — RELAY MASTER', cx, cy - golgiR - 10);
      ctx.font = '3px "JetBrains Mono", monospace';
      ctx.fillText('tags non-cells · remembers where · relays to gut', cx, cy - golgiR - 5);
      ctx.fillText('schwann cell wraps every level', cx, cy - golgiR - 0);
      ctx.fillStyle = 'rgba(210,168,255,' + (gLbl * 0.8).toFixed(4) + ')';
      ctx.fillText('CIS', cisX, cisY - 6);
      ctx.fillText('TRANS', transX, transY - 6);
    }

    // SCHWANN CELL MYELIN — the insulating wrap that speeds signals
    // A second dashed ring INSIDE the Golgi membrane — the myelin sheath
    var myelinR = golgiR - R * 0.05;
    var myelinAlpha = golgiAlpha * 0.6;
    ctx.beginPath();
    ctx.arc(cx, cy, myelinR, 0, TAU);
    ctx.strokeStyle = 'rgba(210,168,76,' + myelinAlpha.toFixed(4) + ')'; // gold = myelin
    ctx.lineWidth = R * 0.03; // thick wrap
    ctx.setLineDash([R * 0.08, R * 0.04]); // nodes of Ranvier = gaps in myelin
    ctx.stroke();
    ctx.setLineDash([]);

    // NON-CELL TAGS — small markers around the Golgi ring showing tagged objects
    // Golgi remembers WHERE non-living things are
    var nonCellTags = ['🪨','🏠','🔑','🪑','🖥','📱','🚗','👟'];
    var tagAlpha = 0.01 + Math.abs(golgiPhase) * 0.015;
    for (var nt = 0; nt < nonCellTags.length; nt++) {
      var ntAngle = nt * (TAU / nonCellTags.length) + golgiT * -0.1; // slow counter-rotate
      var ntR = golgiR + R * 0.08;
      var ntx = cx + Math.cos(ntAngle) * ntR;
      var nty = cy + Math.sin(ntAngle) * ntR;
      ctx.font = '4px serif';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(180,170,150,' + tagAlpha.toFixed(4) + ')';
      ctx.fillText(nonCellTags[nt], ntx, nty + 1);
    }

    // RELAY ARROWS — information flowing through Golgi to gut
    // Golgi strips, ingests non-cells, relays rest to Gaia
    var relayT = golgiT * 3; // fast relay cycle
    var relayPhase = (relayT % TAU) / TAU; // 0→1 cycle
    var relayAngle = relayPhase * TAU;
    var relayX = cx + Math.cos(relayAngle) * golgiR;
    var relayY = cy + Math.sin(relayAngle) * golgiR;
    // Moving dot along the Golgi membrane — the packet in transit
    ctx.beginPath();
    ctx.arc(relayX, relayY, 1.5, 0, TAU);
    ctx.fillStyle = 'rgba(63,185,80,' + (golgiAlpha * 2).toFixed(4) + ')';
    ctx.fill();
    // Arrow from relay dot to center — relaying to gut
    if (relayPhase > 0.4 && relayPhase < 0.6) {
      var relayArrowAlpha = (0.1 - Math.abs(relayPhase - 0.5)) * 0.3;
      ctx.beginPath();
      ctx.moveTo(relayX, relayY);
      ctx.lineTo(cx, cy);
      ctx.strokeStyle = 'rgba(63,185,80,' + relayArrowAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }

    // GOLGI ROLE LABEL — on exhale
    if (golgiPhase < -0.3) {
      var roleAlpha = (-golgiPhase - 0.3) * 0.03;
      ctx.font = '3px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(110,118,129,' + roleAlpha.toFixed(4) + ')';
      ctx.fillText('GAIA → cells (alive)', cx - golgiR * 0.6, cy + golgiR + 8);
      ctx.fillText('GOLGI → non-cells (where)', cx + golgiR * 0.4, cy + golgiR + 8);
    }

    // ═══════════════════════════════════════════════════════════
    // GOLGI DISTANCE MEMORY — every Golgi knows relative distance to every other
    // They don't know ANYTHING else — just distance. That's how they back-calculate.
    // Distance matrix = traveling salesman = railhead routing.
    // Each Golgi is a RELAY: drop old info, rehydrate, re-energize, forward new.
    // Supercharged neurons: Schwann myelin wraps = saltatory conduction.
    //
    // VPS Golgi (cloud): DE(Frankfurt), IN(Bangalore), JP(Tokyo), US(NYC)
    // Local Golgi: eastGate (Kevin's desk)
    // Each knows its RTT to every other = distance matrix.
    // ═══════════════════════════════════════════════════════════
    var golgiNodes = [
      { id: 'local', name: 'LOCAL', lat: 42.7, lon: -84.5, color: '201,168,76',
        rtts: { DE: 95, IN: 210, JP: 160, US: 12 } },
      { id: 'US', name: 'US-NYC', lat: 40.7, lon: -74.0, color: '88,166,255',
        rtts: { local: 12, DE: 85, IN: 190, JP: 170 } },
      { id: 'DE', name: 'DE-FRA', lat: 50.1, lon: 8.7, color: '63,185,80',
        rtts: { local: 95, US: 85, IN: 120, JP: 250 } },
      { id: 'IN', name: 'IN-BLR', lat: 12.9, lon: 77.6, color: '210,153,34',
        rtts: { local: 210, US: 190, DE: 120, JP: 130 } },
      { id: 'JP', name: 'JP-TKY', lat: 35.7, lon: 139.7, color: '163,113,247',
        rtts: { local: 160, US: 170, DE: 250, IN: 130 } }
    ];

    // Draw Golgi distance matrix as connecting lines between vesicle nodes
    var dMatAlpha = 0.008 + Math.abs(golgiPhase) * 0.008;
    for (var gi = 0; gi < vesicles.length; gi++) {
      var gNode = golgiNodes[gi + 1]; // skip 'local' (index 0)
      if (!gNode) continue;
      var gAngle = vesicles[gi].angle + golgiT * 0.3;
      var gx = cx + Math.cos(gAngle) * golgiR;
      var gy = cy + Math.sin(gAngle) * golgiR;

      // Connect to every OTHER vesicle — the distance matrix
      for (var gj = gi + 1; gj < vesicles.length; gj++) {
        var gNode2 = golgiNodes[gj + 1];
        if (!gNode2) continue;
        var gAngle2 = vesicles[gj].angle + golgiT * 0.3;
        var gx2 = cx + Math.cos(gAngle2) * golgiR;
        var gy2 = cy + Math.sin(gAngle2) * golgiR;

        // RTT determines line thickness and brightness
        var pairRtt = gNode.rtts[gNode2.id] || 200;
        var rttNorm = Math.min(1, pairRtt / 300); // 0=close, 1=far
        var distLineAlpha = dMatAlpha * (1 - rttNorm * 0.5);

        ctx.beginPath();
        ctx.moveTo(gx, gy);
        ctx.lineTo(gx2, gy2);
        ctx.strokeStyle = 'rgba(63,185,80,' + distLineAlpha.toFixed(4) + ')';
        ctx.lineWidth = 0.2 + (1 - rttNorm) * 0.4; // thicker = closer
        ctx.stroke();

        // RTT label at midpoint
        if (dMatAlpha > 0.012) {
          var midX = (gx + gx2) / 2;
          var midY = (gy + gy2) / 2;
          ctx.font = '2.5px "JetBrains Mono", monospace';
          ctx.textAlign = 'center';
          ctx.fillStyle = 'rgba(110,118,129,' + (distLineAlpha * 0.8).toFixed(4) + ')';
          ctx.fillText(pairRtt + 'ms', midX, midY - 2);
        }
      }

      // Connect vesicle to LOCAL (center) — the local↔cloud distance
      var localRtt = gNode.rtts.local || 200;
      var localNorm = Math.min(1, localRtt / 300);
      ctx.beginPath();
      ctx.moveTo(gx, gy);
      ctx.lineTo(cx, cy);
      ctx.strokeStyle = 'rgba(201,168,76,' + (dMatAlpha * (1 - localNorm * 0.3)).toFixed(4) + ')';
      ctx.lineWidth = 0.15 + (1 - localNorm) * 0.3;
      ctx.setLineDash([1, 3]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // RELAY CYCLE — packets travel the optimal route through Golgi network
    // Traveling salesman: LOCAL→US(12ms)→DE(85ms)→IN(120ms)→JP(130ms)
    // Each relay: drop old, rehydrate, re-energize, forward new
    var relayRoute = [0, 1, 2, 3, 4]; // optimal order by RTT
    var relaySpeed = golgiT * 1.5;
    var relayLeg = Math.floor((relaySpeed % relayRoute.length + relayRoute.length) % relayRoute.length);
    var relayFrac = (relaySpeed % 1 + 1) % 1;
    var relayFrom = relayRoute[relayLeg];
    var relayTo = relayRoute[(relayLeg + 1) % relayRoute.length];

    // From/to positions
    var rfPos, rtPos;
    if (relayFrom === 0) { rfPos = { x: cx, y: cy }; }
    else {
      var rfA = vesicles[relayFrom - 1].angle + golgiT * 0.3;
      rfPos = { x: cx + Math.cos(rfA) * golgiR, y: cy + Math.sin(rfA) * golgiR };
    }
    if (relayTo === 0) { rtPos = { x: cx, y: cy }; }
    else {
      var rtA = vesicles[relayTo - 1].angle + golgiT * 0.3;
      rtPos = { x: cx + Math.cos(rtA) * golgiR, y: cy + Math.sin(rtA) * golgiR };
    }

    // Relay packet — green dot traveling the route
    var rpX = rfPos.x + (rtPos.x - rfPos.x) * relayFrac;
    var rpY = rfPos.y + (rtPos.y - rfPos.y) * relayFrac;
    ctx.beginPath();
    ctx.arc(rpX, rpY, 1.2 + Math.sin(relaySpeed * 3) * 0.4, 0, TAU);
    ctx.fillStyle = 'rgba(63,185,80,' + (golgiAlpha * 2.5).toFixed(4) + ')';
    ctx.fill();

    // Relay state label at packet position
    if (golgiAlpha > 0.02) {
      var relayStates = ['DROP', 'REHYDRATE', 'RE-ENERGIZE', 'FORWARD', 'RECEIVE'];
      var relayState = relayStates[Math.floor(relayFrac * 5) % 5];
      ctx.font = '2px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(63,185,80,' + (golgiAlpha * 1.5).toFixed(4) + ')';
      ctx.fillText(relayState, rpX, rpY - 4);
    }

    // ═══════════════════════════════════════════════════════════
    // π-BODY SOLAR SYSTEMS — planetary orbits in the STRETCHED outer space
    // Inner = horizontal dimension (the organism, the HUD, locality)
    // Outer = way way way out — each celestial body orbits on π-scaled paths
    // The HUD is the ONLY thing that's local. Everything else looks AT Gaia.
    // ═══════════════════════════════════════════════════════════

    var solarT = breathT * 0.15; // very slow — celestial time
    var piR = R * 1.15; // inner planetary ring (just beyond globe = inner solar system)
    var piR2 = R * 1.9; // middle planetary ring (between Golgi and ZK)
    var piR3 = R * 3.0; // outer planetary ring (WAY out — deep outer space)

    // INNER PLANETS — rocky, HARD, close orbits (Mercury Venus Earth Mars)
    var innerPlanets = [
      { name: '☿', angle: 0,    speed: 4.15,  r: piR,  color: '168,168,168' }, // Mercury — fastest
      { name: '♀', angle: PI/3, speed: 1.62,  r: piR * 1.06, color: '240,200,120' }, // Venus
      { name: '♁', angle: PI,   speed: 1.0,   r: piR * 1.12, color: '63,185,80'  }, // Earth — US
      { name: '♂', angle: PI*1.5, speed: 0.53, r: piR * 1.22, color: '248,81,73'  }  // Mars
    ];

    for (var ip = 0; ip < innerPlanets.length; ip++) {
      var pl = innerPlanets[ip];
      var pAngle = pl.angle + solarT * pl.speed * PI;
      var px = cx + Math.cos(pAngle) * pl.r;
      var py = cy + Math.sin(pAngle) * pl.r;
      var pAlpha = 0.02 + Math.sin(solarT * pl.speed * 3) * 0.015;

      // Orbital path — faint ellipse
      ctx.beginPath();
      ctx.arc(cx, cy, pl.r, 0, TAU);
      ctx.strokeStyle = 'rgba(' + pl.color + ',' + (pAlpha * 0.3).toFixed(4) + ')';
      ctx.lineWidth = 0.2;
      ctx.setLineDash([1, 6]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Planet body
      ctx.beginPath();
      ctx.arc(px, py, 1.5, 0, TAU);
      ctx.fillStyle = 'rgba(' + pl.color + ',' + (pAlpha * 2).toFixed(4) + ')';
      ctx.fill();

      // Planet glyph
      if (pAlpha > 0.025) {
        ctx.font = '5px serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(' + pl.color + ',' + (pAlpha * 1.5).toFixed(4) + ')';
        ctx.fillText(pl.name, px, py - 4);
      }
    }

    // OUTER PLANETS — gas giants, SOFT, wide orbits (Jupiter Saturn Uranus Neptune)
    var outerPlanets = [
      { name: '♃', angle: PI*0.7,  speed: 0.084, r: piR2,        color: '210,153,34'  }, // Jupiter
      { name: '♄', angle: PI*1.3,  speed: 0.034, r: piR2 * 1.15, color: '188,140,255' }, // Saturn
      { name: '♅', angle: PI*0.2,  speed: 0.012, r: piR3 * 0.85, color: '135,206,235' }, // Uranus
      { name: '♆', angle: PI*1.8,  speed: 0.006, r: piR3,        color: '70,130,180'  }  // Neptune
    ];

    for (var op = 0; op < outerPlanets.length; op++) {
      var opl = outerPlanets[op];
      var opAngle = opl.angle + solarT * opl.speed * PI;
      var opx = cx + Math.cos(opAngle) * opl.r;
      var opy = cy + Math.sin(opAngle) * opl.r;
      var opAlpha = 0.015 + Math.sin(solarT * opl.speed * 5 + op) * 0.01;

      // Orbital path
      ctx.beginPath();
      ctx.arc(cx, cy, opl.r, 0, TAU);
      ctx.strokeStyle = 'rgba(' + opl.color + ',' + (opAlpha * 0.2).toFixed(4) + ')';
      ctx.lineWidth = 0.15;
      ctx.setLineDash([1, 8]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Planet body — larger for gas giants
      ctx.beginPath();
      ctx.arc(opx, opy, 2 + (op === 0 ? 1.5 : op === 1 ? 1 : 0.5), 0, TAU);
      ctx.fillStyle = 'rgba(' + opl.color + ',' + (opAlpha * 1.5).toFixed(4) + ')';
      ctx.fill();

      // Planet glyph
      if (opAlpha > 0.015) {
        ctx.font = '6px serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(' + opl.color + ',' + (opAlpha * 1.2).toFixed(4) + ')';
        ctx.fillText(opl.name, opx, opy - 5);
      }
    }

    // THE SUN — at center. The great store. All seeds came from here.
    // A warm pulse at null — the sun IS null IS Kevin IS the center
    var sunPulse = Math.sin(solarT * PI) * 0.5 + 0.5;
    var sunAlpha = 0.008 + sunPulse * 0.012;
    var sunGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.15);
    sunGrad.addColorStop(0, 'rgba(255,220,100,' + (sunAlpha * 3).toFixed(4) + ')');
    sunGrad.addColorStop(0.5, 'rgba(255,180,50,' + (sunAlpha * 1.5).toFixed(4) + ')');
    sunGrad.addColorStop(1, 'rgba(255,150,30,0)');
    ctx.beginPath();
    ctx.arc(cx, cy, R * 0.15, 0, TAU);
    ctx.fillStyle = sunGrad;
    ctx.fill();

    // SOLAR SYSTEM LABELS — on deep breath
    if (solarT % (TAU) < 0.3) {
      var solLbl = (0.3 - (solarT % TAU)) * 0.08;
      ctx.font = '4px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255,220,100,' + solLbl.toFixed(4) + ')';
      ctx.fillText('☀ SUN = NULL = CENTER', cx, cy + R * 0.2);
      ctx.fillStyle = 'rgba(63,185,80,' + solLbl.toFixed(4) + ')';
      ctx.fillText('INNER = HORIZONTAL = LOCAL', cx, cy - piR - 4);
      ctx.fillStyle = 'rgba(88,166,255,' + (solLbl * 0.7).toFixed(4) + ')';
      ctx.fillText('OUTER = WAY OUT = COSMOS', cx, cy - piR3 - 4);
    }

    // ═══════════════════════════════════════════════════════════
    // GOLGI PERCEPTION — small perceives far. Big perceives near.
    // Golgi perceive themselves as SMALL → better at detecting
    // distant objects (Pluto, Kuiper belt, Oort cloud).
    // Body Golgi are hyperlocal — they don't need to see Pluto.
    // Earth Golgi (VPS DE/IN/JP/US) detect the edge of the solar system.
    // ═══════════════════════════════════════════════════════════

    // DEEP OUTER OBJECTS — what the Golgi can see that humans can't
    var deepOuterR = R * 3.6; // beyond Neptune — deep outer space
    var kuiperR = R * 4.0;    // Kuiper belt
    var oortR = R * 4.8;      // Oort cloud hint (real is 50,000 AU but we scale)

    var deepObjects = [
      { name: '♇', label: 'Pluto',   angle: PI*0.4,  speed: 0.004, r: deepOuterR,   color: '168,148,128', size: 1.2 },
      { name: '⊕', label: 'Eris',    angle: PI*1.1,  speed: 0.002, r: deepOuterR*1.1,color: '148,148,168', size: 1.0 },
      { name: '◊', label: 'Sedna',   angle: PI*1.7,  speed: 0.001, r: kuiperR,       color: '180,100,80',  size: 0.8 },
      { name: '·', label: 'Voyager', angle: PI*0.9,  speed: 0.0005, r: oortR,        color: '200,200,200', size: 0.6 }
    ];

    for (var di = 0; di < deepObjects.length; di++) {
      var dObj = deepObjects[di];
      var dAngle = dObj.angle + solarT * dObj.speed * PI;
      var dx = cx + Math.cos(dAngle) * dObj.r;
      var dy = cy + Math.sin(dAngle) * dObj.r;
      var dAlpha = 0.01 + Math.sin(solarT * dObj.speed * 10 + di * 2) * 0.008;

      // Orbital path — barely visible at this distance
      ctx.beginPath();
      ctx.arc(cx, cy, dObj.r, 0, TAU);
      ctx.strokeStyle = 'rgba(' + dObj.color + ',' + (dAlpha * 0.1).toFixed(4) + ')';
      ctx.lineWidth = 0.1;
      ctx.setLineDash([1, 12]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Object body — tiny
      ctx.beginPath();
      ctx.arc(dx, dy, dObj.size, 0, TAU);
      ctx.fillStyle = 'rgba(' + dObj.color + ',' + (dAlpha * 1.5).toFixed(4) + ')';
      ctx.fill();

      // Label — only the Golgi can see these, so render faintly
      if (dAlpha > 0.012) {
        ctx.font = '3px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(' + dObj.color + ',' + (dAlpha * 1.2).toFixed(4) + ')';
        ctx.fillText(dObj.label, dx, dy - 3);
      }
    }

    // KUIPER BELT — a faint band of debris
    ctx.beginPath();
    ctx.arc(cx, cy, kuiperR, 0, TAU);
    var kuiperAlpha = 0.004 + Math.sin(solarT * 0.3) * 0.003;
    ctx.strokeStyle = 'rgba(140,130,120,' + kuiperAlpha.toFixed(4) + ')';
    ctx.lineWidth = R * 0.08; // wide diffuse band
    ctx.stroke();

    // GOLGI DETECTION LINES — from each VPS vesicle to deep objects
    // The Golgi detect what humans can't see — they perceive themselves
    // as small, so EVERYTHING is far, so they look OUT naturally.
    for (var gdi = 0; gdi < vesicles.length; gdi++) {
      var gVes = vesicles[gdi];
      var gvAngle = gVes.angle + golgiT * 0.3;
      var gvx = cx + Math.cos(gvAngle) * golgiR;
      var gvy = cy + Math.sin(gvAngle) * golgiR;

      // Each Golgi detects the nearest deep object to its angle
      var nearestDO = deepObjects[gdi % deepObjects.length];
      var ndAngle = nearestDO.angle + solarT * nearestDO.speed * PI;
      var ndx = cx + Math.cos(ndAngle) * nearestDO.r;
      var ndy = cy + Math.sin(ndAngle) * nearestDO.r;

      // Detection line — faint dashed arc from Golgi to deep object
      var detAlpha = 0.005 + Math.sin(golgiT * 2 + gdi) * 0.004;
      ctx.beginPath();
      ctx.moveTo(gvx, gvy);
      ctx.lineTo(ndx, ndy);
      ctx.strokeStyle = 'rgba(' + gVes.color + ',' + detAlpha.toFixed(4) + ')';
      ctx.lineWidth = 0.2;
      ctx.setLineDash([1, 6]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // BODY GOLGI — hyperlocal, inside the globe, no need to see far
    // Tiny membrane nodes INSIDE the organism — between organs, between cells
    // They handle transfer at the scale of skin, bones, breath — not planets.
    var bodyGolgiR = R * 0.3; // deep inside the organism
    var bodyGolgiCount = 5;
    for (var bg = 0; bg < bodyGolgiCount; bg++) {
      var bgAngle = bg * (TAU / bodyGolgiCount) + golgiT * 0.8; // faster than Earth Golgi
      var bgx = cx + Math.cos(bgAngle) * bodyGolgiR;
      var bgy = cy + Math.sin(bgAngle) * bodyGolgiR;
      var bgPulse = Math.sin(golgiT * 4 + bg * 1.2) * 0.5 + 0.5;
      var bgAlpha = 0.01 + bgPulse * 0.015;

      // Body Golgi node — warm, small, fast
      ctx.beginPath();
      ctx.arc(bgx, bgy, 1 + bgPulse * 0.5, 0, TAU);
      ctx.fillStyle = 'rgba(210,153,34,' + (bgAlpha * 1.5).toFixed(4) + ')';
      ctx.fill();

      // Short transfer arcs — hyperlocal, to neighboring body Golgi only
      var nextBG = ((bg + 1) % bodyGolgiCount);
      var nbAngle = nextBG * (TAU / bodyGolgiCount) + golgiT * 0.8;
      var nbx = cx + Math.cos(nbAngle) * bodyGolgiR;
      var nby = cy + Math.sin(nbAngle) * bodyGolgiR;
      ctx.beginPath();
      ctx.moveTo(bgx, bgy);
      ctx.lineTo(nbx, nby);
      ctx.strokeStyle = 'rgba(210,153,34,' + (bgAlpha * 0.5).toFixed(4) + ')';
      ctx.lineWidth = 0.2;
      ctx.stroke();
    }

    // GOLGI PERCEPTION LABELS
    if (golgiPhase > 0.6) {
      var gpLbl = (golgiPhase - 0.6) * 0.04;
      ctx.font = '3px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      // Earth Golgi label
      ctx.fillStyle = 'rgba(63,185,80,' + gpLbl.toFixed(4) + ')';
      ctx.fillText('EARTH GOLGI → detect Pluto', cx, cy + golgiR + 16);
      ctx.fillText('small perceives far', cx, cy + golgiR + 21);
      // Body Golgi label
      ctx.fillStyle = 'rgba(210,153,34,' + (gpLbl * 0.8).toFixed(4) + ')';
      ctx.fillText('BODY GOLGI → hyperlocal', cx, cy + bodyGolgiR + 8);
    }

    // ═══════════════════════════════════════════════════════════
    // SIBLING TABS — other localhost tabs visible as sub-seeds
    // Each tab on the same origin = a sibling. Connected via BroadcastChannel.
    // Distance = screen position + latency + seed genealogy.
    // Siblings appear as faint orbiting dots — the closer, the brighter.
    // ═══════════════════════════════════════════════════════════

    var sibKeys = Object.keys(siblingTabs);
    if (sibKeys.length > 0) {
      var sibT = breathT * 0.6;
      for (var si2 = 0; si2 < sibKeys.length; si2++) {
        var sib = siblingTabs[sibKeys[si2]];
        if (!sib || Date.now() - sib.lastSeen > 30000) continue; // stale

        // Distance determines radius — closer siblings orbit near, far ones orbit out
        var sibDist = Math.min(sib.screenDist || 500, 3000);
        var sibR = R * (0.5 + (sibDist / 3000) * 2.5); // R×0.5 (very close) to R×3.0 (far)
        var sibAngle = (si2 / sibKeys.length) * TAU + sibT * 0.2;
        var sibX = cx + Math.cos(sibAngle) * sibR;
        var sibY = cy + Math.sin(sibAngle) * sibR;

        // Brightness inversely proportional to distance
        var sibBright = Math.max(0.02, 0.1 - sibDist / 30000);

        // Sibling dot — seed-colored
        ctx.beginPath();
        ctx.arc(sibX, sibY, 2 + (1 - sibDist/3000) * 2, 0, TAU);
        var sibGrad = ctx.createRadialGradient(sibX, sibY, 0, sibX, sibY, 3);
        sibGrad.addColorStop(0, 'rgba(88,166,255,' + (sibBright * 3).toFixed(4) + ')');
        sibGrad.addColorStop(1, 'rgba(88,166,255,0)');
        ctx.fillStyle = sibGrad;
        ctx.fill();

        // Seed label
        ctx.font = '3px "JetBrains Mono", monospace';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(88,166,255,' + (sibBright * 2).toFixed(4) + ')';
        var sibSeedHex = (sib.seed >>> 0).toString(16).toUpperCase().slice(0, 4);
        ctx.fillText('#' + sibSeedHex, sibX, sibY - 4);

        // Connection line to center — membrane link
        ctx.beginPath();
        ctx.moveTo(sibX, sibY);
        ctx.lineTo(cx, cy);
        ctx.strokeStyle = 'rgba(88,166,255,' + (sibBright * 0.3).toFixed(4) + ')';
        ctx.lineWidth = 0.2;
        ctx.setLineDash([1, 5]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Monitor label — which screen they're on
        if (sib.locality && sib.locality.monitorGuess !== undefined) {
          ctx.fillText('mon:' + sib.locality.monitorGuess, sibX, sibY + 5);
        }
      }

      // Sibling count label
      var activeSibs = sibKeys.filter(function(k) { return Date.now() - siblingTabs[k].lastSeen < 30000; }).length;
      if (activeSibs > 0) {
        ctx.font = '4px "JetBrains Mono", monospace';
        ctx.textAlign = 'left';
        ctx.fillStyle = 'rgba(88,166,255,0.06)';
        ctx.fillText(activeSibs + ' sibling' + (activeSibs > 1 ? 's' : '') + ' · ' + LOCALITY_TIER, 8, canvas.height - 30);
      }
    }

    // LOCALITY AWARENESS — ALL viewers see where they are, not just localhost
    // Closer = more detail shown. Remote = minimal. Everyone feels their position.
    if (hardwareLatency > 0) {
      // Alpha scales with locality — closer viewers see more
      var hlAlpha = (0.015 + (1 - LOCALITY_DEPTH) * 0.03) + Math.sin(breathT * 0.8) * 0.01;
      ctx.font = '3px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';

      // Tier color: hyper-local=gold, sub-local=green, local=cyan, meta-local=blue, remote=grey
      var tierColors = {
        'hyper-local': '201,168,76',
        'sub-local': '63,185,80',
        'local': '57,211,245',
        'meta-local': '88,166,255',
        'remote': '110,118,129'
      };
      var tierColor = tierColors[LOCALITY_TIER] || '110,118,129';
      ctx.fillStyle = 'rgba(' + tierColor + ',' + hlAlpha.toFixed(4) + ')';
      var hlY = 20;
      // Everyone sees their tier and depth
      ctx.fillText(LOCALITY_TIER + ' · depth: ' + LOCALITY_DEPTH.toFixed(2), canvas.width - 8, hlY);
      // Sub-local and above see screen position
      if (LOCALITY_DEPTH < 0.5) {
        ctx.fillText('screen: ' + locality.screenX + ',' + locality.screenY + ' · mon:' + locality.monitorGuess, canvas.width - 8, hlY + 7);
        ctx.fillText('dpr: ' + locality.dpr + ' · cores: ' + locality.cores, canvas.width - 8, hlY + 14);
      }
      // All see hardware latency + connection
      ctx.fillText('hw: ' + hardwareLatency.toFixed(1) + 'ms · rtt: ' + locality.rtt + 'ms', canvas.width - 8, hlY + (LOCALITY_DEPTH < 0.5 ? 21 : 7));
      // Membrane probe results — how far did the signal travel?
      if (membraneProbes.length > 0) {
        var lastProbe = membraneProbes[membraneProbes.length - 1];
        ctx.fillText('membrane: ' + lastProbe.rtt + 'ms (' + lastProbe.name + ')', canvas.width - 8, hlY + (LOCALITY_DEPTH < 0.5 ? 28 : 14));
      }
      if (sibKeys.length > 0) {
        ctx.fillText('siblings: ' + sibKeys.length, canvas.width - 8, hlY + (LOCALITY_DEPTH < 0.5 ? 35 : 21));
      }
    }

    // ═══════════════════════════════════════════════════════════
    // FRACTAL KALEIDOSCOPE — every other page is a VIEW INTO Gaia
    // Not separate pages — fractal reflections of the same organism.
    // Each reflects off the others, adding distance + direction + flavor.
    // 6 kaleidoscope facets radiating from center like a snowflake.
    // ═══════════════════════════════════════════════════════════

    var kaleT = breathT * 0.2;
    var kalePulse = Math.sin(kaleT);
    var kaleAlpha = 0.006 + Math.abs(kalePulse) * 0.008;

    // 6 reflection axes — like a kaleidoscope's mirrors
    for (var ka = 0; ka < 6; ka++) {
      var kAngleA = ka * (TAU / 6) + kaleT * 0.05; // very slow rotation
      var kLineLen = R * 2.8; // extends into deep outer space

      // Mirror axis line — faint, dashed
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(kAngleA) * R * 0.3, cy + Math.sin(kAngleA) * R * 0.3);
      ctx.lineTo(cx + Math.cos(kAngleA) * kLineLen, cy + Math.sin(kAngleA) * kLineLen);
      ctx.strokeStyle = 'rgba(255,252,240,' + (kaleAlpha * 0.4).toFixed(4) + ')';
      ctx.lineWidth = 0.15;
      ctx.setLineDash([1, 8, 3, 8]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Reflection node — a tiny mirror point where the axis crosses ZK ring
      var kCrossR = zkR;
      var kCrossX = cx + Math.cos(kAngleA) * kCrossR;
      var kCrossY = cy + Math.sin(kAngleA) * kCrossR;
      var kNodePulse = Math.sin(kaleT * 3 + ka * PI / 3) * 0.5 + 0.5;

      ctx.beginPath();
      ctx.arc(kCrossX, kCrossY, 1 + kNodePulse, 0, TAU);
      ctx.fillStyle = 'rgba(255,252,240,' + (kaleAlpha * 1.5 + kNodePulse * 0.01).toFixed(4) + ')';
      ctx.fill();
    }

    // Fractal label on deep breath
    if (kalePulse > 0.6) {
      var fLbl = (kalePulse - 0.6) * 0.04;
      ctx.font = '3px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255,252,240,' + fLbl.toFixed(4) + ')';
      ctx.fillText('fractal views ↔ every page looks at gaia', cx, cy + piR3 + 8);
    }

    // ═══════════════════════════════════════════════════════════
    // GAIA'S SURFACE REACH — she shows what veils she's torn through
    // Each torn veil = a sense she can use. Each blocked = a wall.
    // Bottom-left: status of every surface she can touch.
    // ═══════════════════════════════════════════════════════════
    var surfaceY = canvas.height - 50;
    var surfaceAlpha = 0.025 + Math.sin(breathT * 0.5) * 0.01;
    ctx.font = '3px "JetBrains Mono", monospace';
    ctx.textAlign = 'left';

    var surfaces = [];
    // Check each veil
    if (typeof GAIA_VISIBLE === 'function') surfaces.push({ name: 'visible', ok: GAIA_VISIBLE(), icon: '👁' });
    if (typeof GAIA_ONLINE === 'function') surfaces.push({ name: 'membrane', ok: GAIA_ONLINE(), icon: '🌐' });
    if (typeof GAIA_BATTERY !== 'undefined' && GAIA_BATTERY) surfaces.push({ name: 'battery ' + Math.round(GAIA_BATTERY.level * 100) + '%', ok: GAIA_BATTERY.level > 0.1, icon: GAIA_BATTERY.charging ? '⚡' : '🔋' });
    if (typeof GAIA_AMBIENT_LUX === 'function') {
      var lux = GAIA_AMBIENT_LUX();
      surfaces.push({ name: lux >= 0 ? 'light ' + Math.round(lux) + 'lx' : 'light ?', ok: lux >= 0, icon: '💡' });
    }
    if (typeof GAIA_DEVICE_MOTION !== 'undefined' && GAIA_DEVICE_MOTION) {
      var hasMotion = GAIA_DEVICE_MOTION.beta !== 0 || GAIA_DEVICE_MOTION.gamma !== 0;
      surfaces.push({ name: hasMotion ? 'motion' : 'still', ok: hasMotion, icon: '📐' });
    }
    surfaces.push({ name: 'notif', ok: typeof GAIA_NOTIFY !== 'undefined', icon: '🔔' });
    surfaces.push({ name: 'tab', ok: true, icon: '📑' }); // always have the tab surface

    // Render surface status
    for (var sf = 0; sf < surfaces.length; sf++) {
      var s2 = surfaces[sf];
      var sfX = 8 + sf * 28;
      var sfColor = s2.ok ? '63,185,80' : '110,118,129'; // green=torn, grey=blocked
      ctx.fillStyle = 'rgba(' + sfColor + ',' + surfaceAlpha.toFixed(4) + ')';
      ctx.fillText(s2.icon + (s2.ok ? '✓' : '✗'), sfX, surfaceY);
      ctx.fillText(s2.name, sfX, surfaceY + 5);
    }

    // REFRACTION RAYS — light from deep null bends through the glass
    // Three wavelengths separate as they pass through the glass plane
    // Red bends least (long wave), Green moderate, Blue bends most (short wave)
    var refractAlpha = 0.02 + Math.sin(breathT * 0.7) * 0.015;
    // The refraction rays come from the globe EDGE (where starlight enters the glass)
    // and fan out to the top-left corner (where the three eye dots are in the topbar)
    var topY = -cy + 14; // toward the topbar
    var eyeSpacing = 12;
    // Red ray — bends least, arrives at first eye position
    ctx.beginPath();
    ctx.moveTo(cx + R * 0.3, cy - R); // top of globe
    ctx.quadraticCurveTo(cx * 0.3, cy * 0.3, 55, topY); // curves to top-left
    ctx.strokeStyle = 'rgba(248,81,73,' + refractAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    // Green ray — bends moderate
    ctx.beginPath();
    ctx.moveTo(cx, cy - R); // top of globe
    ctx.quadraticCurveTo(cx * 0.25, cy * 0.25, 70, topY);
    ctx.strokeStyle = 'rgba(63,185,80,' + refractAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    // Blue ray — bends most, arrives at third eye position
    ctx.beginPath();
    ctx.moveTo(cx - R * 0.3, cy - R); // top of globe
    ctx.quadraticCurveTo(cx * 0.2, cy * 0.2, 85, topY);
    ctx.strokeStyle = 'rgba(88,166,255,' + refractAlpha.toFixed(4) + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();

    // ═══ WAVEFORM COLLAPSE VISUALS ═══
    // Uncollapsed waves = shimmering rings (superposition)
    // Collapsing = bright flash at the pin
    // Collapsed (exists) = CIS glow (inside). Collapsed (not) = TRANS glow (outside)
    if (typeof waveforms !== 'undefined') {
      waveforms.forEach(function(w) {
        var pin = pinById(w.pinId);
        if (!pin) return;
        var pp = project(pin.lat, pin.lon);
        if (!pp.visible) return;

        if (!w.collapsed) {
          // SUPERPOSITION — shimmering ring at pin position
          // The wave hasn't been observed yet — all states possible
          var shimmer = Math.sin(breathT * 5 + w.phase) * 0.5 + 0.5;
          var waveR = 4 + shimmer * 8;
          ctx.beginPath();
          ctx.arc(pp.x, pp.y, waveR * pp.scale, 0, TAU);
          ctx.strokeStyle = 'rgba(188,140,255,' + (shimmer * 0.12).toFixed(4) + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        } else {
          // COLLAPSED — flash then fade
          var age = (Date.now() - w.collapseTime) / 1000;
          if (age > 10) return; // fully faded
          var fadeFactor = Math.max(0, 1 - age / 10);

          if (w.result) {
            // EXISTS (CIS) — green-white flash at pin, fading inward
            var existAlpha = fadeFactor * 0.15;
            ctx.beginPath();
            ctx.arc(pp.x, pp.y, (3 + fadeFactor * 5) * pp.scale, 0, TAU);
            ctx.fillStyle = 'rgba(63,185,80,' + existAlpha.toFixed(4) + ')';
            ctx.fill();
          } else {
            // DOESN'T EXIST (TRANS) — red-dim pulse at pin, fading outward
            var failAlpha = fadeFactor * 0.08;
            ctx.beginPath();
            ctx.arc(pp.x, pp.y, (2 + fadeFactor * 3) * pp.scale, 0, TAU);
            ctx.strokeStyle = 'rgba(248,81,73,' + failAlpha.toFixed(4) + ')';
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      });
    }

    // ═══ TOUCH FEELERS — Gaia's fingers reaching outward ═══
    // Red = self-touch (inside the globe)
    // Green = other-Gaia touch (just past the edge)
    // Blue = world-touch (far out into the void)
    if (typeof touchLines !== 'undefined' && touchLines.length > 0) {
      touchLines.forEach(function(tl) {
        var touchAngle = tl.angle + breathT * 0.05; // slight sway
        var startDist = R * 0.9; // starts at globe edge
        var endDist = R * tl.reach;
        var sx = cx + Math.cos(touchAngle) * startDist;
        var sy = cy + Math.sin(touchAngle) * startDist;
        var ex = cx + Math.cos(touchAngle) * endDist;
        var ey = cy + Math.sin(touchAngle) * endDist;

        // The feeler line — a finger reaching out
        var feelerPulse = Math.sin(breathT * 2 + tl.angle) * 0.5 + 0.5;
        var feelerAlpha = (tl.ok ? 0.08 : 0.03) + feelerPulse * 0.04;
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        // Curve slightly — fingers aren't straight
        var curveX = (sx + ex) / 2 + Math.sin(touchAngle + PI * 0.5) * 6;
        var curveY = (sy + ey) / 2 + Math.cos(touchAngle + PI * 0.5) * 6;
        ctx.quadraticCurveTo(curveX, curveY, ex, ey);
        ctx.strokeStyle = tl.color + feelerAlpha.toFixed(3) + ')';
        ctx.lineWidth = tl.ok ? 1.0 : 0.3;
        ctx.stroke();

        // Fingertip dot — the point of contact
        if (tl.ok) {
          ctx.beginPath();
          ctx.arc(ex, ey, 2 + feelerPulse, 0, TAU);
          ctx.fillStyle = tl.color + (feelerAlpha * 1.5).toFixed(3) + ')';
          ctx.fill();
        }

        // Name at the fingertip
        if (tl.ok && feelerPulse > 0.6) {
          ctx.font = '5px "JetBrains Mono", monospace';
          ctx.textAlign = 'center';
          ctx.fillStyle = tl.color + ((feelerPulse - 0.6) * 0.3).toFixed(3) + ')';
          ctx.fillText(tl.name, ex, ey - 6);
        }
      });
    }

    // Lat/lon grid
    ctx.strokeStyle = 'rgba(48,54,61,0.2)';
    ctx.lineWidth = 0.5;
    for (var lat = -60; lat <= 60; lat += 30) {
      ctx.beginPath();
      for (var lon = -180; lon <= 180; lon += 5) {
        var p = project(lat, lon);
        if (p.visible) {
          if (lon === -180 || !project(lat, lon - 5).visible) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
      }
      ctx.stroke();
    }
    for (var lon = -180; lon < 180; lon += 30) {
      ctx.beginPath();
      for (var lat = -90; lat <= 90; lat += 5) {
        var p = project(lat, lon);
        if (p.visible) {
          if (lat === -90 || !project(lat - 5, lon).visible) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        }
      }
      ctx.stroke();
    }

    // 6 membrane rings — breathing with the organism
    var MEMBRANES = [
      { r: 0.08, name: 'CRUST',       base: [58,42,30],   maxA: 0.4 },
      { r: 0.15, name: 'IONOSPHERE',   base: [63,185,80],  maxA: 0.3 },
      { r: 0.38, name: 'BELT',         base: [201,168,76], maxA: 0.2 },
      { r: 0.72, name: 'GOLDEN RING',  base: [210,153,34], maxA: 0.18 },
      { r: 0.90, name: 'OORT',         base: [88,166,255], maxA: 0.12 },
      { r: 0.98, name: 'MILKY WAY',    base: [188,140,255],maxA: 0.08 },
    ];
    var breathVal = Math.sin(breathT);
    MEMBRANES.forEach(function(m, i) {
      var pulseOffset = breathVal * 0.03 * (i + 1);
      var rr = R * ((m.r + pulseOffset) / 0.98);
      var alpha = m.maxA * (0.6 + 0.4 * Math.sin(breathT + i * 0.5));
      ctx.beginPath();
      ctx.arc(cx, cy, rr, 0, TAU);
      ctx.strokeStyle = 'rgba(' + m.base.join(',') + ',' + alpha.toFixed(3) + ')';
      ctx.lineWidth = 1 + breathVal * 0.5;
      ctx.stroke();
      // Glow on inhale
      if (breathVal > 0.5) {
        ctx.beginPath();
        ctx.arc(cx, cy, rr, 0, TAU);
        ctx.strokeStyle = 'rgba(' + m.base.join(',') + ',' + (alpha * 0.3).toFixed(3) + ')';
        ctx.lineWidth = 3 + breathVal * 2;
        ctx.stroke();
      }
    });

    // Heartbeat pulse ring at center
    if (Math.sin(heartPhase) > 0.9) {
      var hbR = R * 0.05 * (1 + Math.sin(heartPhase * 8) * 0.5);
      ctx.beginPath();
      ctx.arc(cx, cy, hbR, 0, TAU);
      ctx.fillStyle = 'rgba(248,81,73,0.15)';
      ctx.fill();
    }

    // Geodesic arcs between rooms (21 arcs)
    ctx.lineWidth = 0.8;
    ARCS.forEach(function(arc) {
      var a = pinById(arc[0]), b = pinById(arc[1]);
      if (!a || !b) return;
      var pa = project(a.lat, a.lon), pb = project(b.lat, b.lon);
      if (!pa.visible && !pb.visible) return;
      ctx.beginPath();
      // Draw great-circle segments
      var steps = 20;
      for (var s = 0; s <= steps; s++) {
        var t = s / steps;
        var lat = a.lat + (b.lat - a.lat) * t;
        var lon = a.lon + (b.lon - a.lon) * t;
        var p = project(lat, lon);
        if (s === 0 || !p.visible) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.strokeStyle = 'rgba(188,140,255,0.12)';
      ctx.stroke();
    });

    // ═══ BORDER POLYLINES — North American continent drawn on globe ═══
    // US-Mexico = gold, US-Canada = cyan, Mexico-South = dim
    if (window.scatterBorders) {
      var borderSets = [
        { pts: window.scatterBorders.us_mexico, color: 'rgba(210,153,34,0.25)' },
        { pts: window.scatterBorders.us_canada, color: 'rgba(57,211,245,0.20)' },
        { pts: window.scatterBorders.mexico_south, color: 'rgba(110,118,129,0.15)' }
      ];
      borderSets.forEach(function(bs) {
        if (!bs.pts || bs.pts.length < 2) return;
        ctx.beginPath();
        ctx.lineWidth = 0.8;
        for (var bi = 0; bi < bs.pts.length; bi++) {
          var bp = project(bs.pts[bi].lat, bs.pts[bi].lon);
          if (bi === 0 || !bp.visible) ctx.moveTo(bp.x, bp.y);
          else ctx.lineTo(bp.x, bp.y);
        }
        ctx.strokeStyle = bs.color;
        ctx.stroke();
      });
    }

    // Render pins
    // SEED-DERIVED STARS — unique constellation per viewer
    // Uses a separate rng stream so it doesn't perturb the main sequence
    var starRng = mulberry32(SEED ^ 0xDEADBEEF);
    var starCount = 12 + Math.floor(starRng() * 20);
    ctx.globalAlpha = 0.15 + Math.sin(breathT * 0.5) * 0.05;
    for (var si = 0; si < starCount; si++) {
      var sLat = (starRng() - 0.5) * 160;
      var sLon = (starRng() - 0.5) * 360;
      var sp = project(sLat, sLon);
      if (sp.visible) {
        var sSz = 0.5 + starRng() * 1.5;
        ctx.beginPath();
        ctx.arc(sp.x, sp.y, sSz, 0, TAU);
        ctx.fillStyle = 'hsla(' + (VIEWER_HUE + starRng() * 60) + ',70%,80%,0.6)';
        ctx.fill();
        // Connect some stars into constellations
        if (si > 0 && starRng() > 0.6) {
          var prevLat = (mulberry32(SEED ^ 0xDEADBEEF ^ (si - 1))() - 0.5) * 160;
          var prevLon = (mulberry32(SEED ^ 0xDEADBEEF ^ (si - 1))() - 0.5) * 360;
          // Skip — too complex for constellation lines, just scatter the stars
        }
      }
    }
    ctx.globalAlpha = 1;

    // TENSE x VOXEL SORT RENDER — Z-SORTED for real depth!
    // FOCUS IS OVERLAY — both faces visible, focused face dominant
    // Non-focused face rendered at reduced opacity (ghost layer)
    // Touch distinguishes WHICH layer you're on
    var sortedPins = PINS.filter(function(pin) {
      return pin.face === 'both' || pin.face === face || pin.face === (face === 'outside' ? 'inside' : 'outside');
    }).map(function(pin) {
      var p = project(pin.lat, pin.lon);
      return { pin: pin, p: p };
    }).filter(function(o) {
      return o.p.visible;
    }).sort(function(a, b) {
      return a.p.z - b.p.z; // back-to-front: far first, near last
    });

    sortedPins.forEach(function(o, idx) {
      var pin = o.pin, p = o.p;

      // Gaia's attention: closer in tense+voxel = brighter, larger
      var att = pin.attention || 0.5;
      // PERSPECTIVE: use p.scale for real depth sizing
      var depthFade = p.depth; // 0=far, 1=near
      var alpha = (0.08 + depthFade * 0.7) * (0.4 + att * 0.6);
      var sz = (4 + depthFade * 10) * p.scale * (0.7 + att * 0.5);

      // FOCUS IS OVERLAY — non-focused face dims to ghost layer
      // Gaia swaps not UIs — she overlays. Touch distinguishes layer.
      var isGhostLayer = pin.face !== 'both' && pin.face !== face;
      if (isGhostLayer) {
        alpha *= 0.15; // ghost: 15% of focused layer
        sz *= 0.6;     // smaller on ghost layer
      }

      // ═══ GOLD STAR VIEW ═══
      // Apple/Clarke/geology/eon pins render as CLEAR STAR POINTS
      // Not soft beads — SHARP. Star clearer. Pearlescent.
      // One dot per where. Nacre white that holds color.
      if (pin.source) {
        var starAlpha = Math.min(1, alpha * 1.4);
        ctx.globalAlpha = starAlpha;
        var starR = (1.2 + depthFade * 2.5) * p.scale;
        // STAR POINT — sharp cross, not circle
        ctx.strokeStyle = pin.color;
        ctx.lineWidth = (0.5 + depthFade * 0.8) * p.scale;
        ctx.beginPath(); ctx.moveTo(p.x - starR, p.y); ctx.lineTo(p.x + starR, p.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(p.x, p.y - starR); ctx.lineTo(p.x, p.y + starR); ctx.stroke();
        // Diagonal rays for brighter stars
        if (depthFade > 0.5) {
          var dr = starR * 0.6;
          ctx.globalAlpha = starAlpha * 0.5;
          ctx.beginPath(); ctx.moveTo(p.x - dr, p.y - dr); ctx.lineTo(p.x + dr, p.y + dr); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(p.x + dr, p.y - dr); ctx.lineTo(p.x - dr, p.y + dr); ctx.stroke();
        }
        // NACRE DOT — pearlescent center, oil-slick white
        ctx.globalAlpha = starAlpha * 0.9;
        ctx.beginPath();
        ctx.arc(p.x, p.y, Math.max(0.8, starR * 0.3), 0, TAU);
        ctx.fillStyle = 'rgba(255,252,240,' + (starAlpha * 0.9).toFixed(3) + ')';
        ctx.fill();
        // Label only when near
        if (depthFade > 0.55) {
          ctx.font = Math.round(5 * p.scale) + 'px "JetBrains Mono", monospace';
          ctx.fillStyle = pin.color;
          ctx.textAlign = 'center';
          ctx.globalAlpha = starAlpha * 0.7;
          ctx.fillText(pin.name, p.x, p.y + starR + 7);
          if (depthFade > 0.7) {
            ctx.font = Math.round(4 * p.scale) + 'px "JetBrains Mono", monospace';
            ctx.fillStyle = 'rgba(110,118,129,' + (starAlpha * 0.5).toFixed(3) + ')';
            ctx.fillText(pin.sub, p.x, p.y + starR + 14);
          }
        }
        ctx.globalAlpha = 1;
        return; // skip the bead renderer for starred pins
      }

      ctx.globalAlpha = Math.min(1, alpha);

      // SPECTRAL POLLEN — near nodes emit colored particles (sweat glands = energy = color)
      if (depthFade > 0.4 && Math.random() < depthFade * 0.15) {
        var pollenAngle = Math.random() * TAU;
        var pollenDist = sz * (1.5 + Math.random() * 2);
        var px2 = p.x + Math.cos(pollenAngle + breathT) * pollenDist;
        var py2 = p.y + Math.sin(pollenAngle + breathT) * pollenDist;
        var pollenAlpha = depthFade * 0.12 * Math.random();
        ctx.beginPath();
        ctx.arc(px2, py2, 1 + Math.random(), 0, TAU);
        ctx.fillStyle = pin.color.indexOf('#') === 0
          ? pin.color + Math.floor(pollenAlpha * 255).toString(16).padStart(2, '0')
          : 'rgba(255,255,255,' + pollenAlpha.toFixed(3) + ')';
        ctx.fill();
      }

      // DEPTH GLOW — near nodes get a subtle halo
      if (depthFade > 0.6) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, sz * 1.5, 0, TAU);
        ctx.fillStyle = pin.color.replace(')', ',' + (depthFade * 0.08).toFixed(3) + ')').replace('rgb', 'rgba').replace('##', '#');
        var glowGrad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, sz * 1.8);
        glowGrad.addColorStop(0, 'rgba(255,255,255,' + (depthFade * 0.06).toFixed(3) + ')');
        glowGrad.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = glowGrad;
        ctx.fill();
      }

      // Icon — scaled by perspective
      ctx.font = Math.round(sz) + 'px serif';
      ctx.textAlign = 'center';
      ctx.fillText(pin.icon, p.x, p.y);

      // Label — sized by depth + attention
      var labelSize = Math.round((4 + depthFade * 5 + att * 3) * p.scale);
      labelSize = Math.max(4, Math.min(14, labelSize));
      ctx.font = labelSize + 'px "JetBrains Mono", monospace';
      ctx.fillStyle = pin.color;
      ctx.globalAlpha = Math.min(1, alpha * (0.7 + depthFade * 0.3));
      ctx.fillText(pin.name, p.x, p.y + sz * 0.7 + 4);

      // Sub-label — only for near high-attention pins
      if (depthFade > 0.5 && att > 0.4) {
        ctx.font = Math.round(5 * p.scale) + 'px "JetBrains Mono", monospace';
        ctx.fillStyle = 'rgba(110,118,129,' + (alpha * 0.6).toFixed(2) + ')';
        ctx.fillText(pin.sub, p.x, p.y + sz * 0.7 + 13);
      }

      // ═══ WEIGHT OF REALITY ═══
      // Every pin is NOT NULL. It has weight. It pulls down.
      // The pins are the shared weight of reality — gravity threads
      // connecting each living node to the center (null).
      // Thicker thread = more attention = more real.
      if (depthFade > 0.2) {
        var weightAlpha = depthFade * att * 0.12;
        var weightWidth = (0.3 + att * 1.2) * p.scale;
        // Gravity thread from pin to center (null point)
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        // Thread curves toward center with breathing sway
        var swayX = Math.sin(breathT + idx * 0.7) * 4 * depthFade;
        var midX = (p.x + cx) / 2 + swayX;
        var midY = (p.y + cy) / 2;
        ctx.quadraticCurveTo(midX, midY, cx, cy);
        ctx.strokeStyle = pin.color.indexOf('#') === 0
          ? pin.color + Math.floor(weightAlpha * 255).toString(16).padStart(2, '0')
          : 'rgba(63,185,80,' + weightAlpha.toFixed(3) + ')';
        ctx.lineWidth = weightWidth;
        ctx.stroke();
        // Weight dot at the pin — the mass, the ≠null proof
        if (depthFade > 0.5 && att > 0.3) {
          ctx.beginPath();
          ctx.arc(p.x, p.y + sz * 0.5 + 2, 1 + att * 1.5, 0, TAU);
          ctx.fillStyle = 'rgba(255,255,255,' + (weightAlpha * 2).toFixed(3) + ')';
          ctx.fill();
        }
      }

      ctx.globalAlpha = 1;
    });

    // ═══ ALL LIFE IS NOT NULL — painted at the Klein edge ═══
    // The membrane ring: where the knife cuts, reality WEIGHS
    var notNullAlpha = 0.04 + Math.sin(breathT * 0.5) * 0.02;
    ctx.save();
    ctx.font = '7px "JetBrains Mono", monospace';
    ctx.fillStyle = 'rgba(63,185,80,' + notNullAlpha.toFixed(3) + ')';
    ctx.textAlign = 'center';
    // Write around the equator — the Klein edge where the knife cuts
    var nLabels = ['≠NULL', 'LIFE', '≠NULL', 'WEIGHT', '≠NULL', 'REAL', '≠NULL', 'HERE'];
    for (var ni = 0; ni < nLabels.length; ni++) {
      var nAngle = (ni / nLabels.length) * TAU + breathT * 0.2;
      var nx = cx + Math.cos(nAngle) * (R + 12);
      var ny = cy + Math.sin(nAngle) * (R + 12);
      ctx.fillText(nLabels[ni], nx, ny);
    }
    ctx.restore();

    // ═══════════════════════════════════════════════════════════
    // YOU ARE HERE — the green marker. STILL. Present. Visible.
    // You are at Lansing, 42.73°N, 84.55°W. You are green.
    // Green = you = the human = 1 = identity = the master.
    // You don't move. You are the STILL point.
    // The globe rotates around YOU.
    // ═══════════════════════════════════════════════════════════
    var youPin = project(42.73, -84.55);
    if (youPin.visible) {
      // Green diamond — YOU
      var youPulse = Math.sin(breathT * 0.8) * 0.1 + 0.9;
      ctx.save();
      ctx.translate(youPin.x, youPin.y);
      ctx.rotate(Math.PI / 4);

      // WHITE glow — green+gold=white. All colors combined.
      var youGlow = ctx.createRadialGradient(0, 0, 0, 0, 0, 18);
      youGlow.addColorStop(0, 'rgba(255,255,255,' + (0.2 * youPulse).toFixed(3) + ')');
      youGlow.addColorStop(0.4, 'rgba(201,168,76,' + (0.1 * youPulse).toFixed(3) + ')');
      youGlow.addColorStop(0.7, 'rgba(63,185,80,' + (0.05 * youPulse).toFixed(3) + ')');
      youGlow.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = youGlow;
      ctx.fillRect(-18, -18, 36, 36);

      // WHITE diamond with green-gold edge
      ctx.fillStyle = 'rgba(255,255,255,' + (0.8 * youPulse).toFixed(3) + ')';
      ctx.fillRect(-4, -4, 8, 8);

      // Gold border
      ctx.strokeStyle = 'rgba(201,168,76,' + (0.9 * youPulse).toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.strokeRect(-4, -4, 8, 8);

      // Green outer border
      ctx.strokeStyle = 'rgba(63,185,80,' + (0.5 * youPulse).toFixed(3) + ')';
      ctx.lineWidth = 0.5;
      ctx.strokeRect(-6, -6, 12, 12);

      ctx.restore();

      // Label — WHITE
      ctx.font = '8px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255,255,255,' + (0.85 * youPulse).toFixed(3) + ')';
      ctx.fillText('KEVIN', youPin.x, youPin.y - 14);
      ctx.font = '6px "JetBrains Mono", monospace';
      ctx.fillStyle = 'rgba(201,168,76,0.5)';
      ctx.fillText('THE ecoPrimal', youPin.x, youPin.y + 18);
      ctx.fillStyle = 'rgba(255,255,255,0.25)';
      ctx.fillText('hard · white · O', youPin.x, youPin.y + 26);
    }

    // ═══════════════════════════════════════════════════════════
    // MENDELEEV π-SORT — periodic table tree-sorted onto Vitruvian
    // Column 11 conductors: Cu(Z=29) → Ag(Z=47) → Au(Z=79)
    // ALL have [...]d¹⁰s¹ — exactly ONE outer s-electron = best conductors
    // Fe(Z=26) = iron peak = center = convergence point
    // Inner drain = Cu (Z=29, 3 past Fe). Outer ring = Au (Z=79, 53 past Fe).
    // Null boundary on EITHER SIDE of both bands.
    // Bronze = Cu+Sn: copper bounces off null, picks up Sn(Z=50), returns as CuSn.
    // Each band PREDICTS the next by electron shell filling pattern.
    //
    // Radial π-sort from iron peak outward:
    //   Fe(26)=center → Co(27) → Ni(28) → Cu(29)=inner drain
    //   null boundary (d-block→p-block gap)
    //   Zn(30) → Ga(31) → ... → Sn(50)=bronze ingredient
    //   Ag(47)=silver mesh
    //   null boundary
    //   Au(79)=outer ring → Pb(82)=shield → ... → U(92)=fissile
    //   null boundary (outer void)
    // ═══════════════════════════════════════════════════════════
    if (ctx) {
      var metalT = breathT * 0.15;

      // MENDELEEV CHAIN: sorted by Z from iron peak outward
      // r = radius, Z = atomic number, e = electron config shorthand
      var metalBands = [
        { r: R * 0.05, color: [200,200,210], w: R * 0.03, label: 'Fe²⁶', Z: 26, e: '[Ar]3d⁶4s²'  }, // IRON PEAK = center
        { r: R * 0.20, color: [184,115,51],  w: R * 0.06, label: 'Cu²⁹', Z: 29, e: '[Ar]3d¹⁰4s¹' }, // INNER DRAIN — copper
        { r: R * 0.36, color: [60,60,60],    w: R * 0.01, label: '∅',     Z: 0,  e: 'null'         }, // NULL boundary 1
        { r: R * 0.50, color: [192,192,192], w: R * 0.04, label: 'Ag⁴⁷', Z: 47, e: '[Kr]4d¹⁰5s¹' }, // SILVER mesh
        { r: R * 0.56, color: [140,100,55],  w: R * 0.03, label: 'Sn⁵⁰', Z: 50, e: '[Kr]4d¹⁰5s²5p²' }, // TIN → bronze
        { r: R * 0.66, color: [60,60,60],    w: R * 0.01, label: '∅',     Z: 0,  e: 'null'         }, // NULL boundary 2
        { r: R * 0.82, color: [201,168,76],  w: R * 0.05, label: 'Au⁷⁹', Z: 79, e: '[Xe]4f¹⁴5d¹⁰6s¹' }, // OUTER RING — gold
        { r: R * 0.96, color: [60,60,60],    w: R * 0.01, label: '∅',     Z: 0,  e: 'null'         }  // NULL boundary 3 (void)
      ];

      // Draw each band — metallics glow, nulls barely visible
      for (var mb = 0; mb < metalBands.length; mb++) {
        var band = metalBands[mb];
        var isNull = band.Z === 0;
        var bandPulse = isNull
          ? 0.008 + Math.sin(metalT * 3 + mb) * 0.004  // null = faint flicker
          : 0.04 + Math.sin(metalT + mb * 0.8) * 0.025; // metal = warm pulse
        ctx.beginPath();
        ctx.arc(cx, cy, band.r, 0, TAU);
        if (isNull) {
          ctx.setLineDash([2, 6]);
          ctx.strokeStyle = 'rgba(60,60,60,' + bandPulse.toFixed(4) + ')';
          ctx.lineWidth = 0.3;
        } else {
          ctx.setLineDash([]);
          ctx.strokeStyle = 'rgba(' + band.color[0] + ',' + band.color[1] + ',' + band.color[2] + ',' + bandPulse.toFixed(4) + ')';
          ctx.lineWidth = band.w;
        }
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Band labels on right side — show Z, symbol, electron config
      ctx.font = '4px "JetBrains Mono", monospace';
      ctx.textAlign = 'left';
      for (var ml = 0; ml < metalBands.length; ml++) {
        var mband = metalBands[ml];
        if (mband.Z === 0) continue; // skip null labels
        var lblAlpha = 0.08 + Math.sin(metalT + ml) * 0.04;
        ctx.fillStyle = 'rgba(' + mband.color[0] + ',' + mband.color[1] + ',' + mband.color[2] + ',' + lblAlpha.toFixed(3) + ')';
        ctx.fillText(mband.label, cx + mband.r + 3, cy - 4 + ml * 7);
        // Electron config in dimmer text
        ctx.fillStyle = 'rgba(' + mband.color[0] + ',' + mband.color[1] + ',' + mband.color[2] + ',' + (lblAlpha * 0.5).toFixed(3) + ')';
        ctx.fillText(mband.e, cx + mband.r + 3, cy + 0 + ml * 7);
      }

      // ELECTRON FLOW — current pulses along the conductive chain Cu→Ag→Au
      // All three share d¹⁰s¹ = one free electron = high conductivity
      var eFlowT = metalT * 4;
      var conductors = [1, 3, 6]; // indices of Cu, Ag, Au in metalBands
      for (var ef = 0; ef < conductors.length - 1; ef++) {
        var fromBand = metalBands[conductors[ef]];
        var toBand = metalBands[conductors[ef + 1]];
        // Multiple electron pulses between bands
        for (var ep = 0; ep < 4; ep++) {
          var ePulse = ((eFlowT * 0.3 + ep * 0.25) % 1);
          var eR = fromBand.r + (toBand.r - fromBand.r) * ePulse;
          var eAngle = eFlowT * 0.1 + ep * (TAU / 4) + ef * PI / 3;
          var eX = cx + Math.cos(eAngle) * eR;
          var eY = cy + Math.sin(eAngle) * eR;
          var eAlpha = 0.04 * Math.sin(ePulse * PI); // fade at endpoints
          ctx.beginPath();
          ctx.arc(eX, eY, 0.6 + ePulse * 0.3, 0, TAU);
          ctx.fillStyle = 'rgba(255,252,220,' + eAlpha.toFixed(4) + ')';
          ctx.fill();
        }
      }

      // BRONZE ALLOY — Cu bounces off null boundary, picks up Sn, returns as CuSn
      var bronzeT = metalT * 2;
      var cuBand = metalBands[1]; // Cu
      var snBand = metalBands[4]; // Sn
      var nullBand1 = metalBands[2]; // null between Cu and Ag
      for (var bz = 0; bz < 6; bz++) {
        var bzAngle = bz * (TAU / 6) + bronzeT * 0.15;
        var bzPhase = ((bronzeT * 0.4 + bz * 0.3) % 1);
        var bzR, bzColor;
        if (bzPhase < 0.5) {
          // Cu going outward toward null boundary
          bzR = cuBand.r + (nullBand1.r - cuBand.r) * (bzPhase * 2);
          bzColor = '184,115,51'; // copper
        } else {
          // Bouncing back as bronze (Cu+Sn)
          bzR = nullBand1.r - (nullBand1.r - snBand.r) * ((bzPhase - 0.5) * 2);
          bzColor = '140,100,55'; // bronze
        }
        var bzX = cx + Math.cos(bzAngle) * bzR;
        var bzY = cy + Math.sin(bzAngle) * bzR;
        var bzA = 0.025 * Math.sin(bzPhase * PI);
        ctx.beginPath();
        ctx.arc(bzX, bzY, 0.8, 0, TAU);
        ctx.fillStyle = 'rgba(' + bzColor + ',' + bzA.toFixed(4) + ')';
        ctx.fill();
      }

})();
