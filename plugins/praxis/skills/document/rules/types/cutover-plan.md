# Cutover plan

How a change reaches production users in steps: each gate, what has to be true before it opens, what stops it once open, and how it is undone.

## Reader and question

On-call, running the cutover, and the decider who calls go at each gate: "At this gate, do we go, and if it goes wrong, how do we get back?"

## Page

`own page`

## Membership

The steps the change reaches production through, each with its go/no-go card, and the metrics those cards read. What the service must have in place before any gate is the [readiness-review](readiness-review.md)'s; what people are told is the [communications-plan](communications-plan.md)'s; what on-call does when an alert fires is the [runbook](runbook.md)'s. Its subject is the change's path to production, so a task has one. It is filed again when a gate or a metric changes, and after each gate runs.

## Items

**Gate `GATE`.** One step that changes production and can be gone or stopped on its own: a percentage, a cohort, a flag, a switch, a contract removal, or a preparatory step nobody sees, such as copying data, a shadow write or log, or a backfill. (basis: benchmark, 2026-11-13, a copy running in production was filed nowhere, and the status said nothing was built) Its title opens with its step's code, `<code> · <name>`, such as `C1 · MCP requires an organization`, as plan's slice-and-validate phase assigns it. Its fields are its go/no-go card:

- `phase`: enum `expand`, `migrate`, `contract`, `single`. A change to a contract or a data format splits into expand (readers learn the new form), migrate (writers and clients move) and contract (the old form goes); every other step is `single`. (basis: Sato, parallel change; AWS Builders' Library, prepare before activate)
- `exposure`: text. Who or what share of traffic it reaches.
- `users see it`: enum `yes`, `no`. `no` for a preparatory step: whatever share of traffic it touches, no person sees anything change.
- `touches`: list of text. The components its step changes, each named as the design names it, so a reader sees which parts each gate moves.
- `one-way`: enum `yes`, `no`. Whether it can be undone once it has run.
- `opens on`: when. The planned day, a window's first day.
- `driver`: text. The one person who runs the step.
- `decides`: text. The one person who calls go or no-go.
- `go when`: list of text. Each criterion is `MET-n`, a threshold, the window it is observed over, and what the threshold is relative to: `none` (an absolute threshold), `baseline` (the metric's baseline) or `control` (a control group observed over the same window). The gate `rests-on` that metric. (basis: experimentation practice compares a treatment to a control)
- `abort when`: list of text. The same form: what, once the gate is open, means roll back now.
- `bake`: text. How long the gate holds before the next one may open.
- `rollback`: text. The steps that undo it, or, when the documentation plan owes a runbook, the procedure ([runbook](runbook.md)) it `rests-on` that holds them, readers rolled forward first and writers rolled back first, then what undoing it leaves in place, such as credentials already issued, messages already sent or data already written, or `nothing`; for a one-way gate, the restore, which the gate `rests-on` as its restore path (`RST`) when one is filed.
- `rollback tested on`: date, and `rollback tested in`: text, the environment. Both are read from the latest verification of the rehearsal `TEST` ([test-plan](test-plan.md)) that `serves` the gate, never from the gate's own evidence, and are never set without one.
- `fix forward when`: text. The conditions under which fixing forward replaces rolling back, or `never`.

A gate's body is its steps: only the actions that run this gate's step, numbered in order, from the rollout or the sources, each with what it proves or what stops the run when they say so; the order of the gates is the gate timeline's, not a body's. With no steps in the rollout or the sources, the body is one line saying so and what would write them. (basis: benchmark, 2026-11-13, a step's run sheet sat in the sources while every gate card said nothing about what to run)

**A gate filed already run.** A step the sources show run, or running, in production when its gate is first filed. Its `opens on` is the day it started, missing when the sources don't give one, and its run is a verification on it, dated by the source that shows the run, else by this filing: `holds` when the source reports the run without a failure, `fails` when it reports one ([mine-the-sources](../../../../craft/evidence/mine-the-sources.md)). A copy, backfill or shadow write is `expand` when the rollout or the sources name a migrate or contract step for the same data, else `single`.

A gate is `blocked-by` each `UNIT` ([plan](plan.md)) whose code it first exposes to users, for a flagged unit the gate that turns its flag on; later gates reach it through gate order. This is so a review request's brief can name the gates it opens.

(basis: AWS Well-Architected OPS06-BP01, a tested rollback and stated fix-forward conditions; Google SRE ch. 27, named owners per step; the go/no-go card per gate, maintainer, 2026-11-11)

Live field: `readings`, list of number, `telemetry: each go-when criterion's metric over its observation window`, in go-when order.

**Metric `MET`.** One measure, with one definition, that a gate, an objective or the close-out reads.

- `role`: enum `goal`, `guardrail`, `diagnostic`, `data-quality`, `indicator`. A guardrail `serves` the goal it guards, and a diagnostic the metric it explains. An indicator is the one an objective ([slo-document](slo-document.md)) `rests-on`. (basis: Microsoft ExP metric types)
- `definition`: text. For a ratio, numerator over denominator; for a percentile, which percentile of what population.
- `source`: text. A link to where it is read.
- `baseline`: number, and `baseline window`: text, the dates it was taken over.
- `target`: number, and `direction`: enum `up`, `down`, `hold`.
- `tolerance`: number. For a `hold` metric, how far it may move either way and still hold.
- `cadence`: text. How often it is read.
- `owner after close`: text. The one person who keeps reading it once the task closes. (basis: IPA, benefits monitored after the project closes)

Live field: `value`, number, `telemetry: the metric over its latest cadence window`.

Both kinds take Agreement `needed` and change regime `baseline`. A gate's decide-by is its `opens on`, or `build start` while it has none, and a gate filed already run takes its run verification's date, a due point already passed, since the step ran before it was agreed; a metric's is the plan's due point.

Shows `RISK` (home: [raid-log](raid-log.md)).

## Sections

1. **What happens, in what order?** Always. The gate timeline.
2. **What decides each gate?** Always. The gate cards.
3. **What do we measure?** Always. The metric table.
4. **What could go wrong at each gate?** When a `RISK` is `opened-by` a `GATE`. The risk matrix.

## Checks

*Computed:*
- Every gate has `users see it`; every gate not filed already run has its driver, decider, opens-on date, bake, rollback, fix-forward conditions and at least one go-when criterion.
- Each criterion names a `MET` id, a threshold, an observation window and what it is relative to. (basis: prototype sweep, 2026-11-11, thresholds existed in the metrics but no gate linked them)
- A gate whose `users see it` is `yes`, with a run verification or the earliest such gate without one, has its rollback tested on and in, and a one-way gate with no run verification has a tested restore, whether users see it or not. A gate filed already run owes neither, since a rehearsal can't now come before it. (basis: AWS OPS06-BP01; benchmark, 2026-11-13)
- When any gate is `expand`, a `contract` gate exists with an opens-on date, and every `migrate` gate opens after an `expand` gate. (basis: Sato, an unexecuted contract phase can leave things worse than before)
- Every metric has its definition, source, baseline and its window, target, direction and cadence; every goal and guardrail has an owner after close.
- Every `hold` metric has a tolerance.
- Every goal metric has a guardrail serving it, and, when any goal metric exists, at least one metric is `data-quality`. An `indicator` needs no guardrail. (basis: Microsoft ExP; Grove's counter-indicator)

*Judgment:*
- A step that is a one-way door but isn't marked one, often a protocol, serialisation or timeout change. (basis: AWS Builders' Library)
- Old and new versions running side by side with nothing saying how each copes with the other, such as clients holding old credentials across a switch.
- A rollback said to restore the old state while an outside service keeps what the step issued, such as tokens valid until they expire. (basis: benchmark, 2026-11-12)
- An abort condition vague enough that rolling back would be argued mid-incident. (basis: AWS OPS06-BP01's anti-pattern)
- A threshold that can't be crossed within its window, or a guardrail that misses the change's real counter-effect.
- A latency metric taken as a mean. (basis: Google SRE ch. 4)

## Views

- **Gate timeline:** `timeline` of every `GATE` by opens on, showing phase, exposure, one-way, driver and decides.
- **Gate cards:** `cards` of every `GATE`, sorted by opens on: go when with its readings, abort when, bake, rollback, rollback tested on and in, fix forward when.
- **Metric table:** `table` of every `MET` grouped by role: definition, source, baseline and window, target, direction, tolerance, cadence, owner after close, value, and the gates it `supports` (only `GATE`).
- **Risk matrix:** `matrix` with rows `GATE` and columns `RISK`, each cell the risks the gate `opens`, empty marker `none`.

## Minimum form

Each section keeps its heading with one line: no gate or metric is set yet, and who sets them.
