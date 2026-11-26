# Live vs Export Strategy

Choose the target before making changes.

## Choose live `.tyset` editing when

- the installed Typinator behavior must change now
- the user explicitly targets a live rule set
- comments/descriptions in the installed set matter

## Choose export editing when

- the user wants importable CSV/TXT artifacts
- the user explicitly targets exported files
- the work is a cleanup or migration pass across many rows

## Choose Includes/runtime editing when

- scripts, reference files, or text resources are the real source of behavior
- the rule points at shared runtime assets
- the task is adding authoring infrastructure rather than changing one rule

## Choose doctor mode first when

- the failure location is unclear
- multiple layers may be drifting
- you suspect duplicate semantics, dead scripts, or export/live mismatches
