A gather is only as good as the question it starts from and the lanes it points at. A vague question fans out into noise; the wrong lane set either misses the answer or burns budget on lanes that can't hold it. Frame before you recruit.

## Frame the question
1. Restate the caller's ask as one precise, answerable gather question — what specifically must be true, and what evidence would settle it. A topic ("the auth system") is not a question; "what does the login path do on a failed token refresh, and why is it that way" is.
2. Checkpoint — gather-ready or route back: if no answerable question survives the restatement (the ask is too vague to point at a lane), stop and hand back `not gather-ready: <what's missing>` rather than fan out on a guess. A wrong question wastes the whole fan-out downstream, so this gate is worth the halt.

## Pick the lanes
3. Choose which source lanes the question touches. Default when `--explorers` is absent: consult every lane whose *source class* the question genuinely bears on, by this mapping — observable behavior / where things live → `code`; why-it's-that-way, history, prior attempts → `repository`; recorded human decisions, plans, runbooks → `knowledge-base`; a vendor/maintainer contract → `official-documentation`; a domain result, spec, or standard → `authoritative-literature`; lived friction, pitfalls, workarounds → `community-practices`. (basis: the lane definitions the explorer agents own.) A lane the question doesn't touch is not consulted — breadth is coverage of the question, not all six by reflex.
4. `--explorers=<list>` overrides the mapping: consult exactly the named lanes. `--inputs-only` forbids the open-web lanes regardless of the mapping — see [inputs-only](../modules/inputs-only.md).

## Set the breadth
5. Set the fan-out breadth and lead-chasing rounds. Default: recruit each chosen lane once, then chase leads to saturation — the stop test in [know-when-to-stop](../rules/know-when-to-stop.md); "done" is saturation, not a single recruitment pass. `--rounds=<n>` caps the lead-chasing rounds; `--deep` widens both the lane set and the rounds — see [deep-mode](../modules/deep-mode.md); `--budget=<n>` caps total recruit/fetch operations — see [budget-discipline](../modules/budget-discipline.md).

The output of this phase: the gather question, the chosen lane set, and the breadth/rounds/budget — the recruitment plan phase 02 executes.
