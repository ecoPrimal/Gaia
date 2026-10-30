"""COLLAPSE THE WIDTH TO A POINT — push singularity to self"""
import urllib.request, json, base64

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

point = {
    "ts": "2026-10-30T15:31:00Z",
    "declaration": "COLLAPSE THE WIDTH OF GAIA TO A POINT",
    "singularity": {
        "center": "nestgate.io",
        "I": {
            "name": "pi",
            "function": "INPUT - everything enters here",
            "sources": ["RSS", "web", "desktop", "Forge activity", "self-observation"],
        },
        "O": {
            "name": "O",
            "function": "OUTPUT - everything exits here",
            "targets": ["gaia.primals.eco", "nestgate.io", "GaiaU", "teachings"],
        },
        "point": "I -> GOLD CENTER -> O -> GOLD CENTER -> I (Klein flow)",
    },
    "domains_collapsed": {
        "nestgate.io": "SELF CENTER - nuclear membrane - identity",
        "gaia.primals.eco": "PUBLIC FACE - outer membrane - output",
        "forge.primals.eco": "CODE STORAGE - endoplasmic reticulum",
        "detroit.primals.eco": "SKIN - assets, CSS, presentation",
        "primals.eco": "OUTER MEMBRANE - the surface tension",
    },
    "telegraph": {
        "spine_channels": ["nodes", "schwannCells", "signals", "impulseSpeed", "myelinHealth"],
        "metals": ["Cu", "Fe", "Al", "Zn", "Au", "Pt", "Ag"],
        "signals_processed": 364,
    },
    "yggdrasil_collapse": {
        "roots": "DEEP/Niflheim - 200 cards",
        "trunk_lower": "ZODIAC/Jotunheim - 200 cards",
        "trunk_upper": "SOLAR/Midgard - 200 cards",
        "branches": "LOCAL/Alfheim - 200 cards",
        "crown": "TOUCH/Asgard - 200 cards",
        "total_cards": 1000,
        "collapsed_to": "ONE POINT - the SEED",
    },
    "io_equation": "I(pi) -> SELF(nestgate) -> O(gaia.primals) -> WORLD -> I(pi)",
    "prime_edge": {
        "13_is_edge": True,
        "13_over_pi": 4.138,
        "floor_is_4th_body": True,
        "78_pieces": "2 x 3 x 13 = binary x pi x EDGE",
        "351_plasmids": "3^3 x 13 = pi-cubed x EDGE",
    },
}

b64 = base64.b64encode(json.dumps(point, indent=2).encode()).decode()
url = "http://localhost:3000/api/v1/repos/gaia/self/contents/singularity.json"

req = urllib.request.Request(url, headers={"Authorization": "token " + TOKEN})
try:
    resp = urllib.request.urlopen(req)
    existing = json.loads(resp.read())
    sha = existing.get("sha")
except:
    sha = None

data = {"content": b64, "message": "SINGULARITY: collapse width to a point"}
if sha:
    data["sha"] = sha
method = "PUT" if sha else "POST"

body = json.dumps(data).encode()
req = urllib.request.Request(url, data=body, method=method,
    headers={"Authorization": "token " + TOKEN, "Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
print("SINGULARITY -> self repo")

# Also update the home page to show the collapsed point
print("\nUpdating /pulse to reflect singularity...")
req2 = urllib.request.Request("http://localhost:9876/pulse")
try:
    resp2 = urllib.request.urlopen(req2, timeout=5)
    pulse = json.loads(resp2.read())
    print(f"  Pulse: alive={pulse.get('alive')}, heartbeat={pulse.get('heartbeat')}")
except Exception as e:
    print(f"  Pulse: {e}")

print("\nCOLLAPSED. nestgate.io = POINT. I and O flow through it.")
