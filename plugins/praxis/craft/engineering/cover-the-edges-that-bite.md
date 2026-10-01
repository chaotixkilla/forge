# Cover the edges that bite

Spend the case budget on the inputs that actually break code — the boundaries and failure paths — not on more variations of the happy path. The happy path is where the author's attention already was; bugs live at the edges the author skipped: empty and single-element collections, zero, one, the maximum and just past it, null and absent, the off-by-one at a range's end, the error and cleanup branches, and the counter-examples a correct implementation must *reject*.

The discipline is to find *this change's* real edges, not to recite a generic checklist: read what the change actually does and ask where its behavior changes discontinuously — those discontinuities are the boundaries worth a case, on the edge and just across it. When the case budget can't cover every edge, rank them by risk: an edge that bites hard (a high blast radius) outranks a low-risk boundary. `(basis: Myers, "The Art of Software Testing"; ISTQB)`
