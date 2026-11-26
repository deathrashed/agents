# Last.fm Wiki Editor — Agent Skill v1.1

A portable, **research-and-preparation-only** Agent Skill for Last.fm artist, album, and track wiki descriptions, existing-page audits, BBCode revisions, and optional image/artwork sourcing. It **never** edits a page, changes an account, or uploads an image to Last.fm. You copy the text or upload a suitably authorized image yourself.

Based on the [Agent Skills specification](https://agentskills.io/specification), [Last.fm markup reference](https://www.last.fm/help/markup), [community guidelines](https://www.last.fm/help/guidelines), and [terms](https://www.last.fm/legal/terms).

## Contents

```text
lastfm-wiki-editor/
├── SKILL.md                         # Required Agent Skills entry point
├── references/
│   ├── research-protocol.md         # Fact checking, evidence, citations
│   ├── editorial-modes.md           # Modes, prose style, subjects
│   ├── lastfm-bbcode.md             # BBCode formatting and linking
│   ├── page-inspection.md           # Public URL/name lookup and wiki audit
│   └── artwork-sourcing.md          # Artwork research and rights workflow
├── scripts/
│   ├── validate_wiki.py             # Local BBCode lint
│   └── check_artwork.py             # Local PNG/JPEG/GIF metadata checks
├── tests/
│   ├── test_validate_wiki.py
│   └── test_check_artwork.py
├── evals/
│   └── evals.json                   # Agent-level behavioral scenarios
└── README.md
```

## Install

Unzip and copy the **whole** `rd-lastfm-wiki-editor` directory to your Agent Skills-compatible client's skill location. An example for a VS Code / Agent Skills project:

```text
project/.agents/skills/rd-lastfm-wiki-editor/SKILL.md
```

The exact location differs by client; make sure the directory matches the YAML `name: lastfm-wiki-editor`. Browser/search capability is recommended. Python 3 is optional. The package does not authenticate with Last.fm and requires no Last.fm API key.

## How it works

1. **URL or name:** Give a direct Last.fm URL or the artist name / album-and-artist / track-and-artist. The skill resolves the **specific** public Last.fm page.
2. **Inspect:** When checking an existing entry, it tries to read the complete public wiki, distinguishes an empty wiki from inaccessible content, and protects other artists sharing the same name.
3. **Research:** It cross-checks original release dates, credits, labels and background against more reliable evidence.
4. **Draft:** It generates publication-ready, pasteable BBCode, or a research/audit report if that's what you asked for.
5. **Artwork (optional):** It finds authentic artist photos and exact album covers, including source/creator, edition, resolution where measurable, and permissions status. It only produces downloadable copies when the necessary rights can be established; otherwise it provides source leads and identifies the missing permission.
6. **Manual final step:** You review the description and paste it into Last.fm, and separately upload any image for which you have appropriate rights. The skill never submits either.

## Example requests

- `Check https://www.last.fm/music/200+Stab+Wounds and produce a comprehensive revised wiki. Don't edit the page.`
- `Write an album wiki for Manual Manic Procedures by 200 Stab Wounds, checking the existing Last.fm album page first.`
- `Find the original album cover, tell me who owns it, and whether I have permission to upload it to Last.fm.`
- `Find high-quality artist photos for this exact band. Show sources and permission status; don't repackage unlicensed images.`
- `Audit this Last.fm track wiki, check dates and credits, and show the factual corrections before rewriting it.`
- `I've pasted the existing wiki source. Preserve every verified section about other bands sharing this name.`

## Local check commands

From the skill directory:

```bash
python3 scripts/validate_wiki.py /path/to/wiki.txt
python3 scripts/check_artwork.py /path/to/authorized-cover.png
python3 -m unittest discover -s tests -v
```

`validate_wiki.py` checks markup, **not facts**. `check_artwork.py` checks file signatures, dimensions and byte size, **not identity, licensing, rights or actual Last.fm upload acceptance**.

For schema validation, run `skills-ref validate ./lastfm-wiki-editor` if the official [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) tool is installed.

## Output behavior

- **Wiki only:** BBCode only, no headings around it, external URLs, source lists or markdown formatting.
- **Audit/research:** sourced findings with uncertainty and links.
- **Wiki + artwork:** independent, clearly separated paste-ready BBCode and image-candidate report/downloads if appropriately authorized and actually generated.
- **Unreachable wiki:** honest limitation; the skill may request the original text to preserve existing content safely rather than pretending no wiki exists.

**Important:** The skill's no-external-links, neutral third-person style and prose structure are user-defined publishing standards. The Last.fm markup help documents BBCode syntax, not every editorial rule in this skill. Rights and upload rules must be checked against current Last.fm requirements when sourcing artwork.
