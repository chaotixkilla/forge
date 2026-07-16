# github-actions — ci adapter

Implements the **ci** capability for GitHub Actions, over the transport configured in `tools.ci.transport` (cli, api, or mcp). The [ci](../SKILL.md) skill names the operation and dispatches here; each operation below is one of the ci capability's requests, translated to GitHub's concrete surface. Resolve exact field/flag names against the live tool at call time (below) — the names here are not frozen.

## Operations

1. **Run the checks** — given a ref (branch, sha, or PR head), either trigger the checks or read their current state.
   - *trigger:* dispatch the workflow(s) that run the pre-merge checks for the ref. *cli:* the GitHub CLI's workflow-run command against the target workflow and ref; *api/mcp:* the Actions "create a workflow dispatch" endpoint (workflow id + ref, plus any inputs the caller passes).
   - *read:* retrieve the aggregate pass/fail for the ref — the check-runs (Checks API) or the combined commit status on the head sha, plus the matching Actions workflow-run and its `status`/`conclusion`. *cli:* the run list/view commands filtered to the ref; *api/mcp:* list-workflow-runs / list-check-runs-for-ref. Return a single verdict (pass = every required check concluded success; fail = any concluded non-success; pending = any still running).
2. **Await a run** — block until a run settles, within the caller's timeout.
   - *cli:* the run-watch command on the run id, or poll run-view for `status`/`conclusion` until `status` is completed; *api/mcp:* poll get-workflow-run until `status: completed`, then read `conclusion`. Return the terminal verdict; if the timeout elapses while still in progress, report a *retryable* timeout rather than inventing a verdict.
3. **Promote to an environment** — trigger, or read the state of, a deployment of a ref to a named environment.
   - *trigger:* dispatch the deployment workflow for the environment (workflow_dispatch with the environment as an input), or create a deployment against the environment. *cli:* the workflow-run command targeting the deploy workflow with the environment input; *api/mcp:* create-a-deployment (or a workflow dispatch) naming the environment. Respect a configured GitHub Environment's protection rules — a pending required reviewer or wait timer is reported upward as a *pending* promotion, not forced.
   - *read:* the deployment's latest status and the resolved environment. *api/mcp:* list-deployment-statuses for the deployment; *cli:* the deployment view/list commands. Return the state (queued / in_progress / success / failure / pending-approval) and the environment it targeted.
4. **Fetch a run's logs** — the log output of a run, or just its failed jobs.
   - *cli:* the run-view command with the log flag (and the failed-only variant when the caller only needs the failure); *api/mcp:* download-workflow-run-logs (a zip of job logs) or per-job logs. Return the log text (or the failed-job subset), so the caller can diagnose or report.

## Failure surface

Report failures upward in capability terms — the caller hears an outcome, never a raw HTTP code:

- **Not authenticated / token missing or lacking the actions/deployments scope** → report as "ci backend unavailable," which the caller's degrade path handles (and which the [ci](../SKILL.md) skill maps to guiding the user through `init:ci`).
- **Workflow / run / deployment not found, or wrong repo context** → report "the requested run was not found on the configured provider" rather than a 404; do not fall back to a different workflow or run.
- **Rate-limited or transient network failure** → report as a *retryable* ci failure, distinct from a permanent one, so the caller can back off or degrade. An await that times out with the run still in progress is the same retryable class.
- **A run concludes non-success (failed / cancelled / timed_out)** → this is **not** an adapter failure: it is the operation succeeding and returning a red verdict. Relay the verdict (and, on request, the failed-job logs) faithfully; never convert a red run into an "unavailable" that the caller might silently skip.

## Call-time discovery

GitHub Actions' surface shifts (gh subcommand flags, the Actions/Checks/Deployments API shapes, the check-runs-vs-workflow-runs distinction, deployment-status payloads), so name the operation and its purpose here and resolve the exact parameters when you call: confirm the current workflow-dispatch inputs, the run-status/conclusion field names, whether the ref's verdict comes from check-runs or the combined status, and the log-download shape against the live CLI/API at call time. An adapter that pins today's exact field names ages into a confident wrong call; one that names the operation and re-derives the arguments ages gracefully.
