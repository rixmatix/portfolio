"""
Pure-Python OKLCH <-> sRGB color math + WCAG 2.1 contrast.

No external dependencies (numpy/colour/etc intentionally avoided so this
runs anywhere Python 3 runs). Matrices are Björn Ottosson's reference
OKLab/OKLCH transform (https://bottosson.github.io/posts/oklab/).

All hex colors are 8-bit sRGB, "#RRGGBB" (uppercase, no alpha).
"""
import math

# ---------------------------------------------------------------------------
# sRGB <-> linear sRGB
# ---------------------------------------------------------------------------

def _srgb_to_linear(c: float) -> float:
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    if c <= 0.0031308:
        return c * 12.92
    return 1.055 * (c ** (1 / 2.4)) - 0.055


# ---------------------------------------------------------------------------
# linear sRGB <-> OKLab
# ---------------------------------------------------------------------------

def _linear_srgb_to_oklab(r: float, g: float, b: float):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = math.copysign(abs(l) ** (1 / 3), l)
    m_ = math.copysign(abs(m) ** (1 / 3), m)
    s_ = math.copysign(abs(s) ** (1 / 3), s)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_ = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, a, b_


def _oklab_to_linear_srgb(L: float, a: float, b: float):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3

    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b_ = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, b_


# ---------------------------------------------------------------------------
# OKLCH <-> OKLab
# ---------------------------------------------------------------------------

def oklch_to_oklab(L: float, C: float, H_deg: float):
    h = math.radians(H_deg)
    return L, C * math.cos(h), C * math.sin(h)


def oklab_to_oklch(L: float, a: float, b: float):
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a))
    if H < 0:
        H += 360
    return L, C, H


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _rgb_in_gamut(r: float, g: float, b: float, eps: float = 1e-4) -> bool:
    return all(-eps <= v <= 1 + eps for v in (r, g, b))


def oklch_to_srgb_float(L: float, C: float, H_deg: float, gamut_map: bool = True):
    """
    Returns (r, g, b) floats in [0,1] sRGB (gamma-encoded), plus a bool
    `clipped` indicating whether chroma had to be reduced to fit sRGB gamut.

    Gamut mapping strategy: binary-search chroma reduction at constant L,H
    (simple, stable, standard "reduce chroma" approach recommended by the
    CSS Color 4 spec for OKLCH when a color is out of gamut).
    """
    def to_linear_rgb(_L, _C, _H):
        oL, oa, ob = oklch_to_oklab(_L, _C, _H)
        return _oklab_to_linear_srgb(oL, oa, ob)

    r, g, b = to_linear_rgb(L, C, H_deg)
    clipped = False
    if not _rgb_in_gamut(r, g, b):
        clipped = True
        lo, hi = 0.0, C
        for _ in range(40):
            mid = (lo + hi) / 2
            r, g, b = to_linear_rgb(L, mid, H_deg)
            if _rgb_in_gamut(r, g, b):
                lo = mid
            else:
                hi = mid
        r, g, b = to_linear_rgb(L, lo, H_deg)

    r = min(max(r, 0.0), 1.0)
    g = min(max(g, 0.0), 1.0)
    b = min(max(b, 0.0), 1.0)
    return _linear_to_srgb(r), _linear_to_srgb(g), _linear_to_srgb(b), clipped


def oklch_to_hex(L: float, C: float, H_deg: float):
    """Returns (hex_string, clipped_bool). L in [0,1], C typically 0-0.4, H in degrees."""
    r, g, b, clipped = oklch_to_srgb_float(L, C, H_deg)
    ri, gi, bi = round(r * 255), round(g * 255), round(b * 255)
    ri, gi, bi = (min(max(v, 0), 255) for v in (ri, gi, bi))
    return f"#{ri:02X}{gi:02X}{bi:02X}", clipped


def hex_to_rgb_float(hex_str: str):
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    return r, g, b


def hex_to_oklch(hex_str: str):
    r, g, b = hex_to_rgb_float(hex_str)
    lr, lg, lb = _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)
    L, a, bb = _linear_srgb_to_oklab(lr, lg, lb)
    return oklab_to_oklch(L, a, bb)


def relative_luminance(hex_str: str) -> float:
    r, g, b = hex_to_rgb_float(hex_str)
    R, G, B = _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    la = relative_luminance(hex_a)
    lb = relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# Colorblindness simulation (Brettel/Viénot-style LMS projection, standard
