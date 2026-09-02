The ranked list is the audit's substance; this phase gets it to where the owner will act on it, in a shape they can read the same way every run. Two reviewers who reach the same findings must also produce reports of the same character — so the output shape is pinned here, not reinvented per run. The default sink is a human report, and a report is *always* produced as the record even when another sink also fires.

## The default sink: a structured report

Render the findings in a fixed shape, so two runs are comparable and the owner knows where to look:

- **A scope line** — what was audited: the surface (`--changed` window or the whole subject), the breadth (default subset or `--exhaustive`), the threat-modeling framework and adversary scope, and anything deliberately excluded. This makes the audit's coverage — and its silence — legible.
- **A verdict line** — the outcome at a glance: a count by severity (e.g. "1 critical, 2 high, 1 low") leading with the highest present, or plainly **"no reachable abuse found under the threat lens"** when the ranked list is empty. Silence is a real verdict.
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

Order the findings so the owner acts in priority order: **severity descending, confidence as the tie-break, blast radius (how much the abuse reaches) as the final tie-break.** Do not vary the record's fields run to run. `(basis: the field set is the minimum an owner needs to act on a security finding — the grade, the certainty, the location, the attacker path (the proof), the impact, and the fix; it mirrors the adversary/path/abuse shape the security-auditor critic returns and the attacker-path+impact+remediation structure of a conventional pentest finding. Pinning it is what makes two cold reviewers format identically.)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../communicate/rules/deliver-at-the-readers-register.md) before delivering it: take from that rule the obligations this phase has not already settled for itself, and apply its honesty floor to the result. A run with no register to write to falls back on the only vocabulary it has loaded — this procedure's own — which is how a report comes out accurate and unreadable. Read the floor from the rule item by item rather than from memory — the passages it protects are exactly the ones that read as padding to anyone not checking whether the claim is true — and let its carve-out for named levels and verdict values hold the graded rungs and status names this skill defines and reports on.

## The alternate and additional sinks

The sinks are independent and composable; the report above is always the record, and a flag adds delivery on top of it:

- **`--sarif=<path>`** writes the findings as a machine-readable document at the path, in addition to the report — see [sarif-output](../modules/sarif-output.md). A local file write, no backend.
- **`--gate`** reduces the run to a pass/fail verdict with an exit status — see [gate-decision](../modules/gate-decision.md). A local exit, no backend.

They compose without redefining anything: `--sarif` with `--gate` writes the document *and* sets the verdict, both reading the same floored, ranked list this phase produced; neither re-grades. State every sink that fired in the returned record — the report, and for `--sarif`/`--gate` the path written and the verdict set — so the run's outcome is auditable.

## The terminal outcome, when `--gate` is set

`--gate` resolves the run to one of **three** outcomes, not two — proven exhaustive and mutually exclusive so no run falls between them:

- **pass** — the audit completed and no finding meets the gate floor.
- **fail** — the audit completed and at least one finding meets or exceeds the gate floor.
- **inconclusive** — the audit could **not** complete the surface it was asked to: the `--changed` diff could not be scoped because the vcs capability was unavailable ([scoping-the-surface](01-scoping-the-surface.md)), or the surface was otherwise unresolvable. An inconclusive run must **not** be reported as pass — a gate that silently passes an audit it never ran is worse than no gate. Signal it distinctly (a non-pass, non-fail status) so the pipeline treats "we didn't check" differently from "we checked and it's clean."

The gate floor and its default are pinned in [gate-decision](../modules/gate-decision.md). Whichever outcome, the human report is still produced as the record.
