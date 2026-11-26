# shieldcn: complete reference for the agent

Authoritative text of the docs lives in `shieldcn-docs/` (fetched 2026-10-15 from https://shieldcn.dev/docs/*).
This file is the working summary. Anything not listed here: read the matching `shieldcn-docs/*.txt` or
https://shieldcn.dev/docs, then build the URL with `scripts/shieldcn_badge.py` / `scripts/generate-header.py`
(`--param KEY=VALUE` reaches every option).

## URL anatomy

```
https://shieldcn.dev/{provider}/{...params}.svg            image (default; crispest)
.../{...}.png                                              raster, only where SVG is blocked
.../{...}.json                                             resolved data {label,value,color,link}
.../{...}/shields.json                                     shields.io endpoint schema (schemaVersion 1)
```

Query parameters apply to every endpoint; badge groups apply one set to all segments.

## Appearance and colour parameters (all badges)

| Param | Values |
|---|---|
| `variant` | default secondary outline ghost destructive branded |
| `size` | xs sm(default) default lg |
| `mode` | dark(default) light |
| `theme` | zinc slate blue green rose orange violet purple cyan emerald (and others in docs) |
| `font` | inter geist geist-mono jetbrains-mono fira-code roboto space-grotesk |
| `color` `labelColor` `valueColor` `labelTextColor` `labelOpacity` | hex without `#`, or named colour; opacity 0-1 |
| `gradient` | hex stops, optional trailing angle: `ff6b6b,4ecdc4,135` (not in groups) |
| `logo` | SimpleIcons slug; `ri:FaReact` (React Icons); `lu:Rocket` (Lucide); `data:image/svg+xml;base64,...`; remote `https://` image; `false` |
| `logoColor` | hex, or `brand` to paint a SimpleIcon in its brand colour |
| `brand` | python go rust docker github npm typescript react svelte bun cplusplus postgresql sqlite redis vercel openpanel anthropic openai discord youtube homebrew vscode gitlab (others: no effect) |
| `label` `split` `statusDot` | override label; two-tone label/value (not in groups); status dot (auto for CI) |
| `animate` | pulse glow shimmer; SVG-only, CSS keyframes (works on GitHub); pulse/glow need a status dot |
| fine tuning | `height fontSize radius padX iconSize gap labelGap` |

Outline/ghost/secondary draw text in the reader's foreground colour: ship `mode=light` and `mode=dark`
in a `<picture>` pair (default for the scripts). Colour-locked badges (explicit `color`) can stay single.

## Static badge `/badge/{label}-{message}-{color}.svg`

Dashes separate label, message, colour. `_` or `%20` = space, `__` = literal `_`, `--` = literal `-`.
Named colours: brightgreen green yellow orange red blue purple violet grey lightgrey, or any hex.
One segment (`/badge/Python.svg`) is a message-only badge.

## Dynamic JSON `/badge/dynamic/json.svg?url=<https url>&query=<JSONPath>`

`query` supports `$.key`, `$.nested.key`, `$.array[0]`, `$.array.length`; `prefix`, `suffix`, `label` optional.
URL-encode `url` and `$`. Cached 5 minutes.

## HTTPS endpoint `/https/{host}/{path}.svg`

Fetches `https://{host}/{path}` and expects JSON `{"label":"..","value":"..","color":".."}` or badgen's
`{"subject","status","color"}`. Cached 5 minutes. Use to wrap any service (own Worker, RunKit, Vercel).

## Group `/group/{a}+{b}+{c}.svg`

One joined image (shadcn ButtonGroup). Each segment is a normal path (`npm/react`, `github/stars/o/r`);
query applies to all; max about 5 segments; no `split`, no `gradient`; per-segment overrides unsupported;
`variant=branded` uses each provider's brand colour.

## Live providers (selection)

github `stars forks license release ci issues open-prs contributors last-commit watchers dt dependabot downloads views`
(`/github/{topic}/{owner}/{repo}` or `/github/{owner}/{repo}/{topic}`; `ci?workflow=name&branch=main`),
npm (`/npm/{pkg}`, `/npm/dw|dm|dy|dt|license|node|types|dependents/{pkg}`), pypi, crates, docker, jsr,
bundlephobia, homebrew (`/homebrew/{formula}`, `/cask/...`, `dm|dq|dy`), maven, packagist, rubygems, nuget,
pub, cocoapods, codecov, discord, reddit, bluesky, youtube, mastodon, hackernews, vscode, wakatime, tokscale,
skills.sh (`/skills/{o}/{r}/{skill}`, `rank trending hot`), views (`/views/repo/{o}/{r}`, stateful, `?base=N`),
x (`/x/follow/{user}`), nba, country flags (`/flag/{iso2}`, 265 codes, e.g. `gb-eng`), plus gitlab, conda,
chrome web store, AMO, coveralls, sonarqube, jsdelivr, chocolatey, flathub, snapcraft, f-droid, discourse,
stack exchange, modrinth, open vsx, liberapay, matrix, weblate. Full: `~/.agents/skills/shieldcn-badges/SKILL.md`.
GitHub-backed endpoints cannot read private repos.

## Charts (`/chart/...`)

`github/stars/{o}/{r}` (privacy-safe weekly history, works again; `.png` and `.json` too),
`github/issues/{o}/{r}`, `github/commits/{user}` (multi-user compare), `npm/{pkg}` (`days=`), `json.svg?values=1,2,3`
(`dates`, `labels`), `json.svg?url=..&query=..`. Params: `theme font color fill area width height title icon
iconColor mode bg border yScale yMin yMax yTicks xTicks`. Use only when the trend tells a story.

## Headers `/header/{preset}.svg` (or `/header.svg` = surface)

Presets: surface gradient dots grid graph glow transparent. Sizes: banner 750x260 (default), wide 1280x400,
social 1280x640, square 640x640, or `width` 240-2400 / `height` 100-1600. Params: `title subtitle logo logoColor
size width height align(center|left) bg(hex|transparent) gradient glow accent titleColor subtitleColor radius(0-120)
border watermark pattern(dots|grid|graph|none) theme font mode`; photo backgrounds `image overlay tint`.
Your own logo: `logo=https://...png` or a `data:` URI (builder/Studio encode uploads into the URL).
Rendered on demand, never rate-limited; remote logos cached 24h.

## Walls

`/contributors/{o}/{r}.svg` (`limit min names size width align titleAlign bots title`, plus the header
background system), `/sponsors/{login}.svg` (`special backers specialTitle sponsorsTitle backersTitle title size
width limit names`). Both accept `.png` and `.json`. Put below the intro, not in the badge row.

## Adaptive light/dark

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="...&mode=dark" />
  <img alt="..." src="...&mode=light" />
</picture>
```
Wrap in `<a href>` for clickable badges. Studio's "Adaptive" toggle and the CLI's `--theme-aware` do the same.

## shieldcn CLI (`npx shieldcn-cli`)

Scans the local repo (or `owner/repo`, GitHub URL) for stack signals and prints badge Markdown: GitHub, Package,
Tooling (lockfiles, configs), Stack (100+ dependency mappings), Modern (ESM, monorepo...).
`--variant --size --theme --mode`, `--theme-aware`, `--compact`, `--format flat|html`, `--json`, `--copy`.
`init` adds `<!-- shieldcn-start -->` / `<!-- shieldcn-end -->` markers; `--inject` rewrites between them
(good for CI with git-auto-commit). `migrate [file] [--dry] [--write]` converts shields.io URLs
(`flat-square`->secondary, `for-the-badge`->default, `social`->ghost, `plastic`->outline; logo/colour params
carry over; `labelColor` carries but gives split-like looks). It targets npm projects: for Rust/Go/Python
repos use the scripts here instead.

## README Studio (https://shieldcn.dev/studio)

Visual README builder: blocks Text, Header, Badges, Group, Chart, Table, Image; live preview; `Adaptive`
export; paste Markdown back in to edit. Point the owner there for a whole-README redesign.

## shields.io -> shieldcn mapping

`?style=flat-square`=`variant=secondary`, `for-the-badge`=`variant=default`, `social`=`variant=ghost`,
`plastic`=`variant=outline`; `logo`, `logoColor`, `color` unchanged; `labelColor` is accepted but produces a
two-tone look (the owner's classic shields.io style, see `shieldcn-recipes.md` fallback).
