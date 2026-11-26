# Live metrics, counters, badges and charts — any repository

This is a capability of `readme-visual`, not a skills-only recipe. On a README request, identify useful *measurable signals* by reading the actual repository. Make visual summaries that communicate real facts; do not add counters merely to fill space.

## Discovery: inspect before choosing metrics

1. Inspect `git ls-files`, README headings, lockfiles, build manifests, workflows, releases, package publishing, CLI entry points, schemas, configuration defaults, tests, docs, assets, datasets and public service APIs.
2. Propose 3–8 metrics that demonstrate the project's scope, adoption, functionality or maintenance. Explain what a unit means and where it comes from. Examples:
   - **Generic:** files, source lines, supported languages, docs, tests, examples, subcommands, platforms, pipelines, CI jobs, shipped artifacts, integrations, formats, assets, themes, presets, translations, dependencies, API endpoints, database migrations.
   - **Agent tooling:** skills, MCP servers, plugins, rules, prompts, agents, marketplaces, installed packages per machine, installed skill downloads from skills.sh.
   - **Audio/media:** supported codecs, import/export formats, album parsers, metadata actions, fetchers, transformations, presets, documented providers, passing tests.
   - **Apps/UI:** routes/screens, features, keyboard shortcuts, icon packs, UI themes, supported OS builds, modules, extensions.
   - **Packages:** latest versions, package downloads, release assets/downloads, package manager availability.
   - **Operations:** test pass %, coverage (only from coverage reports), latency, throughput, processed items (only when logged), deployments, job success, total schema migrations.
   - **GitHub:** stars, forks, issues, recent commit, releases, release downloads, status, contributions, contributors, repository image fetches.
3. Classify by **source** and **scope**: repository committed state, package ecosystem, external service, local installation, CI/test output, analytics, manual value. Say whether it is instantaneous, cumulative, historical, estimated, or synthetic.
4. Prioritize direct provider badge endpoints for values supported by a published API. Otherwise publish a safe JSON feed with GitHub Actions. Avoid publicizing account secrets, users' machines, detailed home paths, private data or telemetry.
5. For any number that is not verified, explicitly label it example/placeholder. Do not call a local installation count a global skills.sh install count, badge fetches unique visits, or file counts feature counts unless the chosen files genuinely represent features.

## Choices and data contracts

| Need | Approach | Caveats |
| --- | --- | --- |
| Stars, forks, release, CI, download totals | ShieldCN GitHub providers | Verify precise endpoint in current docs |
| Published skills.sh skill installs/rank/trending | `skills/installs/{owner}/{repo}/{skill}` etc. | Only indexed public skill; per skill, not installed machine inventory |
| README image-fetch counter | `/views/repo/{owner}/{repo}.svg` | Requests, not unique users; can increment due to previews/bots |
| Repo-owned counts | `scripts/repo_metrics.py` + configured metric rules | Counts Git-tracked files, not runtime state |
| Metrics from manifests | `json_value` evaluator | Must point at a committed, public numeric JSON property |
| Live external metrics, coverage, releases | Provider API or dedicated collection workflow | Require accurate source/auth/rate limit/caching controls |
| On-device installed counts | opt-in *local* export, aggregates only | Never upload private inventory or machine paths; distinguish machines and deduplicate across devices |
| Growth charts | `stats/history.json` snapshots + `/chart/json.svg` | No historical data before collection begins; daily data points |
| GitHub charts | `/chart/github/stars/{owner}/{repo}.svg`, `/chart/github/issues/...`, `/chart/github/commits/{user}.svg` | User-commit chart is account-wide, not repository commits |
| npm download history | `/chart/npm/{package}.svg` | npm only; use alternative data sources for other registries |

## Generate repository-specific metrics

Use bundled templates as *starting points*, not a copy/paste universal truth:

