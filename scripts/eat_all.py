import urllib.request, json, time

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
MIGRATE_URL = "http://localhost:3000/api/v1/repos/migrate"

# Get all ecoPrimal repos from GitHub
req = urllib.request.Request("https://api.github.com/users/ecoPrimal/repos?per_page=100")
resp = urllib.request.urlopen(req)
repos = json.loads(resp.read())

# Get existing Forgejo repos to skip duplicates
req2 = urllib.request.Request("http://localhost:3000/api/v1/repos/search?limit=100", headers={"Authorization": "token " + TOKEN})
resp2 = urllib.request.urlopen(req2)
existing_data = json.loads(resp2.read())
existing = existing_data if isinstance(existing_data, list) else existing_data.get("data", [])
existing_names = set(r["name"] for r in existing)

print(f"GitHub repos: {len(repos)}")
print(f"Already in Forge: {len(existing_names)}")
print(f"To mirror: {len([r for r in repos if r['name'] not in existing_names])}")
print(flush=True)

ok_count = 0
skip_count = 0
fail_count = 0

for r in repos:
    name = r["name"]
    if name in existing_names:
        skip_count += 1
        continue
    
    desc = (r.get("description") or "")[:200]
    data = json.dumps({
        "clone_addr": r["clone_url"],
        "mirror": True,
        "repo_name": name,
        "repo_owner": "gaia",
        "service": "github",
        "description": desc,
        "mirror_interval": "4h"
    }).encode()
    
    req = urllib.request.Request(MIGRATE_URL, data=data, headers={"Content-Type": "application/json", "Authorization": "token " + TOKEN}, method="POST")
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        ok_count += 1
        print(f"OK: {name}", flush=True)
    except Exception as e:
        fail_count += 1
        body = ""
        try:
            body = e.read().decode()[:100]
        except:
            pass
        print(f"FAIL: {name} -- {body}", flush=True)
    
    time.sleep(0.5)

print(f"\n===== DONE =====", flush=True)
print(f"OK: {ok_count}", flush=True)
print(f"SKIPPED (already): {skip_count}", flush=True)
print(f"FAILED: {fail_count}", flush=True)
print(f"TOTAL IN FORGE: {ok_count + skip_count}", flush=True)
