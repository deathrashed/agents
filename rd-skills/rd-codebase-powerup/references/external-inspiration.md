# External inspiration pass

Use this after the in-repo Pass 1 opportunities exist. The point is **feature
gaps and competitive ideas**, filtered hard so they remain implementable here.

## Inputs from the repo sample

Before leaving the tree, write down:

- Product one-liner and primary users  
- Existing surfaces (CLI verbs, HTTP routes, UI areas)  
- Known competitors / adjacent tools named in README, research, or docs  
- Domains worth skill-searching (e.g. “music metadata”, “docker compose”, “TUI”)

## find-skills

Follow the `find-skills` skill. Typical queries are domain + workflow, not the
repo name:

```bash
npx skills find "music library tagging"
npx skills find "cli tui progress"
```

Record for each hit: skill name, what it does, and whether this repo could
**Wrap** it, **Integrate** it, or only take **Inspiration**.

Do not recommend installing a skill as a product feature unless the user asked
for agent/tooling upgrades; usually map the skill’s *capability* onto a
first-party command or workflow.

## agent-browser / web

Prefer `agent-browser` when you need real UI/docs pages:

```bash
agent-browser skills get core
```

Then open competitor home/docs/changelog pages, snapshot, and extract
user-visible features this project lacks. Fallbacks: browse MCP, `WebFetch`,
or web search — always keep the source URL in the report evidence.

Good targets: official docs, feature comparison pages, release notes — not
random blogs.

## Keep / drop filter

| Keep | Drop |
|---|---|
| Feature attaches to an existing command, provider, screen, or config | Needs a new product category this repo has never approached |
| Competitor pattern matches a gap already hinted by tests/docs | Pure redesign / rebrand with no capability gain |
| Skill/tool can be wrapped behind current CLI JSON/scripted mode | Requires always-on SaaS the owner rejected |
| Evidence includes URL or skill name | Vague “add AI” with no surface |

## Report shape

Under **External Inspiration** (or **Ecosystem Scan** in the full template):

1. **Sources consulted** — skills queries + URLs  
2. **Recommended to implement** — ID, foothold path/command, source  
3. **Worth researching** — interesting but thin foothold  
4. **Not recommended** — one-line why  

External-backed findings still need normal IDs (`INT-001`, `FEAT-001`, …) and
may appear in the Top table only if they survive the foothold filter.
