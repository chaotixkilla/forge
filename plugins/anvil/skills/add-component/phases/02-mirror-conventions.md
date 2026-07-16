A plugin's components of one kind are a family: its adapters share a call-shape and an error posture, its critics open with the same kind of lens statement, its rules carry craft in the same register. A new component that ignores the family reads as foreign — the next maintainer has to context-switch to parse it, and `audit-contract`'s slot-placement and altitude checks may flag it. The cheapest way to write a well-formed component is to make it look like the ones already there, so before composing anything, learn the local convention from the existing files. Conventions are *discovered per plugin, not imposed from a template* — that's the methods-over-facts discipline applied to the kit's own authoring: the kit must build any plugin in any style, so it reads each plugin's house style rather than baking in one.

## Read the siblings

Send the plugin explorer (read-only) to the home you resolved in phase 1 and read the existing components of this same kind. Don't skim — pull out the concrete pattern the family follows:

- **Structure**: do these files lead with a why-paragraph then sections (as the kit's own phases do), or are they tight numbered lists? How long is a typical one?
- **Headers**: what section headings recur across siblings, in what order? An adapter family might consistently separate the capability it serves from the provider-specific calls; a critic family might consistently state its lens, its hunting method, and its output shape.
- **Altitude**: how abstract is the prose? A rule speaks in durable craft; an adapter is the one place that speaks in concrete tool terms. Match the register the siblings use, not a register you'd choose fresh.
- **Naming and anchoring**: how do siblings refer to capabilities, to the parent skill, to other components? Mirror the vocabulary so cross-references resolve.

In capability terms: if the plugin's existing adapters each open by naming the *capability* they back ("this implements the change-request capability for one provider") and then drop into provider specifics, your new adapter opens the same way. The example stops at the capability deliberately — the convention you're mirroring is the *shape*, and a sibling's literal provider name is its own business, not something to copy across into a different adapter.

## Match, don't innovate

This phase is mimicry, not design. If the siblings do something you'd have done differently, follow the siblings anyway — a consistent plugin is worth more than a locally-optimal file, and divergence here is exactly what `audit-contract` reads as drift. If you believe the family's convention is actually wrong, that's a separate conversation with the maintainer, not a thing to fix by quietly writing the odd-one-out.

Anti-pattern: importing a convention from a *different* plugin (or from the kit's own files) because it's the shape you just read. Each plugin owns its house style; the plugin explorer's guardrail is that it reads the target plugin or external prior art, never a sibling plugin in the same catalog. Mirror *this* plugin's family.

## When you're the first of the kind

If the home is empty — no adapters yet, the first critic, the plugin's first hook — there's no family to mirror, and this component *sets* the convention every later sibling will copy. That raises the bar, not lowers it: be deliberate and be minimal. Establish only the structure a second instance of this kind would genuinely need — the test: every section you create must hold real content *now*; a heading you'd leave thin as a placeholder is speculative and gets cut — and no speculative sections "for later" — the scaffolding-skeptic lens applies hardest to a first-of-kind, because premature structure here propagates to every future component. A spare, clear first file is a gift to the family; an over-built one is a tax.

Carry whatever pattern you settled on — mirrored or freshly set — into phase 3, which fills the body against exactly this shape.
