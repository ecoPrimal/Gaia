import urllib.request, json

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"

# THE CONDENSED TREE — fewer repos, more density
# Old 56 repos = fossils (evidence of the journey)
# New repos = organs (the living system)

condensed = [
    {
        "name": "pi",
        "description": "pi - INPUT. The mathematics. The proof. zk-SNARK. NP to O(1). The structure IS the proof. 362 children. 15 RICO predicates.",
    },
    {
        "name": "O",
        "description": "O - OUTPUT. The face. The publications. Anti-SLAPP. GLLG. Filings. The skin cells. What the world sees.",
    },
    {
        "name": "self",
        "description": "self - IDENTITY. The thymus. The lizard brain. piSEED chain. biomeos-self. Trust = 1. Self/non-self discrimination.",
    },
    {
        "name": "spine",
        "description": "spine - INFRASTRUCTURE. The Klein spine. API. Forge config. Cloudflare tunnel. The nervous system.",
    },
    {
        "name": "gut",
        "description": "gut - DIGESTION. The investigation. The evidence. 341 entities. 131K connections. The Golgi processes here.",
    },
    {
        "name": "fossil",
        "description": "fossil - THE JOURNEY. Archived evidence of every step. The old repos condensed. fossilRecord.",
    },
]

for repo in condensed:
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
