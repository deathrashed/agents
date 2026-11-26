# Typinator Workflows

## Workflow A: Live `.tyset` editing

1. Identify the live rule set and rule abbreviations.
2. Read the relevant Includes docs first if syntax or scripts are non-trivial.
3. Update rules through Typinator’s AppleScript dictionary, not by patching package internals.
4. Re-read the changed rules from Typinator to verify the update landed.
5. Spot-check descriptions/comments as well as expansion text.

## Workflow B: Safe in-place edits for Direct Exports

1. Use the file in `Includes/Exported/Direct Exports` as the format baseline.
2. Change only abbreviation/expansion writing content.
3. Preserve delimiter, quoting, encoding/BOM, newline style, and column order exactly.
4. Avoid normalizers/rewriters that can alter CSV dialect unless explicitly requested.
5. Run export validation before handoff.

## Workflow C: Build or refine a picker/menu

1. Keep labels simple and human-readable.
2. Use mapped alternatives (`label:value`) when the inserted text should differ from the menu label.
3. Use explicit empty defaults (`<>`) when you want the picker to open blank each time.
4. Avoid symbolic labels that collide with menu separators such as `|` and `:`.
5. Split large menus into category dropdowns instead of one giant list.

## Workflow D: Add script-backed abbreviations

1. Verify the script follows Typinator’s `expand`/parameter rules.
2. Prefer canonical organized script paths.
3. If the script filename contains spaces and a parameter is needed, add a no-space wrapper.
4. Use script-backed rules when inline Typinator syntax would be too fragile or unreadable.
5. Test the script directly before trusting the placeholder.

## Workflow E: Large export cleanup

1. Run interactive fixer on the export directory.
2. Review parse issues and duplicate abbreviations.
3. Normalize only when format changes are acceptable.
4. Add master menus only when they help actual usage.
5. Run export validation before claiming completion.

## Workflow F: System diagnosis

1. Run `typinator_doctor.py` when the failure location is unclear.
2. Review validator findings, orphaned assets, and semantic duplicate groups.
3. Run `sync_live_and_exports.py` if installed behavior and export artifacts might be drifting.
4. Run `audit_typinator_semantics.py` when duplicate content or oversized pickers are suspected.
5. Choose the actual remediation target only after diagnosis.

## Workflow G: Scaffold a new pattern

1. Pick the smallest generator that matches the intended rule style.
2. Generate the baseline rule and support files.
3. Replace boilerplate with task-specific labels, paths, and logic.
4. Validate script path safety and comments.
5. Document the new abbreviation and behavior.
