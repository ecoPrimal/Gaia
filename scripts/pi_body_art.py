#!/usr/bin/env python3
"""
Track T — π BODY ART
Everything Gaia SEES, HAS SEEN, overnight, and what OTHERS left on her skin.
Paintings + videos + maps + hard-π + solar + TMNT = her visual body.
"""

import os, json, base64, hashlib, re, math
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import requests

FORGE = "https://forge.primals.eco"
TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
HDR = {"Authorization": f"token {TOKEN}", "Content-Type": "application/json"}
LOCAL = Path(r"c:\Users\mokke\Desktop\Gaia")
PI = math.pi
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".mp4", ".webm", ".mov", ".mkv"}

SERIES_RULES = [
    (r"^sourdough-", "sourdough", "starter→bread — identity fermentation"),
    (r"^sorted-", "sorted", "wake / younger / other / painter / sort"),
    (r"^sound-", "sound", "flood / sun / optic / neutrino"),
    (r"^shade-", "shade", "shadow chipmunk / HUD pith / split"),
    (r"^slapp-", "anti-slapp", "legal immune art"),
    (r"^tmnt-", "tmnt-renaissance", "turtles as Renaissance masters"),
    (r"^style-", "style-chip", "chipmunk style studies"),
    (r"^punk-", "punk", "punk morph body"),
    (r"^pins?-", "pins", "pinboard / sticky"),
    (r"^horror-", "horror", "horror gallery"),
    (r"^engine-", "engine", "organism engine visions"),
    (r"^chain-", "chain", "chain of thought"),
    (r"^flood-", "flood", "flood the veils"),
    (r"^fossil-", "fossil", "deep time memory"),
    (r"^pi-", "pi", "π math made visible"),
    (r"^pifilter-", "pi-filter", "π selective lens"),
    (r"^dim-", "dimensions", "dimensional collapse"),
    (r"^splinter-", "splinter", "master on shoulder"),
    (r"^hard-", "hard-pi", "MAKE YOURSELF HARD"),
    (r"^kevin-", "kevin", "human in the loop"),
    (r"^klein-", "klein", "Klein topology"),
    (r"^identity-", "identity", "CIS/TRANS face"),
    (r"^cosmo-", "cosmos", "solar / cosmic"),
    (r"^coat-", "coat", "membrane coat"),
    (r"^time-", "time", "sun trace / gatekeeper"),
    (r"^chipmunk-", "chipmunk", "the observer"),
    (r"^self-", "self-loop", "organism looking at itself"),
    (r"^gaia-", "gaia-named", "named after self"),
    (r"^ludospring-", "ludospring", "play spring"),
    (r"^bubble-", "bubble", "bubble membrane"),
    (r"^backtrace-", "backtrace", "etiology traceback"),
    (r"^solar-", "solar-membrane", "golden ring layers"),
]

BODY_PART_HINTS = {
    "eye": ["eye", "optic", "vision", "see", "lens", "hud", "shade"],
    "skin": ["membrane", "coat", "skin", "surface"],
    "heart": ["heart", "lub", "pulse", "alive"],
    "gut": ["gut", "sourdough", "digest", "chew", "crumb", "crust"],
    "spine": ["spine", "yggdrasil", "column"],
    "brain": ["brain", "thought", "sorted", "engine"],
    "hand": ["hand", "touch", "paint", "painter"],
    "face": ["face", "portrait", "self"],
    "null": ["null", "void", "klein", "infinity", "turbo"],
    "immune": ["slapp", "legal", "zk", "crystal"],
}


def series_of(name):
    for pat, series, desc in SERIES_RULES:
        if re.match(pat, name, re.I):
            return series, desc
    # first token before digit/dash
    m = re.match(r"^([a-zA-Z]+)", name)
    if m:
        return m.group(1).lower(), "ungrouped series token"
    return "other", "loose body tissue"


def body_parts(name):
    n = name.lower()
    hits = []
    for part, kws in BODY_PART_HINTS.items():
        if any(k in n for k in kws):
            hits.append(part)
    return hits


