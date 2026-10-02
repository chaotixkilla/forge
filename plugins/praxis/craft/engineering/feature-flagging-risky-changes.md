# Feature-flagging risky changes

The moment this rule governs is deciding how a change goes live: the pull to gate it behind a switch — a flag, a config toggle, a percentage rollout — so it can be turned off without a code revert. The switch has to exist in the code before the rollout can use it, so the decision is made before the change ships and checked when it does. But a flag is not free. It forks every path it guards, and a flag left in past its purpose is debris that outlives the reason it existed. So the judgment cuts both ways: flag a change too eagerly and you litter the code with dead switches nobody prunes; ship a hard-to-undo change bare and a bad rollout means an emergency revert under fire.

## The discriminator

A change earns a flag when it is **hard to undo once live** *or* **needs a staged rollout** *or* **must be revertible without a code revert** — and a flag that clears that bar is only justified with a **named removal condition** attached at birth.

- **Hard to undo once live.** The operative property is *undo-ability*, not blast radius: gate it when a plain revert would **not** cleanly restore the prior state — the change moves data (a migration, a backfill, a write to a shared store), or alters a user-facing flow people will build habits on, so state or expectations have already shifted by the time you'd roll back. Touching a shared hot path only earns a flag *if it shifts observable behavior* in that irreversible way; a **behavior-identical** change to a hot path (a pure optimization) is *not* hard to undo — a clean revert fully restores it — so it falls under the don't-flag case below, high-traffic or not. Blast radius alone is a reason to test and review hard, not to flag.
- **Needs a staged or percentage rollout.** You want it live for a fraction of traffic, a cohort, or internal users first (a dark launch) before it faces everyone. A flag is the rollout control; without one, "on" means "on for all."
- **Must be revertible without a code revert.** When a bad outcome must be killable in seconds — by an operator flipping a switch, not by shipping and deploying a reverting commit — the switch has to exist ahead of the failure.
- **A trivial, easily-reverted change needs no flag.** A pure internal refactor with unchanged behavior, a change a single clean revert fully undoes, an isolated unit no live path yet reaches — flagging these just pays the branching-and-cleanup cost for nothing. When none of the three tests fire, ship it bare.

Every flag that *is* justified is born with its retirement record — who removes it and the condition that ends it, such as "delete after the cohort hits 100% and holds a week" — per [retire-the-switches](retire-the-switches.md).

(basis: Hodgson, "Feature Toggles", martinfowler.com)

## The anchors

- *Good:* a change to the checkout flow — user-facing and hard to walk back once people transact on it — ships behind a toggle defaulting off, enabled for internal accounts, then a rising traffic percentage, with the flag's declaration reading "remove after 100% for two weeks with error rate flat." One switch flips it off if the funnel drops. The flag is a distinct, focused addition, kept separate from the behavior it guards ([separate-refactor-from-behavior-change](separate-refactor-from-behavior-change.md)).
- *Bad:* a rename of a private helper, behavior identical, wrapped in a new `useNewHelper` flag "to be safe" — a switch guarding a change a one-line revert already undoes, with no removal condition, now a permanent fork two readers must trace. Or the mirror failure: a schema migration shipped bare with no kill switch, so a bad column forces a panicked rollback of already-written data. The flag is a scope decision — keep it deliberate and keep the diff focused on the change it protects ([keep-the-diff-focused](keep-the-diff-focused.md)).
