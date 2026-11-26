---
name: rd-zsh
description: >
  Comprehensive expert context for Riley's macOS Zsh config at ~/.config/zsh
  (repo deathrashed/zsh, m3's login shell). Use for any work on startup flow,
  module architecture, aliases/functions, lazy-loading, fzf pickers, msearch,
  cachy/KDE Connect helpers, git helpers, prompt config, shell debugging, or the
  repo's decorative file banners, Nerd Font section icons, separators, code
  comments, and visual formatting conventions. For Fish (cachy's login shell,
  also on m3) use rd-fish.
---

# Riley Zsh Config Skill (Comprehensive + Personal Preferences)

## Riley Environment Profile

### Hardware / OS / Shell
- Machine: MacBook Air 15-inch M3 (`m3`)
- OS: macOS 27 (27.2.1 on 2026-11-26)
- Shell: Zsh 5.9, the login shell on m3 (`/bin/zsh`). cachy has no
  `~/.config/zsh`; its login shell is Fish (see rd-fish).
- Config root: `~/.config/zsh` (`ZDOTDIR` model, set in `~/.zshenv` →
  `.zshenv`), repo `github.com/deathrashed/zsh`

### Terminal / Prompt Preferences
- Preferred terminal: **Ghostty**
- Also used: VS Code integrated terminal
- Prompt engine: **Starship** via `prompt/starship.toml`

### Core Tool Preferences (day-to-day)
- Editor: `micro` (with VS Code openers as needed)
- File listing: `eza` (preferred over plain `ls` in workflows)
- File search: `fd` (preferred over `find` where practical)
- Text search: `rg`
- Fuzzy selection: `fzf`
- Preview: `bat`
- Directory jump: `zoxide`
- Runtime manager: `mise`
- File manager: `yazi`

## Current Repository Map

Treat this as an orientation map, not a substitute for `rg --files` and the
active `load_module`/`source` calls in `.zshrc`.

```text
~/.config/zsh/
├── .zshenv / .zprofile / .zshrc
├── README.md
├── assets/
│   ├── graf-banner.png
│   └── zsh.png
├── completions/
│   └── _<command>          # repo-local Zsh completion definitions
│                            # (_betteraudio, _broken-links, _ghostty-tools,
│                            #  _herdr, _hermes, _nerd, _ringicon, _scrobbler)
├── docs/
│   ├── AGENTS.md / SKILL.md
│   ├── ARCHITECTURE.md / PERFORMANCE.md
│   ├── INSTALLATION.md / CUSTOMIZATION.md / STYLE.md
│   ├── zsh-config.codemap
│   └── msearch/MSEARCH-UPDATE.md
├── modules/
│   ├── colors.zsh          # sources data/colors/{pantone,material}.zsh
│   ├── config.zsh
│   ├── aliases.zsh          # also exports MUSIC_DIR, ICLOUD, OBSIDIAN, …
│   ├── functions.zsh
│   ├── ai.zsh              # AI-tool env hub (replaces old antigravity.zsh)
│   ├── tagg.zsh             # macOS Finder tag CLI (+ tagg.md notes)
│   ├── cachy.zsh            # ssh/mount/service helpers for cachy (partly stale, see below)
│   ├── kdeconnect.zsh       # kdeconnect-cli shortcuts aimed at cachy
│   ├── fzf.zsh              # dispatcher only, loops over modules/fzf/*.zsh
│   ├── fzf/
│   │   ├── core.zsh         # sources shared/filetypes.zsh
│   │   ├── popup.zsh
│   │   ├── brew.zsh
│   │   ├── reference.zsh
│   │   ├── shell.zsh        # sources files.zsh (not in the dispatcher loop)
│   │   ├── files.zsh        # FZA file manager (~1,100 lines)
│   │   ├── aliases.zsh
│   │   ├── music.zsh        # msearch entry points, cache build/refresh
│   │   ├── shortcuts.zsh
│   │   ├── shared/filetypes.zsh  # file classification for FZA and msearch
│   │   └── msearch/         # msearch-*.zsh (registry, preview, topbar, cache,
│   │                        #  hints, actions), swinsian-fzf-action.zsh, help .md
│   ├── nerdfonts.zsh        # `nerd`/`fznf`/`glyph-info` browser
│   ├── spectrum.zsh         # 256-color helpers (spectrum_ls/spectrum_bls)
│   ├── coolshit.zsh
│   ├── git.zsh
│   ├── loader.zsh
│   ├── lazy.zsh
│   ├── prompt_styles.zsh    # prompt-style switcher + interactive picker
│   ├── ghostty.zsh
│   ├── data/
│   │   ├── colors/{pantone,material}.zsh
│   │   ├── nerdfonts/       # glyphs.tsv (~11k glyphs), cheatsheet, preview.zsh
│   │   └── lazy-symbols.zsh
│   └── README.md
├── prompt/
│   ├── starship.toml
│   ├── starship-terminal.toml   # used when TERM_PROGRAM=Apple_Terminal
│   ├── styles/              # prompt_styles.zsh presets
│   │   ├── boxed.toml / minimal.toml / powerline.toml / time.toml
│   │   └── starship/        # 36 extra starship presets (tokyo-night, pure-preset, …)
│   └── picker/              # Go TUI (`prompt-picker`) used by `prompt` cmd
│       ├── main.go / go.mod / go.sum
│       ├── prompt-picker    # built binary
│       └── preview.sh
├── secrets/                 # never print contents
│   ├── APIs.csv
│   ├── iterm2-integration.zsh
│   └── secrets.zsh
└── .archive/                # old completions, msearch zip, previous modules
```

msearch is live again: it lives in `modules/fzf/msearch/` and is driven from
`modules/fzf/music.zsh` (cache under `${XDG_CACHE_HOME}/msearch/v2`, rebuild with
`msearch-refresh`). The old `modules/data/msearch/` copy is deleted (uncommitted
on 2026-11-26). `modules/antigravity.zsh` no longer exists — `modules/ai.zsh` is
the AI-tool env hub.

---

## Paths Riley Uses Frequently

- Zsh repo root: `~/.config/zsh`
- Modules dir: `~/.config/zsh/modules`
- Prompt config: `~/.config/zsh/prompt/starship.toml`
- Secrets: `~/.config/zsh/secrets/secrets.zsh`, and `~/.env` (exported with
  `set -a` at the very end of `.zshrc`). Never print, copy or commit either.
- Obsidian vault path (`$OBSIDIAN`, used by note helpers):
  - `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian`
  - This is the iCloud vault. The agents' shared vault is a different one:
    `~/Obsidian/Agents` (see `~/.agents/rules/vault.md`).
- iCloud root:
  - `~/Library/Mobile Documents/com~apple~CloudDocs`
- External media volume paths used by aliases/functions:
  - `/Volumes/Eksternal`
  - `/Volumes/Apfspace`

When editing functions, prefer existing env vars (`$MUSIC_DIR`, `$ICLOUD`, `$OBSIDIAN`, etc.) over repeating absolute paths.

---

## Visual Language and Formatting

Treat presentation as part of this repo's maintained interface. Preserve the
stylized, glyph-rich house style when adding or reorganizing Zsh code.

### Inspect before formatting

1. Read the full target file and one recently formatted sibling module.
2. Reuse the target file's existing width, icon, spacing, and header variant.
3. Use a Nerd Font-capable view when judging alignment; ordinary character
   counts do not reliably measure private-use glyph display width.
4. Format the code touched by the task. Do not restyle unrelated legacy
   sections or replace a deliberate banner variant unless asked.
5. If a nearby block is visibly malformed, duplicate-free repair is safe only
   when it is directly adjacent to the requested edit; otherwise report it.

### File mastheads

Use a full decorative masthead at the top of substantial config and module
files. A module masthead contains:

- an optional `#!/usr/bin/env zsh` shebang as the literal first line;
- the boxed `Z S H   M O D U L E` or `C O N F I G U R A T I O N` label;
- one meaningful Nerd Font icon repeated in the header and update footer;
- a spaced module name such as `A L I A S E S`;
- centered FIGlet-style module-name art;
- `https://github.com/deathrashed/zsh`;
- one concise purpose line;
- a centered keyword line separated with bullets;
- a boxed `L A S T  U P D A T E D` footer and current edit date.

Do not generate a new masthead from memory. Copy the complete masthead from the
closest canonical sibling, then change the module name, icon, art, purpose,
keywords, and date while preserving its visual width. Keep every border line
commented and ensure there is no accidental leading space before `#`.

Do not add a large masthead to tiny bootstrap, generated, secret, or compatibility
files merely for uniformity. Match their established local style.

### Header hierarchy

Use one visual level per semantic level. Do not stack two equivalent headers
for the same block.

#### Major section: default

Use this for a category containing multiple aliases, functions, or related
settings:

```zsh
#══════════════════════════════════════════════════════════════════════════════════════════
# 󰯃 SCRIPT HUB
# - A collection of custom scripts and utilities,
#   organized in one central location.
#══════════════════════════════════════════════════════════════════════════════════════════
```

- Choose a Nerd Font icon that identifies the category.
- Write the title in uppercase.
- Add a short `# -` description that explains scope or purpose.
- Wrap long descriptions onto aligned `#   ` continuation lines.
- Keep the top and bottom rule the same width as neighboring sections.

#### Major introduction: expanded

Use the existing expanded form for a file's opening content section when it
includes descriptive metadata:

```zsh
#══════════════════════════════════════════════════════════════════════════════════════════
# 󰘳 ALIASES & SHORTCUTS
#─────────────────────────────────────────────────────────────────────────────
# A large collection of aliases for common commands and workflows.
# Organized by category and kept separate for easy editing.
#─────────────────────────────────────────────────────────────────────────────
```

Preserve optional `Updated:` metadata only where that file already uses it.
Do not add duplicate descriptions or dates.

#### Compact structural section

Use the bullet-capped form where the surrounding file already uses it for
high-level startup/configuration phases:

```zsh
#•═══════════════════════════════════════════════════════════════════════════════════════════•
#  CORE ENVIRONMENT
#•═══════════════════════════════════════════════════════════════════════════════════════════•
```

Do not mix compact and default major headers arbitrarily. Follow the target
file's hierarchy.

### Subsections and item comments

Use a thin rule for a named subsection or a visually distinct action:

```zsh
#─────────────────────────────────────────────────────────────────────────────
# 󰈮 Run all scripts from one interactive TUI
#─────────────────────────────────────────────────────────────────────────────
alias hub='$HOME/Scripts/.hub/script-hub.sh'
```

Use a plain intent comment followed by a thin rule when several neighboring
lines share one explanation:

```zsh
# Clean default: icons and names without metadata clutter.
#─────────────────────────────────────────────────────────────────────────────
alias ls='eza ...'
```

Apply these rules:

- Add an icon to meaningful named actions/categories, not every incidental note.
- Keep the comment immediately attached to the code it documents.
- Use sentence case for prose and uppercase only for section titles.
- Avoid decorative `─` prefixes inside prose when the enclosing thin rule
  already supplies the visual structure.
- Leave enough blank space between major sections to make scanning easy, while
  avoiding large accidental whitespace runs.

### Comments inside complex functions

Document multi-stage functions at the level a maintainer needs to navigate
them. Explain state transitions, destructive actions, non-obvious Zsh
expansions, external side effects, and why a branch exists.

Use compact internal phase labels for long interactive functions:

```zsh
  # ── FILE PICKER ───────────────────────────────────────
  local selected_files

  # ── ACTION PICKER ─────────────────────────────────────
  local action
```

Use ordinary sentence comments for local decisions:

```zsh
    # Audio files open in Swinsian; other formats use their default app.
```

Do not:

- narrate every assignment or obvious command;
- turn every line into a decorated subsection;
- preserve stale comments after behavior changes;
- use comments to excuse unsafe or unclear code.

### Nerd Font and output symbols

- Prefer existing repo glyphs for related concepts before introducing a new one.
- Keep a section's icon semantically consistent across its header and nearby
  success/warning output where appropriate.
- Use the established status language: `󰄬` success, `󰀪` warning, `󰅖` failure,
  unless the local helper has a more specific established symbol.
- Keep a plain-text explanation beside icons; never make meaning depend on the
  glyph alone.
- Do not substitute emoji for established Nerd Font symbols in a formatted module.

### General code style

1. Use `function name() { ... }` consistently.
2. Keep guard clauses explicit and readable.
3. Explain intent, assumptions, side effects, and tradeoffs rather than syntax.
4. Keep interactive output consistent with existing glyph-rich messaging.
5. Keep code practical and maintainable rather than terse for its own sake.

For docs and skill text, prefer explicit headings, grouped sections, practical
checklists, and concrete examples.

---

## Architecture & Load Model

### Shell startup chain

```text
.zshenv -> .zprofile -> .zshrc
```

### Module loading in `.zshrc`

Actual order (verified 2026-11-26 against `.zshrc`; verify again, it drifts):

1. `zsh-defer` is sourced from Homebrew first, because `config.zsh` can defer
   optional integrations.
2. `config.zsh` (env, PATH, framework, completions).
3. `secrets/secrets.zsh` sourced directly (not via `load_module`).
4. Terminal integrations sourced inline: Ghostty shell-integration, VS Code
   shell integration, iTerm2 (`secrets/iterm2-integration.zsh`), zsh-system-clipboard.
5. Eager: `ai.zsh`, `aliases.zsh`, `functions.zsh`, `tagg.zsh`, `cachy.zsh`,
   `kdeconnect.zsh`, `fzf.zsh` (dispatches into `modules/fzf/*.zsh`),
   `nerdfonts.zsh`, `spectrum.zsh`, `coolshit.zsh`.
6. Deferred via `zsh-defer` when available (else eager as fallback):
   `colors.zsh` (sources `data/colors/pantone.zsh` + `material.zsh`),
   `git.zsh`, `loader.zsh`.
7. `loader.zsh` registers stubs; the first stub call sources `lazy.zsh`.
8. Inline in `.zshrc`: mpd/ncmpcpp aliases, `^F` rebound to
   `fzf-history-widget` (`^R` removed), `STARSHIP_CONFIG` chosen
   (`starship-terminal.toml` in Apple Terminal, else `starship.toml`).
9. `prompt_styles.zsh` (prompt-style switcher + `prompt` picker command).
10. Syntax highlighting (fast-syntax-highlighting, else zsh-syntax-highlighting),
    deferred via `zsh-defer`.
11. `ghostty.zsh` through `load_module`.
12. Tail: x-cmd, Otty shell integration, opencode PATH, startup profiling,
    `_final_path_hygiene` (run now, deferred, and on every `precmd`: drops
    `/Volumes/*` entries, orders mise node bins and `~/.local/bin` first),
    `~/.local/bin/env`, then `~/.env` exported with `set -a`.

`colors.zsh` is not the first module; `config.zsh` is. Do not assume
color/data primitives exist during `config.zsh` or the terminal integration
block, or in any eager module (colors load deferred).

`.zprofile` only sources OrbStack's `init.zsh`. `.zshenv` sets `ZDOTDIR` and the
XDG homes, and moves tool homes under them (`CARGO_HOME`, `RUSTUP_HOME`,
`GOPATH`, `GEM_HOME`, `DOCKER_CONFIG`, `GNUPGHOME`, npm config, …).

### Lazy loading contract

- `loader.zsh` discovers top-level function declarations in `lazy.zsh` and
  builds `__functions_symbols` dynamically.
- generated `gitquick_*` names are appended from `GITQUICK_REPOS`.
- each symbol is stubbed to `__functions_stub` -> `__load_functions`
- `__load_functions` sources `lazy.zsh` once

**Hard rule:** keep lazy functions as parseable top-level declarations using
`function name() {` or `name() {`, then verify the generated stub. Do not
reintroduce a manually maintained symbol list.

---

## Module Responsibilities

### `modules/colors.zsh` and `modules/data/colors/*.zsh`
- Define shared terminal status colors and named color lookup/sample helpers
- Sources `data/colors/pantone.zsh` and `data/colors/material.zsh`
  (associative-array datasets)
- Deferred via `zsh-defer` — do not assume it has run yet in eager modules

### `modules/data/lazy-symbols.zsh`
- Data file consumed by `loader.zsh` for lazy-function symbol discovery

### `modules/config.zsh`
- Startup-sensitive core: XDG vars, PATH assembly, OMZ plugin setup, completion config
- Lazy tool init patterns (e.g. NVM, pyenv wrappers)
- History and completion behavior

### `modules/aliases.zsh`
- High-volume aliases and directory vars
- naming systems (e.g., `///name`, `//name`, `bat-name`, `z*`, `g*`, etc.)
- frequent UX shortcuts for file ops and macOS workflows

### `modules/functions.zsh`
- Eager, startup-safe functions
- includes `_fzf_alias_widget` and `ab` behavior
- keep minimal and low-cost

### `modules/coolshit.zsh`
- Eager aliases/functions for terminal visuals, screensavers, and system candy
- Keep optional command dependencies guarded where practical

### `modules/ai.zsh`
- Sources the central AI-tool environment hub when it exists (replaces old
  `antigravity.zsh`)
- Keep it lightweight and tolerant of the external include being absent

### `modules/tagg.zsh` (+ `modules/tagg.md`)
- macOS Finder tag CLI (`tagg COLOR TAGNAME PATH ...`)
- Shells out to a Python helper for `.plist`/xattr tag manipulation

### `modules/fzf.zsh` and `modules/fzf/*.zsh`
- `fzf.zsh` is a thin dispatcher: loops over `modules/fzf/{core,popup,brew,
  reference,shell,aliases,music,shortcuts}.zsh` and errors loudly if one is
  missing/unreadable
- Not in the loop but still loaded: `core.zsh` sources `shared/filetypes.zsh`,
  and `shell.zsh` sources `files.zsh` (the FZA file manager). msearch files
  under `fzf/msearch/` are sourced on demand from `music.zsh` and the registry.
- Add new fzf-driven pickers as a new file under `modules/fzf/` and append it
  to the loop list in `fzf.zsh`, rather than growing one large file

### `modules/cachy.zsh`
- Rewritten 2026-11-27 for the current setup (SMB, Tailscale `100.77.7.7`,
  `~/docker` stacks behind Caddy). Every read-only helper was run against cachy.
- SSH: `cachy`, `cachy-ip`, `cachy-ts`, `cachy-run` (remote side is **fish**; use
  `cachy-run bash -c '…'` for POSIX syntax), `cachy-copy-to/from`.
- SMB (m3 side): `cachy-mounts` (report only), `cachy-smb-status`,
  `cachy-smb-log`, `cachy-smb-run` (kickstart the `com.rd.cachy-smb` watcher),
  `cachy-mount-root` (opens `smb://cachy/root` in Finder). Nothing here mounts
  or unmounts by hand; the watcher owns `/Volumes/home` and `/Volumes/mnt`.
- Health: `cachy-up` (tailnet, ping, one ssh try, port 445), `cachy-smb-server`,
  `cachy-disks`, `cachy-ufw-status`, `cachy-sleep-status`, `cachy-journal [unit]`.
- Docker: `cachy-dps`, `cachy-dlogs`, `cachy-d{start,stop,restart,exec,inspect}`,
  `cachy-stacks`/`cachy-stack-up|down <name>` (folders under `~/docker`),
  `cachy-web <service>` → `https://<service>.cachy` via Caddy + Pi-hole DNS.
- Cloud: `cachy-cloud-status` (pCloud FUSE, OneDrive rclone, iCloud reverse mount).
- NFS, Dockge, Lidarr and open-webui helpers were removed: none of them exist
  on cachy any more. `/etc/fstab` keeps the old NFS lines commented as retired.

### `modules/kdeconnect.zsh`
- `kdeconnect-cli` shortcuts aimed at cachy: `kde`, `kdevices`, `konline`,
  `krefresh`, `kc` (raw), `kclip`, `kping`, `ksend`, `ktext`, `kring`,
  `knotifications`, `klock`, `kcommands`, `krun`, `kmount`, `kmountpoint`,
  `khelp`. Target device via `KDECONNECT_DEVICE_ID` or `KDECONNECT_DEVICE_NAME`.
- On m3 `~/.local/bin/kdeconnect-cli` is a wrapper script (not a link) that
  points the CLI at the app's private D-Bus (`/tmp/private_dbus_address`) and
  hides the harmless "error activating kdeconnectd" line. Without it the CLI
  can't see cachy. Never replace the wrapper by writing through a link into
  `/Applications/KDE Connect.app`.

### `modules/nerdfonts.zsh` and `modules/data/nerdfonts/`
- `nerd`/`fznf` fzf browser over ~11k glyphs (`--print`, `--name`, `--code`,
  `--utf`), `glyph-info`. The database is read only when the picker opens.

### `modules/spectrum.zsh`
- Vendored 256-color helper (`spectrum_ls`, `spectrum_bls`) from
  sykora/etc — leave attribution comment intact

### `modules/prompt_styles.zsh`
- Prompt-style switcher: `prompt-style <name>` and interactive `prompt` command
- Interactive picker prefers `fzf`; falls back to the Go binary at
  `prompt/picker/prompt-picker` (built from `prompt/picker/main.go`) when fzf
  is unavailable
- Presets live as TOML under `prompt/styles/` (`boxed`, `minimal`, `powerline`,
  `time`); also detects external prompt frameworks (Pure, Powerlevel10k,
  Spaceship) if installed

### `modules/lazy.zsh`
- heavy and infrequent functions loaded on demand
- fzf file manager, media tools, git utilities, note helpers, misc utilities

### `modules/loader.zsh`
- Discover lazy declarations, generate stubs, and dispatch the first call
- Keep discovery compatible with the declaration styles used in `lazy.zsh`

### `modules/git.zsh`
- standalone git aliases and helper functions
- `git-tui`/`gtui` interactive helper stack

### `modules/ghostty.zsh`
- Ghostty helpers, diagnostics, captures, and keybind lookup
- Loaded through `load_module` near the end of `.zshrc`, after the prompt and
  syntax highlighting

### Fish bridge
- Riley's Fish config (`~/.config/fish/config/modules/zsh-compat.fish`) makes
  zsh functions and aliases callable from Fish by running them in
  `zsh -ic`, and discovers names by scanning `~/.config/zsh/modules`. Renaming
  or removing a zsh function changes what Fish exposes too. See rd-fish.

### `completions/_*`
- Repo-local completion definitions added to `fpath`
- Name each file after its command and validate it with Zsh completion syntax

Files present in `modules/` are not automatically active. Confirm a file is
sourced before treating it as part of runtime behavior; for example, alternate
or work-in-progress copies such as `aliased.zsh` may exist without being loaded.

---

## Non-Negotiable Guardrails

1. Do **not** export `CONFIG`; keep `typeset -g CONFIG=...` behavior intact.
2. Do **not** use `readonly` for re-source-sensitive shared color vars; use `typeset`.
3. Do **not** create recursive alias patterns like `alias glow='glow ...'` (must use `command glow ...`).
4. Do **not** hardcode secrets in tracked files, and never print, `cat`, grep
   values from, or copy `secrets/*`, `~/.env` or `~/.config/fish/env.fish`. List
   them by name only.
5. Do **not** introduce eager loads for heavyweight tools that are intentionally lazy.
6. Do **not** break fzf keybinding conventions and global/default option layering.
7. Do **not** add bashisms where zsh-native syntax is expected.
8. Do **not** add lazy declarations that the loader's discovery patterns cannot parse.

---

## Coding Standards (Zsh)

- Prefer `function name() { ... }`
- Use `[[ ... ]]`, `(( ... ))`, `${var}` expansions
- Use `local` variables inside functions
- Guard early with explicit `return 1` when input/preconditions fail
- Send errors to stderr where appropriate (`>&2`)
- Avoid absolute `/Users/rd` when `$HOME` or existing env vars are correct
- Keep comments intent-focused (why/tradeoff), not noise

---

## fzf UX Conventions

Global style lives in `.zshrc` (`FZF_DEFAULT_OPTS`, ctrl bindings, theme). In per-function pickers:

- define only context-specific differences (`--prompt`, `--header`, `--preview`, etc.)
- preserve expected control affordances where applicable:
  - open
  - reveal
  - copy
  - toggle preview
- do not duplicate global color/border/pointer/marker defaults unless intentionally overriding

---

## Change Playbooks

### Add a new eager function

1. Implement in `modules/functions.zsh`
2. Keep startup footprint small
3. Add alias entry in `modules/aliases.zsh` if needed
4. Validate syntax and binding behavior

### Add a new lazy function

1. Implement in `modules/lazy.zsh`
2. Use a declaration form recognized by `loader.zsh`
3. Add an alias in `modules/aliases.zsh` if needed
4. Verify discovery creates the stub and the first call resolves the function

### Add/modify alias

1. Place in correct section in `modules/aliases.zsh`
2. Check for naming collisions (`alias <name>`, `type <name>`)
3. Ensure no accidental override of critical commands

### Touch startup-sensitive config

1. Edit `modules/config.zsh` (or `.zshrc`) carefully
2. preserve lazy-load patterns and ordering
3. measure startup if relevant (`PROFILE_ZSH_STARTUP=true zsh`)

### Adjust prompt

- Starship theme changes: `prompt/starship.toml` / `prompt/starship-terminal.toml`
- Custom prompt-style presets: add/edit TOML under `prompt/styles/`, wire
  switching logic in `modules/prompt_styles.zsh`
- Picker UI itself (Go TUI): `prompt/picker/main.go`, rebuild the
  `prompt/picker/prompt-picker` binary after changes
- avoid coupling prompt logic into unrelated module files

---

## Validation Checklist (Before Finishing)

- [ ] syntax check touched zsh files (`zsh -n <file>`)
- [ ] file masthead still has the shebang first, fully commented borders, aligned
      box art, consistent icon, and an accurate update date
- [ ] new sections use the target file's established header width and hierarchy
- [ ] comments describe intent and remain attached to the code they document
- [ ] no accidental leading spaces before top-level `#` banner lines
- [ ] lazy declarations are discovered and their generated stubs resolve
- [ ] no secrets added, no sensitive values echoed in commits
- [ ] no regressions to keybindings/interactive behavior
- [ ] no unnecessary hardcoded absolute home path
- [ ] docs updated when behavior contract changes

---

## Practical Test Commands

```bash
# Syntax checks
zsh -n ~/.config/zsh/.zshrc
zsh -n ~/.config/zsh/modules/config.zsh
zsh -n ~/.config/zsh/modules/functions.zsh
zsh -n ~/.config/zsh/modules/lazy.zsh
zsh -n ~/.config/zsh/modules/loader.zsh

# Reload shell
exec zsh -l

# Startup profiling (when relevant)
PROFILE_ZSH_STARTUP=true zsh

# Verify alias/function visibility
alias <name>
type <function_name>
```

---

## Frequent Risk Areas

- forgetting loader symbol updates after lazy function changes
- introducing startup regressions by moving heavy work into eager paths
- accidental command-shadowing via broad aliases
- fzf option duplication that drifts from global defaults
- changing long-standing key behavior (history vs reveal/open bindings)

---

## Completion Standard

A change is complete only when:

1. the edit is in the correct module,
2. lazy/eager boundaries remain intentional,
3. loader synchronization is correct,
4. visual hierarchy and comments match the surrounding file,
5. syntax passes,
6. behavior is consistent with Riley's formatting/tooling/workflow conventions.
