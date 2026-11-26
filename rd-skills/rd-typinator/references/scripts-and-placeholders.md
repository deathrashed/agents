# Scripts And Placeholders

## Core placeholder rule

Typinator script placeholders have the shape:

`{Scripts/... optionalArgument}`

Typinator effectively has:
- one script path
- one optional argument string

## Important consequence

If a script filename contains spaces and you also need a parameter, the placeholder becomes fragile because Typinator can split the path/argument boundary incorrectly.

## Safe practice

1. Prefer canonical no-space script filenames for parameterized helpers.
2. If the real script name has spaces, add a no-space wrapper script.
3. Point live rules and exports at the wrapper.

## Parameter hints

Parameter comments should use:
- AppleScript: `-- parameter: ...`
- Shell/Python/etc.: `#-- parameter: ...`
- JavaScript/Swift: `//-- parameter: ...`

## Script-choice guidance from the local docs

Use shell when:
- it is a compact, reliable command pipeline
- it avoids overcomplicated AppleScript
- clipboard/text processing is simple

Use AppleScript when:
- app automation is needed
- Finder/System Events/UI scripting is involved
- the workflow is macOS-app specific

Use wrappers when:
- script paths contain spaces
- the placeholder needs a parameter
- you want a stable canonical runtime path
