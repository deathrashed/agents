# Export Validation

Use this checklist and command when finalizing export work.

This is not required for ordinary live `.tyset` edits unless exports are also part of the task.

## One-shot command

```bash
python3 scripts/validate_typinator_exports.py \
  --includes-root /Users/rd/.config/typinator/Sets/Includes \
  --manifest /Users/rd/.config/typinator/Sets/Includes/Documentation/Generated/script-manifest.csv
```

Safe autofix mode:

```bash
python3 scripts/validate_typinator_exports.py \
  --includes-root /Users/rd/.config/typinator/Sets/Includes \
  --manifest /Users/rd/.config/typinator/Sets/Includes/Documentation/Generated/script-manifest.csv \
  --fix
```

Machine-readable report:

```bash
python3 scripts/validate_typinator_exports.py \
  --includes-root /Users/rd/.config/typinator/Sets/Includes \
  --manifest /Users/rd/.config/typinator/Sets/Includes/Documentation/Generated/script-manifest.csv \
  --json
```

Optional abbreviation policy:

```bash
python3 scripts/validate_typinator_exports.py \
  --includes-root /Users/rd/.config/typinator/Sets/Includes \
  --manifest /Users/rd/.config/typinator/Sets/Includes/Documentation/Generated/script-manifest.csv \
  --max-abbr-words 2
```

## Required pass criteria

1. No CSV parse failures.
2. No duplicate abbreviations within a file.
3. No syntax artifacts:
- `{Shell/`
- `{form:...}`
- `<Skip if null>`
4. Every `Scripts/...` reference resolves to an existing path.
5. No `Scripts/...` reference points to a symlink alias path.
6. No unresolved script markers in brace or backtick snippets.
7. No script filenames with marker-conflicting characters in generated sets.
8. No deprecated manifest alias paths remain after canonical rewrite.

## Warnings to review

1. Mixed newline style in CSV files.
2. Interactive scripts used in expansion paths (`display dialog`, `choose from list`, etc.).
3. Coexisting `Includes/Exported` and `Includes/exported` directories.
4. Oversized menus that should be split into grouped pickers.
