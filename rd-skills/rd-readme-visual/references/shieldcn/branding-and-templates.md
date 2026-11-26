# Branding and templates

1. Inspect actual project assets and any explicit colour preferences.
2. Create a palette with background, foreground, border, accent and secondary text; verify contrast in light/dark.
3. Use `presets/*.json` to hold shared ShieldCN query values. Avoid repeating conflicting inline colour values across multiple URLs.
4. Choose a visual density and type scale appropriate to repository type.
5. Generate a hero from `templates/hero.example.json`, then inspect generated markup and GitHub preview.
6. Reuse the project's exact current name and logo. Don't convert a graffiti mark into corporate-style iconography unless requested.
7. Keep informative content out of externally hosted decorative graphics when essential text can remain selectable Markdown.

Colour system is portable: change `presets/white-yellow-outline.json` for another repository without rewriting Python. For local images, preserve licensing and source metadata. Do not rename existing files unless requested.
