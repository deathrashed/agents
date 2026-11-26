# ShieldCN visual system — operating guide

Official references: https://shieldcn.dev/docs ; https://shieldcn.dev/docs/api-reference ; https://shieldcn.dev/studio

ShieldCN is an image-rendering API, not a replacement for GitHub README Markdown. Use it for badge images, headers, SVG charts, contributor and sponsor walls. Use Markdown and GitHub-safe HTML for hierarchy and page composition. Use the `shieldcn_visual.py` helper to generate escaped URLs and `<picture>` markup.

## Select a visual

| Need | Choose | Read |
|---|---|---|
| Top-of-page identity | Header banner plus one-sentence tagline | headers-and-banners.md |
| Release/status/technology | Provider or static badge | badge-design-system.md, provider-catalog.md |
| Multiple related indicators | Badge group or separated rows | groups-and-composition.md |
| Trends, not a snapshot | Historical chart | charts-and-visualizations.md |
| Community acknowledgement | Contributors/sponsors SVG | sponsors-and-contributors.md |
| Category totals, local counts | Repository collector + JSON endpoint | dynamic-data-and-metrics.md |
| Section structure | Iconify and explicit anchors | icons-and-logos.md, readme-layouts.md |

Never claim that rendering works without checking the response as an image. Docs change; verify endpoint and parameters against the current live reference if connectivity is available. Start from repository assets and design preferences. Do not turn a text-only project into a dashboard just because endpoints exist.
