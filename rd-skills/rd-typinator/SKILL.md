---
name: rd-typinator
description: General Typinator skill for syntax, forms, scripts, pickers, exports, Includes resources, and direct .tyset editing. Use when working on Typinator abbreviations, sets, scripts, menus, exports, documentation, or Typinator package structure.
---

# Typinator Skill

## Goal

Work correctly with Typinator as a whole:
- expansion syntax
- input forms and pickers
- Includes scripts, reference assets, and text resources
- exported CSV/TXT sets when they are explicitly in scope
- direct `.tyset` rule-set editing
- organized script/reference architecture

This is a general Typinator skill first, not just an export-auditing skill.

## Environment assumptions

- Typinator Includes path:
`/Users/rd/.config/typinator/Sets/Includes`
- Typinator local docs and resources are maintained in Includes:
`/Users/rd/.config/typinator/Sets/Includes`

## Source-of-truth locations

Prioritize these in this order when both exist:
1. Official Ergonis sources:
- `https://help.typinator.ergonis.com/hc/en-us`
- local topic-first docs under `Includes/Documentation`
2. Local Typinator runtime resources in Includes:
- `/Users/rd/.config/typinator/Sets/Includes`
3. Direct export artifacts when import-compatible file shape matters:
- `/Users/rd/.config/typinator/Sets/Includes/Exported/Direct Exports`

Interpretation:
- For Typinator behavior and syntax, prefer `Includes/Documentation`.
- For runtime source assets referenced by abbreviations, pickers, and lookup scripts, prefer `Includes/Reference`.
- For reusable insertable text and templates, prefer `Includes/Text`.
- For import-compatible exported file format, prefer `Direct Exports`.
- Ignore old vault/Obsidian references unless the user explicitly asks for them.

## Authority model

Not all local docs carry the same weight.

Use these maintained references instead of hard-coding source lists here:
- `references/typinator-feature-map.md`
  Topic-to-source navigation map for the best local and online sources per feature area.
- `references/official-reference-ingest.md`
  Compact memory of what has already been ingested from official local and online sources.
- `references/typinator-feature-map-sources.json`
  Curated manifest that drives the generated feature map.

Authority order:
1. Official Ergonis help-center articles and categories.
2. Local topic docs and Ergonis-authored User's Guide material.
3. Focused local topic references and trusted project notes.
4. Derivative local summaries and convenience notes.

Do not treat unrelated clippings or off-topic articles as Typinator authority.

## Documentation model

Treat the local Includes tree as three layers:
- `Includes/Documentation`
  Topic-first human-readable docs, examples, project notes, and generated indexes.
- `Includes/Reference`
  Runtime CSV/TXT assets and lookup sources that abbreviations, pickers, and scripts reference.
- `Includes/Text`
  Curated reusable insertable text resources and templates.

Current interpretation:
- prefer `Includes/Documentation` for formal behavior and feature rules
- use `Includes/Reference` for CSV/search/terminal/runtime lookup material
- use `Includes/Text` for snippets, template fragments, and include-friendly text
- do not merge these categories blindly; organize by purpose

## Mandatory doc-first read

Before generating or editing non-trivial Typinator content:

1. Read the feature-area entry in:
- `references/typinator-feature-map.md`

2. Use `references/official-reference-ingest.md` as a compact memory refresh for already-ingested official behavior.

3. Read the specific local and online sources listed for the relevant feature area in the feature map.

4. When the task is broad, architectural, or cross-feature, start with the core docs:
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Scripts/Creating-Typinator-Scripts.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Scripts/Typinator™ Scripting Guide.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Regex/Typinator™ Regular Expressions.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Core/Introduction for AI Models.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Core/Typinator Complete Reference.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Core/Advanced Features & Techniques.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Search/Quick Search & Productivity Tips.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Text/Text Formatting & Hyperlinks.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Core/Tips Tricks & Workflows.md`
- `/Users/rd/.config/typinator/Sets/Includes/Documentation/Core/Typinator User's Guide.md`

