"""
Builds usage-guide.md: semantic tokens grouped by how they're actually used
(Backgrounds / Text / Icons / Borders), plus an AAA combination matrix --
for every background, which text/icon tokens pass AAA on it, with ratio
and a recommended-usage note. Additive only: does not rename or restructure
any existing token path.
"""
import json
from build_primitives import ALL_RAMPS
from build_semantic import SURFACE, TEXT, BORDER, FOCUS_RING, INTERACTIVE_PRIMARY, FEEDBACK
from color import contrast_ratio

AAA_NORMAL = 7.0
AAA_LARGE = 4.5


def is_color(hex_or_rgba):
    return not (isinstance(hex_or_rgba, str) and hex_or_rgba.startswith("rgba"))


# ---------------------------------------------------------------------------
# Catalogue: every token, tagged with its usage bucket + a recommended-usage note.
# ---------------------------------------------------------------------------
BACKGROUND_NOTES = {
    "surface.canvas": "Default app/page background -- the base surface nearly everything else sits on.",
    "surface.raised": "Cards, modals, popovers, dropdowns -- anything that should read as lifted above canvas.",
    "surface.sunken": "Inset wells, code blocks, resting input fields -- content that reads as pressed in.",
    "surface.overlay": "Modal/drawer scrim between canvas content and a raised surface. Not a fill for text-bearing content -- no contrast pairing applies.",
    "surface.inverse": "Opposite-theme surface embedded in the current theme (tooltips, toasts, inverted callouts).",
    "interactive.primary.default": "Primary button and other high-emphasis filled controls, default state.",
    "interactive.primary.hover": "Primary button hover state.",
    "interactive.primary.active": "Primary button active/pressed state.",
    "interactive.primary.disabled": "Disabled primary button fill. WCAG-exempt -- inactive controls have no contrast requirement.",
    "interactive.primary.subtle": "Tinted background for secondary-button hover/active, selected rows, subtle brand emphasis.",
    "feedback.success.background": "Subtle success alert/banner background.",
    "feedback.warning.background": "Subtle warning alert/banner background.",
    "feedback.danger.background": "Subtle danger alert/banner background.",
    "feedback.info.background": "Subtle info alert/banner background.",
    "feedback.success.solid": "Solid-filled success badge background.",
    "feedback.warning.solid": "Solid-filled warning badge background.",
    "feedback.danger.solid": "Solid-filled danger badge / danger-button background.",
    "feedback.info.solid": "Solid-filled info badge background.",
}

TEXT_NOTES = {
    "text.primary": "Default body copy and headings.",
    "text.secondary": "Supporting copy one level down from primary -- still full AAA.",
    "text.tertiary": "Captions, metadata -- least-emphasized tier that's still full AAA.",
    "text.disabled": "Disabled control labels. WCAG-exempt.",
    "text.inverse": "Text on surface.inverse.",
    "text.link": "Inline links and clickable text.",
    "text.on-primary": "Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead.",
    "feedback.success.text": "Success alert body copy / status message, on feedback.success.background.",
    "feedback.warning.text": "Warning alert body copy / status message, on feedback.warning.background.",
    "feedback.danger.text": "Danger alert body copy / status message, on feedback.danger.background.",
    "feedback.info.text": "Info alert body copy / status message, on feedback.info.background.",
    "feedback.success.on-status": "Text on a solid-filled success badge/button.",
    "feedback.warning.on-status": "Text on a solid-filled warning badge/button.",
    "feedback.danger.on-status": "Text on a solid-filled danger badge/button.",
    "feedback.info.on-status": "Text on a solid-filled info badge/button.",
}

# Icons have no dedicated semantic tier today -- they reuse text-tier tokens.
# Listed explicitly here because the token itself doesn't say "I'm also an icon color."
ICON_NOTES = {
    "feedback.success.text": "Reused as the alert/badge icon color for success (see component.alert.success.icon).",
    "feedback.warning.text": "Reused as the alert/badge icon color for warning.",
    "feedback.danger.text": "Reused as the alert/badge icon color for danger.",
    "feedback.info.text": "Reused as the alert/badge icon color for info.",
    "interactive.primary.on-primary": "Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked).",
    "text.tertiary": "Reasonable default for neutral/decorative icons (chevrons, overflow menus) that aren't carrying status meaning.",
}

BORDER_NOTES = {
    "border.default": "Default input/card/divider borders that need to be reliably perceivable.",
    "border.subtle": "Decorative dividers -- NOT required to convey a boundary. Exempt from the non-text standard on purpose; a real border token (border.default) exists for anything load-bearing.",
    "border.strong": "Emphasized borders -- active/selected card outlines, table header rules.",
    "border.focus": "Keyboard focus indicator on form controls.",
    "focus-ring": "Standalone focus ring (e.g. around a whole card or custom control), distinct from border.focus for cases needing a visibly separate ring rather than a border-color swap.",
    "feedback.success.border": "Success alert/banner border.",
    "feedback.warning.border": "Warning alert/banner border.",
    "feedback.danger.border": "Danger alert/banner border.",
    "feedback.info.border": "Info alert/banner border.",
}


