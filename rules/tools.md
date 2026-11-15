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

## Token savers

What's installed, versions and owners: `~/.agents/manifest.toml`.
`agents-check` (checks `output_hooks`, `telemetry`, `token_tools`) proves
the wiring. [RD]

One tool per layer per agent, from the tool call to the model's reply: [RD]

1. Tool output: **rtk**. Hooks: Claude (`rtk hook claude`), Cursor
   (`rtk hook cursor`), omp/pi (`~/.config/pi/extensions/rtk.ts`),
   opencode (plugin), Codex (`rtk hook codex`, Bash matcher in
   `~/.codex/hooks.json`, also in cc-presets' bundle so a preset switch
   keeps it). Don't run `rtk init -g --codex` as-is: it adds an `@RTK.md`
   line to `~/.codex/AGENTS.md` (the shared link); merge only its hook.
   kilo and agy get rules files only; Grok has no rtk hook (its Claude and
   Cursor hook compat is off). Check savings with `rtk gain`. Never add a
   second output rewriter to an agent that runs rtk.
2. Context/API compression: **headroom**, per session only:
   `headroom wrap <agent>` (claude, codex, grok, opencode, omp; cursor
   prints manual steps). No permanent `*_BASE_URL` proxy env anywhere, no
   `headroom wrap grok-build` (it edits `~/.grok/config.toml`), never
   `headroom learn --apply` (it writes CLAUDE/AGENTS files). Keep
   `HEADROOM_OUTPUT_SHAPER` off.
3. Reply style: **at most one always-on** of ponytail or caveman per agent.
   - ponytail: native plugin on Claude, opencode, omp, Grok, kilo; Cursor
     hooks from `~/Projects/_forks/ponytail`
     (`node scripts/cursor-hooks.js install|uninstall`). Not on Codex.
     Never copy its `AGENTS.md`. Its ledger is a local CSV under
     `~/.config/ponytail/`; keep `webhookUrl` empty.
   - caveman 4.x upstream: Codex always-on (SessionStart hook in
     `~/.codex/hooks.json`, skills in `~/.agents/skills`). Claude has the
     `caveman@caveman` plugin on demand only
     (`CAVEMAN_DEFAULT_MODE=manual` in `~/.claude/settings.json`), because
     ponytail is Claude's always-on style. No caveman on opencode or Grok
     (their installers write AGENTS.md blocks). Don't install the caveman
     CLI rocks (proxy, Auto routing, Browse). The cc-presets caveman 1.3.4
     (hooks, MCP, `~/.caveman/bin`, `caveman` CLI) is removed; the
     `caveman-learn` skill needs the upstream CLI, so it doesn't work until
     that is installed on purpose (telemetry off first).

Rules for every token tool: [RD]
- No install that edits the shared `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `~/.grok/AGENTS.md` or the `~/.codex/AGENTS.md` link. Use plugins,
  hook-only or dry-run options, and compare the instruction-file sha256
  before and after.
- Telemetry off: rtk consent no; caveman `~/.caveman-cloud/config.json`
  telemetry off; headroom `HEADROOM_TELEMETRY=off` and
  `HEADROOM_BEACON=off` (fish universal, plus `launchctl setenv` on m3);
  ponytail has none.
- Pin versions and update the manifest whenever one changes.
- Measure before keeping: `rtk gain`, `headroom savings`,
  `/ponytail-gain`, `/caveman-stats`. Drop a tool that doesn't pay for
  itself.
