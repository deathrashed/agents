# Patterns adapted from SenaThenu/readme-forge

Source: https://github.com/SenaThenu/readme-forge (MIT licensed; consulted README and repository tree, November 2026). Project describes a **component-based README generator**, pre-designed block categories, **global variables**, **exportable templates**, live preview, theme switching and Markdown export. Not a motion asset renderer.

Relevant source layout:
- `src/data/md-blocks/{animated-basic,basic,design,github,profile}.json`: block catalog.
- `src/data/md-templates/{default,project,profile,...}.json`: reusable compositions.
- `src/shared/utils/markdownTokenReplace.ts`: global-token substitution.
- `src/shared/utils/exportAsMarkdown.ts`: export.
- `src/forge/components/{AvailableBlocks,UsedBlocks,GlobalsDialog,MarkdownPreview}.tsx`: compositional editor UX.

Adapt the architecture, not the copyrighted implementation: treat hero, badges, navigation, screenshots, animated schematic, metric chart and contributors as independent, reorderable README blocks. Keep project name, palette, links, tagline and logos in one variable source. Prefer matching blocks to verified repository facts. Export clean GitHub-compatible Markdown/HTML. Do not claim the repo implements animation authoring or that its own `animated-basic.json` works outside its editor without inspection.

Prioritize composition: animate one functional diagram, not every block. Quality arises from coherence and specific project detail, not adding more widgets.
