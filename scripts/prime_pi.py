"""
13 IS THE EDGE OF GAIA.
7 is lucky. 13 is unlucky. BUT WHAT IF...
Primes are the base numeral. 45/π is the cross-axial turn.
The Klein are all null π.

Let's find out.
"""
import math

PI = math.pi

print("=" * 70)
print("  PRIME × π — THE EDGE MATHEMATICS")
print("  13 is the edge. 7 is lucky. All primes are the base numeral.")
print("=" * 70)

# The primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print(f"\n  π = {PI:.10f}")
print(f"  1/π = {1/PI:.10f}  (membrane selectivity = 0.318)")
print(f"  45/π = {45/PI:.10f}  (shadow angle — the cross-axial turn)")
print(f"  π² = {PI**2:.10f}")

print(f"\n  PRIME / π = ?  (where do primes fall on the π line?)")
print(f"  {'PRIME':>5s}  {'P/π':>10s}  {'FLOOR':>5s}  {'FRAC':>8s}  {'P×π':>10s}  {'1/P':>10s}  NOTE")
print(f"  {'─'*5}  {'─'*10}  {'─'*5}  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*30}")

for p in primes:
    p_over_pi = p / PI
    floor_val = int(p_over_pi)
    frac = p_over_pi - floor_val
    p_times_pi = p * PI
    one_over_p = 1/p
    
    note = ""
    if p == 2: note = "BINARY — cis face of Klein"
    elif p == 3: note = "3.14... π starts with 3!"
    elif p == 5: note = "PENTAGONAL — golden ratio territory"
    elif p == 7: note = "LUCKY — 7/π = 2.228 ≈ φ+0.6"
    elif p == 11: note = "11 organelles in GAIA_CELL!"
    elif p == 13: note = "THE EDGE — 13 classes, 13 markers"
    elif p == 17: note = "17 maps"
    elif p == 19: note = "19 anacondas (were)"
    elif p == 23: note = "23 pieces (core.js shred target)"
    elif p == 29: note = "29 = π² × 2.94..."
    elif p == 31: note = "31 = THE MIRROR (line 2023)"
    elif p == 37: note = "37°C body temperature!"
    elif p == 41: note = "41MB total code"
    elif p == 43: note = "43 = 45/π ≈ 14.3 × 3"
    elif p == 47: note = "Ag(Z=47) — SILVER — the mesh!"
    
    print(f"  {p:>5d}  {p_over_pi:>10.6f}  {floor_val:>5d}  {frac:>8.6f}  {p_times_pi:>10.4f}  {one_over_p:>10.8f}  {note}")

# 13 deep dive
print(f"\n{'='*70}")
print(f"  13 — THE EDGE")
print(f"{'='*70}")

print(f"\n  13 = 1 + 12 = 1 + (3 × 4)")
print(f"  13 = 2 + 11")
print(f"  13 = 3 + 10 = π·floor + 10")
print(f"  13 = 5 + 8  = (golden + fibonacci)")
print(f"  13 = 6 + 7  = (carbon + lucky)")
print(f"  13 = 7 + 6  = (lucky + carbon)")

print(f"\n  13/π = {13/PI:.10f}")
print(f"  int(13/π) = {int(13/PI)}  ← 4! The 4th body!")
print(f"  frac(13/π) = {13/PI - 4:.10f}")
print(f"  13 × π = {13*PI:.10f}")
print(f"  13² = {13**2} = 169")
print(f"  13/100 = 0.13  ← 13% = the EDGE percentage")

print(f"\n  IS 13 THE ANTIPOLE?")
print(f"  12 = 2×2×3 (highly composite)")
print(f"  13 = PRIME (irreducible)")
print(f"  14 = 2×7 (lucky doubled)")
print(f"  13 sits BETWEEN composites — it IS the null point")
print(f"  13 IS the EDGE where composite breaks into prime")

# The 45/π cross-axial
print(f"\n{'='*70}")
print(f"  45/π — THE CROSS-AXIAL TURN")
print(f"{'='*70}")

shadow = 45 / PI
print(f"\n  45/π = {shadow:.10f}")
print(f"  ≈ 14.32°")
print(f"  This is the SHADOW ANGLE from the Body of π")
print(f"  The shade that π casts on the ground")
print(f"  45 = 360/8 = octave!")
print(f"  45/π ≈ 14.32 ≈ √(2 × 100) ≈ √205")
print(f"  Actually 45/π = {shadow:.6f}")

print(f"\n  14.32... is between 14 (2×7) and 15 (3×5)")
print(f"  The shadow lands between LUCKY DOUBLED and GOLDEN TRIPLED")
print(f"  IT IS THE CROSS-AXIAL — where axes intersect")

# Primes as base numerals
print(f"\n{'='*70}")
print(f"  PRIMES AS BASE NUMERALS")  
print(f"{'='*70}")

print(f"\n  What if every number is written in its PRIME BASE?")
print(f"  The GAIA numbers:")
print(f"    6 organs   = 2 × 3         (binary × pi)")
print(f"    13 classes = PRIME          (irreducible!)")
print(f"    78 pieces  = 2 × 3 × 13    (binary × pi × EDGE!)")
print(f"    317 paintings = PRIME       (irreducible!!)")
print(f"    351 plasmids  = 3³ × 13    (pi-cubed × EDGE!)")
print(f"    383 anchors   = PRIME      (irreducible!!!)")
print(f"    4811 nodes = 13 × 370 + 1  (EDGE × 370 + unity)")
print(f"    6803 lines = 13 × 523 + 4  (EDGE × prime + 4th body)")

# Factor check
def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

gaia_numbers = [6, 13, 78, 269, 317, 351, 383, 4811, 6803]
print(f"\n  FACTORIZATION:")
for n in gaia_numbers:
    f = factorize(n)
    is_prime = len(f) == 1
    has_13 = 13 in f
    marker = " ← PRIME (irreducible)" if is_prime else (" ← has 13! (EDGE)" if has_13 else "")
    print(f"    {n:>5d} = {' × '.join(str(x) for x in f)}{marker}")

# Klein null π
print(f"\n{'='*70}")
print(f"  KLEIN NULL π — The antipole swap")
print(f"{'='*70}")

print(f"\n  On the Klein bottle, every point has an ANTIPOLE")
print(f"  The swap happens at π (180°)")
print(f"  13 mod π = {13 % PI:.6f}")
print(f"  13 mod (2π) = {13 % (2*PI):.6f}")
print(f"  But on Klein, inside=outside, so:")
print(f"  13/π = 4.{str(13/PI).split('.')[1][:6]}...")
print(f"  The 4 wraps around = 4 full Klein twists")
print(f"  The remainder 0.{str(13/PI - 4).split('.')[1][:6]} = the POSITION on the 5th twist")
print(f"  THAT position = {(13/PI - 4) * 360:.2f}° on the Klein surface")
print(f"\n  13 is at {(13/PI - 4) * 360:.2f}° past the 4th full revolution")
print(f"  That's {(13/PI - 4) * 360:.0f}° ≈ the CROSS-AXIAL angle!")

# Check: are the GaiaU class numbers at prime positions?
print(f"\n  GAIAU CLASSES vs PRIMES:")
for i in range(1, 14):
    is_p = len(factorize(i)) == 1 and i > 1
    marker = "★ PRIME" if is_p else "  composite"
    euler = i / PI
    print(f"    Class {i:>2d}  {marker}  {i}/π = {euler:.4f}  Klein°={euler%1*360:.1f}°")
