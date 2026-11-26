# Tailored License Blocks

Riley's license assets live in the gupload repo, in
`uploads/files/licenses/<id>/`. Each folder holds the full `LICENSE` text
(already filled in with `2026 deathrashed <dethrashed@gmail.com>` where the
license has a copyright line), `metadata.json`, badge and logo SVGs, and one or
more ready-made README snippets.

Local path: `/Users/rd/Scripts/Riley/gupload/uploads/files/licenses/`
Raw URL base: `https://raw.githubusercontent.com/deathrashed/gupload/refs/heads/main/uploads/files/licenses/`

## Library

The script reads the folders at run time, so this table is a guide, not the source of truth:

```bash
python3 scripts/license-snippet.py --list
```

| id | License | Snippets |
| --- | --- | --- |
| `mit` | MIT | standard, green |
| `bsd` | BSD 2-Clause | standard, green |
| `apache` | Apache 2.0 | standard, green |
| `gpl` | GPL-3.0-or-later | standard, green, free-works |
| `lgpl` | LGPL-3.0-or-later | standard |
| `wtfpl` | WTFPL | standard |
| `unlicense` | Unlicense | standard (public-domain footer) |
| `cc0` | CC0 1.0 | standard (public-domain footer) |
| `cc-by` | CC BY 4.0 | standard |
| `cc-by-sa` | CC BY-SA 4.0 | standard |

Variants:

- **standard** (`snippet.md`): the license's own logo next to "License" and its badge
- **green** (`green-snippet.md`): open-source logo and the green badge; suits green palettes
- **free-works** (`free-works-snippet.md`): free-works logo with the classic badge

## Use

```bash
# Print the block for README
python3 scripts/license-snippet.py gpl --variant free-works

# Also copy the tailored LICENSE into the repo root (asks before overwriting)
python3 scripts/license-snippet.py gpl --variant free-works --install /path/to/repo
```

Rules:

- The block's license must match the repo's `LICENSE`. If they differ, ask which
  is right before changing either.
- Put the block last, under `<a name="license"></a>` so `#license` links work.
- Keep the blank line after `<div align="center">`; without it GitHub shows the
  bold title as literal `**...**`.
- Public-domain licenses (Unlicense, CC0) use a dedication line, not a copyright line.

## Shape

```html
<a name="license"></a>

## <a href="LICENSE_SITE"><img src="LOGO_URL" height="20" alt=""></a> License

<div align="center">

[**𝗚𝗡𝗨 𝗚𝗣𝗟 𝗟𝗜𝗖𝗘𝗡𝗦𝗘**](LICENSE_URL)

<a href="LICENSE_URL"><img src="BADGE_URL" alt="GPL Badge" width="180"></a>

**𝗖𝗢𝗣𝗬𝗥𝗜𝗚𝗛𝗧 © 𝟮𝟬𝟮𝟲 𝗗𝗘𝗔𝗧𝗛𝗥𝗔𝗦𝗛𝗘𝗗**

</div>
```

## Missing license or variant

If the user wants a license or variant that isn't in the library, add it to
gupload first (badge, logo, `LICENSE` filled in with the user's details,
`metadata.json`, snippet) following the existing folders' naming
(`<id>-license-badge.svg`, `<id>-license-logo.svg`), then use it. Real license
badges only, not generic shields. `~/licences/` holds source texts and official artwork.
