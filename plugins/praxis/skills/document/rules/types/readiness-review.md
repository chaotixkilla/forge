# Readiness review

The questions a service must answer before a change reaches its users, drawn from the launch canon and from the team's own incident history, each with its answer.

## Reader and question

The decider at the go/no-go: "Is the service ready for this change to reach users, and if not, what stands in the way?"

## Page

`own page`

## Membership

The checks the change's first exposure to users depends on: capacity, failure modes, client behaviour, monitoring, dependencies, the rollout itself. A gate's own go-when thresholds are the [cutover-plan](cutover-plan.md)'s. Its subject is the service's readiness for this change, so a task has one. It is filed again when a check is added or answered, before each gate a check names.

## Items

**Readiness check `RDY`.** One question that is answered ready or not on its own, written as its title.

- `area`: enum `architecture and dependencies`, `integration`, `capacity`, `failure modes`, `client behaviour`, `monitoring and alerts`, `processes and automation`, `external dependencies`, `rollout`. (basis: Google SRE ch. 27, launch checklist)
- `before`: when. The `GATE` it must be answered before: one whose `users see it` is `yes`, unless the check is about a preparatory step itself.
- `outcome`: enum `not ready`, `ready`, `not applicable`. `ready` and `not ready` are set only from a verification in its evidence. `not applicable` is set by the check's owner, with the reason in the body.
- `learned from`: list of text. Links to the past incidents or follow-up actions the question was drawn from. (basis: AWS operational readiness reviews, questions distilled from the organisation's own incidents)

A check still `not ready` when its gate runs makes that run a no-go, unless an accepted `RISK` `opened-by` that gate names the check, through an `opened-by` link to it as well.

Agreement `needed`, change regime `baseline`. Its decide-by is its `before`.

Shows `GATE` (home: [cutover-plan](cutover-plan.md)) and `RISK` (home: [raid-log](raid-log.md)).

## Sections

1. **What stands between the change and its users?** Always. The open checks, or a line saying every check is answered.
2. **What was checked?** Always. The check table.

## Checks

*Computed:*
- Every check has an area and a `before`.
- Once any check exists, every area has at least one, `not applicable` included. (basis: Google SRE ch. 27)
- A check whose gate has a run verification, or is the earliest gate without one, has an outcome.
- A `ready` or `not ready` outcome has a verification in the check's evidence; a `not applicable` one has its reason in the body.
- No check is `not ready` before a gate with a run verification, unless an accepted `RISK` is `opened-by` both that gate and the check.

*Judgment:*
- Every check copied from a generic list, none drawn from the team's incidents. (basis: AWS ORR)
- No check on the load the switch itself causes, such as every user signing in again at once, against the limits of each service it calls. (basis: Google SRE ch. 27, capacity for launch spikes)
- No check on how clients retry when it fails: backoff, jitter, and whether retries add to the spike.
- No check that the failure users would see pages someone.
- A check whose answer no evidence could turn to `not ready`.

## Views

- **Open checks:** `list` of `RDY` whose outcome is not in `ready`, `not applicable`, so `not ready` or missing, sorted by before: area, before, owner.
- **Check table:** `table` of every `RDY` grouped by area: outcome, before, learned from, owner, the date of its latest verification.

## Minimum form

Each section keeps its heading with one line: no check is answered yet, and who answers them.
