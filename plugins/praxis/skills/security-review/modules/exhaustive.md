# exhaustive (`--exhaustive`)

Activated by `--exhaustive`, referenced from [scoping-the-surface](../phases/01-scoping-the-surface.md), [modeling-the-threats](../phases/02-modeling-the-threats.md) and [hunting-vulnerabilities](../phases/03-hunting-vulnerabilities.md).

The base audit maps the high-likelihood subset of the surface and works the threat classes its boundaries most expose. This module trades speed for completeness. Deletion test: remove it and the audit still runs, on the subset.

## The delta

- **Ask the cost question first**, in the run's opening message, in [ask-before-a-heavyweight-run](../../gather/rules/ask-before-a-heavyweight-run.md)'s own words. A run that can't ask stops cleanly before any work, as that rule says; under `--gate` that run's result is **not checked**, with that reason ([gate-decision](gate-decision.md)).
- **No small-change shortcut.** A `--changed` diff is mapped by recruiting however small it measures, since the inline path exists to save cost the caller has chosen to spend.
- **Every entry point, every threat class.** Enumerate all entry points in scoping, carry every class the framework flags against every element in modeling — recruiting the **completeness-auditor** to name the class or boundary that went unmodeled — and every attack class against every entry point in the hunt, including the low-likelihood combinations the subset skips.
- **A red-team pass.** In the hunt, add the **adversary** critic for a general red-team pass over the same surface, beside the security-auditor. Without fan-out, apply both lenses yourself.

The scope line in the report names the breadth as exhaustive.
