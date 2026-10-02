# Integrate against the current target

The branch was green when it forked from its **integration target** — the branch it lands into: the trunk, or an intermediate line like an epic or `develop` branch — but the target has moved since, and the merge the gate is supposed to vet is the branch *combined with the target's current head*, which the gate never saw. The dangerous case has no textual conflict at all: one side renames `calculateBill` and updates its callers while the branch adds a new call to the old name; the two merge cleanly and the merged code references a method that no longer exists. Version control flags only *textual* overlap, so this **semantic conflict** sails through a clean merge and breaks the line.

## The method — reconcile, then gate, on the target's live head

- **Reconcile against the target's live head before the gate.** Before running the pre-merge gate in [run-the-gate](../phases/03-run-the-gate.md), bring the branch up to the current integration target (merge or rebase per [match-the-team-flow](match-the-team-flow.md)), so the gate runs on the merged result — the actual post-merge tree — not on the base the branch forked from. The target is the one [assess-the-change](../phases/01-assess-the-change.md) resolved, not assumed to be the default branch.
- **If the target moves between the gate and the merge, re-reconcile and re-gate.** A gate that passed against head N is stale once the target is at N+1; landing on N+1 without re-gating merges a base the gate never vetted. Re-reconcile against the new head and re-run the gate before merging. (A merge queue that tests each candidate against the target *tip* automates exactly this on the host's side.)
- **A green branch and a green target do not imply a green merge.** This is the same "green on the parts ≠ green on the whole" trap that governs conflict resolution ([resolve-conflicts-by-intent](resolve-conflicts-by-intent.md)): the merged tree is a third thing neither side tested.

## Why textual cleanliness is not enough

A semantic conflict is a merge that is textually clean yet broken because one side changed a contract the other still relies on. The smaller the divergence window, the smaller that surface: integrating to the target at least daily, on short-lived branches, raises delivery performance. `(basis: Fowler, "SemanticConflict"; the "merge skew" and "Not Rocket Science Rule" accounts behind merge queues; surveys of the conflict class; DORA)`

## The bound on reconciliation

Reconcile enough to gate the true merge; do not turn a routine land into an open-ended rebase of a long-diverged branch. **Deliberately open:** how far a branch has drifted, and whether to reconcile-and-proceed or route back for a fresh rebase, depends on the divergence in front of you — a branch a few commits behind its target reconciles inline; one that has drifted for weeks across a refactor is a signal the *work* needs re-basing before it lands, which land surfaces rather than silently absorbing. The stopping test: reconcile until the gate is running on the real post-merge tree; if reaching that requires re-authoring the change, that is develop's job, not land's.
