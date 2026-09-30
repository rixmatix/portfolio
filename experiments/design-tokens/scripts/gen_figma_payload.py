"""
Builds a compact JSON payload describing every variable to create in Figma
(Primitives / Semantic / Component / Charts collections), reusing the exact
same verified token data as the JSON/CSS generators. A generic Plugin API
script (run via use_figma) walks this payload to create collections,
variables, modes, aliases, scopes, and codeSyntax -- no hand-transcription.

Target shapes:
  "primitive:<family>.<step>" -> alias to a Primitives-collection variable
  "literal:<hex-or-rgba>"     -> a direct value, not an alias
  "semantic:<path>"           -> alias to a Semantic-collection variable (Component payload only)
"""
import json
from build_primitives import ALL_RAMPS, RAMP_STEPS
from build_semantic import SURFACE, TEXT, BORDER, FOCUS_RING, INTERACTIVE_PRIMARY, FEEDBACK, P
from build_charts import ALL_CHART_TOKENS
from gen_component_json import build_component_tree

HEX_TO_PRIM = {}
for family, steps in P.items():
    for step, hex_val in steps.items():
        HEX_TO_PRIM[hex_val] = f"primitive:{family}.{step}"
HEX_TO_PRIM["#FFFFFF"] = "primitive:base.white"
HEX_TO_PRIM["#000000"] = "primitive:base.black"


def semantic_target(v):
    if isinstance(v, str) and v.startswith("rgba"):
        return f"literal:{v}"
    return HEX_TO_PRIM[v]


def build_semantic_theme(theme):
    out = {}
    for k, v in SURFACE[theme].items():
        out[f"surface.{k}"] = semantic_target(v)
    for k, v in TEXT[theme].items():
        out[f"text.{k}"] = semantic_target(v)
    for k, v in BORDER[theme].items():
        out[f"border.{k}"] = semantic_target(v)
    out["focus-ring"] = semantic_target(FOCUS_RING[theme])
    for k, v in INTERACTIVE_PRIMARY[theme].items():
        out[f"interactive.primary.{k}"] = semantic_target(v)
    for fam in ["success", "warning", "danger", "info"]:
        for k, v in FEEDBACK[fam][theme].items():
            out[f"feedback.{fam}.{k}"] = semantic_target(v)
    return out


def flatten_component_tree(node, path):
    if "$value" in node:
        val = node["$value"]
        if val == "transparent":
            yield (".".join(path), "literal:transparent")
        else:
            m = val.strip("{}")
            assert m.startswith("semantic."), f"unexpected component value {val}"
            yield (".".join(path), f"semantic:{m[len('semantic.'):]}")
        return
    for key, child in node.items():
        yield from flatten_component_tree(child, path + [key])


def build_payload():
    primitives = {}
    for family, ramp in ALL_RAMPS.items():
        primitives[family] = {str(step): ramp[step]["hex"] for step in RAMP_STEPS}
    primitives["base"] = {"white": "#FFFFFF", "black": "#000000"}

    semantic_light = build_semantic_theme("light")
    semantic_dark = build_semantic_theme("dark")

    comp_tree = build_component_tree()
    component = dict(flatten_component_tree(comp_tree, []))

    cat = ALL_CHART_TOKENS["categorical"]
    seq = ALL_CHART_TOKENS["sequential"]
    div = ALL_CHART_TOKENS["diverging"]
    sup = ALL_CHART_TOKENS["supporting"]

    def div_key(i):
        return "0" if i == 0 else (f"neg-{abs(i)}" if i < 0 else f"pos-{i}")

    charts_constant = {}
    for name, v in cat.items():
        charts_constant[f"categorical.{name.split('-',1)[1]}"] = f"literal:{v['hex']}"
    for i, v in seq.items():
        charts_constant[f"sequential.{i}"] = f"literal:{v['hex']}"
    for i, v in div.items():
        charts_constant[f"diverging.{div_key(i)}"] = f"literal:{v['hex']}"

    charts_light = dict(charts_constant)
    charts_dark = dict(charts_constant)
    for name, v in sup.items():
        charts_light[f"supporting.{name}"] = semantic_target(v["light"])
        charts_dark[f"supporting.{name}"] = semantic_target(v["dark"])

    return {
        "primitives": primitives,
        "semanticLight": semantic_light,
        "semanticDark": semantic_dark,
        "component": component,
        "chartsLight": charts_light,
        "chartsDark": charts_dark,
    }


if __name__ == "__main__":
    payload = build_payload()
    with open("/tmp/figma_payload.json", "w") as f:
        json.dump(payload, f)
    print("wrote /tmp/figma_payload.json")
    print("sizes:", {k: len(v) for k, v in payload.items()})
