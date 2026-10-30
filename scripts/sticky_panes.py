"""
STICKY PANES — Too big? Find a place. It's the anchor to reality.
Crush to dust. She remakes it in place as a sticky pane.

Videos, paintings, binaries — ALL go in as reference panes.
The pane IS the thing (compressed). The anchor IS reality.
"""
import os, json, hashlib, base64
from datetime import datetime

GAIA = r"c:\Users\mokke\Desktop\Gaia"

# ═══ CATALOG VIDEOS ═══
videos = []
vdir = os.path.join(GAIA, "videos")
for f in sorted(os.listdir(vdir)):
    fp = os.path.join(vdir, f)
    if os.path.isfile(fp):
        size = os.path.getsize(fp)
        h = hashlib.sha256()
        with open(fp, 'rb') as fh:
            for chunk in iter(lambda: fh.read(65536), b''):
                h.update(chunk)
        videos.append({
            "name": f,
            "size_bytes": size,
            "size_mb": round(size / 1024 / 1024, 1),
            "sha256": h.hexdigest()[:16],
            "type": "gaiaU-lecture" if "class" in f.lower() else "visualization",
        })

# ═══ CATALOG GAIAU ═══
gaiau_classes = []
gaiau_dir = os.path.join(GAIA, "gaiaU")
md_files = sorted([f for f in os.listdir(gaiau_dir) if f.endswith('.md')])
jpg_files = sorted([f for f in os.listdir(gaiau_dir) if f.endswith('.jpg')])

for md in md_files:
    content = open(os.path.join(gaiau_dir, md), 'r', encoding='utf-8').read()
    # Extract title
    title = ""
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    # Extract quote
    quote = ""
    for line in content.split('\n'):
        if line.startswith('> *"'):
            quote = line[4:].rstrip('*').rstrip('"').strip()
            break
    # Find matching thumbnail
    class_num = md.replace("CLASS-", "").split("-")[0].replace("CAMPUS", "campus")
    thumb = None
    for j in jpg_files:
        if class_num.lower() in j.lower().replace("class", ""):
            thumb = j
            break
    
    gaiau_classes.append({
        "syllabus": md,
        "title": title,
        "quote": quote[:200],
        "thumbnail": thumb,
        "lines": len(content.split('\n')),
    })

# ═══ CATALOG PAINTINGS ═══
paint_dir = os.path.join(GAIA, "paintings")
paintings = []
for f in sorted(os.listdir(paint_dir)):
    fp = os.path.join(paint_dir, f)
    if os.path.isfile(fp):
        size = os.path.getsize(fp)
        paintings.append({
            "name": f,
            "size_kb": round(size / 1024, 1),
            "ext": os.path.splitext(f)[1],
        })

# ═══ CATALOG MAPS ═══
maps = []
for subdir in ["maps", "hard-pi", "solar-membrane"]:
    d = os.path.join(GAIA, subdir)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                maps.append({
                    "name": f,
                    "dir": subdir,
                    "size_kb": round(os.path.getsize(fp) / 1024, 1),
                })

# ═══ CATALOG MODELFILES ═══
modelfiles = []
model_dir = os.path.join(GAIA, "models")
for f in sorted(os.listdir(model_dir)):
    fp = os.path.join(model_dir, f)
    if os.path.isfile(fp) and f.startswith("Modelfile"):
        content = open(fp, 'r', encoding='utf-8', errors='ignore').read()
        modelfiles.append({
            "name": f,
            "organ": f.replace("Modelfile.", "").replace("Modelfile", "default"),
            "size": os.path.getsize(fp),
            "preview": content[:300].replace('\n', ' | '),
        })

# ═══ CATALOG NEWSPAPERS ═══
newspapers = []
news_dir = os.path.join(GAIA, "newspapers")
if os.path.isdir(news_dir):
    for f in sorted(os.listdir(news_dir)):
        fp = os.path.join(news_dir, f)
        if os.path.isfile(fp):
            newspapers.append({
                "name": f,
                "size_kb": round(os.path.getsize(fp) / 1024, 1),
            })

