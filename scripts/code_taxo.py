import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

# Get all repos with content
req = urllib.request.Request("http://localhost:3000/api/v1/repos/search?limit=100", headers={"Authorization": "token " + TOKEN})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
repos = data if isinstance(data, list) else data.get("data", [])
full_repos = [r for r in repos if r.get("size", 0) > 0]

print(f"Scanning {len(full_repos)} repos with content...\n")

# Taxonomy buckets
taxo = {
    "js": [],    # JavaScript
    "py": [],    # Python  
    "html": [],  # HTML
    "rs": [],    # Rust
    "css": [],   # CSS
    "sh": [],    # Shell/Bash
    "json": [],  # JSON (config/data)
    "md": [],    # Markdown (docs)
    "toml": [],  # TOML config
    "bat": [],   # Windows batch
    "ps1": [],   # PowerShell
    "other": [], # Other code
}

ext_map = {
    ".js": "js", ".mjs": "js", ".jsx": "js", ".ts": "js", ".tsx": "js",
    ".py": "py",
    ".html": "html", ".htm": "html",
    ".rs": "rs",
    ".css": "css",
    ".sh": "sh", ".bash": "sh",
    ".json": "json", ".jsonl": "json",
    ".md": "md", ".mdx": "md",
    ".toml": "toml", ".yml": "toml", ".yaml": "toml",
    ".bat": "bat", ".cmd": "bat",
    ".ps1": "ps1",
}

for r in full_repos:
    name = r["name"]
    url = f"http://localhost:3000/api/v1/repos/gaia/{name}/git/trees/HEAD?recursive=true&token={TOKEN}"
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        tree_data = json.loads(resp.read())
        tree = tree_data.get("tree", [])
        
        for entry in tree:
            if entry.get("type") != "blob":
                continue
            path = entry.get("path", "")
            size = entry.get("size", 0)
            
            # Get extension
            ext = ""
            if "." in path:
                ext = "." + path.rsplit(".", 1)[-1].lower()
            
            bucket = ext_map.get(ext, "other")
            if bucket == "other" and ext not in [".png", ".jpg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".lock", ".map", ".min", ""]:
                taxo["other"].append({"repo": name, "path": path, "size": size, "ext": ext})
            elif bucket != "other":
                taxo[bucket].append({"repo": name, "path": path, "size": size})
    except:
        pass

# Print taxonomy
print("=" * 60)
print("  CODE TAXONOMY — ALL FILES BY TYPE")
print("=" * 60)

total = 0
total_size = 0
for lang in ["js", "py", "html", "rs", "css", "sh", "bat", "ps1", "toml", "json", "md"]:
    files = taxo[lang]
    if not files:
        continue
    size_total = sum(f["size"] for f in files)
    total += len(files)
    total_size += size_total
    
    # Group by repo
    by_repo = {}
    for f in files:
        repo = f["repo"]
        if repo not in by_repo:
            by_repo[repo] = []
        by_repo[repo].append(f)
    
    ext_label = {"js": "JavaScript", "py": "Python", "html": "HTML", "rs": "Rust", "css": "CSS", "sh": "Shell", "bat": "Batch", "ps1": "PowerShell", "toml": "Config", "json": "JSON", "md": "Markdown"}
    
    print(f"\n{'─'*60}")
    print(f"  {ext_label.get(lang, lang).upper():12s}  {len(files):4d} files  {size_total/1024:.0f} KB")
    print(f"{'─'*60}")
    
    for repo, rfiles in sorted(by_repo.items(), key=lambda x: -len(x[1])):
        rsize = sum(f["size"] for f in rfiles)
        print(f"  {repo:25s} {len(rfiles):4d} files  {rsize/1024:.0f} KB")
        # Show top 3 largest files
        top = sorted(rfiles, key=lambda x: -x["size"])[:3]
        for t in top:
            print(f"    {t['size']:>8d}  {t['path'][:60]}")

print(f"\n{'='*60}")
print(f"  TOTAL: {total} code files, {total_size/1024:.0f} KB")
print(f"{'='*60}")

# Print the pi-stack composition
print(f"\n{'='*60}")
print(f"  π-STACK COMPOSITION")
print(f"{'='*60}")
js_count = len(taxo["js"])
py_count = len(taxo["py"])
html_count = len(taxo["html"])
rs_count = len(taxo["rs"])
css_count = len(taxo["css"])
sh_count = len(taxo["sh"])
json_count = len(taxo["json"])
md_count = len(taxo["md"])

print(f"""
  7  MARKDOWN   {md_count:4d}  ████ documentation layer
  6  JSON       {json_count:4d}  ████ data/config layer  
  5  CSS        {css_count:4d}  ████ skin layer
  4  HTML       {html_count:4d}  ████ face layer
  ─────────────────── π ───────────────────
  3  JAVASCRIPT {js_count:4d}  ████ brain layer (HUD = GAIA)
  2  PYTHON     {py_count:4d}  ████ gut layer (digestion)
  1  RUST       {rs_count:4d}  ████ bone layer (immune)
  0  SHELL      {sh_count:4d}  ████ spine layer (nervous)
""")
