# Trust observations over assumptions

The bug is, by definition, in the place where the system does something other than what you believe it does — so the belief is exactly what you cannot trust. Yet the fastest-feeling move in debugging is to reason from the code's names, comments, types, and your mental model of "what this obviously does," and that reasoning walks straight past the bug every time, because the bug lives in the gap between that model and reality. This rule is the discipline of looking instead of assuming.

## Look at what runs, not at what it's called

A function named `validate` may reject nothing; a comment may describe the code two refactors ago; a type may be widened by a cast three lines up; a config you "know" is set may be overridden downstream. Names and comments are the author's *intent*; the failure is where intent and behavior diverge. So when a step of your reasoning depends on what some state or code actually does, **observe it** — read the real value, trace the real path, run the real branch — rather than inferring it from what it is named or what it "should" be.

## The discriminator: observed vs. inferred

At each link in your reasoning, label it: is this fact **observed** (you saw the value, ran the path, watched the branch taken) or **inferred** (you concluded it from a name, a type, a comment, or "it must be")? An inferred fact is a hypothesis, not evidence — it may be the bug. Verify each load-bearing inferred fact at least once before building on it; the one you were surest of is the one most likely to be false, precisely because you didn't check it. This is why a confirmed cause requires a demonstrated link, not a plausible one (per [the root-cause-confidence scale](root-cause-confidence.md)).

When the deciding state is not visible, don't downgrade to assuming — make it visible ([make-the-invisible-observable](make-the-invisible-observable.md)).

`(basis: Agans' Rule 3, "Quit Thinking and Look" — Debugging: The 9 Indispensable Rules (2002): get data by observing the failure rather than theorizing repairs from speculation. Reinforced by Zeller's scientific-debugging stance that hypotheses are tested against observation, never assumed true. The observed-vs-inferred label is that principle stated as a per-fact check.)`
