gather is delegated: its output is raw material for a calling skill, not a human deliverable. So the return is shaped for a consumer to act on — every finding weighted and anchored, every open call flagged, nothing pre-decided that the caller should decide.

## Assemble the picture
1. Return the findings grouped by tier, each carrying its anchor, its tier/grade, and — for a conclusion — its provenance kept distinct. Relay each finding's grade or label *verbatim from its lane* — never collapse a lane's grade or label to a coarser value, which would overstate confidence ([separate-provenance-from-conclusion](../rules/separate-provenance-from-conclusion.md)). Follow with the conflicts (each position, its tier, its basis), the divergences (project-vs-norm), the gaps (documented absences, lanes not consulted), and the transfer questions flagged for the caller.
2. Do not format as a human report or render a verdict — the caller shapes the deliverable and makes the calls gather surfaced.

## The pinned return shape
Two consumers of the same gather must receive the same-shaped picture, so the shape is fixed. (basis: the explorer-family return shapes + the sourcing model, ratified 2026-07-03.)

```
LANES: <consulted> | dropped: <lane: reason>
FINDINGS (by tier):
  authoritative     — <claim> · <anchor: URL§ / RFC§> · <force/scope> · reach: <how far it applies>
  project-internal  — <claim> · <anchor: file:line / commit / page+provenance> · <grade, verbatim from the lane: code path-confirmed|inferred · repository on-record|reconstructed · knowledge-base current|possibly-stale|superseded>
  anecdotal         — <claim + mechanism> · <label, verbatim from the lane: opinion / single-report / corroborated-practice (N independent origins)> · <dates> · <links>
CONFLICTS: <position A (tier, basis)> vs <position B (tier, basis)> — <where the dispute lives>
DIVERGENCES: <code/repo> diverges from <spec/doc> at <anchor>
GAPS: <documented absences; lanes not consulted and why>
TRANSFER (caller decides): <source> reaches <scope>; gap to this project: <what is unverified>
```

3. A section *or an empty tier row* with no entries is stated empty (`CONFLICTS: none`, `authoritative — none`), never dropped — an absent line reads as "not checked," which is a different claim from "checked, none found."

## The shape is gather's completion gate
gather has **not completed** until it emits this shape. A return that hands back raw explorer transcripts, or a synthesis in any other form, is an *incomplete* gather — the pinned shape is the trace that proves phases 03–04 actually ran. A caller that receives anything lacking these sections should treat gather's synthesis as not-run and re-invoke, rather than reason over the raw pile itself (doing so is the delegation-bypass this shape exists to prevent). Emitting the shape is not optional formatting; it is the step's done-state.

The output of this phase: the weighted picture in the pinned shape, handed to the caller.
