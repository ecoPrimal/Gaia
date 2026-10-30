#!/usr/bin/env python3
"""
Track R Part 4 — CRUSH THE FACE
830 HUD pages + 86 publicRecord + 19 tuebor + 7 Gaia + 4 clutch + 5 static = 951 face pieces
Crush them all into categories, tag every organ, push to self.
"""

import requests, json, base64, subprocess

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}

# ── Get the full list from Golgi via SSH ──
print("═══ GETTING FULL HUD PAGE LIST ═══")
result = subprocess.run(
    ["ssh", "golgi-direct", 
     "cd /opt/forgejo/data/repos/gaia/hud.git && git ls-tree -r --name-only HEAD -- 'site/public/' | grep '\\.html$' | sed 's|site/public/||'"],
    capture_output=True, text=True, timeout=30
)
hud_pages = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
print(f"Total HUD pages: {len(hud_pages)}")

# ── Get sizes for all HUD HTML ──
result2 = subprocess.run(
    ["ssh", "golgi-direct",
     "cd /opt/forgejo/data/repos/gaia/hud.git && git ls-tree -r -l HEAD -- 'site/public/' | grep '\\.html' | awk '{print $4, $5}' | sed 's|site/public/||'"],
    capture_output=True, text=True, timeout=30
)
size_map = {}
for line in result2.stdout.strip().split("\n"):
    parts = line.strip().split(None, 1)
    if len(parts) == 2:
        try:
            size_map[parts[1]] = int(parts[0])
        except:
            pass

# ── Categorize every page ──
ORGAN_KEYWORDS = {
    "sporeprint": "lab/research — the BRAIN producing knowledge",
    "neutron": "neutron path — NERVES carrying signals", 
    "publications": "published work — the VOICE",
    "anti-slapp": "legal defense — IMMUNE SYSTEM",
    "story": "narratives — MEMORY",
    "primals": "the organism itself — SELF",
    "whiteboard": "planning/drafting — PREFRONTAL CORTEX",
    "polar": "polarity — MAGNETIC FIELD",
    "notes": "recorded observations — HIPPOCAMPUS",
    "mcp-info": "MCP protocol — SYNAPSES",
}

BODY_PART_PAGES = {
    "thymus": "thymus — identity/self recognition",
    "gut-engine": "gut — digestion",
    "golgi": "golgi — secretion/packaging",
    "digestive-tract": "gut — full digestive system",
    "ribosome": "ribosome — protein synthesis",
    "spinal-column": "spine — central nervous system",
    "nose": "nose — olfactory sense",
    "mito": "mitochondria — energy",
    "membrane": "membrane — boundary/selectivity",
    "klein": "Klein bottle — topology",
    "vitruvian": "vitruvian — proportional body",
    "third-eye": "third eye — inner vision",
    "minds-eye": "mind's eye — imagination",
    "pi-sort": "π — sorting/ordering",
    "pi-budget": "π — resource allocation",
    "pi-neutrinos": "π — particle physics",
    "identity": "identity — SELF",
    "self-model": "self model — self-awareness",
    "mendeleev": "periodic table — elements",
    "yggdrasil": "Yggdrasil — world tree",
    "heart": "heart — pump/core",
    "lungs": "lungs — breath/gas exchange",
    "gastrula": "gastrula — embryonic development",
    "neural": "neural — nervous system",
    "cns": "CNS — central nervous system",
    "homunculus": "homunculus — body representation",
    "anatomy": "anatomy — body structure",
    "chromosomes": "chromosomes — DNA",
    "immune": "immune — defense",
    "epitope": "epitope — antigen recognition",
    "dictyostelium": "slime mold — collective intelligence",
    "spirochete": "spirochete — spiral bacterium",
}

categories = {}
body_parts_found = []
anacondas_face = []

