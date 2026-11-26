# Real Keyboard Maestro Exports

This folder contains real macro exports from your Keyboard Maestro library - what AI needs to study to generate valid macros.

## Selected Examples

Curated examples covering the most common actions:

| File | Description |
|------|-------------|
| `backup-macros.kmmacros` | Complex backup macro with subroutines, conditions, semaphores, regex, AppleScript |
| `text-transformer.kmmacros` | Complex macro with user prompts, AppleScript, transformations |
| `clipboard-history.kmmacros` | Clipboard management with history |
| `ocr-clipboard-image.kmmacros` | OCR functionality |
| `calculate.kmmacros` | Calculator functionality |
| `tinyurl.kmmacros` | URL shortening |
| `insert-text-into-restricted-field.kmmacros` | Insert text into restricted fields |
| `icon-manager.kmmacros` | Manage custom icons |
| `palette-organizer.kmmacros` | Organize KM palettes |
| `upload-macro.kmmacros` | Upload/share macros |

## Scope

This folder currently contains a curated subset of exports chosen for common macro-building tasks. If you need rarer actions, search the original Keyboard Maestro backups and copy the closest matching action block from there.

## All 96 Verified Action Types

See `../references/ACTIONS.md` for complete reference with categories:
- Scripting: ExecuteShellScript, ExecuteAppleScript, ExecuteJavaScript, ExecuteSwift
- Control Flow: IfThenElse, Switch, For, While, Repeat, TryCatch, ExecuteSubroutine
- Variables: SetVariableToText, SetVariableToCalculation, SetVariablesToJSON
- Clipboard: SetClipboardToText, ClipboardHistorySwitcher, PasteByName
- Text: InsertText, SearchReplace, SearchRegEx, Filter
- File: File, Open1File, WriteFile, ReadFile
- And 80+ more...

## Why These Matter

**LLMs cannot generate valid KM macros from knowledge alone.** The only proven method is to show AI real exports first, then it can replicate the exact schema.

These files demonstrate:
- Complex action chaining
- Proper `ActionUID` assignment (unique integer per action)
- AppleScript / JavaScript integration
- User prompt dialogs
- Variable handling (`%Variable%Name%` syntax)
- Conditional logic, loops, subroutines

Most importantly, they let you distinguish:

- stable wrapper structure you can template
- fragile action schemas you should clone directly

## How to Study These

```bash
# View as XML
plutil -convert xml1 -o - filename.kmmacros | less

# Extract actions
plutil -convert xml1 -o - filename.kmmacros | grep -A 30 '<key>Actions</key>'

# Find action types used
plutil -convert xml1 -o - filename.kmmacros | grep '<key>MacroActionType</key>'
```

To find candidate source exports for a specific action type:

```bash
../scripts/find-action.sh ExecuteShellScript
```

For common actions and safe edit boundaries, see `../references/ACTION-SOURCING.md`.

## Source

- Selected examples from: `/Users/rd/.config/keyboard-maestro/km-backups/2026-04-04_20•32•45/`
- Full dataset from: `/Users/rd/.config/keyboard-maestro/km-backups/2026-04-02_14•12•33/` (1,111 macros)
