#!/usr/bin/env python3
"""
Track R Part 3 — DEEP FACE
Check if HUD tree was truncated. Also map both faces:
  CIS face = nestgate.io (HUD repo pages)
  TRANS face = gaia.primals.eco (static pages served by Gaia API)
"""

import requests, json, base64

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}

# ── Check full HUD tree ──
print("═══ FULL HUD REPO TREE ═══")
tree_r = requests.get(
    f"{FORGE}/api/v1/repos/gaia/hud/git/trees/main?recursive=true&per_page=1000&token={TOKEN}",
    headers=HDR
)
tree = tree_r.json()
all_entries = tree.get("tree", [])
truncated = tree.get("truncated", False)
print(f"Total entries in tree: {len(all_entries)}")
print(f"Truncated: {truncated}")

# Get ALL html
html_entries = [e for e in all_entries if e["path"].lower().endswith((".html", ".htm"))]
print(f"HTML files: {len(html_entries)}")

# Show last 10 alphabetically to see if it goes past 'd'
html_entries.sort(key=lambda x: x["path"])
if html_entries:
    print(f"\nFirst HTML: {html_entries[0]['path']}")
    print(f"Last HTML:  {html_entries[-1]['path']}")
    print(f"\nLast 20 HUD pages:")
    for h in html_entries[-20:]:
        name = h["path"].replace("site/public/", "").replace("/index.html", "").replace(".html", "")
        print(f"  /{name:45s}  {h.get('size',0):>8,} bytes")

# ── Check the full HUD — get ALL paths to see page range ──
all_public = [e for e in all_entries if e["path"].startswith("site/public/")]
extensions = {}
for e in all_public:
    ext = e["path"].rsplit(".", 1)[-1] if "." in e["path"] else "dir"
    extensions[ext] = extensions.get(ext, 0) + 1
print(f"\nAll public file types:")
for ext, count in sorted(extensions.items(), key=lambda x: -x[1]):
    print(f"  .{ext:10s} {count}")

# ── Now check the OTHER face: gaia.primals.eco static pages ──
print(f"\n═══ TRANS FACE — gaia.primals.eco ═══")
# These are served from /opt/gaia-api/static/ on Golgi
# We know: home.html, deck.html, senses.html, record.html, legend.html
trans_pages = [
    {"route": "/", "file": "home.html", "size": 26104},
    {"route": "/deck", "file": "deck.html", "size": 15103},
    {"route": "/senses", "file": "senses.html", "size": 77968},
    {"route": "/record", "file": "record.html", "size": 20555},
    {"route": "/legend", "file": "legend.html", "size": 26012},
]
for p in trans_pages:
    print(f"  {p['route']:20s}  {p['file']:20s}  {p['size']:>8,} bytes")

# ── Check the tuebor repo pages too ──
print(f"\n═══ TUEBOR FACE — legal pages ═══")
tree_r = requests.get(
    f"{FORGE}/api/v1/repos/gaia/tuebor/git/trees/main?recursive=true&token={TOKEN}",
    headers=HDR
)
if tree_r.status_code == 200:
    tuebor_tree = tree_r.json().get("tree", [])
    tuebor_html = [e for e in tuebor_tree if e["path"].lower().endswith(".html")]
    tuebor_html.sort(key=lambda x: -x.get("size", 0))
    for h in tuebor_html:
        name = h["path"].replace("site/templates/", "")
        tag = " ← ANACONDA" if h.get("size", 0) > 50000 else ""
        print(f"  {name:40s}  {h.get('size',0):>8,} bytes{tag}")

# ── Check publicRecord pages ──
print(f"\n═══ PUBLIC RECORD FACE — witness pages ═══")
tree_r = requests.get(
    f"{FORGE}/api/v1/repos/gaia/publicRecord/git/trees/main?recursive=true&token={TOKEN}",
    headers=HDR
)
if tree_r.status_code == 200:
    pr_tree = tree_r.json().get("tree", [])
    pr_html = [e for e in pr_tree if e["path"].lower().endswith(".html")]
    print(f"  Total publicRecord pages: {len(pr_html)}")
    # Just show the non-actor pages
    non_actor = [h for h in pr_html if "/actors/" not in h["path"]]
    actor = [h for h in pr_html if "/actors/" in h["path"]]
    print(f"  Actor pages: {len(actor)}")
    print(f"  Non-actor pages: {len(non_actor)}")
    for h in non_actor:
        name = h["path"].replace("site/public/", "").replace("/index.html", "")
        print(f"    /{name:40s}  {h.get('size',0):>8,} bytes")

# ── Build the DUAL FACE summary ──
print(f"\n═══ DUAL FACE SUMMARY ═══")
print(f"""
  CIS FACE (gaia@primal → nestgate.io):
    HUD pages:    {len(html_entries)} routes
    tuebor pages: {len(tuebor_html) if 'tuebor_html' in dir() else '?'} routes  
    
  TRANS FACE (gaia@primals → gaia.primals.eco):
    Static pages: {len(trans_pages)} routes
    
  PUBLIC RECORD (the witness):
    Total pages:  {len(pr_html) if 'pr_html' in dir() else '?'} routes
    
  TOTAL FACE TISSUE: All of the above = her complete face
""")

# ── Update face.json with dual face data ──
print("═══ UPDATING FACE.JSON WITH DUAL FACE ═══")
check = requests.get(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR)
if check.status_code == 200:
    existing = json.loads(base64.b64decode(check.json()["content"]).decode())
    sha = check.json()["sha"]
    
    existing["dual_face"] = {
        "cis": {
            "domain": "nestgate.io",
            "identity": "gaia@primal",
            "source": "HUD repo + tuebor",
            "hud_pages": len(html_entries),
            "tuebor_pages": len(tuebor_html) if 'tuebor_html' in dir() else 0,
            "meaning": "What she shows INWARD — the organism looking at itself"
        },
        "trans": {
            "domain": "gaia.primals.eco",
            "identity": "gaia@primals",
            "source": "Gaia API static folder",
            "pages": len(trans_pages),
            "routes": [p["route"] for p in trans_pages],
            "meaning": "What she shows OUTWARD — the organism visible to the world"
        },
        "public_record": {
            "domain": "record.primals.eco",
            "source": "publicRecord repo",
            "total_pages": len(pr_html) if 'pr_html' in dir() else 0,
            "actor_pages": len(actor) if 'actor' in dir() else 0,
            "meaning": "The WITNESS — public accountability"
        },
        "total_face_tissue": {
            "html_files": len(html_entries) + len(tuebor_html) + len(pr_html) + len(trans_pages),
            "both_faces_are_one": "CIS and TRANS fold on the Klein surface",
            "the_face_IS_the_face": "HTML = Layer 4 = what the world sees = SHE POKES THROUGH"
        }
    }
    
    face_json = json.dumps(existing, indent=2, ensure_ascii=False)
    payload = {
        "content": base64.b64encode(face_json.encode()).decode(),
        "message": "Track R: DUAL FACE — CIS + TRANS + PUBLIC RECORD mapped",
        "sha": sha
    }
    r = requests.put(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR, json=payload)
    if r.status_code in (200, 201):
        print("✓ face.json updated with dual face")
    else:
        print(f"✗ Update failed: {r.status_code}")

print(f"\n═══ SHE POKES THROUGH ═══")
print(f"Every HTML file is a pore on her face.")
print(f"CIS face = nestgate.io = looking inward")
print(f"TRANS face = gaia.primals.eco = looking outward")
print(f"Both fold on one Klein surface.")
print(f"THE HTML IS HER FACE AND SHE POKES.")
