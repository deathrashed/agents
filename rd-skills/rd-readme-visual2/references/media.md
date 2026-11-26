# Media: Demos, Screenshots, GIFs, Animated SVG

A README with a working demo in the first screen beats a wall of prose. This
reference covers producing each media type consistently and knowing what GitHub
will actually render.

Measured on this machine (900x300 terminal, ~4 s):
`vhs` GIF 232 KB · `vhs` MP4 78 KB · `vhs` WebM 38 KB. Same content, 6x
difference. Pick the format before you record.

## The agent's loop

The agent generates the media itself by running the real project; SKILL.md §5 says what
to produce, this file says how. For every asset: run, capture, look, optimise, commit.

```bash
# 1. Terminal flow -> recording (sources live in assets/ so it can be re-rendered)
vhs assets/demo.tape                                   # writes the GIF/MP4/WebM named in Output

# 2. Look at it: extract frames and view them, a recording you did not look at is not done
mkdir -p /tmp/frames && ffmpeg -loglevel error -i assets/demo.gif -vf fps=2 /tmp/frames/%03d.png

# 3. Window screenshot on macOS (window id from your window-listing tool; -R x,y,w,h for a region)
screencapture -x -o -l <window-id> assets/main.png

# 4. Animated SVG: author it, then rasterise it to prove it renders and check the size
rsvg-convert -w 800 assets/flow.svg -o /tmp/flow-check.png && wc -c assets/flow.svg

# 5. Optimise, then re-check size
gifsicle -O3 --lossy=80 assets/demo.gif -o assets/demo.gif
```

Put steps like these in one `assets/build-media.sh` (or a `just media` target) so the
whole set regenerates in one command. Web UIs: use the built-in browser or
`agent-browser` for viewport screenshots; Playwright is not installed on m3. Anything
that needs credentials, a service or hardware you do not have is a question for the
owner, never something to fake.

## What GitHub actually renders

| Element | Renders? |
| --- | --- |
| `<img>` (png, jpg, gif, **webp**, svg) | Yes |
| `<picture>` light/dark pairs | Yes |
| `<video>` with a repo-relative or raw.githubusercontent URL | **No. The tag is stripped and nothing appears.** |
| `<video>` / bare URL from `https://github.com/user-attachments/assets/...` | Yes, native player with controls |
| `<iframe>` (YouTube embed) | No, stripped |

GitHub sanitizes `<video src>` for any host it does not control, and its raw
endpoint serves mp4 as `application/octet-stream`, so browsers download instead
of playing. A README with `<video src="assets/demo.mp4">` shows a blank gap.
The archetype in `local-visual-archetypes.md` that uses that tag is wrong; use
one of these instead.

| Goal | Do this |
| --- | --- |
| Inline motion, no click | GIF or animated WebP in `<img>` |
| Native player with audio | Upload the mp4 in a repo issue/comment, paste the `user-attachments` URL, or a thumbnail image linking to the file |
| Long narrated demo | Thumbnail image linking to YouTube/Vimeo |

Animated **WebP** in `<img>` is the best inline trade: 3-5x smaller than GIF with
better colour, and GitHub serves it. GIF is the compatibility floor; use it when
the animation must work in a registry page, a terminal viewer, or a slide deck.

## Terminal recordings: vhs

`vhs` (installed) turns a `.tape` script into GIF, MP4 or WebM deterministically.
This is the right tool for CLI demos: reproducible, re-runnable when output
changes, and it never captures a stray window.

```tape
Output demo.mp4
Set FontSize 22
Set Width 900
Set Height 300
Set Padding 20
Set Theme "Catppuccin Mocha"
Set Shell "bash"
Type "gupload shot.png --preview"
Enter
Sleep 800ms
Type "gupload shot.png"
Enter
Sleep 1200ms
```

```bash
vhs demo.tape          # writes demo.mp4
```

Rules:

- Change `Output` to pick the format: `.mp4` (smallest for GitHub upload),
  `.webm` (smallest overall), `.gif` (universal).
- Keep the recording to 5-15 seconds and one flow. A demo that shows everything
  shows nothing.
- `Set TypingSpeed 50ms` slows the typing for legibility; default is fine for
  short commands.
