# Dynamic SVG from real data

**Animated** SVG changes by time; **dynamic** SVG changes when data is regenerated. Keep the distinction explicit.

Data pipeline: repo files / tests / release API / public JSON → validated facts → deterministic layout → generated SVG → committed asset → README image. Re-run on relevant push, release, or schedule. A generated SVG is stale until the workflow updates it; it is not a client-side live dashboard.

Recommended stored artifact layout:
```
assets/readme/architecture.svg
assets/readme/architecture-static.svg
stats/readme-metrics.json
.github/workflows/update-readme-media.yml
```

If SVG labels derive from untrusted repositories or JSON: XML-escape text, limit lengths, validate colours, reject scripts and external references. For data points, encode timestamps and source provenance, avoid invented historical backfills, and never expose secrets. Persist a static image where possible. If the workflow can fail, keep last known good generated image instead of committing a broken placeholder.

Regenerate only deterministic content; use fixed seeds and stable sorting. Record provenance in adjacent text/JSON, not false visual claims. Validate with `scripts/check_motion_svg.py`. For raw repo metrics use existing `scripts/repo_metrics.py`; for ShieldCN JSON badges use existing references under `references/shieldcn/`.
