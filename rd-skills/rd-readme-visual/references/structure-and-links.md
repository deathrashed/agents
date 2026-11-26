# Formatting: Sections, Anchors, Links, and GitHub's Unused Features

Companion to `formatting.md` (badges, dropdowns, alerts). This file covers how
the document hangs together: section design, anchors that actually resolve,
internal and external links, and the GitHub syntax most READMEs never use.

## Section design

A section is a question the reader arrives with, and the heading names it.

| Rule | Why |
| --- | --- |
| One to three words, Title Case | `Usage`, `Hard Albums`, `Plans and Undo`. A scanning reader reads the heading, not the paragraph |
| Never a sentence or a colon list | "Matching a hard album: ISRC, AcoustID, MusicBrainz" should be `Matching` with the detail inside |
| Same pattern for siblings | If one is `Tagging`, the next is `Tagging Rules`, not `How tags get applied` |
| The heading answers "what will I learn" | `Configuration` not `About configuration` |
| No question headings except in FAQ | `Why Go?` is fine as a one-off; a page of questions is a page without answers |
| Front-load the distinguishing word | `Album Matching`, not `Matching of Albums`; the outline shows the first words |

Order sections so a reader can stop at any point without having missed something
that changes their decision: identity, then why, then first command, then detail,
then internals. A non-permissive licence goes near the top because it
disqualifies fastest.

Size is content, not a rule. A small tool gets six sections; a full application
gets twenty. What matters is that each section earns its heading. Two sections
that always contain one paragraph each should be one section.

## Anchors that resolve

GitHub builds the anchor from the heading text with these steps, in order:

1. Strip HTML tags (the Iconify `<img>` disappears).
2. Decode HTML entities: `&amp;` becomes `&`.
3. Lowercase.
4. Remove everything that is not a letter, digit, underscore, hyphen or space.
5. Replace each space with a hyphen. **Runs are not collapsed.**
6. On a duplicate, append `-1`, `-2`, and so on.

| Heading | Anchor |
| --- | --- |
| `## Quick Start` | `#quick-start` |
| `## Run &amp; Test` | `#run--test` (two hyphens) |
| `## CLI & Flags` (literal `&`) | `#cli-flags` (one hyphen, `&` removed) |
| `## What's New` | `#whats-new` |
| `## Setup (macOS)` | `#setup-macos` |
| `## 1. Inspect` | `#1-inspect` |
| `## --dry-run Behaviour` | `#--dry-run-behaviour` |

Consequences worth designing around:

- **Prefer `and` over `&` in headings.** `Run and Test` anchors to `#run-and-test`,
  which nobody gets wrong. `Run &amp; Test` anchors to `#run--test`, which looks
  like a typo and breaks hand-written links.
- **Avoid punctuation in headings** (`:`, `?`, `!`, `,`, `’`): it silently
  vanishes from the anchor, so the link differs from the text in a way a reader
  cannot predict.
- **Do not change a heading** without updating every link to it. Anchors are
  derived, not stored.
- `##` and `###` both get anchors. Deep links to a `###` subsection are cheap and
  useful (`#install-homebrew`), so name subsections as carefully as sections.

Verify with `scripts/validate-readme.py`: it resolves every `#anchor` against the
heading tree and reports the ones that will 404.

### Custom anchors

When the target is not a heading (a step in a long list, a specific table row),
add an explicit anchor:

```html
<a name="install-homebrew"></a>
### Install with Homebrew
```

`<a name>` survives GitHub's sanitizer and does not appear in the outline, so use
it to add a second entry point to content that already has a heading.

## The navigation bar

Most of Riley's READMEs put a pipe-separated nav row under the summary:

```html
<p align="center"><a href="#quick-start">Quick Start</a> | <a href="#usage">Usage</a> | <a href="#configuration">Configuration</a> | <a href="#license">License</a></p>
```

Rules:

- **Four to six entries.** More becomes a second table of contents.
- **Only headings that exist**, spelled exactly as the anchor, or the click goes
  nowhere.
- **The order is the reading order**, not alphabetical.
- **No `Contents` heading unless the README is genuinely long.** GitHub renders
  an outline from the headings already (the "Outline" button on the file), so a
  hand-written table of contents duplicates it and then goes stale. If the README
  is over roughly 300 lines or 10 sections, a compact `Contents` list is still
  worth it for readers on a phone, who do not see the outline.

## Links

**Internal.** Always relative and lowercase-safe:

```markdown
[Configuration](#configuration)          <!-- heading anchor -->
[Install with Homebrew](./docs/install.md#homebrew)   <!-- file + anchor -->
```

Two failure modes the validator catches: an anchor that does not match any
heading, and a relative path to a file that is not on disk.

**External.** Link the thing, not the brand:

| Weak | Strong |
| --- | --- |
| [here](https://…) | [the Iconify API syntax](https://…) |
| [click here](https://…) | [install uv](https://…) |
| [GitHub](https://github.com) | [open an issue](https://github.com/o/r/issues/new) |

- Never link a URL you have not confirmed returns 200. `--online` requests every
  one and reports failures.
- Prefer the canonical URL (the repo, the package page, the docs) over a
  blog post that will rot.
- Cross-link between sections when one depends on another:
  "see [Configuration](#configuration)" beats repeating the table.
- Link to a source file with a line range when citing behaviour:
  `[`upload.py:120`](src/upload.py#L120)`.
- Badges are links too: every badge `<a href>` must go somewhere real. A row of
  badges all pointing at `#` is worse than no badges.

**What not to link.** Do not link `CONTRIBUTING.md`, `CHANGELOG.md` or
`SECURITY.md` if those files do not exist: GitHub surfaces them automatically
once they do, and a dead link is a visible defect. One line pointing at the file
is enough; do not inline its content.

## GitHub syntax most READMEs skip

Each of these renders on GitHub today and costs one line. Use them where they
remove a sentence of prose.

**Keyboard keys.** `<kbd>` draws a real key cap: a bordered, monospace, slightly
raised box. Backticks give you plain code text, which reads as a filename or a
command, not as something you press. Use it for every shortcut and key name.

```markdown
Press <kbd>⌘</kbd> + <kbd>K</kbd> to open the palette.
Press <kbd>Esc</kbd> to cancel.
```

In a shortcuts table it is the difference between a table of keyboard keys and a
table of code:

```markdown
| Key | Action |
| --- | --- |
| <kbd>↑</kbd> <kbd>↓</kbd> or <kbd>j</kbd> <kbd>k</kbd> | Navigate menus and lists |
| <kbd>Enter</kbd> | Select, confirm, or open the editor |
| <kbd>Tab</kbd> / <kbd>Shift</kbd> + <kbd>Tab</kbd> | Next / previous view |
| <kbd>Esc</kbd> | Back to the dashboard, or cancel input |
| <kbd>⌘</kbd> + <kbd>S</kbd> | Save |
```

Rules:

- One `<kbd>` per key, joined with `+` in prose: `<kbd>⌘</kbd> + <kbd>K</kbd>`,
  not `<kbd>⌘+K</kbd>`. It reads better and each cap is legible.
- Spell the key as printed on the keyboard: `<kbd>Esc</kbd>`, `<kbd>Enter</kbd>`,
  `<kbd>⌘</kbd>`. Do not translate a mac key to "Cmd" in prose if the cap says ⌘.
- Alternatives go in one cell separated by a slash, each with its own tag.
- Show the platform variant where they differ: `<kbd>⌘</kbd>` for macOS,
  `<kbd>Ctrl</kbd>` for Linux and Windows, on separate rows or with a footnote.
- `<kbd>` works in tables, lists and sentences. It does not work on npm or PyPI,
  which strip raw HTML, so a registry-hosted README shows the literal tag. If a
  README is published to a registry, keep the key names in backticks instead.

**Task lists.** Good for a roadmap or a status page; bad for a README's main
content, where it reads as unfinished work.

```markdown
- [x] Album matching
- [ ] Last.fm metadata
- [ ] Windows build
```

Those boxes are not clickable in a README (only in issues), so do not imply
interaction.

**Footnotes.** Keep a tangent out of the sentence without losing it. GitHub
renders them as superscript markers that jump to a numbered note at the bottom
and link back.

```markdown
Matching uses AcoustID[^1] when the fingerprint is available. Folders with fewer
than three tracks are skipped[^2].

[^1]: AcoustID is a free service; a key is optional but raises accuracy.
[^2]: The threshold is configurable with `--min-tracks`, default 3.
```

Rules:

- Number them `[^1]`, `[^2]`; GitHub renumbers by order of appearance, so do not
  worry about insertion.
- A footnote body can span lines if you end each line with two spaces, and can
  contain a link or a code span.
- Use a footnote for a **detail the sentence needs but the reader may skip**: an
  aside, a caveat, a source. Use a normal link for anything the reader must act
  on, and use `<details>` for a block of content.
- Do not use a footnote for the main explanation. If a reader must read it, it
  belongs in the sentence.
- Footnotes do not work in wikis, and they render as literal `[^1]` on npm and
  PyPI.
- Never fake one with `<sup>1</sup>`: it does not link anywhere.

Good uses in this corpus: the AcoustID and MusicBrainz lookups in the tagging
tools, the "why this threshold" numbers in the matching logic, and the platform
caveats that would otherwise interrupt a quick start.

**Collapsible sections already covered** in `formatting.md`; the rule that bites
is the blank line after `<summary>`.

**Math.** Real LaTeX via MathJax, for audio, crypto, or algorithm repos.

```markdown
Bitrate overhead is $\frac{\text{header}}{\text{payload}}$ per packet.

$$ \text{bitrate} = \frac{\text{file size} \times 8}{\text{duration}} $$
```

Inline math uses single `$`, a block uses `$$` on its own lines. Escape a literal
dollar as `\$`. Math renders on GitHub but not on npm or PyPI, and `$` in prose
can accidentally start an expression, so avoid it in a sentence that also
discusses money.

**Colour chips.** A hex value in backticks renders as a small colour swatch.
GitHub parses these models: `#RRGGBB`, `rgb(r, g, b)`, `hsl(h, s, l)`.

```markdown
The accent is `#b030f0` in dark mode and `#7a1fb0` in light.
Badge fill: `rgb(176, 48, 240)`. Muted text: `hsl(270, 60%, 40%)`.
```

This is the cheapest way to document a palette: the reader sees the colour
instead of decoding a hex. Use it in a theme, palette, or configuration section.
Do not scatter it through prose as decoration, and do not put it in a heading or
a table cell you also need to be searchable. The swatch only renders in issues,
pull requests, discussions and `.md` files, not in every context.

**Subscript and superscript.** Only the HTML tags work on GitHub. The `^x^` and
`~x~` caret forms are Pandoc and Typora syntax and render as literal characters
in a README, so never use them here.

```markdown
Requires Python 3.12<sup>+</sup> and <sub>at least</sub> 4 GB RAM.
E = mc<sup>2</sup>, H<sub>2</sub>O
```

The tags work inline, in a list item, and in a table cell. They do not work
inside a code span. Keep them out of headings, which changes the anchor.

**Mermaid.** Already the house choice for flow diagrams (`section-menu.md`). It
renders natively, so no image and no alt text needed, but it does not render on
package registries; pair it with a sentence that carries the same meaning.

**Alerts.** Five types, documented in `formatting.md`. Keep to two or three in
the whole README; more and they stop standing out.

**Escaping.** Markdown treats some characters as syntax. When you need the
character itself, escape it with a backslash, or wrap it in backticks.

| You want | Write | Why |
| --- | --- | --- |
| A literal `*` or `_` | `\*` / `\_` | Otherwise it starts emphasis |
| A literal `#` at line start | `\#` | Otherwise it is a heading |
| A literal pipe inside a table cell | `\|` | Otherwise it starts a new column |
| A literal backtick | `` \` `` or a `` `` `` fence | Otherwise it closes the code span |
| Literal `<tag>` in prose | `` `<tag>` `` or `&lt;tag&gt;` | Otherwise GitHub may swallow it as HTML |
| A literal `[` or `]` | `\[` / `\]` | Otherwise it starts a link |
| A dollar sign in prose | `\$` | Otherwise MathJax may treat it as math |

The table-pipe case is the one that silently breaks a layout: a cell containing
`--flag | other` renders as two columns. Escape it, or use `&#124;`.

Backticks beat backslashes for anything that is code: `` `<div>` `` is more
readable in source than `&lt;div&gt;` and renders the same.

## Diffusion: make it scannable

The reader is skimming at speed. These rules do most of the work:

| Do | Instead of |
| --- | --- |
| A table for anything with three or more comparable items | A paragraph listing them |
| A short code block per step | One long block with comments |
| Bold the first two words of a bullet, then the explanation | Uniform bullets that all look alike |
| One idea per paragraph, three sentences max | A dense block of justification |
| A `>` alert for the one thing that must not be missed | Burying it mid-paragraph |
| A sentence stating what the project does **not** do | Silence, which the reader fills with doubt |

Three habits that make prose read as machine-written, and what fixes them:

- **Em-dashes and en-dashes** in prose. Use a full stop, a comma, or parentheses.
  The validator flags them.
- **"Not X. But Y." rhetorical pairs**, and "It's not just a tool, it's a
  workflow." Say the thing once.
- **Adjective stacks**: "powerful, flexible, and intuitive." Replace with the one
  measurable claim that matters.

## Checklist before shipping formatting

- [ ] Every `##` is one to three words in Title Case, and the siblings match.
- [ ] No `&`, `:`, `?`, or `’` in headings unless necessary; if used, the anchor
      was checked.
- [ ] Every internal `#link` resolves (validator enforces).
- [ ] The nav bar has four to six entries, all real.
- [ ] No hand-written TOC unless the file is genuinely long.
- [ ] External links have descriptive text and return 200 (`--online`).
- [ ] No dead links to `CONTRIBUTING.md` / `CHANGELOG.md` that do not exist.
- [ ] Scannable: tables where comparisons exist, alerts only where they earn it.
- [ ] `<kbd>` used for every key and shortcut, one tag per key.
- [ ] Palette documented with colour chips, not bare hex in prose.
- [ ] Footnotes carry asides and caveats only, never the main explanation.
- [ ] `<sup>` / `<sub>` tags, never `^x^` or `~x~` (those are Pandoc-only).
- [ ] `kbd`, footnotes, math, task lists used only where they remove prose.
- [ ] Pipes and angle brackets in table cells escaped (`\|`, `` `<tag>` ``).