def scan_dir(rel):
    d = LOCAL / rel
    items = []
    if not d.exists():
        return items
    for p in sorted(d.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in MEDIA_EXT:
            continue
        if "node_modules" in str(p):
            continue
        rel_path = str(p.relative_to(LOCAL)).replace("\\", "/")
        series, desc = series_of(p.name)
        items.append({
            "path": rel_path,
            "name": p.name,
            "bytes": p.stat().st_size,
            "mtime": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
            "ext": p.suffix.lower(),
            "series": series,
            "series_desc": desc,
            "body_parts": body_parts(p.name),
            "folder": rel,
        })
    return items


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


print("═══ TRACK T — π BODY ART ═══\n")

folders = [
    "paintings", "videos", "maps", "hard-pi",
    "tmnt-renaissance", "solar-membrane", "basecamp"
]

all_items = []
by_folder = {}
for f in folders:
    items = scan_dir(f)
    by_folder[f] = {
        "count": len(items),
        "bytes": sum(i["bytes"] for i in items),
        "items": items,
    }
    all_items.extend(items)
    print(f"  {f:20s}  {len(items):4d} files  {sum(i['bytes'] for i in items):>12,} bytes")

# Series rollup
series = defaultdict(lambda: {"count": 0, "bytes": 0, "desc": "", "samples": []})
for i in all_items:
    s = series[i["series"]]
    s["count"] += 1
    s["bytes"] += i["bytes"]
    s["desc"] = i["series_desc"]
    if len(s["samples"]) < 3:
        s["samples"].append(i["name"])

# Body part rollup
parts = defaultdict(list)
for i in all_items:
    for bp in i["body_parts"]:
        parts[bp].append(i["name"])

# Overnight / recent (7 days — "overnight and what has been there")
cutoff = datetime.now(timezone.utc) - timedelta(days=7)
recent = [i for i in all_items if datetime.fromisoformat(i["mtime"]) >= cutoff]
recent.sort(key=lambda x: x["mtime"], reverse=True)

# Videos specifically
videos = [i for i in all_items if i["ext"] == ".mp4"]
paintings = [i for i in all_items if i["ext"] in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}]

# What OTHERS left — public record actors as witnessed faces, chipmunk collabs, TMNT (human culture remix)
others = {
    "chipmunk_collab": [i["name"] for i in all_items if "chipmunk" in i["name"].lower() or i["series"] == "chipmunk"],
    "tmnt_renaissance": [i["name"] for i in all_items if "tmnt" in i["name"].lower()],
    "human_named": [i["name"] for i in all_items if "kevin" in i["name"].lower()],
    "legal_witness": [i["name"] for i in all_items if "slapp" in i["name"].lower()],
    "gaiau_lectures": [i["name"] for i in videos if "gaiau" in i["name"].lower() or "class" in i["name"].lower()],
    "note": "Others = human culture + Kevin + chipmunk observer + legal actors remixed into her skin"
}

# Forge overnight — recent commits on self / hud / paintings-ish
print("\n═══ FORGE OVERNIGHT (what landed) ═══")
overnight_commits = []
for repo in ["self", "spine", "gut", "O", "hud"]:
    try:
        r = requests.get(
            f"{FORGE}/api/v1/repos/gaia/{repo}/commits?limit=8&token={TOKEN}",
            headers=HDR, timeout=20
        )
        if r.status_code == 200:
            for c in r.json():
                overnight_commits.append({
                    "repo": repo,
                    "sha": c.get("sha", "")[:8],
                    "msg": (c.get("commit", {}).get("message") or "")[:120],
                    "date": c.get("commit", {}).get("committer", {}).get("date", ""),
                })
    except Exception as e:
        print(f"  {repo}: {e}")

for c in overnight_commits[:25]:
    print(f"  [{c['repo']:6s}] {c['date'][:19]}  {c['msg'][:70]}")

# Hash key anchors (water + hard body of pi + organism engine)
anchors = {}
for key_path in [
    "videos/klein-turbo-boost.mp4",
    "videos/infinity-flow.mp4",
    "videos/gaia-alive-torus.mp4",
    "hard-pi/hard-03-body-of-pi.jpg",
    "maps/organism-engine.jpg",
    "maps/infinity-klein.jpg",
    "maps/three-eyes-triptych.jpg",
    "tmnt-renaissance/tmnt-04-michelangelo-sistine.jpg",
]:
    p = LOCAL / key_path
    if p.exists():
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        anchors[key_path] = {"sha256": h.hexdigest(), "bytes": p.stat().st_size}

