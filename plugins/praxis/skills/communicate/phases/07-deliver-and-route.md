A finished artifact that never reaches its readers did nothing, and one that reaches them through the wrong path — a durable decision posted as an ephemeral message, an announcement with no link back to the record — reaches them badly. This phase routes the clean export to the targets [choose-form-and-channel](03-choose-form-and-channel.md) resolved, delegating the actual posting and publishing to the ports while keeping the decision of *what goes where* here. The artifact is always produced and returned; the flags add or redirect delivery on top of that.

## The default sink: return the artifact

With no delivery flag, produce the finished artifact and **return it** — to the user, as the record, in the form chosen. This is ambient: it needs no configured backend. Returning is a real terminal outcome, not a failure to deliver — many artifacts (a decision record for the repo, a handoff message the user will place themselves) are correctly *handed back* rather than pushed. State where it is meant to go, so the user can route it if no flag did.

## `--notify` — announce it through the communication port

Under `--notify[=<target>]`, post the artifact (or a fit-for-channel summary of it, with a link back to the full content) to the communication target — see [notify-targets](../modules/notify-targets.md). The post goes through the [communication](../../communication/SKILL.md) port: communicate decides *what* to say, *to whom*, and *whether* to send; the port carries out the post and returns the delivered message's reference. The target is always supplied by the flag — there is no default channel — so a `--notify` with no resolvable target is reported as that, not sent somewhere arbitrary.

## `--publish` — publish it durably through the publish-artifact port

Under `--publish`, publish the artifact as a durable, team-facing document and return its canonical location — see [publish-output](../modules/publish-output.md). The publish goes through the [publish-artifact](../../publish-artifact/SKILL.md) port, which owns the carve into a page tree and the backend; communicate hands over the **clean export** verified in [tighten-and-verify](06-tighten-and-verify.md) — the clean-export bar re-applies at the boundary, because publishing puts the artifact somewhere durable and public. The port publishes faithfully and adds no process metadata of its own.

## `--draft` — hold delivery

Under `--draft`, stop before any external routing and return the content marked as an unsent draft for review — see [draft-only](../modules/draft-only.md). `--draft` is the reader's "let me see it first," so it **wins over the delivery flags**: if `--notify` or `--publish` are also present, they are held, not fired, and the artifact is returned with a note that delivery was suppressed pending review. Nothing is posted or published under `--draft`.

## How the sinks compose

The interactions are defined, not left to chance:

- **`--publish` with `--notify`** — both fire, in order: publish the durable document first, then post the announcement with a link to the published location. Two ports, two jobs — publishing creates the record, notifying tells people it exists. Never post the announcement before the publish resolves, or the link dangles. **If the publish *degrades*** (artifacts backend unavailable) rather than resolving, there is no location to link — so the two channels land in *different* dispositions: the **publish channel is degraded-return** (its own backend was unavailable), and the **notify channel is held** (the home-less branch — nothing to link to, though communication itself is fine) per [notify-targets](../modules/notify-targets.md). Return the clean export for the user to publish by hand *and* the composed announcement for them to post once it has a home; neither fires a dead-link announcement.
- **`--notify` alone on a durable artifact** — the artifact has no home unless it already lives somewhere, so the notify follows [notify-targets](../modules/notify-targets.md)'s home-less branch: hold the announcement for hand-posting after the artifact is placed, or advise pairing `--publish`. A short artifact that *is* the message posts directly.
- **`--draft` with anything** — `--draft` suppresses all delivery; the other flags are recorded as intended-but-held.
- Whatever fires, **return the record of what was delivered** — the artifact itself, plus for `--notify`/`--publish` the reference or canonical location the port returned — so the run's outcome is auditable and the user knows exactly what landed where.

## Degrade — the backend is the port's, the fallback is communicate's

Each port owns its prerequisite and **blocks** when its backend is unconfigured; communicate catches that capability-level signal and **degrades on its own side** rather than stalling:

- **communication unavailable** (under `--notify`): return the composed message and its target for the user to send by hand, noting automated delivery was unavailable. The artifact is still produced.
- **artifacts unavailable** (under `--publish`): return the clean export for the user to publish by hand, noting automated publishing was unavailable. The artifact is still produced.

A port that reports a delivered reference guarantees it even if a follow-on step (fetching a permalink) failed — so a delivered post's reference is complete; **never re-post or re-publish to recover missing metadata**, or the reader gets the artifact twice.

Done-state — the artifact is **always produced and returned**, and each requested delivery channel lands in exactly one disposition (the set is exhaustive and mutually exclusive):

- **sent** — posted or published, with the port's reference or canonical location.
- **held** — composed but deliberately not sent because a precondition isn't met (a durable artifact with no home under `--notify`): returned for the user to send by hand once the precondition is satisfied, with what's missing named.
- **degraded-return** — the channel's backend was unavailable: the finished content is returned for the user to send or publish by hand, noting automated delivery was unavailable.
- **suppressed** — `--draft` held this channel by request; recorded as intended-but-not-sent.

**Precedence when two blockers apply to one channel:** *suppressed* (`--draft`) outranks everything — a held-back run reaches no port at all. Otherwise **held outranks degraded-return**: a `--notify` on a durable artifact with no home is *held* even when the communication backend is also unavailable, because the missing home is the binding blocker — there is nothing postable until the artifact is placed, by hand or automated — so record it as held and note the backend outage alongside. A channel whose *only* blocker is its own backend is degraded-return. This ordering (suppressed → held → degraded-return → sent) makes the four mutually exclusive when more than one trigger matches.

A channel that failed or couldn't fire is reported as *held*, *degraded-return*, or *suppressed* — never as a silent success and never left undefined. The partition has no gap between "sent" and "not sent": every (flag × backend-availability) combination lands each channel in exactly one of these four, and the artifact is returned regardless.

That channel record is what the *caller* reads when the run ends, which makes it a terminal report like any other skill's: lead with what was delivered and where, state plainly what was held, degraded, or suppressed and what that now needs from them, and keep the port, flag, and precedence machinery out of it — the caller needs the disposition, not the mechanism that reached it ([deliver-at-the-readers-register](../rules/deliver-at-the-readers-register.md)).
