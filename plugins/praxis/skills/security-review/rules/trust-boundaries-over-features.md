# Trust boundaries over features

Attention naturally flows to the prominent feature — the big new endpoint, the complex algorithm, the code the change is *about*. But security guarantees are not made where the code is interesting; they are made, and broken, exactly where data changes hands between parties that trust each other differently. A five-line handler that takes a tenant id from the caller and reads a record with it is a smaller feature and a larger risk than a hundred lines of internal computation. This rule redirects the hunt from where the code is big to where the trust changes.

## Enumerate the crossings, prioritize by them

A trust boundary is any line where data or control passes between parties with different privilege or trust: the **network** edge (an external client reaching the system), a **process** or service boundary (one component calling another), a **privilege** boundary (unprivileged code invoking privileged action), a **tenant** boundary (one customer's request touching data partitioned from another's). Map the boundaries the surface crosses first, then drive the hunt by them — the input that just crossed a boundary is the input to distrust, and the action just inside one is the action to guard.

## The discriminator: a crossing, not a call

The test that separates a boundary from ordinary plumbing: **do the two sides trust each other differently — does one hold a privilege, an identity, or a data scope the other must not assume?** If yes, it is a boundary: what crosses it is untrusted until checked, and the guarantee (authentication, authorization, validation, scoping) is owed right there. If both sides are equally trusted internal code, it is a call, not a crossing — real, but not where the breach lives. This is why the surface map in [scoping-the-surface](../phases/01-scoping-the-surface.md) records boundaries, not just files: the boundaries are the map the hunt navigates by.

`(basis: threat-modeling first principle — trust boundaries are the primitive STRIDE/data-flow-diagram threat modeling is organized around; the method, not a graded bar.)`
