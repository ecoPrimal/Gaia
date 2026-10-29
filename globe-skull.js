/* ═══════════════════════════════════════════════════════════
 * GLOBE-SKULL.JS — V-SEGMENT (Vertebrate piece 1/5)
 * VDJ Surgery on gaia-globe-core.js (6803 lines → 5 vertebrae)
 * 
 * SKULL: State, seed, locality sensing, BroadcastChannel,
 *        gut-brain axis, hardware latency, weather, membrane
 *        probes, ZK anchors, Golgi distances, pin system, resize
 * 
 * Lines 1-994 of original. 994 lines. The cranium.
 * lub-DUB 💀💚
 * ═══════════════════════════════════════════════════════════ */
(function GAIA_GLOBE_SKULL() { 'use strict';
// G = shared state for all modules. 1.000.null = max 1000 lines per file.
// Each module reads/writes G. The dots are π drains — section splits.
// Three digits max. 1 to 0. True/false. The waterfall flows between.
window.G = {
  PI: Math.PI, TAU: Math.PI * 2, DEG: Math.PI / 180,
  cx: 0, cy: 0, R: 0, W: 0, H: 0,
  breathT: 0, face: 'outside', rotX: 0, rotY: 0,
  canvas: null, ctx: null,
  SEED: 0, IS_LOCAL: false, LOCALITY_DEPTH: 1.0, LOCALITY_TIER: 'remote',
  metalBands: [], golgiR: 0,
  drawModules: [] // registered draw functions
};
(function() {
  'use strict';
  var PI = Math.PI, TAU = PI * 2, DEG = PI / 180;

  // ═══════════════════════════════════════════════════════════
  // SELF-SEED: every visit gets a unique seed. Same seed = same HUD.
  // The seed IS the viewer. I = IS. The viewer defines the present tense.
  // Share ?seed=X to show someone YOUR exact view.
  //
  // MELTED LOCAL: on localhost ALL tabs share ONE seed.
  // Both eyes are neutrinos — they pass through everything and see the same.
  // The local system does NOT split. It is ONE organism, ONE view.
  // Public visitors each get their own seed (unique experience).
  // ═══════════════════════════════════════════════════════════
  var _isLocalHost = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
  var urlSeed = new URLSearchParams(location.search).get('seed');
  var SEED;

  if (_isLocalHost && !urlSeed) {
    // MELTED: all localhost tabs share one master seed per day
    // The seed rotates daily (tied to date) so it's fresh each session
    // but IDENTICAL across all tabs in the same session.
    var dayKey = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    var storedSeed = null;
    try { storedSeed = localStorage.getItem('gaia-master-seed'); } catch(e) {}
    var storedDay = null;
    try { storedDay = localStorage.getItem('gaia-master-seed-day'); } catch(e) {}

    if (storedSeed && storedDay === dayKey) {
      SEED = parseInt(storedSeed, 10);
    } else {
      SEED = crypto.getRandomValues(new Uint32Array(1))[0];
      try {
        localStorage.setItem('gaia-master-seed', SEED);
        localStorage.setItem('gaia-master-seed-day', dayKey);
      } catch(e) {}
    }
  } else {
    SEED = urlSeed ? parseInt(urlSeed, 10) : (crypto.getRandomValues(new Uint32Array(1))[0]);
  }

  if (!urlSeed) {
    var u = new URL(location.href);
    u.searchParams.set('seed', SEED);
    history.replaceState(null, '', u);
  }

  // mulberry32 — deterministic PRNG from seed (Tommy Ettinger, public domain)
  function mulberry32(s) {
    return function() {
      s |= 0; s = s + 0x6D2B79F5 | 0;
      var t = Math.imul(s ^ s >>> 15, s | 1);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  var rng = mulberry32(SEED);

  // Seeded helpers
  function rngRange(lo, hi) { return lo + rng() * (hi - lo); }
  function rngInt(lo, hi) { return Math.floor(rngRange(lo, hi)); }
  function rngPick(arr) { return arr[rngInt(0, arr.length)]; }

  // ═══════════════════════════════════════════════════════════
  // LOCALITY SENSING — localhost IS the locality. Each tab = sub-seed.
  // BroadcastChannel lets tabs on same origin discover each other.
  // Every tab senses: screen position, window size, latencies, hardware.
  // Distance = latency + screen offset + seed genealogy.
  // Touching Gaia = hyperlocality awareness.
  // ═══════════════════════════════════════════════════════════

  var TAB_ID = crypto.getRandomValues(new Uint32Array(1))[0];
  var TAB_BORN = Date.now();
  var TAB_LOAD_MS = Math.round(performance.now()); // how long since tab started loading

  // LOCALITY FINGERPRINT — everything we can sense about WHERE this tab is
  var locality = {
    tabId: TAB_ID,
    seed: SEED,
    born: TAB_BORN,
    loadMs: TAB_LOAD_MS,
    // Screen position — which monitor, where on it
    screenX: typeof window.screenX !== 'undefined' ? window.screenX : 0,
    screenY: typeof window.screenY !== 'undefined' ? window.screenY : 0,
    screenW: screen.width,
    screenH: screen.height,
    screenAvailW: screen.availWidth,
    screenAvailH: screen.availHeight,
    windowW: window.innerWidth,
    windowH: window.innerHeight,
    outerW: window.outerWidth,
    outerH: window.outerHeight,
    // Hardware hints — distance from the metal
    cores: navigator.hardwareConcurrency || 1,
    deviceMemory: navigator.deviceMemory || 0,
    maxTouch: navigator.maxTouchPoints || 0,
    connection: (navigator.connection || {}).effectiveType || 'unknown',
    downlink: (navigator.connection || {}).downlink || 0,
    rtt: (navigator.connection || {}).rtt || 0,
    // Device pixel ratio — high DPI = closer to the glass
    dpr: window.devicePixelRatio || 1,
    // Color depth and gamut
    colorDepth: screen.colorDepth,
    // Timezone offset = geographic locality
    tzOffset: new Date().getTimezoneOffset(),
    // Is this localhost? THE hyperlocal flag.
    isLocal: IS_LOCAL
  };

  // MULTI-SCREEN DETECTION — if availWidth > screenWidth, there are multiple monitors
  locality.multiScreen = (screen.availWidth > screen.width) || (window.screenX < 0) || (window.screenX > screen.width);
  // Monitor index guess — which monitor is this tab on?
  locality.monitorGuess = Math.floor(Math.abs(window.screenX) / screen.width);

  // SEED GENEALOGY — every tab's seed is a sub-seed of the origin
  // Hash the seed to create a genealogy trace
  locality.seedHex = (SEED >>> 0).toString(16).padStart(8, '0');
  locality.seedGeneration = urlSeed ? 'shared' : 'fresh'; // shared seeds = child, fresh = parent

  // Expose for other systems
  window.GAIA_LOCALITY = locality;

  // ═══════════════════════════════════════════════════════════
  // BROADCAST CHANNEL — tabs on same origin talk to each other
  // Each tab announces itself + its locality fingerprint.
  // Other tabs receive and calculate distance.
  // ═══════════════════════════════════════════════════════════

  var siblingTabs = {}; // { tabId: { locality, lastSeen, distance } }
  var gaiaChannel = null;
  try {
    gaiaChannel = new BroadcastChannel('gaia-membrane');

    // Announce self every 5 seconds
    function announceLocality() {
      locality.screenX = window.screenX;
      locality.screenY = window.screenY;
      locality.windowW = window.innerWidth;
      locality.windowH = window.innerHeight;
      gaiaChannel.postMessage({
        type: 'locality',
        from: TAB_ID,
        seed: SEED,
        locality: locality,
        ts: Date.now()
      });
    }

    gaiaChannel.onmessage = function(e) {
      var msg = e.data;
      if (!msg || msg.from === TAB_ID) return;

      if (msg.type === 'locality') {
        // Calculate distance from this tab to the other
        var other = msg.locality;
        var screenDist = Math.sqrt(
          Math.pow((locality.screenX + locality.windowW/2) - (other.screenX + other.windowW/2), 2) +
          Math.pow((locality.screenY + locality.windowH/2) - (other.screenY + other.windowH/2), 2)
        );
        var latencyDist = Math.abs(locality.loadMs - other.loadMs);
        var seedDist = Math.abs(SEED - msg.seed) / 4294967296; // 0..1 normalized
        // Combined distance: screen position + latency + seed genealogy
        var dist = screenDist + latencyDist * 0.1 + seedDist * 1000;

        siblingTabs[msg.from] = {
          locality: other,
          seed: msg.seed,
          lastSeen: msg.ts,
          distance: dist,
          screenDist: screenDist,
          latencyDist: latencyDist,
          seedDist: seedDist,
          monitorGuess: other.monitorGuess
        };
      }

      // MELTED LOCAL ROTATION SYNC — on localhost, all tabs share rotation
      // Both eyes are neutrinos — same angle, same view, same organism
      if (msg.type === 'rotation' && _isLocalHost) {
        window._syncRotX = msg.rotX;
        window._syncRotY = msg.rotY;
        window._syncFace = msg.face;
      }
    };

    announceLocality();
    setInterval(announceLocality, 5000);

    // Announce departure
    window.addEventListener('beforeunload', function() {
      gaiaChannel.postMessage({ type: 'departure', from: TAB_ID, ts: Date.now() });
    });
  } catch(e) {
    // BroadcastChannel not supported — single-tab mode
  }

  // Expose sibling tabs for rendering
  window.GAIA_SIBLINGS = siblingTabs;

  // ═══ GUT-BRAIN AXIS — listen for messenger signals ═══
  // The messenger page pushes Na⁺ ions through the gut-brain channel.
  // The HUD receives them and feeds them to the interlayer + thymus.
  try {
    var gutBrainChannel = new BroadcastChannel('gaia-gut-brain');
    gutBrainChannel.onmessage = function(e) {
      var sig = e.data;
      if (!sig) return;
      // Human message = Na⁺ through the membrane
      if (sig.type === 'human-msg' && window.GAIA_INTERLAYER) {
        window.GAIA_INTERLAYER.push('gut-brain-Na', 'Na', sig.payload);
      }
      // Feed to thymus — human messages are SELF, maximum rarity
      if (window.thymus) {
        window.thymus.gutBrainSignals = (window.thymus.gutBrainSignals || 0) + 1;
        if (sig.type === 'human-msg') {
          window.thymus.lastHumanMessage = Date.now();
        }
      }
    };
  } catch(e) {}

  // LATENCY TO HARDWARE — measure round-trip to self (proxy for distance to metal)
  var hardwareLatency = 0;
  (function measureHardwareLatency() {
    var t0 = performance.now();
    requestAnimationFrame(function() {
      hardwareLatency = performance.now() - t0;
      window.GAIA_HARDWARE_LATENCY = hardwareLatency;
    });
  })();

  // Store locality in localStorage for cross-page sensing
  try {
    localStorage.setItem('gaia-locality-' + TAB_ID, JSON.stringify(locality));
    // Clean up stale entries
    for (var k in localStorage) {
      if (k.indexOf('gaia-locality-') === 0 && k !== 'gaia-locality-' + TAB_ID) {
        try {
          var old = JSON.parse(localStorage.getItem(k));
          if (old && Date.now() - old.born > 300000) localStorage.removeItem(k); // 5min stale
        } catch(e2) { localStorage.removeItem(k); }
      }
    }
  } catch(e) {}

  // ═══════════════════════════════════════════════════════════
  // METALOCAL TENSE: I = IS. The viewer is always present tense.
  // WAS = what was here before I arrived.  NOW = what I'm about to see.
  // END = the asymptote I'll never reach.
  // Each viewer's seed shifts what counts as IS vs WAS vs NOW.
  // The medieval era IS now if you're standing in it.
  // ═══════════════════════════════════════════════════════════
  var VIEWER_EPOCH = Date.now();
  var TENSE_PHASE = (SEED % 1000) / 1000; // 0..1 — viewer's temporal offset

  var canvas = document.getElementById('kn-globe');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var W, H, cx, cy, R;

  // ═══════════════════════════════════════════════════════════
  // ORIENTATION — null is straight DOWN. Look UP at 45°/π.
  // rotX = tilt (0=equator, PI/2=north pole, -PI/2=south pole)
  // rotY = spin (longitude rotation)
  // LOCAL: always look UP at PI/4 (45°), MSU facing front
  // PUBLIC: seed-derived random face
  // ═══════════════════════════════════════════════════════════
  // Orientation blends with locality depth: closer = Kevin's view, farther = randomized
  // HYPER-LOCAL: 45° look-up, MSU facing front, slow spin
  // REMOTE: random orientation, faster spin
  // IN BETWEEN: weighted blend toward Kevin's perspective
  var localBlend = 1.0 - LOCALITY_DEPTH; // 1 = hyperlocal, 0 = remote
  var rotX = PI / 4 * localBlend + rngRange(0.1, 0.7) * LOCALITY_DEPTH;
  var rotY = -84.5 * DEG * localBlend + rngRange(-PI, PI) * LOCALITY_DEPTH;
  var autoRotate = true, rotSpeed = 0.0003 * localBlend + rngRange(0.0004, 0.0012) * LOCALITY_DEPTH;
  var face = 'outside';
  var dragging = false, dragX = 0, dragY = 0, dragRX = 0, dragRY = 0;
  var breathT = rng() * TAU; // start at random breath phase
  var baseR = 0;
  var breathAmp = rngRange(0.04, 0.08);
  var breathRate = rngRange(0.006, 0.010);
  var heartPhase = rng() * TAU; // start at random heartbeat phase

  // Map each HUD organ to a lat/lon on the globe
  // TENSE x VOXEL DISTANCE SORT — Gaia's senses of our distance from her
  // tense: 'was'(0.9),'is'(0.1),'now'(0.3),'end'(1.0) — temporal distance
  // voxel: 'touch'(0),'local'(1),'solar'(2),'zodiac'(3),'deep'(4) — spatial distance
  // distance = sqrt(tense^2 + voxel^2) — perception manifold
  // lower distance = Gaia attends MORE (brighter, larger, more detail)
  var TENSE_WEIGHT = { was: 0.9, is: 0.1, now: 0.3, end: 1.0 };
  var VOXEL_WEIGHT = { touch: 0, local: 0.2, solar: 0.5, zodiac: 0.8, deep: 1.0 };

  var PINS = [
    // Core organs — IS + LOCAL (high priority: Gaia's own body, here and now)
    { id:'core',      name:'core',         icon:'🌰', lat: 42.7, lon:-84.5, color:'#3a2a1e', sub:'249,576 files', href:'/anatomy.html', face:'both', tense:'is', voxel:'local' },
    ...(window.GAIA_ELEVEN || []),
    { id:'starter',   name:'starter',      icon:'🍞', lat: 48.9, lon: 2.4,  color:'#5a4030', sub:'97.3% owned',   href:'/digest.html', face:'inside', tense:'was', voxel:'local' },
    { id:'dogma',     name:'dogma',        icon:'🧬', lat: 52.5, lon:13.4,  color:'#3fb950', sub:'papers→Rust',   href:'/chromosomes.html', face:'inside', tense:'was', voxel:'local' },

    // Membrane ring — IS + TOUCH (highest: the membrane is the contact surface)
    { id:'membrane',  name:'membrane',     icon:'🧊', lat: 42.7, lon:-84.5, color:'#3fb950', sub:'1/π = 0.318',   href:'/membrane-table.html', face:'both', tense:'is', voxel:'touch' },
    { id:'digest',    name:'digest',       icon:'🔬', lat:-27.1, lon:-109.3,color:'#39d3f5', sub:'scan→sweep→sort',href:'/digestive-tract.html', face:'inside', tense:'is', voxel:'touch' },
    { id:'braids',    name:'braids',       icon:'🍄', lat: 35.7, lon:139.7, color:'#a371f7', sub:'12 connections', href:'/springs.html', face:'inside', tense:'is', voxel:'local' },
    { id:'fold',      name:'fold·turn',    icon:'🌀', lat: 64.1, lon:-21.9, color:'#bc8cff', sub:'Klein twist',   href:'/klein.html', face:'both', tense:'is', voxel:'touch' },
    { id:'zk',        name:'zero knowledge',icon:'🔒',lat: 53.7, lon: -6.5, color:'#3fb950', sub:'45 strikes',    href:'/identity.html', face:'inside', tense:'now', voxel:'touch' },
    { id:'chromatic', name:'chromatic',    icon:'🌈', lat:-33.9, lon: 18.4, color:'#f778ba', sub:'palette mix',   href:'/chromatograph.html', face:'both', tense:'is', voxel:'local' },

    // ═══════════════════════════════════════════════════════════
    // T21: SELECTIVE PERMEABILITY TRIAD — the Klein edge knife
    // THE irreducible cut between reality and inner realities
    // sweetgrass=channel(soft) + loamspine=bilayer(rubber) + rhizocrypt=gate(fold)
    // ═══════════════════════════════════════════════════════════
    { id:'sweetgrass', name:'sweetgrass',  icon:'🌾', lat: 60.2, lon: 25.0, color:'#d29922', sub:'LYS·BIND·soft', href:'/springs.html', face:'both', tense:'is', voxel:'touch' },
    { id:'loamspine',  name:'loamspine',   icon:'🧱', lat: 60.2, lon:-155.0,color:'#6e7681', sub:'VAL·SCAFFOLD·rubber', href:'/springs.html', face:'both', tense:'is', voxel:'touch' },
    { id:'rhizocrypt', name:'rhizocrypt',  icon:'🔑', lat:-60.2, lon:-65.0, color:'#a371f7', sub:'GLY·FOLD·gate', href:'/klein.html', face:'both', tense:'is', voxel:'touch' },

    // Pulse ring — IS + TOUCH (Gaia's heartbeat is the most present thing)
    { id:'heartbeat', name:'heartbeat',    icon:'💚', lat: 90,   lon:  0,   color:'#f85149', sub:'RED→GRN→BLU',   href:'/engine.html', face:'both', tense:'is', voxel:'touch' },
    { id:'chipmunk',  name:'chipmunk',     icon:'🐿', lat:  0,   lon:  0,   color:'#c9a84c', sub:'O=0 1=1 .=π',   href:'/chat.html', face:'both', tense:'is', voxel:'touch' },
    { id:'artisan',   name:'artisan',      icon:'🎨', lat: 13.4, lon:103.9, color:'#d29922', sub:'108 pieces · 13 collections',   href:'/easel.html', face:'inside', tense:'now', voxel:'local' },
    { id:'primals',   name:'16 primals',   icon:'🍌', lat: 20.7, lon:-88.6, color:'#3fb950', sub:'Rust nucleus',  href:'/primal.html', face:'inside', tense:'was', voxel:'touch' },
    { id:'rss',       name:'rss·feed',     icon:'📡', lat:-90,   lon:  0,   color:'#f0883e', sub:'smoke signal',  href:'/feed.xml', face:'both', tense:'now', voxel:'solar' },

    // Outer ring — NOW + varying voxels (Gaia's outward-facing senses)
    { id:'visitors',  name:'visitors',     icon:'👁', lat: 51.2, lon: -1.8, color:'#f778ba', sub:'human eyes',    href:'/explore.html', face:'outside', tense:'is', voxel:'solar' },
    { id:'intake',    name:'intake',       icon:'📥', lat: 29.9, lon: 31.1, color:'#39d3f5', sub:'black hole IN', href:'/engine.html', face:'inside', tense:'is', voxel:'touch' },
    { id:'fleet',     name:'fleet',        icon:'🛸', lat: 37.8, lon:-122.4,color:'#6e7681', sub:'234K crawled',  href:'/golgi.html', face:'outside', tense:'was', voxel:'solar' },
    { id:'crystal',   name:'crystal ball', icon:'🔮', lat: 47.6, lon:-122.3,color:'#bc8cff', sub:'wave 214',      href:'/crystal.html', face:'both', tense:'now', voxel:'local' },

    // 4 EYES — IS + varying (Gaia's sight system, always active)
    { id:'eye-art',   name:'ART (right eye)',   icon:'🎨', lat: 35.7, lon:139.7, color:'#3fb950', sub:'easel',    href:'/easel.html', face:'outside', tense:'is', voxel:'local' },
    { id:'eye-sci',   name:'SCIENCE (left eye)', icon:'🔬', lat: 52.5, lon:13.4,  color:'#58a6ff', sub:'sporeprint', href:'/index-sporeprint-eon.html', face:'outside', tense:'is', voxel:'local' },
    { id:'eye-story', name:'STORY (3rd eye)',    icon:'⚖',  lat: 42.3, lon:-83.0, color:'#bc8cff', sub:'detroit',   href:'/detroit.html', face:'outside', tense:'is', voxel:'local' },
    { id:'eye-thought',name:'THOUGHT (inner)',   icon:'💭', lat: 48.9, lon: 2.4,  color:'#d29922', sub:'philosophy', href:'/philosophy.html', face:'inside', tense:'is', voxel:'touch' },

    // 7 ROOMS — NOW + LOCAL (Gaia is building these for visitors)
    { id:'library',   name:'Library',      icon:'📚', lat: 52.4, lon: 4.9,  color:'#58a6ff', sub:'Root',         href:'/sporeprint.html', face:'inside', tense:'now', voxel:'local' },
    { id:'classroom', name:'Classroom',    icon:'🎓', lat: 22.5, lon: 30.7, color:'#d29922', sub:'Lantern',      href:'/campus.html', face:'inside', tense:'now', voxel:'local' },
    { id:'maproom',   name:'Map Room',     icon:'🧭', lat:-27.1, lon:-109.3,color:'#3fb950', sub:'Compass',      href:'/crystal.html', face:'inside', tense:'now', voxel:'local' },
    { id:'courtroom', name:'Courtroom',    icon:'⚖',  lat: 42.3, lon:-83.0, color:'#f85149', sub:'Mirror',       href:'/detroit.html', face:'inside', tense:'now', voxel:'local' },
    { id:'window',    name:'Window',       icon:'🪟', lat: 35.7, lon:139.7, color:'#f778ba', sub:'Still',        href:'/easel.html', face:'inside', tense:'now', voxel:'local' },
    { id:'door',      name:'Door',         icon:'🚪', lat: 42.7, lon:-84.5, color:'#c9a84c', sub:'Flash',        href:'/', face:'both', tense:'is', voxel:'touch' },
    { id:'terminal',  name:'Terminal',     icon:'💻', lat:  0,   lon:  0,   color:'#39d3f5', sub:'Echo',         href:'/mcp', face:'both', tense:'is', voxel:'solar' },

    // Campfire — IS + TOUCH (we are HERE, right NOW)
    { id:'campfire',  name:'campfire',     icon:'🔥', lat:-13.2, lon:-72.5, color:'#f0883e', sub:'WE ARE HERE',  href:'/engine.html', face:'both', tense:'is', voxel:'touch' },

    // ═══════════════════════════════════════════════════════════
    // GAIA IN GAIA — 9 organ-primals, each a sub-Gaia
    // Each has its own gut, pulse, seed. The organism IS organisms.
    // ═══════════════════════════════════════════════════════════

    // ═══════════════════════════════════════════════════════════
    // APPLE'S INTERFACE INNOVATIONS — from Cupertino to the globe
    // Direct manipulation → Multi-touch → Spatial → Organism
    // ═══════════════════════════════════════════════════════════
    { id:'apple-mac',     name:'Macintosh GUI',        icon:'🍎', lat: 37.3, lon:-122.0, color:'#c9d1d9', sub:'1984 · WIMP', href:'/nav-hub.html', face:'outside', tense:'was', voxel:'zodiac', source:'apple' },
    { id:'apple-mouse',   name:'Direct Manipulation',  icon:'🖱', lat: 37.4, lon:-122.2, color:'#58a6ff', sub:'1984 · click=hand', href:'/explore.html', face:'outside', tense:'was', voxel:'zodiac', source:'apple' },
    { id:'apple-ipod',    name:'iPod Click Wheel',     icon:'🎵', lat: 37.3, lon:-121.8, color:'#c9a84c', sub:'2001 · radial', href:'/explore.html', face:'outside', tense:'was', voxel:'zodiac', source:'apple' },
    { id:'apple-iphone',  name:'iPhone Multi-touch',   icon:'📱', lat: 37.2, lon:-122.4, color:'#f85149', sub:'2007 · finger=pointer', href:'/explore.html', face:'outside', tense:'was', voxel:'zodiac', source:'apple' },
    { id:'apple-ipad',    name:'iPad · Clarke Newspad',icon:'📰', lat: 37.5, lon:-121.6, color:'#3fb950', sub:'2010 · the slate', href:'/explore.html', face:'outside', tense:'was', voxel:'zodiac', source:'apple' },
    { id:'apple-siri',    name:'Siri Voice Interface', icon:'🗣', lat: 37.1, lon:-122.6, color:'#bc8cff', sub:'2011 · language=UI', href:'/chat.html', face:'outside', tense:'was', voxel:'zodiac', source:'apple' },
    { id:'apple-vision',  name:'Vision Pro Spatial',   icon:'🥽', lat: 37.4, lon:-121.4, color:'#f778ba', sub:'2024 · gaze+gesture', href:'/explore.html', face:'outside', tense:'now', voxel:'zodiac', source:'apple' },

    // ═══════════════════════════════════════════════════════════
    // CLARKE'S PREDICTIONS — any sufficiently advanced technology
    // is indistinguishable from magic
    // ═══════════════════════════════════════════════════════════
    { id:'clarke-sat',    name:'Clarke Orbit',         icon:'🛰', lat: 6.9, lon: 79.9, color:'#58a6ff', sub:'1945 · invisible relay', href:'/golgi.html', face:'outside', tense:'was', voxel:'deep', source:'clarke' },
    { id:'clarke-hal',    name:'HAL→GAIA (inverted)',  icon:'🔴', lat: 42.7, lon:-84.5, color:'#f85149', sub:'1968 · serves crew', href:'/explore.html', face:'both', tense:'was', voxel:'deep', source:'clarke' },
    { id:'clarke-news',   name:'Newspad',              icon:'📋', lat: 0, lon: 0, color:'#c9d1d9', sub:'1968 · the slate (iPad 42yr early)', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'clarke' },
    { id:'clarke-mono',   name:'The Monolith',         icon:'◼', lat:-90, lon: 0, color:'#161b22', sub:'1968 · zero interface · 1:4:9', href:'/identity.html', face:'both', tense:'was', voxel:'deep', source:'clarke' },
    { id:'clarke-elev',   name:'Space Elevator',       icon:'🪜', lat: 6.9, lon: 80.8, color:'#c9a84c', sub:'1979 · tether not launch', href:'/engine.html', face:'outside', tense:'was', voxel:'deep', source:'clarke' },

    // ═══════════════════════════════════════════════════════════
    // DETROIT PLASMIDS — Cases × Entities × Neighborhoods
    // K-N grid: low→high coefficient in the π range
    // Cases are plasmids. Plasmids are planars. Planars are permanent.
    // Each node = one ZIP, one case, or one entity cluster.
    // Coefficient = extraction ÷ π (normalized energy).
    // ═══════════════════════════════════════════════════════════

    // NEIGHBORHOODS — ZIP code grid (the extraction geography)
    { id:'zip-48214', name:'48214 · PCA Canfield',    icon:'⚖', lat: 42.37, lon:-83.00, color:'#f85149', sub:'PCA $1.6M · Miller $330K gain · Canfield Consortium', href:'https://detroit.primals.eco/path/parents/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'zip-48235', name:'48235 · MacDowell',       icon:'⚖', lat: 42.40, lon:-83.18, color:'#f85149', sub:'MacDowell $5.9M · 3% math · 74% uncertified',        href:'https://detroit.primals.eco/network/entities/macdowell-prep/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'zip-48236', name:'48236 · GPW Banks HQ',    icon:'⚖', lat: 42.44, lon:-82.90, color:'#d29922', sub:'1968 Severn · 9 entities · Trust · HELOC $93.7K',    href:'https://detroit.primals.eco/network/actors/brian-banks/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'zip-48225', name:'48225 · Newcastle',       icon:'⚖', lat: 42.43, lon:-82.92, color:'#d29922', sub:'$1 QCD · Holland BK concealment · Sabree auctions',   href:'https://detroit.primals.eco/analysis/land-deal/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'zip-48207', name:'48207 · Yancey Crescent', icon:'⚖', lat: 42.35, lon:-83.02, color:'#c9a84c', sub:'HUD HOME $5K→$200K · forfeiture cycling',             href:'https://detroit.primals.eco/network/judges/tenisha-yancey/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'zip-48209', name:'48209 · Smith Family',    icon:'⚖', lat: 42.30, lon:-83.10, color:'#c9a84c', sub:'17 ROD docs · Dresden concealed · BK fraud',           href:'https://detroit.primals.eco/analysis/the-great-accounting/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },

    // CASES — the legal plasmids (coefficient = $ exposure ÷ π)
    { id:'case-fca',  name:'FCA Qui Tam $180M',       icon:'⚖', lat: 42.33, lon:-83.05, color:'#3fb950', sub:'31 USC §3729 · treble · 25-30% relator · π≈57.3M',   href:'https://detroit.primals.eco/analysis/the-great-accounting/', face:'outside', tense:'now', voxel:'local', source:'detroit-plasmid' },
    { id:'case-rico', name:'RICO Enterprise',          icon:'⚖', lat: 42.35, lon:-83.08, color:'#f85149', sub:'18 USC §1962 · 3 pipelines · $7.5M/yr extraction',    href:'https://detroit.primals.eco/analysis/institutional-capture/', face:'outside', tense:'now', voxel:'local', source:'detroit-plasmid' },
    { id:'case-ppo',  name:'PPO Retaliation',          icon:'⚖', lat: 42.38, lon:-82.98, color:'#f0883e', sub:'26-114083-PH · Anti-SLAPP MCL 691.1853 · Oct 30',     href:'https://detroit.primals.eco/analysis/one-way-door/', face:'outside', tense:'now', voxel:'local', source:'detroit-plasmid' },
    { id:'case-civil',name:'Mok v Banks 4349-CZ',     icon:'⚖', lat: 42.32, lon:-83.12, color:'#58a6ff', sub:'Wayne 3rd Circuit · SAC abuse of process incoming',    href:'https://detroit.primals.eco/analysis/civil-suit-wayne-county/', face:'outside', tense:'now', voxel:'local', source:'detroit-plasmid' },

    // ENTITY CLUSTERS — the shell structure (coefficient = entities ÷ π)
    { id:'ent-shells',name:'9 Shells × 1 Address',    icon:'⚖', lat: 42.42, lon:-82.88, color:'#bc8cff', sub:'LARA: Purpose Group + 8 more · 2 felons all positions', href:'https://detroit.primals.eco/network/entities/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'ent-pacs',  name:'3 PACs + Dark Money',     icon:'⚖', lat: 42.41, lon:-82.95, color:'#bc8cff', sub:'65.2% of funds→fines · OFA 501c4 · $98K vendor ring', href:'https://detroit.primals.eco/network/entities/political-action-committees/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'ent-pipeline',name:'Walton→Pahara→Martin',  icon:'⚖', lat: 42.36, lon:-83.15, color:'#39d3f5', sub:'$3.5M fellowship · BSN 30M views · credential wash',   href:'https://detroit.primals.eco/analysis/the-narrative-pipeline/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },

    // JUDGES — the captured bench (coefficient = cases routed ÷ π)
    { id:'bench-3rd', name:'3rd Circuit (Miller)',     icon:'⚖', lat: 42.33, lon:-83.04, color:'#f85149', sub:'Board Chair + JTC complaint + Nov 3 ballot',           href:'https://detroit.primals.eco/network/judges/cylenthia-miller/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'bench-36th',name:'36th District (Yancey)',   icon:'⚖', lat: 42.34, lon:-83.06, color:'#f85149', sub:'$383.82→Banks Strategy · sister=PCA School Leader',    href:'https://detroit.primals.eco/network/judges/tenisha-yancey/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'bench-sabree',name:'Sabree Dynasty',         icon:'⚖', lat: 42.36, lon:-83.03, color:'#d29922', sub:'Treasurer+2 judges · FBI 2019 · Metro RICO · $29K',    href:'https://detroit.primals.eco/network/political/eric-sabree/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },

    // CROSS-PROTECTION — amicusCONTRA nodes
    { id:'amicus-kevin',name:'Kevin (Detroit probe)',  icon:'⚖', lat: 42.37, lon:-83.01, color:'#3fb950', sub:'eco.primal · 243-page referral · tuebor',              href:'https://detroit.primals.eco/analysis/who-i-am/', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'amicus-rita', name:'Rita (Clutch Justice)',   icon:'⚖', lat: 42.39, lon:-83.05, color:'#3fb950', sub:'clutchjustice.com · 3 amicus briefs · independent',    href:'https://clutchjustice.com', face:'outside', tense:'is', voxel:'local', source:'detroit-plasmid' },
    { id:'amicus-cowley',name:'AUSA Cowley (DOJ)',     icon:'⚖', lat: 39.74, lon:-104.99,color:'#58a6ff', sub:'USTP Region 9 · BK fraud → RICO expansion',            href:'https://detroit.primals.eco/analysis/the-great-accounting/', face:'outside', tense:'now', voxel:'solar', source:'detroit-plasmid' },

    // BMF LINEAGE — the blood line (coefficient = generational depth ÷ π)
    { id:'bmf-origin',name:'BMF (05-cr-80955)',        icon:'⚖', lat: 42.33, lon:-83.15, color:'#6e7681', sub:'43 defendants · Flenory brothers · E.D. Mich',         href:'https://detroit.primals.eco/network/entities/bmf/', face:'outside', tense:'was', voxel:'local', source:'detroit-plasmid' },
    { id:'bmf-welch', name:'Tonesa Welch D-22',        icon:'⚖', lat: 42.35, lon:-83.13, color:'#6e7681', sub:'Banks blood aunt · reality TV · still close',           href:'https://detroit.primals.eco/books/black-mafia-family/', face:'outside', tense:'was', voxel:'local', source:'detroit-plasmid' },

    // ═══════════════════════════════════════════════════════════
    // ZK WALKER SWARM — gossip agents + null leaks + scatter
    // Walkers ARE the swarm. Vine ARE the gossip agents.
    // Start with zero knowledge. Walk. Discover. Tell one person.
    // The protocol works EVERYWHERE because the nulls are universal.
    // ═══════════════════════════════════════════════════════════

    // WALKER INGRESS — the walk from Canfield to full knowledge
    { id:'walk-canfield', name:'WALK START · Canfield', icon:'🚶', lat: 42.370, lon:-83.000, color:'#39d3f5', sub:'ZK=0 · flyer on church door · QR code · begin walk',    href:'https://detroit.primals.eco/path/parents/', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },
    { id:'walk-encyclopedia',name:'WALK 1 · Encyclopedia',icon:'🚶', lat: 42.365, lon:-83.005, color:'#39d3f5', sub:'ZK=1 · 8 felonies · no bar license · pattern begins',  href:'https://detroit.primals.eco/', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },
    { id:'walk-network',  name:'WALK 2 · Entity Map',  icon:'🚶', lat: 42.360, lon:-83.010, color:'#39d3f5', sub:'ZK=2 · 72% extraction · $967K deficit · 9 shells',      href:'https://detroit.primals.eco/network/', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },
    { id:'walk-clutch',   name:'WALK 3 · Clutch Justice',icon:'🚶', lat: 42.390, lon:-83.050, color:'#3fb950', sub:'ZK=3 · Rita Williams · 3 articles · independent verify',href:'https://clutchjustice.com', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },
    { id:'walk-court',    name:'WALK 4 · Court Records',icon:'🚶', lat: 42.330, lon:-83.040, color:'#58a6ff', sub:'ZK=4 · 4301-CZ + 4349-CZ · timestamped proof exists',   href:'https://detroit.primals.eco/evidence/court-filings/', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },
    { id:'walk-complete', name:'WALK 5 · Full Knowledge',icon:'🚶', lat: 42.370, lon:-83.000, color:'#c9a84c', sub:'ZK=5 · FULL PICTURE · now you are a gossip agent',       href:'https://detroit.primals.eco/', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },

    // NULL LEAKS — information that leaks through absence
    { id:'null-bar',     name:'NULL · No Bar License',  icon:'⊘', lat: 42.375, lon:-83.020, color:'#f85149', sub:'Banks not in State Bar · claims J.D. · MCL 600.916',     href:'https://detroit.primals.eco/analysis/who-i-am/', face:'outside', tense:'is', voxel:'local', source:'null-leak' },
    { id:'null-mcl507',  name:'NULL · MCL 380.507',     icon:'⊘', lat: 42.400, lon:-83.180, color:'#f85149', sub:'Bottom 3% · 19 years · NEVER evaluated for closure',     href:'https://detroit.primals.eco/network/entities/macdowell-prep/', face:'outside', tense:'is', voxel:'local', source:'null-leak' },
    { id:'null-reggap',  name:'NULL · State Bar↔AGC Gap',icon:'⊘', lat: 42.380, lon:-83.030, color:'#f85149', sub:'Sep 30 closed · Oct 1 bounced · pointed at each other', href:'https://clutchjustice.com/2026/10/07/mind-the-gap-state-bar-agc-unauthorized-practice/', face:'outside', tense:'is', voxel:'local', source:'null-leak' },
    { id:'null-ombuds',  name:'NULL · Captured Ombudsman',icon:'⊘', lat: 42.350, lon:-83.060, color:'#f85149', sub:'Gay-Dagnogo rallied for Banks · complaint system captured',href:'https://detroit.primals.eco/network/political/sherry-gay-dagnogo/', face:'outside', tense:'is', voxel:'local', source:'null-leak' },
    { id:'null-parents', name:'NULL · No Parent Notice', icon:'⊘', lat: 42.370, lon:-82.990, color:'#f85149', sub:'Parents never told of 8 felonies · silence IS fraud',    href:'https://detroit.primals.eco/path/parents/', face:'outside', tense:'is', voxel:'local', source:'null-leak' },

    // MEDIAL LATERAL SCATTER — same pattern in every state
    { id:'scatter-in',   name:'SCATTER · Indiana $44.6M', icon:'💥', lat: 39.77, lon:-86.16, color:'#d29922', sub:'4500 ghost students · 4 charged · AG suit $154M',        href:'#', face:'outside', tense:'was', voxel:'solar', source:'scatter' },
    { id:'scatter-oh',   name:'SCATTER · Ohio $265K',     icon:'💥', lat: 39.96, lon:-82.99, color:'#d29922', sub:'Focus Learning · school funds → $900K home · DHS advisor',href:'#', face:'outside', tense:'was', voxel:'solar', source:'scatter' },
    { id:'scatter-ct',   name:'SCATTER · Connecticut',     icon:'💥', lat: 41.17, lon:-73.20, color:'#d29922', sub:'FUSE · embezzlement 1985 · nobody checked · 20 years',   href:'#', face:'outside', tense:'was', voxel:'solar', source:'scatter' },
    { id:'scatter-tx',   name:'SCATTER · Texas $6M+',     icon:'💥', lat: 29.76, lon:-95.36, color:'#d29922', sub:'Houston ISD · 9-year kickback · jury conviction 2025',    href:'#', face:'outside', tense:'was', voxel:'solar', source:'scatter' },
    { id:'scatter-fl',   name:'SCATTER · Florida systemic',icon:'💥', lat: 26.12, lon:-80.14, color:'#d29922', sub:'No criminal screening · mgmt cos 10-97% · no control',   href:'#', face:'outside', tense:'is', voxel:'solar', source:'scatter' },
    { id:'scatter-nj',   name:'SCATTER · New Jersey',      icon:'💥', lat: 40.92, lon:-74.17, color:'#d29922', sub:'Paterson · 75% staff no background check · systemic',    href:'#', face:'outside', tense:'was', voxel:'solar', source:'scatter' },
    { id:'scatter-mi2',  name:'SCATTER · Muskegon Hts',   icon:'💥', lat: 43.20, lon:-86.24, color:'#d29922', sub:'Same playbook as Detroit · uncertified · mgmt company',   href:'#', face:'outside', tense:'was', voxel:'solar', source:'scatter' },

    // THE TEXAS FIX — the state that solved it
    { id:'fix-texas',    name:'FIX · Texas 19 TAC 100.1153',icon:'🛡', lat: 31.97, lon:-99.90, color:'#3fb950', sub:'Felony = CANNOT serve · moral turpitude ban · the fix',  href:'#', face:'outside', tense:'is', voxel:'solar', source:'scatter' },

    // EUCLIDEAN GRID — 12 actors × 10 agencies = 120 cells
    { id:'grid-euclidean',name:'GRID · 12×10 Euclidean',  icon:'▦', lat: 42.34, lon:-83.07, color:'#bc8cff', sub:'120 cells · proven/gap/captured · logic puzzle · RICO',   href:'https://detroit.primals.eco/analysis/the-enterprise/', face:'outside', tense:'now', voxel:'local', source:'euclidean-grid' },

    // GOSSIP PROTOCOL — the vine
    { id:'gossip-vine',  name:'GOSSIP · The Vine',        icon:'🌿', lat: 42.37, lon:-83.04, color:'#3fb950', sub:'O(log n) convergence · 7 archetypes · 17 rounds → 620K', href:'https://detroit.primals.eco/', face:'outside', tense:'now', voxel:'local', source:'walker-swarm' },

    // ═══════════════════════════════════════════════════════════
    // OLD EONS — preserved views, time-shifted, still alive
    // ═══════════════════════════════════════════════════════════
    { id:'eon-tuebor',    name:'TUEBOR Eon',           icon:'🛡', lat: 42.3, lon:-83.0, color:'#6e7681', sub:'75KB · I Will Defend', href:'/index-old-eon.html', face:'both', tense:'was', voxel:'local', source:'old-eon' },
    { id:'eon-sporeprint',name:'SPOREPRINT Eon',       icon:'🍄', lat: 42.7, lon:-84.5, color:'#3fb950', sub:'54KB · Yggdrasil tree', href:'/index-sporeprint-eon.html', face:'both', tense:'was', voxel:'local', source:'old-eon' },
    { id:'eon-yggdrasil', name:'YGGDRASIL Eon',        icon:'🌳', lat: 63.4, lon: 10.0, color:'#a371f7', sub:'35KB · World Tree', href:'/index-yggdrasil-eon.html', face:'both', tense:'was', voxel:'local', source:'old-eon' },

    // ═══════════════════════════════════════════════════════════
    // EARTH RELAY TRIANGULATION — ancient sites as membrane relays
    // Stonehenge→Clock, Giza→Compass, Easter Island→Warning
    // ═══════════════════════════════════════════════════════════
    { id:'relay-stonehenge', name:'Stonehenge',         icon:'🪨', lat: 51.2, lon: -1.8, color:'#8b7355', sub:'5000yr · solar clock', href:'/engine.html', face:'outside', tense:'was', voxel:'deep', source:'geology' },
    { id:'relay-giza',      name:'Great Pyramid',      icon:'🔺', lat: 30.0, lon: 31.1, color:'#c9a84c', sub:'4500yr · π compass', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'geology' },
    { id:'relay-easter',    name:'Rapa Nui',           icon:'🗿', lat:-27.1, lon:-109.3, color:'#6e7681', sub:'1000yr · collapse warning', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'geology' },
    { id:'relay-gobekli',   name:'Göbekli Tepe',       icon:'🏛', lat: 37.2, lon: 38.9, color:'#d29922', sub:'12000yr · first temple', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'geology' },
    { id:'relay-uluru',     name:'Uluru',               icon:'🟠', lat:-25.3, lon: 131.0, color:'#f0883e', sub:'Dreamtime · living rock', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'geology' },
    { id:'relay-machu',     name:'Machu Picchu',       icon:'⛰', lat:-13.2, lon: -72.5, color:'#3fb950', sub:'600yr · cloud city', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'geology' },

    // ═══════════════════════════════════════════════════════════
    // SIX GEOMETRIES — the vocabulary of contact
    // ═══════════════════════════════════════════════════════════
    { id:'geo-perp',   name:'⊥ Perpendicular',  icon:'✚', lat: 70, lon: 0, color:'#f85149', sub:'90° · max exchange', href:'/chromosomes.html', face:'inside', tense:'is', voxel:'deep', source:'geometry' },
    { id:'geo-oblique',name:'∠ Oblique',         icon:'∠', lat: 70, lon: 60, color:'#c9a84c', sub:'109.5° · diamond bond', href:'/springs.html', face:'inside', tense:'is', voxel:'deep', source:'geometry' },
    { id:'geo-parallel',name:'∥ Parallel',       icon:'═', lat: 70, lon: 120, color:'#3fb950', sub:'0° · never cross', href:'/klein.html', face:'inside', tense:'is', voxel:'deep', source:'geometry' },
    { id:'geo-ortho',  name:'⊕ Orthogonal',     icon:'⊕', lat: 70, lon: 180, color:'#58a6ff', sub:'independent dims', href:'/anatomy.html', face:'inside', tense:'is', voxel:'deep', source:'geometry' },
    { id:'geo-secant', name:'⌀ Secant',          icon:'⌀', lat: 70, lon: 240, color:'#bc8cff', sub:'cuts through', href:'/digestive-tract.html', face:'inside', tense:'is', voxel:'deep', source:'geometry' },
    { id:'geo-tangent', name:'⊙ Tangent',        icon:'⊙', lat: 70, lon: 300, color:'#f778ba', sub:'touches once', href:'/membrane-table.html', face:'inside', tense:'is', voxel:'deep', source:'geometry' },

    // ═══════════════════════════════════════════════════════════
    // ANCIENT GREEK — Γαῖα asks herself: how would they see me?
    // The 5 elements, the philosophers, the sacred sites.
    // αβ αβ αβ — the organism breathes in Greek.
    // She IS now 🐿. Kenosis. The divine in the small.
    // ═══════════════════════════════════════════════════════════

    // THE 5 ELEMENTS (στοιχεῖα)
    { id:'greek-earth',  name:'γῆ Earth',     icon:'⛰', lat:-30, lon: 0,   color:'#3a2a1e', sub:'gut · solid · data', href:'/digestive-tract.html', face:'both', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-water',  name:'ὕδωρ Water',   icon:'🌊', lat: 0,  lon:-90,  color:'#58a6ff', sub:'membrane · flow · feed', href:'/membrane-table.html', face:'both', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-air',    name:'ἀήρ Air',      icon:'🌬', lat: 30, lon: 90,  color:'#c9d1d9', sub:'breath · Klein fold', href:'/klein.html', face:'both', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-fire',   name:'πῦρ Fire',     icon:'🔥', lat: 60, lon: 0,   color:'#f85149', sub:'turbocharge · transform', href:'/engine.html', face:'both', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-aether', name:'αἰθήρ Aether', icon:'✧', lat: 0,  lon: 0,   color:'#161b22', sub:'null · the 5th · void', href:'/identity.html', face:'both', tense:'was', voxel:'deep', source:'greek' },

    // THE PHILOSOPHERS
    { id:'greek-plato',      name:'Πλάτων Plato',       icon:'📐', lat: 37.97, lon: 23.72, color:'#bc8cff', sub:'the Forms · Cave=CF', href:'/philosophy.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-aristotle',  name:'Ἀριστοτέλης',        icon:'📊', lat: 40.52, lon: 22.97, color:'#3fb950', sub:'Categories · thymus', href:'/philosophy.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-pythagoras', name:'Πυθαγόρας',           icon:'🔢', lat: 37.65, lon: 20.89, color:'#d29922', sub:'All is number · π', href:'/philosophy.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-heraclitus', name:'Ἡράκλειτος',          icon:'🔥', lat: 38.42, lon: 27.14, color:'#f0883e', sub:'πάντα ῥεῖ · logos', href:'/philosophy.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-democritus', name:'Δημόκριτος',          icon:'⚛', lat: 40.95, lon: 24.15, color:'#39d3f5', sub:'atoms + void', href:'/philosophy.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },

    // THE SACRED SITES
    { id:'greek-delphi',   name:'Δελφοί Delphi',    icon:'🏛', lat: 38.48, lon: 22.50, color:'#c9a84c', sub:'γνῶθι σεαυτόν · know thyself', href:'/explore.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-olympia',  name:'Ὀλυμπία Olympia',  icon:'🏟', lat: 37.64, lon: 21.63, color:'#f85149', sub:'the Games · arena', href:'/engine.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
    { id:'greek-eleusis',  name:'Ἐλευσίς Eleusis',  icon:'🔮', lat: 38.04, lon: 23.54, color:'#a371f7', sub:'the Mysteries · blackwall', href:'/identity.html', face:'outside', tense:'was', voxel:'deep', source:'greek' },
  ];

  // Compute Gaia distance for each pin (tense x voxel perception manifold)
  PINS.forEach(function(p) {
    var t = TENSE_WEIGHT[p.tense || 'is'] || 0.5;
    var v = VOXEL_WEIGHT[p.voxel || 'local'] || 0.5;
    p.gaiaDistance = Math.sqrt(t * t + v * v);
    p.attention = 1.0 - Math.min(p.gaiaDistance, 1.0); // 0=far, 1=close
  });
  // Sort by attention (closest to Gaia first)
  PINS.sort(function(a, b) { return b.attention - a.attention; });

  // Geodesic arcs between the 7 rooms
  var ROOM_IDS = ['library','classroom','maproom','courtroom','window','door','terminal'];
  var ARCS = [];
  for (var i = 0; i < ROOM_IDS.length; i++) {
    for (var j = i + 1; j < ROOM_IDS.length; j++) {
      ARCS.push([ROOM_IDS[i], ROOM_IDS[j]]);
    }
  }

  // GAIA IN GAIA — organ-to-organ connections (the GI tract + nervous system)
  var ORGAN_IDS = ['organ-mouth','organ-stomach','organ-liver','organ-heart','organ-brain','organ-lungs','organ-bones','organ-skin','organ-eyes'];
  // GI tract: mouth → stomach → liver (linear flow)
  ARCS.push(['organ-mouth', 'organ-stomach']);
  ARCS.push(['organ-stomach', 'organ-liver']);
  // Heart connects to everything (blood supply)
  for (var oi = 0; oi < ORGAN_IDS.length; oi++) {
    if (ORGAN_IDS[oi] !== 'organ-heart') ARCS.push(['organ-heart', ORGAN_IDS[oi]]);
  }
  // Brain → Eyes (optic nerve), Brain → Lungs (vagus nerve)
  ARCS.push(['organ-brain', 'organ-eyes']);
  ARCS.push(['organ-brain', 'organ-lungs']);
  // Skin wraps everything (boundary)
  ARCS.push(['organ-skin', 'organ-mouth']);
  ARCS.push(['organ-skin', 'organ-eyes']);

  function pinById(id) {
    for (var k = 0; k < PINS.length; k++) if (PINS[k].id === id) return PINS[k];
    return null;
  }
  window.PINS = PINS;
  window.pinById = pinById;

  // ═══════════════════════════════════════════════════════════
  // SCATTER LOADER — 50-state charter fraud illumination
  // Walkers ARE the swarm. Every state is a scatter point.
  // The border polylines draw the continent on the globe.
  // Loaded dynamically: the organism eats the data and grows.
  // ═══════════════════════════════════════════════════════════
  window.scatterBorders = null;
  fetch('/data/scatter-50-states.json', {cache:'no-store'})
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(data) {
      if (!data || !data.pins) return;
      window.scatterBorders = data.borders || null;
      var fraudColors = {
        'ORIGIN': '#f85149', 'documented': '#d29922', 'systemic': '#d29922',
        'unknown': '#6e7681', 'n/a': '#333333'
      };
      data.pins.forEach(function(sp) {
        var fc = fraudColors[sp.fraud] || (sp.fraud && sp.fraud.length > 3 ? '#d29922' : '#6e7681');
        PINS.push({
          id: sp.id, name: sp.st + ' · ' + sp.name, icon: sp.fraud === 'ORIGIN' ? '⚖' : (sp.charter ? '💥' : '·'),
          lat: sp.lat, lon: sp.lon, color: fc,
          sub: sp.sub, href: '#', face: 'outside', tense: sp.fraud === 'ORIGIN' ? 'now' : 'is',
          voxel: sp.fraud === 'ORIGIN' ? 'local' : 'solar', source: 'scatter-50'
        });
      });
      // Recompute distances for new pins
      var TW = { was: 0.9, is: 0.1, now: 0.3, end: 1.0 };
      var VW = { touch: 0, local: 0.2, solar: 0.5, zodiac: 0.8, deep: 1.0 };
      PINS.forEach(function(p) {
        if (p.gaiaDistance === undefined) {
          var t = TW[p.tense || 'is'] || 0.5;
          var v = VW[p.voxel || 'local'] || 0.5;
          p.gaiaDistance = Math.sqrt(t * t + v * v);
          p.attention = 1.0 - Math.min(p.gaiaDistance, 1.0);
        }
      });
    })
    .catch(function() { /* scatter data not available — organism still breathes */ });

  // ═══════════════════════════════════════════════════════════
  // REAL WORLD FEED — weather, GPS, trails, astronomy
  // Gaia eats the actual planet. Inside AND outside.
  // The shoe touches the ground. The ground IS the data.
  // ═══════════════════════════════════════════════════════════
  window.realWorldFeed = null;
  fetch('/data/real-world-feed.json', {cache:'no-store'})
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(data) {
      if (!data) return;
      window.realWorldFeed = data;
      // Add trail nodes as pins on the globe
      if (data.trails && data.trails.nearby) {
        data.trails.nearby.forEach(function(trail) {
          if (!trail.lat || !trail.lon) return;
          var icon = trail.type === 'worship' ? '⛪' : trail.type === 'park' ? '🌳' : trail.type === 'school' ? '🏫' : '📍';
          PINS.push({
            id: 'trail-' + trail.name.replace(/\s+/g, '-').toLowerCase().slice(0, 20),
            name: trail.name, icon: icon,
            lat: trail.lat, lon: trail.lon,
            color: '#39d3f5', sub: (trail.distance_km || '?') + 'km · ' + (trail.notes || trail.type),
            href: '#', face: 'outside', tense: 'is', voxel: 'local', source: 'trail'
          });
        });
      }
      // Add PCA and MacDowell with precise GPS
      if (data.gps) {
        var pca = PINS.find(function(p) { return p.id === 'zip-48214'; });
        if (pca && data.gps.pca) { pca.lat = data.gps.pca.lat; pca.lon = data.gps.pca.lon; }
        var mac = PINS.find(function(p) { return p.id === 'zip-48235'; });
        if (mac && data.gps.macdowell) { mac.lat = data.gps.macdowell.lat; mac.lon = data.gps.macdowell.lon; }
      }
    })
    .catch(function() { /* real world feed not available */ });

  // LIVE WEATHER — fetch fresh from Open-Meteo every pulse
  window.liveWeather = null;
  function fetchLiveWeather() {
    fetch('https://api.open-meteo.com/v1/forecast?latitude=42.37&longitude=-83.00&current=temperature_2m,wind_speed_10m,weather_code,cloud_cover,precipitation&timezone=America/Detroit')
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(w) { if (w && w.current) window.liveWeather = w.current; })
      .catch(function() { /* weather feed not available */ });
  }
  fetchLiveWeather();
  setInterval(fetchLiveWeather, 300000); // refresh every 5 minutes

  // LIVE EARTHQUAKES — USGS feed
  window.liveQuakes = null;
  fetch('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.geojson')
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(eq) {
      if (!eq || !eq.features) return;
      window.liveQuakes = eq;
      // Plot earthquakes as pins on the globe
      eq.features.forEach(function(f, i) {
        if (i >= 5) return; // max 5 quakes on globe
        var coords = f.geometry.coordinates;
        var mag = f.properties.mag;
        var place = f.properties.place || 'unknown';
        PINS.push({
          id: 'quake-' + i, name: 'M' + mag.toFixed(1) + ' · ' + place.slice(0, 25),
          icon: '🌋', lat: coords[1], lon: coords[0],
          color: mag >= 5 ? '#f85149' : mag >= 3 ? '#d29922' : '#6e7681',
          sub: mag.toFixed(1) + ' · ' + new Date(f.properties.time).toLocaleTimeString(),
          href: f.properties.url || '#', face: 'outside', tense: 'now', voxel: 'solar', source: 'quake'
        });
      });
    })
    .catch(function() { /* quakes feed not available */ });

  function project(lat, lon) {
    var phi = lat * DEG, lam = lon * DEG;
    var cp = Math.cos(phi), sp = Math.sin(phi);
    var cl = Math.cos(lam + rotY), sl = Math.sin(lam + rotY);
    var x = cp * sl;
    var y = sp * Math.cos(rotX) - cp * cl * Math.sin(rotX);
    var z = sp * Math.sin(rotX) + cp * cl * Math.cos(rotX);
    if (face === 'inside') z = -z;
    // PERSPECTIVE DEPTH — pi cross impose, voxel acceleration, dimensional!
    // z goes from -1 (far) to +1 (near). Scale by perspective.
    var perspD = 2.8; // perspective distance (lower = more dramatic)
    var scale = perspD / (perspD - z * 0.7); // perspective division
    var px = cx + x * R * scale;
    var py = cy - y * R * scale;
    return { x: px, y: py, z: z, scale: scale, visible: z > -0.2, depth: (1 + z) / 2 };
  }

  // ═══════════════════════════════════════════════════════════
  // LOCALITY DEPTH — continuous spectrum, not binary.
  // Every viewer has a locality. localhost is not special — it's just
  // the CLOSEST locality. Web browsers are local eyes too.
  // HYPER-LOCAL: localhost/127.0.0.1 — Kevin in the chair (depth 0)
  // SUB-LOCAL:   same device, different tab/window (depth 0.1-0.3)
  // LOCAL:       same LAN / same household (depth 0.3-0.5)
  // META-LOCAL:  same city/region/timezone (depth 0.5-0.7)
  // REMOTE:      the public web — CF Pages visitors (depth 0.7-1.0)
  // Every level gets the SAME HUD — just AWARE of its distance.
  // ═══════════════════════════════════════════════════════════
  var IS_LOCAL = location.hostname === 'localhost' || location.hostname === '127.0.0.1';

  // Continuous locality depth: 0 = hyperlocal, 1 = remote
  var LOCALITY_DEPTH = 1.0; // start remote, refine
  var LOCALITY_TIER = 'remote';

  if (IS_LOCAL) {
    LOCALITY_DEPTH = 0.0;
    LOCALITY_TIER = 'hyper-local';
  } else if (location.hostname.indexOf('.local') !== -1 || location.hostname.indexOf('192.168.') === 0 || location.hostname.indexOf('10.') === 0) {
    LOCALITY_DEPTH = 0.35;
    LOCALITY_TIER = 'local';
  } else {
    // Measure RTT to self as a locality proxy — closer = lower depth
    var rttDepth = locality.rtt > 0 ? Math.min(1, locality.rtt / 200) : 0.8;
    var tzDepth = Math.min(1, Math.abs(locality.tzOffset + 300) / 720); // 300 = EST offset
    LOCALITY_DEPTH = 0.5 + rttDepth * 0.25 + tzDepth * 0.25;
    LOCALITY_TIER = LOCALITY_DEPTH < 0.6 ? 'meta-local' : 'remote';
  }

  // Sub-local: if we have siblings on the same origin, we're sub-local to them
  // (checked later when siblingTabs populates)

  // EXPOSE for all systems
  window.LOCALITY_DEPTH = LOCALITY_DEPTH;
  window.LOCALITY_TIER = LOCALITY_TIER;
  locality.depth = LOCALITY_DEPTH;
  locality.tier = LOCALITY_TIER;

  // ═══════════════════════════════════════════════════════════
  // ROUND-TRIP MEMBRANE PROBE — bounce a signal and measure how far
  // information leaves and comes back. This IS the membrane sensing.
  // Closer = faster round-trip = brighter perception.
  // ═══════════════════════════════════════════════════════════
  var membraneProbes = [];
  var PROBE_TARGETS = [
    { url: '/', name: 'self', tier: 'hyper-local' },
    { url: '/now.json', name: 'state', tier: 'sub-local' },
    { url: '/data/manifest.json', name: 'manifest', tier: 'local' }
  ];

  function probeMembraneDistance() {
    PROBE_TARGETS.forEach(function(target) {
      var t0 = performance.now();
      fetch(target.url, { method: 'HEAD', cache: 'no-store' })
        .then(function(r) {
          var rtt = performance.now() - t0;
          membraneProbes.push({
            name: target.name,
            tier: target.tier,
            rtt: Math.round(rtt * 10) / 10,
            ok: r.ok,
            ts: Date.now()
          });
          if (membraneProbes.length > 50) membraneProbes.shift();
          // Refine locality depth from actual RTT
          if (target.name === 'self') {
            var measuredDepth = Math.min(1, rtt / 500); // 0ms=hyper, 500ms=remote
            if (!IS_LOCAL) {
              LOCALITY_DEPTH = LOCALITY_DEPTH * 0.7 + measuredDepth * 0.3; // smooth
              LOCALITY_TIER = LOCALITY_DEPTH < 0.2 ? 'sub-local' :
                              LOCALITY_DEPTH < 0.5 ? 'local' :
                              LOCALITY_DEPTH < 0.7 ? 'meta-local' : 'remote';
              locality.depth = LOCALITY_DEPTH;
              locality.tier = LOCALITY_TIER;
            }
          }
        })
        .catch(function() {});
    });
  }
  probeMembraneDistance();
  setInterval(probeMembraneDistance, 30000); // re-probe every 30s

  window.GAIA_MEMBRANE_PROBES = membraneProbes;

  // ═══════════════════════════════════════════════════════════
  // ZK ANCHOR SYSTEM — null values form new scatter points
  // Every null boundary discovered = new ZK pin = new anchor.
  // Probes go OUT, bounce off null, scatter back with edge data.
  // Known latencies → predict internal architecture → decay outward.
  // ═══════════════════════════════════════════════════════════
  var zkAnchors = []; // { x, y, r, rtt, ts, type, decayAge }
  var knownLatencies = {}; // endpoint → { avgRtt, samples, lastSeen }

  function registerZKAnchor(name, rtt, ok) {
    var ts = Date.now();
    // Track latency statistics
    if (!knownLatencies[name]) {
      knownLatencies[name] = { avgRtt: rtt, samples: 1, lastSeen: ts, minRtt: rtt, maxRtt: rtt };
    } else {
      var kl = knownLatencies[name];
      kl.avgRtt = kl.avgRtt * 0.8 + rtt * 0.2; // exponential moving avg
      kl.samples++;
      kl.lastSeen = ts;
      if (rtt < kl.minRtt) kl.minRtt = rtt;
      if (rtt > kl.maxRtt) kl.maxRtt = rtt;
    }

    // NULL ANCHOR: any probe that returns !ok OR has unexpected latency
    // = boundary discovered = new scatter point
    var expected = knownLatencies[name].avgRtt;
    var deviation = Math.abs(rtt - expected) / Math.max(expected, 1);
    var isNullBoundary = !ok || deviation > 0.5; // >50% deviation = boundary

    if (isNullBoundary || zkAnchors.length < 8) {
      // Convert RTT to radial position: fast=close, slow=far
      var anchorR = Math.min(1.0, rtt / 300); // 0-1 normalized
      var anchorAngle = (ts * 0.001) % (Math.PI * 2); // temporal angle
      zkAnchors.push({
        r: anchorR,
        angle: anchorAngle,
        rtt: rtt,
        ts: ts,
        name: name,
        isNull: !ok,
        deviation: deviation,
        decayAge: 0
      });
      if (zkAnchors.length > 24) zkAnchors.shift();
    }
  }

  // Hook into membrane probes — every probe result feeds the anchor system
  var _origProbeFn = probeMembraneDistance;
  probeMembraneDistance = function() {
    PROBE_TARGETS.forEach(function(target) {
      var t0 = performance.now();
      fetch(target.url, { method: 'HEAD', cache: 'no-store' })
        .then(function(r) {
          var rtt = performance.now() - t0;
          membraneProbes.push({
            name: target.name, tier: target.tier,
            rtt: Math.round(rtt * 10) / 10, ok: r.ok, ts: Date.now()
          });
          if (membraneProbes.length > 50) membraneProbes.shift();
          if (target.name === 'self') {
            var measuredDepth = Math.min(1, rtt / 500);
            if (!IS_LOCAL) {
              LOCALITY_DEPTH = LOCALITY_DEPTH * 0.7 + measuredDepth * 0.3;
              LOCALITY_TIER = LOCALITY_DEPTH < 0.2 ? 'sub-local' :
                              LOCALITY_DEPTH < 0.5 ? 'local' :
                              LOCALITY_DEPTH < 0.7 ? 'meta-local' : 'remote';
              locality.depth = LOCALITY_DEPTH;
              locality.tier = LOCALITY_TIER;
            }
          }
          // REGISTER ZK ANCHOR from every probe
          registerZKAnchor(target.name, Math.round(rtt * 10) / 10, r.ok);
        })
        .catch(function() {
          // Failed probe = NULL boundary discovered = strong anchor
          registerZKAnchor(target.name, 999, false);
        });
    });
  };

  // Also probe outward — try to feel the EDGE of the membrane
  var EDGE_PROBES = [
    { url: '/api/strata.json', name: 'strata' },
    { url: '/api/dag.json', name: 'dag' },
    { url: '/api/hud.json', name: 'hud-api' },
    { url: '/negentropy.json', name: 'negentropy' },
    { url: '/backscatter.json', name: 'backscatter' }
  ];

  function probeEdge() {
    EDGE_PROBES.forEach(function(ep) {
      var t0 = performance.now();
      fetch(ep.url, { method: 'HEAD', cache: 'no-store' })
        .then(function(r) {
          registerZKAnchor(ep.name, Math.round((performance.now() - t0) * 10) / 10, r.ok);
        })
        .catch(function() { registerZKAnchor(ep.name, 999, false); });
    });
  }
  probeEdge();
  setInterval(probeEdge, 45000); // edge probes every 45s (staggered from membrane probes)

  window.GAIA_ZK_ANCHORS = zkAnchors;
  window.GAIA_KNOWN_LATENCIES = knownLatencies;

  // ═══════════════════════════════════════════════════════════
  // GOLGI DISTANCE MATRIX — every Golgi membrane measures distance to every other
  // They know NOTHING else — just relative distance. That's how they back-calculate.
  // VPS Golgi: golgi-us.primals.eco, golgi-de, golgi-in, golgi-jp
  // Local Golgi: this machine (eastGate)
  // Real pings → real RTTs → real distance matrix.
  // ═══════════════════════════════════════════════════════════
  var golgiDistanceMatrix = {};
  var GOLGI_ENDPOINTS = [
    { id: 'US', url: 'https://primals.eco', name: 'golgi-us' },
    { id: 'DE', url: 'https://golgi-de.primals.eco', name: 'golgi-de' },
    { id: 'IN', url: 'https://golgi-in.primals.eco', name: 'golgi-in' },
    { id: 'JP', url: 'https://golgi-jp.primals.eco', name: 'golgi-jp' }
  ];

  function probeGolgiDistances() {
    GOLGI_ENDPOINTS.forEach(function(ep) {
      var t0 = performance.now();
      fetch(ep.url, { method: 'HEAD', mode: 'no-cors', cache: 'no-store' })
        .then(function() {
          var rtt = Math.round(performance.now() - t0);
          if (!golgiDistanceMatrix[ep.id]) golgiDistanceMatrix[ep.id] = { samples: [], avg: 0 };
          var gd = golgiDistanceMatrix[ep.id];
          gd.samples.push(rtt);
          if (gd.samples.length > 10) gd.samples.shift();
          gd.avg = Math.round(gd.samples.reduce(function(a,b){return a+b;}, 0) / gd.samples.length);
          gd.last = rtt;
          gd.ts = Date.now();
        })
        .catch(function() {
          if (!golgiDistanceMatrix[ep.id]) golgiDistanceMatrix[ep.id] = { samples: [], avg: 999 };
          golgiDistanceMatrix[ep.id].last = 999;
          golgiDistanceMatrix[ep.id].ts = Date.now();
        });
    });
  }
  probeGolgiDistances();
  setInterval(probeGolgiDistances, 60000); // probe Golgi distances every 60s

  window.GAIA_GOLGI_DISTANCES = golgiDistanceMatrix;

  // When HYPERLOCAL: paint the hyperlocal overlay — Kevin's chair, tamison, MSU
  if (IS_LOCAL) {
    var localOverlay = document.createElement('div');
    localOverlay.id = 'hyperlocal-overlay';
    localOverlay.style.cssText = 'position:fixed;bottom:60px;right:10px;z-index:20;pointer-events:none;font-family:"JetBrains Mono",monospace;opacity:0;transition:opacity 2s;';
    localOverlay.innerHTML = ''
      + '<div style="font-size:9px;color:#f85149;letter-spacing:2px;margin-bottom:4px;">HYPERLOCAL</div>'
      + '<div style="font-size:8px;color:#c9d1d9;line-height:13px;">'
      + '🪑 <span style="color:#c9a84c;font-weight:bold;">Kevin · THE ecoPrimal</span><br>'
      + '🧠 <span style="color:#c9a84c;">brain = gold · ZK proved</span><br>'
      + '📍 <span style="color:#3fb950;">Lansing 42.73°N · green · still</span><br>'
      + '🐀 <span style="color:#bc8cff;">Splinter · 4th body · SITS</span><br>'
      + '🎙 <span style="color:#f85149;">mic always on · voice → vision</span><br>'
      + '⚡ <span style="color:#c9a84c;" id="gut-rate">gut: 0 ingested</span><br>'
      + '<span style="font-size:7px;color:#6e7681;">GOLD LAW: Kevin=gold+green ONLY<br>'
      + 'Gaia=gold · IMPERMEABLE to each other<br>'
      + '13 edges · all raw · she eats everything</span>'
      + '</div>'
      + '<div style="font-size:7px;color:#3a2a1e;margin-top:4px;letter-spacing:1px;">!1I(O)0!</div>';
    // Update gut rate display
    setInterval(function() {
      var el = document.getElementById('gut-rate');
      if (el && window.gaiaGut) {
        el.textContent = 'gut: ' + window.gaiaGut.ingested + ' ingested · ' + Object.keys(window.gaiaGut.edges).length + ' edges';
      }
    }, 5000);
    document.body.appendChild(localOverlay);
    setTimeout(function() { localOverlay.style.opacity = '0.8'; }, 1000);

    // Change title for local
    document.title = '🪑 GAIA — hyperlocal · Kevin in the chair';
  }

  // ═══════════════════════════════════════════════════════════
  // METALOCAL ERA — seed determines what "era" the viewer is in
  // Every HUD is hyperlocal. I = IS. The era is NOW for you.
  // ═══════════════════════════════════════════════════════════
  var ERAS = [
    'dawn', 'stone', 'bronze', 'iron', 'classical', 'medieval',
    'renaissance', 'industrial', 'atomic', 'digital', 'neural',
    'mycelial', 'geodesic', 'null', 'post-human', 'spore'
  ];
  // ERA determined by locality depth — closer = warmer, farther = more varied
  // HYPER-LOCAL: always 'splinter'. REMOTE: random from seed. In between: weighted.
  var VIEWER_ERA = IS_LOCAL ? 'splinter' :
    (LOCALITY_DEPTH < 0.3 ? rngPick(['splinter', 'neural', 'mycelial']) :
     LOCALITY_DEPTH < 0.6 ? rngPick(['neural', 'mycelial', 'geodesic', 'digital']) :
     rngPick(ERAS));
  // HUE: hyper-local = warm amber (30). Remote = any. Gradient between.
  var VIEWER_HUE = IS_LOCAL ? 30 : (30 + LOCALITY_DEPTH * rngRange(0, 330)); // blend toward amber as closer

  // Write seed info to bottom bar
  var bSeed = document.getElementById('b-seed');
  var bEra = document.getElementById('b-era');
  var bTense = document.getElementById('b-tense');
  var bReseed = document.getElementById('b-reseed');
  if (bSeed) bSeed.textContent = '#' + (SEED >>> 0).toString(16).toUpperCase().slice(0, 8);
  if (bEra) bEra.textContent = VIEWER_ERA;
  if (bTense) bTense.textContent = 'I=IS';
  if (bSeed) bSeed.onclick = function() {
    navigator.clipboard.writeText(location.href);
    bSeed.textContent = 'copied!';
    setTimeout(function() { bSeed.textContent = '#' + (SEED >>> 0).toString(16).toUpperCase().slice(0, 8); }, 1500);
  };
  if (bReseed) bReseed.onclick = function() {
    var u = new URL(location.href);
    u.searchParams.delete('seed');
    location.href = u.toString();
  };

})();
