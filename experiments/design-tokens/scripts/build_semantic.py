"""
Semantic layer: maps primitives to purpose, per theme. Built together with
inline contrast verification so the mapping can be iterated against real
numbers rather than eyeballed. scripts/audit.py re-runs this same
verification and emits the formal deliverable report/table.
"""
from build_primitives import ALL_RAMPS
from build_charts import ALL_CHART_TOKENS
from color import contrast_ratio

P = {name: {step: r["hex"] for step, r in ramp.items()} for name, ramp in ALL_RAMPS.items()}

WHITE = "#FFFFFF"
BLACK = "#000000"

# ---------------------------------------------------------------------------
# SURFACE
# ---------------------------------------------------------------------------
SURFACE = {
    "light": {
        "canvas": P["neutral"][50],     # #FAFAFC -- app background
        "raised": WHITE,                # cards/modals -- brighter than canvas = "raised"
        "sunken": P["neutral"][100],    # wells/insets/code blocks
        "overlay": "rgba(26, 25, 28, 0.48)",  # modal scrim, neutral-950 base @ 48%
        "inverse": P["neutral"][950],   # dark surface embedded in a light page (e.g. tooltip)
    },
    "dark": {
        "canvas": P["neutral"][950],    # #1A191C -- solved for relLum ~0.01
        "raised": P["neutral"][900],    # lighter than canvas = "raised" (dark-mode elevation convention)
        "sunken": BLACK,                # deeper than canvas for inset wells
        "overlay": "rgba(0, 0, 0, 0.64)",
        "inverse": P["neutral"][50],    # light surface embedded in a dark page
    },
}

# ---------------------------------------------------------------------------
# TEXT / FOREGROUND
# ---------------------------------------------------------------------------
TEXT = {
    "light": {
        "primary": P["neutral"][900],     # 16.02:1 vs white
        "secondary": P["neutral"][800],   # 11.80:1 vs white
        "tertiary": P["neutral"][700],    # 7.26:1 vs white -- AAA anchor, floor of the AAA range
        "disabled": P["neutral"][400],    # WCAG-exempt (inactive component text has no contrast requirement)
        "inverse": P["neutral"][300],     # for text on surface.inverse (dark) -- AAA anchor
        "link": P["purple"][700],         # AAA anchor vs white
        "on-primary": WHITE,              # vs interactive.primary.default (purple-600): AAA LARGE TEXT tier, see audit note
    },
    "dark": {
        "primary": P["neutral"][50],      # 16.79:1 vs neutral-950
        "secondary": P["neutral"][100],   # 15.56:1 vs neutral-950
        "tertiary": P["neutral"][300],    # AAA anchor
        "disabled": P["neutral"][600],    # WCAG-exempt
        "inverse": P["neutral"][700],     # for text on surface.inverse (light) -- AAA anchor vs white
        "link": P["purple"][300],         # AAA anchor vs neutral-950
        # dark-mode primary button fill is a LIGHT purple (purple-400, see INTERACTIVE_PRIMARY below) --
        # needs dark, not light, text on top of it.
        "on-primary": BLACK,
    },
}

# ---------------------------------------------------------------------------
# BORDER
# ---------------------------------------------------------------------------
BORDER = {
    "light": {
        # default/strong are "functionally required" boundaries (verified to the 4.5:1
        # internal non-text standard); subtle is a decorative divider, deliberately
        # sub-threshold -- see EXEMPT check below and README for the WCAG 1.4.11 rationale.
        "default": P["neutral"][600],   # 5.29:1 vs canvas
        "subtle": P["neutral"][200],    # EXEMPT: decorative
        "strong": P["neutral"][700],    # 8.03:1 vs canvas
        "focus": P["purple"][600],
    },
    "dark": {
        "default": P["neutral"][500],   # 4.78:1 vs canvas
        "subtle": P["neutral"][800],    # EXEMPT: decorative
        "strong": P["neutral"][400],    # 7.06:1 vs canvas
        "focus": P["purple"][400],
    },
}

FOCUS_RING = {
    "light": P["purple"][600],
    "dark": P["purple"][400],
}

