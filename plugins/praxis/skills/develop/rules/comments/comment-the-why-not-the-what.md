# Comment the why, not the what

The moment this rule governs is the one where you've just written a line and feel the pull to explain it. Some of those comments earn their place; most are noise. The failure when it's left to taste: one builder narrates every line (`// increment the counter` above `count++`), producing comments that add nothing and rot the instant the code shifts under them; another writes nothing, leaving the one genuinely non-obvious decision — the workaround, the constraint, the road not taken — unexplained, so the next reader "cleans it up" and reintroduces the bug it dodged. Two builders diverge on which lines deserve a comment.

## The discriminator

A comment earns its place when it says something the code **cannot say itself** — and the test is: *if you deleted the comment, would a competent reader be able to recover this from the code alone?*

- **If yes — the code already says it — the comment is noise.** A comment that restates what the next line plainly does (`// loop over users` above the loop) carries zero information and actively rots: the code changes, the comment doesn't, and now it lies. Delete it.
- **If no — the information lives only in your head — write it.** The things code cannot say: *why this approach over the obvious one*, a *non-obvious constraint* the code must honor, the *reason a workaround exists* (and what breaks without it), a *warning* about a sharp edge, the *load-bearing "why"* behind a choice that looks arbitrary. This is what survives refactoring because it isn't about the mechanics.
- **When the urge is to explain the *what*, first try to make the code say it.** A comment is the second-best tool for clarity; a better name or an extracted, well-named function is the first ([name-for-the-reader](../naming/name-for-the-reader.md)). Reach for a comment only for the meaning that *no* renaming can carry — intent and rationale, not mechanics.

(basis: Ousterhout, *A Philosophy of Software Design* — comments should capture what is *not* obvious from the code; a comment that merely repeats the code adds no information. The why-not-the-what framing is convergent with Hunt & Thomas, *The Pragmatic Programmer* — comment *why* something is done, not *what*.)

## The anchors

- *Good:* `// Retry twice, not the usual once — this endpoint 500s on cold-start and recovers on the second hit.` The reason is invisible in the code; deleting the comment loses it, and a reader who "simplified" the retry would reintroduce the failure.
- *Bad:* `// set the timeout to 30 seconds` above `timeout = 30`. It restates the line, adds nothing, and the day someone changes the value to 60 the comment silently starts lying ([keep-comments-truthful](keep-comments-truthful.md)). If 30 is *load-bearing*, the comment should say *why 30* — not *that it is 30*.
