# Validate generated assets and broken links

Run existing `scripts/validate-readme.py` and new `scripts/audit_visual_assets.py`. For remote verification add `--remote`, respecting rate limits. Then inspect actual SVGs visually in a browser and preview README on GitHub.

| Symptom | Likely cause | Action |
|---|---|---|
| Blank heading icon | Wrong Iconify namespace, missing icon, external outage | Test URL returns SVG, replace/copy locally |
| Full coloured badge not outline | Split + background overrides affecting surfaces | Remove `split=true` or set/test distinct label background |
| White text vanishes | Forced white in light theme | Different light mode colours |
| Badge links do nothing | Bad `href="#..."` target | Add explicit `<a id="...">` before heading |
| `&amp;` visible in request | Double-escaped URL | Escape once in HTML attributes only |
| Chart is empty | Unsupported route, wrong JSONPath, one point, API failure | Test raw JSON and query; check source doc |
| Live count is stale | API/Cloudflare/GitHub caches or scheduled job | Report cache and last updated date |
| Image 200 but broken | Service returned HTML/JSON rather than image | Check body signature/content-type |
| Viewer counter is surprising | Measures badge fetches, not unique users | Relabel or remove misleading claim |

Never silently assume a template works. Check repo file paths, links, alt, source accuracy, colour contrast, and mobile layout. Distinguish unresolved from verified failures.
