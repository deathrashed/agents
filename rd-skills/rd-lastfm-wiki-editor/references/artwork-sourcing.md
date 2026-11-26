# Artwork discovery and upload preparation (manual publication only)

Load only for user requests for artist photographs, band pictures, record-label images, album artwork, cover art, or image files intended for manual Last.fm upload.

## Scope

- Artist photos: authentic images of the **specific** performing artist/band, not similarly named acts, fan edits, logos passed off as portraits, or AI-generated substitutes.
- Album covers: authentic cover for the **exact title, credited artist and edition**; distinguish original artwork, regional variants, reissues, remasters, deluxe editions, alternative covers and singles.
- Tracks: do not assume standalone official track artwork exists; confirm whether a single cover is distinct from the containing album.
- Always keep the image task **separate** from a prose wiki: no image URLs in final BBCode.

## Discovery order

1. User-provided image files, rights information or authorization from the rights holder.
2. Official artist/label/photographer/press-kit sources with an explicit grant matching the intended use.
3. Reputable rights-labelled archives such as Wikimedia Commons, evaluating each image's actual file-level licence, attribution and restrictions.
4. Official release pages, label catalogues, MusicBrainz/Cover Art Archive, Discogs and other music databases as **identity/provenance leads**, not proof that downloads or reuploads are authorized.
5. Other public images only as candidates, clearly labelled **rights unverified**.

Search for source/original page, photographer or artwork creator (if known), exact subject/edition, image resolution, format, visual crop, and stated copyright/licence/permission. Link to source page in the artwork report. Check the source's access and reuse terms before downloading.

## Rights safety gate

- Separate **found image**, **download permission**, and **permission to upload to Last.fm**; these are different claims.
- Do not assume public availability, an image credit, an embedded image, a database copy, Creative Commons labelling without reviewing its terms, or personal/noncommercial use automatically grants the permissions needed for Last.fm's upload terms. Last.fm users warrant rights to submit images and grant Last.fm broad reuse rights (see https://www.last.fm/legal/terms).
- Only package/download a third-party image as an upload candidate when the specific source and rights grant clearly permit the proposed use, or when the user supplied the file with an appropriate authorization. Otherwise **do not repackage** it; link the candidate and say **permission not established; obtain permission before upload**.
- If permission is limited/unclear (e.g. press-only, attribution required with no upload-compatible route, no redistribution, all-rights-reserved), keep it in the discovery report only. Never label it upload-ready.
- Do not bypass watermarks, paywalls, access restrictions, hotlink protections, robots rules, or terms of service.
- Do not synthesize, redraw, recolor, or otherwise fabricate album covers as authentic originals. Never alter a photograph to misrepresent identity or remove creator credits/watermarks.

## Local file checks

When an authorized image is available as a local file and terminal access exists, run:

`python3 scripts/check_artwork.py /path/to/image`

The script checks whether the file resembles PNG, JPEG or GIF and reports byte size and dimensions when extractable. It does **not** establish rights, identity, aesthetic quality, or live Last.fm acceptance. Verify currently documented requirements at the time of use; do not assert a fixed maximum size or dimension unless recently checked against Last.fm's own instructions.

For user-provided files, preserve originals. If a resized/converted derivative is needed for technical compatibility, require that alteration is allowed and retain an unmodified original. Do not crop out watermarks or authorship details.

## Reporting format (never inside wiki BBCode)

For each *distinct* candidate state:

- Kind: artist photo / album cover / other
- Subject and edition match: verified / uncertain, with explanation
- Preview or source page URL (if tools allow)
- Creator and origin/rights holder, if established
- Dimensions, type and file size, if measured (otherwise **not verified**)
- Reuse/upload rights: **documented permission**, **user-provided authorization**, or **permission not established** (not a legal guarantee)
- Local file download link **only if actually created and its reuse rights established**

If no eligible file exists, provide the best source leads and actionable rights questions instead of inventing an upload-ready attachment. The user must manually upload via Last.fm; never navigate to or operate its upload interface.
