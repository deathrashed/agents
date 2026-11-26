---
name: rd-typinator-directory-ingest
description: Process one source file into the Typinator Directory knowledge
  base's correct canonical plaintext document or documents. Use when asked to
  ingest, process, consolidate, transform, merge, route, or archive content
  for `/Users/rd/.config/typinator/Sets/Includes/Text/Directory`, whether the
  source comes from `_extracted/`, from an arbitrary file path, or from a real
  filesystem directory or system path the user wants documented and merged into
  the knowledge base, especially when the request mentions `AGENTS.md`,
  `_docs/INGEST.md`, `_docs/TRANSFORM.md`, or `_docs/STATUS.md`.
---

# Typinator Directory Ingest

## Overview

Execute the ingestion workflow for the Directory knowledge base at:
`/Users/rd/.config/typinator/Sets/Includes/Text/Directory`

Treat the Directory as a domain-organized system of canonical plaintext
documents. Process one source file at a time. Read the governing docs first,
identify domains, route content to the correct canonical file or files, merge
cleanly, update the processing log, and archive the source file when it came
from `_extracted/`.

The source may be:

- a staged raw file in `_extracted/`
- an arbitrary external file path
- a real directory or system path that should be analyzed and reflected in a
  canonical document

Do not treat `_extracted/` as canonical. Do not preserve source structure when
it conflicts with domain structure.

## Governing documents

Read these before making non-trivial ingestion edits:

1. `AGENTS.md`
2. `_docs/INGEST.md`
3. `_docs/TRANSFORM.md`
4. `_docs/STATUS.md`

Apply `AGENTS.md` as the system model and routing policy.
Use `_docs/INGEST.md` as the high-level execution checklist.
Use `_docs/TRANSFORM.md` for output formatting and transformation rules.
Use `_docs/STATUS.md` to understand prior operations and to append the new log
entry in the existing style.

For quick reminders while working:

- domain routing examples and ownership heuristics:
  `references/routing-and-lifecycle.md`
- helper script usage and expected outputs:
  `references/helper-scripts.md`

## Use this skill for

- Processing a file from `_extracted/`
- Processing a file from an arbitrary path outside the Directory
- Analyzing a real directory path and updating the canonical note that owns it
- Consolidating a mixed-domain raw note into canonical files
- Updating one or more existing domain files from a new source
- Creating a new canonical file only when no existing file owns the domain
- Logging completion in `_docs/STATUS.md`
- Archiving the processed source under `_extracted/•processed/` when the source
  came from staging

Do not use this skill for general Typinator rule authoring, export cleanup, or
non-Directory documentation work.

## Workflow

### 1. Establish scope

- Confirm the source file is a single input file
- Work on one source file at a time
- Identify the Directory root:
  `/Users/rd/.config/typinator/Sets/Includes/Text/Directory`
- Run `scripts/validate_ingest_target.py` before substantial edits when the
  source path or Directory root needs confirmation
- If the user points to a real directory path instead of a text file, treat the
  task as system reconstruction from a live path rather than note ingestion
- If the source is outside `_extracted/`, treat it as an external input and do
  not archive it into `•processed/` unless the user explicitly wants it copied
  into staging first

### 2. Build context before editing

- Read the full source file end-to-end
- Identify what the file represents, not just what it contains
- Identify every real domain present in the source
- Inspect existing canonical files that may own those domains before deciding
  whether to create anything new

If the source is a real directory path:

- traverse the directory enough to understand purpose, structure, scale,
  lifecycle, and dependencies
- read representative configs, scripts, and local docs as evidence
- describe the system the path represents, not just the tree

### 3. Route by domain

- Split mixed inputs by domain first
- Map each domain to exactly one canonical owner file
- Prefer updating an existing canonical file over creating a new file
- If multiple canonical files seem to own the same domain, consolidate or
  clarify boundaries before proceeding

Common examples from this Directory:

- Obsidian -> `directory/obsidian.txt`
- Typinator -> `app/typinator.txt`
- Karabiner -> `app/karabiner.txt`
- Keyboard Maestro -> `app/keyboard-maestro.txt`
- `/Volumes/Apfspace/Icons` -> `directory/icons.txt`
- `/Volumes/Apfspace` -> `directory/apfspace.txt`
- Scripts directory -> `directory/scripts.txt`
- Shell config -> `util/shell.txt`
- System profile -> `system/system-profile.txt`

### 4. Extract durable signal

Keep:

- commands
- configurations
- workflows
- real paths
- relationships between tools and files
- constraints, dependencies, and operational context

