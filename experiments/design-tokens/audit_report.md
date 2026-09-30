# Contrast Audit Report

Every semantic text/background, icon/background, and non-text UI pairing in the token system, computed programmatically (`scripts/color.py`, pure-Python WCAG relative-luminance + contrast-ratio implementation, verified against known references -- see `scripts/color.py` `__main__` block).

**Targets:**

- AAA normal text: **7:1**
- AAA large text (>=24px regular or >=18.66px/14pt bold, e.g. headings, button labels): **4.5:1**
- Non-text UI (borders, icons, focus indicators) -- WCAG only defines AA (3:1) for this; this system holds it to an internal standard of **4.5:1**, stricter than the spec.
- Chart supporting tokens (axis line, gridline, data label text) use chart-specific, deliberately relaxed targets: **3:1** for non-text (axis/gridline), **4.5:1** for text (data labels) -- dense charts need lighter supporting marks than general UI to avoid visual noise; documented explicitly here so it is never mistaken for the general 7:1/4.5:1-internal targets above.
- EXEMPT rows are WCAG-recognized carve-outs (disabled/inactive component text has no contrast requirement) or deliberately decorative dividers not required to convey a boundary -- both reasoned explicitly per-row, not silently skipped.

**Summary: 78 pairings checked -- 74 PASS, 0 FAIL, 4 EXEMPT.**

