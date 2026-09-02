# Carry status across sessions

Work outlives a session. A build gets paused, a change gets reviewed, a follow-up gets deferred — and the next session opens with none of it, so it re-derives what the last one already knew, or worse, asks the person to. The repository is not the answer: it records what the code became, never *"this was reviewed and it was clean"* or *"this is paused at slice three, waiting on a decision."* Claude's memory does persist across sessions, so it is where that state can live. The judgment this rule governs is what may be written there and how a later session is allowed to use it — because the failure mode is not forgetting, it is **remembering something that stopped being true**, which is worse than an empty memory: an empty one prompts a look, a stale one prevents it.

## What earns an entry

Write an entry only for state a later session would otherwise re-derive or ask about, and only where the repository cannot answer:

- **The status of a unit of work** — paused at a named point and what it is waiting on; reviewed, with the verdict; landed but carrying a named follow-up.
- **A decision and its reason**, where the reason is not recoverable from the diff or the history.

Write nothing the repository already records — what the code is, what a commit changed, who touched it, when. A memory that duplicates git is a second source that can disagree with the first, and the first is authoritative. Write nothing transient either: a note useful only inside the run that made it belongs in that run's report.

## Every entry names the ref it was true at, and that is what makes it safe

This is the load-bearing clause. An entry is a **record of what was true at a stated point**, never an assertion about the present, so every entry carries the ref it describes — the branch and commit the status was observed at. A reader then has something to check against, and the discipline that follows is not optional:

- **Verify before acting.** A later session treats an entry as a **lead, not a fact**. Check the named ref against the repository as it now stands; where the tree has moved past it, the entry tells you what someone once saw, not what is. Re-read before relying on it.
- **A refless entry is unusable.** An entry that names no ref cannot be checked and therefore cannot be trusted or corrected — it can only mislead. Do not write one, and treat one found as stale by default.
- **Supersede, never accumulate.** When a unit's status changes, **rewrite its entry**; do not add a second. Two entries for one unit is how a reader ends up acting on whichever they happened to read, and the older one usually reads as confidently as the newer.
- **Delete what resolved.** A unit that landed and whose follow-up closed has no status left to carry; remove it. A registry that only grows becomes a field of stale leads, and the cost of reading it eventually exceeds re-deriving the truth.

`(basis: ratified by the maintainer, 2026-09-02, who chose memory over a repository file or the tracker port after the drift cost was raised. The ref-stamp and verify-before-acting discipline are the mitigation that choice requires rather than an embellishment on it: this project has already been misled once by exactly this failure — a status list held in memory went stale and a later session acted on it as current — so the entry shape is pinned to make the check possible and the reader's obligation is pinned to make it happen. Memory is user-global and unversioned; nothing in it can be trusted the way a versioned file can, and the ref is what converts an unverifiable claim into a checkable one.)`
