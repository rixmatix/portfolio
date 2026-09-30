"""Emits tokens/charts.json in DTCG format."""
import json
from build_charts import ALL_CHART_TOKENS

def build_json():
    cat = ALL_CHART_TOKENS["categorical"]
    seq = ALL_CHART_TOKENS["sequential"]
    div = ALL_CHART_TOKENS["diverging"]
    sup = ALL_CHART_TOKENS["supporting"]

    out = {"$description": "Charts/data-visualization tier. Independent from UI semantic tokens -- do not reuse chart.categorical.* for UI elements.", "chart": {}}

    out["chart"]["categorical"] = {
        "$description": "8 mutually distinguishable, colorblind-safe categorical colors. Found via farthest-point sampling maximizing worst-case Euclidean sRGB distance across {normal, protanopia, deuteranopia, tritanopia}. Minimum pairwise worst-case distance: 48.56. See scripts/optimize_categorical.py."
    }
    for name, v in cat.items():
        short = name.split("-", 1)[1]  # cat-1-purple -> 1-purple
        out["chart"]["categorical"][short] = {
            "$type": "color", "$value": v["hex"],
            "$extensions": {"com.circana-ds.oklch": {"L": v["L"], "C": v["C"], "H": v["H"]}},
        }

    out["chart"]["sequential"] = {
        "$description": "9-step magnitude/heatmap ramp derived from the primary purple hue. Index 0 = lowest magnitude, 8 = highest."
    }
    for i, v in seq.items():
        out["chart"]["sequential"][str(i)] = {
            "$type": "color", "$value": v["hex"],
            "$extensions": {"com.circana-ds.oklch": {"L": v["L"], "C": v["C"], "H": v["H"]}},
        }

    out["chart"]["diverging"] = {
        "$description": "9-step diverging ramp around a neutral midpoint (0). Negative = danger red (loss/below baseline), positive = teal (gain/above baseline). Deliberately not success-green on the positive side, to avoid diverging charts being misread as success/danger pairs."
    }
    for i, v in div.items():
        key = "0" if i == 0 else (f"neg-{abs(i)}" if i < 0 else f"pos-{i}")
        out["chart"]["diverging"][key] = {
            "$type": "color", "$value": v["hex"],
            "$extensions": {"com.circana-ds.oklch": {"L": v["L"], "C": v["C"], "H": v["H"]}},
        }

    out["chart"]["supporting"] = {"$description": "Axis/gridline/label tokens. Chart-specific contrast floor: 3:1 for non-text (axis-line, gridline), 4.5:1 for text (data-label-text) -- see audit report for the rationale on why this differs from the general UI 7:1/4.5:1-internal targets."}
    for name, v in sup.items():
        out["chart"]["supporting"][name] = {
            "light": {"$type": "color", "$value": v["light"]},
            "dark": {"$type": "color", "$value": v["dark"]},
        }

    return out

if __name__ == "__main__":
    data = build_json()
    with open("../tokens/charts.json", "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("wrote tokens/charts.json")
