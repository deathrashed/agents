# Provider catalog and discovery

Canonical start: https://shieldcn.dev/docs/api-reference and `https://shieldcn.dev/docs`. Provider routes may change and not all third-party badges support every generic styling parameter.

| Provider | Common data | Example endpoint |
|---|---|---|
| GitHub | stars, forks, releases, issues, CI, license, contributors | `/github/stars/owner/repo.svg` |
| GitHub releases | downloads | `/github/downloads/owner/repo.svg` |
| npm | version, weekly/monthly downloads | `/npm/react.svg`, `/npm/react/downloads.svg` |
| PyPI | version/download statistics | check API reference by provider |
| crates.io | crate release/downloads | check API reference by provider |
| Docker Hub | pulls | check API reference by provider |
| skills.sh | installs, rank, trending | `/skills/installs/owner/repo/skill.svg` |
| Custom JSON | project counts / public API values | `/badge/dynamic/json.svg` |
| ShieldCN views | badge fetch count | `/views/repo/owner/repo.svg` |
| Discord/social | members/followers | verify service IDs and support |

When a README uses a service, inspect its package metadata and actual publication status before adding the provider badge. `OWNER/REPO` is not automatically an npm package or a skill listing. If a route is not in the current API reference, treat it as provisional and verify response content instead of generating a confident dead link.