5. Read runtime assets under `Includes/Reference` and `Includes/Text` only when the task depends on those actual files or their current contents.

6. Regenerate the feature map with `scripts/build_feature_map.py` when the local documentation tree or curated manifest changes materially.

When guidance conflicts, prefer official Ergonis help-center guidance and local canonical docs over local derivative summaries.
If a task depends on product behavior that may have changed, check the live help center before finalizing.

## Core rules

1. Output valid Typinator syntax only.
2. Keep UI tokens compact to avoid blank-line leakage.
3. Use readable labels for form fields.
4. Avoid giant inline option payloads when values are complex.
5. Prefer menu/picker patterns for large sets, but keep them maintainable.
6. For reference-backed lookup menus, prefer a small Includes script with one parameter over large inline `{/Shell ...}` heredocs inside the expansion.
7. Menu-returned reference text is inserted verbatim; do not expect fetched text to be re-expanded by Typinator. Use literal placeholders like `<SOURCE>` in reference files instead of `{{?...}}`.
8. Default to keeping original exports untouched and writing cleaned copies, except when the user explicitly targets `Direct Exports` for in-place content-only edits.
9. Use canonical script paths in exports and live rules.
10. If abbreviation length constraints are requested, enforce them globally.
11. Edit content only unless explicitly asked otherwise: do not change file type, extension, delimiter, quoting mode, encoding, BOM, newline convention, or export dialect.
12. When working from Direct Exports, preserve exact import format and only modify abbreviation/expansion text content.
13. For `.tyset` updates, do not edit package internals directly (`Index`, `X*` files); use Typinator's AppleScript dictionary to create/update rule sets and rules safely.
14. Treat scripts with spaces in filenames as unsafe for direct Typinator placeholders when parameters are involved; prefer no-space wrapper scripts or renamed canonical script files.
15. Prefer direct `.tyset` editing for live sets when the user wants the installed Typinator sets changed.
16. Use exported CSV/TXT files when the user explicitly wants import/export artifacts changed.
17. Understand that Includes placeholders can point to plain text, rich text, or scripts; rich formatting survives only in formatted expansions.
18. Remember that script placeholder syntax includes the file extension in the actual placeholder, even if the menu hides the extension.
19. Treat input forms, variables, calculations, script parameters, comments, and random text as combinable first-class Typinator features.
20. Prefer set-level defaults and word-break behavior when designing large groups of abbreviations, rather than repeating item-level settings manually.
21. Remember that Typinator supports plain text, formatted text, picture, and HTML expansion types, each with different compatibility expectations in target apps.
22. Use descriptions and inline comments as part of the product’s search and maintainability model, not as optional decoration.
23. Treat prefixes, suffixes, magic keys, and set architecture as first-class abbreviation design tools for avoiding conflicts.

## Script correctness rules

1. Script invocation format:
- `{folder/scriptName argument}` with optional single argument.
- Typinator supports one argument only; split it inside the script when multiple values are needed.

2. Parameter hint comments must match language syntax exactly:
- AppleScript: `-- parameter: ...`
- JavaScript: `//-- parameter: ...`
- Shell/Python/etc.: `#-- parameter: ...`
- Swift: `//-- parameter: ...`

3. Runtime and UX constraints:
- AppleScript should complete in under about one second when possible.
- Other script types are hard-terminated at about five seconds.
- Do not show dialogs/alerts in scripts unless the user explicitly wants an interactive helper.

4. File and interpreter rules:
- JavaScript for Typinator must be compiled `.scpt`.
- Shell/Python/Ruby/Swift scripts must be executable and use a valid shebang.
- If a script filename contains spaces and the placeholder also needs a parameter, prefer a wrapper/alias with no spaces in the filename.

5. Prefer Unicode-safe environment access:
- In AppleScript, use `on expand(str, env)` when Unicode fidelity matters.

