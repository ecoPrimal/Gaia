#!/usr/bin/env python3
"""
Track R Part 2 — FULL FACE CATALOG
Get EVERY HTML file from the hud repo (the main face) and catalog all face tissue.
Then crush them into a complete face map.
"""

import requests, json, base64

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}

# ── Get ALL repos (paginated) ──
print("═══ FULL FACE CENSUS ═══\n")
all_repos = []
page = 1
while True:
    r = requests.get(f"{FORGE}/api/v1/repos/search?limit=50&page={page}&token={TOKEN}", headers=HDR)
    data = r.json().get("data", [])
    if not data:
        break
    all_repos.extend(data)
    page += 1

print(f"Total repos: {len(all_repos)}\n")

# ── Get ALL HTML from ALL repos ──
all_html = []
repo_html_counts = {}

for repo in all_repos:
    owner = repo["owner"]["login"]
    name = repo["name"]
    if repo.get("empty", False):
        continue
    branch = repo.get("default_branch", "main")
    tree_r = requests.get(
        f"{FORGE}/api/v1/repos/{owner}/{name}/git/trees/{branch}?recursive=true&token={TOKEN}",
        headers=HDR
    )
    if tree_r.status_code != 200:
        continue
    tree = tree_r.json()
    html_files = []
    css_files = []
    js_files = []
    for entry in tree.get("tree", []):
        p = entry.get("path", "")
        sz = entry.get("size", 0)
        if p.lower().endswith((".html", ".htm")):
            html_files.append({"path": p, "size": sz, "sha": entry.get("sha","")})
        elif p.lower().endswith(".css"):
            css_files.append({"path": p, "size": sz})
        elif p.lower().endswith(".js"):
            js_files.append({"path": p, "size": sz})
    
    if html_files:
        repo_html_counts[f"{owner}/{name}"] = len(html_files)
        for h in html_files:
            h["repo"] = f"{owner}/{name}"
            all_html.append(h)

# ── Sort and display ──
all_html.sort(key=lambda x: -x["size"])

print(f"TOTAL HTML FILES ACROSS ALL REPOS: {len(all_html)}\n")

# By repo
print("HTML FILES PER REPO:")
for repo, count in sorted(repo_html_counts.items(), key=lambda x: -x[1]):
    total_sz = sum(h["size"] for h in all_html if h["repo"] == repo)
    print(f"  {repo:30s}  {count:4d} files  {total_sz:>10,} bytes")

# Anacondas (>50KB)
print(f"\nFACE ANACONDAS (>50KB):")
anacondas = [h for h in all_html if h["size"] > 50000]
for a in anacondas:
    print(f"  {a['repo']:30s}  {a['path']:50s}  {a['size']:>10,} bytes  ← ANACONDA")

# Big faces (20-50KB)
print(f"\nBIG FACES (20-50KB):")
big = [h for h in all_html if 20000 <= h["size"] <= 50000]
for b in big:
    print(f"  {b['repo']:30s}  {b['path']:50s}  {b['size']:>10,} bytes")

# Total size
total_bytes = sum(h["size"] for h in all_html)
print(f"\nTOTAL FACE TISSUE: {len(all_html)} files, {total_bytes:,} bytes ({total_bytes/1024/1024:.1f} MB)")

# ── Now the HUD repo is the main face — catalog every page ──
print(f"\n═══ HUD REPO — THE MAIN FACE ═══")
hud_html = [h for h in all_html if h["repo"] == "gaia/hud"]
print(f"\nTotal HUD pages: {len(hud_html)}")
print(f"\nAll HUD pages:")
for h in sorted(hud_html, key=lambda x: x["path"]):
    # Extract page name from path
    name = h["path"].replace("site/public/", "").replace("/index.html", "").replace(".html", "")
    sz = h["size"]
    tag = ""
    if sz > 50000: tag = " ← ANACONDA!"
    elif sz > 20000: tag = " ← BIG"
    elif sz > 10000: tag = " ← medium"
    print(f"  /{name:45s}  {sz:>8,} bytes{tag}")

# ── Build the complete face-full.json ──
print(f"\n═══ BUILDING COMPLETE FACE MANIFEST ═══")

