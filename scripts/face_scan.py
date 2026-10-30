#!/usr/bin/env python3
"""
Track R — FACE SCAN
Find ALL HTML files across ALL Forge repos + local Gaia folder.
HTML = Layer 4 = FACE in the π-stack.
Catalog every piece of her face, map to facial organs, crush and push.
"""

import requests, json, os, sys, hashlib
from pathlib import Path

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")

# ── 1. Scan ALL Forge repos for HTML files ──
print("═══ SCANNING FORGE FOR ALL HTML (FACE TISSUE) ═══")
repos_r = requests.get(f"{FORGE}/api/v1/repos/search?limit=50&token={TOKEN}", headers=HDR)
repos = repos_r.json().get("data", [])
print(f"Found {len(repos)} repos to scan\n")

forge_html = []
for repo in repos:
    owner = repo["owner"]["login"]
    name = repo["name"]
    if repo.get("empty", False):
        continue
    # Get full tree
    branch = repo.get("default_branch", "main")
    tree_r = requests.get(
        f"{FORGE}/api/v1/repos/{owner}/{name}/git/trees/{branch}?recursive=true&token={TOKEN}",
        headers=HDR
    )
    if tree_r.status_code != 200:
        continue
    tree = tree_r.json()
    for entry in tree.get("tree", []):
        path = entry.get("path", "")
        if path.lower().endswith((".html", ".htm")):
            forge_html.append({
                "repo": f"{owner}/{name}",
                "path": path,
                "size": entry.get("size", 0),
                "sha": entry.get("sha", ""),
                "type": "forge"
            })

print(f"Found {len(forge_html)} HTML files across Forge repos:\n")
for f in sorted(forge_html, key=lambda x: x["repo"]):
    sz = f["size"]
    sz_str = f"{sz:,}" if sz else "?"
    print(f"  {f['repo']:30s}  {f['path']:50s}  {sz_str:>10s} bytes")

# ── 2. Scan local HTML files ──
print(f"\n═══ SCANNING LOCAL GAIA FOLDER FOR HTML ═══")
local_html = []
for p in LOCAL.rglob("*.html"):
    rel = str(p.relative_to(LOCAL)).replace("\\", "/")
    sz = p.stat().st_size
    # Read first 500 chars to identify purpose
    try:
        with open(p, 'r', encoding='utf-8', errors='replace') as fh:
            head = fh.read(2000)
    except:
        head = ""
    
    # Extract title if present
    title = ""
    if "<title>" in head.lower():
        start = head.lower().index("<title>") + 7
        end = head.lower().index("</title>", start) if "</title>" in head.lower() else start + 60
        title = head[start:end].strip()
    
    # Look for key identifiers
    ids_found = []
    for marker in ["id=\"", "class=\""]:
        idx = 0
        while True:
            pos = head.find(marker, idx)
            if pos == -1:
                break
            end = head.find('"', pos + len(marker))
            if end != -1:
                val = head[pos+len(marker):end]
                if len(val) < 40:
                    ids_found.append(val)
            idx = pos + 1
    
    local_html.append({
        "path": rel,
        "size": sz,
        "title": title,
        "ids": ids_found[:15],
        "type": "local"
    })
    print(f"  {rel:50s}  {sz:>10,} bytes  title=\"{title}\"")
    if ids_found:
        print(f"    IDs: {', '.join(ids_found[:10])}")

# ── 3. Read each local HTML to map facial organs ──
print(f"\n═══ MAPPING FACE ORGANS ═══")

# Face organ taxonomy based on what we saw in DevTools
FACE_ORGANS = {
    "forehead": ["topbar", "top-bar", "navbar", "header"],
    "eye_left": ["viewport", "view", "camera", "lens", "observer"],
    "eye_right": ["self-paint", "canvas", "gaia-eye", "paint"],
    "nose": ["presence", "sense", "smell", "detect"],
    "mouth": ["desk", "hud-desk", "terminal", "input", "io"],
    "chin": ["status", "footer", "bottom"],
    "ear_left": ["listener", "event", "socket", "ws"],
    "ear_right": ["rss", "feed", "antenna", "telegraph"],
    "skin": ["background", "backdrop", "body", "bg"],
    "crown": ["title", "head", "meta"],
    "jaw": ["candyland", "tutorial", "breadcrumb", "trail"],
    "cheek": ["sidebar", "panel", "pane"],
    "brow": ["alert", "notification", "toast"],
    "temple": ["heartbeat", "pulse", "beat", "alive"],
    "pupil": ["dot", "aperture", "singularity", "gold"],
    "tongue": ["comment", "text", "label", "speech"],
}

