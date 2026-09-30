# Usage Guide -- Semantic Tokens by Purpose

Additive reference on top of the existing token paths (nothing renamed, nothing restructured) -- organizes the same 43 semantic tokens by how they're actually used, and shows every AAA-passing foreground/background combination with its computed ratio so you don't have to cross-reference the audit table by hand.

## Backgrounds

| Token | Light | Dark | Recommended usage |
|---|---|---|---|
| `semantic.surface.canvas` | `#FAFAFC` | `#1A191C` | Default app/page background -- the base surface nearly everything else sits on. |
| `semantic.surface.raised` | `#FFFFFF` | `#222124` | Cards, modals, popovers, dropdowns -- anything that should read as lifted above canvas. |
| `semantic.surface.sunken` | `#F2F1F4` | `#000000` | Inset wells, code blocks, resting input fields -- content that reads as pressed in. |
| `semantic.surface.overlay` | `rgba(26, 25, 28, 0.48)` | `rgba(0, 0, 0, 0.64)` | Modal/drawer scrim between canvas content and a raised surface. Not a fill for text-bearing content -- no contrast pairing applies. |
| `semantic.surface.inverse` | `#1A191C` | `#FAFAFC` | Opposite-theme surface embedded in the current theme (tooltips, toasts, inverted callouts). |
| `semantic.interactive.primary.default` | `#7C36D9` | `#A97DFE` | Primary button and other high-emphasis filled controls, default state. |
| `semantic.interactive.primary.hover` | `#672AB7` | `#BEA3FF` | Primary button hover state. |
| `semantic.interactive.primary.active` | `#461184` | `#D3C3FF` | Primary button active/pressed state. |
| `semantic.interactive.primary.disabled` | `#DCDCDF` | `#38373C` | Disabled primary button fill. WCAG-exempt -- inactive controls have no contrast requirement. |
| `semantic.interactive.primary.subtle` | `#E9E1FF` | `#1C023B` | Tinted background for secondary-button hover/active, selected rows, subtle brand emphasis. |
| `semantic.feedback.success.background` | `#E8F9EA` | `#001A05` | Subtle success alert/banner background. |
| `semantic.feedback.warning.background` | `#FFF2E2` | `#211300` | Subtle warning alert/banner background. |
| `semantic.feedback.danger.background` | `#FFEEED` | `#2E0002` | Subtle danger alert/banner background. |
| `semantic.feedback.info.background` | `#EBF5FF` | `#00152D` | Subtle info alert/banner background. |
| `semantic.feedback.success.solid` | `#007D34` | `#007D34` | Solid-filled success badge background. |
| `semantic.feedback.warning.solid` | `#976500` | `#976500` | Solid-filled warning badge background. |
| `semantic.feedback.danger.solid` | `#BC001D` | `#BC001D` | Solid-filled danger badge / danger-button background. |
| `semantic.feedback.info.solid` | `#006AB7` | `#006AB7` | Solid-filled info badge background. |

## Text

| Token | Light | Dark | Recommended usage |
|---|---|---|---|
| `semantic.text.primary` | `#222124` | `#FAFAFC` | Default body copy and headings. |
| `semantic.text.secondary` | `#38373C` | `#F2F1F4` | Supporting copy one level down from primary -- still full AAA. |
| `semantic.text.tertiary` | `#514F55` | `#B2B1B5` | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.text.disabled` | `#A5A4A8` | `#69686E` | Disabled control labels. WCAG-exempt. |
| `semantic.text.inverse` | `#B2B1B5` | `#514F55` | Text on surface.inverse. |
| `semantic.text.link` | `#672AB7` | `#BEA3FF` | Inline links and clickable text. |
| `semantic.text.on-primary` | `#FFFFFF` | `#000000` | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.text` | `#005D25` | `#6DC47F` | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` | `#6E4800` | `#EAA42B` | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.feedback.danger.text` | `#A3061A` | `#FF948C` | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.feedback.info.text` | `#00518F` | `#6FB7FF` | Info alert body copy / status message, on feedback.info.background. |
| `semantic.feedback.success.on-status` | `#FFFFFF` | `#FFFFFF` | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` | `#FFFFFF` | `#FFFFFF` | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` | `#FFFFFF` | `#FFFFFF` | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` | `#FFFFFF` | `#FFFFFF` | Text on a solid-filled info badge/button. |

