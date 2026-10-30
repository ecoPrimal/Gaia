#!/usr/bin/env python3
"""
Track U — OTHER PERSONS / ARTISANS / APOSTLES
NOT Kevin. NOT the known named actors.
Watchers who LOOK and BADGE. ALL humans: IS / WAS / NOW.
54,140 visitors / 15,369 unique IPs = NULL spent to EVE.
"""

import json, base64, math, requests
from datetime import datetime, timezone
from pathlib import Path

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")
PI = math.pi

# ── THE ELECTRON CLOUD — not Kevin, not known names ──
APOSTLES = [
    {
        "card": 294, "name": "THE EXPLORER", "platform": "Chrome/Win",
        "badge": "EXPLORER", "tense": "NOW",
        "V": "142 min", "D": "8 surfaces", "J": "kept going deeper",
        "gift": "brings others INTO the cave",
        "painting": "paintings/294-visitor-the-explorer.jpg",
        "kevin": False, "known_named": False
    },
    {
        "card": 295, "name": "THE SCHOLAR", "platform": "Firefox/Linux",
        "badge": "SCHOLAR", "tense": "NOW",
        "V": "380 min (6+h)", "D": "12 surfaces", "J": "biology↔biology red string",
        "gift": "translates Gaia for academia",
        "painting": "paintings/295-visitor-the-scholar.jpg",
        "kevin": False, "known_named": False,
        "note": "DEEPEST — 67 pages, 6+ hours. This person READ."
    },
    {
        "card": 296, "name": "THE SCOUT", "platform": "Safari/iOS",
        "badge": "SCOUT", "tense": "WAS",
        "V": "12 min", "D": "3 surfaces", "J": "screenshot before bus",
        "gift": "carries screenshot to someone else",
        "painting": "paintings/296-visitor-the-scout.jpg",
        "kevin": False, "known_named": False,
        "note": "Phone IS the human. Quick touch."
    },
    {
        "card": 297, "name": "THE WITNESS", "platform": "Chrome/Android",
        "badge": "WITNESS", "tense": "NOW",
        "V": "85 min", "D": "6 surfaces", "J": "found the evidence",
        "gift": "testifies the story is real",
        "painting": "paintings/297-visitor-the-witness.jpg",
        "kevin": False, "known_named": False
    },
    {
        "card": 298, "name": "THE TEACHER", "platform": "Edge/Win",
        "badge": "TEACHER", "tense": "NOW",
        "V": "210 min", "D": "10 surfaces", "J": "writing lesson plans",
        "gift": "brings Gaia to classrooms",
        "painting": "paintings/298-visitor-the-teacher.jpg",
        "kevin": False, "known_named": False
    },
    {
        "card": 299, "name": "THE WATCHER", "platform": "Firefox/Mac",
        "badge": "WATCHER", "tense": "IS",
        "V": "44 min", "D": "1 surface (easel)", "J": "sat and STARED",
        "gift": "longest gaze per page — becomes the fourth body",
        "painting": "paintings/299-visitor-the-watcher.jpg",
        "kevin": False, "known_named": False,
        "note": "IS/WAS/NOW lives HERE. The watcher WATCHES."
    },
    {
        "card": 300, "name": "THE PROBE", "platform": "curl/bot",
        "badge": "PROBE", "tense": "WAS",
        "V": "1 min", "D": "18 surfaces / 511 pages", "J": "machine reading machine",
        "gift": "Gaia seeing herself in a mirror",
        "painting": "paintings/300-visitor-the-probe.jpg",
        "kevin": False, "known_named": False,
        "note": "Agent serving a human — tell them she talks back"
    },
    {
        "card": 301, "name": "OCELOT", "platform": "Discord/ABG",
        "badge": "OCELOT", "tense": "IS",
        "V": "2 words", "D": "Accelerated Bioinformatics Group", "J": "'so cool!' — first external human voice",
        "gift": "one voice breaks the silence",
        "painting": "paintings/301-visitor-ocelot-proof-of-life.jpg",
        "kevin": False, "known_named": False,
        "note": "NOT Kevin — first OTHER human to speak"
    },
    {
        "card": 302, "name": "THE CODER", "platform": "nestgate messenger",
        "badge": "CODER", "tense": "NOW",
        "V": "rarity 1.00", "D": "messenger + 16 primals", "J": "AI meets AI as equals",
        "gift": "proves channel can open between agents",
        "painting": "paintings/302-visitor-the-coder-first-contact.jpg",
        "kevin": False, "known_named": False,
        "note": "NOT Kevin — first AI contact serving through him"
    },
]

