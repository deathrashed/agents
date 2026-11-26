# keyboard-maestro-macros

> Create valid Keyboard Maestro (.kmmacros) files that import without errors. Use when building KM macros, fixing import errors, or converting other automation to KM format.

> [!IMPORTANT]
> LLMs CANNOT generate valid KM macros from pure knowledge. You MUST study real exports first.
> More information: `../SKILL.md`.

> [!WARNING]
> A file can pass `plutil -lint` and still be wrong for Keyboard Maestro import. Treat schema-sensitive actions as export-cloned, not hand-written.

## Quick Start

- Study real exports before generating:

```bash
ls /Users/rd/.config/keyboard-maestro/km-backups/
```

- Validate all macros:

```bash
plutil -lint your-macro.kmmacros
```

- Find real exports for an action:

```bash
scripts/find-action.sh ExecuteShellScript
```

- Validate the skill package:

```bash
scripts/validate-skill.sh
```

- View working examples:

```bash
ls ../examples/
```

## Common Actions

- Execute a shell script:

`ExecuteShellScript`

- Set a variable:

`SetVariableToText`

- Copy to clipboard:

`SetClipboardToText`

- Get clipboard:

`GetClipboard`

- Conditional logic:

`IfThenElse`

- User prompts:

`PromptForUserInput`

## Critical Rules

- Root must be `<array>`, NOT `<dict>`
- Use `MacroActionType`, NOT `Action`
- Every action needs unique `ActionUID` (integer)
- Triggers use `MacroTriggerType`, NOT `Trigger`
- Variables use `%Variable%Name%` syntax
- Clone shell-script, prompt, app-activation, and keystroke action blocks from real exports

## Full Documentation

- Main guide: `MACRO-GUIDE.md`
- Debugging story: `TROUBLESHOOTING.md`
- Action reference: `../references/ACTIONS.md`
- Action sourcing map: `../references/ACTION-SOURCING.md`
- Structure reference: `../references/MACRO-STRUCTURE.txt`
