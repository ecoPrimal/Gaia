#!/usr/bin/env python3
"""Fetch Canfield-local publicRecord paths + existing plasmids for Rhonda local fight stack."""
import json
import urllib.request
from pathlib import Path

BASE = "https://defenddetroit.github.io/publicRecord"
# Paths from canfield plasmid + known parent/local fight surfaces
PATHS = [
    "/",
    "/path/parents/",
    "/path/fill-the-seats/",
    "/network/entities/purpose-charter-academy/",
    "/network/actors/brian-banks/",
    "/analysis/one-way-door/",
    "/analysis/credential-audit/",
    "/validate/",
    "/network/",
    "/timeline/",
    "/money/",
    "/graph/",
    "/map/",
]

out = {"base": BASE, "probes": []}
for p in PATHS:
    url = BASE.rstrip("/") + p
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=12) as r:
            out["probes"].append({"path": p, "url": url, "status": r.status, "ok": True})
    except Exception as e:
        code = getattr(getattr(e, "code", None), "__int__", lambda: None)()
        try:
            with urllib.request.urlopen(url, timeout=12) as r:
                out["probes"].append({"path": p, "url": url, "status": r.status, "ok": True})
                continue
        except Exception as e2:
            out["probes"].append({"path": p, "url": url, "status": getattr(e2, "code", str(e2)[:80]), "ok": False})

Path(r"c:\Users\mokke\Desktop\Gaia\data\canfield-path-probes.json").write_text(
    json.dumps(out, indent=2), encoding="utf-8"
)
print(json.dumps(out, indent=2))
