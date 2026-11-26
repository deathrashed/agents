# Keyboard Maestro Macro Toolkit

## The Problem Solved

For years, no chatbot could create importable Keyboard Maestro macros. This system does.

## Why It Works

The breakthrough from a Keyboard Maestro forum post: **show AI real exports**.

ChatGPT/Claude/etc. generate what responses "would look like" — not what's correct. They hallucinate KM's XML structure because:
- No public schema exists
- UI names differ from internal names  
- Structure is complex and undocumented

**Solution**: Analyze real exports, copy working patterns, and distinguish between:
- stable outer wrapper you can template
- schema-sensitive action blocks you should clone from real exports

## Directory Layout

```
km-macro-creator/
├── SKILL.md
├── README.md
├── docs/
│   ├── MACRO-GUIDE.md
│   ├── TROUBLESHOOTING.md
│   └── TLDR.md
├── examples/
│   ├── README.md
│   └── *.kmmacros
├── real-exports/
│   ├── README.md
│   └── *.kmmacros
├── scripts/
│   ├── find-action.sh
│   └── validate-skill.sh
├── templates/
│   └── status-menu-wrapper.xml
└── references/
    ├── ACTIONS.md
    ├── ACTION-SOURCING.md
    └── MACRO-STRUCTURE.txt
```

## Quick Start

### 0. Decide if the action is safe to template

If the macro uses `ExecuteShellScript`, `PromptForUserInput`, `ActivateApplication`, `SimulateKeystroke`, conditionals, loops, or anything non-trivial, start from a real export, not from a hand-written snippet.

### 1. Validate a Macro

```bash
plutil -lint your-macro.kmmacros
```

### 2. Find a Real Action Source

```bash
scripts/find-action.sh ExecuteShellScript
```

### 3. Validate the Skill Package

```bash
scripts/validate-skill.sh
```

### 4. View as XML

```bash
plutil -convert xml1 your-macro.kmmacros | less
```

### 5. Import to KM

Double-click the `.kmmacros` file in Finder.

## Working Macros

| Macro | Function |
|-------|----------|
| `examples/text-case.kmmacros` | Uppercase clipboard |
| `examples/extract-links.kmmacros` | Extract URLs |
| `examples/sort-lines.kmmacros` | Sort + unique lines |
| `examples/count-lines.kmmacros` | Count lines |

These examples are useful for overall shape and some simple action patterns, but they are not a substitute for cloning action blocks from real exports when using schema-sensitive actions.

## The Complete Story

See `docs/TROUBLESHOOTING.md` for:
- What I looked at
- Initial problems with my macros
- What I found in your real macros
- How I fixed it

## Verification Levels

When creating macros, be precise about what was verified:

| Level | Meaning |
|------|---------|
| `plist validated` | `plutil -lint` passed only |
| `manual import confirmed` | Keyboard Maestro imported the file |
| `behavior confirmed` | The macro imported and was run successfully |

## Canonical Docs

- `SKILL.md` is the entry point future agents should load first.
- `README.md` is the human overview of the skill package.
- `docs/` holds explanatory docs and historical notes.
- `references/` is only for compact reference material that the skill can point at directly.
- `examples/` contains small validated samples.
- `real-exports/` contains larger source-of-truth exports for cloning action blocks.

## Source

- Forum: https://forum.keyboardmaestro.com/t/chatgpt-built-a-working-exportable-macro-that-imported-to-keyboard-maestro-without-errors/49936
- More guides: `/Volumes/666/Actions/toolkit/`
- Example exports: `/Users/rd/.config/keyboard-maestro/km-backups/`
