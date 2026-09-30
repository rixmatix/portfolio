"""Emits tokens/semantic.light.json and tokens/semantic.dark.json in DTCG
format, using $value alias references ("{color.purple.600}") back into
primitives.json rather than duplicating hex values."""
import json
from build_semantic import (
    SURFACE, TEXT, BORDER, FOCUS_RING, INTERACTIVE_PRIMARY, FEEDBACK, P,
)

# Build a reverse lookup: hex -> "{color.family.step}" alias, plus raw
# non-ramp values (white/black/rgba overlays) fall back to a literal $value.
HEX_TO_ALIAS = {}
for family, steps in P.items():
    for step, hex_val in steps.items():
        HEX_TO_ALIAS[hex_val] = f"{{color.{family}.{step}}}"
HEX_TO_ALIAS["#FFFFFF"] = "{color.base.white}"
HEX_TO_ALIAS["#000000"] = "{color.base.black}"


def val(hex_or_rgba):
    if hex_or_rgba.startswith("rgba"):
        return {"$type": "color", "$value": hex_or_rgba}
    alias = HEX_TO_ALIAS.get(hex_or_rgba)
    if alias is None:
        raise ValueError(f"No primitive alias found for {hex_or_rgba} -- semantic tokens must reference primitives, not introduce new raw colors")
    return {"$type": "color", "$value": alias}


def build_theme_json(theme):
    out = {"$description": f"Semantic tokens, {theme} theme. All values alias into primitives.json.", "semantic": {}}

    out["semantic"]["surface"] = {k: val(v) for k, v in SURFACE[theme].items()}
    out["semantic"]["text"] = {k: val(v) for k, v in TEXT[theme].items()}
    out["semantic"]["border"] = {k: val(v) for k, v in BORDER[theme].items()}
    out["semantic"]["focus-ring"] = val(FOCUS_RING[theme])

    out["semantic"]["interactive"] = {"primary": {k: val(v) for k, v in INTERACTIVE_PRIMARY[theme].items()}}

    out["semantic"]["feedback"] = {}
    for fam in ["success", "warning", "danger", "info"]:
        out["semantic"]["feedback"][fam] = {k: val(v) for k, v in FEEDBACK[fam][theme].items()}

    return out


if __name__ == "__main__":
    for theme in ["light", "dark"]:
        data = build_theme_json(theme)
        path = f"../tokens/semantic.{theme}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        print(f"wrote tokens/semantic.{theme}.json")
