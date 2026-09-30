"""
Generates the primitive color ramps in OKLCH, solving specific "AAA anchor"
steps numerically so they hit exact WCAG contrast targets rather than being
eyeballed.

Design decisions (see README for full rationale):
  - All ramps share RAMP_STEPS positions: 25,50,100,200,300,400,500,600,
    700,800,900,950 (12 steps).
  - Hue is held constant across each ramp; only L (lightness) and C (chroma)
    vary. This is deliberate for predictability/maintainability. Chroma
    follows a "dome" shape (rises then falls) because sRGB gamut narrows
    at both lightness extremes -- attempting constant chroma across the
    whole ramp would force clipping at the ends.
  - Step 700 in every ramp is solved so its sRGB relative luminance is
    <= 0.095, which guarantees >=7.24:1 contrast against pure white
    (#FFFFFF) -- comfortably clearing the 7:1 AAA text minimum with an
    8-bit-hex-rounding safety margin.
  - Step 300 in every ramp is solved so its relative luminance is
    >= 0.40, which guarantees >=7.5:1 contrast against the dark-theme
    canvas color (neutral-950, luminance ~0.01, solved below) -- again
    clearing 7:1 with margin.
  - Neutral-950 (dark canvas) and neutral-25 are solved to specific
    luminance targets first since other ramps' dark-mode anchors are
    verified against neutral-950.
"""
import json
from color import (
    oklch_to_hex, hex_to_oklch, relative_luminance, contrast_ratio,
)

