#!/usr/bin/env python3
import re
import subprocess
import time
from pathlib import Path

p = Path("/opt/gaia-api/server.js")
t = p.read_text(encoding="utf-8")

# Ensure path module available OR rewrite handler without path.
if "require('path')" not in t and 'require("path")' not in t:
    # insert after first require/fs line
    m = re.search(r"(const fs = require\(['\"]fs['\"]\);?)", t)
    if m:
        t = t.replace(m.group(1), m.group(1) + "\nconst path = require('path');", 1)
        print("added path require")
    else:
        t = "const path = require('path');\n" + t
        print("prepended path require")
else:
    print("path already required")

p.write_text(t, encoding="utf-8")
subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
for url in [
    "http://127.0.0.1:9876/publicRecord/",
    "http://127.0.0.1:9876/publicRecord/path/parents/",
    "http://127.0.0.1:9876/publicRecord/path/parents/index.html",
    "http://127.0.0.1:9876/publicRecord/network/actors/brian-banks/",
    "http://127.0.0.1:9876/publicRecord/css/main.css",
    "http://127.0.0.1:9876/C",
    "http://127.0.0.1:9876/cash4kids",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)

# nestgate connect file server
for url in [
    "https://127.0.0.1/publicRecord/",
    "https://127.0.0.1/publicRecord/css/main.css",
    "https://127.0.0.1/publicRecord/path/parents/",
]:
    rr = subprocess.run(
        ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", "-H", "Host: nestgate.io", url],
        capture_output=True,
        text=True,
    )
    print("nest", rr.stdout, url)
print("DONE")
