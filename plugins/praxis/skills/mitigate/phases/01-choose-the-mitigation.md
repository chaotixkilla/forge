Once an incident is confirmed, the job changes from *understanding* to *stopping the harm*. mitigate carries the authority to act on production before the cause is known — the authority a plain investigation deliberately doesn't have, and defers to a declared incident.

## Reach for the fastest safe, reversible mitigation

Apply [mitigate-before-diagnose](../rules/mitigate-before-diagnose.md): the question is "what restores service fastest and safely?", not "what caused this?" — finding the cause comes after, and isn't mitigate's. Prefer a **reversible** mitigation whose blast radius you can bound — roll back the recent deploy, fail over to a known-good replica, shed load, flag off the feature. An irreversible action (a data backfill, a schema change, a forward-fix that can't be unwound) is a last resort, taken only with the user's confirmation. That is a question worth stopping for, like the cost question in [ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md): ask with the action and what it can't undo spelled out. With no one to answer, don't take it: return it as the recommended action.

Read the incident's prior actions first, when the caller passes them: a mitigation already tried isn't repeated or undone blindly.

The output of this phase: the chosen mitigation, its kind by [mitigate-before-diagnose](../rules/mitigate-before-diagnose.md)'s test (durable or provisional), the path that owns it, and whether it erases volatile state, for [preserve-the-evidence](02-preserve-the-evidence.md).