6. Special return behaviors:
- Use `{{cancelExpansion=yes}}` to abort expansions when prerequisites are missing.
- Use `{{bs=N}}` to consume typed prefix characters when implementing prefix-driven transforms.
- Return assignments as `{{var=value}}...` when persisting state.
7. Remember the official Typinator script contract:
- one optional string parameter only
- AppleScript parameter hint comment on the `expand` handler line
- JavaScript parameter hint comment with `//-- parameter: ...`
- shell/Python/Ruby parameter hint comment with `#-- parameter: ...`
- output to stdout must be UTF-8 text for non-AppleScript runtimes

## Workflow

1. Decide the target format first.
- Live installed set change: update the `.tyset` through Typinator scripting.
- Import/export artifact change: update exported CSV/TXT safely.
- Includes/runtime capability change: update scripts, reference assets, docs, and text resources under `Includes`.

2. Read the relevant local docs before editing non-trivial syntax or scripts.

3. Choose the right maintenance mode.
- Use `scripts/validate_typinator_exports.py` for export linting and safe autofix.
- Use `scripts/typinator_doctor.py` for a whole-system health check.
- Use `scripts/sync_live_and_exports.py` when live sets and exports both matter.
- Use `scripts/audit_typinator_semantics.py` for duplicate-semantic and oversized-menu analysis.
- For `Direct Exports`, do not run transformations that alter dialect/line endings unless explicitly requested.

4. Fix syntax quality.
- Convert `{form:name}` to `{{?name}}` where needed.
- Remove artifacts like `<Skip if null>`.
- Fix malformed markers such as `{Shell/`.
- Rewrite deprecated script aliases to canonical paths when a manifest is available.

5. Add enhancements.
- Add high-value snippets or picker rules.
- Add master menus only when they actually improve usability.
- Prefer scaffolders for repeatable patterns:
- picker sets via `scripts/create_picker_set.py`
- script-backed rules via `scripts/create_script_backed_rule.py`
- reference lookup rules via `scripts/create_reference_lookup_rule.py`
- transform bundles via `scripts/create_transform_bundle.py`

6. Canonicalize script references before finalizing exports or live rules.
- Rewrite alias-style references to canonical organized script paths.
- Prefer no-space wrapper scripts when Typinator placeholder parsing would otherwise break.

7. Validate script semantics when applicable.
- Verify marker forms, argument count assumptions, and parameter comments.
- Ensure scripts are non-interactive when used as plain expansion helpers.
- Verify the actual placeholder path is Typinator-safe.

8. Document changes.
- Update or add a concise guide in the same folder.
- List new abbreviations and behavior notes.

9. When user targets a `.tyset` package directly.
- Treat `.tyset` as application-managed package storage.
- Perform edits through `osascript` and Typinator scripting classes (`rule set`, `rule`) using `make`, `set`, `delete`, and lookups by set/rule.
- For bulk live-rule creation or migration, prefer `scripts/upsert_live_typinator_rules.py` over a single giant AppleScript payload.
- For plain-text rules, set `plain expansion` and `expansion type`; do not assume `formatted expansion` should also be written.
- Verify by re-reading rule counts and sample abbreviations from Typinator after changes.
- Rule descriptions/comments are part of the live set and should be updated along with expansions when they clarify behavior.
- Live `.tyset` editing is the default path for installed-set changes.

10. When exports are involved, run final validation before claiming completion.
- Use `scripts/validate_typinator_exports.py`.
- Treat validator errors as blockers for export-focused work.

## Decision Matrix

- Live change needed now:
  Use Typinator scripting and verify by re-reading the live rule.
- Export artifact cleanup only:
  Use the validator and optional autofix first, then interactive cleanup for ambiguous duplicate decisions.
- Unsure where the problem lives:
  Run `scripts/typinator_doctor.py` first.
- Need to compare installed state to export artifacts:
  Run `scripts/sync_live_and_exports.py`.
- Need smarter cleanup recommendations:
  Run `scripts/audit_typinator_semantics.py`.
