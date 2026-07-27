# Index versus roster

A file that cites many others is doing one of two very different things, and the measurement cannot tell them apart. This rule pins the discriminator, because the whole value of the fan-out check rests on it: mistake a roster for an index and the audit clears a real defect; mistake an index for a roster and it demands a rewrite of something already correct.

Both shapes look identical in a diff — a list of links under a heading. The difference is what a cold executor can *do* with the list.

## The discriminator: can the executor decide, from the citing file alone, which links are in play?

- **An index routes.** Each entry carries a **firing condition** — the situation that puts that link in play — so an executor reads the list, matches its current situation against the conditions, and opens the two or three that apply. The list's length costs nothing, because triage happens before any file is opened. A twelve-entry index is as cheap as a two-entry one.
- **A roster enumerates.** Entries carry a name and, at most, a category. Nothing on the page says when each applies, so triage can only happen *inside* the files — which means the executor either opens all of them, or picks by guessing from the filename. Both failures are invisible in the output: over-reading looks like diligence and costs the window; under-reading looks like efficiency and silently drops the craft.

The test to run at each site: **cover the link targets and read only the citing file. Can you say which links this run needs?** If yes, it is an index — clear it regardless of its length or ratio. If you would have to open files to find out, it is a roster, and its length is now a real cost.

## What counts as a firing condition

It has to be a *situation*, checkable against the run in front of you, not a restatement of the file's subject:

- **Is a firing condition** — "reaching for a second abstraction", "when the change alters an existing contract", "on a slice that adds branching", "where the input crosses a trust boundary". Each names a state of the work.
- **Is not a firing condition** — a family label ("Naming & intent", "Errors & robustness"), a bare filename, or a gloss that restates what the rule is about ("how to name things well"). These tell the executor what is *inside* the file, which it already inferred from the name; they do not tell it whether *this run* needs it.

The distinction is sharp because a category is a property of the file while a condition is a property of the run. Grouping a roster into tidy families makes it more readable and no more decidable — a common and easy mistake, since the grouping genuinely helps a human browsing the library and does nothing for the executor triaging it.

## Two legitimate shapes that are neither

- **A spine.** A `SKILL.md`'s numbered steps cite every phase, unconditionally, because every phase runs. That is not a roster: there is no triage to do, the order *is* the routing, and the contract audit requires the citations. Never file a spine here.
- **A deliberate library index.** A file whose *whole purpose* is to be the catalogue of a craft library, cited from a phase that states the firing conditions itself, is an index one hop removed. Judge the pair together: if the routing exists anywhere on the path the executor actually reads, the requirement is met. What fails is routing that exists *nowhere* — neither at the citation nor in the file it points to.

## The remedy is conditions, not cuts

When a site is a roster, the fix is almost never to delete rules — they are usually earning their keep individually, and cutting a library to make a routing problem smaller trades a real standard for a token saving. The fix is to give each entry the situation that fires it, so the same library becomes triageable. Where that turns out to be impossible for some entry — no situation distinguishes it, it applies always or never — *that* is worth a second look, because a rule with no firing condition is either a rule that belongs inline in the phase or one whose subject was never a decision. Route that observation to the economy lens rather than resolving it here; this rule is about routing, not about whether a rule deserves to exist.
