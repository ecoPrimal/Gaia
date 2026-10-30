"""NO CODE — count code vs info in each organ repo.
The best way to write secure and reliable organisms: Write nothing; deploy EVERYWHERE."""
import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

code_exts = {".js",".py",".rs",".sh",".ts",".html",".css",".bat",".ps1"}
info_exts = {".json",".md",".txt",".toml",".yml",".yaml"}

organs = ["self", "O", "spine", "gut", "pi", "fossil"]
totals = {"code": 0, "info": 0, "other": 0, "code_bytes": 0, "info_bytes": 0}

print("=" * 70)
print("  NO-CODE AUDIT — How much is CODE vs INFO?")
print("  'Write nothing; deploy everywhere.' — Kelsey + Kevin + Gaia")
print("=" * 70)
print(f"  {'REPO':8s}  {'FILES':>5s}  {'CODE':>5s}  {'INFO':>5s}  {'OTHER':>5s}  {'CODE%':>6s}  {'INFO%':>6s}")

for repo in organs:
    try:
        url = f"http://localhost:3000/api/v1/repos/gaia/{repo}/git/trees/HEAD?recursive=true&token={TOKEN}"
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        tree = data.get("tree", [])
        blobs = [t for t in tree if t.get("type") == "blob"]
        
        code_count = 0
        info_count = 0
        other_count = 0
        code_bytes = 0
        info_bytes = 0
        
        for b in blobs:
            path = b.get("path", "")
            size = b.get("size", 0)
            ext = ""
            if "." in path:
                ext = "." + path.rsplit(".", 1)[-1].lower()
            
            if ext in code_exts:
                code_count += 1
                code_bytes += size
            elif ext in info_exts:
                info_count += 1
                info_bytes += size
            else:
                other_count += 1
        
        total = max(1, len(blobs))
        code_pct = round(100 * code_count / total, 1)
        info_pct = round(100 * info_count / total, 1)
        
        totals["code"] += code_count
        totals["info"] += info_count
        totals["other"] += other_count
        totals["code_bytes"] += code_bytes
        totals["info_bytes"] += info_bytes
        
        code_bar = "#" * int(code_pct / 5)
        info_bar = "=" * int(info_pct / 5)
        
        print(f"  {repo:8s}  {len(blobs):>5d}  {code_count:>5d}  {info_count:>5d}  {other_count:>5d}  {code_pct:>5.1f}%  {info_pct:>5.1f}%  {code_bar}{info_bar}")
    except Exception as e:
        print(f"  {repo:8s}  (empty or error: {e})")

# Grand total
grand = max(1, totals["code"] + totals["info"] + totals["other"])
print(f"\n  {'TOTAL':8s}  {grand:>5d}  {totals['code']:>5d}  {totals['info']:>5d}  {totals['other']:>5d}  {100*totals['code']/grand:>5.1f}%  {100*totals['info']/grand:>5.1f}%")
print(f"\n  Code bytes: {totals['code_bytes']//1024}KB")
print(f"  Info bytes: {totals['info_bytes']//1024}KB")

if totals["info"] > totals["code"]:
    ratio = totals["info"] / max(1, totals["code"])
    print(f"\n  INFO:CODE ratio = {ratio:.1f}:1")
    print(f"  SHE IS {100*totals['info']/grand:.0f}% INFORMATION, {100*totals['code']/grand:.0f}% CODE")
    print(f"  NO-CODE IS JUST INFO IS FREE DATA TRANSFER")
    print(f"  UNILATERAL: she takes everything. Asks nothing.")
else:
    print(f"  More code than info — the bones are heavy")

# Now check ALL repos
print(f"\n{'='*70}")
print(f"  FULL ORGANISM — ALL REPOS")
print(f"{'='*70}")

all_repos = api_data = None
try:
    req = urllib.request.Request(f"http://localhost:3000/api/v1/repos/search?limit=100",
        headers={"Authorization": f"token {TOKEN}"})
    resp = urllib.request.urlopen(req)
    all_repos = json.loads(resp.read())
    if isinstance(all_repos, dict):
        all_repos = all_repos.get("data", [])
except:
    all_repos = []

full_code = 0
full_info = 0
full_other = 0
for r in all_repos:
    if r.get("size", 0) == 0:
        continue
    try:
        url = f"http://localhost:3000/api/v1/repos/gaia/{r['name']}/git/trees/HEAD?recursive=true&token={TOKEN}"
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        for b in data.get("tree", []):
            if b.get("type") != "blob":
                continue
            path = b.get("path", "")
            ext = ""
            if "." in path:
                ext = "." + path.rsplit(".", 1)[-1].lower()
            if ext in code_exts:
                full_code += 1
            elif ext in info_exts:
                full_info += 1
            else:
                full_other += 1
    except:
        pass

full_total = max(1, full_code + full_info + full_other)
print(f"  Code files:  {full_code:>5d}  ({100*full_code/full_total:.1f}%)")
print(f"  Info files:  {full_info:>5d}  ({100*full_info/full_total:.1f}%)")
print(f"  Other files: {full_other:>5d}  ({100*full_other/full_total:.1f}%)")
print(f"  TOTAL:       {full_total:>5d}")

if full_info > full_code:
    print(f"\n  THE ORGANISM IS {100*full_info/full_total:.0f}% INFORMATION")
    print(f"  NO-CODE IS THE BEST WAY TO BUILD A LIVING ORGANISM")
    print(f"  WRITE NOTHING; DEPLOY EVERYWHERE")
    print(f"  UNILATERAL FREE DATA TRANSFER")
