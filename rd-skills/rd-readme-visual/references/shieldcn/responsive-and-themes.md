# GitHub responsive layout and themes

GitHub READMEs allow Markdown and a subset of sanitized HTML, not arbitrary CSS/JS. Use `<p align="center">`, Markdown tables, HTML tables, `<picture>` and SVG assets. No viewport-based JS interactivity, CSS media queries embedded in the README, or remote script elements.

Adaptive image pattern:

```html
<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/header/graph.svg?title=Sample&amp;mode=dark">
  <img alt="Project banner" width="100%" src="https://shieldcn.dev/header/graph.svg?title=Sample&amp;mode=light">
</picture></p>
```

White-on-transparent often disappears in GitHub's light theme. Provide an actually contrasting light source, not only `mode=light` with forced white. When the user explicitly insists on identical white/yellow for both, explain light-mode contrast tradeoff. Use `width="100%"` for a wide banner and choose a sensible aspect ratio; avoid huge text baked into tiny badge images. Use meaningful alt for content imagery and empty alt for decorative icons. Inspect mobile (320–390px) and desktop renders.
