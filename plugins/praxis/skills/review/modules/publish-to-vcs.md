# publish-to-vcs (`--comment`, modified by `--inline`)

Activated by `--comment`, referenced from [deliver-findings](../phases/06-deliver-findings.md).

The base review returns its findings locally, as the structured report. This module adds a *delivery destination*: publish those same findings back onto the change through the vcs capability, where the author and other reviewers already are. Deletion test: remove it and review still delivers the local report; the vcs publication is an additive sink, not the base behavior.

## The delta

- **Publish the delivered findings** — the same floored, ranked list the report contains — back onto the change through the vcs capability. The dispatch resolves to the configured provider; this module names the capability and never the backend.
- **`--inline` modifies the attachment.** With `--inline`, anchor each finding to its exact `file:line` as a line-level annotation on the change; without it, post one summary comment carrying the ranked list. `--inline` does nothing on its own — it is a modifier of this module, not a sink of its own, so it requires `--comment`.
- **Carry a review *stance* with the post.** A posted review must declare a stance — many hosts *require* one (a review is submitted as comment-only, an approval, or a request-for-changes; there is no verdict-less submission). The stance is a capability-level decision review makes, not a backend detail:
  - **`--comment` alone → comment-only.** Post the findings as review comments with **no approval verdict**. praxis reviewing on your behalf must not silently *approve* or *block* a human author's pull request; comment-only delivers the findings and leaves the merge decision to the people on the PR. This is the default and the safe choice.
  - **`--comment` with `--gate` → the gate verdict sets the stance.** `--gate` is an explicit request for a pass/fail decision, so the stance follows it: a **pass** posts as an *approval*, a **fail** as a *request-for-changes*, thresholded against the same gate floor ([gate-mode](gate-mode.md)). Without `--gate`, never escalate past comment-only on your own.

  review names the stance; the adapter maps it to the host's concrete review event and **never invents one**, and the post always goes through the vcs capability's post operation — never a raw API call that bypasses it. (basis: hosts mandate a review event — approve / request-changes / comment — on every submission, so the stance must be *decided*, not invented; comment-only by default keeps praxis from casting a human's approval, and tying escalation to `--gate` is the one place the caller has explicitly asked for a verdict.)
- **Composition** is defined in [deliver-findings](../phases/06-deliver-findings.md): with `--gate`, post *and* set status (and the stance follows the gate verdict, above); with `--fix`, comment on what was not auto-fixed. Publishing never changes the verdict — it delivers the same list the report shows.

## Prerequisite and degrade

Publishing goes through the vcs capability (served by the `vcs` skill). If it reports the backend unavailable — `tools.vcs` unconfigured — **degrade**: fall back to the local report and state clearly that the findings were not posted (the `vcs` skill owns guiding the user through `init:vcs`). Unlike `--pr` (which has nothing to review without the fetch), `--comment` has an honest reduced path: the findings still exist and are still delivered, just locally. The caller gets the review either way; only the destination narrows.
