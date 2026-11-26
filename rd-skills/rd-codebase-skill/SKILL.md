---
name: rd-codebase-skill
description: >
  Analyze any codebase and write an agent skill so other agents can operate
  that project's tools safely and effectively (CLI, scripts, tests, config,
  domain rules). Use when the user asks to create a skill for a repo, generate
  SKILL.md from a codebase, teach agents how to use this CLI/tool, onboard
  agents to a project, or "make a skill for working with X". Prefer evidence
  from the real tree over generic stack advice. Do not use for feature
  roadmaps (that is rd-codebase-powerup) or for inventing skills without a target
  repository.
---

# Codebase → Skill

Turn a repository into a **project skill**: instructions an agent follows to
run commands, respect safety rules, and change code the way this project
expects.

This is the sibling of `rd-codebase-powerup` (which finds *what to build*). Here
you find *how agents should work* and write that up as `SKILL.md`.

## Workflow

### 1. Confirm target and output location

- Target path (repo root). If unclear, ask once.
- Output path (default: `<repo>/.agents/skills/<slug>/` or
  `~/Projects/rd-agents/rd-skills/<slug>/` when the user is collecting first-party
  skills). Confirm before overwriting an existing skill.
- Slug: short kebab-case from the product/CLI name (e.g. `audio-agent`).

### 2. Sample the codebase (do not boil the ocean)

State inspection scope. Prefer:

1. **Entry surfaces** — CLI trees, `__main__`, package scripts, Makefile/just,
   HTTP routers, primary UI entry
2. **How to run** — README install/run, `docs/commands*`, `.env.example`,
   doctor/health commands
3. **Agent rules already present** — `AGENTS.md`, `CLAUDE.md`, `SKILL.md`,
   `CONTEXT.md`, ADRs
4. **Verification** — test command, lint, smoke scripts, CI workflow names
5. **Safety / irreversible ops** — trash vs rm, credentials, publish, sudo,
   library mutations, networked calls
6. **Domain vocabulary** — glossary terms agents must not invent

Heuristics: [references/inspect-heuristics.md](references/inspect-heuristics.md).

### 3. Extract the operating model

Build a short evidence table (keep privately; summarize in the skill):

| Concern | Evidence | Agent rule |
|---|---|---|
| Invoke CLI | … | exact argv patterns |
| Tests | … | exact command |
| Config/secrets | … | env names, never print secrets |
| Dangerous ops | … | ask / dry-run / trash |
| Layout | … | where new code goes |

Only include rules you can cite with a path or command. Mark uncertainty.

### 4. Optional inspiration (thin)

If the repo is a product CLI competing with known tools, a light pass with
`find-skills` / docs URLs can suggest **sections** worth covering (e.g. doctor,
scripted JSON mode). Do not copy foreign workflows that contradict this tree.

### 5. Write the skill package

Create:

```
<slug>/
├── SKILL.md          # required, lean, pushy description
└── references/       # optional: commands.md, safety.md, layout.md
```

Follow [references/skill-template.md](references/skill-template.md).

**Quality bar:**

- Frontmatter `name` + pushy `description` with trigger phrases
- Body under ~400 lines; put long command catalogs in `references/`
- Real commands from the repo (not invented)
- Explicit: scripted vs interactive; test/lint invocations; where not to write
- No secrets, no paste of `.env` values
- Progressive disclosure: point to repo docs instead of duplicating them

### 6. Validate and gate

- YAML frontmatter parses; description mentions when to use the skill
- Spot-check 2–3 commands against README or `--help` if cheap
- Show the user the draft path and a short summary; **do not** overwrite
  without confirmation if a skill already exists

## Relationship to other skills

| Skill | Role |
|---|---|
| `rd-codebase-powerup` | What to build next |
| `rd-codebase-skill` (this) | How agents operate this repo's tools |
| `skill-creator` | Meta craft of skills (structure/evals) |
| prompts.chat `skill-master` | Many stack-pattern skills under `.claude/skills/` — different goal |

## Anti-patterns

- Generic "be a helpful Python assistant" with no repo evidence
- Dumping the whole README into SKILL.md
- Teaching agents to `rm` when the project uses trash
- Ignoring existing `AGENTS.md` constraints
- Generating one skill per framework pattern (leave that to skill-master)
