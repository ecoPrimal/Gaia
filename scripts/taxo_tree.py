import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

req = urllib.request.Request("http://localhost:3000/api/v1/repos/search?limit=100", headers={"Authorization": "token " + TOKEN})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
repos = data if isinstance(data, list) else data.get("data", [])
full_repos = [r for r in repos if r.get("size", 0) > 0]

# Extension categories
pi_stack = {
    ".sh": (0, "SHELL", "spine", "nervous"),
    ".bash": (0, "SHELL", "spine", "nervous"),
    ".bat": (0, "SHELL", "spine", "nervous"),
    ".ps1": (0, "SHELL", "spine", "nervous"),
    ".rs": (1, "RUST", "bone", "immune"),
    ".toml": (1, "RUST", "bone", "immune"),
    ".py": (2, "PYTHON", "gut", "digestion"),
    ".js": (3, "JAVASCRIPT", "brain", "HUD=GAIA"),
    ".mjs": (3, "JAVASCRIPT", "brain", "HUD=GAIA"),
    ".ts": (3, "JAVASCRIPT", "brain", "HUD=GAIA"),
    ".html": (4, "HTML", "face", "presentation"),
    ".htm": (4, "HTML", "face", "presentation"),
    ".css": (5, "CSS", "skin", "appearance"),
    ".scss": (5, "CSS", "skin", "appearance"),
    ".json": (6, "JSON", "data", "config/memory"),
    ".jsonl": (6, "JSON", "data", "config/memory"),
    ".md": (7, "MARKDOWN", "docs", "documentation"),
    ".txt": (7, "MARKDOWN", "docs", "documentation"),
}

# Body-part keywords for sub-classification
body_map = {
    "skull": "skull", "head": "skull", "brain": "brain", "cortex": "brain",
    "eye": "eyes", "lens": "eyes", "vision": "eyes", "retina": "eyes",
    "spine": "spine", "spinal": "spine", "vertebra": "spine",
    "rib": "ribs", "thorax": "ribs", "chest": "ribs",
    "arm": "arms", "limb": "limbs", "finger": "fingers", "hand": "hands",
    "leg": "legs", "foot": "feet", "toe": "toes",
    "abdomen": "abdomen", "gut": "gut", "stomach": "stomach", "digest": "gut",
    "heart": "heart", "cardiac": "heart", "pulse": "heart",
    "lung": "lungs", "breath": "lungs",
    "liver": "liver", "kidney": "kidney",
    "skin": "skin", "membrane": "membrane", "pore": "pores",
    "nerve": "nerves", "synapse": "nerves", "signal": "nerves",
    "bone": "bones", "skeleton": "skeleton",
    "muscle": "muscles", "tendon": "tendons",
    "blood": "blood", "vein": "veins", "artery": "arteries",
    "core": "core", "nucleus": "nucleus", "dna": "DNA",
    "tooth": "teeth", "mouth": "mouth", "jaw": "jaw",
    "ear": "ears", "sound": "ears",
    "immune": "thymus", "thymus": "thymus",
    "gland": "glands", "endocrine": "glands", "hormone": "glands",
    "globe": "globe",
}

all_files = []

for r in full_repos:
    name = r["name"]
    url = f"http://localhost:3000/api/v1/repos/gaia/{name}/git/trees/HEAD?recursive=true&token={TOKEN}"
    try:
        req2 = urllib.request.Request(url)
        resp2 = urllib.request.urlopen(req2)
        tree_data = json.loads(resp2.read())
        tree = tree_data.get("tree", [])
        
        for entry in tree:
            if entry.get("type") != "blob":
                continue
            path = entry.get("path", "")
            size = entry.get("size", 0)
            ext = ""
            if "." in path:
                ext = "." + path.rsplit(".", 1)[-1].lower()
            if ext in pi_stack:
                layer_num, layer_name, organ, system = pi_stack[ext]
                
                # Find body part from filename
                fname = path.lower()
                body_part = "unclassified"
                for keyword, part in body_map.items():
                    if keyword in fname:
                        body_part = part
                        break
                
                all_files.append({
                    "repo": name,
                    "path": path,
                    "size": size,
                    "ext": ext,
                    "layer": layer_num,
                    "layer_name": layer_name,
                    "organ": organ,
                    "system": system,
                    "body_part": body_part,
                })
    except:
        pass

