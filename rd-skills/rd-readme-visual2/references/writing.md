# Writing Pass

Run this over every README before validating. Visual polish doesn't rescue
weak copy. The validator flags dashes and filler words; the rest is judgement.

## Rules

- **Lead with the outcome.** The bold summary says what the reader gets ("Upload
  files to GitHub and copy shareable links"), not what the thing is ("A Python
  tool that...").
- **Problem before features.** If there's a TL;DR, it names a concrete pain point first.
- **Every feature claim has an example** or a number. "Fast" is weaker than
  "scans 10k files in 3 seconds"; "flexible" says nothing.
- **Cut filler:** "simply", "just", "basically", "in order to", "it is important to note".
- **Active voice, one idea per sentence.** Short, but full sentences, not fragments or arrow chains.
- **The project's own words.** Use the same term for the same thing everywhere
  (pick "preset" or "profile", not both).
- **Honest limits.** Say what it doesn't do. It builds trust and saves support questions.
- **Commands are copy-paste ready.** No `$` prompts inside blocks the reader
  will paste, no placeholders left unexplained.

## Machine-written tells to strip

- Em-dashes and en-dashes in prose; use a full stop, comma, colon, or parentheses
- Hollow openers: "In today's fast-paced world", "Whether you're a beginner or an expert"
- Hedging stacks: "might potentially"
- "Not X. But Y." rhetorical beats
- Lists of adjectives: "powerful, flexible, and intuitive"
- Emoji used as bullets or decoration (also a skill rule)

## Before and after

| Before | After |
| --- | --- |
| gupload is a powerful and flexible tool that simply lets you upload files. | Upload a file to GitHub and copy its Markdown link in one command. |
| It is important to note that a token is required. | > [!IMPORTANT] <br> Needs a GitHub token with `contents: write`. |
| Blazing fast performance — try it now! | Plans 500 files offline in under a second. |

## Closing question

After the draft, ask the user one question: **"Anything else to highlight or
include that I might have missed?"**
