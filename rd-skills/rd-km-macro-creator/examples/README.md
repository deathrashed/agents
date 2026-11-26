# Working Examples

These are validated, importable Keyboard Maestro macros created and tested during skill development.

## Files

| File | Description | Verification |
|------|-------------|--------------|
| `text-case.kmmacros` | Uppercase clipboard content | `plist validated` |
| `extract-links.kmmacros` | Extract URLs from text | `plist validated` |
| `sort-lines.kmmacros` | Sort and deduplicate lines | `plist validated` |
| `count-lines.kmmacros` | Count lines in clipboard | `plist validated` |
| `clipboard-history-paster.kmmacros` | Paste from a clipboard history chooser | `plist validated` |

Verification levels:

- `plist validated`: `plutil -lint` passed.
- `manual import confirmed`: Keyboard Maestro imported the file.
- `behavior confirmed`: The macro imported and was run successfully.

## Usage

Import any of these into Keyboard Maestro:
1. Open Keyboard Maestro
2. File → Import Macros
3. Select the .kmmacros file

## Source

These were created by studying real exports, then hand-crafting the XML following the exact structure observed in `/Users/rd/.config/keyboard-maestro/km-backups/`.

## Important Limitation

These examples are best used as:

- proof that a specific file imported successfully
- reference for outer wrapper structure
- reference for some simple action patterns

They should not be treated as a universal schema for all action types. For schema-sensitive actions, prefer cloning from `../real-exports/`.

`text-case.kmmacros` includes a shell-script action that currently passes plist validation. Treat it as a validated example only, not as a universal `ExecuteShellScript` schema. For new shell macros, clone from real exports listed in `../references/ACTION-SOURCING.md`.
