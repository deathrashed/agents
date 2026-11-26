# README layout patterns

1. **Minimal CLI:** small wordmark, one-line tagline, install command, two badge rows, usage examples and clear docs link.
2. **Developer library:** title, version/platform/CI badges, 10-line quick start, API examples, compatibility and releases.
3. **Desktop UI:** branded hero, actual screenshots, supported OS badges, install matrix, controls, troubleshooting.
4. **AI/agent toolkit:** workflow diagram, integrations, agent/skill/plugin counters (if verified), source policies, examples.
5. **Data-heavy project:** concise intro, real metric legend, one growth chart, downloadable data, methodology.
6. **Portfolio/documentation:** subdued banner, rich navigation, projects/cards, contributor/community area.

Arrange as header > tagline > high-signal badges > local navigation > getting started > visual proof > detailed sections > maintenance/community. The hierarchy reflects developer decision-making, not endpoint availability. Put charts lower unless the project itself is an analytics product.

For a fully composed draft, edit `templates/hero.example.json` and run `scripts/compose_readme_hero.py`. It emits a fragment to review, not an automatic in-place overwrite. Existing commands and screenshots remain source of truth.
