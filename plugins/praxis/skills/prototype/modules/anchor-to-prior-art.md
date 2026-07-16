# anchor-to-prior-art (`--prior-art=REF`)

Activated by `--prior-art=REF`, referenced from [build-the-spike](../phases/04-build-the-spike.md).

The base spike builds a probe from the framed question, seeding from whatever [scout-prior-art](../phases/02-scout-prior-art.md) turned up. This module makes the seed *explicit and mandatory*: start by reproducing a *named* reference (a repo, paper, or example) to a known-good baseline, then diverge from it toward the framed unknown. **Deletion test:** remove it and prototype still scouts prior art and builds fresh; the flag adds the reproduce-a-baseline-then-diverge strategy anchored to one specific reference.

## The delta

- **Reproduce the reference first** — build the named REF to a working, observed baseline before touching the question. This confirms you have a correct starting point, so a later failure is attributable to *your divergence*, not to a broken reproduction.
- **Then diverge toward the unknown** — change only what the framed question is about, holding the reproduced baseline fixed ([isolate-what-you-test](../rules/isolate-what-you-test.md)). The divergence *is* the experiment: the delta between "the reference as-is" and "the reference pushed toward our case" is exactly the framed unknown, cleanly isolated.

Starting from working code rather than a blank page is usually the cheapest probe ([pick-the-cheapest-probe](../phases/03-pick-the-cheapest-probe.md)'s "reuse over fresh" discriminator) — but the reproduction must actually run and be observed, or the baseline is an assumption, not a known-good ([ground-claims-in-a-run](../rules/ground-claims-in-a-run.md)). If the reference can't be reproduced, that itself is a finding: the divergence experiment can't be trusted until the baseline is.