def collect_tokens(theme):
    """Returns {path: hex} for every semantic token in a theme."""
    out = {}
    for k, v in SURFACE[theme].items():
        out[f"surface.{k}"] = v
    for k, v in TEXT[theme].items():
        out[f"text.{k}"] = v
    for k, v in BORDER[theme].items():
        out[f"border.{k}"] = v
    out["focus-ring"] = FOCUS_RING[theme]
    for k, v in INTERACTIVE_PRIMARY[theme].items():
        out[f"interactive.primary.{k}"] = v
    for fam in ["success", "warning", "danger", "info"]:
        for k, v in FEEDBACK[fam][theme].items():
            out[f"feedback.{fam}.{k}"] = v
    return out


def build_matrix(theme):
    tokens = collect_tokens(theme)
    bg_paths = [p for p in BACKGROUND_NOTES if p in tokens]
    fg_candidates = {**{p: v for p, v in tokens.items() if p in TEXT_NOTES},
                      **{p: v for p, v in tokens.items() if p in ICON_NOTES}}

    matrix = {}
    for bg_path in bg_paths:
        bg_hex = tokens[bg_path]
        if not is_color(bg_hex):
            matrix[bg_path] = []
            continue
        combos = []
        seen_fg = set()
        for fg_path, fg_hex in fg_candidates.items():
            if fg_path in seen_fg or not is_color(fg_hex):
                continue
            seen_fg.add(fg_path)
            ratio = contrast_ratio(fg_hex, bg_hex)
            if ratio >= AAA_LARGE:
                tier = "AAA normal (7:1+)" if ratio >= AAA_NORMAL else "AAA large only (4.5-6.99:1)"
                combos.append({"fg": fg_path, "fgHex": fg_hex, "ratio": round(ratio, 2), "tier": tier})
        combos.sort(key=lambda c: -c["ratio"])
        matrix[bg_path] = combos
    return matrix


def render_markdown():
    lines = ["# Usage Guide -- Semantic Tokens by Purpose\n"]
    lines.append("Additive reference on top of the existing token paths (nothing renamed, nothing "
                  "restructured) -- organizes the same 43 semantic tokens by how they're actually used, "
                  "and shows every AAA-passing foreground/background combination with its computed ratio "
                  "so you don't have to cross-reference the audit table by hand.\n")

    def section(title, notes_dict, theme_getter):
        out = [f"## {title}\n", "| Token | Light | Dark | Recommended usage |", "|---|---|---|---|"]
        for path, note in notes_dict.items():
            light_hex = theme_getter("light").get(path, "--")
            dark_hex = theme_getter("dark").get(path, "--")
            out.append(f"| `semantic.{path}` | `{light_hex}` | `{dark_hex}` | {note} |")
        return "\n".join(out) + "\n"

    light_tokens = collect_tokens("light")
    dark_tokens = collect_tokens("dark")
    getter = lambda theme: light_tokens if theme == "light" else dark_tokens

    lines.append(section("Backgrounds", BACKGROUND_NOTES, getter))
    lines.append(section("Text", TEXT_NOTES, getter))
    lines.append(section("Icons", ICON_NOTES, getter))
    lines.append(section("Borders", BORDER_NOTES, getter))

    lines.append("## AAA Combination Matrix\n")
    lines.append("For every background token, every text/icon token from the SAME theme that clears at "
                  "least the AAA-large tier (4.5:1), sorted by ratio. Use this as a lookup: \"I have this "
                  "background, what can I put on it?\" Backgrounds not listed (overlay) have no fixed "
                  "foreground pairing -- content sits on the surface revealed underneath, not on the scrim itself.\n")

    for theme in ["light", "dark"]:
        lines.append(f"### {theme.capitalize()} theme\n")
        matrix = build_matrix(theme)
        for bg_path, combos in matrix.items():
            bg_hex = collect_tokens(theme)[bg_path]
            lines.append(f"**`semantic.{bg_path}`** (`{bg_hex}`) -- {BACKGROUND_NOTES[bg_path]}\n")
            if not combos:
                lines.append("_No fixed foreground pairing (see note above)._\n")
                continue
            lines.append("| Foreground | Ratio | Tier | Usage |")
            lines.append("|---|---|---|---|")
            for c in combos:
                note = TEXT_NOTES.get(c["fg"]) or ICON_NOTES.get(c["fg"]) or ""
                lines.append(f"| `semantic.{c['fg']}` (`{c['fgHex']}`) | {c['ratio']}:1 | {c['tier']} | {note} |")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    md = render_markdown()
    with open("../usage-guide.md", "w") as f:
        f.write(md)
    print(f"wrote usage-guide.md ({len(md)} chars)")

    payload = {
        "backgroundNotes": BACKGROUND_NOTES, "textNotes": TEXT_NOTES,
        "iconNotes": ICON_NOTES, "borderNotes": BORDER_NOTES,
        "tokensLight": collect_tokens("light"), "tokensDark": collect_tokens("dark"),
        "matrixLight": build_matrix("light"), "matrixDark": build_matrix("dark"),
    }
    with open("/tmp/figma_usage_payload.json", "w") as f:
        json.dump(payload, f)
    print(f"wrote /tmp/figma_usage_payload.json ({len(json.dumps(payload))} chars)")