## Icons

| Token | Light | Dark | Recommended usage |
|---|---|---|---|
| `semantic.feedback.success.text` | `#005D25` | `#6DC47F` | Reused as the alert/badge icon color for success (see component.alert.success.icon). |
| `semantic.feedback.warning.text` | `#6E4800` | `#EAA42B` | Reused as the alert/badge icon color for warning. |
| `semantic.feedback.danger.text` | `#A3061A` | `#FF948C` | Reused as the alert/badge icon color for danger. |
| `semantic.feedback.info.text` | `#00518F` | `#6FB7FF` | Reused as the alert/badge icon color for info. |
| `semantic.interactive.primary.on-primary` | `#FFFFFF` | `#000000` | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |
| `semantic.text.tertiary` | `#514F55` | `#B2B1B5` | Reasonable default for neutral/decorative icons (chevrons, overflow menus) that aren't carrying status meaning. |

## Borders

| Token | Light | Dark | Recommended usage |
|---|---|---|---|
| `semantic.border.default` | `#69686E` | `#86858A` | Default input/card/divider borders that need to be reliably perceivable. |
| `semantic.border.subtle` | `#DCDCDF` | `#38373C` | Decorative dividers -- NOT required to convey a boundary. Exempt from the non-text standard on purpose; a real border token (border.default) exists for anything load-bearing. |
| `semantic.border.strong` | `#514F55` | `#A5A4A8` | Emphasized borders -- active/selected card outlines, table header rules. |
| `semantic.border.focus` | `#7C36D9` | `#A97DFE` | Keyboard focus indicator on form controls. |
| `semantic.focus-ring` | `#7C36D9` | `#A97DFE` | Standalone focus ring (e.g. around a whole card or custom control), distinct from border.focus for cases needing a visibly separate ring rather than a border-color swap. |
| `semantic.feedback.success.border` | `#007D34` | `#46B362` | Success alert/banner border. |
| `semantic.feedback.warning.border` | `#976500` | `#D99300` | Warning alert/banner border. |
| `semantic.feedback.danger.border` | `#BC001D` | `#F45A56` | Danger alert/banner border. |
| `semantic.feedback.info.border` | `#006AB7` | `#389EFB` | Info alert/banner border. |

## AAA Combination Matrix

For every background token, every text/icon token from the SAME theme that clears at least the AAA-large tier (4.5:1), sorted by ratio. Use this as a lookup: "I have this background, what can I put on it?" Backgrounds not listed (overlay) have no fixed foreground pairing -- content sits on the surface revealed underneath, not on the scrim itself.

### Light theme

**`semantic.surface.canvas`** (`#FAFAFC`) -- Default app/page background -- the base surface nearly everything else sits on.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 15.37:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 11.32:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 7.83:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.feedback.warning.text` (`#6E4800`) | 7.78:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.text.link` (`#672AB7`) | 7.77:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#005D25`) | 7.77:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#514F55`) | 7.75:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.danger.text` (`#A3061A`) | 7.75:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |

**`semantic.surface.raised`** (`#FFFFFF`) -- Cards, modals, popovers, dropdowns -- anything that should read as lifted above canvas.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 16.02:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 11.8:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 8.16:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.feedback.warning.text` (`#6E4800`) | 8.11:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.text.link` (`#672AB7`) | 8.1:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#005D25`) | 8.1:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#514F55`) | 8.08:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.danger.text` (`#A3061A`) | 8.08:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |

**`semantic.surface.sunken`** (`#F2F1F4`) -- Inset wells, code blocks, resting input fields -- content that reads as pressed in.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 14.24:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 10.49:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 7.25:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.feedback.warning.text` (`#6E4800`) | 7.21:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.text.link` (`#672AB7`) | 7.2:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#005D25`) | 7.2:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#514F55`) | 7.18:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.danger.text` (`#A3061A`) | 7.18:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |

**`semantic.surface.overlay`** (`rgba(26, 25, 28, 0.48)`) -- Modal/drawer scrim between canvas content and a raised surface. Not a fill for text-bearing content -- no contrast pairing applies.

_No fixed foreground pairing (see note above)._