# ---------------------------------------------------------------------------
# INTERACTIVE / PRIMARY
# ---------------------------------------------------------------------------
INTERACTIVE_PRIMARY = {
    "light": {
        "default": P["purple"][600],
        "hover": P["purple"][700],
        "active": P["purple"][800],
        "disabled": P["neutral"][200],
        "subtle": P["purple"][100],     # tinted background (e.g. secondary button, selected row)
        "on-primary": WHITE,
    },
    "dark": {
        # dark-mode primary fill is intentionally a LIGHT purple, not a dark one --
        # purple-500 only reaches 3.93:1 against the dark canvas (fails our 4.5:1
        # internal non-text standard for the control itself being visible/distinct);
        # purple-400 clears it with margin. Interaction states get progressively
        # LIGHTER (brighter/more saturated-reading), the inverse of the light-theme
        # progression, matching how dark-mode brand fills conventionally behave.
        "default": P["purple"][400],
        "hover": P["purple"][300],
        "active": P["purple"][200],
        "disabled": P["neutral"][800],
        "subtle": P["purple"][950],
        "on-primary": BLACK,
    },
}

# ---------------------------------------------------------------------------
# FEEDBACK (success / warning / danger / info)
# ---------------------------------------------------------------------------
def feedback_family(prim_key):
    return {
        "light": {
            "background": P[prim_key][50],
            "border": P[prim_key][600],   # darkened from 300 -> clears the 4.5:1 non-text internal standard
            "text": P[prim_key][700],     # AAA anchor
            "solid": P[prim_key][600],    # vivid filled background (danger button, solid badge) -- same value in both themes
            "on-status": WHITE,           # text on .solid (banners, badges) -- vivid-600 stays dark-ish in both themes
        },
        "dark": {
            "background": P[prim_key][950],
            "border": P[prim_key][400],   # lightened from 700 -> clears the 4.5:1 non-text internal standard vs dark canvas
            "text": P[prim_key][300],     # AAA anchor
            "solid": P[prim_key][600],
            "on-status": WHITE,           # vivid-600 fill is unchanged across themes, so white text still wins here too
        },
    }

# Functional (semantic) role -> primitive color-name ramp. Primitives are
# meaning-agnostic (see README "Primitives are color-named, not role-named");
# this is the one place that assigns meaning to a specific hue.
FEEDBACK = {
    "success": feedback_family("green"),
    "warning": feedback_family("amber"),
    "danger": feedback_family("red"),
    "info": feedback_family("blue"),
}


# ===========================================================================
# VERIFICATION
# ===========================================================================
AAA_NORMAL = 7.0
AAA_LARGE = 4.5
NONTEXT_INTERNAL = 4.5
NONTEXT_WCAG_AA = 3.0

CHECKS = []  # (label, fg_hex, bg_hex, target_ratio, target_name, exempt_reason_or_None)

def check(label, fg, bg, target, target_name, exempt=None):
    CHECKS.append((label, fg, bg, target, target_name, exempt))