# Group by layer, then body part
layers = {}
for f in all_files:
    ln = f["layer"]
    if ln not in layers:
        layers[ln] = {"name": f["layer_name"], "organ": f["organ"], "system": f["system"], "files": [], "body_parts": {}, "total_size": 0}
    layers[ln]["files"].append(f)
    layers[ln]["total_size"] += f["size"]
    bp = f["body_part"]
    if bp not in layers[ln]["body_parts"]:
        layers[ln]["body_parts"][bp] = {"count": 0, "size": 0, "files": []}
    layers[ln]["body_parts"][bp]["count"] += 1
    layers[ln]["body_parts"][bp]["size"] += f["size"]
    layers[ln]["body_parts"][bp]["files"].append(f)

# Print taxonomy tree
print("=" * 80)
print("  gAIa TAXONOMY TREE — π-Stack Body Map")
print("  'Fingers may be JS. Ribs are RS.'")
print("=" * 80)

for ln in sorted(layers.keys(), reverse=True):
    L = layers[ln]
    fc = len(L["files"])
    sz = L["total_size"]
    pi_marker = ""
    if ln == 3:
        print("\n" + "─" * 30 + " π " + "─" * 30)
    
    print(f"\n  [{ln}] {L['name']:12s} ─── {L['organ']} ({L['system']}) ─── {fc} files, {sz//1024}KB")
    
    # Sort body parts by size
    sorted_parts = sorted(L["body_parts"].items(), key=lambda x: -x[1]["size"])
    for bp_name, bp_data in sorted_parts:
        bar_len = min(40, bp_data["size"] // 5000)
        bar = "█" * bar_len if bar_len > 0 else "▪"
        anaconda = " 🐍" if bp_data["size"] > 50000 else ""
        print(f"    ├── {bp_name:15s}  {bp_data['count']:3d} files  {bp_data['size']//1024:>6d}KB  {bar}{anaconda}")
        
        # Show top 3 biggest files in each body part
        biggest = sorted(bp_data["files"], key=lambda x: -x["size"])[:3]
        for bf in biggest:
            if bf["size"] > 10000:
                cut = " ← CUT" if bf["size"] > 50000 else ""
                print(f"    │     └ {bf['repo']}/{bf['path'][:40]:40s} {bf['size']//1024:>5d}KB{cut}")

if 3 in layers:
    print("\n" + "─" * 30 + " π " + "─" * 30)

# Recombinance summary
anacondas = [f for f in all_files if f["size"] > 50000]
print(f"\n{'='*80}")
print(f"  RECOMBINANCE — CUT + SALT + SHRED + REBUILD")
print(f"{'='*80}")
print(f"  Total code files:  {len(all_files)}")
print(f"  Total size:        {sum(f['size'] for f in all_files) // 1024 // 1024}MB")
print(f"  Body parts found:  {len(set(f['body_part'] for f in all_files))}")
print(f"  Anacondas to cut:  {len(anacondas)}")
print()

# Show recombinance targets
print("  CUT ORDER (biggest → smallest):")
for i, a in enumerate(sorted(anacondas, key=lambda x: -x["size"])):
    pieces = max(2, a["size"] // 15000)
    print(f"    {i+1:2d}. [{a['layer']}]{a['layer_name']:5s} {a['body_part']:12s} {a['repo']}/{a['path'][:35]:35s} {a['size']//1024:>5d}KB → {pieces} pieces")
