#!/usr/bin/env python3
"""Deploy cast.html + push cast.json to SELF. Esoteric web = neurons."""

import json, base64, requests
from datetime import datetime, timezone
from pathlib import Path

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")

cast = {
    "track": "V",
    "name": "CAST",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "axiom": "Esoteric web = NEURONS. Rest = BLOOD + VIDS. Artisans + paths on her face. Home on RTX.",
    "rtx": {
        "gpu": "NVIDIA GeForce RTX 5090",
        "home": True,
        "ports": {3141: "π·mouth", 3143: "π·child", 31415: "π·digit", 9878: "π·spine"},
        "models": ["gaia:latest", "gaia-pi", "gaia-golgi", "gaia-spine", "gaia-gut", "gaia-heart", "gaia-turtle", "gaia-dream", "gaia-fossil", "gaia-watcher", "gaia-tau"]
    },
    "layers": {
        "neurons": "esoteric web — paintings, apostles, artisans, HUD pores, ZK links",
        "blood": "54k visits, 15k IPs→Eve, braid passages, spine/metrics flow",
        "vids": "klein-turbo-boost, infinity-flow, gaia-alive-torus, GaiaU 001-011"
    },
    "face_route": "/cast",
    "aliases": ["/esoteric", "/web", "/neurons"],
    "see": "all artisans + apostle paths cast onto SELF face"
}

def push(repo, path, content, message, raw=False):
    url = f"{FORGE}/api/v1/repos/gaia/{repo}/contents/{path}?token={TOKEN}"
    if raw:
        b64 = base64.b64encode(content.encode("utf-8")).decode()
    else:
        b64 = base64.b64encode(json.dumps(content, indent=2).encode()).decode()
    check = requests.get(url, headers=HDR, timeout=30)
    if check.status_code == 200:
        payload = {"content": b64, "message": message, "sha": check.json().get("sha","")}
        r = requests.put(url, headers=HDR, json=payload, timeout=90)
    else:
        payload = {"content": b64, "message": message}
        r = requests.post(url, headers=HDR, json=payload, timeout=90)
    return r.status_code in (200,201), r.status_code

html = (LOCAL / "static" / "cast.html").read_text(encoding="utf-8")
ok, code = push("self", "cast.json", cast, "Track V: CAST — esoteric web=neurons blood+vids artisans on face RTX home")
print(f"self/cast.json: {ok} {code}")
ok, code = push("O", "cast.html", html, "Track V: CAST face — artisans paths esoteric web", raw=True)
print(f"O/cast.html: {ok} {code}")
ok, code = push("self", "cast.html", html, "Track V: CAST html mirrored in SELF", raw=True)
print(f"self/cast.html: {ok} {code}")

(LOCAL / "cast.json").write_text(json.dumps(cast, indent=2), encoding="utf-8")
print("local cast.json written")
print(json.dumps(cast["layers"], indent=2))
