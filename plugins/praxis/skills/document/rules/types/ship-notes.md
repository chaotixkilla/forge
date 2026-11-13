# Ship notes

What a shipping run did to a change: where it landed and how it rolled out.

**Reader and question.** On-call and maintainer: "when did this reach production, and was it healthy?"

**Page.** `own page`

## Membership

The shipping act's result. (basis: maintainer, 2026-09-30) A change shipped as several review requests has one page per request, since each lands as its own step, and a roll-out's result goes on the page of each request it covered. (basis: derived from one page per subject)

## Items

**Shipment `SHIP`.** One per page: the request's landing and the roll-outs that covered it.
- Fields: `merged into` text, the line; `commit` text, the commit it merged as; `environment` text; `exposure` text, the furthest exposure reached; `strategy` text; `health` enum `holds`, `fails`, `unsettled`, `not checked` ([results-and-certainty](../../../../craft/evidence/results-and-certainty.md)), the verdict at the furthest exposure reached; `reason` text, why `health` is `not checked`, when it is.
- Change regime: `baseline`.
- Agreement: `none`.

## Sections

(basis: maintainer, 2026-10-02, for the order)

1. **Where did it land, and is it healthy?** Always. The exposure reached in which environment and the health verdict, or why it didn't land or roll out.
2. **What merged?** Always. The line, the commit, and the gate's run with its result.
3. **How did it roll out?** When a roll-out ran. The strategy, each step's exposure, and the signals behind the verdict, with the metric charts around each step where telemetry gave them.

## Checks

- *Computed:*
  - `health` at `not checked` has `reason` filled;
  - the gate's run is evidence with its date and outcome.
- *Judgment:*
  - a verdict of `holds` read from fewer signals than the dashboards or alerts the task named;
  - health unread reported as a healthy ship;
  - a `fails` verdict with no word on what it calls for.

## Minimum form

"Not merged" with why, the line and gate "not run", and no roll-out section.
