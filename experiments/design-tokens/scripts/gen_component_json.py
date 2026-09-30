"""
Emits tokens/component.json in DTCG format.

Naming pattern: component.<component>.<part>.<variant?>.<state>
  - <component>: button, input, alert, badge, link, checkbox, radio, tabs
  - <part>: background, text, border, icon, placeholder (whichever apply)
  - <variant>: only present where a component has meaningfully different
    skins (button: primary/secondary/danger; alert/badge: success/warning/
    danger/info; badge additionally: subtle/solid)
  - <state>: default, hover, active, disabled, focus, error, checked --
    only the states that actually differ from "default" are written; a
    missing state means "same as default" and consumers should fall back.

Every value here is a $value alias into semantic.<theme>.json (e.g.
"{semantic.interactive.primary.default}") -- component tokens NEVER
reference primitives directly. This is the rule to extend by: adding a
new component means picking existing semantic roles and aliasing them,
not inventing new colors. See README "Extending the system".
"""
import json

def sem(path):
    return {"$type": "color", "$value": f"{{semantic.{path}}}"}

def build_component_tree():
    c = {}

    # -----------------------------------------------------------------
    # BUTTON
    # -----------------------------------------------------------------
    c["button"] = {
        "primary": {
            "background": {
                "default": sem("interactive.primary.default"),
                "hover": sem("interactive.primary.hover"),
                "active": sem("interactive.primary.active"),
                "disabled": sem("interactive.primary.disabled"),
            },
            "text": {
                "default": sem("interactive.primary.on-primary"),
                "disabled": sem("text.disabled"),
            },
            "border": {"default": {"$type": "color", "$value": "transparent"}},
        },
        "secondary": {
            "background": {
                "default": {"$type": "color", "$value": "transparent"},
                "hover": sem("interactive.primary.subtle"),
                "active": sem("interactive.primary.subtle"),
                "disabled": {"$type": "color", "$value": "transparent"},
            },
            "text": {
                "default": sem("interactive.primary.default"),
                "disabled": sem("text.disabled"),
            },
            "border": {
                "default": sem("interactive.primary.default"),
                "disabled": sem("border.subtle"),
            },
        },
        "danger": {
            "background": {
                "default": sem("feedback.danger.solid"),
                "hover": sem("feedback.danger.solid"),   # see README: no separate hover/active step defined for solid-fill danger; use opacity or a future danger-700 alias if a distinct hover is needed
                "active": sem("feedback.danger.solid"),
                "disabled": sem("interactive.primary.disabled"),
            },
            "text": {
                "default": sem("feedback.danger.on-status"),
                "disabled": sem("text.disabled"),
            },
            "border": {"default": {"$type": "color", "$value": "transparent"}},
        },
    }

    # -----------------------------------------------------------------
    # INPUT
    # -----------------------------------------------------------------
    c["input"] = {
        "background": {
            "default": sem("surface.raised"),
            "disabled": sem("surface.sunken"),
        },
        "border": {
            "default": sem("border.default"),
            "focus": sem("focus-ring"),
            "error": sem("feedback.danger.border"),
            "disabled": sem("border.subtle"),
        },
        "text": {
            "default": sem("text.primary"),
            "disabled": sem("text.disabled"),
        },
        "placeholder": {
            "default": sem("text.tertiary"),
        },
    }

    # -----------------------------------------------------------------
    # ALERT / BANNER
    # -----------------------------------------------------------------
    c["alert"] = {}
    for fam in ["success", "warning", "danger", "info"]:
        c["alert"][fam] = {
            "background": sem(f"feedback.{fam}.background"),
            "border": sem(f"feedback.{fam}.border"),
            "text": sem(f"feedback.{fam}.text"),
            "icon": sem(f"feedback.{fam}.text"),  # icon matches text color for the same family
        }

    # -----------------------------------------------------------------
    # BADGE (subtle = default pill; solid = filled pill)
    # -----------------------------------------------------------------
    c["badge"] = {}
    for fam in ["success", "warning", "danger", "info"]:
        c["badge"][fam] = {
            "subtle": {
                "background": sem(f"feedback.{fam}.background"),
                "text": sem(f"feedback.{fam}.text"),
            },
            "solid": {
                "background": sem(f"feedback.{fam}.solid"),
                "text": sem(f"feedback.{fam}.on-status"),
            },
        }

    # -----------------------------------------------------------------
    # LINK
    # -----------------------------------------------------------------
    c["link"] = {
        "text": {
            "default": sem("text.link"),
            "hover": sem("interactive.primary.active"),  # verified AAA normal 7:1, see audit
            "visited": sem("text.link"),
        }
    }

    # -----------------------------------------------------------------
    # CHECKBOX / RADIO (share the same token set)
    # -----------------------------------------------------------------
    def checkbox_like():
        return {
            "border": {
                "default": sem("border.default"),
                "checked": sem("interactive.primary.default"),
                "focus": sem("focus-ring"),
                "disabled": sem("border.subtle"),
            },
            "background": {
                "default": {"$type": "color", "$value": "transparent"},
                "checked": sem("interactive.primary.default"),
                "disabled": sem("surface.sunken"),
            },
            "icon": {  # checkmark / dot
                "checked": sem("interactive.primary.on-primary"),
            },
        }
    c["checkbox"] = checkbox_like()
    c["radio"] = checkbox_like()

    # -----------------------------------------------------------------
    # TABS
    # -----------------------------------------------------------------
    c["tabs"] = {
        "text": {
            "default": sem("text.secondary"),
            "hover": sem("text.primary"),
            "active": sem("interactive.primary.default"),
        },
        "border": {
            "default": sem("border.subtle"),   # tab-list baseline rule, decorative
            "active": sem("interactive.primary.default"),  # active-tab underline indicator
        },
    }

    return c


if __name__ == "__main__":
    data = {"$description": "Component tier. Every $value aliases a semantic token -- see this file's docstring for the naming pattern and extension rule.", "component": build_component_tree()}
    with open("../tokens/component.json", "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("wrote tokens/component.json")
