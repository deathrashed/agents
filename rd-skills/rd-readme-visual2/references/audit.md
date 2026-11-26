# README Audit

Diagnose before rewriting. A rewrite that fixes the prose and keeps a broken
install has fixed nothing. In review mode, do not rewrite at all unless asked.

Score the README as it exists today. Print the scorecard before any edit, and
attach evidence to every check: a line number, a quoted sentence, or the output
of a command you ran. A check with no evidence is an opinion, and the owner can
reject it.

The usual top block already satisfies part of this scorecard on purpose (a banner
or title carries the identity, a nav bar links the licence). Where a check below
collides with a layout choice, the note says how it is satisfied.

## Band A - blocking checks

Pass or fail. A single failure means the README is not fit to publish, whatever
the rest scores.

| Check | Passes when | Layout note |
| --- | --- | --- |
| **A1 Identity** | Name and one sentence saying what it is appear before anything a reader must scroll past, and every unusual term is defined or linked | A header banner or title carries the name and subtitle; the bold summary line completes it. A banner with no summary sentence fails |
| **A2 First command runs** | The install command and first usage example, exactly as written, run in a clean environment | Run them. Record any undocumented runtime, system package, env var, or output that differs |
| **A3 Claims verifiable** | Every command, flag, default, env var, config key, path, version, and behavioural assertion matches the repo | Report the count of unverifiable claims on its own line |
| **A4 Status honest** | A reader can tell experimental / beta / stable / maintained / seeking-maintainer without opening the commit history | One line in the top block or a Status section |
| **A5 Licence reachable** | Named in the README and linked to the file | The nav bar's `License` link satisfies it; a non-permissive licence also gets one line near the top, because it disqualifies fastest |

## Band B - scored checks

Score 0, 1 or 2. Zero is absent, one is present but weak, two does its job.

| Check | Two points | Zero points |
| --- | --- | --- |
| **B1 Differentiation** | A concrete axis: a benchmark, dependency count, platform difference, deliberate trade-off | "simple and fast"; a claim with no source |
| **B2 Time to a command** | A copyable command inside the first 400 words | Only after a long preamble, or no code block at all |
| **B3 Runnable example** | Real output or effect shown, ideally also a file in the repo | A bare list of function signatures |
| **B4 Funnel ordering** | Can stop at any point without missing something that changes the decision | Detail before the reader knows what the thing is |
| **B5 Badge discipline** | 3-5, each an assessment signal answering a real question | A badge wall, or "PRs welcome" signals |
| **B6 Nothing trapped in an image** | Alt text everywhere; no command or decision-relevant fact only inside a screenshot or GIF | A GIF that is the only place the demo exists |
| **B7 Links resolve everywhere** | Checked on the repo page *and* the registry page | Assumed |
| **B8 Overflow elsewhere** | Long references and community-health content linked, not inlined | Everything dumped inline |

Pass is all five Band A checks plus 14 of 16 in Band B. That threshold is this
skill's baseline, not a published standard: move it with the owner for a stated
reason and record the reason.

## Verify every claim against the source

A README is a set of claims about a codebase, and each one is checkable. Do not
write from memory of how an API usually looks; a reader cannot tell a verified
line from an invented one.

List every claim, then check it against its own source of truth:

| Claim | Source of truth |
| --- | --- |
| Command, flag, default | Argument parser, `--help` output |
| Environment variable, config key | `os.environ` reads, config schema, example file |
| File path | Does the file exist on disk |
| Version requirement | Manifest (`pyproject.toml`, `package.json`, `Cargo.toml`) |
| Endpoint | Route table |
| Behavioural verb ("retries three times", "case-insensitive") | The code that implements it |
| Performance or scale number | A benchmark script, CI matrix, or changelog entry in the repo |

A flag documented in the README but absent from the parser is a hallucination,
not a typo. Any number, compatibility matrix, or "production ready" with no
source inside the repo comes out. When something cannot be verified, downgrade
the claim to what is verifiable and say which part is unconfirmed.

## Badge discipline

Badges are the one element with a real evidence base. Trockman et al. studied
294,941 npm packages (ICSE 2018): adopting a badge does **not** raise popularity,
and among already-popular packages excessive badge use correlates with
*decreased* popularity. Keep the distinction they draw.

| Signal | Example | Keep? |
| --- | --- | --- |
| **Assessment** - a third-party check that cannot pass unless the fact holds | CI status, coverage, published version, licence | Yes, when it answers a reader's question |
| **Conventional** - states an intent, verifies nothing | "PRs welcome", "made with love" | Cut |

The direction is sourced; a cap of four or five is the house default, not a
published figure. Maintainers over-value badges: in the same study's companion
survey, most contributors said badges do not influence them at all, so a pile of
them buys nothing.

## Common failure modes

| Failure | What it looks like |
| --- | --- |
| Rewriting before diagnosing | New prose over the same broken install |
| Padding to look serious | Architecture and roadmap sections on a 200-line utility |
| Marketing voice | "blazing fast" where a number belongs |
| Auditing one render target | Works on the repo page, dead on the registry |
| Fabricated status | "production ready" disproved by one glance at the commit history |
| Trapped instructions | The only mention of a required flag is inside a screenshot |

## The cold-reader test

Run this after the visual pass, as the outcome check the scorecard only proxies.
Give the README to a reader who has never seen the project, a person if you can
find one, otherwise a fresh agent session with no repository context. Allow 60
seconds from the top.

Ask five questions:

1. What is this?
2. Why would I use it instead of the alternative I already know?
3. Does it fit my language, platform, and licence constraints?
4. What is the first command I would run?
5. Is this project alive?

Five correct answers in the minute is a pass. A wrong answer points at a check:
question 2 is B1, question 4 is B2, question 5 is A4.

## Report format

```
README audit - acme/flowmatic   (audience: solo developer)
Band A: A1 pass · A2 FAIL (install needs Node >=20, undocumented) · A3 FAIL · A4 pass · A5 pass
Claim check: 2 unverifiable; "handles 10k req/s" (no benchmark in repo), --watch not in parser
Band B: 11/16  (B1 0, B2 2, B3 1, B4 2, B5 1, B6 2, B7 2, B8 1)
Verdict: does not pass; A2 and A3 blocking; B1 returns most per hour spent
Cold reader: 3/5; could not answer "why this over X" or "is it alive"

Fix in this order:
1. Document the Node version and re-run the install from clean (A2)
2. Remove or source the throughput claim; drop --watch (A3)
3. Add three sentences on why this over the alternative (B1)
4. Cut the badge row to three assessment signals (B5)
```

Order the fix list by return per hour spent, not by ease and not by damage
undone. Those three orderings disagree: efficiency leads with the status line
and install path, value leads with the install path and differentiation.

## What not to claim afterwards

Do not promise a conversion lift. Record the ship date, compare a full period
before against a full period after, and annotate confounders instead of claiming
a delta. Track support load first (it moves in weeks and costs nothing), then
clone or download conversion, then contributor conversion a quarter out. Drop
stars: they only go up, so they cannot show a regression.
