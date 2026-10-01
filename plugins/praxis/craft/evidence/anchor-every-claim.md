# Anchor every claim

A claim a reader cannot re-check is one they must take on your word, and one they cannot act on. "This feels fragile" gives a reader nowhere to go; "`retry()` at http.py:42 retries on any exception, including the 4xx client errors raised at client.py:88, so a bad request retries three times before failing" gives them the exact lines and the exact behavior. A defect anchored the same way — "line 42 dereferences `user.profile`, which is null whenever the account is unverified; see the caller at line 88" — gives its author the exact edit and the exact reason.

## The anchor each kind of claim owes

- **A behavior or structure claim** → `file:line` (a span for a multi-line mechanism), pointing at the exact site, not the general area. If cause and effect live in different places, name both: the line that acts, or is wrong, and the line that reveals why.
- **A "why it's this way" claim** → the commit or pull request that introduced or changed it (`commit abc123`, `PR #142`), because the reason lives in history, not in the current file.
- **An observed-behavior claim** → the observed output or state *and* how it was produced (the command run, the input, the result), so the observation can be reproduced. Without the how, it can't be graded as observed.
- **A claim that something is wrong or costly** — a defect, a risk, a quality cost → a **scenario** as well as its location: the concrete condition under which it matters. For a defect, the input or state that triggers the wrong behavior and the path that reaches it; for a quality cost, the concrete cost — the future edit a duplication will force into two places, the specific reader a name will mislead.

A claim missing the anchor it owes isn't ready to record or report: it goes back for another read, never into the result with a hedge.

## The discriminator: re-checkable vs. a vague impression

The test that separates a claim from an impression: **could the reader verify or refute it from the anchor alone, without asking you what you meant?** If the locator and the stated behavior let them reproduce it in their editor or their head, it is anchored. If they'd have to reconstruct which line and which case you meant, it is an impression — and an impression dressed as a claim wastes the reader's time and dilutes the claims that matter.

Anchoring is also what makes a claim gradable. How certain a claim is comes from how much of its evidence you actually observed or traced, and how severe from the consequence in its scenario; both need evidence with a location, so an unanchored claim can be graded on neither.
