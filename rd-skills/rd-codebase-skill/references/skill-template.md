# Generated project-skill template

Use this shape for the **output** skill (the one agents will load later).

```markdown
---
name: <slug>
description: >
  How to work in the <Product> repository: run the CLI, tests, and safe
  workflows. Use whenever editing <slug>, running <binary>, or operating
  its library/tagging/download flows — even if the user only names a
  subcommand.
---

# <Product>

One paragraph: what it is and who it is for.

## When this skill applies

Bullet trigger situations.

## Quick commands

| Intent | Command |
|---|---|
| Help / doctor | … |
| Tests | … |
| Lint | … |

Details: [references/commands.md](references/commands.md) if the table grows.

## Safety

- Secrets: never print or commit …
- Destructive: ask before …; prefer trash / dry-run …
- Network: tests mock …; do not …

## Layout

Where CLI, library, tests, and docs live. Where new commands/modules go.

## Domain rules

Glossary terms and invariants from CONTEXT.md / ADRs (short).

## Verification before done

Exact test/lint/smoke commands for this repo.

## Do not

Anti-patterns specific to this tree.
```

### Optional reference files

- `references/commands.md` — fuller command catalog  
- `references/safety.md` — irreversible ops detail  
- `references/layout.md` — module map  

Keep SKILL.md actionable alone; references are progressive disclosure.
