# Offer to coordinate

Work that splits into independent pieces can run in parallel: this session coordinates, and one worker session builds each piece. That multiplies the usage, so it is offered once, never assumed. (basis: maintainer, 2026-11-19, after the visual library's build, which ran as a coordinator and three workers)

## When it is offered

Once per round of an act that builds units, at the first point the round's units are known: at the proposal when they were decomposed already, else as soon as decompose returns them, before any of them is built. A round whose units don't split into two or more pieces isn't offered it.

The units split into **independent pieces** when they group so that:
- no unit in one piece is `blocked-by` a unit in another, nor serves a slice that is;
- no file is changed by two pieces, but for **shared files**: a file each piece only appends to, such as a stylesheet or a module others extend, or an ordered list each adds entries to, such as a registry ([coordinate](../modules/coordinate.md)).

Every unit is in exactly one piece, and the units split into as many pieces as the test allows; between splits of the same count, the one keeping each slice's units together wins. The files a unit changes are the ones its plan names, or decompose names when there is no plan. When it is unclear whether a file is shared, it isn't, so the two pieces join. In an epic, a round's units usually serve one slice, so the offer comes when its anchor spans several slices or its slice's units are independent.

## The ask

One question, put as [ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md) says, suggesting N, the number of pieces:

> This splits into N workstreams: run this session as coordinator with N worker sessions? It uses about N+1 sessions' usage.

Under it, one line per piece names its units. Above five pieces it adds that the coordinator's merging becomes the bottleneck beyond five workers, and offers a grouped split of five or fewer: pieces joined by slice, those serving one slice together, the two with the fewest units joined first, the earlier in unit order on a tie. The user picks N, the grouped number, any number between, or no; a number below N joins pieces the same way. Its default is **no**: the round runs as it would have. A run that can't ask takes no. (basis: maintainer, 2026-11-19 — no hard cap; merging load is the real limit)

A yes runs the round as [coordinate](../modules/coordinate.md) says, as `--coordinate` would. Under `--coordinate`, the offer isn't made and its split is made all the same, at N; units that don't split into two pieces run as a round of this session, which says so.

Cited by [run-the-act](../phases/03-run-the-act.md) and the [coordinate](../modules/coordinate.md) module.
