# publish-incident-record (`--publish`)

Activated by `--publish`, referenced from [learn-and-harden](../phases/06-learn-and-harden.md).

Base behavior: [learn-and-harden](../phases/06-learn-and-harden.md) produces the incident record / postmortem and returns it. This module publishes it as a durable, team-facing document. Deletion test: remove it and learn-and-harden still produces the record inline; publishing it is additive — so it is a module. (A postmortem is a durable *document* — the artifacts capability's job — not a chat message, which is why publishing routes through the artifacts capability rather than a notification.)

## The delta — publish as a clean team-facing document

Hand the finished retrospective to the [publish-artifact](../../publish-artifact/SKILL.md) port as a durable, audience-facing document under the **`postmortems`** type-key — the timeline, impact, contributing factors, and follow-ups. (Name the type as that key, whatever the record is called in prose; the port resolves the key to the configured destination.) **The clean-export bar is a content standard, not a passing note:** the published document carries the incident's substance and decisions and **none** of operate's internal machinery — no phase names, no critic/loop mechanics, no port-call descriptions, no praxis process. Strip every internal-process reference before handing it off; the port publishes faithfully and adds no process metadata of its own. `(basis: ratified house decision — anything written through the artifacts capability is a clean export of the session's substance for a human audience.)`

## Why the artifacts capability, not communication

A postmortem is a durable document a team reads and refers back to — that is [publish-artifact](../../publish-artifact/SKILL.md)'s remit, the settled artifacts-vs-communication line. Posting a *link to* or a *summary of* the published postmortem into an incident channel is a separate [communication](../../communication/SKILL.md) post (`--notify`/[notify-stakeholders](notify-stakeholders.md)); producing the document itself is this module.

## Prerequisite and degrade

The publish goes through the publish-artifact port (doer-owns-prerequisites; operate declares none). Degrade if the artifacts backend is unavailable: return the clean record for the user to publish by hand, noting automated publishing was unavailable — the retrospective is still produced.
