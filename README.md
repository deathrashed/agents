# agents

rd's own global instructions for AI coding agents (Claude Code, Codex,
Gemini, Cursor, Crush, opencode and others), shared between two machines:
`cachy` (CachyOS, Linux) and `m3` (MacBook Air, macOS).

This repo replaces the old `deathrashed/agents`, now
`deathrashed/agents-archive`. It holds only rd's writing. Third-party skills
are managed by `npx skills` (lockfile `~/.local/state/skills/.skill-lock.json`)
and are never committed here.

## Layout

| Path | What it is | Applied on each machine as |
|---|---|---|
| `AGENTS.md` | One-line pointer every tool reads | `~/.agents/AGENTS.md` (tool files such as `~/.claude/CLAUDE.md` link to it) |
| `main.md` | Short index: always-on rules plus topic files | `~/.agents/main.md` |
| `rules/` | Topic files, read when relevant | `~/.agents/rules/` |
| `machines/<host>/manifest.toml` | Third-party agent tools on that machine: owner, version, wiring, telemetry | `~/.agents/manifest.toml` on that host only |

Paths in the rules are written as `~/...` and tagged with the machine they
apply to (`cachy` or `m3`) where the two differ. Don't hardcode
`/home/rd` or `/Users/...`.

`machines/m3/` doesn't exist yet; the Mac's manifest gets written when its
`~/.agents` is migrated.

## Applying

Not wired up yet. The plan is for each machine to link these files into
`~/.agents` (or have chezmoi manage them), leaving skills and tool state in
`~/.agents` untouched. See the change log on cachy
(`~/.local/state/system-cleanup/log.md`) for what has been applied.

## Health check

`just agents-check` (or `scripts/agents-check`) is a read-only check of
`~/.agents` and every agent that reads it. Tool paths live in
`checks/agents.toml`. Flags: `--json`, `--config=PATH`. Exit 0 = no FAIL,
1 = at least one FAIL, 2 = could not run. It never writes and prints file
names only, never secret values. Needs python 3.11+ (or `tomli`).

Weekly routine: `just -f ~/projects/rd-agents/justfile agents-check --json`
