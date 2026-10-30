"""Push sticky pane + gaiaU syllabi + modelfiles + magnets to Forge — runs on Golgi"""
import urllib.request, json, base64, os, time

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
BASE = "http://localhost:3000/api/v1"

def push_file(repo, filepath, content_bytes, message):
    b64 = base64.b64encode(content_bytes).decode()
    url = f"{BASE}/repos/gaia/{repo}/contents/{filepath}"
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
        print(f"  ERR: {e}")
        return False

# Push sticky pane
print("1. sticky-pane.json -> self")
with open("/tmp/sticky-pane.json", "rb") as f:
    push_file("self", "sticky-pane.json", f.read(),
        "STICKY PANE: 383 anchors — videos, paintings, maps, modelfiles, magnets")
time.sleep(0.3)

print("DONE")