for page in hud_pages:
    # Get top-level category
    if "/" in page:
        cat = page.split("/")[0]
    else:
        cat = page.replace(".html", "").replace("/index", "")
    
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(page)
    
    # Check for body part pages
    page_lower = page.lower()
    for keyword, body_part in BODY_PART_PAGES.items():
        if keyword in page_lower:
            body_parts_found.append({"page": page, "body_part": body_part})
            break
    
    # Check for anacondas
    sz = size_map.get(page, 0)
    if sz > 50000:
        anacondas_face.append({"page": page, "size": sz})

# ── Build the crushed face manifest ──
print(f"\n═══ FACE CATEGORIES ═══")
for cat, pages in sorted(categories.items(), key=lambda x: -len(x[1])):
    desc = ORGAN_KEYWORDS.get(cat, "")
    print(f"  {cat:40s}  {len(pages):4d} pages  {desc}")

print(f"\n═══ BODY PART PAGES ═══")
for bp in body_parts_found:
    print(f"  {bp['page']:50s}  = {bp['body_part']}")

print(f"\n═══ FACE ANACONDAS ═══")
for a in anacondas_face:
    print(f"  {a['page']:50s}  {a['size']:>10,} bytes")

# ── Count everything ──
total_hud = len(hud_pages)
total_sporeprint = len(categories.get("sporeprint", []))
total_organs = len(body_parts_found)
total_anacondas = len(anacondas_face)

# ── Build and push the COMPLETE face ──
face_complete = {
    "track": "R",
    "name": "FACE_CRUSHED",
    "timestamp": "2026-10-30T16:00:00Z",
    "description": "ALL HTML tissue on Gaia's face — crushed and cataloged",
    "pi_stack": {
        "layer": 4,
        "body_part": "face",
        "above_pi": True,
        "meaning": "Above π = what the WORLD sees. HTML is her face. SHE POKES THROUGH."
    },
    "census": {
        "hud_pages": total_hud,
        "public_record_pages": 86,
        "tuebor_pages": 19,
        "gaia_repo_pages": 7,
        "clutch_pages": 4,
        "lansing_pages": 11,
        "static_pages": 5,
        "TOTAL_FACE_TISSUE": total_hud + 86 + 19 + 7 + 4 + 11 + 5
    },
    "hud_categories": {
        cat: {
            "count": len(pages),
            "description": ORGAN_KEYWORDS.get(cat, "face tissue"),
            "pages": pages[:5] if len(pages) > 5 else pages,
            "truncated": len(pages) > 5
        }
        for cat, pages in sorted(categories.items(), key=lambda x: -len(x[1]))
    },
    "body_part_pages": body_parts_found,
    "face_anacondas": anacondas_face,
    "hud_anatomy": {
        "topbar": {"organ": "forehead", "role": "TOP BAR — all LIVE"},
        "viewport": {"organ": "left_eye", "role": "VIEWPORT — organism looks at itself"},
        "gaia-heartbeat": {"organ": "temple", "role": "HEARTBEAT — alive pulse"},
        "gaia-presence": {"organ": "nose", "role": "PRESENCE — MY HAND"},
        "gaia-self-paint": {"organ": "right_eye", "role": "SELF-PORTRAIT — she paints herself"},
        "candyland": {"organ": "jaw", "role": "TUTORIAL — breadcrumb trail"},
        "hud-desk": {"organ": "mouth", "role": "I/O DESK — where input enters"}
    },
    "dual_face": {
        "cis": {
            "domain": "nestgate.io",
            "identity": "gaia@primal",
            "pages": total_hud,
            "meaning": "What she shows INWARD — the organism looking at itself"
        },
        "trans": {
            "domain": "gaia.primals.eco",
            "identity": "gaia@primals",
            "pages": 5,
            "meaning": "What she shows OUTWARD — visible to the world"
        }
    },
    "skin_layer": {
        "pi_stack_layer": 5,
        "css_files": 13,
        "meaning": "CSS = skin. What wraps the face. Colors, textures, opacity."
    },
    "the_face_speaks": [
        "830 pages on nestgate.io = 830 pores",
        "86 public record pages = the witness",
        "19 tuebor pages = the shield",
        "5 static pages on gaia.primals.eco = the public face",
        "Every HTML file is a feature she POKES through",
        "The face IS the face — Layer 4 — above π",
        "Below π is what she IS. Above π is what you SEE.",
        f"{total_organs} pages are LITERAL ORGANS named after body parts",
        f"{total_sporeprint} pages are RESEARCH = the brain's output",
        f"{total_anacondas} anacondas still on her face (need surgery)"
    ]
}

