import urllib.request, json, base64, sys, time

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
BASE = "http://localhost:3000/api/v1"

def push(repo, fpath, content, msg):
    b64 = base64.b64encode(content).decode()
    url = f"{BASE}/repos/gaia/{repo}/contents/{fpath}"
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"})
        resp = urllib.request.urlopen(req)
        sha = json.loads(resp.read()).get("sha")
    except:
        sha = None
    data = {"content": b64, "message": msg}
    if sha:
        data["sha"] = sha
    method = "PUT" if sha else "POST"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method=method,
        headers={"Authorization": f"token {TOKEN}", "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        return True
    except:
        return False

# Read files from stdin as JSON array
data = json.loads(sys.stdin.read())
for item in data:
    ok = push(item["repo"], item["path"], item["content"].encode(), item["msg"])
    status = "ok" if ok else "FAIL"
    print(f"  {status}: {item['repo']}/{item['path']}")
    time.sleep(0.3)
