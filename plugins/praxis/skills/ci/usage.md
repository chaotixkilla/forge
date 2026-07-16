# ci — usage

A tool-layer interface skill: the single place the continuous-integration / delivery backend is reached. It fronts the `ci` capability so a workflow skill names *what it needs from the pipeline* — run the checks, wait for a run, promote a build, read a run's logs — and this skill resolves it to whichever provider is configured. The same ports-and-adapters seam `vcs` provides for the code host and `publish-artifact` provides for artifacts.

## When to use
- A skill needs to reach the CI/CD backend and should stay provider-agnostic: trigger or read the pre-merge checks for a ref, wait for a run to finish, promote a merged build to an environment, or pull a failed run's logs. Call `ci` with the operation instead of talking to a provider directly.
- You are adding a new skill that touches the pipeline (integrate, maintain, operate): route its pipeline operations through here rather than giving it its own adapter, so a provider swap changes one file.

## Not for / use instead
- Fetching a change, posting review feedback, or setting a merge-gating status on the code host → **vcs** (that is the code-host port; this is the pipeline port). The two are peers: `vcs` sets a status a human or merge-protection reads; `ci` runs the checks that produce a verdict.
- Reading a production observability signal or log stream to judge post-ship health → **telemetry** (that is the observability port; `ci` reads a *pipeline run's* logs, not the running system's).
- Running the local build/test/lint on the machine (not the hosted pipeline) → that is ambient (any skill runs it directly); this skill is for the *hosted* CI/CD backend.
- Deciding *whether* the gate passes, *what* to ship, or *whether* to promote → that is the calling skill's judgment (e.g. **integrate** runs the gate and decides to land); this skill only carries out the pipeline operation it is handed.

## Operations (extended as consumers need them)
Today it serves the operations `integrate` requires; new consumers add their operations to the same interface and adapter rather than forking a new one:
`run the checks` — trigger the checks for a ref, or read a run's status + pass/fail verdict, by reference.
`await a run` — block until a run settles within a timeout; return the terminal verdict.
`promote to an environment` — trigger, or read the state of, a deployment/promotion of a ref to a named environment.
`fetch a run's logs` — the log output of a run, or of a failed job within it, by reference.

## Gotchas
- **It blocks without a configured backend.** `config_requires: tools.ci` with `if_missing: guide via init:ci, else block` — a pipeline port with no pipeline has nothing to do. Callers that have a meaningful reduced path (e.g. integrate falling back to local checks, or reporting that the hosted gate couldn't run) catch the unavailable signal and degrade on *their* side; this skill itself blocks.
- **It performs side effects.** Triggering a run and promoting to an environment mutate the backend and can move real deployments. Use `--dry-run` to preview the operation — the resolved run/target — without performing it.
- **Triggering is not judging.** `ci` returns a run's verdict; it never decides that a failing gate is acceptable or that a promotion should proceed. The caller owns that call — a returned red verdict is reported faithfully, never softened.
- **It reports failures in capability terms.** The caller hears "the run wasn't found" or "the backend is unavailable," never a provider error code — so the caller's degrade logic never has to learn a provider's vocabulary.
- **Provider coverage is by adapter.** Whichever providers have an adapter under `adapters/` are supported; adding a provider is a new adapter, no change to callers.
