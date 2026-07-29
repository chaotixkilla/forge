# Show, don't just tell

An abstract claim asks the reader to build the picture themselves, and they build it wrong, or don't build it at all. One concrete example, a before/after, or a sample does the building for them — it out-teaches a paragraph of description because it gives the reader something to check their understanding against. This rule pins when an example is owed versus when it's padding. It is applied in [draft-the-content](../phases/05-draft-the-content.md).

## When an example is owed

Ground the abstract in a concrete instance when any of these hold:

- **The claim is a generalization the reader must apply** — a rule, a pattern, a "we always/never." Show one instance of it applied, so the reader can generalize from the case rather than parse the abstraction. (This rule's own sections do this — each states the method, then anchors it.)
- **The abstract term is ambiguous** — "make it more robust," "improve the UX," "clean this up" mean different things to different readers; a concrete before/after pins which one you mean.
- **The reader is learning** — in learning mode ([meet-the-learner-where-they-are](meet-the-learner-where-they-are.md)), a worked example is often the *primary* content and the description is the support, not the reverse.

## When it's padding

An example is overhead, not help, when the claim is already concrete and unambiguous ("the deploy is at 3pm" needs no example), or when the example restates the claim without adding a checkable instance. The discriminator: **does the example let the reader verify or apply the claim in a way the statement alone didn't?** If yes, it earns its place; if it just re-says the point in more words, cut it — that's [respect-the-readers-time](respect-the-readers-time.md) territory. One good example beats three; pick the one that covers the case the reader is most likely to get wrong.

## Prefer the reader's own case

When you can, draw the example from something the reader already knows — their service, their last incident, the code they own — rather than a generic one. A familiar example lands faster because the reader isn't learning the example *and* the point at once. `(basis: minimalism and worked-example pedagogy — concrete, reader-relevant instances teach transferable understanding better than abstract description; strongest for instructional content, applied here as the show-over-tell default.)`