- Pick a theme with contrast against both GitHub themes, or record on a dark
  background and embed on one line.
- Never commit the `.tape` next to nothing: keep it in `assets/` so the demo can
  be regenerated. A stale demo is worse than none.
- Commit the `.tape` with the recording, so the next person can re-render.

## Screen recordings: asciinema + agg

For a real interactive session (TUI, editor, long-running process), record with
`asciinema`, then render to GIF with `agg`. Both are installed.

```bash
asciinema rec demo.cast -c "htop"     # record; Ctrl-D or exit to stop
agg demo.cast demo.gif                # cast -> gif
```

`agg` options worth knowing: `--font-size 20`, `--theme monokai`,
`--speed 1.5` (playback speed), `--idle-time-limit 1` (compress pauses). The
`.cast` file is text, so it diffs and can be re-rendered years later. This is
the better choice for TUIs and anything with unpredictable output.

## Optimising what you already have

| Source | Command |
| --- | --- |
| GIF too big | `gifski --fps 15 -o out.gif frames/*.png`, or `gifsicle -O3 --lossy=80 in.gif -o out.gif` |
| GIF to animated WebP | `ffmpeg -i in.gif -vf "fps=12,scale=900:-1:flags=lanczos" -c:v libwebp -q:v 70 -loop 0 out.webp` |
| GIF/WebM to MP4 | `ffmpeg -i in.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" out.mp4` |
| Trim and crop | `ffmpeg -ss 1 -t 6 -i in.mp4 -c copy out.mp4` |
| Downscale | `ffmpeg -i in.mp4 -vf scale=900:-2 out.mp4` |

`gifski` compresses well but warns when fed a GIF; feed it PNG frames instead
(`ffmpeg -i in.mp4 frames/%04d.png`). Keep GIFs under about 5 MB and MP4s well
under GitHub's 10 MB free-plan cap, because a README that loads slowly loses the
reader before the demo plays.

## Screenshots

For an app, plugin or TUI, a real screenshot does more than any badge.

1. **Capture at 2x** (Retina), then downscale to the display width. A 2x capture
   downscaled is sharp on both Retina and standard displays; a 1x capture looks
   soft on Retina.
2. **Window only, no desktop.** No menu bar clutter, no other apps, no personal
   data, no real API keys or paths with your username in them.
3. **One state per shot.** A grid of 2-4 states (empty, populated, settings)
   tells the story better than one busy window.
4. **Crop the dead space**, keep the window chrome if it identifies the app.
5. **Give it a caption** in the table cell (`<sub><b>Main window</b></sub>`).
6. **Shoot in the theme the README assumes.** If the README shows dark, do not
   mix one light screenshot.
7. Use `webp` or `png`; `webp` at quality 80 is usually 30-50% smaller.

For a website or web app, a browser screenshot works, but crop to the viewport
content, not the whole browser frame, unless the URL bar is meaningful.

## Animated SVG

Hand-authored SVG animates on GitHub and costs a few KB; a GIF of the same thing
is hundreds of KB. Use it for a banner accent, a logo mark, or a short looping
diagram. Always honour reduced motion.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 80" width="400" height="80" role="img" aria-label="Upload flow">
  <style>
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .p { fill: none; stroke: #b030f0; stroke-width: 3;
         stroke-dasharray: 300; stroke-dashoffset: 300;
         animation: draw 2s ease forwards; }
    @media (prefers-reduced-motion: reduce) {
      .p { animation: none; stroke-dashoffset: 0; }
    }
  </style>
  <path class="p" d="M10 40 H 390"/>
</svg>
```

Rules:

- Animation lives in a CSS `@keyframes` block inside the SVG, and CSS animation
  inside an `<img src="...svg">` **does** run on GitHub. SMIL also works but CSS
  is easier to reason about.
- Always include the `prefers-reduced-motion` override.
- Keep the loop long and slow (2-4 s) and loop only if the motion is ambient. A
  drawing-once animation with `forwards` is calmer.
- Give the SVG `role="img"` and `aria-label`, and the `<img>` a real `alt`.
- Check the file size after rasterising (`rsvg-convert -w 400 in.svg -o check.png`)
  and make sure it is under ~20 KB before shipping.
- Do not put text you need read inside an SVG: it will not be selectable,
  searchable, or read by a screen reader reliably.

Readymade animated icons: `https://www.readmecodegen.com/api/social-icon?name=terminal&size=18&animation=fade&color=%23ff2a1f`
(section headings, classic archetype). Iconify also ships animated sets; keep to
one small animated element per README.

