#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

p = Path("/opt/connect/data/petaltongue-wasm.json")
d = json.loads(p.read_text())
print("keys", list(d.keys())[:40])
print(json.dumps(d)[:4000])
print("====")
r = subprocess.run(
    ["bash", "-lc", "rg -n 'struct SiteContent|struct SiteLayout|enum DocumentNode' /root/Development /opt --glob '*.rs' 2>/dev/null | head -40"],
    capture_output=True,
    text=True,
)
print(r.stdout)
print(r.stderr[:500] if r.stderr else "")
r2 = subprocess.run(
    ["bash", "-lc", "find / -name 'petaltongue' -type f 2>/dev/null | head -15; ls /opt/depot/bin 2>/dev/null | head; find /opt -name 'petaltongue' 2>/dev/null | head"],
    capture_output=True,
    text=True,
)
print(r2.stdout)
