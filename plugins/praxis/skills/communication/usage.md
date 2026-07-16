# communication — usage

A tool-layer interface skill: the single place the conversation backend is reached. It fronts the `communication` capability so a workflow skill names *what it needs from the conversation backend* and this skill resolves it to whichever provider is configured — the same ports-and-adapters seam `vcs` provides for the code host and `publish-artifact` provides for artifacts.

## When to use
- A skill needs to reach the conversation backend and should stay provider-agnostic: read a discussion thread to seed from, or post a message/status update to a channel or a person. Call `communication` with the operation instead of talking to a chat provider directly.
- You are adding a new skill that reads or posts on the conversation backend (spec's discussion ingest, communicate, operate): route its messaging operations through here rather than giving it its own adapter, so a provider swap changes one file.

## Not for / use instead
- Publishing a spec, plan, report, or decision record as a **team-facing document** → **publish-artifact** (the artifacts/docs port). This is the settled artifacts-vs-communication line: publish-artifact writes durable, audience-facing *documents* to a docs backend; communication reads and posts *messages and threads* on a conversation backend. Posting a link to — or a summary of — a published document into a channel is a communication `post`; producing the document itself is publish-artifact.
- Fetching or posting on a pull request, or setting a merge-gating status → **vcs** (the code-host port). Creating or updating tracked work-items → **project-mgmt** (the work-tracking port). `communication` fronts the conversation backend, not the code host or the tracker.
- Deciding *what* to post, *to whom*, or *whether* to send at all → the calling skill's judgment (e.g. **communicate** routes and pitches the message at the right altitude and audience; **operate** decides an incident warrants a notification); this skill only carries out the messaging operation it is handed.

## Operations (extended as consumers need them)
Today it serves the operations `spec` (`--from-discussion`) and the messaging consumers require; new consumers add their operations to the same interface and adapter rather than forking a new one:
`read a thread` — a discussion thread's messages, participants, and ordering, by reference, so the caller can distill its decisions, constraints, rejected options, and open points. (`spec --from-discussion` seeds a spec from it.)
`post a message` — a notification or status update to a channel or a person. (`communicate`'s message routing and `operate`'s incident notifications post through it.)

The natural next operations — `reply in a thread` (a post anchored to an existing thread) and `react/acknowledge` — are deliberately **not** exposed yet: no built consumer needs them. Each lands with its first consumer.

## Gotchas
- **It blocks without a configured backend.** `config_requires: tools.communication` with `if_missing: guide via init:communication, else block` — a conversation port with no backend has nothing to do. Callers that have a meaningful fallback (spec degrades to interrogating whatever the caller can summarize inline; a messaging consumer degrades to returning the message for the user to send by hand) catch the unavailable signal and degrade on *their* side; this skill itself blocks.
- **It performs side effects.** Posting a message mutates the conversation backend. Use `--dry-run` to preview the message and target that would be posted, without posting. (Reading a thread is read-only.)
- **It reports failures in capability terms.** The caller hears "the thread wasn't found" or "the backend is unavailable," never a provider error code — so the caller's degrade logic never has to learn a provider's vocabulary.
- **A delivered post always returns its reference.** If the message posts but a follow-on step (fetching its link) fails, the reference still comes back with that step flagged, so the caller never re-posts to recover it — a re-post would duplicate the message, and the returned reference is already complete and usable.
- **Provider coverage is by adapter.** Whichever providers have an adapter under `adapters/` are supported; adding a provider is a new adapter, no change to callers.