- Need to create a new picker, transform, or reference-backed rule:
  Use the generator scripts instead of hand-authoring boilerplate.

## When to use references

- Syntax and dialog patterns: `references/syntax-and-ux.md`
- Master menu architecture: `references/master-menu-patterns.md`
- Set-specific enhancement ideas: `references/set-enhancement-ideas.md`
- Runtime structure and source-of-truth paths: `references/runtime-structure.md`
- Local documentation map: `references/documentation-map.md`
- Documentation cleanup strategy: `references/documentation-cleanup.md`
- Live set editing and `.tyset` operations: `references/live-set-editing.md`
- Set grouping and naming strategy: `references/set-taxonomy.md`
- Scripts, wrappers, and placeholder-safe paths: `references/scripts-and-placeholders.md`
- Handy local utility scripts: `references/handy-scripts.md`
- Required validation checks: `references/quality-gates.md`
- End-to-end task playbooks: `references/workflows.md`
- Deep-read canonical Typinator doc notes: `references/core-doc-notes.md`
- Export validator usage and pass criteria: `references/export-validation.md`
- Canonical alias-to-path mapping policy: `references/script-manifest.md`
- Reusable pattern catalog: `references/pattern-library.md`
- Common failure modes and smells: `references/anti-patterns.md`
- Guidance for choosing live vs export targets: `references/live-vs-export-strategy.md`
- Generated topic-to-source map: `references/typinator-feature-map.md`
- Curated feature-map manifest: `references/typinator-feature-map-sources.json`
- Compact ingest memory of official docs: `references/official-reference-ingest.md`

## Utilities

- `scripts/audit_typinator_tree.py`
Generates a topology audit of the Typinator tree. Useful for large cleanup or migration work, not required for ordinary rule authoring.

- `scripts/audit_typinator_semantics.py`
Finds likely duplicate expansions, oversized menus, and semantic cleanup candidates across export sets.

- `scripts/build_master_menu.py`
Builds/updates a one-abbreviation master menu for a CSV set.

- `scripts/build_master_menu_includes.py`
Builds a master menu using Includes-hosted exports/resources by default.

- `scripts/build_script_manifest.py`
Builds a canonical script manifest for organized Includes scripts and deprecated aliases.

- `scripts/convert_form_placeholders.py`
Converts non-Typinator placeholder styles to Typinator input fields.

- `scripts/create_picker_set.py`
Scaffolds a grouped picker CSV set from a text list.

- `scripts/create_reference_lookup_rule.py`
Scaffolds a reference-backed lookup rule with a source file and wrapper script.

- `scripts/create_script_backed_rule.py`
Scaffolds a script-backed rule plus a Typinator-safe executable helper.

- `scripts/create_transform_bundle.py`
Scaffolds a simple transform rule and companion script.

- `scripts/upsert_live_typinator_rules.py`
Safely upserts live Typinator rules one at a time, avoiding brittle bulk AppleScript and plain/ formatted expansion mismatches.

- `scripts/build_feature_map.py`
Rebuilds `references/typinator-feature-map.md` from the curated source manifest and reports local docs that are not yet classified into a feature area.

- `scripts/interactive_fix_exports.py`
Interactive fixer for exported CSV sets.

- `scripts/normalize_exported_sets.py`
Creates cleaned copies with line-ending and Unicode cleanup. Export-focused utility.

- `scripts/validate_typinator_exports.py`
Runs strict export validation, emits structured findings, and can apply safe autofixes.

- `scripts/sync_live_and_exports.py`
Measures drift between live Typinator rule sets and export artifacts.

- `scripts/typinator_doctor.py`
Runs the broad health check across exports, live sets, scripts, and Includes assets.

## Deliverables

When editing Typinator assets, provide what matches the target:
- Live `.tyset` changes when the installed set was edited
- Updated CSV/TXT files when export artifacts were edited
- Added/updated Includes scripts/docs/text resources when runtime support changed
- A short change summary with exact abbreviations, rules, scripts, or docs changed
