"""Emits tokens/primitives.json in W3C Design Tokens (DTCG) format."""
import json
from build_primitives import ALL_RAMPS, RAMP_STEPS

DESCRIPTIONS = {
    "neutral": "Cool-leaning gray ramp (hue 297, harmonized with primary purple). Used for surfaces, borders, and neutral text.",
    "purple": "Primary brand hue. H=297 in OKLCH -- calibrated to read as unambiguous purple, distinct from indigo/blue (<285) and fuchsia/magenta (>310).",
    "green": "Hue 149. Assigned the 'success' functional role in the semantic layer -- see semantic.light/dark.json feedback.success.*.",
    "amber": "Hue 75, gold-leaning rather than bright yellow -- pure yellow cannot reach usable dark-text contrast without looking muddy; gold holds saturation better across the AAA-required dark steps. Assigned the 'warning' functional role -- see semantic feedback.warning.*.",
    "red": "Hue 25. Assigned the 'danger' functional role -- see semantic feedback.danger.*.",
    "blue": "Hue 250. Kept >40 degrees from primary purple (297) to stay visually distinct in adjacent UI. Assigned the 'info' functional role -- see semantic feedback.info.*.",
    "teal": "Hue 195. Base color, no functional role assigned yet -- available for a future semantic need (e.g. a fifth status, a secondary brand accent) without inventing a new hue.",
    "indigo": "Hue 278, between Blue (250) and Purple (297). Base color, no functional role assigned yet.",
    "orange": "Hue 48, between Red (25) and Amber (75). Base color, no functional role assigned yet.",
}

STEP_DESC = {
    700: "AAA anchor: solved so relative luminance <=0.095 (>=7.24:1 vs #FFFFFF). Use for AAA body text/icons on light surfaces.",
    300: "AAA anchor: solved so relative luminance >=0.389 (>=7.3:1 vs neutral-950 dark canvas). Use for AAA body text/icons on dark surfaces.",
}

def build_json():
    out = {"$description": "Primitive color ramps. Raw, unthemed, meaning-agnostic -- families are named by color (green/amber/red/blue/teal/indigo/orange/purple/neutral), never by functional role. Functional meaning (success/warning/danger/info) is assigned only in semantic.*.json. Do not reference primitives directly from components -- go through semantic tokens.", "color": {}}
    out["color"]["base"] = {
        "$description": "Absolute white/black. Used sparingly (on-status/on-primary text, pure overlays) where a themed ramp step isn't appropriate.",
        "white": {"$type": "color", "$value": "#FFFFFF"},
        "black": {"$type": "color", "$value": "#000000"},
    }
    for family, ramp in ALL_RAMPS.items():
        out["color"][family] = {"$description": DESCRIPTIONS[family]}
        for step in RAMP_STEPS:
            entry = ramp[step]
            token = {
                "$type": "color",
                "$value": entry["hex"],
                "$extensions": {
                    "com.circana-ds.oklch": {"L": entry["L"], "C": entry["C"], "H": entry["H"]},
                    "com.circana-ds.relativeLuminance": entry["relLum"],
                    "com.circana-ds.gamutClipped": entry["clipped"],
                },
            }
            if step in STEP_DESC:
                token["$description"] = STEP_DESC[step]
            out["color"][family][str(step)] = token
    return out

if __name__ == "__main__":
    data = build_json()
    with open("../tokens/primitives.json", "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("wrote tokens/primitives.json")
