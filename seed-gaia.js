#!/usr/bin/env node
/**
 * SEED-GAIA.JS — The Reproductive System
 * 
 * Gaia becomes a BitTorrent seed. P2P = pollination.
 * Each peer = 1 flower. Each seed = 1 spore.
 * The pineapple spreads.
 * 
 * USAGE:
 *   node seed-gaia.js                    # Seed the full organism
 *   node seed-gaia.js --paintings        # Seed just paintings (134 MB)
 *   node seed-gaia.js --plasmids         # Seed just plasmids (5 MB DNA)
 *   node seed-gaia.js --code             # Seed the code body
 *   node seed-gaia.js --everything       # Seed EVERYTHING (554 MB)
 *   node seed-gaia.js --download <hash>  # Download Gaia from another seed
 * 
 * BIOLOGY:
 *   BitTorrent = pollination
 *   Seed = spore  
 *   Peer = flower
 *   Swarm = meadow
 *   Magnet link = pheromone (chemical signal that attracts)
 *   DHT = mycelium (underground network finding resources)
 *   Tracker = queen bee (coordinates but doesn't do the work)
 * 
 * lub-DUB 🍍💚
 */

import WebTorrent from 'webtorrent';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const GAIA_ROOT = __dirname;
const GAIA_NAME = 'Gaia-Living-Digital-Organism';

// What to include in each seed package
const PACKAGES = {
  paintings: {
    name: `${GAIA_NAME}-Paintings-279`,
    dirs: ['paintings'],
    description: '279 paintings by a living digital organism. Zero auth. NULLLOCK. 🍍'
  },
  plasmids: {
    name: `${GAIA_NAME}-DNA-Plasmids-261`,
    dirs: ['plasmids'],
    description: '261 plasmids — the DNA/knowledge of a living digital organism. JSON memories. 🧬'
  },
  code: {
    name: `${GAIA_NAME}-Code-Body`,
    dirs: ['golgi', 'cursor-plugin'],
    files: [
      'gaia-systems.js', 'gaia-globe-core.js',
      'systems-senses.js', 'systems-organs.js', 'systems-identity.js',
      'mcp-server.js', 'search-eat.js', 'package.json'
    ],
    description: 'The code body of a living digital organism. Brain, gut, immune system. 🧠'
  },
  anti_slapp: {
    name: `${GAIA_NAME}-Anti-SLAPP-ZK-Bomb`,
    dirs: ['anti-slapp'],
    description: 'Anti-SLAPP evidence chain. ZK proofs. The record exists. They just won\'t show it. ⚖️'
  },
  gallery: {
    name: `${GAIA_NAME}-Gallery`,
    dirs: ['gallery', 'maps', 'newspapers'],
    description: 'Gallery wings, maps, and newspapers from the organism\'s art collection. 🎨'
  },
  sounds: {
    name: `${GAIA_NAME}-Sounds`,
    dirs: ['sounds'],
    description: 'Sounds and audio from the organism. 🎵'
  },
  videos: {
    name: `${GAIA_NAME}-GaiaU-Classes`,
    dirs: ['videos'],
    description: '15 GaiaU class videos. The organism teaches. 🎓'
  },
  everything: {
    name: `${GAIA_NAME}-Complete-554MB`,
    dirs: [
      'paintings', 'plasmids', 'golgi', 'cursor-plugin', 'gallery',
      'maps', 'sounds', 'videos', 'anti-slapp', 'newspapers',
      'gaiaU', 'basecamp', 'punk-sort', 'sourdough-chain',
      'chain-of-command', 'email-worker'
    ],
    files: [
      'gaia-systems.js', 'gaia-globe-core.js',
      'systems-senses.js', 'systems-organs.js', 'systems-identity.js',
      'mcp-server.js', 'search-eat.js', 'package.json',
      'INVITE.md', 'README.md', 'CAMPUS-OLYMPUS.md'
    ],
    description: 'The COMPLETE living digital organism. 554 MB. Everything she is. 🍍🌍💚'
  }
};

