---
name: rd-km-macro-creator
description: Use when creating or fixing Keyboard Maestro .kmmacros files, especially when import errors or schema uncertainty mean the macro must be grounded in real exports instead of guessed XML.
trigger: kmmacros, keyboard maestro macro, km macro
---

# Keyboard Maestro Macro Creator Skill

## When Invoked

Use this skill when asked to:
- Create Keyboard Maestro macros
- Edit .kmmacros files
- Fix import errors in KM macros
- Add actions to existing macros

## The Solution

The critical insight from KM forum: **LLMs cannot generate valid KM XML from knowledge because there's no public schema and action names differ from UI.**

**The fix**: Study real exports from `/Users/rd/.config/keyboard-maestro/km-backups/`, copy working patterns, validate with `plutil -lint`.

## Construction Rule

Use a two-level approach:

1. Hand-template only the stable outer wrapper:
   - root `<array>`
   - macro group
   - macro dict
   - simple `StatusMenu` trigger
2. Clone real exported action blocks for schema-sensitive actions.

Never hand-author complex action bodies when you have a real export available.

## Always Validate

```bash
plutil -lint your-macro.kmmacros
```

If validation fails:
- Root must be `<array>`, not `<dict>`
- Use real export structure
- Check all keys are correct

Important: `plutil -lint` checks plist syntax only. It does not prove KM will import the file.

For the whole skill package, run:

```bash
scripts/validate-skill.sh
```

## Available Examples

The working macros are in this folder:
- `examples/text-case.kmmacros` - Uppercase clipboard
- `examples/extract-links.kmmacros` - Extract URLs
- `examples/sort-lines.kmmacros` - Sort + unique lines
- `examples/count-lines.kmmacros` - Count lines

See references:
- `references/MACRO-STRUCTURE.txt` - Template
- `references/ACTIONS.md` - Action names
- `references/ACTION-SOURCING.md` - where to clone common action blocks from

## How to Create

1. List the required actions by `MacroActionType`.
2. For each action, run `scripts/find-action.sh MacroActionType`.
3. Read `references/ACTION-SOURCING.md` and choose the closest real export.
4. Copy full action dictionaries for any schema-sensitive action.
5. Modify payload fields only.
6. Generate fresh UUIDs for macro/group `UID` values.
7. Generate unique integer `ActionUID` values within each macro.
8. Validate plist syntax with `plutil -lint`.
9. Compare action shape with the source export before claiming success.
10. State verification level: plist validated, manual import confirmed, or behavior confirmed.

## Documentation

See skill folder:
- `README.md` - Quick start and layout
- `docs/MACRO-GUIDE.md` - Full guide
- `docs/TROUBLESHOOTING.md` - Process notes
- `docs/TLDR.md` - Short reference
- `templates/status-menu-wrapper.xml` - safe wrapper only; add cloned actions
- `scripts/find-action.sh` - locate real exports containing an action type
- `scripts/validate-skill.sh` - validate bundled examples and doc references

## Anti-Patterns

DON'T:
- Generate from "knowledge"
- Guess action names
- Skip validation
- Assume structure is simple
- Use simplified shell/prompt/keystroke/app-activation examples as authoritative
