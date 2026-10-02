# The risk scale

A plan spends its deepest work on the flows most likely to hurt. Rating them by feel sends that work to whichever flow was listed first; this scale rates each on two axes so two planners rank the same flows the same way.

`(basis: maintainer, 2026-07-05; after the AIAG-VDA FMEA Handbook 2019 and ISO 31000)`

- **Severity — how hard it bites** (assign by the *worst realistic* consequence if the flow fails):
  - *Critical* — irreversible or safety/legal/data-loss: data corruption, a security breach, regulatory noncompliance, unrecoverable state.
  - *Significant* — a primary user journey degrades or breaks, but it is recoverable and bounded.
  - *Minor* — no discernible effect on the user; cosmetic or a slight, secondary inconvenience.
- **Likelihood-to-bite — how likely it is to go wrong**, assigned from four checklist answers — prevention controls, the path's novelty or complexity, prior incidents on it, and test coverage — each strong, partial, or weak/absent:
  - *High* — any one answer weak or absent: weak or absent controls, a new or complex path, a history of failing here, or no test coverage.
  - *Medium* — none weak or absent, at least one partial.
  - *Low* — all four strong: strong controls, a well-trodden path, no known prior failure, high coverage.

  `(basis: derived from the checklist's own four items)` (routed to maintainer: absent coverage counted as an absent control, so it alone makes High.)

**Combining the two axes is a fork — plan does not crown one** (encode the fork, route the choice): *severity-dominant* (any Critical flow is top-priority regardless of likelihood; likelihood only orders within a severity band — `basis: AIAG-VDA Action Priority`) versus *symmetric* (likelihood × impact / RAG grid — `basis: PMI PMBOK 6e`). Cox (2008, *Risk Analysis*) is the caution against naive multiplication — a symmetric grid can mask a low-likelihood/Critical flow behind a high-likelihood/Minor one. Routing: the surrounding team's existing risk practice wins → house rule → maintainer. Whichever is used, a Critical flow is never deprioritized on low likelihood without a documented reason.
