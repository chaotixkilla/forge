# Anchor every claim

A claim a reader cannot re-check is one they must take on your word — and understand's product is precisely a map they can *verify*, not trust. "The retry logic looks fragile" gives a reader nowhere to go; "`retry()` at http.py:42 retries on any exception including the 4xx client errors raised at client.py:88, so a bad request retries three times before failing" gives them the exact lines and the exact behavior. This rule requires every claim in the map to carry a locator matched to its kind, so any reader can re-verify it and any later run can build on it.

## The anchor each kind of claim owes
- **A behavior or structure claim** → `file:line` (a span for a multi-line mechanism), pointing at the exact site. If cause and effect live in different places, name both — the line that acts and the line that reveals why.
- **A "why it's this way" claim** → the commit or PR that introduced or changed it (`commit abc123`, `PR #142`), because the reason lives in history, not the current file.
- **An "observed behavior" claim** → the observed output or state *and* how it was produced (the command run, the input, the result), so the observation can be reproduced — this is what earns the *observed* certainty rung ([separate-fact-from-inference](separate-fact-from-inference.md)).

## The discriminator: re-checkable vs. a vague impression
The test that separates a claim from an impression: **could a reader verify or refute it from the anchor alone, without asking you what you meant?** If the locator and the stated behavior let them reproduce it in their editor or their head, it is anchored. If they'd have to reconstruct which line and which case you meant, it is an impression — send it back for another read, don't record it with a hedge. An unanchored claim also cannot be graded on the certainty scale, since the grade comes from evidence that has a location — another way of seeing that it isn't finished.

Cited from [trace-the-behavior](../phases/03-trace-the-behavior.md), [corroborate-against-reality](../phases/04-corroborate-against-reality.md), and [synthesize-the-answer](../phases/05-synthesize-the-answer.md).
