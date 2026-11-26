# Custom shieldcn badge gallery

Everything here is built with `scripts/shieldcn_badge.py` (adaptive light/dark pair by default). Raw URLs
shown for reference. All examples were fetched and return `image/svg+xml`; the ones marked (R) were rendered
and looked at.

## Two things to know before styling

1. **Outline/ghost/secondary badges draw their label in the reader's foreground colour.** A single
   `mode=dark` image has white label text, so on GitHub's light theme the label disappears (seen on the
   "Runs on" and "Claude" badges). Always ship `mode=light` + `mode=dark` in a `<picture>`, or pick a filled
   variant with an explicit `color`.
2. **`brand=` only knows some brands.** It recolours the badge and logo for: python go rust docker github npm
   typescript react svelte bun cplusplus postgresql sqlite redis vercel openpanel anthropic openai discord
   youtube homebrew vscode gitlab. For anything else (tauri, windows, linux, apple, node, java, swift, ...)
   it does nothing: give `color=` and `logo=` yourself, or use `--platform` for operating systems.

## Patterns (the owner's examples)

| Intent | Command | Notes |
|---|---|---|
| Two-part "Runs on" badge (R) | `--label "Runs on" --message Linux --platform linux --variant outline` | `Runs%20on-Linux-FCC624`, logo `linux`, logoColor `f1be1c` |
| Dark filled platform badge (R) | `--label "Runs on" --message MacOS --color 000000 --logo apple --logo-color ffffff --mode light` | looks identical in both themes |
| Brand outline with custom value colour (R) | `--message Python --brand python --variant outline --value-color ffff --logo-color f1be1c` | `brand=python` gives the blue border and yellow logo |
| Brand-filled (R) | `--message Go --brand go --variant branded` | go cyan; Rust renders black with a white gear |
| Brand badge, other service | `--label analytics\ by --message OpenPanel --color 2564EB --logo openpanel --variant outline --brand openpanel` | |
| Tool badge with explicit colour (R) | `--label Claude --message Code --color D97757 --logo anthropic --variant outline` | name split into label + message |
| Live provider, outline, bigger | `--provider npm/license/react --variant outline --size default` | |
| Joined group (one image) | `--group npm/react github/stars/vercel/next.js github/ci/vercel/next.js github/license/vercel/next.js --theme zinc` | rows that share one link |
| Branded overview group | `--group npm/react github/stars/vercel/next.js github/license/vercel/next.js --variant branded` | |
| Outline trio, slate theme | `--group github/stars/OWNER/REPO github/forks/OWNER/REPO github/license/OWNER/REPO --variant outline --theme slate` | |

## Patterns from the owner's READMEs (read on 2026-11-22)

| README | What it does | Take from it |
|---|---|---|
| lastfm-scrobbler | shields.io `style=for-the-badge`, brand logo, **one accent on every badge** (`f8211c`, Last.fm red), `logoColor=white`; a missing logo comes from `custom-icon-badges.demolab.com` (the WTFPL badge) | When the project has a strong brand colour, paint every badge in it |
| wikimedia | shieldcn `variant=outline`, two-tone: label colour in the path, value `color=006699`, `valueColor=ffffff`, `labelTextColor=ffffff`, `logoColor=ba1919`, icons from `ri:` sets and brand slugs (`wikipedia`, `wikimediacommons`) | Two-tone badges that echo the logo's two colours |
| perkolator | shieldcn `variant=outline&theme=emerald`, real tool logos (`rust`, `kde`, `wayland`, `apple`) with `logoColor=ffffff`, `mode=auto` | One theme, brand logos, a row that doubles as a compatibility list |

The accent comes from the repo's logo or icon; with none, ask the owner. Headers are dark in all three
(a PNG, a custom SVG card on `#09090b`, a shieldcn `mode=dark` grid).

## Custom ones: levers

| Want | Parameter |
|---|---|
| exact surface colour | path colour segment (`Runs%20on-Linux-FCC624`) or `color=` |
| value text colour / label text colour / label opacity | `valueColor` / `labelTextColor` / `labelOpacity` |
| icon | `logo=<simple-icons slug>`, `logo=ri:Name`, `logo=data:image/svg+xml;base64,...`, `logo=false` |
| icon colour | `logoColor=<hex>` (bare hex, `%23` also accepted) |
| gradient fill | `gradient=ff6b6b,4ecdc4,135` |
| animation | `animate=pulse|glow|shimmer` (SVG only; sparingly) |
| status dot | `statusDot=true` |
| two-tone label/value | `split=true` (soft, use for status/data pairs) |
| size / font | `size=xs|sm|default|lg`, `font=inter|geist|geist-mono|jetbrains-mono|fira-code|roboto|space-grotesk` |
| fine tuning | `height fontSize radius padX iconSize gap labelGap` |
| shadcn accent | `theme=zinc slate blue green rose orange violet purple cyan emerald` |

Dashes in labels/messages are doubled (`foo--bar`) in the path; spaces become `%20`. `scripts/shieldcn_badge.py`
does both.

## Live providers worth using in READMEs

github (stars forks license release ci issues open-prs contributors last-commit watchers dt), npm, pypi,
crates, docker, jsr, homebrew, maven, packagist, rubygems, nuget, pub, cocoapods, codecov, discord, reddit,
bluesky, youtube, mastodon, hackernews, vscode, wakatime. Full list: `~/.agents/skills/shieldcn-badges/SKILL.md`
and https://shieldcn.dev/docs. Private repos: `github/*` endpoints do not work for repos the badge service
cannot read.

## Other custom assets

- Header banners: `scripts/generate-header.py` (presets dots, graph, grid, gradient, glow, surface, transparent).
- Charts: `/chart/npm/{pkg}.svg`, `/chart/github/issues/{o}/{r}.svg`, `/chart/github/commits/{user}.svg`,
  `/chart/github/stars/{o}/{r}.svg`, `/chart/json.svg?values=...` (build with `shieldcn_badge.py --provider chart/...`).
- Contributor and sponsor walls: `/contributors/{o}/{r}.svg`, `/sponsors/{login}.svg`.
- Anything else: build the URL in README Studio (https://shieldcn.dev/studio) or the badge/header generators
  (https://shieldcn.dev/gen, https://shieldcn.dev/header), then paste it through `validate-readme.py --online`.
