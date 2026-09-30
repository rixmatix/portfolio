"""
Formal contrast audit deliverable. Re-runs the same verification used while
building the semantic layer (build_semantic.run_checks) plus the chart
supporting-token checks, and emits audit_report.md -- every pairing, its
computed ratio, and pass/fail/exempt status.
"""
from build_semantic import run_checks
from build_charts import ALL_CHART_TOKENS
from color import contrast_ratio
from build_primitives import CANVAS_DARK_HEX

def chart_supporting_checks():
    sup = ALL_CHART_TOKENS["supporting"]
    rows = []
    targets = {
        "axis-line": (3.0, "chart non-text minimum 3:1"),
        "gridline": (3.0, "chart non-text minimum 3:1"),
        "data-label-text": (4.5, "chart text minimum 4.5:1"),
    }
    for name, v in sup.items():
        target, target_name = targets[name]
        r_light = contrast_ratio(v["light"], "#FFFFFF")
        rows.append({"label": f"chart.{name} (light) vs canvas", "fg": v["light"], "bg": "#FFFFFF",
                      "ratio": round(r_light, 2), "target": target, "target_name": target_name,
                      "status": "PASS" if r_light >= target else "FAIL", "exempt_reason": None})
        r_dark = contrast_ratio(v["dark"], CANVAS_DARK_HEX)
        rows.append({"label": f"chart.{name} (dark) vs canvas", "fg": v["dark"], "bg": CANVAS_DARK_HEX,
                      "ratio": round(r_dark, 2), "target": target, "target_name": target_name,
                      "status": "PASS" if r_dark >= target else "FAIL", "exempt_reason": None})
    return rows


def render_markdown(rows):
    lines = []
    lines.append("# Contrast Audit Report\n")
    lines.append("Every semantic text/background, icon/background, and non-text UI pairing in the token system, "
                  "computed programmatically (`scripts/color.py`, pure-Python WCAG relative-luminance + contrast-ratio "
                  "implementation, verified against known references -- see `scripts/color.py` `__main__` block).\n")
    lines.append("**Targets:**\n")
    lines.append("- AAA normal text: **7:1**")
    lines.append("- AAA large text (>=24px regular or >=18.66px/14pt bold, e.g. headings, button labels): **4.5:1**")
    lines.append("- Non-text UI (borders, icons, focus indicators) -- WCAG only defines AA (3:1) for this; this system "
                  "holds it to an internal standard of **4.5:1**, stricter than the spec.")
    lines.append("- Chart supporting tokens (axis line, gridline, data label text) use chart-specific, deliberately "
                  "relaxed targets: **3:1** for non-text (axis/gridline), **4.5:1** for text (data labels) -- dense "
                  "charts need lighter supporting marks than general UI to avoid visual noise; documented explicitly "
                  "here so it is never mistaken for the general 7:1/4.5:1-internal targets above.")
    lines.append("- EXEMPT rows are WCAG-recognized carve-outs (disabled/inactive component text has no contrast "
                  "requirement) or deliberately decorative dividers not required to convey a boundary -- both "
                  "reasoned explicitly per-row, not silently skipped.\n")

    total = len(rows)
    passed = sum(1 for r in rows if r["status"] == "PASS")
    failed = sum(1 for r in rows if r["status"] == "FAIL")
    exempt = sum(1 for r in rows if r["status"] == "EXEMPT")
    lines.append(f"**Summary: {total} pairings checked -- {passed} PASS, {failed} FAIL, {exempt} EXEMPT.**\n")

    lines.append("| Status | Pairing | Foreground | Background | Ratio | Target |")
    lines.append("|---|---|---|---|---|---|")
    for r in rows:
        status_icon = {"PASS": "PASS", "FAIL": "**FAIL**", "EXEMPT": "EXEMPT"}[r["status"]]
        note = f" ({r['exempt_reason']})" if r.get("exempt_reason") else ""
        lines.append(f"| {status_icon} | {r['label']}{note} | `{r['fg']}` | `{r['bg']}` | {r['ratio']}:1 | {r['target_name']} |")

    lines.append("")
    if failed:
        lines.append(f"## ⚠ {failed} failing pairings require attention before ship.\n")
        for r in rows:
            if r["status"] == "FAIL":
                lines.append(f"- {r['label']}: {r['fg']} vs {r['bg']} = {r['ratio']}:1, needs {r['target_name']}")
    else:
        lines.append("## All non-exempt pairings pass their target. No failing pairings.\n")

    return "\n".join(lines)


if __name__ == "__main__":
    semantic_rows = run_checks(verbose=False)
    chart_rows = chart_supporting_checks()
    all_rows = semantic_rows + chart_rows

    md = render_markdown(all_rows)
    with open("../audit_report.md", "w") as f:
        f.write(md + "\n")

    total = len(all_rows)
    passed = sum(1 for r in all_rows if r["status"] == "PASS")
    failed = sum(1 for r in all_rows if r["status"] == "FAIL")
    exempt = sum(1 for r in all_rows if r["status"] == "EXEMPT")
    print(f"wrote ../audit_report.md -- {total} checks: {passed} PASS, {failed} FAIL, {exempt} EXEMPT")