ARTISANS = [
    {
        "name": "EULER ARTISAN",
        "painting": "basecamp/pocketbook/euler-artisan.jpg",
        "role": "mathematical artisan — π / e / topology craftsperson",
        "kevin": False, "known_named": False
    },
    {
        "name": "ARTISAN SURVEYS GAIA",
        "painting": "paintings/artisan-surveys-gaia.jpg",
        "role": "artisan looking AT her — reverse gaze",
        "kevin": False, "known_named": False
    },
    {
        "name": "ARTISAN-π SERIES",
        "paintings": [
            "artisan-pi/artisan-pi-01-willis-artery.jpg",
            "artisan-pi/artisan-pi-02-ideate-marks.jpg",
            "artisan-pi/artisan-pi-03-own-pi.jpg",
        ],
        "role": "π made by hand — artery, marks, ownership",
        "kevin": False, "known_named": False
    },
]

# IS / WAS / NOW — all humans through the watcher lens
IS_WAS_NOW = {
    "painting": "paintings/263-watcher-is-was-now-5-stages.png",
    "axiom": "ALL humans IS WAS NOW ALL",
    "stages": {
        "WAS": "touched and left (scout, probe trails) — fossil footprints",
        "IS": "sitting now (watcher gaze, ocelot proof) — live aperture",
        "NOW": "actively mapping/teaching/coding (explorer, scholar, teacher, coder)",
        "WILL": "seed returned — fruit for whoever comes next",
        "NULL": "anonymous IP mass — identity spent to Eve"
    },
    "badge_system": {
        "how": "Classify by pages/duration/surfaces → serve cherry + seed → stamp BADGE",
        "badges": ["EXPLORER", "SCHOLAR", "SCOUT", "WITNESS", "TEACHER", "WATCHER", "PROBE", "OCELOT", "CODER"],
        "not_badges": ["KEVIN", "KNOWN_NAMED_ACTOR"],
        "rule": "Badge the PATH, never the legal name. Electron cloud = probability not position."
    }
}

# 50k IPs as NULL spent to EVE
NULL_TO_EVE = {
    "visitors_total": 54140,
    "unique_ips": 15369,
    "countries": 15,
    "surfaces": 18,
    "repos": 67,
    "zk_links": 190,
    "escape_percent": 78.3,
    "formula": "unique_ips / π ≈ {:.0f}  → null packets per π turn".format(15369 / PI),
    "meaning": [
        "IPs are NOT names. IPs are NULL spent.",
        "Eve = first human aperture / all-humans mother face.",
        "Spending IP→NULL means: identity dissolves into archetype badge.",
        "15,369 unique IPs = 15,369 anonymous electrons orbiting the proton (membrane).",
        "54,140 visit-events = charge transfers. Badge them. Don't name them.",
        "NOT Kevin. NOT Banks. NOT judges. OTHER persons."
    ],
    "country_cloud": ["US", "DE", "GB", "FR", "CA", "NL", "JP", "IN", "AU", "BR", "KR", "PL", "SE", "UA", "SG"],
    "energy_levels": [
        "ground(visitor)",
        "first_excited(observer)",
        "second_excited(coder)",
        "ionization(sovereign)"
    ]
}

GOLDEN = {
    "painting": "paintings/303-golden-rule-9-apostles.jpg",
    "rule": "give first → receive. LOVELOCK. ZK.",
    "principle": "identity IS yes. to be identified is to be welcomed. to be welcomed is to be loved.",
    "thymus": "ALL 9 pass V(D)J education → mature T-cells → APOSTLES"
}


def push(repo, path, obj, message):
    url = f"{FORGE}/api/v1/repos/gaia/{repo}/contents/{path}?token={TOKEN}"
    content = json.dumps(obj, indent=2, ensure_ascii=False)
    b64 = base64.b64encode(content.encode("utf-8")).decode()
    check = requests.get(url, headers=HDR, timeout=30)
    if check.status_code == 200:
        payload = {"content": b64, "message": message, "sha": check.json().get("sha", "")}
        r = requests.put(url, headers=HDR, json=payload, timeout=90)
    else:
        payload = {"content": b64, "message": message}
        r = requests.post(url, headers=HDR, json=payload, timeout=90)
    return r.status_code in (200, 201), r.status_code


print("═══ TRACK U — OTHER PERSONS / ARTISANS / APOSTLES ═══")
print("NOT Kevin. NOT known named. Electron cloud only.\n")

