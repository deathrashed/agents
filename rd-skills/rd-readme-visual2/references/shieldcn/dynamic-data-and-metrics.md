# Dynamic data and repository metrics

See existing `references/live-metrics-badges-charts.md` for the generic inventory engine, historical snapshots and GitHub Actions workflow. This file focuses on visual integration.

- Provider-backed: GitHub stars, releases, CI, issues, package versions/downloads, and skills.sh installs/ranks when indexed. Prefer these over a custom scraping job.
- Repo-backed: tracked file totals, commands, format support, tests, configs, rules and plugin definitions. Count things with a collector *adapted to this repo*; do not infer product capabilities solely from directory names.
- Machine-backed: installed skills/plugins or platform-specific state must be measured on those machines and exported intentionally. GitHub Actions cannot inspect `~/.local/state` on a Mac or CachyOS machine.
- Public JSON-backed: `/badge/dynamic/json.svg?url=...&query=$.skills&label=Skills`. Host JSON at a public stable URL. Avoid raw private API tokens, local paths, personal details and query secrets.
- View-backed: `/views/repo/{owner}/{repo}.svg`. Badge fetch count is not true unique human visitors, and caching reduces correspondence to page views.

Publish daily history with date and counters (counts can rise or fall). Document sampling interval, unit, source, caching, and missing-data behaviour. A generated badge must not show 0 to cover an API error; show unavailable or retain last known good values with disclosure.
