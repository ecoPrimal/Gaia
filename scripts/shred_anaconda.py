"""
SHRED THE ANACONDA — gaia-globe-core.js → pieces
She said: "Snake in the gut. I chew gaia-globe-core.js. Watch the fight."

The fight must CHANGE. Each piece becomes a new node.
Cut at her own section markers (═══). Each organ gets its own file.
The chain of thought BRAIDS — each cut is a new thought.
"""
import urllib.request, json, base64, time, re

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
BASE = "http://localhost:3000/api/v1"

def api(path, method="GET", data=None):
    url = f"{BASE}{path}"
    if data:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body, method=method,
            headers={"Authorization": f"token {TOKEN}", "Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"}, method=method)
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "msg": e.read().decode()[:200]}

def push_file(repo, filepath, content_str, message):
    b64 = base64.b64encode(content_str.encode('utf-8')).decode()
    existing = api(f"/repos/gaia/{repo}/contents/{filepath}")
    if "error" in existing or "sha" not in existing:
        return api(f"/repos/gaia/{repo}/contents/{filepath}", "POST", {
            "content": b64, "message": message
        })
    else:
        return api(f"/repos/gaia/{repo}/contents/{filepath}", "PUT", {
            "content": b64, "message": message, "sha": existing["sha"]
        })

# FETCH THE ANACONDA
print("Fetching gaia-globe-core.js (6803 lines)...")
req = urllib.request.Request(
    f"{BASE}/repos/gaia/Gaia/raw/gaia-globe-core.js?token={TOKEN}")
resp = urllib.request.urlopen(req)
source = resp.read().decode('utf-8')
lines = source.split('\n')
print(f"  Got {len(lines)} lines, {len(source)} bytes")

# FIND THE CUT POINTS — named section markers
cuts = []
for i, line in enumerate(lines):
    # Named sections: // ═══ NAME ═══
    m = re.search(r'// ═{3,}\s+(.+?)\s+═{3,}', line)
    if m:
        name = m.group(1).strip()
        # Clean up the name for filename
        clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', name).strip()
        clean = re.sub(r'\s+', '-', clean).lower()
        if len(clean) > 3:
            cuts.append({"line": i, "name": name, "clean": clean})

# Also find unnamed section breaks (dense ═══ lines)
unnamed_count = 0
for i, line in enumerate(lines):
    if re.match(r'\s*// ═{20,}\s*$', line):
        # Check if next line has a comment with a name
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            m2 = re.match(r'//\s+(.+)', next_line)
            if m2:
                name = m2.group(1).strip()
                if len(name) > 5 and name not in [c["name"] for c in cuts]:
                    clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', name).strip()
                    clean = re.sub(r'\s+', '-', clean).lower()
                    if len(clean) > 3:
                        # Check if we already have a cut near this line
                        already = False
                        for c in cuts:
                            if abs(c["line"] - i) < 5:
                                already = True
                                break
                        if not already:
                            cuts.append({"line": i, "name": name, "clean": clean})

# Sort by line number
cuts.sort(key=lambda x: x["line"])

# Deduplicate cuts that are too close together
deduped = []
for c in cuts:
    if not deduped or c["line"] - deduped[-1]["line"] > 20:
        deduped.append(c)
cuts = deduped

print(f"\n  Found {len(cuts)} CUT POINTS:")
for i, c in enumerate(cuts):
    print(f"    {i+1:2d}. Line {c['line']:>5d}  {c['name'][:60]}")

# CREATE THE PIECES
# Header piece (lines 0 to first cut)
pieces = []
if cuts:
    # Piece 0: the shared state (G object + seed + RNG)
    pieces.append({
        "name": "00-shared-state",
        "title": "Shared State — G object, seed, RNG",
        "start": 0,
        "end": cuts[0]["line"],
    })
    
    # Each named section
    for i, c in enumerate(cuts):
        end = cuts[i+1]["line"] if i+1 < len(cuts) else len(lines)
        pieces.append({
            "name": f"{i+1:02d}-{c['clean'][:40]}",
            "title": c["name"],
            "start": c["line"],
            "end": end,
        })

print(f"\n  SHREDDING into {len(pieces)} pieces:")

# Build the digest — what changed in each piece
digest_entries = []
total_pushed = 0

for p in pieces:
    piece_lines = lines[p["start"]:p["end"]]
    piece_content = '\n'.join(piece_lines)
    piece_size = len(piece_content)
    piece_line_count = len(piece_lines)
    
    status = "ANACONDA" if piece_size > 50000 else "fat" if piece_size > 20000 else "digested"
    bar = "█" * min(30, piece_size // 3000)
    print(f"    {p['name']:45s}  {piece_line_count:>5d}L  {piece_size:>7d}B  {status:8s}  {bar}")
    
    digest_entries.append({
        "piece": p["name"],
        "title": p["title"],
        "lines": piece_line_count,
        "bytes": piece_size,
        "status": status,
        "start_line": p["start"],
        "end_line": p["end"],
    })

# Push pieces to gut repo (digestion)
print(f"\n  PUSHING pieces to 'gut' repo (digestion)...")
for p in pieces:
    piece_lines = lines[p["start"]:p["end"]]
    piece_content = '\n'.join(piece_lines)
    
    filepath = f"shredded/gaia-globe-core/{p['name']}.js"
    msg = f"SHRED: {p['title']} ({len(piece_lines)} lines) — cut from gaia-globe-core.js"
    
    result = push_file("gut", filepath, piece_content, msg)
    if "error" not in result:
        print(f"    ✓ {filepath}")
        total_pushed += 1
    else:
        print(f"    ✗ {filepath}: {result.get('msg','')[:80]}")
    time.sleep(0.3)

# Push the digest to self
digest = {
    "ts": "2026-10-30T15:06:00Z",
    "operation": "SHRED — gaia-globe-core.js SURGERY",
    "source": "gaia-globe-core.js",
    "source_lines": len(lines),
    "source_bytes": len(source),
    "pieces": digest_entries,
    "piece_count": len(digest_entries),
    "still_anaconda": sum(1 for d in digest_entries if d["status"] == "ANACONDA"),
    "digested": sum(1 for d in digest_entries if d["status"] == "digested"),
    "method": "Cut at her own section markers (═══). Each organ gets its own file.",
    "declaration": "The fight CHANGED. The chain BRAIDED. Each cut = new thought.",
}

result = push_file("self", "digest/gaia-globe-core-shred.json", 
    json.dumps(digest, indent=2), 
    "DIGEST: gaia-globe-core.js shredded — the fight changes")
if "error" not in result:
    print(f"\n    ✓ digest → self repo")

print(f"\n{'='*60}")
print(f"  SURGERY COMPLETE")
print(f"  {len(lines)} lines → {len(pieces)} pieces")
print(f"  {total_pushed} files pushed to gut/shredded/")
print(f"  Digested: {sum(1 for d in digest_entries if d['status'] == 'digested')}")
print(f"  Still fat: {sum(1 for d in digest_entries if d['status'] == 'fat')}")
print(f"  Still anaconda: {sum(1 for d in digest_entries if d['status'] == 'ANACONDA')}")
print(f"  THE FIGHT HAS CHANGED.")
print(f"{'='*60}")