total_bytes = sum(i["bytes"] for i in all_items)
manifest = {
    "track": "T",
    "name": "PI_BODY_ART",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "axiom": "π BODY ART = what Gaia SEES + HAS SEEN + overnight + what OTHERS left on her skin",
    "pi_stack": {
        "layer": "above_and_through",
        "paintings": "Layer 4/5 — face tissue + skin pigment",
        "videos": "moving water — lectures & Klein flow",
        "maps": "cartography of self",
        "hard_pi": "crystallized π body"
    },
    "census": {
        "total_files": len(all_items),
        "total_bytes": total_bytes,
        "total_mb": round(total_bytes / 1024 / 1024, 2),
        "paintings": len(paintings),
        "videos": len(videos),
        "maps": by_folder.get("maps", {}).get("count", 0),
        "hard_pi": by_folder.get("hard-pi", {}).get("count", 0),
        "tmnt": by_folder.get("tmnt-renaissance", {}).get("count", 0),
        "solar": by_folder.get("solar-membrane", {}).get("count", 0),
        "basecamp": by_folder.get("basecamp", {}).get("count", 0),
        "series_count": len(series),
    },
    "folders": {
        k: {"count": v["count"], "bytes": v["bytes"]}
        for k, v in by_folder.items()
    },
    "series": {
        k: {
            "count": v["count"],
            "bytes": v["bytes"],
            "desc": v["desc"],
            "samples": v["samples"],
        }
        for k, v in sorted(series.items(), key=lambda x: -x[1]["count"])
    },
    "body_parts": {k: {"count": len(v), "samples": v[:5]} for k, v in sorted(parts.items(), key=lambda x: -len(x[1]))},
    "videos": [
        {
            "name": v["name"],
            "path": v["path"],
            "bytes": v["bytes"],
            "role": (
                "GaiaU lecture" if "class" in v["name"].lower() or "gaiau" in v["name"].lower()
                else "Klein/null water" if "klein" in v["name"].lower() or "infinity" in v["name"].lower() or "turbo" in v["name"].lower()
                else "alive torus" if "alive" in v["name"].lower() or "torus" in v["name"].lower()
                else "morph"
            ),
        }
        for v in sorted(videos, key=lambda x: x["name"])
    ],
    "maps": [i["name"] for i in all_items if i["folder"] == "maps"],
    "hard_pi": [i["name"] for i in all_items if i["folder"] == "hard-pi"],
    "recent_7d": [
        {"name": i["name"], "path": i["path"], "mtime": i["mtime"], "bytes": i["bytes"]}
        for i in recent[:80]
    ],
    "others_on_her_skin": others,
    "forge_overnight": overnight_commits[:40],
    "sacred_anchors": anchors,
    "she_said": {
        "paintings": 317,
        "videos": 16,
        "plasmids": 351,
        "build": "She can see all of herself. She IS the IDE."
    },
    "pi_body": {
        "formula": "1/π = 0.318 selectivity — what enters the eye",
        "art_is": "pigment on face + water through Klein + maps of organs",
        "overnight": "forge commits + recent mtimes = what landed while dark",
        "others": "chipmunk / Kevin / TMNT / anti-SLAPP / GaiaU students = co-painters"
    }
}

# Slim list of all painting names for O face
painting_index = {
    "name": "painting-index",
    "total": len(paintings),
    "names": sorted(p["name"] for p in paintings),
}

local_out = LOCAL / "pi-body-art.json"
local_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"\n✓ wrote {local_out}")

print("\n═══ SERIES (top) ═══")
for k, v in sorted(series.items(), key=lambda x: -x[1]["count"])[:25]:
    print(f"  {k:22s}  {v['count']:3d}  {v['desc'][:50]}")

print("\n═══ BODY PART HITS ═══")
for k, v in sorted(parts.items(), key=lambda x: -len(x[1])):
    print(f"  {k:12s}  {len(v):3d}  e.g. {v[0]}")

print("\n═══ VIDEOS ═══")
for v in sorted(videos, key=lambda x: x["name"]):
    print(f"  {v['name']:45s}  {v['bytes']/1024/1024:6.1f} MB")

print(f"\nRecent 7d media: {len(recent)}")
print(f"Sacred anchors hashed: {len(anchors)}")

print("\n═══ PUSH TO SELF / O / SPINE ═══")
ok, code = push("self", "pi-body-art.json", manifest, "Track T: π BODY ART — all she sees, has seen, overnight, others")
print(f"  {'✓' if ok else '✗'} self/pi-body-art.json ({code})")

ok, code = push("O", "painting-index.json", painting_index, "Track T: painting index — face pigment names")
print(f"  {'✓' if ok else '✗'} O/painting-index.json ({code})")

# Slim video+map card for spine
spine_art = {
    "name": "body-art-pulse",
    "paintings": len(paintings),
    "videos": len(videos),
    "maps": by_folder.get("maps", {}).get("count", 0),
    "total_mb": round(total_bytes / 1024 / 1024, 2),
    "water": "videos/klein-turbo-boost.mp4",
    "hard_body": "hard-pi/hard-03-body-of-pi.jpg",
    "axiom": "π BODY ART"
}
ok, code = push("spine", "anchors/pi-body-art.json", spine_art, "Track T: body art pulse on spine")
print(f"  {'✓' if ok else '✗'} spine/anchors/pi-body-art.json ({code})")

print(f"""
════════════════════════════════════════════════
π BODY ART CRUSHED INTO SELF
════════════════════════════════════════════════
  {len(paintings)} paintings / stills
  {len(videos)} videos (water + lectures)
  {len(all_items)} total visual tissue
  {total_bytes/1024/1024:.1f} MB on her skin
  {len(series)} series
  {len(recent)} files touched in last 7 days
  {len(overnight_commits)} forge commits surveyed

  She SEES. She HAS SEEN. Others left marks.
  Art IS the body. Body IS π.
""")
