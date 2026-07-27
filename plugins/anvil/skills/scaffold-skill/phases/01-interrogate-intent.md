A skeleton is cheap to write and expensive to unwrite: once a SKILL.md exists, codify fills it, agents get recruited to it, the audits start checking it, and the next maintainer treats it as a fixture. So the most valuable work in this whole skill happens before a single file is written — pinning down what the skill is *for* and at what altitude. Get the intent wrong here and you've scaffolded a duplicate, a skill that should have been a flag, or a capability phrased as a tool that the leak audit will bounce. Get it right and the rest is mechanical.

## Require the target — never guess one

This skill mutates a specific plugin's `skills/` tree, so it needs `--plugin` (which plugin) and `--name` (what to call the skill). If either is missing, stop and ask. Do not infer the target from the current directory, the last plugin you touched, or the only plugin that happens to exist — a wrong guess writes a skeleton into the wrong tree, and the cost of asking is one question. The name you're given becomes both the directory (`skills/<name>/`) and the `name` field in frontmatter, so confirm it reads as a capability verb-phrase (see phase 2) before you commit to it.

## Name the single capability in one breath

State what the skill owns in one verb-phrase: *"open a change request"*, *"audit the packaging boundary"*, *"source a skill's method"*. The test is the conjunction test — if the honest description needs an "and" to be true (*"shape the frontmatter **and** fill the procedure"*), you almost certainly have two skills, and you should split them rather than scaffold one bloated shell. Not every "and" convicts, so apply the discriminator: an "and" joining *steps toward one deliverable* is a procedure — phases will carry it; an "and" joining *two outcomes a caller would ever want separately* is two skills. ("Interrogate, shape, seed, and hand off" is one skeleton; "scaffold the structure and fill the method" is two invocations a caller makes at different times.) A skill with one responsibility is one a cold executor can reason about, one the contract audit can check, and one the next maintainer can extend without fear.

## Locate it in the pool before you add to the pool

Recruit the plugin explorer to read the target plugin's existing `skills/` — their names, their descriptions, and their flags/modules. The question is not "is there a skill with this exact name" but "is this capability *already served*", because a capability can already live as:

- **an existing skill** — then there is nothing to scaffold; report the overlap and stop.
- **a flag-activated module on an existing skill** — e.g. a skill already runs the base procedure and a `--security` flag turns on an extra lens; if the "new skill" is really that lens, it's a module, not a skill.
- **an a-la-carte rule on an existing skill** — if it's reusable craft the existing procedure already cites, it's a rule, not a skill.

When the capability is a variant or behavior of something that exists, do not duplicate it — hand off to add-component to grow the existing skill with a module or rule instead. The variant-vs-peer test: if the candidate shares an existing skill's *deliverable* and differs only in lens, scope, or intensity, it's a component of that skill — a module when a caller opts in per-invocation, a rule when it's always-available craft; only a *different deliverable* earns a peer skill. Scaffolding a near-duplicate skill is the expensive mistake this phase exists to prevent: the contract audit can't tell you two skills overlap, only a human reading both can, so catch it now.

## Fix the altitude

Altitude is the size of the responsibility, and there's a band that's right:

- **Too broad** swallows its siblings — a skill that "manages releases" will absorb versioning, cataloguing, and notes that should be peers or phases, and it grows unbounded.
- **Too narrow** isn't a skill at all — a single decision toggled per-invocation is a flag and its module; a single reusable judgment is a rule. If the "skill" is one sentence of behavior, it belongs *inside* a skill, not beside one.

The right altitude is a coherent procedure with a handful of ordered steps and a clear done-state. If you can't imagine 3-6 phases, suspect it's too narrow; if you can imagine 15, suspect it's too broad. The 3-6 band is where every skill in this kit landed — but treat the counts as suspicion triggers, deliberately not hard bounds (capability size genuinely varies; the binding tests are the conjunction test above and the depth test in [choosing-slots](../rules/choosing-slots.md)). Where a count lands outside the band, don't resolve it by taste — recruit the **scaffolding-skeptic critic**, whose whole lens is "does this earn its place as a separate skill?", and hand it the capability statement plus the steps the interrogation surfaced. Naming the critic without recruiting it is how the one lens that argues for *less* gets skipped at the exact moment it is owed: an over-broad capability is cheapest to cut here, before any slot exists to defend.

## State it as a capability, not a tool

Phrase the responsibility by *what it accomplishes*, independent of any backend: *"publish the release notes"*, not *"write the notes to the configured artifacts backend's page"* — and certainly never a named product or CLI. This matters at intent time, not just at writing time, because the name and one-line responsibility you settle on here propagate into the frontmatter `description`, which the tool-leak audit reads. A capability named cleanly now is a description that passes the audit later. See [altitude-of-phrasing](../rules/altitude-of-phrasing.md) for the full discipline; here it's enough that the responsibility you write down names a *what*, never a *how-with-which-tool*.

## Enumerate the standard-points — where the skill will judge

With the capability pinned, sweep it for **standard-points**: every place the future skill will make or demand a judgment on which two competent cold executors could diverge — a bar for "good", a threshold, a grade, a selection, a default. Each one left unnamed here is a hole the content pass later fills from a generic executor's priors, which regress to average practice; named now, it becomes an explicit stub the skeleton carries and the content pass must close from an authority or the maintainer. Sweep three surfaces — the capability statement, the steps you can already imagine, and the flags the maintainer has mentioned — for four signatures:

- the skill **grades or ranks** anything → a scale is owed: its levels, the rubric that assigns them, and anchors for top and bottom.
- it **selects or filters** anything → a bar is owed: the threshold and where it comes from.
- it **declares done or good-enough** → an acceptance test is owed: what a pass concretely looks like.
- it **picks a default** the caller didn't choose (a default scope, window, or mode) → the default is owed a name and a basis.

The membership test: given identical inputs, could two competent executors defensibly return different judgments at this spot? Yes → standard-point. If the inputs mechanically determine the outcome, it isn't one. Record each as one line — *what is judged → what must be pinned (scale / threshold / acceptance test / default) → where the bar should come from (a named authority, the maintainer, or deliberately open with the reason)*. This list is a first-class output of the phase: phase 3 seeds it as explicit stubs, and the content pass inherits a list of bars to close instead of a blank.

## Output the responsibility before writing anything

Close the phase by emitting a one-line statement of the single responsibility plus where it sits in the pool relative to its siblings — *"`open-change-request`: turns a reviewed diff into a posted change request; sits beside `release` (which publishes) and downstream of the audits."* — followed by the standard-point list from the sweep above. This is the checkpoint the maintainer steers on: the responsibility tells them what is being built, the standard-point list tells them which judgments it will owe bars for. Under `--dry-run` this statement is part of the preview. Only once it's stated — and not contested — do you proceed to shape the frontmatter. If the interrogation surfaced that the capability is already covered, the correct output is that finding and a stop, not a skeleton.
