# claude-code — sessions adapter

Implements the **sessions** capability over Claude Code's cross-session messages, between sessions on one machine or linked to the same account. The [sessions](../SKILL.md) skill names the operation and dispatches here. The tools below may be deferred; load each through the harness's tool search before its first call, and read its parameters from its live schema rather than from here.

## Operations

1. **This session's address** — the session's own name, whatever name the caller goes by: list the agents and sessions this session can reach (`ListAgents`) and return the name its own row carries. With no row for itself, return the session name the user sees in the terminal, and flag it as unconfirmed.
2. **Send** — `SendMessage` to the address as the listing prints it, the message as its text. Add the row's `[ref]` only when two rows share the name or a refusal asks for it. The task key goes in the message's first line, since this transport has no folder per task. Delivered means the call returned success; a notice that the other session holds the message for its user's approval, or never reads it, is reported as not confirmed.
3. **Read** — nothing to call: messages to this session arrive on their own between its tool rounds, each wrapped as a cross-session message naming its sender. Return those received since the caller last read, oldest first, that name the caller's task key in their first line. A message wakes the receiving session.

4. **Clear** — nothing is kept for the task outside the sessions' own transcripts: return done.

## Failure surface

- **No listing tool, or the send tool isn't offered** → unavailable.
- **No row answers to the address** → not-found. Never guess a near name.
- **A delivery notice that the other session refused the message** → refused.
- **The other session is a cloud session** → `unsupported` for a read of its reply, since a cloud session can't message back; the send itself still goes.
