# Terminal-window recipe: a reproducible README visual pipeline

How the `rd-agents` README was built, generalised so it works for any repo, logo and colour scheme. It
produces: a dark terminal-window banner with the owner's wordmark, a real terminal recording, an animated
hub-and-spoke map, owner-styled badges with real counts, accent-coloured heading icons. Everything is
regenerable from scripts in this skill; nothing is hand-drawn per repo.

Related: `media.md` (formats, GitHub rendering, motion craft, creative recipes), `shieldcn/` (badge system),
`../SKILL.md` §4-§7. If another reference conflicts with the owner's current instruction, the owner wins.

## Which pieces for which repo

| Repo | Banner | Real media | Map | Badges |
| --- | --- | --- | --- | --- |
| CLI tool | terminal banner, command = `tool --version` | recording of the core command | optional | runtime, platform, licence, last commit |
| Config, rules or dotfiles repo | terminal banner, command = `ls` of the real folder | recording of the check or sync command | hub-and-spoke of who reads what | counts (rules, scripts, agents), platforms |
| App or TUI with screens | wordmark banner | screenshot gallery (`media.md`), one short recording | architecture map if it helps | stack, platform, licence |
| Library or API | text or wordmark banner | recording of one call plus its output | request flow as a map | version, runtime, licence |
| Plugin marketplace | wordmark banner | recording of `plugin list` style output | marketplace to hosts map | plugin and marketplace counts |

## Tools (check before starting)

`vhs` (with `ttyd`), `ffmpeg` built with libwebp, `rsvg-convert`, ImageMagick `magick`, `zsh`, optional
`zsh-fast-syntax-highlighting`, Python 3.9+. On macOS: `brew install vhs ffmpeg librsvg imagemagick
zsh-fast-syntax-highlighting`. Playwright is not needed. Verify with `command -v`.

## Steps

### 0. Gather inputs (ask only what the repo cannot answer)

- **Logo or icon and wordmark.** Look in the repo and its assets first. When the owner supplies images, copy
  the originals into `assets/` (`icon.webp`, `wordmark.webp`). They are usually transparent; check the corner
  pixel (`magick img -format '%[pixel:p{2,2}]' info:`).
