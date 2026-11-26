# Typinator Quality Gates

Choose the gates that match the target.

## Gate 1: syntax integrity

- No malformed shell markers such as `{Shell/`.
- No foreign placeholder DSLs unless intentionally preserved.
- No broken brace/marker syntax.
- Menu labels do not accidentally contain unescaped `|` or `:` in ways that break parsing.

## Gate 2: dialog UX

- Labels are readable.
- UI-only tokens are compact to avoid blank-line leakage.
- Large menus are grouped when needed.
- Fields use explicit empty defaults `<>` when blank-reset behavior is desired.

## Gate 3: script safety

- Every referenced script exists.
- Script files used with parameters are placeholder-safe.
- Executables have valid shebangs and execute permissions.
- Parameter comments follow Typinator syntax.

## Gate 4: live set integrity

- Changes were applied through Typinator scripting, not raw `.tyset` internals.
- The changed rule can be re-read from Typinator after the update.
- Descriptions/comments match actual behavior.

## Gate 5: export integrity

- CSV parses without errors.
- No duplicate abbreviations within the same file unless intentionally allowed.
- For `Direct Exports`, delimiter/quoting/column shape match the baseline exactly.
- For `Direct Exports`, encoding/BOM/newline convention remain unchanged.
- Deprecated manifest alias paths are rewritten to canonical script paths.

## Gate 6: canonical path integrity

- `Scripts/...` references resolve to real files.
- Avoid compatibility symlink/alias targets in final references.
- Prefer the organized canonical `Scripts/` tree.

## Gate 7: abbreviation policy compliance

- Enforce requested abbreviation constraints globally.
- Verify uniqueness after any rename, split, or normalization step.

## Gate 8: semantic maintainability

- Oversized pickers are split or intentionally accepted.
- Duplicate expansions are reviewed for consolidation opportunities.
- Orphan scripts and reference files are either documented or removed.
