# rickysunay.com — portfolio site

Static HTML/CSS/JS. No CMS, no framework, no build step. Open any file, edit, save, deploy.

## Where things live

| I want to change… | Edit this |
|---|---|
| Colors, type, spacing, radii (the whole theme) | `css/tokens.css` — **Tier 1 primitives only** |
| What a color role points to (e.g. link color) | `css/tokens.css` — Tier 2 semantic aliases |
| Layout or component styling | `css/main.css` (references tokens only — no raw hex values here) |
| Page copy | The HTML files. Every copy block is fenced with `<!-- ===== COPY: ... ===== -->` comments — search for `COPY:` and edit between the fences |
| Images | Drop files in `assets/img/`, update the `src` and `alt` in the HTML |
| Image width (full vs centered) | Add `spec-figure--narrow` (680px) or `spec-figure--medium` (920px) to the `<figure>` class — remove it to go back to full width |
| Resume | Replace `assets/docs/RickySunay-Resume.pdf` (keep the filename and no links break) |
| The footer token readout / press-G grid | `js/site.js` (the only JS on the site) |

## Layout patterns

`work/_layout-template.html` is an internal page (noindex, not linked anywhere)
demoing every available layout with copy-paste markup: full-width / full-bleed /
centered figures, half-and-half splits (plus flipped and sticky variants), a 3:4
portrait grid, a 3/4 + 1/4 aside, a bento grid, scrollytelling, and a carousel.
Each section has an HTML comment explaining usage. The styles live in
`css/main.css` section 17.

## Adding a full case study

1. Copy `work/liquid-m1.html` as your template.
2. Replace the copy between the `COPY:` fences and swap the figures.
3. Update the matching card in `index.html` (remove `case-card--pending`, add real description + tags).

## Header/footer note

There's no templating, so the header and footer are repeated in every HTML file
on purpose (it keeps the site dependency-free). If you change the nav or footer,
find-and-replace across all files: `index.html`, `about.html`, `contact.html`,
and everything in `work/`.

## Deploying

**Netlify:** drag the whole folder onto app.netlify.com. Done.
**Vercel:** `npx vercel` in this folder, or import the repo on vercel.com. No config needed — it's plain static files.

## Accessibility checklist (already in place — keep it that way)

- One `h1` per page; headings never skip levels
- Every image has descriptive `alt` text
- All text colors pass WCAG AA on their backgrounds (ratios documented in `tokens.css` comments)
- Red fills always use dark text (`--fg-on-accent`), never white
- Keyboard: skip link, `:focus-visible` rings, no focus traps
- `prefers-reduced-motion` respected
