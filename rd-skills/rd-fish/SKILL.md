---
name: rd-fish
description: >
  Expert context for Riley's Fish shell config at ~/.config/fish (repo
  deathrashed/fish), shared by cachy (CachyOS, Fish is the login shell) and m3
  (macOS, Fish installed, zsh is the login shell). Use for any work on Fish
  startup, the config/linux/macos platform split, functions, modules, aliases
  and abbreviations, fisher plugins, prompt profiles, the zsh bridge, the ~/.env
  cache, running commands on cachy over ssh, or the repo's banner and comment
  style. For Zsh on m3 use rd-zsh.
---

# Riley Fish Config Skill

## Environment

| | cachy | m3 |
|---|---|---|
| OS | CachyOS Linux, KDE Plasma 6, Wayland | macOS 27 |
| Fish | 4.9.3, **login shell** | 4.9.3 (`/opt/homebrew/bin/fish`), login shell is zsh |
| Platform folder | `linux/` | `macos/` |
| zsh config | none | `~/.config/zsh` (rd-zsh) |
| `env.fish` (secrets cache) | absent | present (generated, git-ignored) |

- Repo: `github.com/deathrashed/fish` (private), checked out at `~/.config/fish`
  on both machines. Both were on commit `807e6b9` ("Move machine-specific startup
  into linux/ and macos/") on 2026-11-26. cachy had 12 uncommitted changes then,
  so pull or compare before editing on one machine what the other also changed.
- **Commands sent to cachy over ssh run in Fish.** POSIX syntax (`. file`,
  heredocs `<<EOF`, `VAR=$(...)`) fails there. Wrap them:
  `ssh cachy "bash -c '…'"`, or pipe a script to `bash -s`.

## Layout

```text
~/.config/fish/
├── config.fish              # one line: sources config/config.fish
├── config/                  # shared by both machines
│   ├── config.fish          # the loader (see Startup)
│   ├── conf.d/30-modules.fish
│   ├── modules/             # utilities, git, ghostty, zsh-compat
│   ├── functions/           # one function per file (ab, bak, c, fe, ff, fin, mkcd, prompt_profile, …)
│   ├── completions/
│   ├── fish_plugins         # fisher plugin list
│   └── fish_variables       # tracked universal variables (no secrets; keep it that way)
├── linux/                   # cachy only
│   ├── conf.d/              # nix env, REA (60/61), ported aliases, ccr, zz-config, zz-linuxbrew
│   ├── functions/           # fish_ssh_agent, install-deb
│   ├── completions/
│   ├── profiles/garuda.fish
│   └── vendor/              # cachyos-config.fish (repo copy of the system file), done, nix-env
├── macos/                   # m3 only
│   ├── conf.d/              # 10-environment, 20-interactive, 40-preferences, plugin conf
│   │                        # (pure, fzf, z, nvm, done, autopair, ggl), atuin/uv env, zz-local
│   ├── functions/           # ~93, mostly plugin internals (_fzf_*, _autopair_*, _pure_*)
│   ├── completions/         # docker, kubectl, orbctl, otty, scrobbler
│   ├── modules/music.fish
│   ├── aliases.fish         # ~359 aliases
│   └── abbreviations.fish   # ~65 abbreviations
├── docs/                    # prompts.md (prompt profiles), views.md (README banner), icon/
├── archive/                 # generated backups, legacy z data
├── local.fish               # optional, git-ignored, machine-local
├── prompt-profile.fish      # written by prompt_profile, git-ignored
└── env.fish                 # generated secrets cache, git-ignored (m3)
```

## Startup

`config.fish` → `config/config.fish`, which:

1. Picks the platform folder from `uname -s` (`Darwin` → `macos`, `Linux` → `linux`).
2. Prepends `config/functions` and `<platform>/functions` to `fish_function_path`,
   and the same for completions.
3. Sources `local.fish`, then `prompt-profile.fish` if present.
4. Sources every `*.fish` in `config/conf.d`, then `<platform>/conf.d`, in
   filename order. Number prefixes set the order (`10-`, `20-`, `40-`, `zz-` last).
5. Sources `<platform>/aliases.fish` and `<platform>/abbreviations.fish`.
6. macOS only: sources `~/.fish_profile` if present.
7. Applies the saved prompt profile.

`config/conf.d/30-modules.fish` sources `config/modules/{utilities,git,ghostty,
zsh-compat}.fish`, plus `macos/modules/music.fish` on macOS.

## Where Things Go

| Change | Put it in |
|---|---|
| Behavior that's the same on both machines | `config/` |
| Something only one machine has (tool, path, package manager) | `linux/` or `macos/` |
| A reusable command | one file per function in `config/functions/<name>.fish` (autoloaded), or the platform `functions/` |
| A group of related commands | a module in `config/modules/`, added to the loop in `30-modules.fish` |
| Startup environment or settings | a numbered file in the platform `conf.d/` |
| Aliases and abbreviations | `<platform>/aliases.fish`, `<platform>/abbreviations.fish` |
| One machine's private tweaks | `local.fish` (not committed) |

Keep the meaning the same on both machines and only the platform detail
different. If something exists only on m3 today (most aliases), say so rather
than copying it to `config/` untested on Linux.

## Plugins (fisher)

`config/fish_plugins`: `pure-fish/pure`, `franciscolourenco/done`,
`jorgebucaran/fisher`, `jethrokuan/z`, `patrickf1/fzf.fish`,
`jorgebucaran/nvm.fish`, `yo-goto/ggl.fish`. Their conf and functions live under
`macos/`, so on cachy these plugins aren't present unless installed there.
Don't hand-edit plugin-owned files (`_fzf_*`, `_pure_*`, `_autopair_*`, `__z*`,
`_nvm_*`); change settings in `40-preferences.fish` instead.

