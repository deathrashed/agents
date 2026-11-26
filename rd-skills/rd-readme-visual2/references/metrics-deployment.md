# Deploying repository metrics safely

Metrics live in the **target repository**. Nothing in the skill's templates updates a README automatically until installed.

## Install and customise

From anywhere, run:

```bash
python3 /path/to/readme-visual/scripts/install_metrics.py /path/to/target-repo
```

The bootstrap copies the metrics collector to `scripts/repo_metrics.py`, an editable configuration to `.readme-metrics.json`, and the workflow to `.github/workflows/readme-metrics.yml`. It does **not** overwrite files unless `--force` is passed. It does not change `README.md`. Use `--dry-run` to inspect destinations.

Edit `.readme-metrics.json` to reflect actual tracked paths. The examples count files/manifest values, **not** conceptual features. Remove irrelevant metrics and categories. Commit the config and workflow, then run `python3 scripts/repo_metrics.py --config .readme-metrics.json` from the target repository root. Inspect `stats/badges.json` and `stats/history.json` before publishing. History starts on the first run; old dates are never invented.

The workflow runs on push, manual dispatch and daily schedule, and commits changed JSON only. The target repository must allow workflow `contents: write` permissions and must have a `main` default branch, or the copied workflow must be changed to match its branch. For large repositories, tune file patterns to avoid scanning irrelevant generated code.

## Build badges

```bash
python3 /path/to/readme-visual/scripts/render_metric_badges.py OWNER/REPO skills plugins rules
```

Use only keys present in the generated JSON. Verify every `#` anchor in the HTML; replace nonexistent anchors with real documentation URLs or relevant paths.

## Sources and limitations

- ShieldCN view badge counts requests to its image endpoint, not unique visitors.
- `skills.sh` installation badges count published skills under a specific indexed slug; they are not local inventories.
- Local installations on macOS/Linux require an explicitly configured local export and safe public aggregate reporting. Never publish lockfiles, usernames, personal paths or secrets.
- Remote chart series require data shaped for the endpoint's JSON query; confirm it against actual generated `stats/history.json`.
- GitHub's image caching can make values appear stale even after JSON updates.
- External API endpoints, especially GitHub and ShieldCN-specific routes, must be tested against current provider documentation.

## Test and rollback

Run the local collector twice on the same day; there must remain exactly one snapshot for that date. Check the generated JSON and the output of the HTML renderer. On failure, inspect GitHub Actions logs, repo write permissions, missing config paths, and the branch name. Remove the generated workflow and JSON files to disable publication; do not remove existing unrelated stats.
