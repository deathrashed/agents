# Last.fm BBCode: supported syntax and publication style

**Authoritative format guide:** https://www.last.fm/help/markup

Last.fm supports the tokens below. Its markup documentation explains syntax; the extra editorial restrictions in this skill (such as “no external links” and “no bulleted discographies”) are **user-defined publication style**, not claims about what the parser technically permits.

| Element | Syntax |
| --- | --- |
| Bold | `[b]Text[/b]` |
| Italic | `[i]Text[/i]` |
| Raw URL | `[url]https://www.last.fm/[/url]` |
| URL with label | `[url=https://www.last.fm/]Last.fm[/url]` |
| Unordered list (supported, normally avoid in wiki prose) | `[ulist][li]One[/li][li]Two[/li][/ulist]` |
| Last.fm user | `[user]username[/user]` |
| Artist | `[artist]Artist Name[/artist]` |
| Album | `[album artist=Artist Name]Album Title[/album]` |
| Track | `[track artist=Artist Name]Track Title[/track]` |
| Genre/tag | `[tag]genre name[/tag]` |
| Event | `[event=123456]Event label[/event]` |

## Linking rules

1. Prefer dedicated artist/album/track/tag tags instead of URL markup.
2. Use artist metadata corresponding to the *actual* album/track entry. Featured artists and compilations require extra care. A correct title with an incorrect `artist=` attribute can point to the wrong page.
3. Link established entities on relevant first mentions, not every occurrence. Do not automatically self-link the entry's subject to its own page.
4. Genre links represent documented, appropriate categories. Do not over-tag merely because tags exist in the Last.fm database.
5. Internal URL tags may point only to `last.fm` and its legitimate subdomains. This skill bans **external** URLs in published wikis even though Last.fm's parser technically supports generic URLs.
6. Do not create links based only on coincidental name matches; verify identity.
7. The bracket content and closing tag must match the syntax exactly. Example: `[album artist=Radiohead]Kid A[/album]`, not Markdown and not `[album]Kid A[/album]`.
8. Last.fm markup does not require self-linking artist names. Start with plain text where the article already identifies its subject.

## Formatting examples (illustrative only)

Artist-style passage:

```text
Example Artist is a fictional group used here to demonstrate formatting. Its sample album, [album artist=Example Artist]Example Album[/album], contains [track artist=Example Artist]Example Track[/track].

[b]Related Recordings[/b]
The sample recording is associated with [tag]death metal[/tag] in this formatting demonstration.
```

Album-style passage:

```text
Example Album is a fictional release attributed to Example Artist. Its illustrative opening track is [track artist=Example Artist]Example Track[/track].
```

These are syntax demonstrations, **not sourced music facts**. Never reuse fictional assertions in a real wiki.

## Publication prohibitions

- No external links, citations, research source lists, Markdown headings, Markdown link syntax, or Markdown `**bold**` in final wiki text.
- Do not wrap the completed wiki in a Markdown code fence; output its BBCode as plain text.
- No unrequested unordered lists or one-line metadata tables, even though Last.fm recognizes list markup.
- `user` and `event` tags are supported but should be included only when directly relevant and verified.

## Pre-publish syntax checks

Use `python3 scripts/validate_wiki.py <draft.txt>` if local Python is available. The bundled checker detects common errors (unbalanced tags, missing artist attributes, external HTTP links, and Markdown markers). It cannot verify factual claims, navigation targets, stylistic quality, or Last.fm server-side rendering; review those manually.