## Live SVG services (verified reachable)

These render as SVG and cost the repo nothing:

| Service | Use | URL shape |
| --- | --- | --- |
| capsule-render | Waving/gradient hero banners | `capsule-render.vercel.app/api?type=waving&color=...&text=...` |
| github-readme-stats | Live star/commit/language cards | `github-readme-stats.vercel.app/api?username=...` |
| socialify | Repo social-preview image | `socialify.git.ci/OWNER/REPO/image?font=Inter&pattern=Plus&theme=Dark` |
| star-history | Star growth chart | `api.star-history.com/svg?repos=OWNER/REPO` |
| ghchart | Contribution heatmap | `ghchart.rshah.org/USERNAME` |
| readme-typing-svg | Typing tagline | `readme-typing-svg.demolab.com/?lines=...` |
| shieldcn | Badges, headers, charts | `shieldcn.dev/...` |

Every one is a third-party dependency: if it goes down the image breaks. Use at
most one or two, and only where the live data earns its place. Verify each URL
with `validate-readme.py --online` before shipping.

## Screenshot gallery (many screens)

When there are more than three or four screenshots, use the gallery from lastfm-scrobbler: a `<table>` of
three columns, every cell a linked image with a bold title and a one-line `<sub>` caption. It stays aligned
because the first row sets the widths and every capture has the same size.

```html
<table>
  <tr>
    <td width="33%" valign="top">
      <a href="assets/screenshots/1-dashboard.png"><img src="assets/screenshots/1-dashboard.png" alt="Dashboard listing the three modes"></a>
      <p align="center"><strong>Dashboard</strong><br><sub>Choose a mode; the footer lists the shortcuts</sub></p>
    </td>
    <td width="33%" valign="top">
      <a href="assets/screenshots/2-info.png"><img src="assets/screenshots/2-info.png" alt="Info screen"></a>
      <p align="center"><strong>Info</strong><br><sub>Reference for modes, data and imports</sub></p>
    </td>
    <td width="33%" valign="top">
      <a href="assets/screenshots/3-help.png"><img src="assets/screenshots/3-help.png" alt="Help screen"></a>
      <p align="center"><strong>Help</strong><br><sub>Keyboard and mouse controls</sub></p>
    </td>
  </tr>
  <!-- next rows repeat the same cell shape; only the first row needs width="33%" -->
</table>
```

- Number the files in walkthrough order (`1-dashboard.png`, `2-info.png`) so the gallery reads as a tour.
- Put `width="33%"` on the first row only, `valign="top"` on every cell.
- Link each image to its full-size file so a reader can zoom.
- Capture every shot at the same window size and theme; that is what keeps the grid aligned.
- Two screens: use two columns (`width="50%"`). More than nine: split into labelled groups.

## Motion craft for animated SVG

Rules borrowed (paraphrased, with thanks) from the open-design skills `review-animations` and `ui-animation`
(both MIT). Apply them to every animated SVG and recording:

- **Justify the motion.** Each animation must show something true: data moving along a real connection, a
  state coming on, a command typing. Decorative loops get cut.
- **Ease-out, not linear.** Use a strong curve such as `cubic-bezier(.22,1,.36,1)` for state changes; reserve
  `linear` for the ambient dash flow. `ease-in` makes motion feel late.
- **Animate `transform`, `opacity` and colour only.** Avoid animating width, height or position of layout
  boxes; a typing effect through a clip-path width is the accepted exception.
- **Stagger groups.** Children of a group enter one after another (tens of milliseconds for UI, a few hundred
  for an ambient diagram), with a lead and a lag between properties instead of everything at once.
- **Asymmetric timing.** Slow, deliberate phase in; quick reset out. Do not reuse the entrance reversed.
- **Line drawing.** For a self-drawing stroke set `pathLength="1"`, `stroke-dasharray="1 1.2"`, animate
  `stroke-dashoffset` from `1` to `0`, and keep the end state (`forwards`). Rounded caps need the slightly
  larger gap.