| Status | Pairing | Foreground | Background | Ratio | Target |
|---|---|---|---|---|---|
| PASS | text.primary (light) vs canvas | `#222124` | `#FAFAFC` | 15.37:1 | AAA normal 7:1 |
| PASS | text.primary (light) vs raised | `#222124` | `#FFFFFF` | 16.02:1 | AAA normal 7:1 |
| PASS | text.secondary (light) vs canvas | `#38373C` | `#FAFAFC` | 11.32:1 | AAA normal 7:1 |
| PASS | text.secondary (light) vs raised | `#38373C` | `#FFFFFF` | 11.8:1 | AAA normal 7:1 |
| PASS | text.tertiary (light) vs canvas | `#514F55` | `#FAFAFC` | 7.75:1 | AAA normal 7:1 |
| PASS | text.tertiary (light) vs raised | `#514F55` | `#FFFFFF` | 8.08:1 | AAA normal 7:1 |
| EXEMPT | text.disabled (light) vs canvas (WCAG 2.1: inactive/disabled UI components and their text have no contrast requirement) | `#A5A4A8` | `#FAFAFC` | 2.38:1 | exempt |
| PASS | text.inverse (light) vs surface.inverse | `#B2B1B5` | `#1A191C` | 8.21:1 | AAA normal 7:1 |
| PASS | text.link (light) vs canvas | `#672AB7` | `#FAFAFC` | 7.77:1 | AAA normal 7:1 |
| PASS | text.link (light) vs raised | `#672AB7` | `#FFFFFF` | 8.1:1 | AAA normal 7:1 |
| PASS | text.on-primary (light) vs interactive.primary.default | `#FFFFFF` | `#7C36D9` | 6.2:1 | AAA large-text 4.5:1 (button labels/headings only) |
| PASS | interactive.primary.on-primary (light) vs interactive.primary.default (same token pair) | `#FFFFFF` | `#7C36D9` | 6.2:1 | AAA large-text 4.5:1 (button labels/headings only) |
| PASS | text.on-primary (light) vs interactive.primary.active (normal-text safety check) | `#FFFFFF` | `#461184` | 12.55:1 | AAA normal 7:1 |
| PASS | border.default (light) vs canvas | `#69686E` | `#FAFAFC` | 5.29:1 | non-text internal 4.5:1 |
| PASS | border.strong (light) vs canvas | `#514F55` | `#FAFAFC` | 7.75:1 | non-text internal 4.5:1 |
| EXEMPT | border.subtle (light) vs canvas (subtle border is intentionally sub-threshold (barely-there divider, not a required-to-perceive boundary)) | `#DCDCDF` | `#FAFAFC` | 1.31:1 | decorative |
| PASS | border.focus (light) vs canvas | `#7C36D9` | `#FAFAFC` | 5.95:1 | non-text internal 4.5:1 |
| PASS | focusRing (light) vs canvas | `#7C36D9` | `#FAFAFC` | 5.95:1 | non-text internal 4.5:1 |
| PASS | interactive.primary.default (light) vs canvas | `#7C36D9` | `#FAFAFC` | 5.95:1 | non-text internal 4.5:1 |
| PASS | component: link/tabs hover-active text (light) vs canvas | `#461184` | `#FAFAFC` | 12.04:1 | AAA normal 7:1 |
| PASS | feedback.success.text (light) vs feedback.success.background | `#005D25` | `#E8F9EA` | 7.39:1 | AAA normal 7:1 |
| PASS | feedback.success.text (light) vs canvas | `#005D25` | `#FAFAFC` | 7.77:1 | AAA normal 7:1 |
| PASS | feedback.success.border (light) vs canvas | `#007D34` | `#FAFAFC` | 5.06:1 | non-text internal 4.5:1 |
| PASS | feedback.success.on-status (light) vs feedback.success.solid (vivid fill) | `#FFFFFF` | `#007D34` | 5.27:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | feedback.warning.text (light) vs feedback.warning.background | `#6E4800` | `#FFF2E2` | 7.36:1 | AAA normal 7:1 |
| PASS | feedback.warning.text (light) vs canvas | `#6E4800` | `#FAFAFC` | 7.78:1 | AAA normal 7:1 |
| PASS | feedback.warning.border (light) vs canvas | `#976500` | `#FAFAFC` | 4.82:1 | non-text internal 4.5:1 |
| PASS | feedback.warning.on-status (light) vs feedback.warning.solid (vivid fill) | `#FFFFFF` | `#976500` | 5.03:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | feedback.danger.text (light) vs feedback.danger.background | `#A3061A` | `#FFEEED` | 7.2:1 | AAA normal 7:1 |
| PASS | feedback.danger.text (light) vs canvas | `#A3061A` | `#FAFAFC` | 7.75:1 | AAA normal 7:1 |
| PASS | feedback.danger.border (light) vs canvas | `#BC001D` | `#FAFAFC` | 6.38:1 | non-text internal 4.5:1 |
| PASS | feedback.danger.on-status (light) vs feedback.danger.solid (vivid fill) | `#FFFFFF` | `#BC001D` | 6.65:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | feedback.info.text (light) vs feedback.info.background | `#00518F` | `#EBF5FF` | 7.4:1 | AAA normal 7:1 |
| PASS | feedback.info.text (light) vs canvas | `#00518F` | `#FAFAFC` | 7.83:1 | AAA normal 7:1 |
| PASS | feedback.info.border (light) vs canvas | `#006AB7` | `#FAFAFC` | 5.38:1 | non-text internal 4.5:1 |
| PASS | feedback.info.on-status (light) vs feedback.info.solid (vivid fill) | `#FFFFFF` | `#006AB7` | 5.61:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | text.primary (dark) vs canvas | `#FAFAFC` | `#1A191C` | 16.79:1 | AAA normal 7:1 |
| PASS | text.primary (dark) vs raised | `#FAFAFC` | `#222124` | 15.37:1 | AAA normal 7:1 |
| PASS | text.secondary (dark) vs canvas | `#F2F1F4` | `#1A191C` | 15.56:1 | AAA normal 7:1 |
| PASS | text.secondary (dark) vs raised | `#F2F1F4` | `#222124` | 14.24:1 | AAA normal 7:1 |
| PASS | text.tertiary (dark) vs canvas | `#B2B1B5` | `#1A191C` | 8.21:1 | AAA normal 7:1 |
| PASS | text.tertiary (dark) vs raised | `#B2B1B5` | `#222124` | 7.51:1 | AAA normal 7:1 |
| EXEMPT | text.disabled (dark) vs canvas (WCAG 2.1: inactive/disabled UI components and their text have no contrast requirement) | `#69686E` | `#1A191C` | 3.17:1 | exempt |
| PASS | text.inverse (dark) vs surface.inverse | `#514F55` | `#FAFAFC` | 7.75:1 | AAA normal 7:1 |
| PASS | text.link (dark) vs canvas | `#BEA3FF` | `#1A191C` | 8.23:1 | AAA normal 7:1 |
| PASS | text.link (dark) vs raised | `#BEA3FF` | `#222124` | 7.53:1 | AAA normal 7:1 |
| PASS | text.on-primary (dark) vs interactive.primary.default | `#000000` | `#A97DFE` | 7.05:1 | AAA large-text 4.5:1 (button labels/headings only) |
| PASS | interactive.primary.on-primary (dark) vs interactive.primary.default (same token pair) | `#000000` | `#A97DFE` | 7.05:1 | AAA large-text 4.5:1 (button labels/headings only) |
| PASS | text.on-primary (dark) vs interactive.primary.active (normal-text safety check) | `#000000` | `#D3C3FF` | 13.02:1 | AAA normal 7:1 |
| PASS | border.default (dark) vs canvas | `#86858A` | `#1A191C` | 4.78:1 | non-text internal 4.5:1 |
| PASS | border.strong (dark) vs canvas | `#A5A4A8` | `#1A191C` | 7.06:1 | non-text internal 4.5:1 |
| EXEMPT | border.subtle (dark) vs canvas (subtle border is intentionally sub-threshold (barely-there divider, not a required-to-perceive boundary)) | `#38373C` | `#1A191C` | 1.48:1 | decorative |
| PASS | border.focus (dark) vs canvas | `#A97DFE` | `#1A191C` | 5.88:1 | non-text internal 4.5:1 |
| PASS | focusRing (dark) vs canvas | `#A97DFE` | `#1A191C` | 5.88:1 | non-text internal 4.5:1 |
| PASS | interactive.primary.default (dark) vs canvas | `#A97DFE` | `#1A191C` | 5.88:1 | non-text internal 4.5:1 |
| PASS | component: link/tabs hover-active text (dark) vs canvas | `#D3C3FF` | `#1A191C` | 10.85:1 | AAA normal 7:1 |
| PASS | feedback.success.text (dark) vs feedback.success.background | `#6DC47F` | `#001A05` | 8.57:1 | AAA normal 7:1 |
| PASS | feedback.success.text (dark) vs canvas | `#6DC47F` | `#1A191C` | 8.21:1 | AAA normal 7:1 |
| PASS | feedback.success.border (dark) vs canvas | `#46B362` | `#1A191C` | 6.57:1 | non-text internal 4.5:1 |
| PASS | feedback.success.on-status (dark) vs feedback.success.solid (vivid fill) | `#FFFFFF` | `#007D34` | 5.27:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | feedback.warning.text (dark) vs feedback.warning.background | `#EAA42B` | `#211300` | 8.5:1 | AAA normal 7:1 |
| PASS | feedback.warning.text (dark) vs canvas | `#EAA42B` | `#1A191C` | 8.2:1 | AAA normal 7:1 |
| PASS | feedback.warning.border (dark) vs canvas | `#D99300` | `#1A191C` | 6.77:1 | non-text internal 4.5:1 |
| PASS | feedback.warning.on-status (dark) vs feedback.warning.solid (vivid fill) | `#FFFFFF` | `#976500` | 5.03:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | feedback.danger.text (dark) vs feedback.danger.background | `#FF948C` | `#2E0002` | 8.83:1 | AAA normal 7:1 |
| PASS | feedback.danger.text (dark) vs canvas | `#FF948C` | `#1A191C` | 8.22:1 | AAA normal 7:1 |
| PASS | feedback.danger.border (dark) vs canvas | `#F45A56` | `#1A191C` | 5.37:1 | non-text internal 4.5:1 |
| PASS | feedback.danger.on-status (dark) vs feedback.danger.solid (vivid fill) | `#FFFFFF` | `#BC001D` | 6.65:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | feedback.info.text (dark) vs feedback.info.background | `#6FB7FF` | `#00152D` | 8.64:1 | AAA normal 7:1 |
| PASS | feedback.info.text (dark) vs canvas | `#6FB7FF` | `#1A191C` | 8.25:1 | AAA normal 7:1 |
| PASS | feedback.info.border (dark) vs canvas | `#389EFB` | `#1A191C` | 6.21:1 | non-text internal 4.5:1 |
| PASS | feedback.info.on-status (dark) vs feedback.info.solid (vivid fill) | `#FFFFFF` | `#006AB7` | 5.61:1 | AAA large-text 4.5:1 (badge/banner labels) |
| PASS | chart.axis-line (light) vs canvas | `#69686E` | `#FFFFFF` | 5.52:1 | chart non-text minimum 3:1 |
| PASS | chart.axis-line (dark) vs canvas | `#86858A` | `#1A191C` | 4.78:1 | chart non-text minimum 3:1 |
| PASS | chart.gridline (light) vs canvas | `#86858A` | `#FFFFFF` | 3.66:1 | chart non-text minimum 3:1 |
| PASS | chart.gridline (dark) vs canvas | `#69686E` | `#1A191C` | 3.17:1 | chart non-text minimum 3:1 |
| PASS | chart.data-label-text (light) vs canvas | `#514F55` | `#FFFFFF` | 8.08:1 | chart text minimum 4.5:1 |
| PASS | chart.data-label-text (dark) vs canvas | `#B2B1B5` | `#1A191C` | 8.21:1 | chart text minimum 4.5:1 |

## All non-exempt pairings pass their target. No failing pairings.

