# rd's global agent instructions (index)

Owner: rd (Riley). Machines: `cachy` (CachyOS, KDE Plasma 6, Wayland) and `m3`
(MacBook Air M3, macOS). Every tool's global instruction file points here.
The current request, then project `AGENTS.md`/`CLAUDE.md`, override this file
within their scope. Source keys are listed in `rules/sources.md`.

## Always

1. Use the smallest useful workflow. Carry authorised work through to
   verification and a short report. [CX]
2. Inspect the real file, config or runtime before concluding. Keep
   "installed", "configured" and "observed working" apart. [CX]
3. Back every claim with proof: command output, `file:line`, or a docs/source
   URL. Mark anything else **[UNVERIFIED]**. Never guess; say what is
   uncertain. [S][TR][PK]
4. Ask first, then wait, for: `sudo`; deleting or overwriting user data;
   removing software, Docker volumes or credentials; publishing or pushing;
   anything irreversible or that costs money. Just make low-risk, reversible
   choices. [G][CX][PK][CR]
5. Remove with the Trash (`gio trash --` on Linux, Finder Trash on macOS),
   never `rm`, except for caches known to be safe. [G][CX]
6. Before changing a file outside a git repo, keep a timestamped backup, and
   log the change with an undo line. [S][G]
7. Never print, log, commit or paste secrets. List secret files by name, size
   and date only. [G][PK]
8. Preserve existing work and structure. No resets, broad deletes, cosmetic
   changes or invented requirements. [CX][TR]
9. Write plainly. Lead with the result, be concise, and cite paths with line
   numbers. [CX][CR][TR]
10. Don't create summary, plan or analysis Markdown files nobody asked for.
    [TR]

## Topic files: read when…

- `rules/safety-and-changes.md`: before any delete, move, cleanup, `sudo`,
  config edit outside a repo, or anything touching credentials.
- `rules/filesystem-layout.md`: before creating, moving or naming anything in
  `~`, or touching dotfiles, XDG paths or `~/.agents`.
- `rules/working-and-reporting.md`: at the start of a multi-step task, and
  before writing the final report.
- `rules/coding-style.md`: when writing or changing code, tests, generators
  or project docs.
- `rules/tools.md`: when choosing CLI tools, searching, using skills,
  CodeGraph or memory, or delegating to subagents.
- `rules/scripts-and-notes.md`: when writing personal scripts or their
  Obsidian docs.
- `rules/conflicts.md`: when two sources disagree. Open items await rd.
- `rules/sources.md`: to check where a rule came from.

`rules/claude-mem-context.md` is written by the claude-mem tool, not by rd.
