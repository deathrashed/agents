# Charts and visualizations

Docs: https://shieldcn.dev/docs/charts ; https://shieldcn.dev/docs/charts/star-history

Current documented chart paths include `/chart/github/issues/{owner}/{repo}.svg`, `/chart/github/stars/{owner}/{repo}.svg`, `/chart/github/commits/{user}.svg`, `/chart/npm/{package}.svg`, and `/chart/json.svg` for inline values or remote JSON series. IMPORTANT: Older bundled snapshots claimed GitHub star-history charts were retired. Current documentation says privacy-safe weekly star history works; confirm on live service rather than repeating that retired claim.

Parameters include `color`, `fill`, `area`, `width`, `height`, `title`, `icon`, `iconColor`, `mode`, `theme`, `font`, `bg`, `border`, `yScale`, `yMin`, `yMax`, `yTicks`, `xTicks`. JSON charts: `values`, `url`, `query`, `dateQuery` where documented. Avoid charting only a single point or fabricated dates.

```sh
python3 scripts/shieldcn_visual.py chart --kind github-issues --repo owner/repo --title 'Issue history' --style presets/white-yellow-outline.json
python3 scripts/shieldcn_visual.py chart --kind github-stars --repo owner/repo --style presets/white-yellow-outline.json
python3 scripts/shieldcn_visual.py chart --kind json --json-url https://example.org/history.json --query '$.history[*].skills' --date-query '$.history[*].date' --style presets/white-yellow-outline.json
```

For repo-specific growth, collect on a schedule into `stats/history.json`. Store real observations only; first day is starting baseline, not project inception. Distinguish account-wide commit charts from a particular repository. Label data freshness and units. Test the remote JSON response, its shape, query expression, and chart SVG before using.
