# Runbook

What the on-call engineer does when an alert fires: what each alert means, what to check first, what to do, who is next, and the procedures they run by hand.

## Reader and question

The on-call engineer, at the moment of the page: "This alert fired: what does it mean, and what do I do?"

## Page

`own page`

## Membership

The alerts of the services the work runs or changes, one playbook entry each, and the procedures those entries point to. The objectives the alerts protect are the [slo-document](slo-document.md)'s. Its subject is the service, so a task has one per service. It is filed again when an alert or a procedure changes; whoever is paged and finds an entry wrong files the correction. (basis: SRE Workbook, on-call)

**Operational.**

## Items

**Alert `ALR`.** One alert condition and its playbook entry.

- `service`: text.
- `severity`: enum `page`, `ticket`.
- `signal`: enum `symptom`, `cause`. (basis: Google SRE ch. 6, page on symptoms)
- `condition`: text. What fires it.
- `long window` and `short window`: period, and `burn rate`: number. For an alert that serves an `SLO`. One alert holds one window pair, so the Workbook's page pairs and ticket pairs are separate alerts. (basis: SRE Workbook, multiwindow multi-burn-rate alerts)
- `defined in`: text. A link to where the alert is defined: pinned to a commit when it is in code, else the alerting tool's link or the condition's id; missing while it is only planned.
- `routes to`: text. The rotation or person it reaches.
- `means`, `impact`, `first check`: text.
- `likely causes`: list of text.
- `do`: text, and `procedures`: list of id, the `PROC` items it runs.
- `escalate`: text. Who is next, how to reach them, and after how long.

An alert on an objective `serves` that `SLO`. (basis: alert cards, prototype sweep, 2026-11-11)

**Procedure `PROC`.** One sequence of steps someone runs by hand. Its body is the steps, each command copyable.

- `service`: text.
- `when`: text. When to run it.
- `verify`: text. How to tell it worked.
- `undo`: text. How to undo it, or that it can't be.
- `automate`: enum `yes`, `no`. Whether it is a fixed sequence that should become automation, with why in its body. (basis: SRE Workbook, a fixed sequence is automated, not documented)

Both kinds take Agreement `needed` and change regime `baseline`. Each one's decide-by is the plan's due point.

Shows `SLO` (home: [slo-document](slo-document.md)).

## Sections

1. **This alert fired: what do I do?** Always. The alert cards.
2. **Which alerts can fire?** Always. The alert table.
3. **How do I run each procedure?** When a `PROC` exists. The procedure cards.
4. **Who answers, and who is next?** Always. Prose: the rotation, the escalation chain, and where each shift writes its handoff. (basis: SRE Workbook, on-call handoff)

## Checks

*Computed:*
- Every alert has its service, severity, signal, condition, routes to, means, impact, first check, do and escalate.
- A cause alert is `ticket`, unless it serves an objective. (basis: Google SRE ch. 6; SRE Workbook)
- An alert serving an objective has a long and a short window and a burn rate, the short window a twelfth of the long.
- Every objective whose service is the page subject has a `page` alert of that service serving it, and, when any `page` alert of that service exists, at least one is a symptom. (basis: prototype sweep, 2026-11-11, the symptom alert never built)
- Every procedure has its service, when, verify, undo and automate.

*Judgment:*
- A page nobody can act on. (basis: Google SRE ch. 6, every page actionable)
- A first check or procedure naming something production no longer has.
- A procedure marked `no` for automation that is a fixed sequence.
- An alert nothing uses, or one that routes to a rotation nobody staffs.

## Views

- **Alert cards:** `cards` of `ALR` whose service is `page subject`, sorted by severity, `page` first: means, impact, first check, likely causes, do, procedures, escalate.
- **Alert table:** `table` of `ALR` whose service is `page subject`: severity, signal, the `SLO` it `serves`, routes to, defined in with the empty marker `planned`.
- **Procedure cards:** `cards` of `PROC` whose service is `page subject`: when, its body (the steps), verify, undo, automate.

## Minimum form

Each section keeps its heading with one line: no alert or procedure is written yet, and who writes them.
