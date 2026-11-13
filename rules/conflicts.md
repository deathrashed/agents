# Conflicts between sources

Found while building these rules on 2026-11-11. "Resolved" means this rule
set follows the rule shown. "Open" means rd needs to decide.

| # | Conflict | Status |
|---|---|---|
| C1 | CR says "always ask before deleting files" and "explain your approach before implementing". CX and PK say make reasonable reversible choices and don't stop for approval at each step. | Resolved: ask before destructive or irreversible actions; act without asking on reversible, authorised work (main.md rule 4). |
| C2 | The gentle-ai CodeGraph block (tool-generated) says initialise CodeGraph without asking. CX (rd) says initialise only when rd asks. | Resolved: CX. The tool block isn't rd's. |
| C3 | CX: update memory only when rd explicitly asks. The CX Notion block: agents may save durable decisions to Notion without asking. HA: update `~/MEMORY.md` and `~/MEMORY.json` after any structural change. | Resolved by rd (2026-11-11): update memory after structural changes. See `tools.md`. |
| C4 | PRE: search the skill library before every non-trivial task ("even a 1% chance"). CX: load skills only when invoked or clearly useful. | **Open.** For now: PRE applies on m3 only (its path exists only there); elsewhere CX. |
| C5 | TR's own storage example uses `convert-json-to-csv.applescript` (kebab-case), against its naming rule (spaces, Smart Sentence Case). | **Open.** For now: the naming rule. |
| C6 | TR stores scripts in `~/Scripts` (m3). G: folders in `~` are lowercase, `~/scripts` (cachy). | Resolved: per machine. |
| C7 | TR: never auto-create summary, plan or analysis Markdown. PK: keep plan status and ADRs updated. Cleanup tasks require reports. | Resolved: the project or the request wins; the TR rule is the global default. |
| C8 | TR machine facts (macOS Sequoia 15.7.2, 8 GB) date from 2026-01. | **Open [UNVERIFIED]:** possibly stale. Left out of main.md. |
