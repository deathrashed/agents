# Inspection heuristics

## Detect the primary surface

| Signal | Likely surface |
|---|---|
| Click/Typer/Clap/Cobra/`argparse` trees, `docs/commands.md` | CLI product |
| FastAPI/Flask/Express routers, OpenAPI | HTTP API |
| `package.json` scripts + `src/` UI | App + npm scripts |
| `justfile` / `Makefile` / `Taskfile` | Task runner |
| Only `src/` library, no CLI | Library — skill focuses on import/test/release |

## Must-find artifacts

- Install / run blocks in README
- Test invocation (`pytest`, `cargo test`, `npm test`, …) as actually documented
- Lint/format commands if present
- `.env.example` key *names* only
- `AGENTS.md` / project skill already in-tree
- Safety: trash, dry-run, `--yes`, network guards in tests

## Command extraction

Prefer in order: `docs/commands.md` → `--help` on primary binary → README →
CI workflows. Record exact strings agents should run.

## Layout rules

Note package layout (`src/<pkg>/`), where CLI lives, where tests live, and any
"new command goes in X module" convention from AGENTS.md or ADRs.
