"""
Charts/data-visualization tier: categorical (8, CVD-safe), sequential,
diverging, and supporting (axis/gridline/label) tokens.
"""
import itertools
from color import (
    oklch_to_hex, relative_luminance, contrast_ratio,
    simulate_colorblindness, euclidean_rgb_distance,
)
from build_primitives import PURPLE_HUE, NEUTRAL_HUE, CANVAS_DARK_HEX

# ---------------------------------------------------------------------------
# CATEGORICAL — 8 mutually distinguishable, CVD-safe swatches.
# Strategy: vary hue AND lightness/chroma together (not hue rotation alone)
# so that pairs which collapse toward each other under a given dichromacy
# (e.g. red/green under protanopia+deuteranopia) are still separated by a
# lightness difference. This mirrors the logic behind Okabe-Ito.
# ---------------------------------------------------------------------------
# Found via scripts/optimize_categorical.py: farthest-point sampling over an
# OKLCH candidate grid (hue x 3 lightness bands), scored by the MINIMUM
# Euclidean sRGB distance across {normal vision, protanopia, deuteranopia,
# tritanopia} for every pair. Naive evenly-spaced hues (the first attempt)
# put purple and blue only 6.4 apart under deuteranopia -- this search
# maximizes the worst-case pairwise distance directly. Final minimum
# pairwise distance across all 8 colors, all 4 vision types: 48.56.
# (hue, L, C) triples:
CATEGORICAL_CANDIDATES = [
    ("cat-1-purple",     297, 0.58, 0.19),   # seed: brand hue
    ("cat-2-coral",       42, 0.78, 0.12),
    ("cat-3-rose",        12, 0.55, 0.16),
    ("cat-4-sky-blue",   264, 0.78, 0.12),
    ("cat-5-mustard",     90, 0.66, 0.145),
    ("cat-6-deep-teal",  216, 0.55, 0.16),
    ("cat-7-mint",       186, 0.78, 0.12),
    ("cat-8-olive-green",126, 0.66, 0.145),
]

def build_categorical():
    out = {}
    for name, hue, L, C in CATEGORICAL_CANDIDATES:
        hx, clipped = oklch_to_hex(L, C, hue)
        out[name] = {"hex": hx, "L": L, "C": C, "H": hue, "clipped": clipped}
    return out


def cvd_report(categorical):
    """For each CVD type, simulate all 8 colors and report the minimum
    pairwise distance + which pair is closest."""
    kinds = ["protanopia", "deuteranopia", "tritanopia"]
    names = list(categorical.keys())
    report = {}
    for kind in kinds:
        sims = {n: simulate_colorblindness(categorical[n]["hex"], kind) for n in names}
        pairs = []
        for a, b in itertools.combinations(names, 2):
            d = euclidean_rgb_distance(sims[a], sims[b])
            pairs.append((d, a, b, sims[a], sims[b]))
        pairs.sort(key=lambda x: x[0])
        report[kind] = pairs
    return report


# ---------------------------------------------------------------------------
# SEQUENTIAL — single ramp for magnitude/heatmap, derived from primary hue.
# 9 steps, monotonic lightness, light->dark = low->high magnitude.
# ---------------------------------------------------------------------------
SEQUENTIAL_STEPS = [0, 1, 2, 3, 4, 5, 6, 7, 8]
SEQUENTIAL_L = [0.97, 0.90, 0.82, 0.73, 0.63, 0.53, 0.44, 0.34, 0.24]
SEQUENTIAL_C = [0.015, 0.05, 0.10, 0.15, 0.19, 0.215, 0.19, 0.155, 0.115]

def build_sequential():
    out = {}
    for i in SEQUENTIAL_STEPS:
        hx, clipped = oklch_to_hex(SEQUENTIAL_L[i], SEQUENTIAL_C[i], PURPLE_HUE)
        out[i] = {"hex": hx, "L": SEQUENTIAL_L[i], "C": SEQUENTIAL_C[i], "H": PURPLE_HUE, "clipped": clipped}
    return out


# ---------------------------------------------------------------------------
# DIVERGING — two-hue ramp around a neutral midpoint. Negative side = danger
# red (loss/below-baseline), positive side = a teal/cyan (gain/above-
# baseline) chosen (a) far from purple-brand hue to avoid implying "this IS
# the brand metric" and (b) far from danger-red hue for max distinguishability,
# (c) still distinguishable from success-green so diverging charts don't get
# read as a success/danger pair by accident.
# ---------------------------------------------------------------------------
DIVERGING_NEG_HUE = 25   # red, matches danger primitive
DIVERGING_POS_HUE = 195  # teal/cyan
DIVERGING_STEPS = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
DIVERGING_L = {-4: 0.30, -3: 0.42, -2: 0.56, -1: 0.72, 0: 0.90,
               1: 0.72, 2: 0.56, 3: 0.42, 4: 0.30}
