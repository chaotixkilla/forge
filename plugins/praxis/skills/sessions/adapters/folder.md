# folder — sessions adapter

Implements the **sessions** capability over files in the main checkout, which every worktree of the repository shares, for when the harness offers no cross-session messages. The [sessions](../SKILL.md) skill names the operation and dispatches here. It needs nothing installed.

The task's folder is `.claude/praxis/coordination/<key>/` in the main checkout, `<key>` the task key. Each session has a folder there by its address, holding `inbox/` and `read/`.

## Operations

1. **This session's address** — the name the caller goes by. Create its folder if missing and return the name.
2. **Send** — write the message as one file in the recipient's `inbox/`, named `<UTC time, to the millisecond>-<sender address>.md`. Write it under a temporary name in the same folder first, then rename it, so a reader never sees half a file. Delivered means the rename succeeded.
3. **Read** — list this session's `inbox/` in name order, which is time order. Return each file's text with its sender and time from the name, then move it to `read/`. Nothing announces a new file, so a message doesn't wake the receiving session.

4. **Clear** — remove the task's folder and everything in it.

## Failure surface

- **The main checkout can't be found from this worktree** → unavailable.
- **No folder for the recipient** → not-found.
- **A file system error on write or rename** → retryable once, then permanent, with the path.
- **Refused** never happens here: a file can't be declined. A session that won't take a message says so in a reply.
