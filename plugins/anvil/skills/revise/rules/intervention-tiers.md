# The intervention-tier scale

Every change `revise` makes is sized here first. The tier is the **smallest mechanism that resolves the finding** — never the largest that would "do it properly." This scale is the direct fix for the bloat failure mode: it is what stops a one-word method pin from becoming a new rule, and a missing citation from spinning up any engine at all. It is cited from [03-size-intervention](../phases/03-size-intervention.md) (where each item is sized) and [05-verify-and-report](../phases/05-verify-and-report.md) (where the acceptance check asks whether every T3/T4 addition was truly the lowest tier that would reach the finding's resolved-state).

**The axis is intervention *size*, orthogonal to severity.** A finding's severity — how bad it is — is honored for ranking in [02-triage-and-dedup](../phases/02-triage-and-dedup.md); its *tier* — how much machinery the fix needs — is decided here, independently. A high-severity finding can be a one-line T1 (a data-loss bug whose fix is a single missing citation to an existing guard-rule); a low-severity one can be a T3 (a cosmetic inconsistency whose honest fix is a new shared rule). Do not let severity pull the tier up or down.

## The four tiers

Each tier names its one-clause trigger, its **resolved-state** (the observable condition that means the fix is done), and the owner that performs it.

- **T1 — Wire** *(lightest).* The finding closes by repairing or adding a **reference between pieces that already exist**: a missing citation link from a phase to an existing rule, an undeclared activating flag for an existing module, a dangling or bare-backtick link. No method judgment, no new file. *Resolved-state:* the reference resolves and loads at runtime. *Owner:* **revise edits this directly** — the only tier whose fix revise's own Edit touches, and it touches wiring, never method. *(e.g. a phase applies a rule's craft but never links it → insert the citation.)*
- **T2 — Method.** The finding lives in an existing slot's **method** — an unstated default, an open standard-point, an undefined scale, a leaked tool name that must become capability phrasing, a below-bar thin body. Closing it edits procedure or judgment prose. *Resolved-state:* two cold runs converge on the step (codify's convergence gate). *Owner:* **dispatch to [codify](../../codify/SKILL.md)** — revise never hand-authors method. *(e.g. a phase selects a default window without stating it → codify pins the default with a basis.)*
- **T3 — Component.** Closing the finding needs a **new file that does not yet exist**, inside a skill/plugin that does: a rule cited from ≥1 phase, a module plus its activating flag, an adapter, a plugin-wide explorer/critic/hook. Adding a **first-of-kind** component — a skill's *first* adapter or *first* rule — is T3, not T4: the skill it lands in already exists. *Resolved-state:* the component exists in its canonical home, wired per its kind (and for a rule, cited from the consuming phase — the T1 follow-through revise then applies). *Owner:* **dispatch to [add-component](../../add-component/SKILL.md)**. *(e.g. one judgment recurs identically across three phases with no shared home → extract one rule and cite it from each.)*
- **T4 — Structure** *(heaviest).* The finding needs **structure the skeleton does not yet have**: a new phase in a skill, a skill split, a new skill, or a new plugin. *Resolved-state:* the new structure exists and its method is filled. *Owner:* **route out** — revise recommends [scaffold-skill](../../scaffold-skill/SKILL.md) or new-plugin with its reason; the maintainer runs the builder. revise births no structure (ratified 2026-07-13). *(e.g. a friction showing one skill does two distinct jobs → recommend a split.)*

## Assignment rule

Assign each item the **lowest tier whose resolved-state the fix reaches.** Climbing a tier requires a **recorded one-clause reason** that the lower tier's resolved-state is genuinely unreachable — "a citation can't close this because the rule it would cite does not exist yet → T3," not "this feels important." The default direction is *down*: when two tiers both seem to fit, take the lower and record why if you don't. This one rule is the anti-bloat gate in a sentence.

## Adjacent-tier discriminators — mechanical, never length-based

The boundary tests are the mechanism the fix requires, not how many characters it writes:

- **T1 | T2** — does closing it **edit method prose** (a procedure, a bar, a scale, a default)? → **T2**. Does it only add or repair a **reference/declaration between existing pieces**? → **T1**.
- **T2 | T3** — does it need a **new file that does not yet exist**? → **T3**. Is it resolvable **inside an existing slot**? → **T2**.
- **T3 | T4** — does the structure the fix nests into **already exist** (an existing skill to add a rule or a *first* adapter to)? → **T3**. Must **new structure be born first** (a skill that lacks the phase, a plugin that lacks the skill)? → **T4**.

Length is explicitly *not* the boundary: a one-line edit to a judgment bar is T2 (it touches method), and a fifty-line new rule file is T3 (it is a new file). Sizing by line count would misfile both — which is exactly the reversal the ratified basis below forbids.

`(basis: ratified by the maintainer, 2026-07-13. The four-tier ladder and its mechanical boundaries are a maintainer-ratified house rule — the tiers map one-to-one onto the four owners of a fix in this kit (revise / codify / add-component / scaffold-skill+new-plugin), so each rung has a distinct owner and a distinct mechanical test. No external authority sets the tier count or the cut-points; the minimality principle they enforce — smallest *scope* that resolves, not fewest lines — is the established editorial one, grounded in the levels-of-edit tradition (JPL's Levels of Edit; the Chicago Manual's mechanical-vs-substantive distinction). No praxis scale is mirrored.)`
