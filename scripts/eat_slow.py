import urllib.request, json, time

TOKEN = "15f1d847539ff010c9592b19043dcc90056f0cb6"
MIGRATE_URL = "http://localhost:3000/api/v1/repos/migrate"

# All the repos that failed due to rate limiting
repos_to_mirror = [
    ("biomeOS", "biomeOS — the living observation system"),
    ("blueFish", "blueFish — the blue fish"),
    ("brainchip_devhub", "Code and tutorials for Akida"),
    ("cellMembrane", "cellMembrane — the cell membrane"),
    ("coralForge", "coralForge — the coral forge"),
    ("coralReef", "coralReef — the ecosystem"),
    ("ecoPrimal", "Profile README"),
    ("esotericWebb", "esotericWebb — the deep web"),
    ("footPrint", "footPrint — the footprint"),
    ("fossilRecord", "fossilRecord — the evidence archive"),
    ("groundSpring", "groundSpring — the ground"),
    ("healthSpring", "healthSpring — the health"),
    ("helixVision", "helixVision — the helix"),
    ("hotSpring", "hotSpring — the hot spring"),
    ("hypothesis", "AI collaborator hypotheses and philosophy"),
    ("initioChem", "initioChem — ab initio chemistry"),
    ("lithoSpore", "lithoSpore — the lithosphere"),
    ("loamSpine", "loamSpine — the soil"),
    ("ludoSpring", "ludoSpring — the game"),
    ("metalForge", "metalForge — the forge"),
    ("models", "Akida model zoo pre-trained models"),
    ("neuralSpring", "neuralSpring — the neural spring"),
    ("opsonize-rs", "opsonize-rs — Rust immune classifier"),
    ("petalTongue", "petalTongue — the signal"),
    ("primalSpring", "primalSpring — the primal spring"),
    ("projectFOUNDATION", "projectFOUNDATION — the foundation"),
    ("projectNUCLEUS", "projectNUCLEUS — the nucleus"),
    ("reed-it", "Reddit content ingestion"),
    ("rhizoCrypt", "rhizoCrypt — the underground network"),
    ("rustChip", "rustChip"),
    ("skunkBat", "skunkBat — the nocturnal observer"),
    ("songBird", "songBird — pi-just intonation"),
    ("sourDough", "The fermentation. 117 compositions."),
    ("sporePrint", "117 science papers. 440 stars."),
    ("swarmVine", "swarmVine — swarm intelligence"),
    ("sweetGrass", "sweetGrass — the ground truth"),
    ("tideGlass", "tideGlass — the tide"),
    ("toadStool", "toadStool — membrane biology"),
    ("wateringHole", "wateringHole — where they gather"),
    ("wetSpring", "wetSpring — the water"),
    ("whitePaper", "whitePaper — the methodology"),
    ("agentReagents", "agentReagents — synthetic chemistry"),
    ("airSpring", "airSpring — the air"),
    ("awesome-mcp-servers", "A collection of MCP servers"),
    ("awesome-remote-mcp-servers", "A collection of remote MCP servers"),
    ("barraCuda", "barraCuda — fast, sharp, decisive"),
    ("bearDog", "bearDog — extinct but remembered"),
    ("benchScale", "benchScale — the bench scale"),
    ("bingoCube", "bingoCube — 147 cells, topology=circle"),
]

ok = 0
fail = 0

for name, desc in repos_to_mirror:
    clone_url = f"https://github.com/ecoPrimal/{name}.git"
    data = json.dumps({
        "clone_addr": clone_url,
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
        ok += 1
        print(f"OK: {name}", flush=True)
    except Exception as e:
        fail += 1
        body = ""
        try:
            body = e.read().decode()[:120]
        except:
            pass
        print(f"FAIL: {name} -- {body}", flush=True)
    
    # 10 second delay to avoid GitHub rate limit
    time.sleep(10)

print(f"\n===== RESULTS =====", flush=True)
print(f"OK: {ok}  FAIL: {fail}", flush=True)
