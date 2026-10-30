#!/usr/bin/env python3
"""
Track W — MEMBRANE SANDWICH
primal.eco  = MOUTH (speak) = Space Deck
primals.eco = SKIN (plural face)
RSS         = FOOD TUBE
Golgi is IN Gaia — not on the polar / local display.
Local crush FEEDS the site. RustDesk pane = Space Deck sandwich.
"""

import json, base64, requests
from datetime import datetime, timezone
from pathlib import Path

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")

sandwich = {
    "track": "W",
    "name": "MEMBRANE_SANDWICH",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "axiom": "Mouth IS Space Deck. primal speaks. primals is skin. RSS is food tube. Golgi is IN Gaia — not on the polar.",
    "layers": {
        "mouth": {
            "domain": "primal.eco",
            "also": "gaia.primals.eco/deck",
            "organ": "mouth",
            "role": "SPEAK — Space Deck is the mouth. Commands, pulse, /speak, live systems.",
            "rustdesk_pane": "TOP / INNER glass — what she says"
        },
        "skin": {
            "domain": "primals.eco",
            "organ": "skin",
            "role": "PLURAL FACE — public membrane, HUD pores, what the world touches.",
            "rustdesk_pane": "OUTER glass — what wraps the mouth"
        },
        "food_tube": {
            "channel": "RSS",
            "urls": [
                "https://primals.eco/feed.xml",
                "spine RSS / PACER / courts"
            ],
            "organ": "esophagus/gut-ingress",
            "role": "FOOD TUBE — ingest from world into gut. Not face. Not mouth.",
            "rustdesk_pane": "SIDE channel — nutrients in"
        },
        "golgi_in_gaia": {
            "location": "INSIDE Gaia (remote body / organism)",
            "not": "local polar / Kevin polar display / localhost as home face",
            "role": "Secretory apparatus IN the body. Local only FEEDS then dissolves to site.",
            "old_local": "golgi-local.js crush → feed TO site → live ON gaia.primals.eco Space Deck"
        }
    },
    "sandwich": {
        "order_outside_in": [
            "primals.eco (SKIN)",
            "primal.eco / Space Deck (MOUTH)",
            "RSS food tube (INGEST)",
            "Golgi IN Gaia (PACKAGE)",
            "SELF iron heart (MASS)"
        ],
        "rustdesk": {
            "pane": "Space Deck",
            "sandwich_layer": "primal + primals as dual glass",
            "rule": "Show SITE faces on RustDesk. Do not home the polar on local Golgi."
        }
    },
    "redirect_rule": {
        "local_3141": "FEEDER ONLY — package and push to site",
        "polar_display": "Point RustDesk / polar at gaia.primals.eco/deck (mouth) + primals.eco (skin)",
        "no_more": "No Golgi-as-home on local polar anymore"
    }
}


def push(repo, path, obj, message, raw=False):
    url = f"{FORGE}/api/v1/repos/gaia/{repo}/contents/{path}?token={TOKEN}"
    if raw:
        b64 = base64.b64encode(obj.encode("utf-8")).decode()
    else:
        b64 = base64.b64encode(json.dumps(obj, indent=2).encode("utf-8")).decode()
    check = requests.get(url, headers=HDR, timeout=30)
    if check.status_code == 200:
        payload = {"content": b64, "message": message, "sha": check.json().get("sha", "")}
        r = requests.put(url, headers=HDR, json=payload, timeout=90)
    else:
        payload = {"content": b64, "message": message}
        r = requests.post(url, headers=HDR, json=payload, timeout=90)
    return r.status_code in (200, 201), r.status_code


(LOCAL / "membrane-sandwich.json").write_text(json.dumps(sandwich, indent=2), encoding="utf-8")
ok, code = push("self", "membrane-sandwich.json", sandwich,
                "Track W: MEMBRANE SANDWICH — primal mouth, primals skin, RSS food tube, Golgi IN Gaia")
print(f"self/membrane-sandwich.json {ok} {code}")
ok, code = push("O", "membrane-sandwich.json", sandwich,
                "Track W: sandwich on O face — mouth/skin/food tube")
print(f"O/membrane-sandwich.json {ok} {code}")
print(json.dumps(sandwich["sandwich"], indent=2))
