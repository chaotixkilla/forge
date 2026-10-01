Get the ranked list to where the owner will act on it, in a shape they can read the same way every run.

## The default sink: a structured report

Render the findings in a fixed shape, so two runs are comparable and the owner knows where to look:

- **A scope line** — what was audited: the surface (`--changed` window or the whole subject), the breadth (default subset or `--exhaustive`), the threat-modeling framework and adversary scope, and anything deliberately excluded. This makes the audit's coverage — and its silence — legible.
- **A verdict line** — the outcome at a glance: a count by severity (e.g. "1 critical, 2 high, 1 low") leading with the highest present, or plainly **"no reachable abuse found under the threat lens"** when the ranked list is empty.
- **The findings, ranked**, each as a fixed record — location and path and remediation are mandatory ([confirm-reachability-before-flagging](../rules/confirm-reachability-before-flagging.md), [exploit-then-impact](../rules/exploit-then-impact.md)):

  ```
  [severity · confidence] file:line — <title>
    Adversary: <who they are and what they control>
    Path:      <source → hop → sink; the boundary crossed; the missing/broken guard>
    Impact:    <what the attacker gains — the concrete C/I/A abuse>
    Fix:       <the smallest change that breaks the attack path>
  ```

- **A hardening section**, separate and **unscored** — the defense-in-depth observations pulled out in [assessing-severity](04-assessing-severity.md) ([separate-finding-from-noise](../rules/separate-finding-from-noise.md)), never ranked or graded alongside the findings.
- **A coverage section**, only when `--standard` is set — see [standard-mapping](../modules/standard-mapping.md).

Order the findings so the owner acts in priority order: **severity descending, confidence as the tie-break, blast radius (how much the abuse reaches) as the final tie-break.** Do not vary the record's fields run to run. `(basis: derived from the security-auditor critic's return shape and a conventional pentest finding)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

## The alternate and additional sinks

The sinks are independent and composable; the report above is always the record, and a flag adds delivery on top of it:

- **`--sarif=<path>`** writes the findings as a machine-readable document at the path, in addition to the report — see [sarif-output](../modules/sarif-output.md). A local file write, no backend.
- **`--gate`** reduces the run to a pass/fail verdict with an exit status — see [gate-decision](../modules/gate-decision.md). A local exit, no backend.

They compose without redefining anything: `--sarif` with `--gate` writes the document *and* sets the verdict, both reading the same floored, ranked list this phase produced; neither re-grades. State every sink that fired in the returned record — the report, and for `--sarif`/`--gate` the path written and the verdict set — so the run's outcome is auditable.

## The terminal outcome, when `--gate` is set

`--gate` resolves the run to one of **three** outcomes, not two — proven exhaustive and mutually exclusive so no run falls between them:

- **pass** — the audit completed and no finding meets the gate floor.
- **fail** — the audit completed and at least one finding meets or exceeds the gate floor.
- **inconclusive** — the audit could **not** complete the surface it was asked to: the subject could not be resolved, because it doesn't exist or can't be read. `--changed` with no derivable base isn't this case: it audits the whole subject instead ([scoping-the-surface](01-scoping-the-surface.md)). An inconclusive run must **not** be reported as pass — a gate that silently passes an audit it never ran is worse than no gate. Signal it distinctly (a non-pass, non-fail status) so the pipeline treats "we didn't check" differently from "we checked and it's clean."

The gate floor and its default are pinned in [gate-decision](../modules/gate-decision.md). Whichever outcome, the human report is still produced as the record.
