"""
Generates dist/tailwind/tailwind.tokens.js -- a Tailwind config `extend`
fragment that maps color utilities to the SAME CSS custom properties
dist/css emits (var(--semantic-text-primary) etc), not duplicated hex
values. This means the Tailwind build and the raw-CSS build always agree,
and theme switching (toggling [data-theme]) works with Tailwind classes
for free since the underlying var already re-resolves per theme.

Usage: merge the exported object into your tailwind.config.js `theme.extend`.
Requires dist/css/tokens.css to be loaded on the page (Tailwind only
generates utility classes; it does not ship the custom-property values).
"""
import json
import re

ALIAS_RE = re.compile(r"^\{([^}]+)\}$")

def css_var_name(path_parts):
    return "--" + "-".join(path_parts)

def as_css_value(value):
    if isinstance(value, str):
        m = ALIAS_RE.match(value)
        if m:
            return f"var({css_var_name(m.group(1).split('.'))})"
    return value

def load(path):
    with open(path) as f:
        return json.load(f)

def nest_set(d, keys, value):
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value

def flatten_tokens(node, path):
    if not isinstance(node, dict):
        return
    if "$value" in node:
        yield (path, node["$value"])
        return
    for key, child in node.items():
        if key.startswith("$"):
            continue
        yield from flatten_tokens(child, path + [key])


def build_color_tree(data, root_key, css_prefix):
    """Builds a nested JS-object-shaped dict: primary-600 style flat keys
    under a Tailwind color group, using kebab-case matching the DTCG path."""
    tree = {}
    for path, value in flatten_tokens(data[root_key], [css_prefix] + [root_key] if False else [root_key]):
        # Tailwind color keys: join everything after the root as kebab-case,
        # e.g. semantic.text.primary -> colors.semantic['text-primary']
        group = path[0]
        rest = "-".join(path[1:]) if len(path) > 1 else group
        css_var_path = [css_prefix] + path
        nest_set(tree, [group, rest], f"var({css_var_name(css_var_path)})")
    return tree


def main():
    primitives = load("../tokens/primitives.json")
    semantic = load("../tokens/semantic.light.json")  # light/dark share the same var *names*; values differ per [data-theme]
    component = load("../tokens/component.json")
    charts = load("../tokens/charts.json")

    colors = {}

    # primitives: colors.purple['600'], colors.neutral['50'], colors.base.white
    for path, value in flatten_tokens(primitives["color"], ["color"]):
        # path like ["color","purple","600"] -> group "purple", key "600"
        group = path[1]
        key = "-".join(path[2:])
        nest_set(colors, [group, key], f"var({css_var_name(path)})")

    # semantic: colors.semantic['surface-canvas'], colors.semantic['text-primary'], etc.
    for path, value in flatten_tokens(semantic["semantic"], ["semantic"]):
        key = "-".join(path[1:])
        nest_set(colors, ["semantic", key], f"var({css_var_name(path)})")

    # component: colors.component['button-primary-background-default'] etc.
    for path, value in flatten_tokens(component["component"], ["component"]):
        key = "-".join(path[1:])
        nest_set(colors, ["component", key], f"var({css_var_name(path)})")

    # charts: colors.chart['categorical-1-purple'], colors.chart['sequential-0'], etc.
    # supporting tokens are theme-scoped via [data-theme] (one var per name, like semantic.*),
    # so they get ONE Tailwind key each, not light/dark-suffixed duplicates.
    chart_colors = {}
    for group_name, group_val in charts["chart"].items():
        if group_name.startswith("$"):
            continue
        if group_name == "supporting":
            for name, v in group_val.items():
                if name.startswith("$"):
                    continue
                chart_colors[f"supporting-{name}"] = f"var({css_var_name(['chart', 'supporting', name])})"
            continue
        for step, v in group_val.items():
            if step.startswith("$"):
                continue
            key = f"{group_name}-{step}" if group_name != "categorical" else step
            chart_colors[key] = f"var({css_var_name(['chart', group_name, step])})"
    colors["chart"] = chart_colors

    js = "// Generated from tokens/*.json. Do not hand-edit.\n"
    js += "// Merge into tailwind.config.js `theme.extend.colors`. Requires dist/css/tokens.css on the page.\n"
    js += "/** @type {import('tailwindcss').Config['theme']} */\n"
    js += "module.exports = {\n  extend: {\n    colors: "
    js += json.dumps(colors, indent=6).replace("\n", "\n    ")
    js += "\n  }\n};\n"

    with open("../dist/tailwind/tailwind.tokens.js", "w") as f:
        f.write(js)
    print("wrote dist/tailwind/tailwind.tokens.js")


if __name__ == "__main__":
    main()