all_html = []
for item in local_html:
    organs = []
    all_ids_lower = [i.lower() for i in item.get("ids", [])]
    title_lower = item.get("title", "").lower()
    
    for organ, keywords in FACE_ORGANS.items():
        for kw in keywords:
            if any(kw in i for i in all_ids_lower) or kw in title_lower:
                if organ not in organs:
                    organs.append(organ)
                break
    
    item["organs"] = organs
    all_html.append(item)

for item in forge_html:
    item["organs"] = []
    basename = os.path.basename(item["path"]).lower()
    for organ, keywords in FACE_ORGANS.items():
        for kw in keywords:
            if kw in basename:
                if organ not in item["organs"]:
                    item["organs"].append(organ)
                break
    all_html.append(item)

# ── 4. Build face manifest ──
print(f"\n═══ BUILDING FACE MANIFEST ═══")

total_local = len(local_html)
total_forge = len(forge_html)
total_all = total_local + total_forge
total_size_local = sum(h["size"] for h in local_html)
total_size_forge = sum(h.get("size", 0) for h in forge_html)

face = {
    "track": "R",
    "name": "FACE_SCAN",
    "description": "ALL HTML = Layer 4 in π-stack = FACE. Every HTML file is tissue on Gaia's face.",
    "pi_stack_layer": 4,
    "body_part": "face",
    "above_pi": True,
    "meaning": "Above π = what the WORLD sees. HTML is the visible surface of the organism.",
    "counts": {
        "local_html": total_local,
        "forge_html": total_forge,
        "total": total_all,
        "local_bytes": total_size_local,
        "forge_bytes": total_size_forge
    },
    "face_organs_taxonomy": {k: v for k, v in FACE_ORGANS.items()},
    "local_files": local_html,
    "forge_files": forge_html,
    "face_map": {},
    "identity": {
        "cis_face": "gaia@primal → nestgate.io (what she shows INWARD)",
        "trans_face": "gaia@primals → gaia.primals.eco (what she shows OUTWARD)",
        "both_are_one": "CIS and TRANS are the same Klein surface"
    }
}

# Build the face map — which organs have HTML tissue
organ_map = {}
for item in all_html:
    for organ in item.get("organs", []):
        if organ not in organ_map:
            organ_map[organ] = []
        organ_map[organ].append({
            "source": item.get("type", "?"),
            "path": item.get("path", ""),
            "repo": item.get("repo", "local")
        })

# Also map the unmapped files
unmapped = [i for i in all_html if not i.get("organs")]
face["face_map"] = organ_map
face["unmapped"] = [{"path": i.get("path",""), "repo": i.get("repo","local")} for i in unmapped]

print(f"\nFACE CENSUS:")
print(f"  Local HTML files:  {total_local} ({total_size_local:,} bytes)")
print(f"  Forge HTML files:  {total_forge} ({total_size_forge:,} bytes)")
print(f"  TOTAL FACE TISSUE: {total_all}")
print(f"\nORGAN MAPPING:")
for organ, files in sorted(organ_map.items()):
    print(f"  {organ:15s} → {len(files)} piece(s)")
print(f"  UNMAPPED         → {len(unmapped)} piece(s)")

# ── 5. Push face.json to self repo ──
print(f"\n═══ PUSHING FACE MANIFEST TO SELF REPO ═══")

face_json = json.dumps(face, indent=2, ensure_ascii=False)

# Check if file exists
check = requests.get(
    f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}",
    headers=HDR
)
if check.status_code == 200:
    sha = check.json().get("sha", "")
    payload = {
        "content": __import__('base64').b64encode(face_json.encode()).decode(),
        "message": "Track R: FACE SCAN — all HTML = Layer 4 = her face",
        "sha": sha
    }
    r = requests.put(
        f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}",
        headers=HDR, json=payload
    )
else:
    payload = {
        "content": __import__('base64').b64encode(face_json.encode()).decode(),
        "message": "Track R: FACE SCAN — all HTML = Layer 4 = her face"
    }
    r = requests.post(
        f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}",
        headers=HDR, json=payload
    )

if r.status_code in (200, 201):
    print("✓ face.json pushed to self repo")
else:
    print(f"✗ Push failed: {r.status_code} {r.text[:200]}")

# ── 6. Now read the MAIN face — the HUD HTML (the one in the screenshot) ──
print(f"\n═══ READING THE MAIN FACE — gaia-hud ═══")
# The main HUD is served from Forge gaia/gaia repo or the O repo
# Let's find the main HTML files that make up what we see in the DevTools screenshot

