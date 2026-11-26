# Typing SVG Tagline

[readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) renders
text that types itself out. Use it as a tagline under the header, or as a
section intro, for apps, showcases, and personal projects. Leave it out of
READMEs that should read calm and technical.

Generate it with `scripts/typing-svg.py`:

```bash
python3 scripts/typing-svg.py --color b030f0 --width 520 \
  "upload • reference • archive" "copy links in any format"
```

## Snippet

```html
<p align="center"><a href="#quick-start"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&size=18&duration=3000&pause=1200&color=B030F0&center=true&vCenter=true&repeat=false&width=520&lines=upload+%E2%80%A2+reference+%E2%80%A2+archive;copy+links+in+any+format">
  <img alt="upload, reference, archive; copy links in any format" src="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&size=18&duration=3000&pause=1200&color=7A1FB0&center=true&vCenter=true&repeat=false&width=520&lines=upload+%E2%80%A2+reference+%E2%80%A2+archive;copy+links+in+any+format">
</picture></a></p>
```

## Parameters

| Param | Notes |
| --- | --- |
| `lines` | `;`-separated; `+` for spaces; URL-encode symbols (`•` = `%E2%80%A2`) |
| `font` | Google Font name (`JetBrains+Mono` matches shieldcn headers) |
| `size`, `weight`, `letterSpacing` | Text styling |
| `color` | Hex without `#`; use the palette accent (darker shade for light mode) |
| `background` | Hex with alpha, default transparent (`00000000`) |
| `center`, `vCenter` | `true` to centre inside the box |
| `width`, `height` | Box size; width must fit the longest line (about `size × 0.6 × chars`) |
| `duration`, `pause` | Typing time per line and pause after it (ms) |
| `repeat` | `false` stops after the last line; **default to `false`** |
| `multiline` | `true` keeps earlier lines visible (one row each) |
| `random` | Random line order |

## Rules

- Default `repeat=false` so it doesn't loop forever (accessibility checklist).
  Use `repeat=true` only when the user asks for it.
- Alt text carries the full text of every line.
- Keep to 1–3 short lines. It's a tagline, not documentation.
- Don't put critical information only in the animation; repeat it in text.
- It's one signature element; don't also add animated badges (`animate=`).
