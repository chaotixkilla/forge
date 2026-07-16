The audit is only worth what the maintainer can do with it. This phase delivers the ranked findings in the form the caller asked for, and — when `--fix` is set — actually performs the repairs rather than only describing them. The two modes share the same finding list; they differ in whether the file ends changed or merely understood.

## Emit the findings

Return the ranked list per `--report`. Default is **inline**: prose back to the caller, worst leak first, each finding carrying its file:line anchor, the offending text, and the concrete suggestion ranking produced. Inline is the right default because the maintainer usually wants to act in the same session they audited in.

Emit every finding in one shape, so two runs of this audit read identically:

```
<tier> · <file>:<line> · "<offending span>" → "<replacement text>"                    (rephrase)
<tier> · <file>:<line> · "<offending span>" → name <capability>, detail → <adapter>   (relocate)
```

Prose around the lines is welcome where a finding needs context; the lines themselves are not optional.

With `--report=artifact`, render the same findings as a structured page via the configured artifacts backend (or a local file where that's the configured target). Reach for the artifact form when the list is long, when it needs to be shared or revisited, or when a side-by-side of leak-and-suggestion reads better than a scroll of prose. The *content* is identical to inline — same anchors, same suggestions, same order; only the surface changes. Don't let the artifact form tempt you into padding the findings to fill a page; a three-leak audit is a three-leak page.

Report honestly when the audit is clean: zero leaks is a result, not a non-answer. Say what was scoped so "clean" is legibly "clean across *this*," not silence that could mean "found nothing" or "looked nowhere" — one line carries it: `clean — <N> skill-layer files across <M> skills scanned, adapters excluded, 0 leaks.`

## With `--fix` — apply the repairs

`--fix` shifts the skill from reporting to repairing. Work the ranked list top-down and apply each finding's suggestion:

- **Rephrases** are mechanical: replace the offending span in the skill-layer file with the capability wording the suggestion specified. This is an edit to a phase, rule, module, `SKILL.md`, or agent file.
- **Relocations** are two-sided: rewrite the skill-layer line to name the capability and dispatch to the matching adapter, *and* move the tool-intrinsic detail down into that adapter. The skill layer ends knowing only the capability; the adapter ends holding the concrete detail.

A relocation has a prerequisite the rephrase doesn't: an adapter home must exist for that capability and provider. If one does, move the detail into it. If none exists, you cannot silently invent one inside this audit — hand off to the component-adding skill to scaffold the adapter for that provider×transport first, then complete the relocation. If even that can't be resolved (the capability isn't represented in the plugin's config at all, so there's nothing for an adapter to bind to), **flag-and-stop** that finding: report it as an unfixable leak with the reason, and leave the file untouched rather than apply a half-fix that breaks the contract. A correctly-reported leak the maintainer must resolve is a better outcome than a rewrite that dangles a capability with no backing.

## Re-scan after fixing

A rewrite can introduce a new reference — a rephrase that reaches for a word that is itself tool-flavored, a relocation whose dispatch phrasing accidentally names the adapter. After applying fixes, re-run detection over the edited files until a pass comes back clean. Each pass re-enters the same classify-and-rank logic; edits beget candidates, so don't trust a single post-fix scan. Loop until the skill layer holds no concrete tool reference outside `adapters/`. Bound the loop: if the same span is still dirty after two repair attempts, stop repairing it and flag-and-stop that finding with the reason — a span that won't converge in two attempts needs the maintainer's judgment, not a third guess.

Edge case — `--fix` with relocations that needed an adapter handoff: re-scanning after that handoff matters most, because you've touched two layers and added a dispatch seam, which is exactly where a new leak slips in. Treat "clean after the loop" as the only acceptable exit; a fix that leaves the next scan dirty is not a fix.

The output of this phase is the delivered report — and, under `--fix`, a skill layer that is tool-agnostic again, with any genuinely unfixable leak reported rather than papered over.