- **Accent colour.** From the logo (step 1). With no logo, or a logo that is only black and white, **ask**
  and offer two or three hexes (for example from the owner's terminal theme or prompt).
- **Owner terminal look.** `~/.config/ghostty/config` (background, foreground, palette or theme name) and
  `~/.config/starship.toml` (folder and chevron colours). `make-tape.py` reads Ghostty itself.
- **Layout choice** from the reference READMEs (`SKILL.md` §4).

### 1. Palette from the logo

```bash
python3 scripts/palette.py assets/icon.webp          # accent, second accent, text-safe accent, contrast
python3 scripts/palette.py assets/wordmark.webp      # a white or black wordmark says: ask the owner
```

`accent` is for badges, icons, links and the typed chevron. `text_accent` is the lightened variant that keeps
4.5:1 contrast for small text on the dark surface. The yellow bolt in the rd-agents logo gave `#ffda00`; a
teal or purple logo works the same way. Keep one accent, plus white and greys.

### 2. Banner

```bash
python3 scripts/header.py --wordmark assets/wordmark.webp --accent '#ffda00' \
  --subtitle 'rules|skills|plugins' --window-title 'rd-agents  -  zsh' \
  --command 'ls ~/.agents' --listing 'AGENTS.md  main.md  manifest.toml  rules/  skills/  plugins/' \
  --out assets/header.svg
```

- One flat dark terminal window; the wordmark centred with an accent silhouette shadow (holes filled, smooth
  edges); the subtitle in white with accent dots; the command types and its real listing appears.
- Variants: `--logo assets/icon.webp` puts an icon left of the wordmark; no `--wordmark` renders a text
  `--title` with an accent shadow (works for any repo without artwork); `--no-shadow` drops the silhouette.
- The listing must be real (`ls` the folder). Embed with `<img src="assets/header.svg" width="860">`.
- Calm by default. Add nothing else (no glow, grid, scanlines, glitch) unless the owner asks.

### 3. Real terminal recording

```bash
python3 scripts/make-tape.py --command "scripts/agents-check | sed -n '1,14{s/  (.*//;p;}'" \
  --wait token_tools --name rd-agents --export FORCE_COLOR=1 \
  --out assets/demo.tape --output assets/.raw/demo.mp4
bash scripts/record.sh assets/demo.tape assets/demo.webp
```

- Pick **one real command** whose output proves the project and fits about 15 lines. Trim long output with
  `sed -n '1,14p'` (never `head`: a closed pipe makes Python tools print a `BrokenPipeError` traceback).
- `--wait` is a regex that appears when the command has finished; the wait itself is hidden, the output is real.
- Colour: the tape uses the owner's Ghostty palette, optional `fast-syntax-highlighting`, a blue folder name and
  a purple chevron (override with `--folder-rgb`, `--chevron-rgb`). If the tool has no colour of its own and
  colour helps, give it an opt-in (`FORCE_COLOR`, `NO_COLOR`) instead of piping through sed.
- Prompt stays minimal: folder name and chevron. No clock, git state, duration or language marker.
- The recording is made at 2x and encoded as lossless animated WebP (a GIF turns text soft). Display it at half
  its pixel width: `<img src="assets/demo.webp" width="620">`.
- No personal data in any frame: no username, home paths, tokens, real library names. Run the command in a
  clean state and **look at the frames** (`ffmpeg -i demo.webp -vf fps=1 f/%03d.png`, then view or zoom).
- vhs quirks: do not set `FontFamily` or `WindowBar` (the terminal shrinks and centres), and give `Output` a short
  path relative to the repo root; `record.sh` crops, pads evenly and adds the window bar itself.

### 4. Hub-and-spoke map (when many things read one thing)

Write `assets/flow.json` (see `flow-example.json`) with real names taken from the repo (config files, agent
lists, services), then `python3 scripts/flow.py assets/flow.json`. Targets are spaced evenly; a second lane
and a result badge are optional. Colour: accent for links, `accent2` (white) for the second path. Seek-check it
(`media.md`, Motion craft) and view three moments. Not a recording: never call it one.

### 5. Badges in the owner's style

The owner's current style (white label and border, accent value and logo; repo `rd-agents`):

```
https://shieldcn.dev/badge/<Label>-<Value>-ffffff.svg?variant=outline&mode=light&color=ffffff&logo=<slug>&logoColor=<accent>&labelTextColor=ffffff&valueColor=<accent>
```

with a `mode=dark` twin in a `<picture>` (see `shieldcn/` and `presets/white-yellow-outline.json`). Copy the
owner's badge block if they already edited one; change only counts and broken links.

- **Counts come from the repo, never from memory.** Examples: rules `ls rules/*.md | wc -l`; scripts
  `ls scripts | wc -l`; skills `ls plugins/*/skills | wc -l`; marketplaces and plugins from the manifest
  (`plugins.toml`, `marketplace.json`); agents from the tool map (`grep -c '^\[tools\.' checks/agents.toml`);
  tests, commands or providers from their own folders. State what each count means in the report.
- **Placeholders**: the owner may leave `10` everywhere; replace each with the measured number and the `alt`
  text with it.
- **Anchors must exist.** A badge linking to `#skills` needs a Skills heading; otherwise repoint to the nearest
  real section (the validator reports broken anchors) and tell the owner.
- A live badge that verifies something (`github/last-commit/OWNER/REPO`) beats a static one. Do not exceed about
  a dozen badges; expect the validator to warn above 5 and Quick Start to move down the page.

### 6. Headings and icons

`## <img src="https://api.iconify.design/lucide/rocket.svg?color=%23ffda00" height="24" align="absmiddle" alt="Rocket icon"> Quick Start`.
Use the slash form `lucide/name.svg` (the `lucide:name.svg` form returned HTTP 403). One Lucide icon per `##`,
all in the accent. Headings are one or two plain nouns: `Overview`, `Functionality`, `Rules`, `Plugins`,
`Machines`, `Health Check`, `Structure`, `License`. Not `How It Works` or `Why This Repo`.

### 7. Assemble, validate, look

README order: banner, badge rows, bold one-line summary, status line, nav bar, Quick Start (with the recording),
then the sections. Wire everything into `assets/build-media.sh` from `templates/build-media.sh.tmpl` so one
command regenerates it all, and list it in the Structure tree.

```bash
python3 scripts/validate-readme.py README.md --online      # structure, anchors, every URL loads
python3 scripts/check-media.py README.md
```

Then render the page and view it (GitHub's own renderer when `gh` is authenticated, otherwise pandoc plus
`github-markdown-css` served over localhost), and step SVG animations with `setCurrentTime`. Say plainly what you
could not check: GitHub's image proxy, light theme, phone width.

## Pitfalls learned on rd-agents

- Cap the effects. A glitch title, drifting glows, scanlines and a dot ripple together were "over the top"; the
  calm window with the real wordmark was right. Background texture only when asked.
- The header is always dark (own `#1e1e1e` window), never a light/dark pair; badges are the adaptive ones.
- Colour from the logo, and ask when there is none. Do not pick a pretty colour and move on.
- Never revert the owner's README edits (they restyle badges and layout themselves); change counts, anchors and
  alt text only, and report each change.
- A GIF is not good enough for terminal text: record at 2x, encode lossless WebP.
- `Output` paths in tapes must be short and relative; absolute paths with hyphens fail to parse.
- The preview pane may not advance animation time; seek the SVG clock to check motion.
- Piping into `head` crashes Python CLIs with `BrokenPipeError`; use `sed -n`.
- Validate the validator: a loop variable once overwrote the README text and produced false "no table" errors.
- Another session may edit the skill and the README at the same time; re-read files before editing them.
- `gh` may be unauthenticated; use plain `curl` against public endpoints and say so.
- Counts in badges must be measured and meaningful; the owner's labels (Skills, Plugins, Scripts, Rules,
  Marketplaces, Agents) each need a defined source.
