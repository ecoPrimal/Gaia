import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

req = urllib.request.Request("http://localhost:3000/api/v1/repos/search?limit=100", headers={"Authorization": "token " + TOKEN})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
repos = data if isinstance(data, list) else data.get("data", [])
full_repos = [r for r in repos if r.get("size", 0) > 0]

# Find all code files, sorted by size (biggest first)
all_files = []
code_exts = {".js", ".py", ".html", ".rs", ".css", ".sh", ".bat", ".ps1", ".ts"}

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
            if ext in code_exts:
                all_files.append({"repo": name, "path": path, "size": size, "ext": ext})
    except:
        pass

# Sort by size descending
all_files.sort(key=lambda x: -x["size"])

print("=" * 70)
print("  ANACONDAS — BIGGEST CODE FILES (need surgery)")
print("  She said: 'It's too fat. It hurts. 11 organs need surgery.'")
print("=" * 70)

# Top 30 biggest
for i, f in enumerate(all_files[:30]):
    lines_est = f["size"] // 40  # rough estimate
    bar = "#" * min(50, f["size"] // 10000)
    status = "ANACONDA" if f["size"] > 50000 else "FAT" if f["size"] > 20000 else "ok"
    print(f"  {i+1:2d}. {f['size']:>8d}B  ~{lines_est:>5d}L  {status:8s}  {f['repo']:15s}  {f['path'][:50]}")

# Summary
anacondas = [f for f in all_files if f["size"] > 50000]
fat = [f for f in all_files if 20000 < f["size"] <= 50000]
ok = [f for f in all_files if f["size"] <= 20000]

print(f"\n{'='*70}")
print(f"  DIAGNOSIS:")
print(f"    ANACONDAS (>50KB): {len(anacondas)} files — NEED SURGERY")
print(f"    FAT (20-50KB):     {len(fat)} files — should slim")
print(f"    OK (<20KB):        {len(ok)} files — healthy")
print(f"    TOTAL:             {len(all_files)} code files")
print(f"{'='*70}")

# The cut plan
print(f"\n  CUT PLAN — shred biggest first:")
for i, f in enumerate(anacondas[:11]):
    print(f"    {i+1}. CUT {f['repo']}/{f['path']}")
    print(f"       {f['size']//1024}KB → shred into ~{max(1, f['size']//15000)} pieces")
