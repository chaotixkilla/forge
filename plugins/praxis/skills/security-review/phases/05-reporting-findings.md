Get the ranked list to where the owner will act on it, in a shape they can read the same way every run.

## The default sink: a structured report

Render the findings in a fixed shape, so two runs are comparable and the owner knows where to look:

- **A posture line**, first — what the top-ranked finding lets the modeled adversary do to the audited surface as it stands, in one sentence the owners can act on, with its severity and location: *an unauthenticated caller can read any tenant's invoices through the export endpoint (critical, `api/export.py:42`)*. When the list is empty, the verdict line's empty statement is printed once, as the posture, and the verdict line isn't repeated. (basis: maintainer, 2026-10-02)
- **A verdict line** — the outcome at a glance: a count by severity (e.g. "1 critical, 2 high, 1 low") leading with the highest present. When the list is empty, the line says which empty it is: plainly **"no reachable abuse found for <the adversary modeled>"** only when nothing cleared the floor; when `--severity-min` withheld every graded finding, **"none at or above <level>; <n> withheld below it, highest <severity>"** — never the clean line.
- **A scope line** — what was audited: the surface (the changed code and what newly reaches it, or the whole subject), the breadth (the high-likelihood entry points and threat classes, or every one under `--exhaustive`), the threat-modeling framework and adversary scope, and anything deliberately excluded. This makes the audit's coverage — and its silence — legible.
- **The findings, ranked**, each as a fixed record — location and path and remediation are mandatory ([confirm-reachability-before-flagging](../rules/confirm-reachability-before-flagging.md), [exploit-then-impact](../rules/exploit-then-impact.md)):

  ```
  [severity · certainty] file:line — <title>
    Adversary: <who they are and what they control>
    Path:      <source → hop → sink; the boundary crossed; the missing/broken guard>
    Impact:    <what the attacker gains — the concrete C/I/A abuse>
    Fix:       <the smallest change that breaks the attack path>
  ```

- **A hardening section**, separate and **unscored** — the defense-in-depth observations pulled out in [assessing-severity](04-assessing-severity.md) ([separate-finding-from-noise](../rules/separate-finding-from-noise.md)), never ranked or graded alongside the findings.
- **A coverage section**, only when `--standard` is set — see [standard-mapping](../modules/standard-mapping.md).

Order the findings so the owner acts in priority order: **severity descending, certainty as the tie-break, blast radius (how much the abuse reaches) as the final tie-break.** Do not vary the record's fields run to run. `(basis: derived from the security-auditor critic's return shape and a conventional pentest finding)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

**And a visual where prose would carry it worse:** the trust boundaries the change crosses and the reachable paths from its entry points to the assets worth protecting are relations; show it rather than describe it, per `output.diagrams` ([report-style-settings](../../../craft/writing/report-style-settings.md)) and [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md), which decides whether one is owed, drawn from the surface map. `(basis: maintainer, 2026-10-07)`

## The alternate and additional sinks

The sinks are independent and composable; the report above is always the record, and a flag adds delivery on top of it:

- **`--sarif=<path>`** writes the findings as a machine-readable document at the path, in addition to the report — see [sarif-output](../modules/sarif-output.md). A local file write, no backend.
- **`--gate`** reduces the run to a returned gate result — holds, fails, or not checked — see [gate-decision](../modules/gate-decision.md). A local return, no backend.

They compose without redefining anything: `--sarif` with `--gate` writes the document *and* sets the gate result, both reading the same floored, ranked list this phase produced; neither re-grades. State every sink that fired in the returned record — the report, and for `--sarif`/`--gate` the path written and the gate result set — so the run's outcome is auditable.

## When `--gate` is set

The run resolves to holds, fails or not checked by [gate-decision](../modules/gate-decision.md); whichever outcome, the human report is still produced as the record.
