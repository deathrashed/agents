# shieldcn first: badges, headers, groups

Complete spec: `shieldcn-api.md` (and raw docs in `shieldcn-docs/`). Builders: `scripts/shieldcn_badge.py` (any endpoint, `--param` for any option), `scripts/generate-header.py`, `scripts/generate-badge-row.py`.

Primary system for badges and the hero header: https://shieldcn.dev (shadcn/ui-styled, shields.io
alternative; docs https://shieldcn.dev/docs, studio https://shieldcn.dev/studio, installed skill
`~/.agents/skills/shieldcn-badges` has the full endpoint list). The owner's own shields.io style and the
huge catalog in `/Users/rd/Obsidian/Shields.md` (md-badges list) are the fallback and the logo-slug lookup.

All of these were rendered and looked at (2026-10-15); do the same for any new combination before shipping.

## Top block

One common order (gupload, perkolator): banner, one badge row, summary, nav. In a private repo give the banner the
project icon as a `data:` URI (96 px WebP, about 1.7 KB, URL under ~4,000 characters for GitHub's proxy); never a
raw-repo URL with its expiring `?token=`.

```html
<div align="center">

<p align="center"><img alt="PROJECT" src="https://shieldcn.dev/header/grid.svg?title=PROJECT&subtitle=verb+%E2%80%A2+verb+%E2%80%A2+verb&logo=LOGO_URL_ENCODED&mode=dark&font=jetbrains-mono"></p>

<p align="center">
  ONE ROW OF 3-5 OUTLINE BADGES (generate-badge-row.py --variant outline; it writes this <p> itself)
</p>
<p align="center"><strong>One sentence saying what it does for the reader.</strong></p>
<p align="center"><a href="#quick-start">Quick Start</a> | <a href="#usage">Usage</a> | <a href="#license">License</a></p>

</div>

---
```

## Always adaptive: light and dark pairs

GitHub READMEs are read in both themes, so every shieldcn image is a `<picture>` pair:

```html
<a href="https://www.rust-lang.org/"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/badge/rust.svg?variant=secondary&size=sm&logo=rust&logoColor=5fe27f&mode=dark" />
  <img alt="Built with Rust" src="https://shieldcn.dev/badge/rust.svg?variant=secondary&size=sm&logo=rust&logoColor=5fe27f&mode=light" />
</picture></a>
```

`scripts/generate-badge-row.py` writes these rows for you.

## Colour: derive from the header image

- `theme=` picks the shadcn accent: `zinc slate blue green rose orange violet purple cyan emerald`. Map the
  icon's dominant colour to the nearest theme (LED green -> `green`/`emerald`).
- `logoColor=<hex>` tints the logo (use the icon's accent, e.g. `5fe27f`).
- `color=<hex>` sets the main surface only when no theme fits.

## Badge variants (rendered)

| variant | look | use |
|---|---|---|
| `outline` | border only | the usual choice in gupload, dockmoid and lyrixearch |
| `secondary` | quiet filled pill | calm rows, readable in both themes |
| `branded` | brand-coloured | one or two hero badges only |
| `default` | solid accent | single call-to-action badge |
| `split=true` | two-tone label/value | status/data pairs (`Rust` / `2024`); soft, low contrast, use sparingly |

Sizes `xs sm default lg`; keep rows to 3-6 badges. `/group/<badge>+<badge>.svg` renders one joined image.
Rows: themed, each in its own `<p align="center">`: (1) stack/product, (2) platforms, (3) license/status.

## Palette

Choose one accent hex and use it everywhere:

| Place | How |
| --- | --- |
| shieldcn badges | `theme=` nearest named theme, or `color=`/`logoColor=` hex |
| shieldcn header | `theme=`, `accent=`, `titleColor=` |
| Iconify headings | `?color=%23HEX` |
| Typing SVG | `color=HEX` (no `#`) |
| License block | pick the license variant that fits (green variants for green palettes) |

Past palettes (avoid copying the previous project's exactly):

| Project | Accent | Theme |
| --- | --- | --- |
| gupload | `#b030f0` | purple |
| dockmoid | `#2560ff` / `#759bff` | blue |
| lyrixearch | `#5fe27f` / `#1f8f43` | green |
| komp (classic) | `#cf1f25` + `#fec900` | — |

## Headers (rendered)

Generate one with `scripts/generate-header.py --title NAME --subtitle "tagline" [--preset dots|graph|grid|gradient|glow|surface|transparent] [--logo slug --logo-color hex] [--align left|center]`.
The owner's reference banner is `dots`, left-aligned, upper-case title, no logo: `![LYRIXEARCH](https://shieldcn.dev/header/dots.svg?title=LYRIXEARCH&subtitle=find%2C+review+%26+embed+lyrics+for+your+audio+library&mode=dark&align=left)` (always ship it as the light/dark pair below).

```html
<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/header/graph.svg?title=NAME&subtitle=TAGLINE&logo=rust&logoColor=5fe27f&font=geist-mono&align=left&border=false&mode=dark" />
  <img alt="NAME" src="https://shieldcn.dev/header/graph.svg?title=NAME&subtitle=TAGLINE&logo=rust&logoColor=5fe27f&font=geist-mono&align=left&border=false&mode=light" />
</picture></p>
```

Presets: `graph` (technical grid, best for CLIs/dev tools), `grid` (light technical), `gradient` (soft
centred product look), `dots`, `glow`, `surface`, `transparent`. Params: `title subtitle logo logoColor theme
font align border radius bg gradient pattern glow accent titleColor subtitleColor image overlay tint watermark`.
Fonts: `inter geist geist-mono jetbrains-mono fira-code roboto space-grotesk`.

The header replaces the plain `<h1>` + icon only when the owner wants a banner. Keep the project icon
(`assets/icon.png`) as the logo when it exists: pass it via `image=` only if it is publicly reachable;
otherwise use the icon in a normal `<img>` above the header or use a SimpleIcons slug in `logo=`.

## Gotchas

- Private repo assets do not load for other readers; use public URLs only.
- Logos are SimpleIcons slugs; if a slug is missing use `logo=ri:Name` or a `data:` URI, or fall back to
  a shields.io / custom-icon-badges badge. Check slugs in `/Users/rd/Obsidian/Shields.md`.
- Star-history charts work again (`/chart/github/stars/{o}/{r}.svg`, privacy-safe weekly counts; the older note that they were retired is out of date). Verify with `curl -s URL | wc -c` (a retired chart returns a 100x1 blank).
- Do not mix many styles: one variant per row.
- Always `curl -sIL` each URL (the validator does this with `--online`).

## shields.io fallback (the owner's style)

Two-tone path colours (`badge/label-msg-colorA-colorB`) are unreliable; the reliable way to get an icon
segment is the `labelColor` query parameter:

```
https://img.shields.io/badge/<label>-<bg>?style=for-the-badge&logo=<slug>&logoColor=<accent>&labelColor=<lighter-bg>
```

Example: `badge/rust-202327?style=for-the-badge&logo=rust&logoColor=5fe27f&labelColor=40474e`. For logos
shields.io lacks (MIT licence, GPL) use `https://custom-icon-badges.demolab.com/badge/...&logo=<name>`.
