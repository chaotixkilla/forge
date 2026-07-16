`--budget=<n>` caps the total number of recruit/fetch operations the gather may spend, for cost- or latency-bounded runs.

1. Allocate the budget across the chosen lanes by importance — the lanes most likely to hold the answer get the most operations; a lane the question only grazes gets one pass or none.
2. Stop spending on a sub-question once it is settled (saturated), and redirect the remainder to the still-open ones rather than over-gathering a decided point.
3. When the budget binds before saturation, stop and flag it per [know-when-to-stop](../rules/know-when-to-stop.md) — the budget is the cap that forces the early stop, so the caller reads the picture as bounded, not complete.
