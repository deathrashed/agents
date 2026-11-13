# Filesystem layout

Sources: G (Layout conventions, Phase 5), HA, S. The m3 rules come from HA and
TR and are [UNVERIFIED] for current state.

## cachy (Linux)

- Folders in `~` are lowercase: `desktop documents downloads music pictures
  projects public templates videos applications backups docker kde obsidian
  scripts syncthing`. `~/Documents` → `~/documents` is a symlink; leave it.
  [G]
- Shell configs live in `~/.config/{fish,zsh,bash}`. `~/.config/fish` is a git
  repo. `~/.bashrc`, `~/.bash_profile` and `~/.zshenv` are intentional stubs.
  [G]
- Tool state follows XDG. Put session variables in
  `~/.config/environment.d/50-xdg.conf` and mirror them in
  `~/.config/fish/linux/conf.d/50-xdg.fish`. [G]
- User executables go in `~/.local/bin`, AppImages in `~/applications`. [G]
- Planned `~/projects` split: `active/`, `forks/` (remote not owned by
  `deathrashed`), `archive/` (90 days idle). Get rd's sign-off before moving
  anything. [G]
- `~/downloads` and `~/desktop` are inboxes, not storage. [G]

## Agent config (both machines)

- `~/.agents/AGENTS.md` is the single global instruction file; tool files
  symlink to it or point at this index. `~/.agents/skills/` is the shared
  skills dir (Agent Skills standard). [S]
- Keep one source of truth. Don't create per-tool copies of instructions or
  skills. [S][CX]

## m3 (macOS)

- `~/AGENTS.md` is the home-level router to `~/MEMORY.md`, `~/MEMORY.json`,
  `~/Memory/` and `~/KB/`. Read `~/KB/AGENTS.md` before editing KB files.
  [HA]
- Don't remove or overwrite another agent's memory store under `~/Memory/`.
  [HA]
