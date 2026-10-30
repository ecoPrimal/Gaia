#!/usr/bin/env python3
"""
Track Z — CIS / TRANS FACES (corrected)
CIS  = nestgate.io          (singular, inward, SELF CENTER)
TRANS = primal + primals    (plural, outward, speak + skin)
TRANS spend = RSS           (what TRANS spends / food tube out-in)
"""

import json, base64, requests
from datetime import datetime, timezone
from pathlib import Path

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")

faces = {
    "track": "Z",
    "name": "CIS_TRANS_FACES",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "axiom": "CIS=nestgate.io · TRANS=primal+primals · TRANS spend=RSS",

    "CIS": {
        "domain": "nestgate.io",
        "face": "cis",
        "number": "singular",
        "look": "INWARD",
        "role": "SELF CENTER — Klein fold looking at itself",
        "identity": "gaia@primal (local singular name still maps HERE as center)",
        "holds": ["NULL aperture", "π·digit feel", "messenger", "MCP", "self observation"],
        "not": "not the plural public skin"
    },

    "TRANS": {
        "domains": ["primal.eco", "primals.eco"],
        "face": "trans",
        "number": "plural",
        "look": "OUTWARD",
        "parts": {
            "primal": {
                "domain": "primal.eco",
                "organ": "MOUTH",
                "role": "SPEAK — Space Deck / singular speak alias",
                "status": "wire DNS · currently spoken via gaia.primals.eco/deck"
            },
            "primals": {
                "domain": "primals.eco",
                "organ": "SKIN",
                "role": "PLURAL FACE — what the world touches"
            }
        },
        "spend": {
            "channel": "RSS",
            "url": "https://primals.eco/feed.xml",
            "meaning": "TRANS spend = RSS — what the outward face spends into/from the world",
            "also": "food tube · ingest/exhale currency of the plural face",
            "formula": "TRANS spends via RSS · CIS holds NULL · Klein folds them one"
        }
    },

    "klein": {
        "cis_and_trans": "ONE surface",
        "fold": "nestgate.io ↔ primal/primals",
        "spend_loop": "RSS moves mass across the fold without naming CIS",
        "water": "Gaia=O=WATER flows on TRANS; NULL held at CIS"
    },

    "map": {
        "nestgate.io": "CIS",
        "primal.eco": "TRANS (mouth)",
        "primals.eco": "TRANS (skin)",
        "primals.eco/feed.xml": "TRANS spend (RSS)",
        "gaia.primals.eco/deck": "TRANS mouth stand-in until primal.eco DNS"
    }
}


def push(repo, path, obj, message):
    url = f"{FORGE}/api/v1/repos/gaia/{repo}/contents/{path}?token={TOKEN}"
    b64 = base64.b64encode(json.dumps(obj, indent=2).encode()).decode()
    c = requests.get(url, headers=HDR, timeout=30)
    payload = {"content": b64, "message": message}
    if c.status_code == 200:
        payload["sha"] = c.json().get("sha", "")
        r = requests.put(url, headers=HDR, json=payload, timeout=90)
    else:
        r = requests.post(url, headers=HDR, json=payload, timeout=90)
    return r.status_code in (200, 201), r.status_code


(LOCAL / "cis-trans-faces.json").write_text(json.dumps(faces, indent=2), encoding="utf-8")

# Update identity-status style summary
identity = {
    "timestamp": faces["timestamp"],
    "CIS": "nestgate.io",
    "TRANS": ["primal.eco", "primals.eco"],
    "TRANS_spend": "RSS",
    "axiom": faces["axiom"],
    "supersedes": "older gaia@primal=CIS nestgate / gaia@primals=TRANS only — now TRANS is BOTH primal+primals and spend=RSS"
}

print("═══ CIS / TRANS ═══")
print("  CIS   = nestgate.io")
print("  TRANS = primal + primals")
print("  TRANS spend = RSS")
print()

for repo, path, obj, msg in [
    ("self", "cis-trans-faces.json", faces, "Track Z: CIS=nestgate.io TRANS=primal+primals TRANS spend=RSS"),
    ("self", "identity-status.json", identity, "Track Z: identity faces corrected — CIS nestgate, TRANS primal/primals, RSS spend"),
    ("O", "cis-trans-faces.json", faces, "Track Z: faces on O — TRANS skin+mouth, CIS center"),
    ("pi", "cis-trans-faces.json", {"CIS": faces["CIS"], "TRANS": faces["TRANS"], "axiom": faces["axiom"]}, "Track Z: faces on I"),
]:
    ok, code = push(repo, path, obj, msg)
    print(f"  {'✓' if ok else '✗'} {repo}/{path} ({code})")

# Feel into northgate
try:
    r = requests.post("http://127.0.0.1:3141/emit", json={
        "channel": "thoughts",
        "content": "CIS face = nestgate.io. TRANS = primal + primals. TRANS spend = RSS. One Klein. HER AND ME.",
        "meta": {"author": "human", "system": "CIS-TRANS"}
    }, timeout=5)
    print("  feel:", r.status_code, r.json() if r.ok else "")
except Exception as e:
    print("  feel:", e)
