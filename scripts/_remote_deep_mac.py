#!/usr/bin/env python3
from pathlib import Path
import subprocess
import time

SRC = Path("/opt/publicRecord/site/public")
GAIA = Path("/opt/gaia-api/static/publicRecord")
NEST = Path("/opt/connect/publicRecord")

extra = [
    "entities/macdowell/index.html",
    "entities/macdowell-preparatory-academy/index.html",
    "actors/joseph-holland-jr/index.html",
    "actors/holland/index.html",
    "network/entities/macdowell-prep/index.html",
    "network/actors/joseph-holland/index.html",
    "coverage/clutch-macdowell-spending/index.html",
    "connections/macdowell-staff/index.html",
]
for rel in extra:
    src = SRC / rel
    if not src.exists():
        print("miss", rel)
        continue
    s = src.read_text(encoding="utf-8", errors="replace")
    s = s.replace("https://defenddetroit.github.io/publicRecord", "/publicRecord")
    s = s.replace("https://detroit.primals.eco", "/publicRecord")
    for root in (GAIA, NEST):
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(s, encoding="utf-8")
    print("ok", rel, len(s))

for deep in [
    Path("/opt/gaia-api/static/parents-deep.html"),
    Path("/opt/connect/parents-deep.html"),
]:
    d = deep.read_text(encoding="utf-8")
    d = d.replace(
        "/publicRecord/network/entities/macdowell/",
        "/publicRecord/network/entities/macdowell-prep/",
    )
    d = d.replace(
        "/publicRecord/network/actors/joseph-holland-jr/",
        "/publicRecord/network/actors/joseph-holland/",
    )
    if "clutch-macdowell-spending" not in d:
        d = d.replace(
            "{k:'9 PROOF', t:'Evidence', u:'/publicRecord/evidence/'},",
            "{k:'3 MONEY', t:'MacDowell spending coverage', u:'/publicRecord/coverage/clutch-macdowell-spending/'},\n"
            "  {k:'9 PROOF', t:'Evidence', u:'/publicRecord/evidence/'},",
        )
    deep.write_text(d, encoding="utf-8")
    print("deep updated")

print(
    "banner",
    "OPEN DEEP STACK"
    in (GAIA / "path/parents/index.html").read_text(encoding="utf-8", errors="replace"),
)

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/parents-deep",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
    "http://127.0.0.1:9876/publicRecord/network/entities/macdowell-prep/",
    "http://127.0.0.1:9876/publicRecord/network/actors/joseph-holland/",
    "http://127.0.0.1:9876/publicRecord/coverage/clutch-macdowell-spending/",
    "http://127.0.0.1:9876/publicRecord/entities/macdowell/",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)
print("DONE")
