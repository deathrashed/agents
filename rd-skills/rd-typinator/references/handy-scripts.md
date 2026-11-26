# Handy Scripts

These are the local skill utilities under:
`/Users/rd/.config/typinator/.skill/scripts`

They are helper tools for larger maintenance tasks. They are not required for every Typinator change.

## Export-focused utilities

- `interactive_fix_exports.py`
  Interactive CSV/TXT export fixer for duplicate abbreviations, malformed markers, Unicode cleanup, and placeholder conversion.

- `normalize_exported_sets.py`
  Normalizes exported CSV files into cleaned copies. Useful only when format-preserving direct-export rules are not required.

- `validate_typinator_exports.py`
  Final export validator for syntax artifacts, duplicates, script references, alias use, and manifest checks. Supports structured findings and safe autofix.

- `typinator_doctor.py`
  Whole-system health report spanning exports, live sets, scripts, text assets, orphaned resources, and semantic duplicates.

- `sync_live_and_exports.py`
  Drift checker between installed Typinator rule sets and export artifacts.

- `audit_typinator_semantics.py`
  Deeper semantic audit for duplicate expansions, oversized menus, and repetition patterns.

## Menu/build utilities

- `build_master_menu.py`
  Adds or updates a master-menu row for a specific CSV file.

- `build_master_menu_includes.py`
  Convenience wrapper for building master menus against Includes-hosted exports.

## Structure and migration utilities

- `upsert_live_typinator_rules.py`
  Safely creates or updates live Typinator rules one at a time through AppleScript. Use this for bulk installed-set updates instead of building one giant inline AppleScript blob.

- `audit_typinator_tree.py`
  Produces a quick topology report of Sets and Includes. Useful during major cleanup/migration work.

- `build_script_manifest.py`
  Scans organized scripts and builds the alias-to-canonical manifest used for export validation and path migration.

- `convert_form_placeholders.py`
  Converts foreign placeholder forms such as `{form:name}` into Typinator input fields.

- `create_picker_set.py`
  Scaffolds a grouped picker set from a newline-delimited option list.

- `create_script_backed_rule.py`
  Scaffolds a script-backed rule and a companion executable helper.

- `create_reference_lookup_rule.py`
  Scaffolds a lookup rule with a source file and wrapper script.

- `create_transform_bundle.py`
  Scaffolds a simple transform bundle for repeated text operations.

## Practical rule

Use these utilities when:
- cleaning exports at scale
- running system-wide health checks
- generating repeatable rule patterns
- migrating large script trees
- generating CSV-driven menus
- validating final export deliverables

Do not default to them when:
- editing live `.tyset` rules directly
- making small one-off abbreviation changes
- adjusting a few picker/menu entries in installed sets

Exception:
- for larger live-set upserts, prefer `upsert_live_typinator_rules.py` over handwritten bulk AppleScript
