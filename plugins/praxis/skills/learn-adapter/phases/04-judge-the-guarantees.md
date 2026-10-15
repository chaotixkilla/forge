A dedicated adapter keeps the port's guarantees because someone wrote it to. A learned mapping keeps them only where the tool's surface, or the map's own design, shows it can't break them. A mapping that might break one is worse than no mapping, so each guarantee gets a verdict. `(basis: maintainer, 2026-10-13)`

## The verdict per guarantee

For each operation, judge each guarantee the port's **Guarantees** section states for it. A guarantee is **kept** by one of two tests, and the verdict cites the line that meets it.

1. **By the surface.** The behaviour that breaks it needs an input the map never sets, such as a force or admin-override flag left unset, or the call can't express it at all.
2. **By the map.** The map's own calls, returns or failures realize it. Examples:
   - returning each created item's reference as its call returns, before the next call runs;
   - mapping a source that collects nothing to `not collected`;
   - reporting `private-until-shared` when the surface can't show who has access.

Otherwise it is **not shown**: the behaviour is undocumented, or an input the map can't leave out could break it. A description's words can only turn a verdict into not shown, never ground a kept. A tried read is evidence only for what it showed. A write's guarantee is never inferred from a run, since none happens. `(basis: derived — the surface and the map are the only read-only evidence)`

A guarantee the port keeps in its own procedure, before dispatch, is not judged here. Communication's check that a target may be reached is one: it runs whatever route the call takes.

## Variants

A **variant** is one value of an alternative the port's operation lists, named in the port's words: a merge strategy, a review's stance, a run triggered or read, a change fetched with or without its description, a share's scope, a flag's mode. Anything else is the whole operation.

An operation with every guarantee kept is usable. One with any guarantee not shown is `unsupported` for the variant it affects, and only that variant. For example, a merge whose rebase strategy can't be shown to respect the landing constraint is unsupported for rebase, while its merge-commit variant may still be usable. `(basis: maintainer, 2026-10-13)`

The output is each operation's verdicts, and the operations or variants made unsupported with the guarantee that did it, for [write-the-map](05-write-the-map.md).
