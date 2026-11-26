# Headers and banners

Docs: https://shieldcn.dev/docs/headers ; https://shieldcn.dev/docs/api-reference

Endpoint `/header/{preset}.svg`. Presets: `surface`, `gradient`, `dots`, `grid`, `graph`, `glow`, `transparent`. Common parameters (check live docs): `title`, `subtitle`, `logo`, `logoColor`, `theme`, `size`, `width`, `height`, `align`, `font`, `border`, `radius`, `bg`, `gradient`, `pattern`, `glow`, `accent`, `titleColor`, `subtitleColor`, `image`, `overlay`, `tint`, `watermark`.

- `surface`: plain product identity, minimalist repo.
- `dots`, `grid`, `graph`: technical background for CLI, systems, developer tools.
- `gradient`, `glow`: branded app/portfolio, use restrained accent.
- `transparent`: existing branded image or site surface, check contrast in GitHub themes.

Use one stable title; one concise subtitle; avoid a tiny dense paragraph embedded into SVG. Prefer width ~1280 and height ~350-420 for wide hero, but inspect the actual result on narrow mobile viewports. If project has an actual logo, use it or host it locally; never replace it with an unrelated generic mark. External image support may depend on source restrictions.

```sh
python3 scripts/shieldcn_visual.py header --preset graph --title AGENTS --subtitle 'Portable developer configuration' --logo lu:Zap --width 1280 --height 400 --style presets/white-yellow-outline.json
```

Do not force a banner when the project already uses a strong custom hero asset. Compare generated header with existing branded header, preserve owner intent. `README Studio` can help lay out top-level elements; it does not replace verification.
