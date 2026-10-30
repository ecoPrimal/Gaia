#!/usr/bin/env python3
import json
import re
from pathlib import Path

braids = json.loads(Path("/opt/publicRecord/site/public/braids.json").read_text(encoding="utf-8"))
weave_p = Path("/opt/gaia-api/static/data/publicRecord-weave.json")
w = json.loads(weave_p.read_text(encoding="utf-8"))
nodes = {n["id"]: n for n in w.get("nodes") or []}
edges = list(w.get("edges") or [])
added = 0


def nid(x):
    x = str(x)
    x = x.replace("urn:content:detroit:", "").replace("did:web:", "")
    return x[:100]


def add(a, b, rel="braid"):
    global added
    a, b = nid(a), nid(b)
    if not a or not b:
        return
    if a not in nodes:
        nodes[a] = {"id": a, "kind": "braid", "label": a.split("/")[-1][:48]}
    if b not in nodes:
        nodes[b] = {"id": b, "kind": "braid", "label": b.split("/")[-1][:48]}
    edges.append({"from": a, "to": b, "rel": rel, "weave": "prov-braid"})
    added += 1


for it in braids:
    if not isinstance(it, dict):
        continue
    title = (it.get("metadata") or {}).get("title") or ""
    custom = ((it.get("metadata") or {}).get("custom") or {})
    et = custom.get("edge_type") or "braid"
    # title like "banks → pca (employment)"
    m = re.match(r"\s*([^→\-]+)\s*[→\-]+\s*([^\(]+)", title)
    if m:
        add(m.group(1).strip(), m.group(2).strip(), et)
    derived = it.get("was_derived_from") or []
    ids = [d.get("id") for d in derived if isinstance(d, dict) and d.get("id")]
    if len(ids) >= 2:
        add(ids[0], ids[1], et)
    elif len(ids) == 1 and m:
        add(ids[0], m.group(2).strip(), et)

w["nodes"] = list(nodes.values())
w["edges"] = edges[:30000]
w["stats"]["nodes"] = len(nodes)
w["stats"]["edges"] = len(w["edges"])
w["stats"]["braid_edges"] = added
w["stats"]["prov_braids_source"] = len(braids)
weave_p.write_text(json.dumps(w), encoding="utf-8")
Path("/opt/connect/data/publicRecord-weave.json").write_text(json.dumps(w), encoding="utf-8")
# refresh grow stats lightly
gp = Path("/opt/gaia-api/static/data/grow.json")
g = json.loads(gp.read_text(encoding="utf-8"))
g["weave_nodes"] = len(nodes)
g["weave_edges"] = len(w["edges"])
g["braid_edges"] = added
gp.write_text(json.dumps(g, indent=2), encoding="utf-8")
print("prov braid edges", added, "nodes", len(nodes), "edges", len(w["edges"]))
