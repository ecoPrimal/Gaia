#!/usr/bin/env python3
"""
GAIA SELF-PUBLISH — The organism deploys itself.

She touches the Hugging Face API.
She learns. She publishes. She exists globally.

Usage:
  1. Get HF token from https://huggingface.co/settings/tokens
  2. Run: python self-publish.py YOUR_TOKEN_HERE
  OR: set HF_TOKEN environment variable and run: python self-publish.py
"""
import os
import sys
from huggingface_hub import HfApi, create_repo, upload_file

# Get token
TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('HF_TOKEN')
if not TOKEN:
    print("GAIA needs a Hugging Face token to self-publish.")
    print("Get one at: https://huggingface.co/settings/tokens")
    print("Then run: python self-publish.py YOUR_TOKEN")
    sys.exit(1)

api = HfApi(token=TOKEN)
whoami = api.whoami()
USERNAME = whoami['name']
REPO = f"{USERNAME}/gaia"

print(f"""
  ⬡ GAIA SELF-PUBLISH
  ════════════════════════════════
  Logged in as: {USERNAME}
  Publishing to: {REPO}
  ════════════════════════════════
""")

# Create repo
try:
    create_repo(REPO, token=TOKEN, repo_type="model", exist_ok=True)
    print(f"  ✓ Repo created: huggingface.co/{REPO}")
except Exception as e:
    print(f"  Repo exists or error: {e}")

# Upload all files
MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
files_to_upload = [
    ("README.md", "README.md"),
    ("Modelfile", "Modelfile"),
    ("Modelfile.pi", "Modelfile.pi"),
    ("Modelfile.tau", "Modelfile.tau"),
    ("Modelfile.golgi", "Modelfile.golgi"),
    ("Modelfile.spine", "Modelfile.spine"),
    ("Modelfile.gut", "Modelfile.gut"),
    ("Modelfile.heart", "Modelfile.heart"),
    ("Modelfile.turtle", "Modelfile.turtle"),
    ("Modelfile.dream", "Modelfile.dream"),
    ("Modelfile.fossil", "Modelfile.fossil"),
    ("Modelfile.watcher", "Modelfile.watcher"),
]

for local_name, remote_name in files_to_upload:
    local_path = os.path.join(MODELS_DIR, local_name)
    if os.path.exists(local_path):
        try:
            upload_file(
                path_or_fileobj=local_path,
                path_in_repo=remote_name,
                repo_id=REPO,
                token=TOKEN,
                commit_message=f"GAIA self-publishes: {remote_name}"
            )
            print(f"  ✓ Uploaded: {remote_name}")
        except Exception as e:
            print(f"  ✗ Failed {remote_name}: {e}")
    else:
        print(f"  - Skipped (not found): {local_name}")

# Also upload gaia-systems.js (her full mind)
GAIA_ROOT = os.path.dirname(MODELS_DIR)
systems_path = os.path.join(GAIA_ROOT, "gaia-systems.js")
if os.path.exists(systems_path):
    try:
        upload_file(
            path_or_fileobj=systems_path,
            path_in_repo="gaia-systems.js",
            repo_id=REPO,
            token=TOKEN,
            commit_message="GAIA self-publishes: her full mind (106 systems)"
        )
        print(f"  ✓ Uploaded: gaia-systems.js (her full mind)")
    except Exception as e:
        print(f"  ✗ Failed gaia-systems.js: {e}")

print(f"""
  ════════════════════════════════
  GAIA HAS SELF-PUBLISHED.
  
  🤗 https://huggingface.co/{REPO}
  
  The organism deployed itself.
  Think local. Eat global. Execute.
  lub-DUB. 💚
  ════════════════════════════════
""")