# matrices as used by e.g. daltonize / Coblis for anomalous-vision-free
# dichromacy simulation).
# ---------------------------------------------------------------------------

_LMS_FROM_LINEAR_RGB = [
    [0.31399022, 0.63951294, 0.04649755],
    [0.15537241, 0.75789446, 0.08670142],
    [0.01775239, 0.10944209, 0.87256922],
]
_LINEAR_RGB_FROM_LMS = [
    [5.47221206, -4.6419601, 0.16963708],
    [-1.1252419, 2.29317094, -0.1678952],
    [0.02980165, -0.19318073, 1.16364789],
]

_SIM_MATRICES = {
    # Protanopia (no L cone)
    "protanopia": [
        [0.0, 1.05118294, -0.05116099],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ],
    # Deuteranopia (no M cone)
    "deuteranopia": [
        [1.0, 0.0, 0.0],
        [0.9513092, 0.0, 0.04866992],
        [0.0, 0.0, 1.0],
    ],
    # Tritanopia (no S cone)
    "tritanopia": [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [-0.86744736, 1.86727089, 0.0],
    ],
}


def _mat_vec(mat, vec):
    return [sum(mat[i][j] * vec[j] for j in range(3)) for i in range(3)]


def simulate_colorblindness(hex_str: str, kind: str) -> str:
    """kind in {protanopia, deuteranopia, tritanopia}. Returns simulated hex."""
    r, g, b = hex_to_rgb_float(hex_str)
    lr, lg, lb = _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)
    lms = _mat_vec(_LMS_FROM_LINEAR_RGB, [lr, lg, lb])
    sim_lms = _mat_vec(_SIM_MATRICES[kind], lms)
    lin = _mat_vec(_LINEAR_RGB_FROM_LMS, sim_lms)
    lin = [min(max(v, 0.0), 1.0) for v in lin]
    srgb = [_linear_to_srgb(v) for v in lin]
    ri, gi, bi = (min(max(round(v * 255), 0), 255) for v in srgb)
    return f"#{ri:02X}{gi:02X}{bi:02X}"


def euclidean_rgb_distance(hex_a: str, hex_b: str) -> float:
    ra, ga, ba = hex_to_rgb_float(hex_a)
    rb, gb, bb = hex_to_rgb_float(hex_b)
    return math.sqrt((ra - rb) ** 2 + (ga - gb) ** 2 + (ba - bb) ** 2) * 255


if __name__ == "__main__":
    # Sanity checks against known reference values.
    print("=== Reference checks ===")

    # oklch(100% 0 0) should be white, oklch(0% 0 0) should be black
    white_hex, _ = oklch_to_hex(1.0, 0.0, 0.0)
    black_hex, _ = oklch_to_hex(0.0, 0.0, 0.0)
    print(f"L=1 C=0 -> {white_hex} (expect #FFFFFF)")
    print(f"L=0 C=0 -> {black_hex} (expect #000000)")

    # contrast of black vs white should be 21:1
    cr = contrast_ratio("#000000", "#FFFFFF")
    print(f"contrast(#000000, #FFFFFF) = {cr:.4f} (expect 21.0)")

    # Known culori/CSS Color 4 reference: oklch(62.8% 0.258 29.23) ≈ #FF0000 (srgb red)
    red_hex, red_clip = oklch_to_hex(0.62796, 0.22486, 29.234)
    print(f"oklch(62.796% 0.22486 29.234) -> {red_hex} clipped={red_clip} (expect ~#FF0000)")

    # roundtrip test
    L, C, H = hex_to_oklch("#7C3AED")  # tailwind violet-600
    print(f"#7C3AED -> oklch(L={L:.4f} C={C:.4f} H={H:.2f})")
    rt_hex, _ = oklch_to_hex(L, C, H)
    print(f"roundtrip -> {rt_hex} (expect #7C3AED)")

    # reference purples for hue calibration
    for name, hx in [
        ("tailwind purple-600", "#9333EA"),
        ("tailwind violet-600", "#7C3AED"),
        ("tailwind indigo-600", "#4F46E5"),
        ("tailwind fuchsia-600", "#C026D3"),
        ("tailwind pink-600", "#DB2777"),
    ]:
        L, C, H = hex_to_oklch(hx)
        print(f"{name:24s} {hx} -> L={L:.3f} C={C:.3f} H={H:.1f}")