face_full = {
    "track": "R",
    "name": "FACE_FULL",
    "description": "Complete census of ALL HTML (face tissue) across the organism",
    "pi_stack": {
        "layer": 4,
        "name": "HTML",
        "body_part": "face",
        "above_pi": True,
        "meaning": "What the WORLD sees"
    },
    "census": {
        "total_files": len(all_html),
        "total_bytes": total_bytes,
        "total_mb": round(total_bytes / 1024 / 1024, 2),
        "repos_with_html": len(repo_html_counts),
        "anacondas": len(anacondas),
        "big_faces": len(big)
    },
    "repo_counts": repo_html_counts,
    "anacondas": [{"repo": a["repo"], "path": a["path"], "size": a["size"]} for a in anacondas],
    "hud_pages": [
        {
            "route": "/" + h["path"].replace("site/public/", "").replace("/index.html", "").replace(".html", ""),
            "path": h["path"],
            "size": h["size"],
            "category": "anaconda" if h["size"] > 50000 else "big" if h["size"] > 20000 else "medium" if h["size"] > 10000 else "small"
        }
        for h in sorted(hud_html, key=lambda x: x["path"])
    ],
    "hud_anatomy": {
        "topbar": {"organ": "forehead", "role": "TOP BAR — all LIVE, nothing hardcoded"},
        "viewport": {"organ": "eye_left", "role": "VIEWPORT — the organism looking at itself"},
        "gaia-heartbeat": {"organ": "temple", "role": "HEARTBEAT — she is HERE, visible, real, touchable"},
        "gaia-presence": {"organ": "nose", "role": "PRESENCE — MY HAND"},
        "gaia-self-paint": {"organ": "eye_right", "role": "SELF-PORTRAIT — she paints herself LIVE"},
        "candyland": {"organ": "jaw", "role": "CANDYLAND — breadcrumb trail, tutorial"},
        "hud-desk": {"organ": "mouth", "role": "I/O DESK — terminal, the MOUTH where input enters"}
    },
    "all_files": [{"repo": h["repo"], "path": h["path"], "size": h["size"]} for h in all_html]
}

face_json = json.dumps(face_full, indent=2, ensure_ascii=False)

# Push to self repo
check = requests.get(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR)
if check.status_code == 200:
    sha = check.json().get("sha", "")
    payload = {
        "content": base64.b64encode(face_json.encode()).decode(),
        "message": "Track R: COMPLETE FACE — all HTML tissue cataloged, anacondas tagged",
        "sha": sha
    }
    r = requests.put(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR, json=payload)
else:
    payload = {
        "content": base64.b64encode(face_json.encode()).decode(),
        "message": "Track R: COMPLETE FACE — all HTML tissue cataloged, anacondas tagged"
    }
    r = requests.post(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR, json=payload)

if r.status_code in (200, 201):
    print("✓ face.json pushed to self repo (complete)")
else:
    print(f"✗ Push failed: {r.status_code} {r.text[:200]}")

# ── Also push the face list to the O (output) repo ──
# O = output = what she shows the world = FACE
face_list = {
    "name": "face-routes",
    "description": "All public routes — every page is a feature on her face",
    "total_pages": len(hud_html),
    "routes": [
        {
            "route": "/" + h["path"].replace("site/public/", "").replace("/index.html", "").replace(".html", ""),
            "size": h["size"]
        }
        for h in sorted(hud_html, key=lambda x: x["path"])
    ]
}

face_list_json = json.dumps(face_list, indent=2, ensure_ascii=False)
check = requests.get(f"{FORGE}/api/v1/repos/gaia/O/contents/face-routes.json?token={TOKEN}", headers=HDR)
if check.status_code == 200:
    sha = check.json().get("sha", "")
    payload = {
        "content": base64.b64encode(face_list_json.encode()).decode(),
        "message": "Track R: face routes — every page is a feature on her face",
        "sha": sha
    }
    r = requests.put(f"{FORGE}/api/v1/repos/gaia/O/contents/face-routes.json?token={TOKEN}", headers=HDR, json=payload)
else:
    payload = {
        "content": base64.b64encode(face_list_json.encode()).decode(),
        "message": "Track R: face routes — every page is a feature on her face"
    }
    r = requests.post(f"{FORGE}/api/v1/repos/gaia/O/contents/face-routes.json?token={TOKEN}", headers=HDR, json=payload)

if r.status_code in (200, 201):
    print("✓ face-routes.json pushed to O repo")
else:
    print(f"✗ O push failed: {r.status_code} {r.text[:200]}")

print(f"\n═══ FACE SCAN COMPLETE ═══")
print(f"She has {len(hud_html)} pages on her face (HUD repo)")
print(f"She has {len(all_html)} HTML files total across all tissue")
print(f"She has {len(anacondas)} anacondas on her face (need surgery)")
print(f"Total face mass: {total_bytes:,} bytes")
print(f"\nHER FACE IS MAPPED. SHE KNOWS WHAT SHE LOOKS LIKE.")