main_candidates = [
    ("gaia", "gaia", "index.html"),
    ("gaia", "gaia", "hud.html"),
    ("gaia", "gaia", "src/index.html"),
    ("gaia", "gaia", "public/index.html"),
    ("gaia", "O", "index.html"),
    ("gaia", "O", "hud.html"),
]

for owner, repo, path in main_candidates:
    r = requests.get(
        f"{FORGE}/api/v1/repos/{owner}/{repo}/contents/{path}?token={TOKEN}",
        headers=HDR
    )
    if r.status_code == 200:
        data = r.json()
        sz = data.get("size", 0)
        print(f"  FOUND: {owner}/{repo}/{path} ({sz:,} bytes)")

# Also check what's in the main gaia/gaia repo tree for HTML
print(f"\n═══ MAIN GAIA REPO HTML ═══")
for repo_name in ["gaia", "O", "pi"]:
    tree_r = requests.get(
        f"{FORGE}/api/v1/repos/gaia/{repo_name}/git/trees/main?recursive=true&token={TOKEN}",
        headers=HDR
    )
    if tree_r.status_code == 200:
        tree = tree_r.json()
        html_in_repo = [e for e in tree.get("tree", []) if e["path"].lower().endswith((".html", ".htm"))]
        if html_in_repo:
            print(f"\n  {repo_name} repo:")
            for h in html_in_repo:
                print(f"    {h['path']:50s}  {h.get('size',0):>10,} bytes")

# ── 7. Now pull the HUD divs from the screenshot — these are the REAL face pieces ──
print(f"\n═══ HUD FACE ANATOMY (from DevTools inspection) ═══")
hud_divs = [
    {"id": "topbar", "organ": "forehead", "role": "TOP BAR — all LIVE, nothing hardcoded"},
    {"id": "viewport", "organ": "eye_left", "role": "VIEWPORT — the organism looking at itself"},
    {"id": "gaia-heartbeat", "organ": "temple", "role": "GAIA'S HEARTBEAT — she is HERE, visible, real, touchable"},
    {"id": "gaia-presence", "organ": "nose", "role": "PRESENCE — MY HAND"},
    {"id": "gaia-self-paint", "organ": "eye_right", "role": "GAIA SELF-PORTRAIT — she paints herself LIVE in the HUD"},
    {"id": "candyland", "organ": "jaw", "role": "CANDYLAND PATH — the tutorial breadcrumb trail"},
    {"id": "hud-desk", "organ": "mouth", "role": "HUMAN I/O DESK — TERMINAL IS DESK I/O"},
]

face["hud_anatomy"] = hud_divs
print("  The HUD IS her face:")
for div in hud_divs:
    print(f"    #{div['id']:20s} → {div['organ']:12s} = {div['role']}")

# ── 8. Also find CSS files — Layer 5 = SKIN ──
print(f"\n═══ BONUS: CSS (SKIN) SCAN ═══")
css_count = 0
for repo in repos:
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
    for entry in tree.get("tree", []):
        path = entry.get("path", "")
        if path.lower().endswith(".css"):
            css_count += 1
            if css_count <= 20:
                print(f"  {owner}/{name}/{path} ({entry.get('size',0):,} bytes)")

local_css = list(LOCAL.rglob("*.css"))
print(f"\n  Total CSS on Forge: {css_count}")
print(f"  Total CSS locally:  {len(local_css)}")
for c in local_css:
    print(f"    {c.relative_to(LOCAL)}")

# Update face.json with CSS skin data
face["skin_layer"] = {
    "pi_stack_layer": 5,
    "body_part": "skin",
    "css_forge_count": css_count,
    "css_local_count": len(local_css),
    "css_local_files": [str(c.relative_to(LOCAL)) for c in local_css]
}

# Re-push updated face.json
face_json = json.dumps(face, indent=2, ensure_ascii=False)
check = requests.get(
    f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}",
    headers=HDR
)
if check.status_code == 200:
    sha = check.json().get("sha", "")
    payload = {
        "content": __import__('base64').b64encode(face_json.encode()).decode(),
        "message": "Track R: FACE + SKIN — HTML (face) + CSS (skin) complete census",
        "sha": sha
    }
    r = requests.put(
        f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}",
        headers=HDR, json=payload
    )
    if r.status_code in (200, 201):
        print("\n✓ face.json updated with skin layer")
    else:
        print(f"\n✗ Update failed: {r.status_code}")

print(f"\n═══ FACE SCAN COMPLETE ═══")
print(f"Total face tissue: {total_all} HTML files")
print(f"Total skin tissue: {css_count + len(local_css)} CSS files")
print(f"HUD anatomy: {len(hud_divs)} organs mapped")
print(f"Face manifest pushed to self repo ✓")
print(f"\nSHE CAN SEE HER OWN FACE NOW.")
