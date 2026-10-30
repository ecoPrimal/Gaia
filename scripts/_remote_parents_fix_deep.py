#!/usr/bin/env python3
import re
import shutil
import subprocess
import time
from pathlib import Path

SRC = Path("/opt/publicRecord/site/public")
GAIA = Path("/opt/gaia-api/static/publicRecord")
NEST = Path("/opt/connect/publicRecord")

# find macdowell / holland
print("=== find entities ===")
for p in SRC.rglob("*"):
    if not p.is_file():
        continue
    n = p.as_posix().lower()
    if "macdowell" in n or "holland" in n or "purpose-group" in n:
        print(p.relative_to(SRC))

parents = GAIA / "path/parents/index.html"
raw = parents.read_bytes()
# show link patterns
text = raw.decode("utf-8", errors="replace")
print("=== link samples ===")
for pat in [
    r"href=[^\s>]+",
    r"href\s*=\s*[^\s>]+",
    r'["\'](/?[^"\']+(?:analysis|network|path|entity)[^"\']*)["\']',
]:
    ms = re.findall(pat, text, re.I)
    print(pat, "count", len(ms))
    for m in ms[:15]:
        print(" ", m[:160])

# Zola often emits href=/publicRecord/... without quotes? or absolute
# Also: href=../analysis/foo/

REWRITE = [
    ("https://defenddetroit.github.io/publicRecord", "/publicRecord"),
    ("https://detroit.primals.eco", "/publicRecord"),
    ("http://detroit.primals.eco", "/publicRecord"),
]


def melt(rel):
    src = SRC / rel
    if not src.exists():
        if (SRC / rel / "index.html").exists():
            rel = rel.rstrip("/") + "/index.html"
            src = SRC / rel
        else:
            print("still missing", rel)
            return False
    data = src.read_bytes()
    if rel.endswith((".html", ".css", ".js", ".json", ".txt")):
        s = data.decode("utf-8", errors="replace")
        for a, b in REWRITE:
            s = s.replace(a, b)
        s = re.sub(
            r"https?://(?:detroit\.primals\.eco|defenddetroit\.github\.io/publicRecord)",
            "/publicRecord",
            s,
        )
        data = s.encode("utf-8")
    for root in (GAIA, NEST):
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    print("melted", rel, len(data))
    return True


# melt likely alt names
for cand in list(SRC.joinpath("network/entities").glob("*mac*")) + list(
    SRC.joinpath("network/entities").glob("*Mac*")
):
    if (cand / "index.html").exists():
        melt(str(cand.relative_to(SRC) / "index.html").replace("\\", "/"))
for cand in list(SRC.joinpath("network/actors").glob("*holland*")) + list(
    SRC.joinpath("network/actors").glob("*Holland*")
):
    if (cand / "index.html").exists():
        melt(str(cand.relative_to(SRC) / "index.html").replace("\\", "/"))

# Fix parents HTML links aggressively
s = text
for a, b in REWRITE:
    s = s.replace(a, b)
s = re.sub(
    r"https?://(?:detroit\.primals\.eco|defenddetroit\.github\.io/publicRecord)",
    "/publicRecord",
    s,
)
# unquoted href=../x or href=/x
s = re.sub(r"href=\.\./\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/",
           r"href=/publicRecord/\1/", s)
s = re.sub(r"href=\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/",
           r"href=/publicRecord/\1/", s)
# quoted relatives
s = re.sub(r'href="\.\./\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/',
           r'href="/publicRecord/\1/', s)
s = re.sub(r"href='\.\./\.\./(analysis|network|path|validate|timeline|evidence|courts|connections|about)/",
           r"href='/publicRecord/\1/", s)

# inject deeper banner if missing
if "OPEN DEEP STACK" not in s and "parents-deep" not in s:
    banner = (
        '<div id="gaia-deeper" style="position:sticky;top:0;z-index:100000;background:#140808;'
        'border-bottom:2px solid #f85149;padding:10px 12px;font:13px/1.4 ui-monospace,Menlo,monospace;color:#e6edf3">'
        '<b style="color:#f85149">NOPE — DEEPER</b> · '
        '<a href="/parents-deep" style="color:#3fb950;font-weight:bold">OPEN DEEP STACK</a> · '
        '<a href="/publicRecord/analysis/funding-flow/" style="color:#58a6ff">money</a> · '
        '<a href="/publicRecord/analysis/credential-audit/" style="color:#58a6ff">creds</a> · '
        '<a href="/publicRecord/analysis/rico-pattern/" style="color:#58a6ff">RICO</a> · '
        '<a href="/publicRecord/analysis/banks-holland-partnership/" style="color:#58a6ff">Banks–Holland</a> · '
        '<a href="/mito" style="color:#f0883e">MITO</a></div>'
    )
    s = re.sub(r"(<body[^>]*>)", r"\1" + banner, s, count=1, flags=re.I)

parents.write_text(s, encoding="utf-8")
(NEST / "path/parents/index.html").write_text(s, encoding="utf-8")
print("parents rewritten", len(s))
print("has deep banner", "OPEN DEEP STACK" in s)

# update parents-deep layers with discovered paths
deep = Path("/opt/gaia-api/static/parents-deep.html")
d = deep.read_text(encoding="utf-8")
# discover actual mac/holland hrefs after melt
mac = list((GAIA / "network/entities").glob("*acdowell*")) + list((GAIA / "network/entities").glob("*macdowell*"))
hol = list((GAIA / "network/actors").glob("*olland*"))
print("mac dirs", [x.name for x in mac])
print("hol dirs", [x.name for x in hol])
if mac:
    d = d.replace(
        "/publicRecord/network/entities/macdowell/",
        f"/publicRecord/network/entities/{mac[0].name}/",
    )
if hol:
    d = d.replace(
        "/publicRecord/network/actors/joseph-holland-jr/",
        f"/publicRecord/network/actors/{hol[0].name}/",
    )
deep.write_text(d, encoding="utf-8")
Path("/opt/connect/parents-deep.html").write_text(d, encoding="utf-8")

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/parents-deep",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
    "http://127.0.0.1:9876/publicRecord/analysis/funding-flow/",
    "http://127.0.0.1:9876/publicRecord/analysis/banks-holland-partnership/",
]:
    import subprocess as sp

    rr = sp.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
    print(rr.stdout, url)
# list melted mac/holland
for p in (GAIA / "network").rglob("index.html"):
    if "macdowell" in str(p).lower() or "holland" in str(p).lower():
        print("live", p.relative_to(GAIA), p.stat().st_size)
print("DONE")
