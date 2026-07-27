# verify — usage

Establish that a change actually works by driving the real running application: frame the flows that would settle the claim, stand a real instance up and record the environment, exercise each flow end-to-end through the entry point a user reaches, separate a genuine behavioral defect from environment noise, and return a per-flow verdict with reproductions.

## When to use
- The suite is green and you want to know *the thing works*. A passing suite says the code satisfies the checks someone wrote for it; it does not say a user can complete the flow. When those two questions have come apart, this is the one that settles the second.
- A change is wired and you want to confirm it is actually **reachable** — that the entry point exists, resolves, and lands in the new behavior, rather than a feature sitting complete behind nothing that points at it.
- You are about to land something whose failure would be *invisible* to the suite: rendering, navigation, a flow that crosses several units and a boundary, anything the automated checks structurally cannot see because no case was ever written at that altitude.
- A spec's requirements need checking against running behavior rather than against the diff — each requirement driven and reported on individually (`--from-spec`).
- You need to know what *using* it is actually like (`--ux`), or what a user of assistive technology encounters when they try (`--as-user`).

## Not for / use instead
- **Authoring or running the automated suite** → **test**. The boundary is reciprocal and load-bearing: test designs and runs the checks and never drives the application; verify drives the application and never authors a case.
- **Root-causing a failure whose cause is unknown** → **debug**. verify localizes only far enough to tell a defect in the change from noise in the setup around it, then hands off with a reproduction; chasing the cause down through the code is debug's work.
- **Reading the change without running it** → **review**. review reads statically and executes nothing. verify's evidence is *always* an observation of a running system — a conclusion drawn from how the code looks is not a verify result at all.
- **A throwaway probe answering an open question** → **prototype**. prototype builds something new to learn from and discards it; verify exercises the real built thing, as wired, and changes nothing.
- **A live production incident** → **operate**, which owns the running production system. verify is a pre-landing check against an instance you stood up.
- **Fixing what verify found** → **develop**. The verdict and its reproductions are the deliverable; the change that clears them is a separate run of a different skill.
- **Getting the verdict in front of people** → **communicate**. That is deliberately not a flag here; verify returns the verdict to its caller.

## Examples
`--flows=checkout,password-reset` — *replaces* the set framed from the change with exactly these, so anything else stays unobserved and is reported as such. Flow names are the project's own vocabulary, not a fixed menu: whatever this codebase calls a flow is a valid name.
`--from-spec=specs/checkout.md` — derive the flows from the spec's requirements and key the report per requirement instead of per flow, which is what makes a requirement that *no flow could reach* surface as unobserved rather than quietly go missing from the report.
`--ux` — add an experiential pass over the same flows: every point of hesitation, dead end, and unexplained state gets recorded, on top of whether the flow functioned. It adds findings; it does not change what counts as functioning.
`--as-user=<persona>[,<persona>...]` — drive and report the flows as each named user, including a user of assistive technology; two names are two drives with two records, never averaged. Findings come back scoped to a persona, which is the point: what that user hits is a fact about that user's path, not a claim about everyone's.
`--sandbox` — stand the instance up in a disposable, isolated environment so a driven flow cannot write to real state. Reach for it whenever the flows mutate data or send anything outward; the sandbox then *is* the environment the verdict is scoped to.
`verify` (bare) — the default and the common case: flows derived from the change in hand, one functional pass through the real entry points, a verdict per flow.
`--flows=checkout --sandbox` — one flow, against throwaway state; the usual shape when the flow you need to drive is the one that charges, sends, or deletes something.
`--from-spec=specs/checkout.md --ux` — check the spec's requirements *and* record what satisfying each one is actually like to do, since a requirement can be fully met and still be painful to complete.

## Gotchas
- **A `works` verdict is scoped, never global.** It means: the flows that were driven, in the environment the run recorded, behaved as claimed — never "the application works." Read it, and pass it on, with the flows and the environment attached.
- **verify does not fix.** The deliverable is the verdict plus a reproduction per defect; closing one is develop's run (or debug's first).
- **An unobserved step is unobserved, not passing.** A step not reached, skipped past, or read off a log instead of watched is a gap, and a flow containing one cannot come back `works` however healthy the rest looked.
- **A confusing-but-functioning flow is `works` plus a usability finding, not a defect.** The level tracks completion; friction rides alongside it as findings (hunted deliberately under `--ux` / `--as-user`).
- **verify needs no configuration.** There is no backend and nothing to set up before a run; routing the verdict onward is communicate's part, and that is where a prerequisite lives.
- **Driving through a test harness, or calling the handler directly, is writing a test — not verifying.** The distinction the whole skill turns on. If the real entry point cannot be reached at all, that is a stated stop with the reason, not a pass earned through the harness.
