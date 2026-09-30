"""
Farthest-point-sampling search for an 8-color CVD-safe categorical palette.

Candidate pool: OKLCH colors at a grid of hues (every 6 deg) x 3 lightness
bands (deep/medium/light) x per-band chroma tuned near-gamut-max for
visual "weight" parity. For every candidate we compute FOUR renderings:
normal vision, protanopia, deuteranopia, tritanopia. The distance between
two candidates is defined as the MINIMUM Euclidean sRGB distance across
those four renderings (worst case across vision types) -- this is what
actually matters for CVD-safety, not just normal-vision distance.

We seed the selection with the brand purple (primitive purple-500-ish),
then greedily add whichever remaining candidate maximizes the minimum
worst-case distance to every already-chosen color, until 8 are picked.
A minimum lightness gap is also enforced against neighbors in hue to
avoid picking two colors that are CVD-safe only by lightness trickery
but look like near-duplicates to normal vision.
"""
import itertools
from color import oklch_to_hex, simulate_colorblindness, euclidean_rgb_distance
from build_primitives import PURPLE_HUE

CVD_KINDS = ["protanopia", "deuteranopia", "tritanopia"]

def renderings(hex_color):
    return [hex_color] + [simulate_colorblindness(hex_color, k) for k in CVD_KINDS]

def worst_case_distance(hex_a, hex_b):
    ra, rb = renderings(hex_a), renderings(hex_b)
    return min(euclidean_rgb_distance(a, b) for a, b in zip(ra, rb))

# Candidate pool: 3 lightness bands with chroma tuned per band for visual parity
BANDS = [
    ("deep",   0.55, 0.16),
    ("medium", 0.66, 0.145),
    ("light",  0.78, 0.12),
]

def build_pool():
    pool = []
    for hue in range(0, 360, 6):
        for band_name, L, C in BANDS:
            hx, clipped = oklch_to_hex(L, C, hue)
            pool.append({"hue": hue, "band": band_name, "L": L, "C": C, "hex": hx, "clipped": clipped})
    return pool

def farthest_point_sample(pool, seed_hex, n=8, min_hue_gap=28):
    chosen = [{"hue": PURPLE_HUE, "band": "seed", "L": None, "C": None, "hex": seed_hex}]
    while len(chosen) < n:
        best = None
        best_score = -1
        for cand in pool:
            # avoid picking the same hue (or a near-neighbor) twice across ANY band --
            # categorical colors must be distinguishable by hue, not just by lightness.
            too_close_hue = any(
                min(abs(cand["hue"] - c["hue"]), 360 - abs(cand["hue"] - c["hue"])) < min_hue_gap
                for c in chosen
            )
            if too_close_hue:
                continue
            d = min(worst_case_distance(cand["hex"], c["hex"]) for c in chosen)
            if d > best_score:
                best_score = d
                best = cand
        if best is None:
            break
        chosen.append(best)
    return chosen

if __name__ == "__main__":
    pool = build_pool()
    seed_hex, _ = oklch_to_hex(0.58, 0.19, PURPLE_HUE)
    print(f"Seed (brand purple): {seed_hex}")

    chosen = farthest_point_sample(pool, seed_hex, n=8)

    print("\n=== Selected palette ===")
    for c in chosen:
        print(f"  hue={c['hue']:>3}  band={c['band']:6s}  {c['hex']}")

    print("\n=== Pairwise worst-case (min across normal+3 CVD) distances ===")
    pairs = []
    for a, b in itertools.combinations(chosen, 2):
        d = worst_case_distance(a["hex"], b["hex"])
        pairs.append((d, a["hex"], b["hex"]))
    pairs.sort(key=lambda x: x[0])
    for d, ha, hb in pairs:
        flag = "  <-- LOW" if d < 40 else ""
        print(f"  {ha} vs {hb}  worst-case dist={d:6.2f}{flag}")

    print(f"\nMinimum pairwise worst-case distance in final palette: {pairs[0][0]:.2f}")
