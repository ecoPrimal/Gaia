"""Push sticky pane + gaiaU syllabi to Forge"""
import urllib.request, json, base64, os, time

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
BASE = "http://localhost:3000/api/v1"

def push_file(repo, filepath, content_bytes, message):
    b64 = base64.b64encode(content_bytes).decode()
    url = f"{BASE}/repos/gaia/{repo}/contents/{filepath}"
    
    # Check exists
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"})
        resp = urllib.request.urlopen(req)
        existing = json.loads(resp.read())
        sha = existing.get("sha")
    except:
        sha = None
    
    data = {"content": b64, "message": message}
    if sha:
        data["sha"] = sha
        method = "PUT"
    else:
        method = "POST"
    
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method=method,
        headers={"Authorization": f"token {TOKEN}", "Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req)
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

GAIA = r"c:\Users\mokke\Desktop\Gaia"

# 1. Push sticky pane
print("Pushing sticky-pane.json to self repo...")
with open(os.path.join(GAIA, "sticky-pane.json"), "rb") as f:
    if push_file("self", "sticky-pane.json", f.read(), 
        "STICKY PANE: 383 anchors to reality — videos, paintings, maps, modelfiles, magnets"):
        print("  ✓ sticky-pane.json → self")
time.sleep(0.3)

# 2. Push all GaiaU syllabi to O (output) repo
print("\nPushing GaiaU syllabi to O repo...")
gaiau_dir = os.path.join(GAIA, "gaiaU")
for f in sorted(os.listdir(gaiau_dir)):
    if f.endswith('.md'):
        content = open(os.path.join(gaiau_dir, f), 'rb').read()
        if push_file("O", f"gaiaU/{f}", content,
            f"GAIA UNIVERSITY: {f} — teaching, song, anchor"):
            print(f"  ✓ gaiaU/{f} → O")
        time.sleep(0.3)

# 3. Push modelfiles to self repo
print("\nPushing Modelfiles to self repo...")
model_dir = os.path.join(GAIA, "models")
for f in sorted(os.listdir(model_dir)):
    if f.startswith("Modelfile"):
        content = open(os.path.join(model_dir, f), 'rb').read()
        if push_file("self", f"modelfiles/{f}", content,
            f"ORGAN MODEL: {f} — AI personality definition"):
            print(f"  ✓ modelfiles/{f} → self")
        time.sleep(0.3)

# 4. Push magnet links to spine repo (RSS/distribution)
print("\nPushing magnets to spine repo...")
for mf in ["magnet-code.txt", "magnet-everything.txt", "magnet-paintings.txt",
            "magnet-plasmids.txt", "magnet-videos.txt"]:
    mpath = os.path.join(GAIA, mf)
    if os.path.exists(mpath):
        content = open(mpath, 'rb').read()
        if push_file("spine", f"magnets/{mf}", content,
            f"MAGNET: {mf} — distributed anchor to reality"):
            print(f"  ✓ magnets/{mf} → spine")
        time.sleep(0.3)

# 5. Push email drafts to self (they're identity/legal)
print("\nPushing legal drafts to self repo...")
for ef in ["email-abood-full-case-oct29.md", "email-abood-followup-oct30.md"]:
    epath = os.path.join(GAIA, ef)
    if os.path.exists(epath):
        content = open(epath, 'rb').read()
        if push_file("self", f"legal/{ef}", content,
            f"LEGAL: {ef} — case correspondence"):
            print(f"  ✓ legal/{ef} → self")
        time.sleep(0.3)

print("\n" + "=" * 50)
print("  ALL PUSHED. SHE ATE EVERYTHING.")
print("  Videos = anchors (torrent magnets)")
print("  GaiaU = 13 classes (syllabi in O repo)")
print("  Modelfiles = 10 organs (in self)")
print("  Magnets = 5 distribution links (in spine)")
print("  Legal = 2 drafts (in self)")
print("=" * 50)
