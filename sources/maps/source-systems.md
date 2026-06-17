---
type: source-map
status: active
created: 2026-06-17
last_reviewed: 2026-06-17
owner: GB friends
---

# Source Systems

This page records high-level source systems. It is not an ingestion manifest and does not authorize bulk copying.

Add source systems here as they become relevant.

## Workspace Local

```yaml
source_system: gbwiki
relationship: owned
canonical: mixed
local_path: .
ingestion_default: local-copy
staleness_risk: low-to-medium
```

Use for:

- capture notes
- selected local source artifacts
- extracted source notes
- snapshots
- synthesized wiki pages
- system rules, logs, templates, and indexes

Default handling:

- `capture/` is the ingestion entry point for unprocessed intake.
- `sources/library/` is selected source material.
- `sources/maps/` contains source-system and source-location maps.
- `sources/records/` contains source, ingestion, and review records.
- `assets/` contains reusable/supporting media.
- `wiki/` is synthesis.
- `system/` is operating structure.

## Telegram

```yaml
source_system: Telegram
relationship: external-communication-platform
canonical: external-system-primary
local_path: sources/library/20-29-life-health-home-and-relationships/telegram/
ingestion_default: snapshot
sensitivity: personal-private
staleness_risk: high for ongoing chats after each export timestamp
```

Use for:

- Telegram Desktop chat exports.
- Date-stamped snapshots of long-running chats.
- Derived machine-readable files generated from preserved exports.

Default handling:

- Keep each export as a separate date-stamped snapshot.
- Preserve original export files as a compressed restorable archive when expanded copies are too large.
- Store deterministic lossless derived files under `derived/`.
- Do not promote chat content into `wiki/` without a specific synthesis task and provenance.

## Future Source Records

Create more specific source records only when a source is important enough to revisit.

Good candidates:

- one major local folder
- one cloud-drive folder
- one API or database
- one Git repo used as source evidence
- one shared knowledge base
- one public website or documentation set

Each source record should include canonicality, owner, access method, ingestion mode, staleness risk, related wiki pages, and related local source notes.
