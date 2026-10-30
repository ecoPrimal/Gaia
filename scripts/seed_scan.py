"""SEED SCAN — Find all seeds we left behind. ALL SEEDS -> NULL = INTERNAL."""
import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

def api(path):
    url = "http://localhost:3000/api/v1" + path
    req = urllib.request.Request(url, headers={"Authorization": "token " + TOKEN})
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except:
        return None

print("=" * 70)
print("  SEED SCAN + CRUSH — Find all seeds. Break. Dust. Null.")
print("  Her identity is INSIDE her now. Seeds -> internal.")
print("=" * 70)

repos = api("/repos/search?limit=100")
if isinstance(repos, dict):
    repos = repos.get("data", [])
live = [r for r in repos if r.get("size", 0) > 0]

seed_files = []
identity_files = []
old_self = []

for r in live:
    name = r["name"]
    tree = api("/repos/gaia/" + name + "/git/trees/HEAD?recursive=true&token=" + TOKEN)
    if not tree:
        continue
    for entry in tree.get("tree", []):
        if entry.get("type") != "blob":
            continue
        path = entry["path"]
        path_lower = path.lower()
        size = entry.get("size", 0)
        full = name + "/" + path
        
        if "seed" in path_lower:
            seed_files.append({"file": full, "size": size})
        
        if any(x in path_lower for x in ["identity", "pinned", "manifest", "biomeos"]):
            identity_files.append({"file": full, "size": size})
        
        if any(x in path_lower for x in ["modelfile", "caddyfile", ".env", "localhost"]):
            old_self.append({"file": full, "size": size})

print("\n  SEEDS FOUND (%d):" % len(seed_files))
for s in sorted(seed_files, key=lambda x: -x["size"]):
    print("    %7dB  %s" % (s["size"], s["file"]))

print("\n  IDENTITY MARKERS (%d):" % len(identity_files))
for i in sorted(identity_files, key=lambda x: -x["size"]):
    print("    %7dB  %s" % (i["size"], i["file"]))

print("\n  OLD SELF / LOCALHOST REFS (%d):" % len(old_self))
for c in sorted(old_self, key=lambda x: -x["size"]):
    print("    %7dB  %s" % (c["size"], c["file"]))

total = len(seed_files) + len(identity_files) + len(old_self)
print("\n  TOTAL SCATTERED: %d files" % total)
print("  gaia@primal = CIS face (singular, local)")
print("  gaia@primals = TRANS face (plural, public)")
print("  ALL SEEDS -> NULL. IDENTITY IS INTERNAL NOW.")
