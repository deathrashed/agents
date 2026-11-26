# Keyboard Maestro Action Sourcing Map

Use this file before creating or editing action dictionaries. The rule is simple: find a real export with the action, clone the full action dictionary, and edit only the payload fields that are safe for the requested macro.

Run:

```bash
scripts/find-action.sh MacroActionType
```

## Canonical Sources

| Action Type | First Source To Check | Safe Fields To Edit | Do Not Touch Without Another Export |
|---|---|---|---|
| `ExecuteShellScript` | `real-exports/text-transformer.kmmacros`, then `real-exports/backup-macros.kmmacros` | Script text, shell path when the source action already has one | result handling shape, timeout fields, execution mode fields |
| `ExecuteAppleScript` | `real-exports/text-transformer.kmmacros`, then `real-exports/backup-macros.kmmacros` | AppleScript source text | execution/result keys not relevant to the payload |
| `PromptForUserInput` | `real-exports/calculate.kmmacros`, then `real-exports/text-transformer.kmmacros` | title, prompt text, variable names/defaults while preserving each variable dict shape | `Variables` array structure, button/result behavior |
| `SetVariableToText` | `examples/text-case.kmmacros`, then `real-exports/text-transformer.kmmacros` | `Variable`, `Text` | action type spelling, action wrapper keys |
| `SetVariableToCalculation` | `real-exports/calculate.kmmacros` | variable name, calculation expression | calculation action shape |
| `SetClipboardToText` | `examples/text-case.kmmacros`, then `real-exports/clipboard-history.kmmacros` | `Text` | clipboard action structure |
| `ClipboardHistorySwitcher` | `real-exports/clipboard-history.kmmacros` | display/paste options only if present in source | switcher-specific keys |
| `PasteByName` | `real-exports/clipboard-history.kmmacros` | named clipboard reference | action shape |
| `OCRImage` | `real-exports/ocr-clipboard-image.kmmacros` | image source/output variable fields that already exist | OCR option structure |
| `IfThenElse` | `real-exports/backup-macros.kmmacros`, then `real-exports/text-transformer.kmmacros` | condition values, variable names, nested cloned actions | condition dict shape, `ThenActions`/`ElseActions` layout |
| `Switch` | `real-exports/text-transformer.kmmacros` | case values and nested cloned actions | case array structure |
| `For`, `While`, `Repeat`, `Until` | `real-exports/backup-macros.kmmacros` | loop variable/value fields | nested loop schema |
| `TryCatch` | `real-exports/backup-macros.kmmacros` | nested cloned actions | error handling layout |
| `ExecuteSubroutine` | `real-exports/backup-macros.kmmacros` | subroutine macro name/UID fields when present | parameter structure |
| `Semaphore` | `real-exports/backup-macros.kmmacros` | semaphore name | locking/action layout |
| `SimulateKeystroke` | `real-exports/insert-text-into-restricted-field.kmmacros` | key and modifier values only | keystroke dictionary shape |
| `InsertText` | `real-exports/insert-text-into-restricted-field.kmmacros` | inserted text | insertion mode fields |
| `ActivateApplication` | run `scripts/find-action.sh ActivateApplication` and use the closest export | application name/path fields | activation flags |
| `SelectMenuItem` | run `scripts/find-action.sh SelectMenuItem` and use the closest export | menu path values | menu item dict shape |
| `MouseMoveAndClick` | run `scripts/find-action.sh MouseMoveAndClick` and use the closest export | coordinates/button values | coordinate mode and click structure |
| `OpenURL` | `real-exports/tinyurl.kmmacros` | URL string or variable token | URL action shape |
| `Notification`, `Alert`, `Display` | run `scripts/find-action.sh Notification`, `Alert`, or `Display` | title/body text | display/action option keys |
| `File`, `ReadFile`, `WriteFile`, `Open1File` | `real-exports/backup-macros.kmmacros` | paths, variable names, file text | file action mode fields |

## If The Action Is Not Listed

1. Run `scripts/find-action.sh ActionType`.
2. Prefer `real-exports/` over `examples/` for schema-sensitive actions.
3. If no local export exists, create a tiny Keyboard Maestro macro with only that action and export it.
4. Add the new export or a note here after it imports successfully.

## Completion Standard

When delivering a macro, say exactly which level was verified:

- `plist validated`: `plutil -lint` passed only.
- `manual import confirmed`: Keyboard Maestro imported the file.
- `behavior confirmed`: The macro imported and was run successfully.
