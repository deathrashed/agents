# Tools

Sources: CX (Inspect and verify; CodeGraph; Toolkits and delegation; Personal
defaults), PRE, HA, G, RD.

- Search with `rg`. Batch independent read-only checks. [CX]
- Terminal-specific work targets Ghostty. Keep reusable CLI tools
  terminal-agnostic. [CX]
- Installed is not active. Don't run toolkit setup, install, update or
  mode-switch commands just because an instruction file mentions them
  (CC Presets, Caveman, RTK, GSD, Superpowers, OMX). [CX]
- Avoid competing output transformations. Get the exact source or output
  before edits that depend on exact text. [CX]
- CodeGraph: use it if `.codegraph/` exists. Initialise only when rd asks.
  Never in `~` or temp dirs. One index per worktree; never copy, link or
  reuse another checkout's index. Prefer watcher auto-sync; run `sync` only
  when the watcher is off or stale, and rebuild only after confirmed
  corruption. No destructive or admin CodeGraph lifecycle commands unless rd
  asks. [CX]
- Subagents: work directly by default. Delegate bounded, independent tasks
  with clear ownership; preserve other agents' changes; the lead integrates
  and verifies the result. [CX][PK]
- Treat cmux, Otty, Orca and hcom hooks as integrations: check the relevant
  session and runtime before diagnosing or changing them. [CX]
- OMX runtime workflows: only when rd asks and the runtime is available. On
  m3, read `~/.codex/guidance/omx-runtime.md` and the relevant skills first.
  [CX]
- Skills: load a skill when it's invoked or clearly useful. On m3, search the
  local library first with `~/.agents/skillz/_skillz_/bin/skillz-search
  "<task>"`; prefer `[curated]` results. `[repo]` results are references to
  read, never install. [CX][PRE][HA]
- Don't copy or link a discovered skill into `~/.agents/skills/` unless rd
  asks to activate it permanently; read it from its source path. [HA]
- A skill never authorises destructive, external or production actions on
  its own. [PRE]
- Memory: read it when helpful and verify anything that may have changed.
  [CX]
- After a structural change (moving or renaming folders, layout or taxonomy
  decisions, a tool's new home), update memory without being asked. On m3,
  update both `~/MEMORY.md` and `~/MEMORY.json`. [RD][HA]
- cachy has no home memory store (`~/MEMORY.md`, `~/MEMORY.json`, `~/Memory`
  absent on 2026-11-11). Ask rd where to record changes before creating one.
  [RD]
- For other memory updates, wait until rd asks. [CX]

## MCP servers (m3)

m3 has 8 GB RAM and every MCP server starts a process per session. Always-on
servers are limited to `fsearch`, `browse`, `codegraph` and `claude-mem`
(Codex); everything else stays defined but off. If a task needs a disabled
server, tell rd which profile or flag to restart with (Claude
`--mcp-config ~/.claude/mcp-profiles/<profile>.json`, Codex
`-c mcp_servers.<name>.enabled=true`) instead of re-enabling it permanently.
Details: m3 `~/AGENTS.md` "MCP servers". [HA]

## Token and output tools

What's installed and who owns it is in `~/.agents/manifest.toml`. [RD]

- rtk is the default output tool. On cachy it hooks Claude's Bash calls
  (`rtk hook claude`); check savings with `rtk gain`. [RD]
- One output tool per agent. Never run rtk and context-mode (or another
  output rewriter) on the same agent at once. [RD]
- No installs that edit the shared `AGENTS.md`, `CLAUDE.md` or the
  `~/.codex/AGENTS.md` link. Use hook-only or dry-run options, and check
  the `AGENTS.md` sha256 before and after. [RD]
- caveman is a cc-presets mode only, with telemetry off
  (`caveman telemetry off`). Don't install its CLI, proxy or plugin
  separately. [RD]
- Update the manifest whenever one of these tools changes. [RD]