1. In the target repository, copy skill `scripts/repo_metrics.py` to `scripts/repo_metrics.py`; copy `templates/readme-metrics.example.json` to `.readme-metrics.json`.
2. Modify *every rule* to match the real tracked paths. Remove irrelevant metrics. Inspect `git ls-files` and consider whether file count, unique directory count, regex occurrence count, line count, bytes, or a trusted manifest numeric property is the right measurement. Do not count generated files, vendored copies, symlink aliases or duplicate profile deployments as separate logical resources. Remove `stats/**` from globs.
3. Rule formats:

```json
{
  "metrics": {
    "commands": {"type": "files", "include": ["cmd/*/main.go"]},
    "packages": {"type": "directories", "include": ["packages/**/package.json"], "parent_depth": 1},
    "source_lines": {"type": "lines", "include": ["src/**/*.py", "src/*.py"]},
    "api_routes": {"type": "regex_matches", "include": ["src/routes/*.py"], "pattern": "@app\\.(get|post|put|delete)\\("},
    "integration_count": {"type": "json_value", "path": "stats/public-integrations.json", "key": "integrations.count"}
  }
}
```

`directories` counts parents of matching tracked files. `parent_depth=1` counts the containing directory; adjust when nesting requires. `regex_matches` counts textual matches, not AST entities; use an AST-based dedicated collector if syntax makes regex unreliable. `lines` includes blank lines unless you define a separate collector. `json_value` requires a pre-existing numeric JSON field. Glob matching uses Python `fnmatch` against repo-relative paths: test patterns because `*` and `**` both can match slashes there. In all cases label actual measurement faithfully.

4. Execute from target root:

```bash
python3 scripts/repo_metrics.py --root . --config .readme-metrics.json
cat stats/badges.json
cat stats/history.json
```

5. Copy `templates/readme-metrics.yml` to `.github/workflows/readme-metrics.yml` and configure default branch / paths; on push and daily it updates JSON, committing only when changed. Workflow has `contents: write`; choose least privilege, assess fork protection and repository policies. Actions scheduling can be delayed. Repeated runs on a day replace same day's snapshot; first collection has no retroactive history. Ensure the workflow doesn't trigger itself in a loop.
6. Test on a branch and check generated values against manual counts; audit every HTML anchor and remote badge SVG. Validate action permissions before merging. Add safeguards (error/unknown values should never masquerade as `0`).

## Rendering badge HTML

In target repository, from this skill's `scripts/render_metric_badges.py` (copy it to `scripts/` or execute by absolute path):

```bash
python3 scripts/render_metric_badges.py deathrashed/agents skills plugins scripts rules marketplaces agents
python3 scripts/render_metric_badges.py deathrashed/agents skills plugins --chart
```

The generator emits a README-safe centered `<p>` with per-item `<a><picture><source ...><img ...></picture></a>` and consistent default accent: white outline `ffffff`, yellow icon `ffda00`, white label `ffffff`, yellow value `ffda00`; scheme can be tailored to the user's repository. Generated hrefs point at `#metric-name`; **verify matching README anchors or replace links with real destinations**. For a different default branch, change the `/main/` path in renderer or make a repo-specific generator. Rendered `mode=light` keeps white text by user request and may be unreadable on light GitHub themes: offer a darker adaptive alternative rather than silently violating their visual brief.

Provider example (replace placeholders with existing skill slug):

```html
<img src="https://shieldcn.dev/skills/installs/OWNER/REPO/SKILL.svg?variant=outline&amp;mode=dark&amp;color=ffffff&amp;logo=lu%3ADownload&amp;logoColor=ffda00&amp;labelTextColor=ffffff&amp;valueColor=ffda00" alt="Published skill installs">
```

Static numeric badge vs dynamic JSON:

```
https://shieldcn.dev/badge/Tests-120-ffffff.svg?variant=outline&logo=lu%3AFlaskConical&logoColor=ffda00&labelTextColor=ffffff&valueColor=ffda00
https://shieldcn.dev/badge/dynamic/json.svg?url=PUBLIC_JSON_URL&query=%24.tests&label=Tests&variant=outline&mode=dark&color=ffffff&logo=lu%3AFlaskConical&logoColor=ffda00&labelTextColor=ffffff&valueColor=ffda00
```

