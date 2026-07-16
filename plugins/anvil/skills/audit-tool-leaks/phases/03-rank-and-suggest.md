A finding the maintainer can't act on is half an audit. By now you have the confirmed leaks; this phase turns each one into something fixable — a precise location, the right shape of repair, and an order that puts the leaks that matter most at the top. The goal is that a maintainer (or `--fix`) can work the list top-down and stop early without leaving the worst leaks behind.

## Pin each leak to a location and the offending text

For every confirmed leak, record the file, the line, and the exact offending text — the token or phrase, not a paraphrase. "Line 12 names a tool" sends the maintainer hunting; "line 12: `the configured tracker` should be `the configured change-request backend`" lets them act without re-deriving what you already found. The anchor came from detection; carry it through verbatim. The quoting bar: the minimal span an exact-match edit would land on exactly once in the file — usually the offending phrase plus the clause it sits in, never the whole paragraph. The offending span is what gets rewritten, and a quote that matches twice sends the fix to the wrong line.

## Choose the fix shape

Each leak has one of two repairs, and which one depends on a single question: **is this detail something the skill layer should be saying differently, or something it shouldn't be saying at all?**

- **Rephrase to a capability** — when the sentence is genuinely about *what* gets done and the tool name is just the wrong word for it. The fix is a swap to a capability noun. A phase reading "publish the report to <a named backend>" becomes "publish the report to the configured artifacts backend"; the step is unchanged, only the altitude is corrected. Most leaks are this shape, because most leaks are a careless word, not a misplaced responsibility.

- **Relocate into an adapter** — when the leaked text is genuinely tool-intrinsic: an exact parameter, a transport detail, a call sequence that only one provider has. That detail doesn't belong reworded in the skill layer; it belongs *moved down* into the adapter that wraps the tool, with the skill layer left naming only the capability that dispatches to it. The recommendation is "name the capability here, move this detail to the adapter for that provider." If no adapter home exists yet for that capability, the relocation has a prerequisite — creating the adapter — which the fix phase handles via a handoff; here you just name the relocation as the correct shape.

The discriminator is the swap test again, applied to the *detail* rather than the token: if rewording to a capability noun fully captures what the step needs, rephrase; if rewording would lose information a real run actually needs, that information is tool-intrinsic and must relocate, not reword. Don't reach for relocation when a rephrase suffices — moving a careless word into an adapter manufactures adapter cruft and leaves the skill layer no cleaner than a one-word swap would have.

For each leak, write the concrete suggestion, and hold it to the bar that makes it applicable rather than a category label. A suggested rephrase is acceptable when all four hold (the bar is this skill's own tests — the swap test and the configured-X form in [what-counts-as-a-tool-name](../rules/what-counts-as-a-tool-name.md)):

1. **Drop-in** — it is exact replacement text: paste it over the offending span and the sentence parses.
2. **Passes the swap test itself** — the fix doesn't smuggle in a new tool-flavored word.
3. **Action-preserving** — same verb, same role for the object; only the altitude is corrected.
4. **Vocabulary-reusing** — it names the capability in the plugin's existing terms (the configured-X form keyed to a capability the plugin already declares), not a synonym minted on the spot. Two leaks against the same capability must land on the same noun, or the "fix" seeds a second vocabulary.

A relocation suggestion is acceptable when it names both sides: the capability phrasing that stays in the skill layer, and the specific adapter — existing or to-be-scaffolded — that receives the detail. "Reword this to capability level" meets none of these; that is the finding restated, not a suggestion.

## Rank by how load-bearing the leak is

Order the findings by blast radius, most severe first, so the list reads worst-to-least and an early stop still clears the leaks that matter:

- **Highest — the skill's own contract surface**: the `SKILL.md` description and flag meanings, and any phase line a cold executor would directly act on. A leaked tool name in a description pins the whole skill to one vendor in the place every reader and every downstream audit looks first; a leak in an actionable step makes a cold run guess or hard-depend on a tool the skill claims not to know.
- **Middle — body procedure and craft**: a leak buried inside a phase's prose, a rule's method, or a module's behavior. Real, but less exposed than the contract surface and acted on only by a reader already deep in that file.
- **Lowest — incidental asides**: a tool named in a parenthetical, a comment, or a passing illustration that nonetheless failed the swap test. Still a leak, still fixed, but it neither pins the contract nor misleads a run.

The tier test, for a leak that could read as two of these: `SKILL.md` description and flag text are highest by position; for everything else, strike the sentence and imagine a cold run. If the run would *do* something different — a step skipped, a target changed, a parameter lost — the line is acted on: highest. If the run behaves the same but a judgment somewhere loses its calibration — a rule's test, a module's behavior — the text steers without being executed: middle. If nothing changes in behavior or judgment, the sentence was ornament: lowest.

Two leaks of the same severity can be broken by reach: one that pins a capability used across many phases outranks one confined to a single step. The principle is constant — the more a leak commits the skill to a specific tool, and the more places that commitment radiates to, the higher it ranks.

The output of this phase is the ranked, anchored, suggestion-bearing finding list — ready for the report phase to emit, or for `--fix` to apply top-down.
