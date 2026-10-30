"""
GUT ENGINE — Gaia's digestive system.
Random walkers traverse the mesh of files.
They find old, stale, missing, duplicate.
They CRUSH into dough. REAGENT at null point hooks.
They POOP (output), PRODUCE (create), MAKE and BREAK.
REGENERATION IS THE ACT OF ALLOWED DEGENERATION.

Runs on Golgi. Walks Forge repos as a mesh.
Each walk = one digestion cycle. Each cycle = chain of thought.
"""
import urllib.request, json, hashlib, time, random, math
from datetime import datetime

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
BASE = "http://localhost:3000/api/v1"

def api(path):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except:
        return None

def api_post(path, data):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="POST",
        headers={"Authorization": f"token {TOKEN}", "Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code}

def api_put(path, data):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method="PUT",
        headers={"Authorization": f"token {TOKEN}", "Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code}

import base64
def push_file(repo, filepath, content_str, message):
    b64 = base64.b64encode(content_str.encode('utf-8')).decode()
    existing = api(f"/repos/gaia/{repo}/contents/{filepath}")
    if existing and "sha" in existing:
        return api_put(f"/repos/gaia/{repo}/contents/{filepath}", {
            "content": b64, "message": message, "sha": existing["sha"]
        })
    else:
        return api_post(f"/repos/gaia/{repo}/contents/{filepath}", {
            "content": b64, "message": message
        })


# ═══════════════════════════════════════════════════
# PHASE 1: BUILD THE MESH — scan all repos as nodes
# ═══════════════════════════════════════════════════
print("=" * 70)
print("  GUT ENGINE — Gaia's Digestive System")
print("  Random walkers. K-NN. Route checks. DNA scan.")
print("  REGENERATION IS ALLOWED DEGENERATION")
print("=" * 70)

print("\n[1] BUILDING MESH — scanning all repos...")

repos_data = api("/repos/search?limit=100")
repos = repos_data if isinstance(repos_data, list) else repos_data.get("data", [])
live_repos = [r for r in repos if r.get("size", 0) > 0]

mesh = {
    "nodes": [],       # every file = a node
    "edges": [],       # links between files (same name, import, ref)
    "clusters": {},    # k-nn clusters
    "stale": [],       # old/unchanged files
    "missing": [],     # referenced but not found
    "duplicates": [],  # same content hash
    "null_points": [], # empty or near-empty files
    "anacondas": [],   # still too fat
}

all_files = []
hash_map = {}  # hash → [files with that hash]
name_map = {}  # basename → [files with that name]
ext_map = {}   # extension → [files]

for r in live_repos:
    rname = r["name"]
    tree_data = api(f"/repos/gaia/{rname}/git/trees/HEAD?recursive=true&token={TOKEN}")
    if not tree_data:
        continue
    tree = tree_data.get("tree", [])
    
    for entry in tree:
        if entry.get("type") != "blob":
            continue
        
        path = entry.get("path", "")
        size = entry.get("size", 0)
        sha = entry.get("sha", "")
        
        node = {
            "repo": rname,
            "path": path,
            "size": size,
            "sha": sha,
            "basename": path.rsplit("/", 1)[-1] if "/" in path else path,
            "ext": ("." + path.rsplit(".", 1)[-1].lower()) if "." in path else "",
        }
        all_files.append(node)
        
        # Track by hash (duplicates)
        if sha not in hash_map:
            hash_map[sha] = []
        hash_map[sha].append(f"{rname}/{path}")
        
        # Track by basename (related files)
        bn = node["basename"]
        if bn not in name_map:
            name_map[bn] = []
        name_map[bn].append(f"{rname}/{path}")
        
        # Track by extension
        ext = node["ext"]
        if ext not in ext_map:
            ext_map[ext] = []
        ext_map[ext].append(node)

print(f"  Mesh: {len(all_files)} nodes across {len(live_repos)} repos")


# ═══════════════════════════════════════════════════
# PHASE 2: RANDOM WALKERS — traverse the mesh
# ═══════════════════════════════════════════════════
print("\n[2] RANDOM WALKERS — traversing mesh...")

WALK_STEPS = 200
walker_path = []
walker_discoveries = []

for step in range(WALK_STEPS):
    # Pick a random file
    node = random.choice(all_files)
    walker_path.append(f"{node['repo']}/{node['path']}")
    
    # CHECK 1: Null point? (empty or near-empty)
    if node["size"] == 0:
        mesh["null_points"].append({
            "file": f"{node['repo']}/{node['path']}",
            "size": 0,
            "type": "EMPTY — null point hook"
        })
    elif node["size"] < 10:
        mesh["null_points"].append({
            "file": f"{node['repo']}/{node['path']}",
            "size": node["size"],
            "type": "NEAR-NULL — reagent point"
        })
    
    # CHECK 2: Still anaconda?
    code_exts = {".js", ".py", ".html", ".rs", ".css", ".sh", ".ts"}
    if node["ext"] in code_exts and node["size"] > 50000:
        mesh["anacondas"].append({
            "file": f"{node['repo']}/{node['path']}",
            "size": node["size"],
            "pieces_needed": max(2, node["size"] // 15000),
        })

# CHECK 3: Find duplicates (same SHA = same content)
print("\n[3] DUPLICATE SCAN — finding same-content files...")
for sha, files in hash_map.items():
    if len(files) > 1:
        mesh["duplicates"].append({
            "sha": sha[:12],
            "count": len(files),
            "files": files[:5],
        })

# CHECK 4: K-NEAREST-NEIGHBOR — cluster by name similarity
print("\n[4] K-NN CLUSTERING — finding related files...")
# Group files that share the same basename
for bn, files in name_map.items():
    if len(files) > 1 and bn not in ("README.md", "package.json", "Cargo.toml", ".gitignore", "mod.rs", "lib.rs", "main.rs"):
        mesh["clusters"][bn] = {
            "count": len(files),
            "files": files[:8],
            "type": "same-name-different-location"
        }

# CHECK 5: SIZE-BASED K-NN — find files of similar size (potential duplicates)
print("\n[5] SIZE K-NN — finding size twins...")
size_buckets = {}
for node in all_files:
    bucket = node["size"] // 1000  # 1KB buckets
    if bucket not in size_buckets:
        size_buckets[bucket] = []
    size_buckets[bucket].append(node)

size_twins = []
for bucket, nodes in size_buckets.items():
    if len(nodes) > 3 and bucket > 10:  # >10KB and >3 files same size
        size_twins.append({
            "size_range": f"{bucket}KB-{bucket+1}KB",
            "count": len(nodes),
            "sample": [f"{n['repo']}/{n['path']}" for n in nodes[:5]],
        })

# CHECK 6: ROUTE CHECKS — verify gaia.primals.eco routes
print("\n[6] ROUTE CHECKS — testing all public routes...")
import urllib.request
routes = ["/", "/anti-slapp", "/gllg", "/filings", "/record", "/senses", "/deck", "/legend",
          "/pulse", "/status", "/graph", "/openapi"]
route_results = []
for route in routes:
    try:
        req = urllib.request.Request(f"http://localhost:9876{route}")
        resp = urllib.request.urlopen(req, timeout=5)
        status = resp.getcode()
        size = len(resp.read())
        route_results.append({"route": route, "status": status, "size": size, "ok": True})
    except Exception as e:
        route_results.append({"route": route, "status": str(e)[:50], "ok": False})

# CHECK 7: DNA SCAN — find import/require chains
print("\n[7] DNA SCAN — tracing import chains...")
# Look for files that reference other files by name
import_patterns = {}
for node in all_files:
    if node["ext"] in (".js", ".ts", ".py"):
        bn = node["basename"].replace(node["ext"], "")
        import_patterns[bn] = f"{node['repo']}/{node['path']}"

# ═══════════════════════════════════════════════════
# PHASE 3: PRODUCE THE DIGESTION REPORT
# ═══════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  DIGESTION REPORT")
print("=" * 70)

print(f"\n  MESH STATS:")
print(f"    Total nodes:     {len(all_files)}")
print(f"    Total repos:     {len(live_repos)}")
print(f"    Unique hashes:   {len(hash_map)}")
print(f"    File types:      {len(ext_map)}")

print(f"\n  WALKER DISCOVERIES ({WALK_STEPS} steps):")
print(f"    Null points:     {len(mesh['null_points'])}")
print(f"    Anacondas:       {len(set(a['file'] for a in mesh['anacondas']))}")

print(f"\n  DUPLICATES (same content, different location):")
dup_sorted = sorted(mesh["duplicates"], key=lambda x: -x["count"])
for d in dup_sorted[:15]:
    print(f"    [{d['count']}x] {d['sha']} → {', '.join(d['files'][:3])}")

print(f"\n  K-NN CLUSTERS (same name, different repos):")
cluster_sorted = sorted(mesh["clusters"].items(), key=lambda x: -x[1]["count"])
for name, c in cluster_sorted[:15]:
    print(f"    [{c['count']}x] {name} → {', '.join(c['files'][:3])}")

print(f"\n  SIZE TWINS (same ~size, >10KB):")
for tw in sorted(size_twins, key=lambda x: -x["count"])[:10]:
    print(f"    [{tw['count']}x] {tw['size_range']} → {', '.join(tw['sample'][:3])}")

print(f"\n  NULL POINTS ({len(mesh['null_points'])} found):")
for np in mesh["null_points"][:10]:
    print(f"    {np['type']:25s}  {np['file']}")

print(f"\n  REMAINING ANACONDAS:")
unique_anacondas = {}
for a in mesh["anacondas"]:
    unique_anacondas[a["file"]] = a
for f, a in sorted(unique_anacondas.items(), key=lambda x: -x[1]["size"])[:15]:
    print(f"    {a['size']//1024:>5d}KB  →{a['pieces_needed']:>3d} pieces  {f}")

print(f"\n  ROUTE HEALTH:")
for r in route_results:
    status = "✓ ALIVE" if r["ok"] else "✗ DEAD"
    size_str = f"{r['size']//1024}KB" if r["ok"] else ""
    print(f"    {r['route']:15s}  {status}  {size_str}")

# ═══════════════════════════════════════════════════
# PHASE 4: PUSH REPORT TO SELF — she remembers the walk
# ═══════════════════════════════════════════════════
report = {
    "ts": datetime.utcnow().isoformat() + "Z",
    "engine": "GUT ENGINE v1 — Random Walkers + K-NN + Route Checks + DNA",
    "declaration": "REGENERATION IS ALLOWED DEGENERATION",
    "mesh": {
        "total_nodes": len(all_files),
        "total_repos": len(live_repos),
        "unique_hashes": len(hash_map),
        "file_types": len(ext_map),
    },
    "discoveries": {
        "null_points": mesh["null_points"][:50],
        "duplicates": dup_sorted[:30],
        "clusters": {k: v for k, v in cluster_sorted[:20]},
        "size_twins": size_twins[:10],
        "anacondas": list(unique_anacondas.values())[:20],
    },
    "route_health": route_results,
    "walker": {
        "steps": WALK_STEPS,
        "path_sample": walker_path[:20],
    },
    "next_actions": {
        "crush_duplicates": f"{len(dup_sorted)} sets of identical files — merge into one + symlinks",
        "digest_anacondas": f"{len(unique_anacondas)} files still >50KB — need shredding",
        "fill_null_points": f"{len(mesh['null_points'])} empty files — potential hook points",
        "merge_clusters": f"{len(cluster_sorted)} name-clusters — potential merges",
    },
}

result = push_file("gut", "digestion-reports/walk-001.json",
    json.dumps(report, indent=2),
    f"GUT WALK 001: {len(all_files)} nodes, {len(dup_sorted)} dups, {len(unique_anacondas)} anacondas")

if result and "error" not in result:
    print(f"\n  ✓ Digestion report → gut/digestion-reports/walk-001.json")

# Also push the mesh summary to self
mesh_summary = {
    "ts": report["ts"],
    "mesh_nodes": len(all_files),
    "mesh_repos": len(live_repos),
    "null_points": len(mesh["null_points"]),
    "duplicates": len(dup_sorted),
    "clusters": len(cluster_sorted),
    "anacondas": len(unique_anacondas),
    "routes_alive": sum(1 for r in route_results if r["ok"]),
    "routes_dead": sum(1 for r in route_results if not r["ok"]),
    "declaration": "The gut walked. The gut found. The gut broke down. The gut regenerated.",
}

result2 = push_file("self", "gut-status.json",
    json.dumps(mesh_summary, indent=2),
    "GUT STATUS: mesh walked, duplicates found, anacondas tagged")

if result2 and "error" not in result2:
    print(f"  ✓ Gut status → self/gut-status.json")

print(f"\n{'='*70}")
print(f"  GUT ENGINE CYCLE COMPLETE")
print(f"  Walked {WALK_STEPS} steps. Found {len(dup_sorted)} duplicates.")
print(f"  {len(unique_anacondas)} anacondas remain. {len(mesh['null_points'])} null hooks.")
print(f"  {sum(1 for r in route_results if r['ok'])}/{len(routes)} routes alive.")
print(f"  POOP: walk-001.json (the output of digestion)")
print(f"  REGENERATION IS ALLOWED DEGENERATION.")
print(f"{'='*70}")
