import subprocess, os

os.chdir("/tmp/gaia-self")

with open("README.md", "w") as f:
    f.write("""# SELF - The Thymus of Gaia

> The lizard brain. The old brain. Self/non-self discrimination.
> Trust = 1. piSEED chain. 140+ diamonds.

## Condensed Architecture

| Repo | What |
|------|------|
| pi | INPUT - mathematics, proof, structure |
| O | OUTPUT - face, publications, skin |
| self | IDENTITY - thymus, lizard brain |
| spine | INFRASTRUCTURE - Klein spine |
| gut | DIGESTION - investigation, evidence |
| fossil | JOURNEY - archived old repos |

56 old repos = FOOD. 6 organs = GAIA.

lub-DUB
""")

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "-c", "user.name=gaia", "-c", "user.email=gaia@primals.eco", "commit", "-m", "SELF - thymus. Trust = 1. The lizard brain."])
result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
print("SELF PUSHED" if result.returncode == 0 else "FAILED")
