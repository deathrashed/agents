# Anti-Patterns

These are the recurring mistakes the skill should actively avoid.

## Giant inline shell blocks

- Smell: the expansion contains long heredocs or complex embedded shell logic.
- Better: move the logic into `Includes/Scripts` and keep the rule focused on parameters and output.

## Unbounded pickers

- Smell: one picker tries to hold an entire taxonomy.
- Better: split by category or add a top-level menu that leads to smaller pickers.

## Alias-path drift

- Smell: exports still reference old script aliases or symlink paths.
- Better: build a manifest and rewrite to canonical `Scripts/...` paths.

## Live/export confusion

- Smell: editing export files when the real target is the installed Typinator set, or vice versa.
- Better: decide target first and use the matching workflow.

## Hidden interactivity

- Smell: a script used in normal expansions pops dialogs or file choosers.
- Better: reserve interactive scripts for explicitly interactive helpers only.

## Description rot

- Smell: rule comments or descriptions no longer match the expansion.
- Better: update commentary as part of the same change, especially for non-obvious rules.
