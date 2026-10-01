Before any work, ask whatever the run needs answered, all in one message ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)); with `--deep`, that includes the cost question ([ask-before-a-heavyweight-run](../../gather/rules/ask-before-a-heavyweight-run.md)).

"Understand the auth system" points at everything and settles nothing; "what does the login path do when the token refresh fails, and why is it built that way" names what must be true and what evidence would prove it. Every later phase scopes itself to this one: set the scope wrong and the trace wanders.

## Frame the ask into an answerable question
State the caller's ask as one precise investigation question: what specifically must be true about the system, and what evidence would settle it. Two moves convert a topic into a question — name the concrete behavior or relationship in doubt (not "the auth system" but "the login path's behavior on a failed refresh"), and name what would answer it (the code path, the history, the observed output). `(basis: derived from [gather](../../gather/SKILL.md)'s answerable-question test)`

## Checkpoint: answerable, or narrow it
Before proceeding, confirm an answerable question survived the restatement. If the ask is too broad to point at specific surfaces ("explain the whole codebase"), narrow it with the caller, or split it into the sub-questions you would actually investigate and pick the one asked — do **not** fan out on a topic, which burns the whole investigation downstream on a guess. This is a gate. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.

## Set the scope and depth of the dig
Fix how deep to go: the **target certainty rung** for the load-bearing claims (default *traced*; [certainty-scale](../rules/certainty-scale.md)) and the **initial blast radius** — the surfaces the question directly turns on. The scope *is* the question and the stopping rule is [stop-when-answered](../rules/stop-when-answered.md); how deep varies with the question, so this is a judgment call, guided by one rule: dig until the claims the question turns on reach their target rung, no further. `--deep` raises that target — see [deep-dive](../modules/deep-dive.md).

## Seeding modes — `--symbol` and `--from-code`
Two flags seed the frame differently; both are inputs to *this* phase (a different starting point), after which the rest of the procedure runs unchanged — which is why neither is a module.
- `--symbol=<name>` seeds the frame from a named symbol: the question becomes "what does `<name>` do, and how is it used," anchored at its definition, and [locate-the-surfaces](02-locate-the-surfaces.md) starts from that definition and its call sites (rather than discovering the entry point from a free-text ask). Look the name up before the opening question: when it names more than one symbol, ask which one there.
- `--from-code=<glob|symbol>` inverts the direction: with no starting question, read the given code enough to state "what does this do and why does it exist," and let that reconstructed question set the scope. Only the frame is inverted — locate, trace, corroborate, and synthesize then run exactly as for a posed question.

The output of this phase: the framed question, the target certainty rung, and the initial scope — the investigation plan the later phases execute.