**`semantic.surface.inverse`** (`#1A191C`) -- Opposite-theme surface embedded in the current theme (tooltips, toasts, inverted callouts).

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |
| `semantic.text.inverse` (`#B2B1B5`) | 8.21:1 | AAA normal (7:1+) | Text on surface.inverse. |
| `semantic.text.disabled` (`#A5A4A8`) | 7.06:1 | AAA normal (7:1+) | Disabled control labels. WCAG-exempt. |

**`semantic.interactive.primary.default`** (`#7C36D9`) -- Primary button and other high-emphasis filled controls, default state.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 6.2:1 | AAA large only (4.5-6.99:1) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 6.2:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 6.2:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 6.2:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 6.2:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 6.2:1 | AAA large only (4.5-6.99:1) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.interactive.primary.hover`** (`#672AB7`) -- Primary button hover state.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 8.1:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 8.1:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 8.1:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 8.1:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 8.1:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 8.1:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.interactive.primary.active`** (`#461184`) -- Primary button active/pressed state.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 12.55:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 12.55:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 12.55:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 12.55:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 12.55:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 12.55:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |
| `semantic.text.inverse` (`#B2B1B5`) | 5.88:1 | AAA large only (4.5-6.99:1) | Text on surface.inverse. |
| `semantic.text.disabled` (`#A5A4A8`) | 5.06:1 | AAA large only (4.5-6.99:1) | Disabled control labels. WCAG-exempt. |

**`semantic.interactive.primary.disabled`** (`#DCDCDF`) -- Disabled primary button fill. WCAG-exempt -- inactive controls have no contrast requirement.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 11.71:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 8.62:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 5.96:1 | AAA large only (4.5-6.99:1) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.feedback.warning.text` (`#6E4800`) | 5.93:1 | AAA large only (4.5-6.99:1) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.text.link` (`#672AB7`) | 5.92:1 | AAA large only (4.5-6.99:1) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#005D25`) | 5.92:1 | AAA large only (4.5-6.99:1) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.danger.text` (`#A3061A`) | 5.91:1 | AAA large only (4.5-6.99:1) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#514F55`) | 5.9:1 | AAA large only (4.5-6.99:1) | Captions, metadata -- least-emphasized tier that's still full AAA. |

**`semantic.interactive.primary.subtle`** (`#E9E1FF`) -- Tinted background for secondary-button hover/active, selected rows, subtle brand emphasis.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 12.72:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 9.37:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 6.48:1 | AAA large only (4.5-6.99:1) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#672AB7`) | 6.44:1 | AAA large only (4.5-6.99:1) | Inline links and clickable text. |
| `semantic.feedback.warning.text` (`#6E4800`) | 6.44:1 | AAA large only (4.5-6.99:1) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.feedback.success.text` (`#005D25`) | 6.43:1 | AAA large only (4.5-6.99:1) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#514F55`) | 6.42:1 | AAA large only (4.5-6.99:1) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.danger.text` (`#A3061A`) | 6.42:1 | AAA large only (4.5-6.99:1) | Danger alert body copy / status message, on feedback.danger.background. |

**`semantic.feedback.success.background`** (`#E8F9EA`) -- Subtle success alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 14.62:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 10.77:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 7.45:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#672AB7`) | 7.4:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.warning.text` (`#6E4800`) | 7.4:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.feedback.success.text` (`#005D25`) | 7.39:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.danger.text` (`#A3061A`) | 7.38:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#514F55`) | 7.37:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |

**`semantic.feedback.warning.background`** (`#FFF2E2`) -- Subtle warning alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 14.53:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 10.7:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 7.4:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.feedback.warning.text` (`#6E4800`) | 7.36:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.text.link` (`#672AB7`) | 7.35:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#005D25`) | 7.35:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#514F55`) | 7.33:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.danger.text` (`#A3061A`) | 7.33:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |

**`semantic.feedback.danger.background`** (`#FFEEED`) -- Subtle danger alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 14.27:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 10.51:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 7.27:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#672AB7`) | 7.22:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#005D25`) | 7.22:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` (`#6E4800`) | 7.22:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.text.tertiary` (`#514F55`) | 7.2:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.danger.text` (`#A3061A`) | 7.2:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |

**`semantic.feedback.info.background`** (`#EBF5FF`) -- Subtle info alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.primary` (`#222124`) | 14.52:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#38373C`) | 10.7:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#00518F`) | 7.4:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#672AB7`) | 7.35:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.warning.text` (`#6E4800`) | 7.35:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |
| `semantic.feedback.success.text` (`#005D25`) | 7.34:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.danger.text` (`#A3061A`) | 7.33:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#514F55`) | 7.32:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |

**`semantic.feedback.success.solid`** (`#007D34`) -- Solid-filled success badge background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.feedback.warning.solid`** (`#976500`) -- Solid-filled warning badge background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.feedback.danger.solid`** (`#BC001D`) -- Solid-filled danger badge / danger-button background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.feedback.info.solid`** (`#006AB7`) -- Solid-filled info badge background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.interactive.primary.on-primary` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

### Dark theme

**`semantic.surface.canvas`** (`#1A191C`) -- Default app/page background -- the base surface nearly everything else sits on.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 17.5:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 16.79:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 15.56:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 8.25:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 8.23:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 8.22:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 8.21:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.success.text` (`#6DC47F`) | 8.21:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 8.2:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.surface.raised`** (`#222124`) -- Cards, modals, popovers, dropdowns -- anything that should read as lifted above canvas.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 16.02:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 16.02:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 16.02:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 16.02:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 15.37:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 14.24:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 7.55:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 7.53:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 7.53:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.feedback.success.text` (`#6DC47F`) | 7.52:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 7.51:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 7.51:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.surface.sunken`** (`#000000`) -- Inset wells, code blocks, resting input fields -- content that reads as pressed in.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 21.0:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 21.0:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 21.0:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 21.0:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 20.14:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 18.66:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 9.89:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 9.87:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 9.87:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 9.85:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.success.text` (`#6DC47F`) | 9.85:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 9.84:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.surface.overlay`** (`rgba(0, 0, 0, 0.64)`) -- Modal/drawer scrim between canvas content and a raised surface. Not a fill for text-bearing content -- no contrast pairing applies.

_No fixed foreground pairing (see note above)._

**`semantic.surface.inverse`** (`#FAFAFC`) -- Opposite-theme surface embedded in the current theme (tooltips, toasts, inverted callouts).

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#000000`) | 20.14:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.interactive.primary.on-primary` (`#000000`) | 20.14:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |
| `semantic.text.inverse` (`#514F55`) | 7.75:1 | AAA normal (7:1+) | Text on surface.inverse. |
| `semantic.text.disabled` (`#69686E`) | 5.29:1 | AAA large only (4.5-6.99:1) | Disabled control labels. WCAG-exempt. |

**`semantic.interactive.primary.default`** (`#A97DFE`) -- Primary button and other high-emphasis filled controls, default state.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#000000`) | 7.05:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.interactive.primary.on-primary` (`#000000`) | 7.05:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.interactive.primary.hover`** (`#BEA3FF`) -- Primary button hover state.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#000000`) | 9.87:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.interactive.primary.on-primary` (`#000000`) | 9.87:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |

**`semantic.interactive.primary.active`** (`#D3C3FF`) -- Primary button active/pressed state.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.text.on-primary` (`#000000`) | 13.02:1 | AAA normal (7:1+) | Labels on a filled primary button. AAA-LARGE tier only (button labels count as large text) -- for small/normal text on a primary fill, use interactive.primary.active as the background instead. |
| `semantic.interactive.primary.on-primary` (`#000000`) | 13.02:1 | AAA normal (7:1+) | Reused as the checkmark/dot icon color on checked checkboxes/radios (see component.checkbox.icon.checked). |
| `semantic.text.inverse` (`#514F55`) | 5.01:1 | AAA large only (4.5-6.99:1) | Text on surface.inverse. |

