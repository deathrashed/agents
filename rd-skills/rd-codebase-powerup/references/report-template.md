# Report templates

## Compact report (default)

```markdown
# Codebase Power-Up Report

## Executive Summary
[2–4 sentences: highest-leverage moves and why]

## Inspection Scope
[What was sampled; what was skipped]

## Top Power-Up Opportunities
| ID | Priority | Category | Opportunity | Evidence | Impact | Effort | Risk | Confidence |
|---|---|---|---|---|---|---|---|---|
| LEV-001 | P1 | Existing capability leverage | ... | `path` / command | ... | S | Low | High |

## Details
### LEV-001 — …
- **Why it matters:**
- **Recommended implementation:**
- **Action Type:** Build | Wrap | Integrate | Document
- **Affected files/modules:**
- **Dependencies:** none | list
- **Effort / Risk / Confidence:**

## Implementation Gate
Pick finding IDs to implement. A patch plan comes next before any edits.
```

When the external pass ran, add:

```markdown
## External Inspiration
### Sources consulted
- find-skills: …
- URLs: …

### Recommended to implement
| ID | Opportunity | Local foothold | Source |
|---|---|---|---|

### Worth researching
…

### Not recommended
…
```

## Full report (deep audit / formal roadmap)

Add these sections after the compact core:

1. **Project Understanding** — purpose, users, feature set, workflows, extension points, key modules inspected  
2. **Existing Capability Map** — commands, scripts, APIs, plugins, templates, docs already present  
3. **External Inspiration / Ecosystem Scan** (if run) — sources, Recommended / Worth researching / Not recommended  
4. **Hidden Capability Leverage** — asset → location → what it can become  
5. **Suggested Roadmap** — Quick wins / High-leverage / Larger platform / Experimental  

Keep the same ID scheme and Implementation Gate.
