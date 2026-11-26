# Asset management and repeatable rendering

- Use SVG for high-DPI badges/headers; PNG fallback only if a renderer blocks SVG.
- Render remote URLs with `curl -fL` and check `Content-Type` plus image signature. HTTP 200 can still be an HTML error page.
- For critical images, download approved public assets to `assets/readme-external/` with `scripts/cache_visual_assets.py`, inspect the files, then use `--apply` deliberately. Avoid copying logos without license checks.
- Keep original source URL and attribution in documentation when appropriate. Never expose private or secret-bearing URLs in a public README.
- Image proxies and caches can retain stale versions; a parameter change may not immediately purge every GitHub proxy cache.
- Don't use animated SVG if GitHub's image proxy or renderer disables the animation. Provide a static alternative.

```sh
python3 scripts/audit_visual_assets.py README.md --remote
python3 scripts/cache_visual_assets.py README.md
python3 scripts/cache_visual_assets.py README.md --apply
```

`cache_visual_assets.py` purposefully limits downloads and does not rewrite the README without `--apply`. Review `git diff` after using it.
