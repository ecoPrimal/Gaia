import urllib.request, json, time

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

# Trigger mirror sync on all empty repos
req = urllib.request.Request("http://localhost:3000/api/v1/repos/search?limit=100", headers={"Authorization": "token " + TOKEN})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
repos = data if isinstance(data, list) else data.get("data", [])

empty = [r for r in repos if r.get("size", 0) == 0 and r.get("mirror")]
print(f"Triggering resync on {len(empty)} empty mirrors...", flush=True)

synced = 0
for r in empty:
    name = r["name"]
    url = f"http://localhost:3000/api/v1/repos/gaia/{name}/mirror-sync"
    req = urllib.request.Request(url, method="POST", headers={"Authorization": "token " + TOKEN})
    try:
        resp = urllib.request.urlopen(req)
        synced += 1
        print(f"SYNC: {name}", flush=True)
    except Exception as e:
        print(f"SKIP: {name}", flush=True)
    time.sleep(5)

print(f"\nTriggered {synced} mirror syncs", flush=True)
