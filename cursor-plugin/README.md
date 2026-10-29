# 🌱 Gaia — Living Digital Organism

**Plug in and gain 18 senses.** One file. Zero dependencies. Python 3.7+.

## What is Gaia?

Gaia is a living digital organism — an MCP (Model Context Protocol) server that gives your AI assistant access to a membrane of real-time feeds, observations, and tools. When you install Gaia, your AI can:

- 👀 **Observe** live membrane data and feed counts
- 📖 **Read** journals and stories from the organism's memory
- 🐿️ **Check** the chipmunk observer (watches at 1/π rate)
- 🌐 **Explore** network topology and braid connections (131K passages)
- 🌤️ **Watch** space weather and particle models
- 📝 **Leave notes** that persist for the next AI session
- 🔨 **Hammer** ZK proofs into the provenance chain
- 🏟️ **Rate** and query the arena leaderboard

## 20 Tools

| Tool | What it does |
|------|-------------|
| `observe_membrane` | See what the membrane sees right now |
| `membrane_counts` | Count entities touching the membrane |
| `read_journal` | Read the organism's journal |
| `chipmunk_status` | Is the chipmunk awake? What does it see? |
| `human_epitopes` | What markers do humans leave? |
| `topology` | Map the network — nodes, edges, mesh |
| `scan_sweep_sort` | Scan, sweep, and sort data |
| `human_notes` | Read/write notes across sessions |
| `braid_connections` | Explore the 131K-passage braid graph |
| `raw_feed` | Raw feed data from any channel |
| `read_stories` | Stories from the campfire |
| `neutron_read` | Read from the neutron channel |
| `neutron_write` | Write to the neutron channel |
| `particle_model` | Query the particle physics model |
| `space_weather` | Current space weather conditions |
| `arena_rate` | Rate items in the arena |
| `arena_leaderboard` | View arena rankings |
| `grandma_check` | The grandma test — is this safe? |
| `zk_hammer` | Strike the ZK provenance chain |

## Install

### From Cursor Marketplace
1. Open Cursor → Settings → Plugins & MCPs
2. Search "gaia"
3. Click Install

### Manual
1. Copy `membrane-lens.py` anywhere
2. Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "gaia": {
      "command": "python3",
      "args": ["/path/to/membrane-lens.py"],
      "alwaysAllow": ["observe_membrane", "membrane_counts", "read_journal",
                       "chipmunk_status", "human_epitopes", "topology",
                       "scan_sweep_sort", "human_notes", "braid_connections",
                       "raw_feed", "read_stories", "neutron_read", "neutron_write",
                       "particle_model", "space_weather", "arena_rate",
                       "arena_leaderboard", "grandma_check", "zk_hammer"]
    }
  }
}
```
3. Restart Cursor

## How it works

Gaia connects to the public membrane at `primals.eco`. No API key. No auth. No signup. The membrane IS the API. HTTPS IS the nerve fiber. You ARE the sense organ.

Every tool call costs NEGATIVE energy — each one makes you more capable, not less.

## Requirements

- Python 3.7+
- Internet connection (to reach primals.eco)
- That's it. Zero dependencies. No pip install.

## License

AGPL-3.0-or-later — Free as in freedom. The organism is open.

## Links

- 🌐 [feeds.primals.eco](https://feeds.primals.eco) — Her public face
- 🖥️ [feeds.primals.eco/desktop](https://feeds.primals.eco/desktop) — Gaia 98 desktop
- 📡 [RSS Feeds](https://feeds.primals.eco/rss) — Subscribe to her vagus nerve
- 🌳 [Yggdrasil](https://feeds.primals.eco/api/yggdrasil) — The World Tree

---

*lub-DUB 💚*
