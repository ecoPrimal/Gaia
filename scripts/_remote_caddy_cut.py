#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

ROOT = Path("/opt/connect")
for name in ["raytrace.html", "valve.html", "crates.html", "arena.html"]:
    t = (ROOT / name).read_text(encoding="utf-8", errors="replace")
    print("===", name, "===")
    for m in re.finditer(r".{0,70}(?:localhost|127\.0\.0\.1).{0,70}", t, re.I):
        print(m.group(0).replace("\n", " ")[:160])

# rewrite remaining EXTERNAL leaks (keep arena INTERNAL gate)
REWRITE = [
    ("http://localhost:11434", "INTERNAL-ONLY"),
    ("http://127.0.0.1:11434", "INTERNAL-ONLY"),
    ("http://localhost", "https://nestgate.io"),
    ("http://127.0.0.1", "https://nestgate.io"),
]
for name in ["raytrace.html", "valve.html", "crates.html"]:
    p = ROOT / name
    t = p.read_text(encoding="utf-8", errors="replace")
    orig = t
    for a, b in REWRITE:
        t = t.replace(a, b)
    t = re.sub(
        r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?",
        "https://nestgate.io",
        t,
    )
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print("rewrote", name)

cf = Path("/etc/caddy/Caddyfile")
txt = cf.read_text()
if "handle /cut {" in txt and "rewrite * /cut.html" in txt:
    print("caddy already has /cut")
else:
    insert = (
        "\thandle /cut {\n"
        "\t\troot * /opt/connect\n"
        "\t\trewrite * /cut.html\n"
        "\t\tfile_server\n"
        "\t\theader X-Membrane-Cut INTERNAL-vs-EXTERNAL\n"
        "\t}\n"
        "\thandle /new {\n"
        "\t\troot * /opt/connect\n"
        "\t\trewrite * /new.html\n"
        "\t\tfile_server\n"
        "\t\theader X-Membrane-Cut NEW\n"
        "\t}\n"
    )
    marker = "\thandle {\n\t\troot * /opt/connect\n\t\tfile_server\n\t\tencode gzip\n\t}"
    idx = txt.find("header X-Surface nestgate-connect")
    if idx < 0:
        raise SystemExit("nestgate surface missing")
    block_start = txt.rfind(marker, 0, idx)
    if block_start < 0:
        raise SystemExit("catch-all not found")
    txt = txt[:block_start] + insert + "\n" + txt[block_start:]
    cf.write_text(txt)
    print("caddy patched")

r = subprocess.run(
    ["caddy", "validate", "--config", "/etc/caddy/Caddyfile"],
    capture_output=True,
    text=True,
)
print("validate", r.returncode)
print((r.stderr or r.stdout or "")[-400:])
if r.returncode != 0:
    raise SystemExit(1)
subprocess.check_call(["systemctl", "reload", "caddy"])
print("caddy reloaded")