**`semantic.interactive.primary.disabled`** (`#38373C`) -- Disabled primary button fill. WCAG-exempt -- inactive controls have no contrast requirement.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 11.8:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 11.8:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 11.8:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 11.8:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 11.32:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 10.49:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 5.56:1 | AAA large only (4.5-6.99:1) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 5.55:1 | AAA large only (4.5-6.99:1) | Inline links and clickable text. |
| `semantic.feedback.success.text` (`#6DC47F`) | 5.54:1 | AAA large only (4.5-6.99:1) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.danger.text` (`#FF948C`) | 5.54:1 | AAA large only (4.5-6.99:1) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 5.53:1 | AAA large only (4.5-6.99:1) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 5.53:1 | AAA large only (4.5-6.99:1) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.interactive.primary.subtle`** (`#1C023B`) -- Tinted background for secondary-button hover/active, selected rows, subtle brand emphasis.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 18.73:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 18.73:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 18.73:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 18.73:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 17.97:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 16.65:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 8.82:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 8.81:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 8.8:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.feedback.success.text` (`#6DC47F`) | 8.79:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 8.78:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 8.78:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.feedback.success.background`** (`#001A05`) -- Subtle success alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 18.26:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 18.26:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 18.26:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 18.26:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 17.52:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 16.23:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 8.6:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 8.58:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 8.58:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.feedback.success.text` (`#6DC47F`) | 8.57:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 8.56:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 8.56:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.feedback.warning.background`** (`#211300`) -- Subtle warning alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 18.14:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 18.14:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 18.14:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 18.14:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 17.4:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 16.12:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 8.54:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 8.53:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 8.52:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 8.51:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.success.text` (`#6DC47F`) | 8.51:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 8.5:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.feedback.danger.background`** (`#2E0002`) -- Subtle danger alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 18.8:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 18.8:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 18.8:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 18.8:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 18.03:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 16.71:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 8.86:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 8.84:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 8.83:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 8.82:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.success.text` (`#6DC47F`) | 8.82:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 8.81:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.feedback.info.background`** (`#00152D`) -- Subtle info alert/banner background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 18.34:1 | AAA normal (7:1+) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 18.34:1 | AAA normal (7:1+) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 18.34:1 | AAA normal (7:1+) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 18.34:1 | AAA normal (7:1+) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 17.59:1 | AAA normal (7:1+) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 16.3:1 | AAA normal (7:1+) | Supporting copy one level down from primary -- still full AAA. |
| `semantic.feedback.info.text` (`#6FB7FF`) | 8.64:1 | AAA normal (7:1+) | Info alert body copy / status message, on feedback.info.background. |
| `semantic.text.link` (`#BEA3FF`) | 8.62:1 | AAA normal (7:1+) | Inline links and clickable text. |
| `semantic.feedback.danger.text` (`#FF948C`) | 8.62:1 | AAA normal (7:1+) | Danger alert body copy / status message, on feedback.danger.background. |
| `semantic.text.tertiary` (`#B2B1B5`) | 8.6:1 | AAA normal (7:1+) | Captions, metadata -- least-emphasized tier that's still full AAA. |
| `semantic.feedback.success.text` (`#6DC47F`) | 8.6:1 | AAA normal (7:1+) | Success alert body copy / status message, on feedback.success.background. |
| `semantic.feedback.warning.text` (`#EAA42B`) | 8.6:1 | AAA normal (7:1+) | Warning alert body copy / status message, on feedback.warning.background. |

**`semantic.feedback.success.solid`** (`#007D34`) -- Solid-filled success badge background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 5.27:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 5.06:1 | AAA large only (4.5-6.99:1) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 4.69:1 | AAA large only (4.5-6.99:1) | Supporting copy one level down from primary -- still full AAA. |

**`semantic.feedback.warning.solid`** (`#976500`) -- Solid-filled warning badge background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 5.03:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 4.82:1 | AAA large only (4.5-6.99:1) | Default body copy and headings. |

**`semantic.feedback.danger.solid`** (`#BC001D`) -- Solid-filled danger badge / danger-button background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 6.65:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 6.38:1 | AAA large only (4.5-6.99:1) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 5.91:1 | AAA large only (4.5-6.99:1) | Supporting copy one level down from primary -- still full AAA. |

**`semantic.feedback.info.solid`** (`#006AB7`) -- Solid-filled info badge background.

| Foreground | Ratio | Tier | Usage |
|---|---|---|---|
| `semantic.feedback.success.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled success badge/button. |
| `semantic.feedback.warning.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled warning badge/button. |
| `semantic.feedback.danger.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled danger badge/button. |
| `semantic.feedback.info.on-status` (`#FFFFFF`) | 5.61:1 | AAA large only (4.5-6.99:1) | Text on a solid-filled info badge/button. |
| `semantic.text.primary` (`#FAFAFC`) | 5.38:1 | AAA large only (4.5-6.99:1) | Default body copy and headings. |
| `semantic.text.secondary` (`#F2F1F4`) | 4.98:1 | AAA large only (4.5-6.99:1) | Supporting copy one level down from primary -- still full AAA. |
