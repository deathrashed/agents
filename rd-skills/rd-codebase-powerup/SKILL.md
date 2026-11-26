---
name: rd-codebase-powerup
description: >
  Find practical ways to expand a codebase's capabilities: missing commands,
  power-user workflows, plugins, integrations, and especially hidden or
  half-built features that should be exposed or reused. Also scan comparable
  products on the web and the agent-skills ecosystem for implementable
  inspiration that fits this project's surfaces. Use whenever the user asks
  what to build next, how to power up / level up a repo, what's missing, what
  else the CLI/API can do, how to expose buried tools, wants competitive
  feature ideas, or wants a feature roadmap that fits the existing
  architecture — even if they never say "power-up". Prefer leverage of what
  already exists over inventing greenfield features. Do not use for pure
  refactors, performance-only work, or bug hunts unless those directly unlock
  a new user-facing capability.
---

# Codebase Power-Up

Identify high-leverage capability expansions that fit the repo as it is. The
goal is a short, evidence-backed set of power-ups the user can approve — not a
generic wishlist and not an implementation dump.

Focus on **new user workflows and discoverability**. Skip performance and
refactor ideas unless they clearly unlock a capability.

## Workflow

### 1. Inspect with a sampling plan (do not boil the ocean)

Large repos cannot be read file-by-file. Build a deliberate sample, then state
exactly what you covered. Prefer:

1. Entry surfaces — CLI command tree, HTTP routes, UI entrypoints, `README` /
   `docs/commands`, package scripts
2. Domain context — `CONTEXT.md`, `AGENTS.md`, ADRs, product specs under
   `.scratch/` or `docs/`
3. Extension points — provider/plugin registries, config schemas, hook tables
4. Half-built / hidden assets — `tools/`, prototypes, unfinished modules,
   advisor plans, commented command stubs
5. Tests that document intended behavior for missing UX

If something important was not inspected, say so. Never claim full-repo
coverage you did not do. For inspection heuristics, see
[references/inspect-heuristics.md](references/inspect-heuristics.md).

### 2. Rank leverage before invention

Score candidates so **expose / wrap / connect existing code** beats greenfield
unless evidence shows a real gap. Prefer:

- Promoting a script or helper into a command
- Wiring two modules that already exist
- Making a dry-run / JSON / batch path discoverable
- Documenting or indexing a buried workflow

Avoid trendy features with no foothold in the tree.

### 3. Two-pass opportunity search

**Pass 1 (required):** up to **3** highest-confidence opportunities from:

1. **New functionality** — commands, flags, endpoints, import/export, repair /
   check / preview modes
2. **Power-user workflows** — batch, watch, presets, scripting, pipelines,
   keyboard/CLI-first paths
3. **Existing capability leverage** — expose, wrap, connect, or index what is
   already there

**Pass 2 (optional):** add more only with concrete evidence, from:

4. Integrations  
5. Developer / admin tooling  
6. Extensibility  
7. AI-native enhancements  
8. Product / platform expansion  

If the repo has no CLI, API, or UI surface, stay inside that constraint and say
when the surface cannot support more.

### 4. External inspiration (feature gaps outside the tree)

After Pass 1, run a **project-shaped** external pass so recommendations are not
only “what’s already half-built.” Keep only ideas that fit an existing CLI,
API, UI, config, or extension point.

**When to run (default on for product CLIs/apps; skip for tiny libraries):**

- The user wants gaps, inspiration, competitors, or “what should we build”
- Pass 1 found fewer than 3 strong opportunities
- The project clearly competes with known tools (music clients, devops CLIs, …)

**How — use the right skills/tools:**

1. **Agent skills ecosystem** — read and follow the `find-skills` skill
   (`npx skills find …` / skills.sh). Search for skills that match this
   project’s domain and workflows (tagging, downloads, Docker, TUI, etc.).
   Note installable capabilities the repo could wrap or mirror.
2. **Live product / docs inspiration** — prefer the `agent-browser` skill for
   interacting with competitor sites, docs, or demos (load
   `agent-browser skills get core` first). If that CLI is unavailable, use
   the browse MCP, WebFetch, or web search instead — still cite URLs.
3. **Map each external idea → local foothold** — reject anything with no
   command, route, provider, config, or prototype to attach to.

Details and filters:
[references/external-inspiration.md](references/external-inspiration.md).

Omit this section only when the surface truly cannot absorb external ideas
(e.g. a tiny pure library with no user surface) or the user forbids network.

### 5. Report, then gate

Produce the **Codebase Power-Up Report** and **stop**. Do not install tools,
edit code, or implement until the user picks finding IDs.

Default to the **compact report**. Use the **full report** only when the user
asks for a deep audit, a formal roadmap, or a large multi-surface review.
Templates live in
[references/report-template.md](references/report-template.md).

## Confidence and IDs

- Assign stable IDs (`CMD-001`, `FLOW-001`, `LEV-001`, `INT-001`, …).
- Mark **High** confidence only with concrete evidence (`path`, symbol, or
  command). Otherwise **Medium** or **Low**.
- Every opportunity needs: why it matters, action type
  (`Build` / `Wrap` / `Integrate` / `Document`), effort, risk.

## After the user picks IDs

Write a **Patch Plan** first (files, commands, deps, migration, rollback,
tests). Edit code only after they approve that plan.
