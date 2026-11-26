# Inspection heuristics

Use this when choosing what to sample. Adjust to the stack in front of you.

## Fast surface map

| Signal | Where to look |
|---|---|
| CLI | `**/cli/**`, `__main__.py`, `cmd/`, `cobra`/`clap`/`click` trees, `docs/commands.md` |
| HTTP/API | `**/routes/**`, `openapi*`, `**/api/**`, framework routers |
| UI | `**/pages/**`, `**/screens/**`, app entry + nav config |
| Config | `.env.example`, `config.*`, schema files |
| Domain glossary | `CONTEXT.md`, `AGENTS.md`, `docs/adr/` |
| Hidden tools | `tools/`, `scripts/`, `bin/`, `.scratch/`, `advisor-plans/`, `docs/archive/prototypes/` |
| Extension points | `*Provider*`, `*Plugin*`, registry dicts, adapter folders |

## Half-built detectors

- Commands referenced in docs/tests but missing from the command tree  
- Modules imported by few callers (candidate for a public command)  
- `--dry-run` / `--json` on some commands but not siblings  
- Prototypes or spikes under archive/scratch with no product home  
- TODO/FIXME near user-facing verbs (`export`, `sync`, `doctor`, `watch`)

## Anti-patterns

- Reading every file under `src/` “just in case”  
- Recommending a dashboard/auth/marketplace with no existing surface  
- Treating archived plans as unfinished product requirements without checking status  
- Ecosystem name-dropping without a repo foothold