Remove:

- conversational filler
- AI output noise
- repeated explanation
- partial fragments that do not preserve real meaning

### 5. Merge into canonical files

For each destination file:

- preserve the file as the source of truth
- merge into the correct section instead of appending blindly
- remove duplication introduced by the new source
- preserve or improve the canonical structure
- fully integrate related concepts instead of leaving partial fragments

At least one canonical file must be updated for a valid ingest operation.

### 6. Enforce formatting and reference rules

Canonical files in this Directory must be:

- plaintext only
- objective and professional in tone
- structured with ASCII-style section headers
- readable in terminal width
- based on real values only

Reference rules:

- inside the knowledge base, use Directory-root-relative paths only
- outside the knowledge base, use absolute paths only
- never use absolute paths that point back into the Directory for internal
  cross-references
- never use `./` or `../` internal references

### 7. Finalize lifecycle actions

After canonical updates are complete:

- add a processed entry to `_docs/STATUS.md`
- if the source came from `_extracted/`, archive the original source into
  `_extracted/•processed/`
- preserve the original source content in the archive when archiving applies

Mirror the STATUS entry style already used in `_docs/STATUS.md`.

## Helper scripts

Use these when they save time or reduce avoidable mistakes.

### `scripts/validate_ingest_target.py`

Validate that:

- the Directory root looks correct
- the source file exists
- whether the source is staged or external
- if staged, whether it is already in `•processed/`
- governing docs exist

Example:

`python3 scripts/validate_ingest_target.py --directory-root "/Users/rd/.config/typinator/Sets/Includes/Text/Directory" --source "/Users/rd/.config/typinator/Sets/Includes/Text/Directory/_extracted/foo.txt"`

It reports whether the source is:

- `STAGED` for a live `_extracted/` input
- `EXTERNAL` for a user-specified file outside `_extracted/`
- invalid for already archived or missing sources

### `scripts/format_status_entry.py`

Generate a STATUS line in the established format for quick copy into
`_docs/STATUS.md`.

Example:

`python3 scripts/format_status_entry.py --source "_extracted/foo.txt" --dest "app/typinator.txt" --dest "directory/scripts.txt"`

For external paths, pass the source label exactly as you want it recorded, for
example:

`python3 scripts/format_status_entry.py --source "/Volumes/Apfspace/Icons" --dest "directory/icons.txt"`

### `scripts/archive_processed_input.py`

Move a processed staged source file into `_extracted/•processed/` while
preserving the source path relative to `_extracted/`.

Example:

`python3 scripts/archive_processed_input.py --directory-root "/Users/rd/.config/typinator/Sets/Includes/Text/Directory" --source "/Users/rd/.config/typinator/Sets/Includes/Text/Directory/_extracted/foo.txt"`

### `scripts/suggest_destination.py`

Suggest likely canonical destination files from a source label or real path.
Use this as a starting heuristic, then confirm against existing canonical file
scope before editing.

Examples:

`python3 scripts/suggest_destination.py --source "/Volumes/Apfspace/Icons"`

`python3 scripts/suggest_destination.py --source "/Users/rd/.config/karabiner"`

## Output standards

The result must explain how the real system works, not just what files exist.

Aim for documents that are:

- standalone months later
- explicit about dependencies and constraints
- rich in operational context
- domain-scoped rather than source-scoped

Do not dump raw directory trees unless they directly clarify workflow.

## Decision rules

### Create a new canonical file only when all are true

- the source contains a distinct system or domain
- no existing canonical file clearly owns it
- the content is substantial enough to stand alone

Otherwise update an existing canonical file.

### Add cross-references when content spans files

- add reciprocal related-file references where useful
- keep them Directory-root-relative
- avoid copying full content between files

## Completion checklist

Before claiming the ingest is complete, verify:

- the source file was fully read
- the correct canonical file or files were updated
- no duplicate or orphaned content remains
- formatting matches Directory standards
- internal references are Directory-root-relative
- `_docs/STATUS.md` was updated
- if the source came from `_extracted/`, it was archived into
  `_extracted/•processed/`

## Example user requests

- Process `_extracted/foo.txt` into the Directory knowledge base
- Process `/some/other/path/notes.txt` into the Directory knowledge base
- Analyze `/Volumes/Apfspace/Icons` and update `directory/icons.txt`
- Ingest this raw note and merge it into the correct canonical docs
- Consolidate a mixed-domain `_extracted` file, update STATUS, and archive it
- Validate whether this staged file is ready for ingest and tell me where it
  should route
