# Documentation Cleanup

## Current state

The local Typinator knowledge base exists in two places:
- `Includes/Documentation`
- `Includes/Text`

They overlap, but they do not serve the same purpose yet.

## Recommended model

### Keep in `Includes/Documentation`

- official or canonical reference material
- long-form user guides
- scripting and regex guides
- structured feature reference
- formal explanations of Typinator behavior

### Keep in `Includes/Text`

- reusable text resources for Includes insertion
- compact examples
- CSV examples and search assets
- focused guides for conditionals, escaping, and practical patterns
- curated AI-facing quick references

## Safe cleanup strategy

1. Inventory topics that exist in both trees.
2. Decide whether each item is:
- canonical reference
- reusable Includes content
- project-specific note
- obsolete duplicate
3. Move only after the replacement location is clearly better.
4. Update all internal paths and skill references after any move.
5. Preserve import/runtime assets in place if Typinator placeholders already depend on them.

## Important rule

Do not flatten `Documentation` into `Text` wholesale.

Better structure is:
- `Documentation` = authoritative docs
- `Text` = reusable Includes content and curated examples

If a future cleanup merges material, it should be topic-by-topic with path validation, not by broad folder collapse.
