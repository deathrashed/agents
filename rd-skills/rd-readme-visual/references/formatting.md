# Formatting Guide

Read while drafting. Covers badge rows, the contents list, dropdowns, showcase
grids, spacing, colour harmony, accessibility, and what belongs in `docs/`.

### Badge Patterns & Multi-Row Organization

**Single-row badges** work for 3-4 items. **Multiple rows** organize by category/theme:

**Pattern 1: Themed rows (recommended)**
```html
<p align="center">
  <!-- Primary integrations/services -->
  <a href="https://www.last.fm/"><img src="https://img.shields.io/badge/Last.fm-Scrobbler-f8211c?style=for-the-badge&logo=last.fm&logoColor=white" alt="Last.fm"></a>
  <a href="https://go.dev/"><img src="https://img.shields.io/badge/Go-%201.24.2%2B-f8211c?style=for-the-badge&logo=go&logoColor=white" alt="Go 1.24.2+"></a>
  <a href="https://license.url"><img src="https://custom-icon-badges.demolab.com/badge/Licence-wtfpl-f8211c?style=for-the-badge&logo=wtfpl-logo-white&logoColor=white" alt="WTFPL 2"></a>
</p>

<p align="center">
  <!-- Platform & runtime -->
  <a href="https://apple.com/macos"><img src="https://img.shields.io/badge/OS-macOS-1e1e1e?style=for-the-badge&logo=apple&logoColor=white" alt="macOS"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.12-1e1e1e?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12"></a>
  <a href="https://example.com"><img src="https://img.shields.io/badge/tool-name-1e1e1e?style=for-the-badge&logo=tool&logoColor=white" alt="Tool"></a>
</p>
```

**Services used:**
- `shields.io` — Standard badges (`style=for-the-badge`)
- `custom-icon-badges.demolab.com` — Custom logos (WTFPL, niche tools)