DIVERGING_C = {-4: 0.145, -3: 0.185, -2: 0.195, -1: 0.13, 0: 0.006,
               1: 0.11, 2: 0.155, 3: 0.135, 4: 0.10}

def build_diverging():
    out = {}
    for step in DIVERGING_STEPS:
        hue = DIVERGING_NEG_HUE if step < 0 else (NEUTRAL_HUE if step == 0 else DIVERGING_POS_HUE)
        L, C = DIVERGING_L[step], DIVERGING_C[step]
        hx, clipped = oklch_to_hex(L, C, hue)
        out[step] = {"hex": hx, "L": L, "C": C, "H": hue, "clipped": clipped}
    return out


# ---------------------------------------------------------------------------
# SUPPORTING — axis line, gridline, data label text.
# Solved against BOTH light canvas (#FFFFFF) and dark canvas (neutral-950)
# so each has an explicit light/dark value meeting its own minimum.
# ---------------------------------------------------------------------------
def build_supporting():
    # Chart-specific targets per brief: axis-line & gridline (non-text) >=3:1;
    # data-label-text (text) >=4.5:1 -- deliberately relaxed vs the general
    # 7:1 UI-text / 4.5:1 non-text-internal-standard tiers, since dense charts
    # need lighter supporting marks to avoid visual noise. Verified below.
    from build_primitives import ALL_RAMPS
    neutral = ALL_RAMPS["neutral"]
    return {
        "axis-line": {
            "light": neutral[600]["hex"],   # 5.52:1 vs white
            "dark": neutral[500]["hex"],    # 4.78:1 vs neutral-950
        },
        "gridline": {
            "light": neutral[500]["hex"],   # 3.66:1 vs white -- subtler than axis, still clears 3:1
            "dark": neutral[600]["hex"],    # 3.17:1 vs neutral-950
        },
        "data-label-text": {
            "light": neutral[700]["hex"],   # 7.26:1 vs white (exceeds the 4.5:1 chart-text floor)
            "dark": neutral[300]["hex"],    # 7.32:1 vs neutral-950 (exceeds the 4.5:1 chart-text floor)
        },
    }


ALL_CHART_TOKENS = {
    "categorical": build_categorical(),
    "sequential": build_sequential(),
    "diverging": build_diverging(),
    "supporting": build_supporting(),
}

if __name__ == "__main__":
    cat = ALL_CHART_TOKENS["categorical"]
    print("=== Categorical ===")
    for name, v in cat.items():
        print(f"  {name:16s} {v['hex']}  L={v['L']:.2f} C={v['C']:.2f} H={v['H']}  clipped={v['clipped']}")

    print("\n=== CVD pairwise minimum distances (lower = more confusable) ===")
    report = cvd_report(cat)
    for kind, pairs in report.items():
        print(f"\n  -- {kind} --")
        for d, a, b, sa, sb in pairs[:4]:
            flag = "  <-- CHECK" if d < 40 else ""
            print(f"    {a:16s} vs {b:16s}  dist={d:6.2f}  ({sa} vs {sb}){flag}")

    print("\n=== Sequential ===")
    for i, v in ALL_CHART_TOKENS["sequential"].items():
        print(f"  {i}  {v['hex']}  L={v['L']:.2f} C={v['C']:.2f}  clipped={v['clipped']}")

    print("\n=== Diverging ===")
    for i, v in ALL_CHART_TOKENS["diverging"].items():
        print(f"  {i:+d}  {v['hex']}  L={v['L']:.2f} C={v['C']:.2f} H={v['H']}  clipped={v['clipped']}")

    print("\n=== Supporting ===")
    for name, v in ALL_CHART_TOKENS["supporting"].items():
        cr_light = contrast_ratio(v["light"], "#FFFFFF")
        cr_dark = contrast_ratio(v["dark"], CANVAS_DARK_HEX)
        print(f"  {name:18s} light={v['light']} ({cr_light:.2f}:1 vs white)   dark={v['dark']} ({cr_dark:.2f}:1 vs {CANVAS_DARK_HEX})")