for theme in ["light", "dark"]:
    canvas = SURFACE[theme]["canvas"]
    raised = SURFACE[theme]["raised"]
    sunken = SURFACE[theme]["sunken"]

    # text vs canvas AND vs raised (both are realistic surfaces text sits on)
    for role in ["primary", "secondary", "tertiary"]:
        check(f"text.{role} ({theme}) vs canvas", TEXT[theme][role], canvas, AAA_NORMAL, "AAA normal 7:1")
        check(f"text.{role} ({theme}) vs raised", TEXT[theme][role], raised, AAA_NORMAL, "AAA normal 7:1")

    check(f"text.disabled ({theme}) vs canvas", TEXT[theme]["disabled"], canvas, None, "exempt",
          "WCAG 2.1: inactive/disabled UI components and their text have no contrast requirement")

    inverse_bg = SURFACE[theme]["inverse"]
    check(f"text.inverse ({theme}) vs surface.inverse", TEXT[theme]["inverse"], inverse_bg, AAA_NORMAL, "AAA normal 7:1")

    check(f"text.link ({theme}) vs canvas", TEXT[theme]["link"], canvas, AAA_NORMAL, "AAA normal 7:1")
    check(f"text.link ({theme}) vs raised", TEXT[theme]["link"], raised, AAA_NORMAL, "AAA normal 7:1")

    # on-primary: text on the DEFAULT filled primary button -- documented as AAA-large tier
    # (button labels are explicitly "large text" per the brief's own definition).
    prim_default = INTERACTIVE_PRIMARY[theme]["default"]
    check(f"text.on-primary ({theme}) vs interactive.primary.default", TEXT[theme]["on-primary"], prim_default,
          AAA_LARGE, "AAA large-text 4.5:1 (button labels/headings only)")
    check(f"interactive.primary.on-primary ({theme}) vs interactive.primary.default (same token pair)",
          INTERACTIVE_PRIMARY[theme]["on-primary"], prim_default, AAA_LARGE, "AAA large-text 4.5:1 (button labels/headings only)")
    # active state has more contrast headroom than default in every case here -- confirm it also
    # clears full AAA normal-text 7:1, so on-primary text is safe even for longer strings once active/hovered.
    prim_active = INTERACTIVE_PRIMARY[theme]["active"]
    check(f"text.on-primary ({theme}) vs interactive.primary.active (normal-text safety check)",
          TEXT[theme]["on-primary"], prim_active, AAA_NORMAL, "AAA normal 7:1")

    # borders: internal non-text standard 4.5:1 vs canvas
    check(f"border.default ({theme}) vs canvas", BORDER[theme]["default"], canvas, NONTEXT_INTERNAL, "non-text internal 4.5:1")
    check(f"border.strong ({theme}) vs canvas", BORDER[theme]["strong"], canvas, NONTEXT_INTERNAL, "non-text internal 4.5:1")
    check(f"border.subtle ({theme}) vs canvas", BORDER[theme]["subtle"], canvas, None, "decorative",
          "subtle border is intentionally sub-threshold (barely-there divider, not a required-to-perceive boundary)")
    check(f"border.focus ({theme}) vs canvas", BORDER[theme]["focus"], canvas, NONTEXT_INTERNAL, "non-text internal 4.5:1")
    check(f"focusRing ({theme}) vs canvas", FOCUS_RING[theme], canvas, NONTEXT_INTERNAL, "non-text internal 4.5:1")

    # interactive primary button fill vs canvas -- needs to read as a distinct control (non-text internal std)
    check(f"interactive.primary.default ({theme}) vs canvas", prim_default, canvas, NONTEXT_INTERNAL, "non-text internal 4.5:1")

    # component-layer reuses: link hover state (active-purple as text), tabs active-tab text
    prim_active_component = INTERACTIVE_PRIMARY[theme]["active"]
    check(f"component: link/tabs hover-active text ({theme}) vs canvas", prim_active_component, canvas, AAA_NORMAL, "AAA normal 7:1")

    # feedback
    for fam in ["success", "warning", "danger", "info"]:
        f = FEEDBACK[fam][theme]
        check(f"feedback.{fam}.text ({theme}) vs feedback.{fam}.background", f["text"], f["background"], AAA_NORMAL, "AAA normal 7:1")
        check(f"feedback.{fam}.text ({theme}) vs canvas", f["text"], canvas, AAA_NORMAL, "AAA normal 7:1")
        check(f"feedback.{fam}.border ({theme}) vs canvas", f["border"], canvas, NONTEXT_INTERNAL, "non-text internal 4.5:1")
        check(f"feedback.{fam}.on-status ({theme}) vs feedback.{fam}.solid (vivid fill)", f["on-status"], f["solid"], AAA_LARGE, "AAA large-text 4.5:1 (badge/banner labels)")


def run_checks(verbose=True):
    results = []
    for label, fg, bg, target, target_name, exempt in CHECKS:
        if bg.startswith("rgba"):
            continue  # overlay tokens: no fixed contrast pairing to check
        ratio = contrast_ratio(fg, bg)
        if target is None:
            status = "EXEMPT"
            passed = True
        else:
            passed = ratio >= target
            status = "PASS" if passed else "FAIL"
        results.append({
            "label": label, "fg": fg, "bg": bg, "ratio": round(ratio, 2),
            "target": target, "target_name": target_name, "status": status,
            "exempt_reason": exempt,
        })
    if verbose:
        fails = [r for r in results if r["status"] == "FAIL"]
        for r in results:
            flag = "" if r["status"] != "FAIL" else "  <<<<< FAIL"
            print(f"  [{r['status']:6s}] {r['label']:70s} {r['fg']} vs {r['bg']}  {r['ratio']:.2f}:1  (target {r['target_name']}){flag}")
        print(f"\n{len(results)} checks: {len(fails)} FAIL, {sum(1 for r in results if r['status']=='PASS')} PASS, {sum(1 for r in results if r['status']=='EXEMPT')} EXEMPT")
    return results


if __name__ == "__main__":
    run_checks()