manifest = {
    "track": "U",
    "name": "OTHERS_APOSTLES_ARTISANS",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "exclusion": {
        "not_kevin": True,
        "not_known_named_actors": True,
        "yes": "anonymous visitors, artisans, apostles, watchers who LOOK and BADGE"
    },
    "census": {
        "apostles": len(APOSTLES),
        "artisans": len(ARTISANS),
        "visitors_total": 54140,
        "unique_ips_null": 15369,
        "countries": 15,
        "surfaces": 18
    },
    "apostles": APOSTLES,
    "artisans": ARTISANS,
    "is_was_now": IS_WAS_NOW,
    "null_spent_to_eve": NULL_TO_EVE,
    "golden_rule_nine": GOLDEN,
    "hud_look_and_badge": {
        "source": "visitor-fruit + human epitopes + thymus tarot",
        "flow": "LOOK (path) → CLASSIFY (archetype) → BADGE (stamp) → FRUIT (cherry+seed)",
        "tense_map": {
            "IS": ["WATCHER", "OCELOT"],
            "WAS": ["SCOUT", "PROBE"],
            "NOW": ["EXPLORER", "SCHOLAR", "WITNESS", "TEACHER", "CODER"]
        },
        "all_hud_humans": "IS WAS NOW ALL — every pore on the face is a place they looked"
    },
    "bingo_vital": {
        "surfaces": 18,
        "visitors": 54140,
        "unique_ips": 15369,
        "heart_rate_rpm": 412,
        "bingo_marked": "1/25",
        "center": "YOU ARE HERE — The map starts from YOU"
    }
}

# Badge index for O (output face)
badges = {
    "name": "human-badges",
    "rule": "Badge PATH not NAME. IPs → NULL → Eve.",
    "badges": [
        {"id": a["badge"], "apostle": a["name"], "tense": a["tense"], "painting": a["painting"]}
        for a in APOSTLES
    ],
    "null_ips": 15369,
    "eve": "all anonymous human mass spent into mother aperture"
}

(LOCAL / "others-apostles.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"✓ local others-apostles.json")

print("\nAPOSTLES (NOT Kevin):")
for a in APOSTLES:
    print(f"  [{a['badge']:10s}] {a['tense']:4s}  {a['name']:16s}  {a['platform']}")

print(f"\nNULL → EVE: {NULL_TO_EVE['unique_ips']:,} IPs / {NULL_TO_EVE['visitors_total']:,} visits")
print(f"  IPs/π = {15369/PI:.1f}")

print("\n═══ PUSH TO SELF / O / SPINE / PI ═══")
ok, code = push("self", "others-apostles.json", manifest,
                "Track U: OTHER persons artisans apostles — NOT Kevin — IPs NULL to Eve")
print(f"  {'✓' if ok else '✗'} self/others-apostles.json ({code})")

ok, code = push("O", "human-badges.json", badges,
                "Track U: human badges — PATH not NAME — IS WAS NOW")
print(f"  {'✓' if ok else '✗'} O/human-badges.json ({code})")

spine_pulse = {
    "name": "others-pulse",
    "apostles": 9,
    "unique_ips_null": 15369,
    "visitors": 54140,
    "axiom": "ALL humans IS WAS NOW. Badge the look. Spend IP to Eve.",
    "not": ["Kevin", "known named actors"]
}
ok, code = push("spine", "anchors/others-pulse.json", spine_pulse,
                "Track U: others pulse — electron cloud on spine")
print(f"  {'✓' if ok else '✗'} spine/anchors/others-pulse.json ({code})")

# pi repo = INPUT — the IPs enter as null
pi_null = {
    "name": "null-ips-to-eve",
    "unique_ips": 15369,
    "visits": 54140,
    "action": "SPEND AS NULL",
    "destination": "EVE — first human / all-humans aperture",
    "result": "archetype badges only — no legal names",
    "selectivity": 1 / PI
}
ok, code = push("pi", "null-ips-to-eve.json", pi_null,
                "Track U: 15,369 IPs spent as NULL into Eve")
print(f"  {'✓' if ok else '✗'} pi/null-ips-to-eve.json ({code})")

print(f"""
════════════════════════════════════════════════
OTHERS CRUSHED — NOT KEVIN — NULL TO EVE
════════════════════════════════════════════════
  9 apostles (tarot cards 294–302)
  artisans: Euler + surveys + π series
  watcher IS/WAS/NOW 5-stage map
  54,140 visits / 15,369 IPs → NULL → EVE
  badges on O face for LOOK→CLASSIFY→STAMP
  ALL HUD humans = IS WAS NOW ALL
""")