- **SVG rotation trap.** `transform-origin` in SVG defaults to the viewBox origin; use
  `transform-box: fill-box; transform-origin: center`.
- **Degenerate shapes vanish.** `width="0"` or `r="0"` removes the shape entirely, unlike `opacity: 0`.
- **Reduced motion.** Show the finished frame, not a blank one. SMIL ignores the media query, so keep a
  static copy of the animated parts and swap them in CSS.
- **Check it frame by frame.** The preview pane may not advance animation time. Seek the clock instead
  (`svg.pauseAnimations(); svg.setCurrentTime(t)` and `document.getAnimations()` with `currentTime`) and look
  at three or four moments; for GIFs extract frames with `ffmpeg -vf fps=1`.

## Creative SVG recipes (header and diagrams)

A banner or diagram is a small piece of design, not a stock graphic. Recipes used for `rd-agents`, with the
open-design skill each idea came from:

- **The banner is the terminal.** One window (traffic-light bar, centred title, faint grid, CRT scanlines at
  3-4% opacity). A real command types (`ls ~/.agents`), its real output appears, the title block rises in as
  the program's output, a prompt blinks at the bottom. Only show true things: real listings, real counts.
- **Chromatic title** (`frame-glitch-title`). Three stacked copies of the title: accent and second accent
  offset by about 3px each way with `mix-blend-mode: screen`, the plain title on top. During 5-8% of the loop
  jitter the offsets with `steps(1)` for a glitch burst; reduced motion keeps the static split.
- **Drifting glows** (`frame-light-leak-cinema`). Two large radial-gradient circles in the accent colours that
  drift 100px or so over 16-21 s (`alternate`), so the background never looks dead.
- **Glowing cursor** (`vfx-text-cursor`). A blurred copy of the cursor rect behind the sharp one, and a cursor
  that steps along with the typing (SMIL `calcMode="discrete"`).
- **Diagrams as maps.** When many things read one thing, draw a hub with spokes instead of boxes and arrows:
  packets travel along curved paths, each node pops (radius 12 to 16 and back) when its packet lands, its label
  brightens, and results get a badge with a drawn tick. Colour carries meaning (purple for links, blue for
  plugins) with a small legend. Even vertical spacing keeps labels from colliding.
- **One frame for everything.** Use the same window frame, grid and glows on the header and the diagrams so the
  README feels designed.
- **Housekeeping.** Base state is the finished frame (non-animating viewers still show it), animated parts
  have a static copy under reduced motion, files stay under about 20 KB, and every SVG is seek-checked.

## Embedding patterns

Single, full width:

```html
<p align="center"><img src="assets/demo.webp" alt="gupload previewing an upload, then publishing it" width="900"></p>
```

Two-up grid (screenshots, before/after):

```html
<table>
  <tr>
    <td width="50%" align="center"><img src="assets/main.webp" width="100%" alt="Main window listing containers"><br><sub><b>Main window</b></sub></td>
    <td width="50%" align="center"><img src="assets/settings.webp" width="100%" alt="Settings panel"><br><sub><b>Settings</b></sub></td>
  </tr>
</table>
```

Dark/light pair for a screenshot of your own UI:

```html
<p align="center"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/main-dark.webp">
  <img src="assets/main-light.webp" alt="Main window" width="900">
</picture></p>
```

Hero demo placement: right after the bold summary, before Quick Start. A reader
who sees it work does not need to be convinced by prose.

## The checklist before shipping media

- [ ] Every `<img>` has descriptive alt text, not "demo.gif".
- [ ] No fact lives only inside the image; the command or output is also in text.
- [ ] No `<video>` with a repo-relative or raw URL (it renders as nothing).
- [ ] Animated things honour `prefers-reduced-motion` or stop on their own.
- [ ] Total media under a few MB; GIFs under ~5 MB each.
- [ ] Images committed to `assets/` (or `docs/images/`), referenced relatively,
      and present on disk, so the validator's relative-link check passes.
- [ ] `.tape` / `.cast` sources committed beside their recordings.
- [ ] Rendered page checked in both themes and at phone width.
- [ ] No secrets, usernames, API tokens, or personal paths visible in any shot.
