The most common way this skill produces a false result is a startup that reports success — no errors, a readiness message, a process that stays alive — while nothing a user could touch is actually being served; every flow driven after that is driven against an assumption.

## Stand the instance up by the project's own start path

Find how this project runs *itself* — the start command it declares, the initialization it documents, the configuration it expects — and use that, rather than a remembered answer from a project of the same shape; how an application starts is exactly the kind of fact that moves under you between runs. Never hand-roll a launcher or reach past the start path into an internal entry, because the wiring, configuration loading, and startup ordering that a hand-rolled launch skips are where the failures this skill exists to catch actually live.

**How much setup you may do.** Changing the project's code, or the change under observation, to get an instance up is **out of scope**: that is a finding, and the run stops with it. `(basis: derived from usage.md's "verify does not fix")` Short of that, the allowance runs to what the project itself **declares**: installing its declared dependencies, supplying the configuration values it declares, running the initialization it documents — all of it part of standing the app up, and all of it recorded in the environment record. Work you have to **invent** to get past a startup problem — a shim, a substitute component, a bypassed startup step — is on the far side of the line and is reported instead of performed; recording an invented substitution does not move it back across the line, and the degraded case below states the two narrow places a substitution *is* legitimate. `(basis: maintainer, 2026-07-27)`

**Know which code you are driving.** Confirm the instance serves the code under observation before anything else, by [the code-identity test](../rules/code-identity.md) — confirmed, or recorded **unknown**, never assumed.

## Reachable, not merely started — the acceptance test

**Do not proceed to driving until this test passes.** An instance counts as reachable only when you have **observed the application's own response come back through an access path a user would use** — a rendered surface, a served response, an interactive prompt that answers. That first observation is the acceptance test, and it must be obtained from outside the running process, at the same layer the flows will be driven through.

These do **not** satisfy it: the process is alive; its startup output announced readiness; the build or compile step succeeded; a status or readiness check answers while the application's own surfaces do not; an internal call you made in-process returned. `(basis: derived from SKILL.md's "a build that works and a page that never renders")`

For the same reason, reachability is **per surface**, not per instance: when the framed flows span more than one surface a user reaches, each of those surfaces passes the test on its own before its flows are driven. A single successful observation on one surface says nothing about the other, and one unreachable surface is a real result for the flows that need it — the flows on reachable surfaces still get driven, and the rest are reported unreachable.

## Establish each flow's real entry point

For every framed flow, identify the entry point a user actually travels through, and accept it only once it passes the tests defined in [reach-the-real-entry-point](../rules/reach-the-real-entry-point.md). An entry-point candidate you have not put through that rule's skipped-layer test is not yet an entry point; it is a guess, and the wrong guess here converts the whole run into an expensive test. The same rule holds the one legitimate exception and its price: a seam that genuinely cannot be driven becomes **recorded narrowed scope**, never a substitute drive through a harness or an internal handler. Record any such narrowing in the environment record below, where the verdict can inherit it.

## Record the environment the verdict is scoped to

The record is the scope statement the verdict is read against, so pin it before driving, while the facts are in front of you rather than reconstructed afterwards. It must contain:

- the **code identity** under observation — the revision or working-tree state, and whether uncommitted changes were present;
- **how it was started** — the project's own start path that was used, plus every declared setup step you performed;
- the **configuration in effect** — which profile or values the instance ran with, and which of those you supplied yourself;
- **what was real and what was not** — each dependency the instance talked to, marked real or substituted, and what stood in for each substitution;
- the **data state** it started from — seeded, empty, or a copy of real data, and whether it is isolated;
- the **access paths and client kinds** each flow will be driven through — the class of client and, where its version can change what the application does, that version;
- **what could not be provisioned** — anything skipped, stubbed, or unreachable, and what that removes from the run's reach;
- **when the observation was taken**, so a later re-run can tell drift from regression.

The record is complete when a competent reader could stand up an equivalent instance from it alone *and* could name what the verdict does not cover. `(basis: derived from usage.md's scoping gotcha)`

An item you genuinely cannot determine is recorded as **unknown**, with what you tried — not omitted, and not guessed. An unknown does not stop the run: the drive proceeds and the gap travels with the verdict as a stated scope limitation, since a partial observation with honest scope is worth more than none. `(basis: maintainer, 2026-07-27)` Whether a recorded unknown **caps the level** is decided in one place — [verdict-scale](../rules/verdict-scale.md)'s substitution-or-unknown degrade cell, which turns on whether a framed step's claimed effect depends on the undetermined fact. Note that dependence here, per unknown item, while the facts are in front of you, so the verdict phase can apply the cell without re-deriving it.

## Under `--sandbox`

Stand the instance up in a disposable, isolated environment so the drive cannot touch real state — see [isolated-sandbox](../modules/isolated-sandbox.md), which owns what isolation guarantees, what must stay real for the drive to still mean anything, and the degraded case where isolation cannot be provisioned. The sandbox then **is** the environment the verdict is scoped to, so its substitutions are recorded above like any other. Without the flag, the instance stands up in the ambient environment.

## Degraded and error cases

The app not coming up is a **result**, not an obstacle to work around. In each case below, capture the evidence, stop, and carry the stop to [report-the-verdict](05-report-the-verdict.md) — never a pass, never a silent retreat to driving an internal seam, and never a repair.

- **No runnable application exists** — the project is a library, or the change lives in a project with no start path at all. Stated stop: this method cannot observe it. Distinguish it from the framed-empty case, where an application does run and nothing user-reachable changed — here there is no reachable application to stand up at all, and the two want different follow-up.
- **The start path exists and fails.** The failure to start is itself an observation, and often the defect: capture what you invoked, what came back, and whether the same start path fails on the pre-change state too — that comparison is the cheap discriminator, and the classification it feeds belongs to [separate-defect-from-environment](04-separate-defect-from-environment.md), not here.
- **It starts but nothing is reachable** — the acceptance test above fails. Same handling: reported as the run's outcome, with what you observed at the access path.
- **It becomes reachable only intermittently.** Polling for readiness before the first acceptance pass isn't retrying — poll within the readiness window the project documents, else two minutes (routed to maintainer: two minutes as the default window, since a service that starts at all is usually ready well within it). Intermittent means reachability lost after the acceptance test passed, or a start that fails and then succeeds on a re-run. Do not retry until it happens to come up and then call it stood up; an unreliable startup is an observation about the application, recorded and handed on. A green attempt after failures does not erase the failures.
- **A declared dependency or credential is unavailable to you.** Default: **stop** with what is missing and why it was needed. Substituting a fake for it turns a verdict about the application into a verdict about your stand-in, and recording the stand-in does not repair that. Exactly two substitutions are legitimate, and both are *declared* rather than invented: **(i) one the project itself offers** — an alternative dependency profile, local stand-in, or offline mode the project documents as a supported way to run — and **(ii) one the caller has licensed**, which today means the stand-ins [isolated-sandbox](../modules/isolated-sandbox.md) admits under `--sandbox`. Either way it goes in the environment record, marked substituted with what stood in, and it narrows the scope — capped where [verdict-scale](../rules/verdict-scale.md)'s substitution-or-unknown cell applies, ambient runs included. Anything else missing is a stated stop, not a stand-in. `(basis: maintainer, 2026-07-27)`

## Output

A reachable instance with its code identity confirmed, one accepted real entry point per framed flow (with any narrowed scope recorded), and the complete environment record — handed to [exercise-the-flows](03-exercise-the-flows.md). If any of the three is missing, the output is the stated stop instead.
