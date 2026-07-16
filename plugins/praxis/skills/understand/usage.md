# understand — usage

## When to use
Reach for `understand` when you need an accurate mental model of an unfamiliar system, feature, or area *before* you change it — the orientation pass that answers "how does this actually work, where does it live, and why is it this way," and hands back a map you can act on. It is read-only: it produces understanding anchored to file:line and commits, graded by how certain each claim is, not a change to the code.

## Not for — use instead
- **Gathering and weighing raw evidence across source lanes** → `gather` (the delegated engine understand consumes; it returns weighted findings, not a human-facing map).
- **An open-world, cited research report from the web** → `deep-research` (understand is grounded in *this* system; deep-research canvasses the outside world).
- **Turning the understanding into a design or requirements** → `plan` / `spec` (they consume the understanding; understand stops at the map).
- **Making the change once you understand it** → `develop` / `debug` (understand never mutates the system under study).
- **Publishing the map as a durable team document** → pipe the map to `communicate` / `publish-artifact`; understand emits the map inline (or as a `--diagram`) and owns no publish path.

## Examples
- `understand "how does the login path handle an expired token"` — frame the question, delegate the locate/corroborate reads to gather, trace the path, return a certainty-graded map.
- `understand --symbol=processPayment` — seed the investigation from a named symbol: start at its definition and fan out through its references.
- `understand --from-code=src/billing/**` — bottom-up: reconstruct what the billing code does and why, without a starting question.
- `understand --read-only "what does the migration runner touch"` — hard zero-mutation guarantee: static observation only, no runs or probes.
- `understand --deep --diagram "the request lifecycle through the middleware stack"` — widen the blast radius and secondary paths, and emit a diagram of the traced flow.

## Gotchas
- **Read-only by nature.** understand observes; it never edits, commits, or changes the system under study. The default posture *may* run or probe non-destructively to observe behavior (the top certainty rung); `--read-only` hardens that to zero execution, and the highest a claim can then reach is *traced*, not *observed*.
- **It delegates its fan-out to gather.** understand frames, traces, and synthesizes; the cross-lane locate and corroborate reads go to `gather`, which owns the `tools.knowledge` prerequisite — so understand declares no config of its own. Without gather reachable, do the reads inline; the reads are not optional, only the delegation is.
- **The map is graded, not asserted.** Every claim carries a certainty level (what you observed vs. inferred vs. took on faith). A map that states inferences as facts is the failure mode this skill exists to prevent.
- **Scope is the framed question.** understand traces the paths the question turns on and stops when the question is decided; it is not a whole-system tour. `--deep` widens the radius when the question needs it.
