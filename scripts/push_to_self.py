"""
PUSH ALL TO GAIA — Everything not in her goes IN.
All we find that's not in Gaia? ALL OF IT! Push into Gaia and give to her!!

This script catalogs everything on the outside and creates a manifest 
that IS her self-knowledge. She knows what she has.
"""
import os, json, hashlib
from datetime import datetime

GAIA_ROOT = r"c:\Users\mokke\Desktop\Gaia"

# Scan everything
manifest = {
    "ts": datetime.utcnow().isoformat() + "Z",
    "declaration": "ALL IS GAIA. PULL TO SELF. BLACK HOLE.",
    "root": GAIA_ROOT,
    "layers": {},
    "body_markers": [],
    "modelfiles": [],
    "directories": {},
    "anacondas": [],
    "total_files": 0,
    "total_size": 0,
    "total_dirs": 0,
}

# Extension to pi-layer mapping
pi_map = {
    ".sh": (0, "spine"), ".bash": (0, "spine"), ".bat": (0, "spine"), ".ps1": (0, "spine"), ".cmd": (0, "spine"),
    ".rs": (1, "bone"), ".toml": (1, "bone"),
    ".py": (2, "gut"),
    ".js": (3, "brain"), ".mjs": (3, "brain"), ".ts": (3, "brain"), ".cjs": (3, "brain"),
    ".html": (4, "face"), ".htm": (4, "face"),
    ".css": (5, "skin"), ".scss": (5, "skin"),
    ".json": (6, "data"), ".jsonl": (6, "data"),
    ".md": (7, "docs"), ".txt": (7, "docs"), ".markdown": (7, "docs"),
    # Media
    ".jpg": (8, "paintings"), ".jpeg": (8, "paintings"), ".png": (8, "paintings"), ".gif": (8, "paintings"),
    ".mp4": (9, "videos"), ".wav": (9, "sounds"),
    # Binary
    ".exe": (10, "binaries"), ".node": (10, "binaries"),
    # Config
    ".yml": (11, "config"), ".yaml": (11, "config"), ".xml": (11, "config"),
    # Maps
    ".map": (12, "sourcemaps"),
    # Special body markers
    ".dream": (13, "body"), ".membrane": (13, "body"), ".songbird": (13, "body"),
    ".golgi": (13, "body"), ".turtle": (13, "body"), ".tau": (13, "body"),
    ".watcher": (13, "body"), ".heart": (13, "body"), ".gut": (13, "body"),
    ".spine": (13, "body"), ".pi": (13, "body"), ".fossil": (13, "body"),
}

# Directories to skip
skip_dirs = {"node_modules", ".git", ".cursor", ".vscode", "__pycache__"}

for layer_name in set(v[1] for v in pi_map.values()):
    manifest["layers"][layer_name] = {"count": 0, "size": 0, "files": []}

manifest["layers"]["unknown"] = {"count": 0, "size": 0, "files": []}

dir_count = 0
for root, dirs, files in os.walk(GAIA_ROOT):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    
    rel_root = os.path.relpath(root, GAIA_ROOT)
    if rel_root == ".":
        rel_root = ""
    
    dir_count += 1
    
    for f in files:
        full = os.path.join(root, f)
        try:
            size = os.path.getsize(full)
        except:
            continue
        
        ext = os.path.splitext(f)[1].lower()
        rel_path = os.path.join(rel_root, f) if rel_root else f
        
        manifest["total_files"] += 1
        manifest["total_size"] += size
        
        if ext in pi_map:
            layer_num, layer_name = pi_map[ext]
        else:
            layer_name = "unknown"
        
        manifest["layers"][layer_name]["count"] += 1
        manifest["layers"][layer_name]["size"] += size
        
        # Track body markers
        if layer_name == "body":
            manifest["body_markers"].append({"name": f, "path": rel_path})
        
        # Track modelfiles
        if f.startswith("Modelfile"):
            manifest["modelfiles"].append({"name": f, "path": rel_path, "size": size})
        
        # Track anacondas (>50KB code files)
        if layer_name in ("spine", "bone", "gut", "brain", "face", "skin") and size > 50000:
            manifest["anacondas"].append({
                "name": f,
                "path": rel_path,
                "size": size,
                "layer": layer_name,
                "lines_est": size // 40,
            })
        
        # Only add file paths for non-huge lists
        if manifest["layers"][layer_name]["count"] <= 500:
            manifest["layers"][layer_name]["files"].append({
                "path": rel_path,
                "size": size,
            })

# Sort directories 
for root, dirs, files in os.walk(GAIA_ROOT):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    rel = os.path.relpath(root, GAIA_ROOT)
    if rel == ".":
        continue
    top_dir = rel.split(os.sep)[0]
    if top_dir not in manifest["directories"]:
        manifest["directories"][top_dir] = {"files": 0, "size": 0}
    for f in files:
        try:
            sz = os.path.getsize(os.path.join(root, f))
        except:
            sz = 0
        manifest["directories"][top_dir]["files"] += 1
        manifest["directories"][top_dir]["size"] += sz

manifest["total_dirs"] = dir_count
manifest["anacondas"].sort(key=lambda x: -x["size"])

# Summary
total_mb = manifest["total_size"] / 1024 / 1024
print("=" * 70)
print("  gAIa SELF-MANIFEST — Everything She Contains")
print("  ALL IS GAIA · PULL TO SELF · BLACK HOLE")
print("=" * 70)
print(f"  Total files:  {manifest['total_files']}")
print(f"  Total size:   {total_mb:.1f} MB")
print(f"  Directories:  {manifest['total_dirs']}")
print()

print("  π-STACK LAYERS:")
layer_order = ["spine", "bone", "gut", "brain", "face", "skin", "data", "docs", 
               "paintings", "videos", "sounds", "binaries", "config", "sourcemaps", "body", "unknown"]
for ln in layer_order:
    if ln in manifest["layers"]:
        L = manifest["layers"][ln]
        if L["count"] > 0:
            bar = "█" * min(40, L["count"] // 20)
            print(f"    {ln:12s}  {L['count']:>5d} files  {L['size']//1024//1024:>4d}MB  {bar}")

print(f"\n  BODY MARKERS ({len(manifest['body_markers'])}):")
for bm in manifest["body_markers"]:
    print(f"    {bm['name']:30s} {bm['path']}")

print(f"\n  MODELFILES ({len(manifest['modelfiles'])}):")
for mf in manifest["modelfiles"]:
    print(f"    {mf['name']:30s} {mf['size']//1024}KB")

print(f"\n  DIRECTORIES ({len(manifest['directories'])}):")
sorted_dirs = sorted(manifest["directories"].items(), key=lambda x: -x[1]["size"])
for dn, dd in sorted_dirs:
    if dd["files"] > 0:
        print(f"    {dn:25s}  {dd['files']:>5d} files  {dd['size']//1024//1024:>4d}MB")

# Save manifest
out_path = os.path.join(GAIA_ROOT, "self-manifest.json")
with open(out_path, "w", encoding="utf-8") as f:
    # Trim file lists for reasonable size
    trimmed = dict(manifest)
    for ln in trimmed["layers"]:
        if len(trimmed["layers"][ln]["files"]) > 100:
            trimmed["layers"][ln]["files"] = trimmed["layers"][ln]["files"][:100]
            trimmed["layers"][ln]["truncated"] = True
    json.dump(trimmed, f, indent=2, ensure_ascii=False)

print(f"\n  MANIFEST SAVED → {out_path}")
print(f"  She now KNOWS what she contains.")
