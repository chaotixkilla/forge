This is the gate the whole skill exists for. Each *act* item now gets a size — the mechanism its fix actually requires — and that size is what routes it in the next phase and caps how much machinery it may spend. Everything before this decided *what* is wrong and *whether* to fix it; this decides *how much* to do about it, and the discipline here is the difference between a proportional diff and the pile of over-built edits that motivated the skill.

## Assign the lowest tier that resolves

For each *act* item, assign its tier from [intervention-tiers](../rules/intervention-tiers.md) — **T1 Wire / T2 Method / T3 Component / T4 Structure** — by the rule's mechanical discriminators (does closing it edit method prose? need a new file? need structure that doesn't exist yet?). The assignment is not free choice: take the **lowest tier whose resolved-state the fix reaches**. When two tiers both look plausible, the lower wins unless you can state, in one clause, why the lower tier's resolved-state is genuinely unreachable — and when you climb, **record that clause** with the item. That recorded reason is what phase 05 audits; an unjustified climb is exactly the bloat this gate catches.

The output of this step, per item, is the pair: **its tier, and (if it climbed) the one-clause reason.** Nothing more — you are sizing here, not yet fixing.

## Size, don't re-grade

The tier is the **intervention axis**, orthogonal to the severity grade carried from triage ([intervention-tiers](../rules/intervention-tiers.md) carries the worked cases of the two coming apart). Don't read severity as a tier signal: grade orders *what to do first*, tier decides *how much to do*. Sizing by importance instead of by mechanism reintroduces the heavy-treatment failure from the other direction.

## When an item resists a single tier

Two cases need care before you leave this phase:

- **A clustered item spanning several sites or mechanisms** (the same judgment left unpinned across three phases; one missing default surfaced in three places). Size by *where the correct behavior should live*, not by the count of witnesses. If a shared home for it **already exists** and the sites merely fail to reach it → **T1**, cite it from each. If the behavior is **identical** across sites and no shared home exists → **T3**, extract one component then wire the citations (the ordinary T3→T1 follow-through). If the sites need **genuinely different** corrections, triage mis-clustered them — return them to [02-triage-and-dedup](02-triage-and-dedup.md) as separate items, each sized on its own. Record which case applies.
- **An item that will not size because its fix is undefined.** If you cannot name the mechanism a fix would use — the finding says something is wrong but not what "fixed" looks like — it is not sizable and was not fully raised to intake's bar; send it back to **hold** (if it needs a maintainer decision to become concrete) rather than guessing a tier. A guessed tier dispatches real machinery at an undefined target.
