import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
req = urllib.request.Request("http://localhost:3000/api/v1/repos/search?limit=100", headers={"Authorization": "token " + TOKEN})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
repos = data if isinstance(data, list) else data.get("data", [])

empty = []
full = []
for r in repos:
    size = r.get("size", 0)
    if size == 0:
        empty.append(r["name"])
    else:
        full.append(r["name"])

print(f"TOTAL: {len(repos)} repos in the Forge")
print(f"FULL: {len(full)}")
print(f"EMPTY (need resync): {len(empty)}")
print()
if empty:
    print("Empty repos:")
    for n in sorted(empty):
        print(f"  - {n}")
