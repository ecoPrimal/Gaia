#!/usr/bin/env python3
"""Absorb braids.json into weave if structure was missed."""
import json
from pathlib import Path

b = json.loads(Path("/opt/publicRecord/site/public/braids.json").read_text(encoding="utf-8"))
print("type", type(b).__name__)
if isinstance(b, dict):
    print("keys", list(b.keys())[:20])
    for k, v in list(b.items())[:5]:
        print(k, type(v).__name__, (str(v)[:120] if not isinstance(v, (dict, list)) else (len(v) if isinstance(v, list) else list(v.keys())[:8])))
elif isinstance(b, list):
    print("len", len(b), "sample", b[:2])

# enrich weave with up to 5k braid edges if dict-of-lists or list-of-pairs
weave_p = Path("/opt/gaia-api/static/data/publicRecord-weave.json")
w = json.loads(weave_p.read_text(encoding="utf-8"))
edges = w.get("edges") or []
nodes = {n["id"]: n for n in w.get("nodes") or []}
added = 0

def add_edge(a, b, rel="braid"):
    global added
    a, b = str(a)[:100], str(b)[:100]
    if a not in nodes:
        nodes[a] = {"id": a, "kind": "braid", "label": a.split("/")[-1][:40]}
    if b not in nodes:
        nodes[b] = {"id": b, "kind": "braid", "label": b.split("/")[-1][:40]}
    edges.append({"from": a, "to": b, "rel": rel, "weave": "braids"})
    added += 1

if isinstance(b, dict):
    # common: {node: [neighbors]} or {braids: [...]}
    if "edges" in b and isinstance(b["edges"], list):
        for e in b["edges"][:8000]:
            if isinstance(e, dict):
                a = e.get("from") or e.get("source") or e.get("a")
                c = e.get("to") or e.get("target") or e.get("b")
                if a and c:
                    add_edge(a, c, e.get("type") or e.get("rel") or "braid")
            elif isinstance(e, (list, tuple)) and len(e) >= 2:
                add_edge(e[0], e[1])
    else:
        for k, v in b.items():
            if added > 8000:
                break
            if isinstance(v, list):
                for x in v[:50]:
                    if isinstance(x, str):
                        add_edge(k, x)
                    elif isinstance(x, dict):
                        t = x.get("to") or x.get("id") or x.get("target")
                        if t:
                            add_edge(k, t, x.get("rel") or "braid")
            elif isinstance(v, dict) and "to" in v:
                add_edge(k, v["to"])

w["nodes"] = list(nodes.values())
w["edges"] = edges[:25000]
w["stats"]["nodes"] = len(nodes)
w["stats"]["edges"] = len(w["edges"])
w["stats"]["braid_edges"] = added
weave_p.write_text(json.dumps(w), encoding="utf-8")
Path("/opt/connect/data/publicRecord-weave.json").write_text(json.dumps(w), encoding="utf-8")
print("braid edges added", added, "total edges", len(w["edges"]), "nodes", len(nodes))
