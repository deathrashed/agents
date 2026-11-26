# Questions to Ask

Inspect the repo first, then ask only what it can't tell you. One short round
of 1–4 questions. Every question must:

- be about something concrete: a file, a colour hex, a section, a license
- offer real options taken from the repo (actual image paths, actual colours)
- put the recommended option first and say why in a few words

Never ask about abstract things like "vibe", "feel", or "tone". Decide those
yourself from the project and say what you chose.

If the repo answers everything, skip the questions and state your choices in
two or three lines before drafting.

## Good questions

**Layout** (when more than one reference README fits)

> Which of your READMEs should this one feel closest to?
> 1. `dockmoid` for the screenshots section and compatibility table (recommended: this is an app with a UI)
> 2. `gupload` for a short, single-purpose layout
> 3. `audio-agent` for a long, fully documented layout

State the recommended one and why from the project, then borrow ideas from it; never
copy it whole.

**Colour** (when the repo has no logo or icon to take colours from, or the icon has several strong colours)

> The icon has purple `#b030f0` and pink `#f03090`. Which should lead?
> 1. Purple `#b030f0` for badges and headings, pink for alternating headings (recommended: purple is the dominant colour)
> 2. Pink `#f03090` leading
> 3. Purple only

**Header image** (when there are several candidates)

> Which image goes in the header banner?
> 1. `assets/icon.png` (recommended: square, reads well at small size)
> 2. `docs/banner.png` as a full-width banner instead of a shieldcn header

**Screenshots** (when it has a UI but no images in the repo)

> Do you have screenshots or GIFs to include?
> 1. Yes, I'll add them to `docs/screenshots/` (I'll lay out a grid)
> 2. No, skip the gallery

**Demo** (when the project has runnable or visible output)

> The README needs real media. How should I produce it?
> 1. Generate it myself by running the project: `vhs` recordings, screenshots, an animated SVG diagram (recommended: reproducible, re-renderable when output changes)
> 2. Use the screenshots/GIFs you already have
> 3. Skip the media

Never promise a demo you cannot actually run: if the tool needs credentials, a
service, or hardware you do not have, say so and ask for a recording instead.

**License block** (when the repo's license has several variants)

> Which GPL license block?
> 1. Free-works logo with the classic badge (recommended: matches gupload)
> 2. Green open-source logo with the green badge
> 3. GPL logo with the classic badge

**Existing copy** (when the README has the user's own writing)

> Keep your existing wording?
> 1. Keep it and restyle only (recommended)
> 2. Tighten it as I go

**Extras** (only when the project could clearly use one)

> Add a typing tagline under the header ("upload • reference • archive" → "copy links in any format")?
> 1. No (recommended for tools that should read calm)
> 2. Yes, in the accent colour, playing once

## Bad questions

- "What vibe should the README have?"
- "Should it be calm or playful?"
- "Which sections do you want?" (decide from the code, then show the plan)
- Anything already answered by the repo: language, license, platform, commands

## After the draft

Ask one closing question: **"Anything else to highlight or include that I might have missed?"**
