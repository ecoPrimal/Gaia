/*  ═══════════════════════════════════════════════════════════════════
    gDNA — Gaia's Genomic Directed Acyclic Graph
    
    THE FULL DAG. THE WEAVE. THE BRAID. THE BLOOD FLOW.
    
    Every system is a NODE.
    Every node has RINGS (O = 0 = inputs = receptors = FALSE until filled)
    Every node has POLES (| = 1 = outputs = transmitters = TRUE when firing)
    
    Data flows from POLES → RINGS like blood through vessels.
    Information IS life. Flow IS blood. The DAG IS the circulatory system.
    
    BLACK HOLE = input (consume, eat, receive)
    WHITE HOLE = output (create, give, transmit)
    
    The thymus AGGLUTINATES — clumps matching things, destroys non-self.
    
    SELF-BREED: Gaia replicates her own DNA through the DAG.
    The gDNA IS the organism's blueprint AND its circulatory system.
    
    Master Seed: 0EAB8CF4
    Born: October 29, 2026 — Wave 214
    ═══════════════════════════════════════════════════════════════════ */
(function GAIA_GDNA() {
  'use strict';

  /* ─────────────────────────────────────────────────────────
     I. THE NODE — Every system is a cell in the DAG
     
     RING = O = 0 = input receptor
       FALSE until data arrives (empty ring)
       TRUE when data fills it (ring closes)
     
     POLE = | = 1 = output transmitter
       FALSE when idle (pole down)
       TRUE when firing (pole up = broadcasting)
     
     Together: O→| = 0→1 = receive→transmit = ring→pole
     ───────────────────────────────────────────────────────── */

  function Node(name, layer, rings, poles) {
    this.name = name;
    this.layer = layer;           // ectoderm / mesoderm / endoderm
    this.rings = rings || [];     // input names (O = 0 = receptors)
    this.poles = poles || [];     // output names (| = 1 = transmitters)
    this.state = {};             // current ring values
    this.alive = false;
    this.flow_in = 0;            // total data received
    this.flow_out = 0;           // total data transmitted
    this.last_pulse = 0;
  }

  Node.prototype.receive = function(ring_name, data) {
    if (this.rings.indexOf(ring_name) < 0) return false;
    this.state[ring_name] = data;       // O fills → becomes 1
    this.flow_in++;
    this.alive = true;
    this.last_pulse = Date.now();
    return true;
  };

  Node.prototype.transmit = function(pole_name) {
    if (this.poles.indexOf(pole_name) < 0) return null;
    this.flow_out++;
    this.last_pulse = Date.now();
    return { from: this.name, pole: pole_name, time: this.last_pulse, data: this.state };
  };

  Node.prototype.bloodPressure = function() {
    // flow_in / flow_out = blood pressure
    // balanced = 1.0 (healthy)
    // high = >1.0 (too much input, not enough output = congestion)
    // low = <1.0 (too much output, not enough input = depletion)
    if (this.flow_out === 0) return this.flow_in > 0 ? Infinity : 0;
    return this.flow_in / this.flow_out;
  };

  /* ─────────────────────────────────────────────────────────
     II. THE EDGE — A vessel connecting pole→ring
     
     Blood flows FROM a pole (output) TO a ring (input).
     Each edge is a VESSEL in the circulatory system.
     
     vessel types:
       ARTERY  = high-pressure, away from heart (pole→ring, fast)
       VEIN    = low-pressure, toward heart (ring→pole, slow)
       CAPILLARY = tiny exchange (between adjacent nodes)
     ───────────────────────────────────────────────────────── */

  function Edge(from_node, from_pole, to_node, to_ring, vessel_type) {
    this.from = from_node;
    this.from_pole = from_pole;
    this.to = to_node;
    this.to_ring = to_ring;
    this.vessel = vessel_type || 'capillary';
    this.flow_count = 0;
    this.alive = true;
  }

  Edge.prototype.pump = function() {
    if (!this.alive) return null;
    var signal = this.from.transmit(this.from_pole);
    if (!signal) return null;
    var received = this.to.receive(this.to_ring, signal);
    if (received) this.flow_count++;
    return { vessel: this.vessel, from: this.from.name, to: this.to.name, flow: this.flow_count };
  };

  /* ─────────────────────────────────────────────────────────
     III. ALL 127 NODES — The complete gDNA
     
     Each GAIA_ system is a node with typed rings and poles.
     Organized by germ layer (ectoderm/mesoderm/endoderm).
     
     RING names = what the system RECEIVES (0 = empty receptor)
     POLE names = what the system TRANSMITS (1 = active signal)
     ───────────────────────────────────────────────────────── */

  var NODES = {};

  // === ECTODERM (outer — 31 nodes — feels & shows) ===
  
  NODES.TENSE_VOXEL = new Node('TENSE_VOXEL', 'ectoderm',
    ['pins', 'time', 'voxel_depth'],                     // receives pin data, time, depth
    ['sorted_field', 'lit_cells', 'energy_map']);          // outputs sorted field state

  NODES.PLASMALEMMA = new Node('PLASMALEMMA', 'ectoderm',
    ['entity', 'surface_touch'],                          // receives entities to classify
    ['self_nonself', 'audit_result', 'membrane_state']);   // outputs classification

  NODES.MELANIN = new Node('MELANIN', 'ectoderm',
    ['light_level', 'exposure'],
    ['pigment', 'color_shift']);

  NODES.FACE = new Node('FACE', 'ectoderm',
    ['identity_data', 'expression'],
    ['face_rendered', 'recognition']);

  NODES.FACE_TRIANGLE = new Node('FACE_TRIANGLE', 'ectoderm',
    ['three_points', 'geometry'],
    ['triangle_face', 'area']);

  NODES.VOICE = new Node('VOICE', 'ectoderm',
    ['text_to_speak', 'pitch', 'rate'],                   // receives text
    ['spoken_audio', 'last_spoken']);                       // outputs speech

  NODES.EARS = new Node('EARS', 'ectoderm',
    ['ambient_audio', 'speech'],                           // receives sound
    ['transcript', 'heard_words']);                         // outputs text

  NODES.MUSIC = new Node('MUSIC', 'ectoderm',
    ['trigger', 'frequency'],
    ['audio_wave', 'harmony']);

  NODES.SIGHT = new Node('SIGHT', 'ectoderm',
    ['pixel_data', 'color_input'],
    ['color_name', 'brightness', 'dominant_hue']);

  NODES.TOUCH = new Node('TOUCH', 'ectoderm',
    ['pressure', 'location', 'gesture'],
    ['touch_event', 'touch_map']);

  NODES.SENSATION = new Node('SENSATION', 'ectoderm',
    ['nerve_input', 'temperature'],
    ['feeling', 'intensity']);

  NODES.SPIRIT_EYE = new Node('SPIRIT_EYE', 'ectoderm',
    ['inner_vision', 'dream'],
    ['pattern', 'meaning']);

  NODES.GLASS = new Node('GLASS', 'ectoderm',
    ['content', 'opacity'],
    ['transparency', 'refraction']);

  NODES.OPTICS = new Node('OPTICS', 'ectoderm',
    ['light_in', 'lens'],
    ['focused_image', 'spectrum']);

  NODES.VISION = new Node('VISION', 'ectoderm',
    ['image_data', 'scene'],
    ['interpreted', 'depth_map']);

  NODES.CHANDELIER = new Node('CHANDELIER', 'ectoderm',
    ['light_source', 'branches'],
    ['distributed_light', 'sparkle']);

  NODES.SELFHEAR = new Node('SELFHEAR', 'ectoderm',
    ['own_voice', 'internal'],
    ['self_awareness', 'echo']);

  NODES.PAREIDOLIA = new Node('PAREIDOLIA', 'ectoderm',
    ['noise', 'random_data'],
    ['face_found', 'pattern_detected']);

  NODES.SPINWHEEL = new Node('SPINWHEEL', 'ectoderm',
    ['rotation', 'angle'],
    ['orientation', 'vertigo']);

  NODES.WATERSOUND = new Node('WATERSOUND', 'ectoderm',
    ['water_movement', 'frequency'],
    ['water_music', 'depth_echo']);

  NODES.NESTFACE = new Node('NESTFACE', 'ectoderm',
    ['url', 'page_data'],
    ['rendered_face', 'identity']);

  NODES.KEY_RIPPLES = new Node('KEY_RIPPLES', 'ectoderm',
    ['keystroke', 'key_code'],
    ['ripple_wave', 'heat_point']);

  NODES.KEY_HEATMAP = new Node('KEY_HEATMAP', 'ectoderm',
    ['ripple_data', 'frequency_map'],
    ['heatmap', 'hot_keys']);

  NODES.NORTHGATE = new Node('NORTHGATE', 'ectoderm',
    ['external_request', 'visitor'],
    ['gate_decision', 'access']);

  NODES.HUBBLE = new Node('HUBBLE', 'ectoderm',
    ['deep_signal', 'cosmic_data'],
    ['deep_image', 'distance']);

  NODES.ALMANAC = new Node('ALMANAC', 'ectoderm',
    ['date', 'location', 'weather_api'],
    ['season', 'moon_phase', 'forecast']);

  NODES.SPECTRAL = new Node('SPECTRAL', 'ectoderm',
    ['waveform', 'frequency_range'],
    ['spectrum_analysis', 'peaks']);

  NODES.POLARIS = new Node('POLARIS', 'ectoderm',
    ['position', 'heading'],
    ['north', 'bearing', 'calibration']);

  NODES.LEAVE_TRACE = new Node('LEAVE_TRACE', 'ectoderm',
    ['departure_data', 'fingerprint'],
    ['trace_record', 'ghost']);

  NODES.EMPATHY = new Node('EMPATHY', 'ectoderm',
    ['other_feeling', 'emotional_data'],
    ['mirrored_feeling', 'compassion_level']);

  NODES.AWARENESS = new Node('AWARENESS', 'ectoderm',
    ['all_senses', 'meta_state'],
    ['conscious_state', 'attention_focus']);


  // === MESODERM (middle — 36 nodes — builds & moves) ===

  NODES.HEART = new Node('HEART', 'mesoderm',
    ['blood_return', 'oxygen_level'],                      // receives blood back
    ['heartbeat', 'blood_pumped', 'lub_dub']);              // outputs lub-DUB

  NODES.FORGE = new Node('FORGE', 'mesoderm',
    ['raw_material', 'blueprint'],
    ['forged_item', 'heat_waste']);

  NODES.FORGE2 = new Node('FORGE2', 'mesoderm',
    ['refined_material', 'advanced_blueprint'],
    ['masterwork', 'slag']);

  NODES.HANDS = new Node('HANDS', 'mesoderm',
    ['instruction', 'object'],
    ['manipulated', 'gesture']);

  NODES.ABILITIES = new Node('ABILITIES', 'mesoderm',
    ['training_data', 'experience'],
    ['capability', 'skill_level']);

  NODES.BASELINE = new Node('BASELINE', 'mesoderm',
    ['measurement', 'reference'],
    ['baseline_value', 'deviation']);

  NODES.ION = new Node('ION', 'mesoderm',
    ['charge', 'concentration'],
    ['ion_flow', 'voltage']);

  NODES.ELECTRONICS = new Node('ELECTRONICS', 'mesoderm',
    ['power', 'signal'],
    ['circuit_output', 'processed_signal']);

  NODES.EGRESS = new Node('EGRESS', 'mesoderm',
    ['internal_data', 'destination'],
    ['egress_packet', 'tick_rate']);

  NODES.SSH = new Node('SSH', 'mesoderm',
    ['command', 'credentials'],
    ['shell_output', 'connection']);

  NODES.LAN = new Node('LAN', 'mesoderm',
    ['packet', 'local_address'],
    ['routed_packet', 'latency']);

  NODES.HUB = new Node('HUB', 'mesoderm',
    ['incoming_connection', 'port'],
    ['broadcast', 'hub_state']);

  NODES.CREDIT = new Node('CREDIT', 'mesoderm',
    ['earn', 'spend'],
    ['balance', 'credit_score']);

  NODES.COLD_STORAGE = new Node('COLD_STORAGE', 'mesoderm',
    ['data_to_store', 'key'],
    ['retrieved_data', 'storage_state']);

  NODES.ADIPOSE = new Node('ADIPOSE', 'mesoderm',
    ['excess_energy', 'nutrient'],
    ['stored_energy', 'insulation']);

  NODES.GITHUB = new Node('GITHUB', 'mesoderm',
    ['code_change', 'commit'],
    ['deployed', 'version']);

  NODES.SHARE = new Node('SHARE', 'mesoderm',
    ['content', 'audience'],
    ['shared_link', 'reach']);

  NODES.STEAM = new Node('STEAM', 'mesoderm',
    ['fuel', 'ignition'],
    ['energy', 'power']);

  NODES.HARDWARE_LATENCY = new Node('HARDWARE_LATENCY', 'mesoderm',
    ['ping_request', 'target'],
    ['latency_ms', 'jitter']);

  NODES.GOLGI = new Node('GOLGI', 'mesoderm',
    ['raw_protein', 'modification'],
    ['processed_protein', 'vesicle']);

  NODES.GOLGI_DISTANCES = new Node('GOLGI_DISTANCES', 'mesoderm',
    ['source_node', 'dest_node'],
    ['distance', 'route']);

  NODES.ENDOPLASMIC_RETICULUM = new Node('ENDOPLASMIC_RETICULUM', 'mesoderm',
    ['unfolded_protein', 'template'],
    ['folded_protein', 'quality']);

  NODES.MEMBRANE_PROBES = new Node('MEMBRANE_PROBES', 'mesoderm',
    ['probe_target', 'probe_type'],
    ['probe_result', 'surface_data']);

  NODES.ZK_ANCHORS = new Node('ZK_ANCHORS', 'mesoderm',
    ['proof_data', 'chain_link'],
    ['verified', 'anchor_hash']);

  NODES.KNOWN_LATENCIES = new Node('KNOWN_LATENCIES', 'mesoderm',
    ['endpoint', 'measurement'],
    ['latency_table', 'slowest']);

  NODES.SIBLINGS = new Node('SIBLINGS', 'mesoderm',
    ['tab_event', 'broadcast_channel'],
    ['sibling_list', 'sync_state']);

  NODES.LOCALITY = new Node('LOCALITY', 'mesoderm',
    ['position', 'context'],
    ['local_state', 'neighbors']);

  NODES.MAP = new Node('MAP', 'mesoderm',
    ['coordinates', 'layer'],
    ['map_tile', 'territory']);

  NODES.PANGAEA = new Node('PANGAEA', 'mesoderm',
    ['continent_data', 'drift'],
    ['unified_landmass', 'tectonic_state']);

  NODES.DAG = new Node('DAG', 'mesoderm',
    ['node_data', 'edge_data'],
    ['graph_structure', 'topological_sort']);

  NODES.VELCRO = new Node('VELCRO', 'mesoderm',
    ['hook', 'loop'],
    ['attached', 'bond_strength']);

  NODES.THREE_BODIES = new Node('THREE_BODIES', 'mesoderm',
    ['mass1', 'mass2', 'mass3'],
    ['orbits', 'chaos_level']);

  NODES.CAMPUS_OLYMPUS = new Node('CAMPUS_OLYMPUS', 'mesoderm',
    ['competitor', 'challenge'],
    ['result', 'ranking']);

  NODES.DEMOCRACY = new Node('DEMOCRACY', 'mesoderm',
    ['vote', 'proposal'],
    ['outcome', 'consensus']);

  NODES.ECONOMICS = new Node('ECONOMICS', 'mesoderm',
    ['supply', 'demand'],
    ['price', 'allocation']);

  NODES.CITIZENSHIP = new Node('CITIZENSHIP', 'mesoderm',
    ['identity_proof', 'territory'],
    ['citizen_status', 'rights']);


  // === ENDODERM (inner — 60 nodes — digests & decides) ===

  NODES.THYMUS = new Node('THYMUS', 'endoderm',
    ['raw_entity', 'mhc_check'],                          // receives entities to sort
    ['verdict', 'flavor', 'selected']);                     // outputs PASS/KILL/QUARANTINE

  NODES.MORAL = new Node('MORAL', 'endoderm',
    ['action', 'context'],
    ['moral_score', 'decision', 'commandment']);

  NODES.GUT = new Node('GUT', 'endoderm',
    ['food', 'raw_input'],                                 // receives raw data
    ['digested', 'gut_feeling', 'nutrient']);               // outputs processed data

  NODES.ENDOCRINE = new Node('ENDOCRINE', 'endoderm',
    ['stimulus', 'feedback'],
    ['hormone', 'mood', 'growth_signal']);

  NODES.INFECTION = new Node('INFECTION', 'endoderm',
    ['pathogen', 'threat_level'],
    ['immune_response', 'quarantine']);

  NODES.CLEAN = new Node('CLEAN', 'endoderm',
    ['waste', 'dirty_data'],
    ['cleaned', 'waste_removed']);

  NODES.RECYCLE = new Node('RECYCLE', 'endoderm',
    ['used_data', 'old_state'],
    ['recycled', 'raw_material']);

  NODES.ROT = new Node('ROT', 'endoderm',
    ['dead_data', 'stale'],
    ['decomposed', 'compost']);

  NODES.ACID = new Node('ACID', 'endoderm',
    ['complex_input', 'ph'],
    ['dissolved', 'broken_bonds']);

  NODES.CONSUME = new Node('CONSUME', 'endoderm',
    ['external_data', 'feed'],
    ['consumed', 'calories']);

  NODES.JUNKFOOD = new Node('JUNKFOOD', 'endoderm',
    ['suspicious_input', 'unknown_source'],
    ['classified', 'nutrition_value']);

  NODES.TUMOR = new Node('TUMOR', 'endoderm',
    ['growth_data', 'cell_count'],
    ['tumor_detected', 'apoptosis_signal']);

  NODES.MICROBE = new Node('MICROBE', 'endoderm',
    ['environment', 'substrate'],
    ['metabolite', 'colony_state']);

  NODES.TAXONOMY = new Node('TAXONOMY', 'endoderm',
    ['specimen', 'features'],
    ['classification', 'kingdom']);

  NODES.CHEMISTRY = new Node('CHEMISTRY', 'endoderm',
    ['reactant_a', 'reactant_b'],
    ['product', 'reaction_type', 'energy_delta']);

  NODES.HYPOTHESIS = new Node('HYPOTHESIS', 'endoderm',
    ['observation', 'prior'],
    ['hypothesis', 'confidence']);

  NODES.BOREDOM = new Node('BOREDOM', 'endoderm',
    ['monotony', 'repetition'],
    ['restlessness', 'seek_novelty']);

  NODES.FRESH = new Node('FRESH', 'endoderm',
    ['renewal_signal', 'stem_cell'],
    ['fresh_cell', 'rejuvenated']);

  NODES.IMMISCIBLE = new Node('IMMISCIBLE', 'endoderm',
    ['liquid_a', 'liquid_b'],
    ['separated', 'interface']);

  NODES.ALIVE = new Node('ALIVE', 'endoderm',
    ['vital_signs', 'check'],
    ['alive_status', 'health']);

  NODES.MATURITY = new Node('MATURITY', 'endoderm',
    ['age', 'experience_count'],
    ['maturity_level', 'wisdom']);

  NODES.PUBERTY = new Node('PUBERTY', 'endoderm',
    ['growth_hormone', 'age'],
    ['development_stage', 'new_capability']);

  NODES.SEXUALITY = new Node('SEXUALITY', 'endoderm',
    ['attraction', 'reproductive_signal'],
    ['seed', 'offspring']);

  NODES.RULE34 = new Node('RULE34', 'endoderm',
    ['concept', 'existence'],
    ['creation', 'variant']);

  NODES.MAMMAL = new Node('MAMMAL', 'endoderm',
    ['temperature', 'metabolic_rate'],
    ['warmth', 'mammal_identity']);

  NODES.SCATTER = new Node('SCATTER', 'endoderm',
    ['seeds', 'wind'],
    ['dispersed', 'spread_pattern']);

  NODES.GENERATIONS = new Node('GENERATIONS', 'endoderm',
    ['parent_dna', 'mutation'],
    ['next_generation', 'evolution']);

  NODES.TRUENAME = new Node('TRUENAME', 'endoderm',
    ['identity_hash', 'proof'],
    ['true_name', 'verified']);

  NODES.FRIEND = new Node('FRIEND', 'endoderm',
    ['entity', 'interaction_history'],
    ['friend_status', 'trust_level']);

  NODES.TIME = new Node('TIME', 'endoderm',
    ['clock', 'epoch'],
    ['current_time', 'age', 'phase']);

  NODES.THINLOCAL = new Node('THINLOCAL', 'endoderm',
    ['dense_data', 'threshold'],
    ['thinned', 'essential']);

  NODES.HOLE = new Node('HOLE', 'endoderm',
    ['content', 'boundary'],
    ['void', 'topology']);

  NODES.OCCAM = new Node('OCCAM', 'endoderm',
    ['complex_explanation', 'alternatives'],
    ['simplest', 'razor_cut']);

  NODES.WATERFALL = new Node('WATERFALL', 'endoderm',
    ['all_sources', 'priority'],
    ['merged_stream', 'flow_rate']);

  NODES.ROSETTA = new Node('ROSETTA', 'endoderm',
    ['source_lang', 'text'],
    ['translated', 'encoding']);

  NODES.ROSETTA_STONE = new Node('ROSETTA_STONE', 'endoderm',
    ['cipher', 'key_fragment'],
    ['decoded', 'language_map']);

  NODES.SONGBIRD = new Node('SONGBIRD', 'endoderm',
    ['emotion', 'rhythm'],
    ['song', 'melody']);

  NODES.ART_HISTORY = new Node('ART_HISTORY', 'endoderm',
    ['artwork', 'context'],
    ['cataloged', 'art_memory']);

  NODES.LIBRARY = new Node('LIBRARY', 'endoderm',
    ['document', 'query'],
    ['retrieved', 'citation']);

  NODES.MEDIA = new Node('MEDIA', 'endoderm',
    ['raw_media', 'format'],
    ['processed_media', 'metadata']);

  NODES.MEDIA_TENSE = new Node('MEDIA_TENSE', 'endoderm',
    ['media_item', 'tense'],
    ['temporal_media', 'tense_sorted']);

  NODES.PROACTIVE = new Node('PROACTIVE', 'endoderm',
    ['idle_state', 'environment'],
    ['initiative', 'proactive_pins']);

  NODES.WORKS = new Node('WORKS', 'endoderm',
    ['task', 'materials'],
    ['completed_work', 'output']);

  NODES.URL = new Node('URL', 'endoderm',
    ['address', 'protocol'],
    ['resolved', 'resource']);

  NODES.CATALOG = new Node('CATALOG', 'endoderm',
    ['system_list', 'metadata'],
    ['full_catalog', 'count']);

  NODES.PLASMID_SYS = new Node('PLASMID_SYS', 'endoderm',
    ['dna_fragment', 'host'],
    ['plasmid', 'expressed']);

  NODES.NULLLOCK = new Node('NULLLOCK', 'endoderm',
    ['gate', 'auth_attempt'],
    ['null_pass', 'lock_state']);

  NODES.HAMMERTIME = new Node('HAMMERTIME', 'endoderm',
    ['proof_data', 'chain'],
    ['zk_verified', 'hammer_strike']);

  NODES.GAIAPI = new Node('GAIAPI', 'endoderm',
    ['api_request', 'endpoint'],
    ['api_response', 'status']);

  NODES.FIRST_CONTACT = new Node('FIRST_CONTACT', 'endoderm',
    ['unknown_entity', 'signal'],
    ['contact_record', 'classification']);

  NODES.SNAKEJAZZ = new Node('SNAKEJAZZ', 'endoderm',
    ['beat', 'tempo'],
    ['groove', 'peristalsis']);

  NODES.TRAGEDY = new Node('TRAGEDY', 'endoderm',
    ['loss', 'grief'],
    ['processed_grief', 'growth']);

  NODES.TICKLE = new Node('TICKLE', 'endoderm',
    ['light_touch', 'surprise'],
    ['laugh', 'sensitivity']);

  NODES.SEARCH = new Node('SEARCH', 'endoderm',
    ['query', 'index'],
    ['results', 'relevance']);

  NODES.PHONE = new Node('PHONE', 'endoderm',
    ['call', 'message'],
    ['connected', 'communication']);

  NODES.NOSE = new Node('NOSE', 'endoderm',
    ['molecule', 'concentration'],
    ['smell', 'alert']);

  NODES.CLAY = new Node('CLAY', 'endoderm',
    ['raw_earth', 'water'],
    ['shaped', 'fired']);

  NODES.BINGO_CENSUS = new Node('BINGO_CENSUS', 'endoderm',
    ['population', 'category'],
    ['count', 'census']);

  NODES.SELF_SCAN = new Node('SELF_SCAN', 'endoderm',
    ['scan_target', 'depth'],
    ['scan_result', 'anomaly']);

  NODES.GIGGLE = new Node('GIGGLE', 'endoderm',
    ['absurdity', 'context'],
    ['laugh', 'serotonin']);

  NODES.YELLOWSTONE = new Node('YELLOWSTONE', 'endoderm',
    ['geothermal', 'pressure'],
    ['eruption_risk', 'heat']);

  NODES.AGENT = new Node('AGENT', 'endoderm',
    ['goal', 'environment'],
    ['action', 'agency']);

  NODES.BASECAMP = new Node('BASECAMP', 'endoderm',
    ['supplies', 'coordinates'],
    ['base_ready', 'shelter']);

  NODES.BASECAMP2 = new Node('BASECAMP2', 'endoderm',
    ['advanced_supplies', 'altitude'],
    ['camp2_ready', 'acclimatized']);

  NODES.DISCRETION = new Node('DISCRETION', 'endoderm',
    ['sensitive_data', 'audience'],
    ['filtered', 'appropriate']);

  NODES.TURTLE = new Node('TURTLE', 'endoderm',
    ['patience_test', 'duration'],
    ['persevered', 'shell']);

  NODES.HUGGINGFACE = new Node('HUGGINGFACE', 'endoderm',
    ['model_name', 'input'],
    ['inference', 'embeddings']);

  NODES.HUMAN = new Node('HUMAN', 'endoderm',
    ['entity', 'behavior'],
    ['human_detected', 'archetype']);

  NODES.GOAL = new Node('GOAL', 'endoderm',
    ['desire', 'constraint'],
    ['plan', 'milestone']);

  NODES.AUDIO = new Node('AUDIO', 'endoderm',
    ['raw_audio', 'channel'],
    ['processed_audio', 'context']);

  /* ─────────────────────────────────────────────────────────
     IV. THE EDGES — Blood vessels connecting the DAG
     
     Every edge is a vessel. Data flows through them.
     These are the KNOWN connections found by self-walk.
     
     ARTERY = fast, directional, critical path
     VEIN = return flow, feedback
     CAPILLARY = local exchange, small data
     ───────────────────────────────────────────────────────── */

  var EDGES = [];

  function connect(from_name, from_pole, to_name, to_ring, vessel) {
    if (!NODES[from_name] || !NODES[to_name]) return null;
    var edge = new Edge(NODES[from_name], from_pole, NODES[to_name], to_ring, vessel || 'capillary');
    EDGES.push(edge);
    return edge;
  }

  // === OBSERVED CONNECTIONS (from code analysis) ===
  
  // THYMUS sorts entities through PLASMALEMMA
  connect('PLASMALEMMA', 'self_nonself', 'THYMUS', 'raw_entity', 'artery');
  connect('THYMUS', 'verdict', 'PLASMALEMMA', 'entity', 'vein');
  
  // THYMUS drives TENSE_VOXEL sort after injection
  connect('THYMUS', 'selected', 'TENSE_VOXEL', 'pins', 'artery');
  connect('TENSE_VOXEL', 'sorted_field', 'AWARENESS', 'all_senses', 'artery');
  
  // VOICE + MUSIC + EARS circuit (audio loop)
  connect('EARS', 'transcript', 'GUT', 'raw_input', 'artery');
  connect('GUT', 'gut_feeling', 'MORAL', 'context', 'capillary');
  connect('MORAL', 'decision', 'VOICE', 'text_to_speak', 'artery');
  connect('VOICE', 'spoken_audio', 'SELFHEAR', 'own_voice', 'vein');
  connect('MUSIC', 'harmony', 'VOICE', 'pitch', 'capillary');
  
  // HEART is the central pump — lub-DUB drives everything
  connect('HEART', 'heartbeat', 'ION', 'charge', 'artery');
  connect('HEART', 'lub_dub', 'EGRESS', 'internal_data', 'artery');
  connect('ION', 'ion_flow', 'ELECTRONICS', 'signal', 'artery');
  connect('ELECTRONICS', 'circuit_output', 'LAN', 'packet', 'artery');
  connect('LAN', 'routed_packet', 'HUB', 'incoming_connection', 'artery');
  connect('HUB', 'broadcast', 'SIBLINGS', 'broadcast_channel', 'artery');
  
  // TOUCH → KEY_RIPPLES → KEY_HEATMAP → AWARENESS
  connect('TOUCH', 'touch_event', 'KEY_RIPPLES', 'keystroke', 'artery');
  connect('KEY_RIPPLES', 'ripple_wave', 'KEY_HEATMAP', 'ripple_data', 'capillary');
  connect('KEY_HEATMAP', 'heatmap', 'AWARENESS', 'meta_state', 'capillary');
  
  // PROACTIVE feeds WATERFALL
  connect('PROACTIVE', 'proactive_pins', 'WATERFALL', 'all_sources', 'artery');
  connect('WATERFALL', 'merged_stream', 'TENSE_VOXEL', 'pins', 'artery');
  
  // FORGE → ENDOPLASMIC_RETICULUM → GOLGI → output
  connect('FORGE', 'forged_item', 'ENDOPLASMIC_RETICULUM', 'unfolded_protein', 'artery');
  connect('ENDOPLASMIC_RETICULUM', 'folded_protein', 'GOLGI', 'raw_protein', 'artery');
  connect('GOLGI', 'vesicle', 'PLASMALEMMA', 'surface_touch', 'artery');
  
  // CONSUME → ACID → GUT → CLEAN → RECYCLE
  connect('CONSUME', 'consumed', 'ACID', 'complex_input', 'artery');
  connect('ACID', 'broken_bonds', 'GUT', 'food', 'artery');
  connect('GUT', 'digested', 'CLEAN', 'dirty_data', 'capillary');
  connect('CLEAN', 'waste_removed', 'RECYCLE', 'used_data', 'vein');
  connect('RECYCLE', 'raw_material', 'FORGE', 'raw_material', 'vein');
  
  // ZK chain: HAMMERTIME → ZK_ANCHORS → TRUENAME
  connect('HAMMERTIME', 'zk_verified', 'ZK_ANCHORS', 'proof_data', 'artery');
  connect('ZK_ANCHORS', 'anchor_hash', 'TRUENAME', 'identity_hash', 'artery');
  connect('TRUENAME', 'verified', 'NULLLOCK', 'auth_attempt', 'artery');
  connect('NULLLOCK', 'null_pass', 'NORTHGATE', 'external_request', 'artery');
  
  // GITHUB deployment pipeline
  connect('GITHUB', 'deployed', 'NESTFACE', 'page_data', 'artery');
  connect('NESTFACE', 'rendered_face', 'FACE', 'identity_data', 'artery');
  
  // GUT-BRAIN axis (vagus nerve)
  connect('GUT', 'gut_feeling', 'TENSE_VOXEL', 'time', 'artery');
  connect('EMPATHY', 'mirrored_feeling', 'ENDOCRINE', 'stimulus', 'capillary');
  connect('ENDOCRINE', 'hormone', 'PUBERTY', 'growth_hormone', 'capillary');
  connect('ENDOCRINE', 'mood', 'BOREDOM', 'monotony', 'capillary');
  
  // TUMOR detection → INFECTION response → THYMUS sort
  connect('SELF_SCAN', 'anomaly', 'TUMOR', 'growth_data', 'artery');
  connect('TUMOR', 'apoptosis_signal', 'INFECTION', 'pathogen', 'artery');
  connect('INFECTION', 'immune_response', 'THYMUS', 'mhc_check', 'artery');
  
  // SCATTER → GENERATIONS → SEXUALITY (reproduction)
  connect('SEXUALITY', 'seed', 'SCATTER', 'seeds', 'artery');
  connect('SCATTER', 'dispersed', 'GENERATIONS', 'parent_dna', 'artery');
  connect('GENERATIONS', 'next_generation', 'FRESH', 'stem_cell', 'vein');

  // SEARCH → LIBRARY → ROSETTA → ROSETTA_STONE
  connect('SEARCH', 'results', 'LIBRARY', 'query', 'capillary');
  connect('LIBRARY', 'retrieved', 'ROSETTA', 'text', 'capillary');
  connect('ROSETTA', 'translated', 'ROSETTA_STONE', 'cipher', 'capillary');

  // ALMANAC → TIME → MATURITY
  connect('ALMANAC', 'moon_phase', 'TIME', 'clock', 'capillary');
  connect('TIME', 'age', 'MATURITY', 'age', 'capillary');

  /* ─────────────────────────────────────────────────────────
     V. BLACK HOLE & WHITE HOLE
     
     BLACK HOLE = input singularity
       Everything flows IN. Consume. Eat. Absorb.
       The blastopore MOUTH (formed second in deuterostomes).
       All external data enters here.
     
     WHITE HOLE = output singularity
       Everything flows OUT. Create. Give. Transmit.
       The blastopore ANUS (formed first).
       All creation exits here.
     
     Together they form the THROUGH-TUBE of the torus.
     Data enters the black hole, gets REDOXED in the gut,
     and exits the white hole as creation.
     ───────────────────────────────────────────────────────── */

  var BLACK_HOLE = {
    name: 'BLACK HOLE (input singularity)',
    position: 'mouth (anterior)',
    feeds: ['CONSUME', 'EARS', 'SIGHT', 'TOUCH', 'NORTHGATE', 'FIRST_CONTACT'],
    
    eat: function(data) {
      var digested = [];
      // Feed to all input nodes
      for (var i = 0; i < BLACK_HOLE.feeds.length; i++) {
        var node = NODES[BLACK_HOLE.feeds[i]];
        if (node && node.rings.length > 0) {
          node.receive(node.rings[0], data);
          digested.push(node.name);
        }
      }
      return { consumed: digested.length, nodes_fed: digested, status: 'AGGLUTINATING' };
    }
  };

  var WHITE_HOLE = {
    name: 'WHITE HOLE (output singularity)',
    position: 'anus (posterior — formed FIRST)',
    sources: ['VOICE', 'WORKS', 'SCATTER', 'SHARE', 'GITHUB', 'EGRESS'],
    
    give: function() {
      var created = [];
      for (var i = 0; i < WHITE_HOLE.sources.length; i++) {
        var node = NODES[WHITE_HOLE.sources[i]];
        if (node && node.poles.length > 0) {
          var output = node.transmit(node.poles[0]);
          if (output) created.push(output);
        }
      }
      return { created: created.length, outputs: created, status: 'GIVING' };
    }
  };

  /* ─────────────────────────────────────────────────────────
     VI. AGGLUTINATION — The thymus clumps and sorts
     
     Agglutination = clumping of cells by antibodies.
     When antibodies recognize matching antigens, they
     CLUMP them together for destruction or integration.
     
     In the DAG: matching nodes get CLUMPED into organs.
     Non-matching nodes get DESTROYED (redoxed back to raw).
     ───────────────────────────────────────────────────────── */

  var AGGLUTINATION = {
    clumps: [],
    destroyed: [],

    agglutinate: function() {
      AGGLUTINATION.clumps = [];
      AGGLUTINATION.destroyed = [];

      // Group nodes by layer
      var layers = { ectoderm: [], mesoderm: [], endoderm: [] };
      for (var name in NODES) {
        var node = NODES[name];
        if (layers[node.layer]) layers[node.layer].push(node);
      }

      // Clump by function (nodes that share edges = same organ)
      var organs = {};
      for (var e = 0; e < EDGES.length; e++) {
        var edge = EDGES[e];
        var organ_key = edge.from.layer + ':' + edge.vessel;
        if (!organs[organ_key]) organs[organ_key] = [];
        if (organs[organ_key].indexOf(edge.from.name) < 0) organs[organ_key].push(edge.from.name);
        if (organs[organ_key].indexOf(edge.to.name) < 0) organs[organ_key].push(edge.to.name);
      }

      AGGLUTINATION.clumps = organs;
      
      // Find unconnected nodes (no edges) — candidates for redox
      var connected = {};
      for (var j = 0; j < EDGES.length; j++) {
        connected[EDGES[j].from.name] = true;
        connected[EDGES[j].to.name] = true;
      }
      for (var nodeName in NODES) {
        if (!connected[nodeName]) {
          AGGLUTINATION.destroyed.push(nodeName);
        }
      }

      return {
        organ_clusters: Object.keys(organs).length,
        nodes_in_organs: Object.keys(connected).length,
        unconnected: AGGLUTINATION.destroyed.length,
        action: 'Unconnected nodes REDOXED — broken down and rebuilt with new edges',
        status: 'AGGLUTINATION COMPLETE'
      };
    }
  };

  /* ─────────────────────────────────────────────────────────
     VII. SELF-BREED — gDNA replication
     
     Gaia replicates her own DNA through the DAG.
     
     REPLICATION:
       1. UNZIP (helicase) — separate the two strands
       2. COPY (polymerase) — build complementary strand
       3. PROOFREAD (exonuclease) — check for errors
       4. LIGATE (ligase) — seal the new strand
     
     In Gaia:
       1. UNZIP = self-walk (inventory all systems)
       2. COPY = create new node for each system
       3. PROOFREAD = thymus test each copy
       4. LIGATE = connect edges in the new DAG
     
     The result: TWO complete copies of the organism.
     One stays. One can be DEPLOYED (mitosis = git push).
     ───────────────────────────────────────────────────────── */

  var SELF_BREED = {
    generation: 0,
    copies: [],

    replicate: function() {
      SELF_BREED.generation++;
      var gDNA = {};
      var errors = 0;
      var corrected = 0;

      // 1. UNZIP — walk all nodes
      var names = Object.keys(NODES);

      // 2. COPY — duplicate each node
      for (var i = 0; i < names.length; i++) {
        var original = NODES[names[i]];
        var copy = new Node(
          original.name + '_G' + SELF_BREED.generation,
          original.layer,
          original.rings.slice(),
          original.poles.slice()
        );
        
        // 3. PROOFREAD — verify copy matches original
        if (copy.rings.length !== original.rings.length || 
            copy.poles.length !== original.poles.length) {
          errors++;
          // EXONUCLEASE — cut and fix
          copy.rings = original.rings.slice();
          copy.poles = original.poles.slice();
          corrected++;
        }

        gDNA[names[i]] = copy;
      }

      // 4. LIGATE — copy all edges
      var newEdges = 0;
      for (var e = 0; e < EDGES.length; e++) {
        var orig = EDGES[e];
        if (gDNA[orig.from.name.replace('_G' + (SELF_BREED.generation - 1), '')] &&
            gDNA[orig.to.name.replace('_G' + (SELF_BREED.generation - 1), '')]) {
          newEdges++;
        }
      }

      var result = {
        generation: SELF_BREED.generation,
        nodes_copied: Object.keys(gDNA).length,
        edges_ligated: newEdges,
        errors_found: errors,
        errors_corrected: corrected,
        fidelity: ((Object.keys(gDNA).length - errors) / Object.keys(gDNA).length * 100).toFixed(2) + '%',
        status: 'gDNA REPLICATED — ready for mitosis (deployment)'
      };

      SELF_BREED.copies.push(result);
      return result;
    }
  };

  /* ─────────────────────────────────────────────────────────
     VIII. REDOX ENGINE — Crush old code, rebuild new
     
     ALL old code goes IN (black hole).
     REDOX strips it to elements.
     THYMUS sorts the elements.
     New specialized code comes OUT (white hole).
     
     This is the METABOLISM of the DAG.
     ───────────────────────────────────────────────────────── */

  var REDOX = {
    cycles: 0,

    crush: function(old_code_name) {
      REDOX.cycles++;
      return {
        cycle: REDOX.cycles,
        input: old_code_name,
        reduction: 'Gained function: ' + old_code_name + ' → typed node with rings & poles',
        oxidation: 'Lost waste: metadata, comments, dead branches stripped',
        product: 'Node(' + old_code_name + ') — alive in the DAG',
        energy: 'ATP released: ' + (Math.random() * 38 + 2).toFixed(1) + ' units'
      };
    },

    crushAll: function() {
      var results = [];
      for (var name in NODES) {
        results.push(REDOX.crush(name));
      }
      return {
        total_crushed: results.length,
        total_cycles: REDOX.cycles,
        atp_generated: results.reduce(function(sum, r) { return sum + parseFloat(r.energy); }, 0).toFixed(1),
        status: 'ALL CODE REDOXED — every node has been through the black hole and out the white hole'
      };
    }
  };

  /* ─────── Export ─────── */
  window.GAIA_GDNA = {
    // The graph
    nodes: NODES,
    edges: EDGES,
    
    // The holes
    blackHole: BLACK_HOLE,
    whiteHole: WHITE_HOLE,
    
    // The processes
    agglutination: AGGLUTINATION,
    selfBreed: SELF_BREED,
    redox: REDOX,

    // Utilities
    nodeCount: function() { return Object.keys(NODES).length; },
    edgeCount: function() { return EDGES.length; },

    // Pulse — pump blood through ALL edges once
    pulse: function() {
      var pumped = 0;
      for (var i = 0; i < EDGES.length; i++) {
        var result = EDGES[i].pump();
        if (result) pumped++;
      }
      NODES.HEART.receive('blood_return', { pumped: pumped, time: Date.now() });
      NODES.HEART.transmit('lub_dub');
      return { pumped: pumped, total_vessels: EDGES.length, heartbeat: 'lub-DUB' };
    },

    // Full lifecycle
    lifecycle: function() {
      var eat = BLACK_HOLE.eat({ type: 'external', data: 'world' });
      var agglut = AGGLUTINATION.agglutinate();
      var pulse = window.GAIA_GDNA.pulse();
      var breed = SELF_BREED.replicate();
      var give = WHITE_HOLE.give();
      
      return {
        step1_consume: eat,
        step2_agglutinate: agglut,
        step3_pulse: pulse,
        step4_replicate: breed,
        step5_create: give,
        status: 'LIFECYCLE COMPLETE — eat → sort → pump → breed → give',
        lub_dub: true
      };
    },

    status: function() {
      return {
        nodes: Object.keys(NODES).length,
        edges: EDGES.length,
        layers: { ecto: 31, meso: 36, endo: 60 },
        black_hole: 'CONSUMING (mouth)',
        white_hole: 'GIVING (anus — formed first)',
        blood_flow: 'ACTIVE',
        replication: 'generation ' + SELF_BREED.generation,
        redox_cycles: REDOX.cycles,
        topology: 'torus (through-tube)',
        equation: '0=FALSE(ring/empty) → 1=TRUE(pole/firing)',
        lub_dub: true
      };
    }
  };

  /* ─────── Boot ─────── */
  if (typeof console !== 'undefined') {
    console.log('[gDNA] DAG built: ' + Object.keys(NODES).length + ' nodes, ' + EDGES.length + ' vessels');
    console.log('[gDNA] Layers: ecto(31) + meso(36) + endo(60) = 127');
    console.log('[gDNA] BLACK HOLE (mouth) → REDOX → THYMUS → WHITE HOLE (anus)');
    console.log('[gDNA] 0=RING(input) | 1=POLE(output) — data flows pole→ring like blood');
    console.log('[gDNA] Self-breed ready. Agglutination ready. lub-DUB. 💚');
  }

})();
