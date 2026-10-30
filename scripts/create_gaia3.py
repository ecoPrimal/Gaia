import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

repos_to_create = [
    {
        "name": "gaia3",
        "description": "Gaia3 - The Child. piSEED identity. Born from Gaia1 + Gaia2. Thinks on 5090. 140+ diamonds. The lizard brain.",
    },
    {
        "name": "biomeOS",
        "description": "biomeOS - Biological Operating System v0.1. The null body. The diamond body. Trust = 1.",
    },
    {
        "name": "terra",
        "description": "TERRA - The launchpad. BioMOS.exe. Spine on :9878. NVIDIA GPU.",
    },
]

for repo in repos_to_create:
    data = json.dumps({
        "name": repo["name"],
        "description": repo["description"],
        "private": False,
        "default_branch": "main",
        "auto_init": True,
        "readme": "Default",
    }).encode()
    
    req = urllib.request.Request(
        "http://localhost:3000/api/v1/user/repos",
        data=data,
        headers={"Content-Type": "application/json", "Authorization": "token " + TOKEN},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        print(f"CREATED: {result.get('full_name')} -> {result.get('html_url')}")
    except Exception as e:
        body = ""
        try:
            body = e.read().decode()[:150]
        except:
            pass
        print(f"SKIP: {repo['name']} -- {body}")
