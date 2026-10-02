# Give the task a branch

An act that changes the code builds on a branch of its own, so nothing reaches the integration line except through a review request.

Before step 1, give the task a branch: when the work starts on the integration line, cut one from its head, named for the task's key, and run every step on it; work already on a branch of its own stays there, and on resume, a task whose branch exists checks it out instead of cutting another. Nothing the act changes reaches the integration line except through a review request. (basis: derived from [open-the-review-request](open-the-review-request.md)'s no-direct-merge)