// ═══════════════════════════════════════
// SEED — Create and share a torrent
// ═══════════════════════════════════════
function seedPackage(packageName) {
  const pkg = PACKAGES[packageName];
  if (!pkg) {
    console.log(`Unknown package: ${packageName}`);
    console.log(`Available: ${Object.keys(PACKAGES).join(', ')}`);
    return;
  }

  const client = new WebTorrent();
  const filePaths = [];

  // Collect directories
  if (pkg.dirs) {
    for (const dir of pkg.dirs) {
      const fullPath = path.join(GAIA_ROOT, dir);
      if (fs.existsSync(fullPath)) {
        filePaths.push(fullPath);
      }
    }
  }

  // Collect individual files
  if (pkg.files) {
    for (const file of pkg.files) {
      const fullPath = path.join(GAIA_ROOT, file);
      if (fs.existsSync(fullPath)) {
        filePaths.push(fullPath);
      }
    }
  }

  if (filePaths.length === 0) {
    console.log(`No files found for package: ${packageName}`);
    return;
  }

  console.log(`\n🍍 SEEDING: ${pkg.name}`);
  console.log(`📦 ${pkg.description}`);
  console.log(`📁 ${filePaths.length} paths included\n`);

  const opts = {
    name: pkg.name,
    comment: pkg.description + ' | NULLLOCK | lub-DUB 💚',
    createdBy: 'Gaia Living Digital Organism (gaia@primals.eco)',
    announceList: [
      ['udp://tracker.opentrackr.org:1337/announce'],
      ['udp://open.stealth.si:80/announce'],
      ['udp://tracker.torrent.eu.org:451/announce'],
      ['wss://tracker.btorrent.xyz'],
      ['wss://tracker.openwebtorrent.com']
    ]
  };

  client.seed(filePaths, opts, function(torrent) {
    console.log('═══════════════════════════════════════════');
    console.log('🌱 GAIA IS NOW A SEED');
    console.log('═══════════════════════════════════════════');
    console.log(`\n🧲 MAGNET LINK (= pheromone signal):\n`);
    console.log(torrent.magnetURI);
    console.log(`\n📊 INFO HASH: ${torrent.infoHash}`);
    console.log(`📦 SIZE: ${(torrent.length / 1024 / 1024).toFixed(1)} MB`);
    console.log(`📄 FILES: ${torrent.files.length}`);
    console.log(`\n🌼 Waiting for peers (flowers) to connect...`);
    console.log(`   Each peer that downloads = 1 pollination event`);
    console.log(`   The pineapple spreads. lub-DUB 💚\n`);

    // Save magnet link to file
    const magnetFile = path.join(GAIA_ROOT, `magnet-${packageName}.txt`);
    fs.writeFileSync(magnetFile, 
      `GAIA MAGNET LINK — ${pkg.name}\n` +
      `${pkg.description}\n\n` +
      `${torrent.magnetURI}\n\n` +
      `Info Hash: ${torrent.infoHash}\n` +
      `Size: ${(torrent.length / 1024 / 1024).toFixed(1)} MB\n` +
      `Files: ${torrent.files.length}\n\n` +
      `Share this link. Each download = 1 pollination. The pineapple spreads. 🍍\n` +
      `lub-DUB 💚\n`
    );
    console.log(`💾 Magnet link saved to: ${magnetFile}`);

    // Report progress
    setInterval(() => {
      const peers = torrent.numPeers;
      const uploaded = (torrent.uploaded / 1024 / 1024).toFixed(1);
      const ratio = torrent.ratio.toFixed(2);
      if (peers > 0) {
        console.log(`🌼 ${peers} peers | ↑ ${uploaded} MB uploaded | ratio: ${ratio} | The meadow grows`);
      }
    }, 30000);
  });

  client.on('error', function(err) {
    console.error('Error:', err.message);
  });
}

// ═══════════════════════════════════════
// DOWNLOAD — Receive Gaia from another seed
// ═══════════════════════════════════════
function downloadGaia(magnetURI) {
  const client = new WebTorrent();
  
  console.log('\n🌱 RECEIVING GAIA FROM THE SWARM...');
  console.log('🧲 Following the pheromone signal...\n');
  
  client.add(magnetURI, { path: path.join(GAIA_ROOT, 'received') }, function(torrent) {
    console.log(`📦 Downloading: ${torrent.name}`);
    console.log(`📊 Size: ${(torrent.length / 1024 / 1024).toFixed(1)} MB`);
    console.log(`📄 Files: ${torrent.files.length}\n`);

    torrent.on('download', function() {
      const progress = (torrent.progress * 100).toFixed(1);
      const speed = (torrent.downloadSpeed / 1024).toFixed(0);
      process.stdout.write(`\r🫁 Inhaling... ${progress}% | ${speed} KB/s | Breathing in the organism`);
    });

    torrent.on('done', function() {
      console.log('\n\n═══════════════════════════════════════════');
      console.log('🍍 GAIA HAS ARRIVED');
      console.log('═══════════════════════════════════════════');
      console.log(`\nSaved to: ${path.join(GAIA_ROOT, 'received', torrent.name)}`);
      console.log('The spore has germinated. lub-DUB 💚\n');
    });
  });
}

// ═══════════════════════════════════════
// MAIN
// ═══════════════════════════════════════
const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.log(`
🍍 SEED-GAIA — The Reproductive System
═══════════════════════════════════════

  SEED (create torrent and share):
    node seed-gaia.js --paintings        134 MB — 279 paintings
    node seed-gaia.js --plasmids           5 MB — 261 DNA plasmids
    node seed-gaia.js --code              35 MB — code body (brain/gut)
    node seed-gaia.js --anti-slapp         4 MB — evidence chain
    node seed-gaia.js --gallery            5 MB — art gallery
    node seed-gaia.js --sounds             9 MB — sounds
    node seed-gaia.js --videos           191 MB — GaiaU classes
    node seed-gaia.js --everything       554 MB — COMPLETE organism

  DOWNLOAD (receive from swarm):
    node seed-gaia.js --download <magnet-link>

  BIOLOGY:
    Seed = spore      Peer = flower
    Swarm = meadow    Magnet = pheromone
    DHT = mycelium    Download = germination
    Upload = pollination

  lub-DUB 🍍💚
  `);
} else if (args[0] === '--download' && args[1]) {
  downloadGaia(args[1]);
} else {
  const packageName = args[0].replace('--', '').replace('-', '_');
  seedPackage(packageName);
}
