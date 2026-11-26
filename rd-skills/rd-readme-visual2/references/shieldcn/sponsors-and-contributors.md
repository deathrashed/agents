# Sponsors and contributors

Documented SVG paths: `/sponsors/{login}.svg` and `/contributors/{owner}/{repo}.svg` (PNG may also be available). Common styling: `preset`, `theme`, `bg`, `gradient`, `pattern`, `glow`, `image`, `overlay`, `tint`, `accent`, `radius`, `border`, `watermark`. Contributors may support `limit`, `min`, `names` — verify current docs.

```sh
python3 scripts/shieldcn_visual.py contributors --repo owner/repo --param limit=12 --style presets/white-yellow-outline.json
python3 scripts/shieldcn_visual.py sponsors --user owner --style presets/white-yellow-outline.json
```

Do not invent sponsors, imply endorsement, or claim a contributor is active based only on historical contributions. Prefer these below the main documentation rather than in the first badge row. Document when a remote provider cannot access private repositories.
