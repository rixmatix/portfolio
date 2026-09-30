"""
Generates dist/css/*.css custom properties from the DTCG token source JSON.

Convention: token path `a.b.c` -> CSS var `--a-b-c`. DTCG alias values like
"{color.purple.600}" resolve to `var(--color-purple-600)`. Non-alias literal
values (hex, "transparent", rgba(...)) pass through unchanged.
"""
import json
import re

ALIAS_RE = re.compile(r"^\{([^}]+)\}$")

def css_var_name(path_parts):
    return "--" + "-".join(path_parts)

def resolve_value(value):
    m = ALIAS_RE.match(value) if isinstance(value, str) else None
    if m:
        alias_path = m.group(1).split(".")
        return f"var({css_var_name(alias_path)})"
    return value

def flatten_tokens(node, path):
    """Yields (path_parts, value) for every $value leaf in a DTCG tree."""
    if not isinstance(node, dict):
        return
    if "$value" in node:
        yield (path, node["$value"])
        return
    for key, child in node.items():
        if key.startswith("$"):
            continue
        yield from flatten_tokens(child, path + [key])


def render_css_block(selector, declarations):
    lines = [f"{selector} {{"]
    for name, value in declarations:
        lines.append(f"  {name}: {resolve_value(value)};")
    lines.append("}")
    return "\n".join(lines)


def load(path):
    with open(path) as f:
        return json.load(f)


def gen_primitives_css():
    data = load("../tokens/primitives.json")
    decls = []
    for path, value in flatten_tokens(data["color"], ["color"]):
        decls.append((css_var_name(path), value))
    css = "/* Generated from tokens/primitives.json. Do not hand-edit. */\n\n"
    css += render_css_block(":root", decls) + "\n"
    with open("../dist/css/primitives.css", "w") as f:
        f.write(css)
    print(f"wrote dist/css/primitives.css ({len(decls)} vars)")


def gen_charts_css():
    data = load("../tokens/charts.json")
    constant_decls = []
    light_decls = []
    dark_decls = []
    for group_name, group_val in data["chart"].items():
        if group_name.startswith("$"):
            continue
        if group_name == "supporting":
            # theme-dependent: follow the same [data-theme] cascade as semantic.css,
            # one var per token name (not light/dark-suffixed duplicates).
            for name, v in group_val.items():
                if name.startswith("$"):
                    continue
                var_name = css_var_name(["chart", "supporting", name])
                light_decls.append((var_name, v["light"]["$value"]))
                dark_decls.append((var_name, v["dark"]["$value"]))
            continue
        for path, value in flatten_tokens(group_val, ["chart", group_name]):
            constant_decls.append((css_var_name(path), value))

    css = "/* Generated from tokens/charts.json. Do not hand-edit. */\n"
    css += "/* categorical/sequential/diverging are theme-independent; supporting tokens follow [data-theme] like semantic.css. */\n\n"
    css += render_css_block(":root", constant_decls) + "\n\n"
    css += render_css_block(":root, [data-theme=\"light\"]", light_decls) + "\n\n"
    css += render_css_block("[data-theme=\"dark\"]", dark_decls) + "\n"
    with open("../dist/css/charts.css", "w") as f:
        f.write(css)
    print(f"wrote dist/css/charts.css ({len(constant_decls)} constant + {len(light_decls)} theme-scoped vars)")


def gen_semantic_css():
    light = load("../tokens/semantic.light.json")
    dark = load("../tokens/semantic.dark.json")

    light_decls = [(css_var_name(p), v) for p, v in flatten_tokens(light["semantic"], ["semantic"])]
    dark_decls = [(css_var_name(p), v) for p, v in flatten_tokens(dark["semantic"], ["semantic"])]

    css = "/* Generated from tokens/semantic.light.json + semantic.dark.json. Do not hand-edit. */\n"
    css += "/* Theme switch: set data-theme=\"light\"|\"dark\" on <html> (or any ancestor). Light is the default (no attribute needed). */\n\n"
    css += render_css_block(":root, [data-theme=\"light\"]", light_decls) + "\n\n"
    css += render_css_block("[data-theme=\"dark\"]", dark_decls) + "\n"
    with open("../dist/css/semantic.css", "w") as f:
        f.write(css)
    print(f"wrote dist/css/semantic.css ({len(light_decls)} light + {len(dark_decls)} dark vars)")


def gen_component_css():
    data = load("../tokens/component.json")
    decls = []
    for path, value in flatten_tokens(data["component"], ["component"]):
        decls.append((css_var_name(path), value))
    css = "/* Generated from tokens/component.json. Do not hand-edit. */\n"
    css += "/* Component vars alias semantic vars, which are theme-scoped -- component vars automatically follow whatever [data-theme] is active. */\n\n"
    css += render_css_block(":root", decls) + "\n"
    with open("../dist/css/component.css", "w") as f:
        f.write(css)
    print(f"wrote dist/css/component.css ({len(decls)} vars)")


def gen_index_css():
    css = (
        "/* Import order matters: primitives -> semantic (theme-scoped) -> component -> charts. */\n"
        "@import \"./primitives.css\";\n"
        "@import \"./semantic.css\";\n"
        "@import \"./component.css\";\n"
        "@import \"./charts.css\";\n"
    )
    with open("../dist/css/tokens.css", "w") as f:
        f.write(css)
    print("wrote dist/css/tokens.css (index)")


if __name__ == "__main__":
    gen_primitives_css()
    gen_charts_css()
    gen_semantic_css()
    gen_component_css()
    gen_index_css()