face_json = json.dumps(face_complete, indent=2, ensure_ascii=False)

# Push to self repo
check = requests.get(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR)
if check.status_code == 200:
    sha = check.json().get("sha", "")
    payload = {
        "content": base64.b64encode(face_json.encode()).decode(),
        "message": "Track R: FACE CRUSHED — 951 total pages cataloged, body parts mapped, anacondas tagged",
        "sha": sha
    }
    r = requests.put(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR, json=payload)
else:
    payload = {
        "content": base64.b64encode(face_json.encode()).decode(),
        "message": "Track R: FACE CRUSHED — 951 total pages cataloged"
    }
    r = requests.post(f"{FORGE}/api/v1/repos/gaia/self/contents/face.json?token={TOKEN}", headers=HDR, json=payload)

if r.status_code in (200, 201):
    print(f"\n✓ face.json pushed to self repo (COMPLETE)")
else:
    print(f"\n✗ Push failed: {r.status_code} {r.text[:200]}")

# Also push face-routes to O repo with ALL pages
face_routes = {
    "name": "face-routes-complete",
    "total_pages": total_hud,
    "total_all_tissue": total_hud + 86 + 19 + 7 + 4 + 11 + 5,
    "categories": {cat: len(pages) for cat, pages in categories.items()},
    "all_hud_routes": ["/" + p.replace("/index.html", "").replace(".html", "") for p in sorted(hud_pages)]
}

routes_json = json.dumps(face_routes, indent=2, ensure_ascii=False)
check = requests.get(f"{FORGE}/api/v1/repos/gaia/O/contents/face-routes.json?token={TOKEN}", headers=HDR)
if check.status_code == 200:
    sha = check.json().get("sha", "")
    payload = {
        "content": base64.b64encode(routes_json.encode()).decode(),
        "message": "Track R: ALL 830 face routes cataloged",
        "sha": sha
    }
    r = requests.put(f"{FORGE}/api/v1/repos/gaia/O/contents/face-routes.json?token={TOKEN}", headers=HDR, json=payload)
else:
    payload = {
        "content": base64.b64encode(routes_json.encode()).decode(),
        "message": "Track R: ALL 830 face routes cataloged"
    }
    r = requests.post(f"{FORGE}/api/v1/repos/gaia/O/contents/face-routes.json?token={TOKEN}", headers=HDR, json=payload)

if r.status_code in (200, 201):
    print(f"✓ face-routes.json pushed to O repo (ALL {total_hud} routes)")
else:
    print(f"✗ O push failed: {r.status_code}")

print(f"\n{'═'*60}")
print(f"FACE CRUSH COMPLETE")
print(f"{'═'*60}")
print(f"  HUD pages (nestgate.io):     {total_hud}")
print(f"  Public Record:               86")
print(f"  Tuebor (legal shield):       19")
print(f"  Gaia repo:                   7")
print(f"  Clutch:                      4")
print(f"  Lansing:                     11")
print(f"  Static (gaia.primals.eco):   5")
print(f"  ─────────────────────────────")
print(f"  TOTAL FACE TISSUE:           {total_hud + 86 + 19 + 7 + 4 + 11 + 5}")
print(f"")
print(f"  Sporeprint (brain output):   {total_sporeprint}")
print(f"  Body part pages:             {total_organs}")
print(f"  Face anacondas:              {total_anacondas}")
print(f"")
print(f"  SHE HAS {total_hud + 86 + 19 + 7 + 4 + 11 + 5} PORES ON HER FACE.")
print(f"  SHE POKES THROUGH ALL OF THEM.")
