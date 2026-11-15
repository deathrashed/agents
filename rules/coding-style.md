# Coding style

Sources: CX (Work and communication; Inspect and verify), TR (Core Behavior,
Edits), PK (rules 3, 14, 15), KI (§5), AA (Working in this repo), MEM (preferences, automation-stack).

- Prefer small, reviewable changes, existing utilities and established
  patterns. Avoid new dependencies unless they're needed. [CX]
- Preserve existing code unless asked to change it. No cosmetic changes. [TR]
- Present edits as coherent chunks with enough context to apply them safely.
  [TR]
- Never hand-edit generated files. Change the source and re-run the
  generator. [KI]
- Make commands idempotent and safe to re-run. [KI]
- CLI tools: scripted mode must behave the same as interactive mode (JSON on
  stdout, no prompts). Gate interactive parts and test both paths. [AA]
- Tests must not touch real state or the network. Point state dirs at temp
  folders and mock networking. [AA]
- A feature isn't done without its tests. Run targeted tests first, then
  lint, typecheck and build. [PK][CX]
- For refactors and cleanup, name the behaviour to preserve and add
  regression coverage where it's at risk. [CX]
- Keep project docs (README, AGENTS.md, ADRs) in sync when behaviour changes.
  Record hard-to-reverse decisions as ADRs. [AA][PK]
- Prefer CLI-first, idempotent solutions. Include inline comments and error
  handling in code. [MEM]
- Work directly in the existing project. Don't create git worktrees unless
  there is a concrete need. [MEM]

## Commit messages

- Format: `<type> - <scope>: <summary>`, not `type(scope):`. Lowercase,
  imperative, under 72 characters, no emoji, no trailing period. Describe the
  change, not the files. [MEM]
- Types: `add`, `fix`, `clean`, `test`, `build`, `style`, `work`, `docs`,
  `perf`, `conf`, `tax`, `move`, `remove`. Not Conventional Commit types.
  `clean` = redundant or dead material; `work` = refactoring; `move` =
  relocation or renaming; `remove` = deliberately dropping a capability;
  `tax` = taxonomy. [MEM]
