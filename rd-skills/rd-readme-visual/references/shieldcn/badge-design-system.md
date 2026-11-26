# Badge design system

Documentation: https://shieldcn.dev/docs/api-reference and https://shieldcn.dev/docs/badges/static

Static: `/badge/{label}-{value}-{color}.svg`; live providers: `/github/stars/{owner}/{repo}.svg` etc. Badge `variant`: `default`, `secondary`, `outline`, `ghost`, `destructive`, `branded`. Badge parameters include `mode`, `logo`, `logoColor`, `color`, `valueColor`, `labelTextColor`, `labelColor`, `split`, `font`, `size`, `radius`, `iconSize`, `padX`, `gap`, `labelGap`, `gradient`, `animate` (subject to renderer support).

## Critical relationships

- `color` is not always an outline-only property; `split=true` changes surfaces. Test visual output, particularly when `labelColor` is also set.
- `labelTextColor` controls label text; `valueColor` controls value text. Keep both distinct from `logoColor`.
- `mode=dark` and `mode=light` alone do not guarantee contrast if explicit white text is forced on a light page.
- URL parameters require `&amp;` *inside HTML attributes*, and `#` must be encoded as `%23` when it belongs to a URL parameter.
- `logo=lu:Zap`, `logo=ri:BsPlugin`, `logo=python` are different namespaces. Icon identifiers are not guaranteed to exist; verify by rendering.
- True split label-value badges may need label background overrides. Don't promise transparent surfaces with `split=true` without verifying.

## Presets

`presets/white-yellow-outline.json`: white outline `ffffff`, yellow icons `ffda00`, white label, yellow value. `presets/lastfm-red.json`: Last.fm accent. `presets/zinc-minimal.json`: muted grayscale. Adapt individual variants for legibility in GitHub light theme; never assume the dark preset is readable there.

## Recipe

```sh
python3 scripts/shieldcn_visual.py badge --label Skills --value 10 --logo lu:Zap --style presets/white-yellow-outline.json
```

Use secondary row for operating systems or community/status badges. Link each badge to a real relevant section or destination. Never make every badge link to a project root when more meaningful links exist.
