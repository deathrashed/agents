## Helper scripts

### `validate_ingest_target.py`

Purpose:

- catch path mistakes before editing
- distinguish staged from external source files
- confirm governing docs exist

Use when:

- the user gives a full path
- the source may already be archived
- the working directory is not obviously the Directory root
- you need to know whether archiving should happen at the end
- you want a quick yes-no check for a file source before ingest

### `format_status_entry.py`

Purpose:

- generate a consistent STATUS log line
- avoid hand-format drift

Use when:

- one source updates one or more canonical files
- a quick status entry is needed after merge completion

### `archive_processed_input.py`

Purpose:

- move processed input into `•processed/`
- preserve source-relative layout from `_extracted/`

Use when:

- canonical updates and STATUS logging are finished
- the source came from `_extracted/` and should leave staging

### `suggest_destination.py`

Purpose:

- offer likely canonical target files from a path or source label
- speed up path-driven documentation tasks

Use when:

- the user points at a real path like `/Volumes/Apfspace/Icons`
- you want a first-pass guess before reading canonical owner files
- the task is "document this path" rather than "process this extracted note"
