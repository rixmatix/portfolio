# Circana DS — Color Token System

A three-tier color token system (Primitive → Semantic → Component) plus a
dedicated Charts/data-visualization tier, purple-branded, WCAG 2.1 AAA
verified, with light and dark themes.

Figma file: [Circana-DS](https://www.figma.com/design/YBDljbFKuGOJsfrZMomVjR/Circana-DS?node-id=4001-2)
— the **Color** page has four stacked sections: Primitives, Semantic
(Light vs Dark), Charts, and a Usage Guide; the file's Variables panel has
Primitives / Semantic / Component / Charts collections.

## Architecture

```
tokens/primitives.json          raw OKLCH-derived ramps, unthemed
tokens/semantic.light.json      purpose-mapped tokens, light theme
tokens/semantic.dark.json       purpose-mapped tokens, dark theme
tokens/component.json           component-part tokens, theme-independent
tokens/charts.json              categorical / sequential / diverging / supporting

dist/css/*.css                  generated CSS custom properties
dist/tailwind/tailwind.tokens.js generated Tailwind `theme.extend.colors` fragment

scripts/                        the entire build pipeline (Python)
audit_report.md                 every contrast pairing, computed, pass/fail
usage-guide.md                  semantic tokens grouped by usage (Backgrounds/Text/Icons/
                                 Borders) + a full AAA combination matrix per background
```

Each tier **only references the tier below it** — this is the rule the
whole system is built to enforce:

- **Primitive**: raw hex values, generated from OKLCH (`scripts/build_primitives.py`, `scripts/build_charts.py`). Never themed, never referenced by product code directly. **Primitives are named by color, never by role** — `neutral`, `purple`, `green`, `amber`, `red`, `blue`, `teal`, `indigo`, `orange`, `base` (white/black). A primitive ramp has no idea it might mean "success" or "danger" — see Semantic below.
- **Semantic**: maps primitives to *purpose* (`surface.canvas`, `text.primary`, `feedback.danger.text`...), one value per theme (`scripts/build_semantic.py`). **This is the only layer where meaning is assigned** — e.g. `feedback.success.*` aliases the `green` primitive ramp, `feedback.danger.*` aliases `red`. This is the layer that changes between light and dark.
- **Component**: maps semantic tokens to *component parts* (`button.primary.background.default`...). Every component value is an alias into semantic — never a primitive, never a raw hex (`scripts/gen_component_json.py`).
- **Charts**: independent of the UI semantic tree. Categorical/sequential/diverging ramps plus supporting axis/gridline/label tokens, themed separately (`scripts/build_charts.py`).

`teal`, `indigo`, and `orange` currently have **no functional role assigned**
— they exist as base colors so a future semantic need (a fifth status, a
secondary accent) can alias an already-built, already-AAA-verified ramp
instead of inventing a new hue under deadline pressure.

Source of truth is the JSON in `tokens/` (W3C Design Tokens / DTCG format:
`$type`, `$value`, `$description`, alias values written as `{color.purple.600}`).
Everything else — CSS, Tailwind, Figma Variables — is *generated* from that
JSON by the scripts in `scripts/`. If you need to change a color, change the
Python source (`build_primitives.py`/`build_semantic.py`/etc.), not the
generated JSON/CSS/JS files by hand.

### Regenerating everything

```bash
cd scripts
python3 gen_primitives_json.py
python3 gen_charts_json.py
python3 gen_semantic_json.py
python3 gen_component_json.py
python3 gen_css.py
python3 gen_tailwind.py
python3 audit.py             # re-verify contrast + regenerate audit_report.md
python3 gen_usage_guide.py   # regenerate usage-guide.md + the Figma usage-guide payload
```

No npm/node dependency — the whole pipeline is pure Python 3, including the
OKLCH↔sRGB color math and WCAG contrast implementation in `scripts/color.py`
(verified against known reference conversions in its own `__main__` block).
To push token changes into Figma Variables, see `scripts/gen_figma_payload.py`
— it emits a JSON payload consumed by a generic Plugin API script (not
checked in as a `.js` file; see the Figma MCP call history, or regenerate
the payload and write a short walker script following the pattern in that
file: create a collection per tier, `createVariable`, alias via
`{type:'VARIABLE_ALIAS', id}`, `setVariableCodeSyntax('WEB', ...)`).

## Naming convention

```
<tier>.<category>.<role>[.<variant>][.<state>]
```

- **Primitive**: `color.<family>.<step>` — e.g. `color.purple.600`, `color.green.700`. Families (color-named, not role-named): `neutral`, `purple`, `green`, `amber`, `red`, `blue`, `teal`, `indigo`, `orange`, `base` (white/black). Steps: `25,50,100,200,300,400,500,600,700,800,900,950`.
- **Semantic**: `semantic.<category>.<role>` — e.g. `semantic.text.primary`, `semantic.feedback.danger.border`. Categories: `surface`, `text`, `border`, `focus-ring`, `interactive.primary`, `feedback.<success|warning|danger|info>` (which alias the `green`/`amber`/`red`/`blue` primitives respectively — see `usage-guide.md` for every token grouped by Background/Text/Icon/Border usage, with recommended-usage notes and a full AAA combination matrix per background).
- **Component**: `component.<component>.<part>.<state>` or `component.<component>.<variant>.<part>.<state>` — e.g. `component.button.primary.background.hover`, `component.badge.danger.solid.text`.
- **Charts**: `chart.<tier>.<key>` — e.g. `chart.categorical.1-purple`, `chart.sequential.4`, `chart.diverging.neg-2`, `chart.supporting.axis-line`.

CSS custom properties join the path with `-`: `--semantic-text-primary`,
`--component-button-primary-background-hover`. Figma variable names join
with `/` (Figma's native grouping separator) and carry a `codeSyntax.WEB`
value equal to the CSS var, so dev handoff always points at the real
variable name — never a hand-typed guess.

## Color science (brief)

- Ramps are generated in **OKLCH**, not HSL — HSL's uneven perceptual
  lightness (especially in blue/purple hues) is why hand-tuned HSL ramps
  routinely fail contrast at some steps and look banded at others.
- **Primary purple**: hue 297° in OKLCH. Chosen by rendering a hue sweep
  (260°→330°) and picking the zone that reads as unambiguous purple —
  260–280° reads blue/indigo, 310°+ drifts toward magenta/fuchsia; 295–300°
  is the stable "textbook purple" zone. Chroma peaks ~0.23 at the 500/600
  vivid step and tapers at both lightness extremes (sRGB gamut narrows
  there — this is physics, not a choice).
- **Neutral gray**: same hue (297°) at near-zero chroma (0.003–0.009) — a
  cool lean that harmonizes with the brand hue and reads more
  technical/enterprise than a warm gray would.
- Two "AAA anchor" steps are **numerically solved**, not eyeballed, per
  ramp: step `700` is binary-searched so its sRGB relative luminance stays
  under a threshold that guarantees ≥7:1 against every light surface in the
  system (canvas *and* raised, whichever is tighter); step `300` is solved
  the same way for ≥7:1 against every dark surface. See
  `scripts/build_primitives.py` `solve_L_for_luminance`.
- **Charts categorical palette**: *not* evenly-spaced hues. That first
  attempt put purple and blue only 6.4 apart under simulated deuteranopia —
  functionally indistinguishable. `scripts/optimize_categorical.py` instead
  runs farthest-point sampling over an OKLCH hue×lightness grid, scoring
  each candidate pair by the **minimum** Euclidean sRGB distance across
  {normal vision, protanopia, deuteranopia, tritanopia}. Final palette's
  worst-case pairwise distance: 48.56 (up from 6.4).

## Contrast targets & where they apply

| Context | Target | Notes |
|---|---|---|
| Body/UI text | 7:1 (AAA normal) | `text.primary/secondary/tertiary`, `feedback.*.text`, `text.link` |
| Large text (≥24px regular / ≥18.66px 14pt bold — headings, button labels) | 4.5:1 (AAA large) | `text.on-primary`, `feedback.*.on-status` |
| Non-text UI (borders, icons, focus rings) | 4.5:1 — **internal standard**, stricter than WCAG's own 3:1 AA-only tier | `border.default/strong/focus`, `focus-ring`, `interactive.primary.default` |
| Chart supporting tokens (axis/gridline/data-label) | 3:1 non-text / 4.5:1 text — **relaxed vs. the general UI targets above**, on purpose | Dense charts need lighter marks than general UI chrome; see `audit_report.md` intro for the explicit callout |
| Disabled/inactive text | **Exempt** | WCAG 2.1 carve-out: inactive UI components have no contrast requirement. Still computed and logged in the audit, never silently skipped. |
| Decorative dividers (`border.subtle`) | **Exempt** | Not required to convey a boundary; a real border token exists (`border.default`) for anything that is. |

Every non-exempt pairing is programmatically checked in `scripts/audit.py`
(78 checks, 0 failures as of the last run) — see `audit_report.md` for the
full table with computed ratios.

## Usage guide (tokens grouped by purpose)

`usage-guide.md` (and the matching "Usage Guide" section on the Figma Color
page) is an **additive** reference — it doesn't rename or restructure
anything in `tokens/`. It groups the same 43 semantic tokens by how they're
actually used:

- **Backgrounds** — every token valid as a fill (surfaces, interactive
  states, feedback backgrounds/solids)
- **Text** — every token valid as text color
- **Icons** — tokens icons reuse today (there's no dedicated icon tier yet;
  icons currently borrow `feedback.*.text` and a couple of others — flagged
  explicitly since the token names alone don't say "I'm also an icon color")
- **Borders**

...plus an **AAA combination matrix**: for every background, every
same-theme text/icon token that clears at least the AAA-large tier (4.5:1),
sorted by ratio, with a usage note — a direct answer to "I have this
background, what can I legally put on it, and at what ratio."

## Extending the system

**Adding a new functional color** (e.g. a fifth status beyond success/warning/danger/info):
1. Check whether an unassigned base primitive already fits (`teal`, `indigo`, `orange` currently have no role — see Architecture above). If one does, skip straight to step 3.
2. If none fit, add a new `FOO_HUE`/`FOO_CHROMA`/`FOO_L_GUESS` block to `scripts/build_primitives.py` and call `build_ramp2(...)`, add it to `ALL_RAMPS` under its **color name**, not its intended role. Run the script — check the printed diagnostics for monotonicity and that steps 700/300 land near the AAA anchor luminance targets (they're solved automatically, just confirm no unexpected gamut clipping at those two steps specifically), and visually sanity-check it reads as the intended color and stays distinct from its hue neighbors (render a swatch strip, see `build_primitives.py`'s hue-sweep approach in the conversation history).
3. In `scripts/build_semantic.py`, call `feedback_family("<primitive-color-name>")` and assign it to the new functional key in the `FEEDBACK` dict (this is the one place meaning gets attached to a hue); add the new checks to the `CHECKS` list (copy the existing success/warning/danger/info block).
4. Run `python3 build_semantic.py` — fix anything that FAILs before moving on.
5. Regenerate JSON/CSS/Tailwind (`gen_*.py` scripts), re-run `audit.py`, and regenerate `usage-guide.md` (`gen_usage_guide.py`) so the new status shows up in the categorized reference and combination matrix.
6. Extend `component.json`'s `alert`/`badge` sections (`gen_component_json.py`) with the new family, matching the existing pattern exactly.
7. Push to Figma using the same payload-and-walker approach as `gen_figma_payload.py` (if you consumed an existing unassigned primitive, no new Primitives-collection variables are needed — only new Semantic/Component ones).

**Adding a new component:**
1. Identify which existing semantic tokens the component's parts need (background/text/border/icon × states). Don't invent new colors — if nothing fits, that's a sign a semantic token is missing, not that the component needs a bespoke hex.
2. Add the component to `build_component_tree()` in `scripts/gen_component_json.py`, following the `<component>.<part>.<state>` pattern (or `<component>.<variant>.<part>.<state>` if it has skins like button does). Every `$value` must be `sem("...")` or a literal like `"transparent"` — never a raw hex.
3. Regenerate `component.json`, `dist/css/component.css`, `dist/tailwind/tailwind.tokens.js`, and push the new variables to Figma's Component collection (1 mode, aliasing Semantic).
4. No new contrast checks are needed *if* you only reused already-verified semantic pairings. If you pair a semantic token against a surface it wasn't checked against before (e.g. text on `surface.sunken` instead of `surface.canvas`), add that pairing to `build_semantic.py`'s `CHECKS` and re-run the audit before shipping.

## Known, deliberate trade-offs (read before "fixing")

- `interactive.primary.default` is **purple-600 in light mode but purple-400 in dark mode** — not a mirrored pair. Purple-500 only reaches 3.93:1 against the dark canvas (fails the 4.5:1 internal non-text standard for the control itself being visibly distinct); purple-400 clears it. This is why dark-mode brand fills often read lighter than their light-mode counterparts in AAA-constrained systems — it's physics, not inconsistency.
- `text.on-primary` is verified to the **4.5:1 AAA-large tier**, not full 7:1 normal-text AAA, because it's scoped to button labels/headings (explicitly "large text" in the brief's own definition). If you ever need small/normal-size text on a primary-filled surface, use `interactive.primary.active` as the background instead — it clears full 7:1 with white/black text (see `audit_report.md`).
- Chart supporting tokens (`axis-line`, `gridline`, `data-label-text`) intentionally use a **lower** contrast floor (3:1/4.5:1) than the general UI system (7:1/4.5:1-internal). This is called out explicitly in both `audit_report.md` and `charts.json`'s `$description` so it doesn't read as an inconsistency later.
- `border.subtle` and `text.disabled` are the only two EXEMPT categories in the whole system, and both have a one-line WCAG-grounded justification attached in the audit — not a silent skip.
- The primitive families were renamed from their original functional names (`success`→`green`, `warning`→`amber`, `danger`→`red`, `info`→`blue`) partway through building this system, once it became clear the primitive tier shouldn't know what its colors *mean*. The rename was done **in place** in Figma (same variable IDs, just new names/codeSyntax) specifically so every existing Semantic-tier alias kept resolving without needing to be rebuilt — if you're diffing an older export against this one and see primitive names change with identical hex values underneath, that's why.