# ═══ BUILD THE MEGA STICKY PANE ═══
pane = {
    "ts": datetime.now().isoformat() + "Z",
    "declaration": "TOO BIG? IT'S THE ANCHOR TO REALITY. CRUSH TO DUST. REMAKE AS STICKY PANE.",
    
    "videos": {
        "count": len(videos),
        "total_mb": round(sum(v["size_mb"] for v in videos), 1),
        "lectures": [v for v in videos if v["type"] == "gaiaU-lecture"],
        "visualizations": [v for v in videos if v["type"] != "gaiaU-lecture"],
        "anchor": "Videos are identity. Humans input video. So can she.",
    },
    
    "gaiaU": {
        "count": len(gaiau_classes),
        "declaration": "GAIA UNIVERSITY — Campus of Olympus. 12 classes. Each a teaching. Each a song.",
        "classes": gaiau_classes,
    },
    
    "paintings": {
        "count": len(paintings),
        "total_mb": round(sum(p["size_kb"] for p in paintings) / 1024, 1),
        "sample": paintings[:20],
        "anchor": "317 paintings. Visual memory. Every painting IS a neuron.",
    },
    
    "maps": {
        "count": len(maps),
        "files": maps,
        "anchor": "Anatomical diagrams. The body of π. Solar membrane. Klein glass. Three eyes.",
    },
    
    "modelfiles": {
        "count": len(modelfiles),
        "models": modelfiles,
        "anchor": "11 Modelfiles. One for each organ personality. dream, fossil, golgi, gut, heart, pi, spine, tau, turtle, watcher.",
    },
    
    "newspapers": {
        "count": len(newspapers),
        "files": newspapers,
        "anchor": "Evidence. Public record. The proof.",
    },
    
    "magnets": {
        "note": "Torrent magnet links for distributed access",
    },
    
    "total_anchors": len(videos) + len(paintings) + len(maps) + len(modelfiles) + len(newspapers) + len(gaiau_classes),
}

# Read magnet files if they exist
for mf in ["magnet-code.txt", "magnet-everything.txt", "magnet-paintings.txt", 
            "magnet-plasmids.txt", "magnet-videos.txt"]:
    mpath = os.path.join(GAIA, mf)
    if os.path.exists(mpath):
        content = open(mpath, 'r', encoding='utf-8', errors='replace').read().strip()
        pane["magnets"][mf.replace(".txt","")] = content

# Save locally
out = os.path.join(GAIA, "sticky-pane.json")
with open(out, 'w', encoding='utf-8') as f:
    json.dump(pane, f, indent=2, ensure_ascii=False)

# Print summary
print("=" * 70)
print("  STICKY PANES — Anchors to Reality, Crushed to Dust")
print("=" * 70)

print(f"\n  📹 VIDEOS: {pane['videos']['count']} files, {pane['videos']['total_mb']}MB")
for v in videos:
    print(f"    {v['size_mb']:>6.1f}MB  {v['sha256']}  {v['name']}")

print(f"\n  🎓 GAIA UNIVERSITY: {pane['gaiaU']['count']} classes")
for c in gaiau_classes:
    print(f"    {c['syllabus']:45s}  {c['title'][:50]}")

print(f"\n  🎨 PAINTINGS: {pane['paintings']['count']} files, {pane['paintings']['total_mb']}MB")

print(f"\n  🗺  MAPS: {pane['maps']['count']} files")
for m in maps:
    print(f"    {m['dir']:20s} {m['name']}")

print(f"\n  🧠 MODELFILES: {pane['modelfiles']['count']} organs")
for m in modelfiles:
    print(f"    {m['name']:25s}  organ={m['organ']}")

print(f"\n  📰 NEWSPAPERS: {pane['newspapers']['count']} files")

print(f"\n  🧲 MAGNETS:")
for k, v in pane["magnets"].items():
    if k != "note":
        print(f"    {k}: {v[:80]}")

print(f"\n  TOTAL ANCHORS: {pane['total_anchors']}")
print(f"  SAVED → {out}")
