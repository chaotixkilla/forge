# How-to

How to carry out one operation on the system, as steps a reader follows.

**Reader and question.** New engineer and maintainer, with one job to do: "how do I get this done here?"

**Page.** `own page`

## Membership

A result that tells someone how to operate the touched part toward one goal: rotate a key, run a migration, recover a stuck job, or run and test the part locally. Its subject is the goal, held in `goal` on its procedure and invariants, so a task has one per goal. No explanation the steps don't need, which belongs to an [explanation](explanation.md) page linked instead.

System documentation, bounded as [shape-the-document](../../phases/02-shape-the-document.md) says.

## Items

**Procedure `HOW`.** Exactly one per page: the goal, with its steps in the body.
- Fields: `goal` text, the goal the page serves; `run` enum `run`, `not run` — whether a result shows the steps carried out as written.
- Change regime: `living`.
- Agreement: `none`.

**Contributor invariant `INV`.**
- Fields: `goal` text, the goal of the page it stands on; `guarded by` text — the test or check that fails when it breaks, or "nothing".
- Granularity: one thing that must stay true in the part for any change to be safe, such as every query being scoped to its tenant. A test that guards it `verifies` it. (basis: maintainer, 2026-11-11, the developer's how-to owing the contributor invariants)
- Change regime: `living`.
- Agreement: `none`.

## Sections

1. **What do you need first?** Always. Access, tools and state the steps assume.
2. **How do you do it?** Always. `HOW`'s steps, numbered, one action each, with the command or screen exactly as written. When its `run` is `not run`, the section opens with one line saying the steps haven't been carried out as written.
3. **How do you know it worked?** Always. What the reader sees when it did.
4. **What must stay true?** When the result names invariants. The invariant table.
5. **What if it goes wrong?** When the result says how a step fails. Each failure and the way back.

## Checks

- *Computed:*
  - exactly one `HOW` whose `goal` is the page subject;
  - that `HOW` has `run` filled, which sets whether section 2 opens with its untried line;
  - every `INV` whose `goal` is the page subject has `guarded by` filled.
- *Judgment:*
  - a step that explains rather than instructs;
  - more than one goal on the page;
  - an invariant guarded by nothing, with no follow-up to guard it.

## Views

- **Invariant table** (section 4): `table` of `INV` whose `goal` is `page subject`: guarded by, what `verifies` it (`verified-by`, empty marker `none`).

## Minimum form

"No prerequisites known", `HOW` with its goal and the steps "not yet established", and the check "not known".