## Prompt Profiles

`prompt_profile [plain|pure|cachy|garuda|compact]` switches prompt, greeting and
`ls` style, and writes `prompt-profile.fish` (not committed). Details are in
`docs/prompts.md`. `garuda` and `compact` use Starship themes, which keep the
Fish prompt when Starship isn't installed.

## The Zsh Bridge (m3)

`config/modules/zsh-compat.fish` makes every zsh function and alias in
`~/.config/zsh/modules` callable from Fish. It runs them in `zsh -ic`
(`__riley_zsh_run`, `__riley_zsh_alias`) and discovers names with `rg`, skipping
protected builtins. It does nothing when `~/.config/zsh` is missing (cachy).
Fish-native versions in the other modules win. When you port a zsh command to
Fish, write it natively and keep the name, so the bridge stops wrapping it.

## Secrets

- `~/.env` holds the shared credentials. On m3, `macos/conf.d/zz-local.fish`
  converts it to Fish with `~/.local/lib/env-keys/env_keys.py fish` only when its
  mtime changes, caches the result in `env.fish` (mode 600, git-ignored), and
  sources it.
- **Never print, `cat`, grep values from, copy or commit `env.fish`, `~/.env`
  or anything under `secrets/`.** List them by name only. To check whether a
  variable exists, test it (`set -q NAME`), don't echo it.
- Keep `fish_variables` free of secrets. It is committed.

## House Style

Module files use the same banner family as the zsh repo, labelled
`F I S H   M O D U L E`:

```fish
#                                ╭───────────────────────────╮
#╭───────────────────────────────┤   F I S H   M O D U L E   ├───────────────────────────────╮
#│                               ╰───╮   •────  ────•   ╭───╯                               │
#│        •───────•───────•───────•  │       G I T       │  •───────•───────•───────•        │
#│                                   ╰───────────────────╯                                   │
#│                                                                                           │
#│                         Commits • snapshots • remotes • workflows                         │
#│                                                                                           │
#╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

- Copy the banner from the closest sibling module and change the name, icon,
  keywords and date. Never draw one from memory. The width must stay the same.
- Larger modules (e.g. `zsh-compat.fish`) use the full masthead with FIGlet art,
  the repo URL, a purpose line and a `L A S T  U P D A T E D` footer.
- Every function gets `--description "..."`. Write descriptions in sentence case.
- Comments explain why, not what, and the same rules as rd-zsh apply.

## Fish Idioms

- `set -l`/`set -g`/`set -gx`, never `export VAR=` in new code. `set -U` only on purpose
  (it's written to the committed `fish_variables`).
- `test`, `string`, `path`, `contains`, `count`. Never `[[ ]]`. Fish 4 accepts
  `$(...)` and `&&`, but the repo mostly uses `(...)` and `; and`/`; or`: match
  the neighbouring code.
- `command name` to bypass a function of the same name. No recursive wrappers.
- Interactive-only setup belongs behind `status is-interactive`.
- Use `$__fish_config_dir`, never a hardcoded `/Users/rd` or `/home/rd`.

## Validation

```fish
fish --no-execute ~/.config/fish/config/config.fish      # syntax check (any file)
fish_indent --check <file>                              # formatting
fish -c 'functions -q <name>; and type <name>'          # function resolves
fish -l -c exit                                         # full startup, both machines if shared
```

Before finishing:

- [ ] syntax check every touched file
- [ ] shared changes in `config/` work on both platforms (or are guarded)
- [ ] no secrets added, no secret values printed in output or commits
- [ ] banners copied from a sibling, same width, date updated
- [ ] cachy and m3 checkouts reconciled if both changed (no force-push)
