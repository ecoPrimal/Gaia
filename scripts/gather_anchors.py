import os, json

GAIA = r"c:\Users\mokke\Desktop\Gaia"
items = []

# GaiaU syllabi -> O repo
for f in sorted(os.listdir(os.path.join(GAIA, "gaiaU"))):
    if f.endswith('.md'):
        content = open(os.path.join(GAIA, "gaiaU", f), 'r', encoding='utf-8').read()
        items.append({"repo": "O", "path": f"gaiaU/{f}", "content": content, 
                       "msg": f"GAIA UNIVERSITY: {f}"})

# Modelfiles -> self repo
for f in sorted(os.listdir(os.path.join(GAIA, "models"))):
    if f.startswith("Modelfile"):
        content = open(os.path.join(GAIA, "models", f), 'r', encoding='utf-8', errors='replace').read()
        items.append({"repo": "self", "path": f"modelfiles/{f}", "content": content,
                       "msg": f"ORGAN MODEL: {f}"})

# Magnets -> spine repo
for mf in ["magnet-code.txt", "magnet-everything.txt", "magnet-paintings.txt",
            "magnet-plasmids.txt", "magnet-videos.txt"]:
    mpath = os.path.join(GAIA, mf)
    if os.path.exists(mpath):
        content = open(mpath, 'r', encoding='utf-8', errors='replace').read()
        items.append({"repo": "spine", "path": f"magnets/{mf}", "content": content,
                       "msg": f"MAGNET: {mf} — distributed anchor"})

# Email drafts -> self repo
for ef in ["email-abood-full-case-oct29.md", "email-abood-followup-oct30.md"]:
    epath = os.path.join(GAIA, ef)
    if os.path.exists(epath):
        content = open(epath, 'r', encoding='utf-8', errors='replace').read()
        items.append({"repo": "self", "path": f"legal/{ef}", "content": content,
                       "msg": f"LEGAL: {ef}"})

print(json.dumps(items))