RAMP_STEPS = [25, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

LIGHT_AAA_LUM_MAX = 0.080   # margin'd for the tightest real light surface (neutral-50 canvas, lum ~0.957), not just #FFFFFF
DARK_AAA_LUM_MIN = 0.40     # placeholder; recomputed below from actual neutral-900 (raised) luminance


def solve_L_for_luminance(target_lum, C, H, mode="max", lo=0.0, hi=1.0, iters=60):
    """Binary-search OKLCH L so the resulting hex's sRGB relative luminance
    hits target_lum. mode='max' finds largest L with lum <= target (for dark
    anchors), mode='min' finds smallest L with lum >= target (for light anchors)."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        hx, _ = oklch_to_hex(mid, C, H)
        lum = relative_luminance(hx)
        if mode == "max":  # want lum <= target; L and lum are positively correlated
            if lum <= target_lum:
                lo = mid
            else:
                hi = mid
        else:  # mode == 'min', want lum >= target
            if lum >= target_lum:
                hi = mid
            else:
                lo = mid
    result_L = lo if mode == "max" else hi
    hx, clipped = oklch_to_hex(result_L, C, H)
    return result_L, hx, clipped


def build_ramp(name, hue, chroma_curve, l_curve, anchor_700_C=None, anchor_300_C=None,
                solve_anchors=True):
    """
    chroma_curve: dict {step: C}
    l_curve: dict {step: L} (initial guess; 700/300 overwritten if solve_anchors)
    """
    ramp = {}
    L_by_step = dict(l_curve)

    if solve_anchors:
        c700 = anchor_700_C if anchor_700_C is not None else chroma_curve[700]
        L700, hex700, clip700 = solve_L_for_luminance(LIGHT_AAA_LUM_MAX, c700, hue, mode="max")
        L_by_step[700] = L700
        chroma_curve = dict(chroma_curve)
        chroma_curve[700] = c700

        c300 = anchor_300_C if anchor_300_C is not None else chroma_curve[300]
        L300, hex300, clip300 = solve_L_for_luminance(DARK_AAA_LUM_MIN, c300, hue, mode="min")
        L_by_step[300] = L300
        chroma_curve[300] = c300

    for step in RAMP_STEPS:
        L = L_by_step[step]
        C = chroma_curve[step]
        hx, clipped = oklch_to_hex(L, C, hue)
        ramp[step] = {
            "hex": hx, "L": round(L, 4), "C": round(C, 4), "H": round(hue, 2),
            "clipped": clipped, "relLum": round(relative_luminance(hx), 4),
        }
    return ramp


def print_ramp(name, ramp):
    print(f"\n--- {name} ---")
    for step in RAMP_STEPS:
        r = ramp[step]
        vs_white = contrast_ratio(r["hex"], "#FFFFFF")
        flag = " CLIP" if r["clipped"] else ""
        print(f"  {step:>4}  {r['hex']}  L={r['L']:.3f} C={r['C']:.3f}  "
              f"relLum={r['relLum']:.4f}  vsWhite={vs_white:.2f}:1{flag}")


# ---------------------------------------------------------------------------
# NEUTRAL — solved first; dark canvas (950) anchors the dark-mode AAA target
# for every other ramp.
# ---------------------------------------------------------------------------
NEUTRAL_HUE = 297.0  # cool lean, harmonizes with purple brand hue (see README)
NEUTRAL_CHROMA = {
    25: 0.0025, 50: 0.003, 100: 0.004, 200: 0.005, 300: 0.006, 400: 0.007,
    500: 0.008, 600: 0.009, 700: 0.009, 800: 0.008, 900: 0.006, 950: 0.005,
}
NEUTRAL_L_GUESS = {
    25: 0.995, 50: 0.985, 100: 0.960, 200: 0.895, 300: 0.815, 400: 0.720,
    500: 0.620, 600: 0.520, 700: 0.430, 800: 0.340, 900: 0.250, 950: 0.150,
}

# Solve neutral-950 for a specific dark-canvas luminance target (~0.01) and
# neutral-25 for a specific light-canvas-adjacent luminance (very near white).
CANVAS_DARK_LUM_TARGET = 0.010
L950, hex950, clip950 = solve_L_for_luminance(CANVAS_DARK_LUM_TARGET, NEUTRAL_CHROMA[950], NEUTRAL_HUE, mode="max")
NEUTRAL_L_GUESS[950] = L950

neutral_ramp = build_ramp("neutral", NEUTRAL_HUE, NEUTRAL_CHROMA, NEUTRAL_L_GUESS, solve_anchors=True)

CANVAS_DARK_HEX = neutral_ramp[950]["hex"]
CANVAS_DARK_LUM = neutral_ramp[950]["relLum"]

# raised (dark) = neutral-900, LIGHTER than canvas (950) -- that's the stricter
# constraint for "text is light enough to hit 7:1", since a lighter dark-mode
# surface leaves less room. Solve DARK_AAA_LUM_MIN against neutral-900, not 950.
_raised900_hex, _ = oklch_to_hex(NEUTRAL_L_GUESS[900], NEUTRAL_CHROMA[900], NEUTRAL_HUE)
RAISED_DARK_LUM = relative_luminance(_raised900_hex)
DARK_AAA_LUM_MIN = 7.0 * (RAISED_DARK_LUM + 0.05) - 0.05
DARK_AAA_LUM_MIN *= 1.08  # safety margin above the exact 7:1 threshold
print(f"Canvas dark (neutral-950) = {CANVAS_DARK_HEX}  relLum={CANVAS_DARK_LUM:.4f}")
print(f"Raised dark (neutral-900) relLum={RAISED_DARK_LUM:.4f}")
print(f"Recomputed DARK_AAA_LUM_MIN (margin'd vs raised) = {DARK_AAA_LUM_MIN:.4f}")

# Rebuild neutral ramp's 300 anchor now that DARK_AAA_LUM_MIN is precise.
neutral_ramp = build_ramp("neutral", NEUTRAL_HUE, NEUTRAL_CHROMA, NEUTRAL_L_GUESS, solve_anchors=True)


# ---------------------------------------------------------------------------
# Shared solver using the precise DARK_AAA_LUM_MIN
# ---------------------------------------------------------------------------
def build_ramp2(name, hue, chroma_curve, l_curve, anchor_700_C=None, anchor_300_C=None):
    ramp = {}
    L_by_step = dict(l_curve)
    chroma_curve = dict(chroma_curve)

    c700 = anchor_700_C if anchor_700_C is not None else chroma_curve[700]
    L700, hex700, clip700 = solve_L_for_luminance(LIGHT_AAA_LUM_MAX, c700, hue, mode="max")
    L_by_step[700] = L700
    chroma_curve[700] = c700

    c300 = anchor_300_C if anchor_300_C is not None else chroma_curve[300]
    L300, hex300, clip300 = solve_L_for_luminance(DARK_AAA_LUM_MIN, c300, hue, mode="min")
    L_by_step[300] = L300
    chroma_curve[300] = c300

    for step in RAMP_STEPS:
        L = L_by_step[step]
        C = chroma_curve[step]
        hx, clipped = oklch_to_hex(L, C, hue)
        ramp[step] = {
            "hex": hx, "L": round(L, 4), "C": round(C, 4), "H": round(hue, 2),
            "clipped": clipped, "relLum": round(relative_luminance(hx), 4),
        }
    return ramp


neutral_ramp = build_ramp2("neutral", NEUTRAL_HUE, NEUTRAL_CHROMA, NEUTRAL_L_GUESS)

# ---------------------------------------------------------------------------
# PURPLE (primary brand)
# ---------------------------------------------------------------------------
PURPLE_HUE = 297.0
PURPLE_CHROMA = {
    25: 0.012, 50: 0.022, 100: 0.045, 200: 0.085, 300: 0.135, 400: 0.185,
    500: 0.225, 600: 0.230, 700: 0.205, 800: 0.170, 900: 0.135, 950: 0.100,
}
PURPLE_L_GUESS = {
    25: 0.985, 50: 0.965, 100: 0.925, 200: 0.850, 300: 0.780, 400: 0.690,
    500: 0.595, 600: 0.520, 700: 0.430, 800: 0.345, 900: 0.270, 950: 0.195,
}
purple_ramp = build_ramp2("purple", PURPLE_HUE, PURPLE_CHROMA, PURPLE_L_GUESS)

# ---------------------------------------------------------------------------
# SUCCESS (green)
# ---------------------------------------------------------------------------
SUCCESS_HUE = 149.0
SUCCESS_CHROMA = {
    25: 0.014, 50: 0.026, 100: 0.050, 200: 0.090, 300: 0.130, 400: 0.155,
    500: 0.170, 600: 0.165, 700: 0.150, 800: 0.125, 900: 0.100, 950: 0.075,
}
SUCCESS_L_GUESS = {
    25: 0.985, 50: 0.965, 100: 0.925, 200: 0.850, 300: 0.775, 400: 0.685,
    500: 0.595, 600: 0.515, 700: 0.425, 800: 0.340, 900: 0.265, 950: 0.190,
}
success_ramp = build_ramp2("success", SUCCESS_HUE, SUCCESS_CHROMA, SUCCESS_L_GUESS)

# ---------------------------------------------------------------------------
# WARNING (amber)
# ---------------------------------------------------------------------------
WARNING_HUE = 75.0
WARNING_CHROMA = {
    25: 0.018, 50: 0.032, 100: 0.062, 200: 0.110, 300: 0.150, 400: 0.175,
    500: 0.185, 600: 0.180, 700: 0.160, 800: 0.130, 900: 0.100, 950: 0.075,
}
WARNING_L_GUESS = {
    25: 0.985, 50: 0.968, 100: 0.930, 200: 0.865, 300: 0.795, 400: 0.715,
    500: 0.630, 600: 0.545, 700: 0.450, 800: 0.360, 900: 0.280, 950: 0.200,
}
warning_ramp = build_ramp2("warning", WARNING_HUE, WARNING_CHROMA, WARNING_L_GUESS)

# ---------------------------------------------------------------------------
# DANGER (red)
# ---------------------------------------------------------------------------
DANGER_HUE = 25.0
DANGER_CHROMA = {
    25: 0.014, 50: 0.026, 100: 0.052, 200: 0.098, 300: 0.150, 400: 0.190,
    500: 0.210, 600: 0.205, 700: 0.180, 800: 0.150, 900: 0.120, 950: 0.090,
}
DANGER_L_GUESS = {
    25: 0.985, 50: 0.963, 100: 0.920, 200: 0.840, 300: 0.760, 400: 0.670,
    500: 0.580, 600: 0.500, 700: 0.415, 800: 0.335, 900: 0.260, 950: 0.190,
}
danger_ramp = build_ramp2("danger", DANGER_HUE, DANGER_CHROMA, DANGER_L_GUESS)

# ---------------------------------------------------------------------------
# INFO (blue)
# ---------------------------------------------------------------------------
INFO_HUE = 250.0
INFO_CHROMA = {
    25: 0.013, 50: 0.024, 100: 0.048, 200: 0.088, 300: 0.130, 400: 0.165,
    500: 0.185, 600: 0.185, 700: 0.165, 800: 0.135, 900: 0.105, 950: 0.080,
}
INFO_L_GUESS = {
    25: 0.985, 50: 0.965, 100: 0.925, 200: 0.850, 300: 0.775, 400: 0.685,
    500: 0.595, 600: 0.515, 700: 0.425, 800: 0.340, 900: 0.265, 950: 0.195,
}
info_ramp = build_ramp2("info", INFO_HUE, INFO_CHROMA, INFO_L_GUESS)

# ---------------------------------------------------------------------------
# TEAL (base color, no functional role assigned yet)
# ---------------------------------------------------------------------------
TEAL_HUE = 195.0
TEAL_CHROMA = {
    25: 0.013, 50: 0.024, 100: 0.048, 200: 0.088, 300: 0.125, 400: 0.150,
    500: 0.160, 600: 0.155, 700: 0.140, 800: 0.115, 900: 0.090, 950: 0.068,
}
TEAL_L_GUESS = {
    25: 0.985, 50: 0.965, 100: 0.925, 200: 0.850, 300: 0.775, 400: 0.685,
    500: 0.595, 600: 0.515, 700: 0.425, 800: 0.340, 900: 0.265, 950: 0.195,
}
teal_ramp = build_ramp2("teal", TEAL_HUE, TEAL_CHROMA, TEAL_L_GUESS)

# ---------------------------------------------------------------------------
# INDIGO (base color, no functional role assigned yet) -- sits between Blue
# (250) and Purple (297); distinguishability from both comes primarily from
# chroma, since 278 is roughly equidistant in hue from its two neighbors.
# ---------------------------------------------------------------------------
INDIGO_HUE = 278.0
INDIGO_CHROMA = {
    25: 0.012, 50: 0.022, 100: 0.044, 200: 0.082, 300: 0.128, 400: 0.172,
    500: 0.205, 600: 0.205, 700: 0.182, 800: 0.150, 900: 0.118, 950: 0.088,
}
INDIGO_L_GUESS = {
    25: 0.985, 50: 0.965, 100: 0.925, 200: 0.850, 300: 0.780, 400: 0.690,
    500: 0.595, 600: 0.515, 700: 0.425, 800: 0.340, 900: 0.265, 950: 0.195,
}
indigo_ramp = build_ramp2("indigo", INDIGO_HUE, INDIGO_CHROMA, INDIGO_L_GUESS)

# ---------------------------------------------------------------------------
# ORANGE (base color, no functional role assigned yet) -- sits between Red
# (25) and Amber (75).
# ---------------------------------------------------------------------------
ORANGE_HUE = 48.0
ORANGE_CHROMA = {
    25: 0.017, 50: 0.030, 100: 0.058, 200: 0.105, 300: 0.150, 400: 0.185,
    500: 0.200, 600: 0.195, 700: 0.172, 800: 0.140, 900: 0.108, 950: 0.080,
}
ORANGE_L_GUESS = {
    25: 0.985, 50: 0.967, 100: 0.928, 200: 0.858, 300: 0.785, 400: 0.700,
    500: 0.610, 600: 0.525, 700: 0.435, 800: 0.348, 900: 0.272, 950: 0.196,
}
orange_ramp = build_ramp2("orange", ORANGE_HUE, ORANGE_CHROMA, ORANGE_L_GUESS)


ALL_RAMPS = {
    "neutral": neutral_ramp,
    "purple": purple_ramp,
    "green": success_ramp,
    "amber": warning_ramp,
    "red": danger_ramp,
    "blue": info_ramp,
    "teal": teal_ramp,
    "indigo": indigo_ramp,
    "orange": orange_ramp,
}

if __name__ == "__main__":
    for name, ramp in ALL_RAMPS.items():
        print_ramp(name, ramp)

    print("\n=== Monotonicity check (relLum should strictly decrease as step increases) ===")
    for name, ramp in ALL_RAMPS.items():
        lums = [ramp[s]["relLum"] for s in RAMP_STEPS]
        ok = all(lums[i] > lums[i + 1] for i in range(len(lums) - 1))
        print(f"  {name}: {'OK' if ok else 'NOT MONOTONIC -> ' + str(lums)}")

    print("\n=== Any gamut clipping? ===")
    for name, ramp in ALL_RAMPS.items():
        clipped_steps = [s for s in RAMP_STEPS if ramp[s]["clipped"]]
        if clipped_steps:
            print(f"  {name}: clipped at steps {clipped_steps}")
    print("  (none printed above = no clipping anywhere)")

    print(f"\nCanvas dark (neutral-950): {CANVAS_DARK_HEX} relLum={CANVAS_DARK_LUM}")
