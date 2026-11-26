# Icons, logos and section-heading icons

ShieldCN `logo=` accepts recognized Simple Icons slugs, `ri:...` or `lu:...` icon identities (where supported), and custom logo methods described by official docs. Iconify URL syntax for README headings is `/COLLECTION/NAME.svg?color=%23HEX`, e.g. `https://api.iconify.design/lucide/terminal.svg?color=%23ffda00`.

- Main H2 headings: 20–24px icon, primary accent.
- H3 subheadings: 14–18px, contrasting neutral icon (white on dark; dark on light).
- Decorative icons in headings: `alt=""`; text heading remains accessible.
- Always use explicit anchors before icon-bearing headings because inferred GitHub slugs can vary.
- Prefer topic-specific icons: `package-check` installation, `terminal` CLI, `settings` config, `shield-check` authentication, `history` recovery, `database` persistence, `chart-no-axes-combined` statistics.
- Treat unconfirmed names like `ri:BsRobo` as candidates, not guaranteed API-valid icons; test via HTTP + SVG body inspection.

Critical images (project identity, logos, many repeated heading icons) should be vendored into `assets/` when stable delivery matters. Iconify availability and GitHub proxy caching can diverge from local preview. Source the icon/mark's license and do not blindly recolor third-party brands when trademark rules prohibit it.

Example markup is in `templates/heading-icons.example.md`.
