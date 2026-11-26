---
name: rd-readme-visual2
description: Create, restyle, extend, or audit visually distinctive GitHub READMEs with verified documentation, project-specific design, authentic screenshots and demos, accessible diagrams, badges, and optional sourced metrics. Use for README visual redesign, repository documentation, README media, banners, or documentation audits.
---

# README Visual

Create an accurate, useful README with a visual identity belonging to the project. Preserve correct information and existing work. Choose the smallest structure and visual treatment that serve its readers; the bundled visual recipes are options, not a universal template.

Paths below are relative to this skill directory, not the target repository. Resolve the skill directory first and use absolute script paths when working elsewhere. The bundled references and tools remain available when this folder is moved.

## Workflow

1. **Scope.** Identify whether the request is creation, restyling, a section or asset, metrics, or an audit. Audit-only means report findings; do not edit without authorization. Preserve wording and working links in visual-only restyles.
2. **Inspect.** Read the existing README, relevant entry points, manifests, documentation, license, tests, and visual assets. Establish the reader's first successful action, supported platforms, commands, dependencies, and claims supported by evidence. Read `references/audit.md` for audit or restyle work.
3. **Design.** Derive a palette and visual grammar from the project's actual interface, assets, domain, and user preferences. Choose useful sections, navigation, media, and density for this project; do not require a centred hero, icons, badge row, tree, animation, or dropdowns on every README. `references/section-menu.md`, `references/local-visual-archetypes.md`, and `references/motion/art-direction.md` offer choices. The terminal-window aesthetic in `references/pipeline.md` is optional, not a mandatory template.
4. **Make.** Verify commands, versions, flags, paths, links, feature claims, and examples against the project. Prefer authentic captures to represent behavior; label illustrations as illustrations and use real architecture and data. Do not fabricate screenshots, metrics, history, or benchmarks. Avoid exposing secrets, private paths, usernames, or personal data. Retain license and attribution requirements for third-party assets.
5. **Verify.** Run appropriate commands and check anchors, links, image responses, alt text, and media. Inspect actual rendered output where feasible, including narrow and light/dark views, animation frames, and reduced-motion/static fallbacks when relevant. `scripts/validate-readme.py` and `scripts/check-media.py` help identify issues; style warnings are judgment calls, not mandatory layout. Test generated workflows and data locally before proposing publication. Report unavailable tools, external services, or GitHub rendering as unverified.
6. **Deliver.** Return the requested README, assets, or evidence-backed audit; summarize meaningful decisions and checks. Do not commit, publish, overwrite unrelated files, install tools, or enable write-capable automation without authorization.

## References and tools

Read the relevant material only. Some legacy references describe Riley's personal aesthetic or a required skeleton; the user's request and this skill's project-specific selection take precedence. Check tool availability and use each script's `--help` before use.

| Task | Resources |
| --- | --- |
| Writing, structure, navigation, accessibility | `references/writing.md`, `references/formatting.md`, `references/structure-and-links.md` |
| Review, cold-reader test | `references/audit.md`, `references/interview.md` |
| Shields, branding, icons and visual layouts | `references/shieldcn/`, `references/shieldcn-recipes.md`, `references/icons-and-shields.md`; `scripts/shieldcn_visual.py`, `scripts/generate-badge-row.py`, `scripts/compose_readme_hero.py` |
| Real screenshots and recordings | `references/media.md`, `references/motion/animated-demos.md`; `scripts/make-tape.py`, `scripts/record.sh`, `templates/demo.tape.tmpl` |
| Optional dark terminal header and flow map | `references/pipeline.md`, `references/flow-example.json`; `scripts/palette.py`, `scripts/header.py`, `scripts/flow.py` |
| Original illustrations and motion | `references/motion/animated-svg-design.md`, `references/motion/motion-design-recipes.md`, `references/motion/dynamic-svg-generation.md`; `scripts/generate_motion_svg.py`, `scripts/render_motion_frames.py`, `scripts/check_motion_svg.py` |
| Metrics and charts | `references/live-metrics-badges-charts.md`, `references/metrics-deployment.md`, `references/shieldcn/dynamic-data-and-metrics.md`; `scripts/install_metrics.py`, `scripts/repo_metrics.py`, `scripts/render_metric_badges.py` |
| Asset reliability | `scripts/audit_visual_assets.py`, `scripts/cache_visual_assets.py`, `templates/visual-checklist.md` |

The optional `scripts/license-snippet.py` and license-specific validator matching use Riley's external gupload license library; the snippet tool accepts `--root`. If that library is unavailable, use the target repository's actual LICENSE instead. Recording and image-generation tools also require their respective external programs.

## Media and metrics safeguards

Use real program output for demonstrations; show static illustrations only as illustrations. Use self-contained SVGs and readable first frames; honor reduced motion and supply a static alternative where animation is not reliable. Check actual output frames and GitHub compatibility instead of assuming a successful command produced usable media. Respect theme contrast and accessible names; decorative icons can have empty alt text.

Only add meaningful, sourced badges or metrics. A file count is not a feature count, published installs are not local installations, and image requests are not unique visitors. Never fabricate historical data. For custom metrics, inspect `scripts/install_metrics.py --dry-run` and target paths, adapt its config and branch, and inspect generated JSON before any publication. Its workflow writes repository contents; enabling or publishing it requires explicit authorization. Verify provider endpoints and account for caching and network availability.

## Quality gate

The reader can identify what the project does and how to use it; edited claims are evidenced; media and links are inspectable; no sensitive data is exposed; and any remaining unverified behavior is reported. Never force decorations or hide real validation failures to satisfy an aesthetic checklist.
