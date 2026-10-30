#!/usr/bin/env python3
"""Rewrite root-relative href=/network|/analysis|... → /publicRecord/... across melted HTML."""
import re
import subprocess
import time
from pathlib import Path

GAIA = Path("/opt/gaia-api/static/publicRecord")
NEST = Path("/opt/connect/publicRecord")

# paths that belong to the publicRecord site (not gaia organs)
PREFIX_NEED = (
    "network",
    "analysis",
    "path",
    "validate",
    "timeline",
    "evidence",
    "courts",
    "connections",
    "about",
    "actors",
    "entities",
    "coverage",
    "sources",
    "contact",
    "legal",
    "open-letters",
    "books",
    "site-index",
    "the-graph",
    "docs",
    "signal",
    "api",
    "graph",
)


def fix_html(s: str) -> str:
    # href=/network/... or href="/network/..." or src=/js/...
    def repl_href(m):
        quote = m.group(1) or ""
        path = m.group(2)
        first = path.strip("/").split("/", 1)[0]
        if first in PREFIX_NEED and not path.startswith("/publicRecord"):
            return f"href={quote}/publicRecord{path}{quote}"
        return m.group(0)

    s2 = re.sub(r"""href=(["']?)(/(?:""" + "|".join(PREFIX_NEED) + r""")[^"'>\s]*)\1""", repl_href, s)

    # also unquoted: href=/network/foo
    s2 = re.sub(
        r"href=/(?!publicRecord/)(" + "|".join(PREFIX_NEED) + r")(/[^>\s]*)",
        r"href=/publicRecord/\1\2",
        s2,
    )
    return s2


n = 0
changed = 0
for root in (GAIA, NEST):
    for p in root.rglob("*.html"):
        n += 1
        s = p.read_text(encoding="utf-8", errors="replace")
        s2 = fix_html(s)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
            changed += 1

print("scanned", n, "changed", changed)

# verify parents sample links
parents = (GAIA / "path/parents/index.html").read_text(encoding="utf-8", errors="replace")
for needle in [
    "href=/publicRecord/network/actors/brian-banks/",
    "href=/publicRecord/network/actors/joseph-holland/",
    "href=/publicRecord/analysis/funding-flow/",
    "href=/network/actors/brian-banks/",
    "OPEN DEEP STACK",
]:
    print(needle, needle in parents)

subprocess.run(["systemctl", "restart", "gaia-api"], check=False)
time.sleep(1)
# probe deep targets
for url in [
    "http://127.0.0.1:9876/publicRecord/network/actors/brian-banks/",
    "http://127.0.0.1:9876/publicRecord/network/actors/joseph-holland/",
    "http://127.0.0.1:9876/publicRecord/analysis/funding-flow/",
    "http://127.0.0.1:9876/publicRecord/network/judges/",
    "http://127.0.0.1:9876/publicRecord/validate/",
    "http://127.0.0.1:9876/parents-deep",
]:
    rr = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
    )
    print(rr.stdout, url)
print("DONE")