URL-encode the nested `url` parameter and JSONPath via `urllib.parse.urlencode` (the generator does this). HTML-escape query `&` as `&amp;`. `labelTextColor` affects label; `valueColor` affects the numeric text in outline badges. `split=true` may visually fill sections; only enable after previewing with the selected theme. Badges must be scoped and linked to meaningful headings, repo pages, or documentation.

## Charts

- **Instant GitHub**: `https://shieldcn.dev/chart/github/stars/OWNER/REPO.svg`; similarly `chart/github/issues/OWNER/REPO.svg`. `chart/github/commits/USER.svg` charts *user lifetime* activity. These are not invented per-repository commit charts.
- **Live project history**: generate `stats/history.json` with `repo_metrics.py`, and use `/chart/json.svg?url=...&query=$.history[*].skills&dateQuery=$.history[*].date&color=ffda00&bg=transparent&mode=dark&title=Skills%20Growth`. `query` and `dateQuery` MUST return parallel arrays. The chart generator demonstrates URL encoding.
- **One metric per chart** unless current docs confirm multi-series support; for multiple categories produce separate charts or create static SVG using actual daily data, committing the file. Static SVG can be generated in CI, still updating daily.
- **No fabricated trend**: not enough snapshots means show current counts until history accumulates; never manufacture earlier datapoints. Charts of test results or benchmarking require stable environment and known collection conditions.

## Operating system installed counts

Repository metrics only see Git-tracked artifacts. For local installed tools, count via local commands or lockfiles **on each machine**. Obtain opt-in before exporting; only send aggregate JSON such as `{"machines":{"cachyos":12,"macos":9},"total_unique":17}` after deduping on logical package IDs. If there is no cloud collection mechanism and user did not authorize publishing, explain the gap and leave count local. Public skills.sh install counts are completely different.

## View counters and limitations

```
https://shieldcn.dev/views/repo/OWNER/REPO.svg?variant=outline&mode=dark&color=ffffff&logo=lu%3AEye&logoColor=ffda00&labelTextColor=ffffff&valueColor=ffda00
```

This counts image render requests (bots/caches included), not unique repository visitors. Do not claim zero setup implies unique visitor analytics or reliable traffic history. If a true traffic analytics metric is requested, use GitHub Traffic API with permissions and retention constraints, or a trusted analytics provider, with privacy and rate-limit safeguards.

## Deeper, repo-specific collectors

For counts that basic patterns can't derive reliably, create a small self-contained collector that reads the project's *actual* canonical data and writes numeric `stats/public-*.json`, then include it as an upstream action step before `repo_metrics.py`. Examples: introspect a CLI's `--help --json`, parse a typed manifest, read test report XML/coverage JSON, count supported platforms in release manifest, parse generated schema endpoints, extract package versions, summarize static datasets, or query APIs with tokens supplied as GitHub Actions secrets. Never install/run untrusted dependencies merely to make a badge. Keep failure states visible: do not replace failing external API stats with fictitious zeros.

## Validation checklist

- [ ] Badge proves a useful repo fact, not decoration
- [ ] Each metric specifies counting rules, source, scope and last update
- [ ] Count is checked against actual files or API
- [ ] Historical chart data accumulated honestly; no fake backfill
- [ ] Values are not misrepresented (download vs installs vs unique users)
- [ ] External endpoints verified current with docs; icon names render
- [ ] Workflow permission minimal; no secrets in output
- [ ] No recursive workflow commits or public local inventory leaks
- [ ] Dynamic URLs URL-encoded and HTML escaped; `source` and fallback `img` present
- [ ] README section anchors and badge click targets exist
- [ ] Contrast checked for both GitHub themes
- [ ] Badge sets compact, grouped by meaning, not an overwhelming scoreboard

## Current reference pages

- https://shieldcn.dev/docs/api-reference
- https://shieldcn.dev/docs/badges/dynamic-json
- https://shieldcn.dev/docs/badges/skills
- https://shieldcn.dev/docs/charts

Check these live when connectivity is available; bundled copies are reference snapshots and may be stale.
