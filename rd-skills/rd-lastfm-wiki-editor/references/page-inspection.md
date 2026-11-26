# Public Last.fm page inspection

Load for requests involving a Last.fm URL, checking an existing wiki, revising a live Last.fm entry, or finding a page by name.

## Input and identification

Accepted:

- Full public Last.fm artist, album, track or `+wiki` URL; or
- Artist name; album title **plus credited artist**; track title **plus credited artist**; or enough context to establish these without confusion.

When given a URL, open **that exact page first** with read-only tools; follow public redirects to learn the canonical identity. Do not substitute a search result for the supplied page without explaining the difference. For a name, search Last.fm and identify the exact canonical page rather than blindly constructing URL paths. Prefer verified public Last.fm locations:

- Artist: `https://www.last.fm/music/<artist>`
- Album: `https://www.last.fm/music/<artist>/<album>`
- Track: `https://www.last.fm/music/<artist>/_/<track>`
- Wiki views, where available, may appear at `.../+wiki`.

The patterns are informative, **not** permission to guess URL encodings or assume that every endpoint works. Verify redirects and label the entity **artist / album / track**. Do not conflate the artist's album title, the album's title track, and a similarly titled recording.

## Read-only inspection checklist

1. Confirm final Last.fm URL, displayed name, type, primary artist credits, and whether the page redirected or represents more than one entity.
2. Open the publicly accessible wiki/biography view when available and read enough to understand the **full** existing description. The page may render BBCode as HTML; do not imply rendered prose is the exact original BBCode source. Preserve BBCode when the user pastes its source.
3. Record whether the wiki is **present**, **explicitly absent**, or **not determinable**. Only choose absent if the full public page explicitly says there is no background/wiki (not simply because a crawler omitted a section).
4. Note key existing facts, valid passages worth retaining, conflicting claims, promotional language, poor formatting, missing context, and relevant shared-name artist material.
5. For existing descriptions, research important claims independently before revising. Avoid copying chunks verbatim from the existing page; honor third-party text licences and original writing requirements.
6. If content is truncated, blocked, inaccessible, or rendered without complete context, **explain that limitation** and ask the user to paste current wiki text if needed for faithful revision. You may still produce an independently researched new draft, but label it a *new draft*, not a confirmed preservation of the page's existing content.

## Shared-name safeguards

- Last.fm artist pages can combine same-name acts. Do not delete a separate act's description.
- Clearly distinguish which background belongs to which artist; explain any potential overlap to the user when auditing.
- If a full multi-artist page cannot be inspected, do not promise a comprehensive replacement preserving all existing entries. Request the relevant full text before making a replacement meant to preserve it.

## Outputs

- **Inspect/audit only:** identify page, availability of complete wiki, supported facts, problems, and recommended changes; cite sources *outside* any proposed wiki.
- **Revise:** supply updated, paste-ready BBCode; when user wants an audit too, give the audit separately. Never edit the online page.
- **Name lookup with ambiguous hits:** explain the ambiguity and ask the smallest necessary identifying question; do not silently pick an artist.
- **Missing wiki:** draft a new entry from independently verified sources, without claiming the draft was published.
