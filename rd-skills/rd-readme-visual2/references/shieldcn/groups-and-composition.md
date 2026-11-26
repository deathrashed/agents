# Badge groups and composition

Docs: https://shieldcn.dev/docs/badges/group

Join endpoint paths with `+`: `/group/github/stars/owner/repo+github/forks/owner/repo.svg?variant=outline`. Query parameters apply globally to grouped segments. Groups are a *single image* with one clickable destination, so use individual badges if the segments need different links.

```sh
python3 scripts/shieldcn_visual.py group --segments github/stars/owner/repo github/forks/owner/repo --style presets/white-yellow-outline.json
```

Suggested composition: row 1 language/release/license; row 2 real category statistics; row 3 OS/platform and contribution/status; chart only when useful. Prefer 3–6 high-signal items above fold. Use `<p align="center">` containers for distinct rows. A literal line break within one paragraph may be reflowed by GitHub; use separate `<p>` elements.

Use *one badge per category*, not duplicated labels with inconsistent counts. If a badge is dynamic, title/alt should describe its measurement. Avoid combining counts that do not share a source or time horizon.
