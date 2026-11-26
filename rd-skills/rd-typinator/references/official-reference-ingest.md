# Official Reference Ingest

This note captures the key Typinator behaviors that were explicitly ingested from the local topic-based documentation corpus under:

`/Users/rd/.config/typinator/Sets/Includes/Documentation`

and the official online help center:

`https://help.typinator.ergonis.com/hc/en-us`

Use it as a compact memory layer, not as a replacement for the original docs.

## High-confidence Typinator facts

- The Includes folder extends the `{…}` menu and can contain plain text, rich text, and executable scripts.
- Includes subfolders become submenus in Typinator.
- Rich text and embedded images are not preserved when inserted into plain text expansions.
- Script placeholders use the form `{folder/scriptName argument}` with at most one parameter string.
- Typinator menu display may hide script extensions, but the real placeholder includes the extension.
- AppleScript may be plain `.applescript` or compiled `.scpt`; JavaScript must be compiled `.scpt`.
- Other scripting languages require executable files, a valid shebang, and stdout text output.
- Typinator supports one script parameter only; multi-part inputs must be split inside the script.
- Parameter hint comments are part of the UX contract and differ by language.
- Input forms support text fields, pop-ups, combo boxes, and checkboxes.
- Form inputs can assign variables, feed scripts, and participate in calculations.
- Extended text results let a menu label differ from the inserted value.
- Combo boxes are created by allowing free text in an alternatives field.
- Quick Search can be improved with descriptions and inline comments like `{{-- comment --}}`.
- Random content can be generated with `{/Any /pattern/text/}` and can source text from Includes files.
- Clipboard content can be stored and recalled through Typinator variables without scripting.
- Set-level defaults matter for scale: case behavior, word-break settings, and suffix strategies belong at the set level when repeated across many items.
- Typinator’s default expansion model is natural typing flow; explicit trigger characters are optional, not foundational.
- Modifier keys can act as “magic keys” inside abbreviations, prefixes, suffixes, and searches.
- HTML is a distinct expansion type and should be treated differently from plain text that merely contains HTML source.
- Picture and formatted-text expansions depend on target-app support.
- Descriptions are part of first-class item metadata and are especially important for long or picture expansions.
- Quick Search behavior depends on set configuration as well as descriptions/comments.
- The full product surface includes sets, publications/subscriptions, markers, regular expressions, calculator behavior, exceptions, and troubleshooting guidance from the User’s Guide.
- Quick Search supports multiple-word matching, exact-phrase matching with quotes, quick access to recent items, and editing a result with Command-Return.
- Set syncing and sharing are part of the official product story through shared folders/Dropbox and publication workflows.
- Typinator supports migration/import workflows such as importing aText snippets through exported plist/Text Substitutions data.
- Date calculation and formatting can be composed with markers plus built-in functions like `/Choose` and `/Case`.
- Trigger loops and re-triggering other abbreviations are documented patterns, including AppleScript-based self-trigger loops where direct self-invocation is otherwise not possible.

## Pattern implications for this skill

- Prefer Includes-backed text or data files over repeating long text in multiple expansions.
- Prefer script-backed helpers when inline syntax becomes brittle.
- Prefer variable assignment to repeating identical input-field definitions.
- Prefer word-break expansion for whole-word abbreviations and auto-corrections.
- Prefer descriptions/comments for discoverability when Quick Search would otherwise miss items.

## Files explicitly ingested

### Broad Core And Topic Docs

- `Introduction for AI Models.md`
- `Typinator Complete Reference.md`
- `Advanced Features & Techniques.md`
- `Quick Search & Productivity Tips.md`
- `Text Formatting & Hyperlinks.md`
- `Tips Tricks & Workflows.md`
- `Typinator User's Guide.md`

### Online Help Center

- Category: Getting Started
- Category: Using Typinator
- Category: Troubleshooting
- Category: Tips & Tricks
- `Maximize your productivity with Typinator: essential tips and tricks`
- `Fast searching and editing abbreviations`
- `Sync Typinator sets with Dropbox`
- `Publish Sets to share with others`
- `Trigger abbreviations with user input in a loop`
- `Import your abbreviations from aText`
- `Date Calculation - Creating a date for "next Saturday", etc.`
- `Formatting dates with ordinal numbers`
- `Triggers for expansions`
- `Using Typinator as a clip collection`
- `Custom search terms in Quick Search`
- `Input fields with default values`
- `Preset for Options`
- `The power of Typinator forms`
- `Easy calculations with Typinator`
- `Convert clipboard to plain text`
- `Different ways to create a line break in Typinator`
- `Variables in Typinator`
- `Creating expansions with interactive input fields`
- `Performing calculations in Typinator expansions`
- `Advanced markers in Typinator`

### Focused Topic Docs

- `About the “Includes” folder.md`
- `Advanced Expansions.md`
- `Clip Variables.md`
- `Convert Script for Typinator.md`
- `Creating Typinator Scripts.md`
- `Default Options.md`
- `Expansion Triggers.md`
- `Formatted Text.md`
- `Input Forms.md`
- `Plain Text.md`
- `Quick Ref.md`
- `Quick Search.md`
- `Random Text.md`
- `The power of Typinator forms.md`
- `TinyURL Script for Typinator.md`
- `Typinator's Default Includes.md`

## Files intentionally not treated as Typinator authority

- `Exploit GitHub as infinite storage.md`

Reason:
- it is an unrelated clipping, not Typinator documentation
