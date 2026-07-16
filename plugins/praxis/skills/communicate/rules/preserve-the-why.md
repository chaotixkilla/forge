# Preserve the why

A decision recorded as only its conclusion is a decision that will be re-litigated. Six months on, no one remembers why the obvious-looking alternative was rejected, someone proposes it again, and the team re-runs the whole argument — or worse, reverses the call without knowing what it cost last time. The reasoning and the roads not taken are what survive to prevent that; the conclusion alone does not. This rule pins what a preserved why must contain. It is applied in [frame-the-message](../phases/01-frame-the-message.md) (recognizing the type owes a why) and [draft-the-content](../phases/04-draft-the-content.md) (writing it).

## When the why is owed

The why is mandatory for a **decision record**, and for any artifact that documents a choice future readers will live with or reconsider — an architecture note, a policy, a "we're going with X" message that closes a debate. It is *not* owed by a pure status update or a coordination message, which record a state, not a choice. The tell: **will someone later ask "why did we do it this way?"** If yes, the why is content, not optional.

## What a preserved why must contain

A why that actually prevents re-litigation carries three things — a bare "we chose X because it's better" preserves nothing:

- **The reasoning** — the criteria that decided it and how X met them, concretely enough that a reader can tell whether the reasoning still holds when circumstances change.
- **The rejected alternatives** — the real options considered, each with the specific reason it lost. This is the part most often dropped and the part that most prevents re-argument: the next person who proposes alternative Y finds Y already weighed and why it was set aside.
- **The conditions** — what would change the decision. A choice made "because we're small" should say so, so the team knows to revisit it when they're not. `(basis: ADR (Architecture Decision Record) practice — Nygard — which pins Context / Decision / Consequences and the explicit recording of alternatives and their rejection as the structure that keeps a decision from being silently re-opened.)`

## When a component isn't recoverable — say so, don't invent it

The three components are owed, but the substance gathered in [frame-the-message](../phases/01-frame-the-message.md) may not hold all of them: the decision is recorded, but the alternatives that were weighed, or the conditions that would revisit it, may simply not exist in any source you can read. When a mandated component is genuinely unrecoverable, take the same out make-the-ask-explicit takes for a nonexistent ask — **state that it is unrecorded, explicitly** ("alternatives considered: not recorded at the time"), rather than the two failing moves: omitting it silently (which produces the hollow why this rule exists to prevent) or **reconstructing plausible-sounding history** (inventing alternatives that "were probably considered" — fabrication into a record of record, the worse failure, because a future reader will trust it). A recorded gap is honest and still useful; an invented why is a landmine. If the missing component is load-bearing enough that the record is misleading without it, surface that to the user rather than shipping a record that reads complete and isn't.

## Record the honest why, not the tidy one

The reasoning recorded must be the one that actually decided the call, including the unglamorous parts — "we picked the boring option because the team already knows it" is a real and valuable why. A rationalized after-the-fact why that omits the true deciding factor (a deadline, a skills gap, a political constraint) misleads the future reader into thinking the decision rested on grounds it didn't, and they'll misjudge when it's safe to revisit. Preserve what was true, at the register the tier allows.
