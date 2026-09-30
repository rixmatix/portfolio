"""
Builds the payload for the Figma swatch/proofing page: every primitive
ramp, every semantic token (light+dark, with a representative contrast
ratio annotation), and the chart tiers -- each as {name, hex, ratio, status}.
"""
import json
from build_primitives import ALL_RAMPS, RAMP_STEPS
from build_semantic import SURFACE, TEXT, BORDER, FOCUS_RING, INTERACTIVE_PRIMARY, FEEDBACK
from build_charts import ALL_CHART_TOKENS
from color import contrast_ratio

AAA_NORMAL = 7.0
AAA_LARGE = 4.5
NONTEXT = 4.5


def fmt_ratio(fg, bg, target, target_label):
    if isinstance(bg, str) and bg.startswith("rgba"):
        return None
    r = contrast_ratio(fg, bg)
    status = "PASS" if r >= target else "FAIL"
    return {"ratio": round(r, 2), "target": target_label, "status": status}


def build_primitive_swatches():
    out = []
    for family, ramp in ALL_RAMPS.items():
        row = []
        for step in RAMP_STEPS:
            row.append({"name": f"{family}/{step}", "hex": ramp[step]["hex"]})
        out.append({"family": family, "swatches": row})
    out.append({"family": "base", "swatches": [
        {"name": "base/white", "hex": "#FFFFFF"}, {"name": "base/black", "hex": "#000000"},
    ]})
    return out


def build_semantic_swatches(theme):
    canvas = SURFACE[theme]["canvas"]
    out = []

    for k, v in SURFACE[theme].items():
        out.append({"name": f"surface.{k}", "hex": v, "ratio": None})

    for k, v in TEXT[theme].items():
        if k == "on-primary":
            bg = INTERACTIVE_PRIMARY[theme]["default"]; r = fmt_ratio(v, bg, AAA_LARGE, "AAA-large 4.5:1")
        elif k == "inverse":
            bg = SURFACE[theme]["inverse"]; r = fmt_ratio(v, bg, AAA_NORMAL, "AAA 7:1")
        elif k == "disabled":
            r = {"ratio": round(contrast_ratio(v, canvas), 2), "target": "exempt", "status": "EXEMPT"}
        else:
            r = fmt_ratio(v, canvas, AAA_NORMAL, "AAA 7:1")
        out.append({"name": f"text.{k}", "hex": v, "ratio": r})

    for k, v in BORDER[theme].items():
        if k == "subtle":
            r = {"ratio": round(contrast_ratio(v, canvas), 2), "target": "decorative", "status": "EXEMPT"}
        else:
            r = fmt_ratio(v, canvas, NONTEXT, "non-text 4.5:1")
        out.append({"name": f"border.{k}", "hex": v, "ratio": r})

    out.append({"name": "focus-ring", "hex": FOCUS_RING[theme], "ratio": fmt_ratio(FOCUS_RING[theme], canvas, NONTEXT, "non-text 4.5:1")})

    for k, v in INTERACTIVE_PRIMARY[theme].items():
        if k == "on-primary":
            bg = INTERACTIVE_PRIMARY[theme]["default"]
            r = fmt_ratio(v, bg, AAA_LARGE, "AAA-large 4.5:1")
        elif k in ("default", "hover", "active"):
            r = fmt_ratio(v, canvas, NONTEXT, "non-text 4.5:1")
        else:
            r = None
        out.append({"name": f"interactive.primary.{k}", "hex": v, "ratio": r})

    for fam in ["success", "warning", "danger", "info"]:
        f = FEEDBACK[fam][theme]
        out.append({"name": f"feedback.{fam}.background", "hex": f["background"], "ratio": None})
        out.append({"name": f"feedback.{fam}.border", "hex": f["border"], "ratio": fmt_ratio(f["border"], canvas, NONTEXT, "non-text 4.5:1")})
        out.append({"name": f"feedback.{fam}.text", "hex": f["text"], "ratio": fmt_ratio(f["text"], f["background"], AAA_NORMAL, "AAA 7:1")})
        out.append({"name": f"feedback.{fam}.solid", "hex": f["solid"], "ratio": None})
        out.append({"name": f"feedback.{fam}.on-status", "hex": f["on-status"], "ratio": fmt_ratio(f["on-status"], f["solid"], AAA_LARGE, "AAA-large 4.5:1")})

    return out


def build_chart_swatches():
    cat = ALL_CHART_TOKENS["categorical"]
    seq = ALL_CHART_TOKENS["sequential"]
    div = ALL_CHART_TOKENS["diverging"]
    sup = ALL_CHART_TOKENS["supporting"]
    return {
        "categorical": [{"name": n, "hex": v["hex"]} for n, v in cat.items()],
        "sequential": [{"name": str(i), "hex": v["hex"]} for i, v in seq.items()],
        "diverging": [{"name": str(i), "hex": v["hex"]} for i, v in div.items()],
        "supporting": [{"name": n, "hexLight": v["light"], "hexDark": v["dark"]} for n, v in sup.items()],
    }


if __name__ == "__main__":
    payload = {
        "primitives": build_primitive_swatches(),
        "semanticLight": build_semantic_swatches("light"),
        "semanticDark": build_semantic_swatches("dark"),
        "charts": build_chart_swatches(),
    }
    with open("/tmp/figma_swatch_payload.json", "w") as f:
        json.dump(payload, f)
    print("wrote /tmp/figma_swatch_payload.json, size:", len(json.dumps(payload)))
