# Keep callers working

When you change existing code — a signature, a return shape, a default, an error mode — the code in front of you can be perfectly correct and still ship a regression, because something you can't see on screen was calling it the old way. The judgment this rule governs is how far out from the edited line your responsibility reaches. Left to taste it goes wrong by tunnel vision — a builder makes the local change work, sees green on the file in front of them, and calls it done, while a caller two modules away now passes an argument that no longer exists. Two builders left to instinct read the blast radius to different distances. This rule pins the discriminator so two builders converge on which callers must be handled before done.

## The discriminator

The trigger is whether the change is a **contract change** — anything a caller could depend on. If it is, **every caller must be migrated or confirmed unaffected** before the change is done.

- **Is this a contract change?** A change to a **signature** (parameters, order, types), a **return shape**, an **invariant** the code guaranteed, an **error mode** (what it throws/returns on failure), or a **default** is a contract change — callers may depend on any of them. A change to purely internal implementation, with the contract identical, is not; it has no blast radius beyond itself.
- **If yes, read the full blast radius.** Find *every* caller — a usage search across the repo, the code explorer's reverse-dependency read — and for each, either **migrate** it to the new contract or **confirm** it's unaffected. Not a sample, not the ones you remember: all of them. A locally-correct change that silently breaks a caller is a **regression, not a change**.
- **If a caller can't be migrated now, the contract change isn't ready.** A caller you can't reach or can't safely update is a blocker on the change, not something to leave broken and note later — either keep the old contract working alongside the new (a compatibility path), or the change stops until the caller can move.

This is the reverse-dependency reading the orient phase set up, cashed at integration ([integrate-and-wire-up](../../phases/04-integrate-and-wire-up.md)); the migrated callers are required lines in the diff, not scope creep ([keep-the-diff-focused](keep-the-diff-focused.md)).

(basis: the **read-the-blast-radius** discipline — a change's responsibility extends to everything that depends on the contract it touches (mirrors review's read-the-diff-in-its-blast-radius stance); backward-compatibility and caller-migration practice — you change a contract *and its callers together*, or you keep the old one working until they move.)

## The anchors

- *Good:* you add a required parameter to a widely-called function, run a usage search, find all eleven call sites, and update each in the same change — the diff carries the signature change and its full blast radius, green everywhere.
- *Bad:* you change a function's return from a value to a wrapped result, fix the one caller you were thinking about, and ship — the other four callers still unwrap the old shape and now fail at runtime, a regression that looked "done" because the edited file was green.
