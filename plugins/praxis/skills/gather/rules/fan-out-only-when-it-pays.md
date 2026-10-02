# Fan out only when it pays

Recent models already delegate more than a task needs, and every agent a run recruits spends its own context and tokens: a run that recruits by reflex can use a session's whole budget on work one context would have done. So every "recruit" in praxis grants permission; it doesn't command.

## When to recruit

Recruit an agent only when one of these holds, and say which:

- **Independent breadth.** Two or more lanes or units each need more reading than fits beside the rest in this context, and none depends on another's result.
- **An independent view.** The procedure calls for a judgment made without this context's assumptions (a critic, a refuter) at the rigor the run carries.
- **Isolation.** An input must stay out of the work, and this context already holds it.

Otherwise work directly. A sequential step, a single file or module, a lane of a few reads, or anything this context already holds is done inline. Every recruiting step in praxis says what to do without fan-out, and that path is the default.

## The cap

Each recruiting step recruits at most three agents, in a single round. A heavyweight flag the user approved ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)) lifts the cap to twelve. Never recruit again to chase what a round brought back: follow its leads yourself, with the method of the lane that owns each, until the procedure's own stop. A step with more lanes or views than its cap recruits up to the cap and does the rest inline.

(basis: maintainer, 2026-09-02, for never passing session limits, a dozen at most and one round; Anthropic's prompting guidance on recent models' predilection for subagents) (routed to maintainer: three per step by default, since most phases recruit one to three explorers or critics.)

This is a run-conduct rule, kept in gather beside [ask-while-the-user-is-here](ask-while-the-user-is-here.md) and [ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md) though every skill that recruits cites it, because none of the craft library's three families fits it. (routed to maintainer: a fourth craft family for run conduct, or leave the three here.)
