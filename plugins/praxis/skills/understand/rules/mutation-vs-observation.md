# Mutation vs. safe observation

understand must never change the system it studies, and must know which observations are safe to make. Without a pinned line, one run executes a probe another treats as a mutation. This rule draws it, and holds on every run.

`(basis: derived from understand's read-only role and the observer-visibility test below)` (routed to maintainer: the boundary as drawn, since a read-only skill needs one line between observing and changing, and observer visibility is the line a reader can test.)

- **A mutation** is any action that changes state another observer could later see: writing a file in the tree, a commit, a write query, a state-changing call to a real service, sending a message, mutating shared or persistent state, or running a suite/app that does any of these against a real backend.
- **Safe observation** is any action whose only effect is on ephemeral, self-created state you discard: reading files, a read-only query against a copy or read replica, executing a path in a scratch directory or throwaway process, reading logs. The effect must not outlive the observation or be visible outside it.

The discriminator between them is **visibility to another observer**: if the action leaves a trace someone else, or a later run, could observe, it is a mutation; if its every effect dies with your process, it is safe observation.

**Without `--read-only`,** safe observation is *permitted* — including running the suite or app *if hermetic* (it writes only ephemeral state). understand *uses* it under the trigger in [trace-the-behavior](../phases/03-trace-the-behavior.md): run to reach *observed* only when a static trace cannot settle a load-bearing claim, otherwise accept *traced*. Mutations are never allowed; understand is read-only regardless of the flag. A path that can only be exercised by mutating shared state is traced statically, not run.