**Building custom badges:**
Use [DenverCoder1/custom-icon-badges](https://github.com/DenverCoder1/custom-icon-badges) to generate custom badges:

```
https://custom-icon-badges.demolab.com/badge/LABEL-VALUE-HEX?style=for-the-badge&logo=ICON_NAME&logoColor=HEX
```

**Example (WTFPL):**
```html
<img src="https://custom-icon-badges.demolab.com/badge/Licence-wtfpl-622284?style=for-the-badge&logo=wtfpl-logo-white&logoColor=white" alt="WTFPL">
```

**Get icons from:**
- Repo's own asset folder (`logo.svg`, icon from project)
- [Iconify](https://iconify.design/) (convert SVG to icon name)
- Custom upload (repo provides the SVG, badge maker hosts it)

**Color strategies:**
- Primary row: Brand accent (e.g., `f8211c` red)
- Secondary row: Dark neutral (`1e1e1e`) or archetype color
- Keep consistent within rows; can vary across rows for hierarchy

**Organization by:**
1. Primary integrations/services
2. Platform & runtime requirements
3. Dependencies & libraries
4. License (custom badge often goes with integrations or last)

### Table of Contents (TOC) Pattern

**When to use:** README >200 lines or >6 sections

**Manual TOC (GitHub auto-anchors headers):**
```markdown
## Contents

- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
```

GitHub automatically converts `## Quick Start` to anchor `#quick-start` (lowercase, dashes).

**Auto-generate with tools:**
```bash
# Generate TOC automatically
npx markdown-toc README.md

# Or use doctoc
npx doctoc README.md
```

**Placement:** After hero/badges, before quick start. Makes README navigable for long documents.

**Rule:** If your README has a TOC, update it when sections change (manual or auto-tool in CI).

### Collapsible Dropdowns and Showcase Grids

**Collapsible details syntax (GitHub Flavored Markdown):**
```html
<details>
<summary><strong>Advanced configuration</strong></summary>

Content here is hidden by default. Include setup instructions, verbose config,
or options users don't need to see immediately.

</details>
```

**Video/image showcase pattern:**
```markdown
## Demo

| Feature | Screenshot |
|---------|-----------|
| Installation | ![Install GIF](assets/install.gif) |
| Usage | ![Usage GIF](assets/usage.gif) |
| Configuration | ![Config GIF](assets/config.gif) |
```
Use when: project has GIFs showing workflow, has before/after, or visual features worth demoing.

### Spacing & Formatting Rules

**Between hero and first section:** 2 blank lines
```markdown
</div>

---

## Section Title
```

**Between sections:** 1 blank line before `##` header
```markdown
Content above.

## Next Section
```

**Within tables/lists:** Single line breaks in markdown; GitHub renders them correctly
```markdown
| Col A | Col B |
|-------|-------|
| Data  | Data  |
```

**Code block wrapping:** Line length <100 chars when possible (git diffs are readable; mobile-friendly)
```bash
# ✅ Good: Short, easy to diff and read on mobile
git clone https://github.com/user/repo.git && cd repo

# ❌ Bad: Long line hard to see on mobile
git clone https://github.com/verylongusername/verylongreponame.git && cd verylongreponame && npm install && npm run build
```

**Blank lines in code blocks:** Use `<!-- -->` comments as spacers if needed (preserves formatting)

### Color Harmony (Header-Image-Derived)

When the project has a header/logo image, derive the accent palette from it instead of defaulting to the archetype color:

1. **Extract 2 colors from the header image**: a dominant accent (badge backgrounds, primary Iconify color) and a secondary accent (badge `logoColor`, alternating Iconify color).
2. **Apply consistently**: badge background = dominant accent, `logoColor` = secondary accent; Iconify section headers **alternate** between the two accents down the document.
3. **Ask the user when ambiguous**: if the image has more than two strong colors, or the user hasn't provided an image, ask which colors they want before drafting. Never silently pick a palette that clashes with their image.
4. **shields.io constraints**: the badge color field takes ONE hex (no `#`, URL-encode as-is, e.g. `badge/label-value-cf1f25`); two-tone label/value badges (`-colorA-colorB`) are unreliable on GitHub — prefer single background color + `logoColor`. Hex in query params (`logoColor`, Iconify `?color=`) must be `%23`-prefixed.

### Accessibility Checklist (Required)

Before publishing, verify:

- [ ] **Alt text on all images**: Every `<img>` has `alt="description"` (badges, logos, screenshots, GIFs)
- [ ] **Color contrast**: Badge text readable on background (test with [contrast checker](https://webaim.org/resources/contrastchecker/))
- [ ] **No image-only sections**: Text + image, never image alone for critical info
- [ ] **Semantic HTML**: Proper `<h1>`, `<h2>`, `<h3>` hierarchy (not `<div>` styled as headers)
- [ ] **Link text is descriptive**: "Click here" ❌ → "View documentation" ✅
- [ ] **Code blocks have language tag**: ` ```python ` not ` ``` `
- [ ] **Lists are proper lists**: `- item` not just dashes in paragraphs
- [ ] **Table headers marked**: First row is `<th>` or markdown `|`
- [ ] **No flashing/auto-play**: GIFs don't auto-loop endlessly
- [ ] **Readable on mobile**: Test on narrow screen (badges wrap, text stays readable)
- [ ] **Badge links are real**: Every badge `<a href>` points to actual resource (tool, docs, service)
- [ ] **Internal references work**: Links to sections match actual headers (e.g., `[Quick Start](#quick-start)` matches `## Quick Start`)
- [ ] **No dead badge links**: Every badge `href` points to working resource (broken links = broken trust)

### Content Separation: README vs. `/docs/`

The README holds the documentation: every feature area, workflow, setting,
troubleshooting entry and nuance belongs in it, however long that makes it. Keep it
scannable with tables and `<details>` dropdowns rather than by moving content out.

`/docs/` is only for material that is generated or too mechanical to read top to
bottom (a full per-option command reference, API dumps), plus ADRs and plans. Link to
it from the README; never move hand-written explanation there to shorten the README.

### Advanced Dropdown Patterns

Use dropdowns for everything a first-time reader can skip. Keep the summary
bold and specific so a scanning reader knows what's inside.

**Full option reference** (keep the common options visible above it):

```html
<details>
<summary><b>All options</b></summary>

| Flag | Default | Description |
| --- | --- | --- |
| `--dry-run` | off | Show the plan without changing anything |
| `--json` | off | Machine-readable output |

</details>
```

**Per-platform setup** (one dropdown per platform, alert inside when needed):

~~~html
<details>
<summary><b>Linux setup</b></summary>

> [!NOTE]
> Clipboard support needs `wl-copy` (Wayland) or `xclip` (X11).

```bash
sudo apt install xclip
```

</details>
~~~

**Troubleshooting / FAQ** (one dropdown per problem, phrased as the symptom):

```html
<details>
<summary><b>"Permission denied" when installing</b></summary>

Run the installer as your user, not with `sudo`. It writes to `~/.local`.

</details>
```

**Grouped catalogue** (one dropdown per category, with a count in the summary):

```html
<details>
<summary><b>Audio tools</b> · 12 scripts</summary>

| Script | What it does |
| --- | --- |
| `normalize.sh` | Loudness-normalises a folder |

</details>
```

Rules:

- A blank line after `<summary>…</summary>` and before `</details>`, or Markdown inside won't render.
- No emoji in summaries; use plain bold text, or a small Iconify `<img height="16">` before the text.
- Don't nest dropdowns more than one level deep.

### GitHub Alert Hints

| Alert | Use for |
| --- | --- |
| `> [!TIP]` | Shortcuts and nicer ways to do something |
| `> [!NOTE]` | Context that helps but isn't required |
| `> [!IMPORTANT]` | Requirements and must-do setup steps |
| `> [!WARNING]` | Things that can break, overwrite, or publish publicly |
| `> [!CAUTION]` | Irreversible actions or data loss |

Place each alert right next to the step it's about. Use 2–5 per README; more
than that and they stop standing out.
