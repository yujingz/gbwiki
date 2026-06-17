---
type: index-page
status: active
created: 2026-06-17
last_reviewed: 2026-06-17
---

# Index

This is the main navigation map for `gbwiki`.

It is not a full directory listing. It keeps the entry points future agents should read first.

## System

- [[system/agent-instructions/source-philosophy]]: canonical source philosophy.
- [[system/operating-model]]: implementation mapping for this workspace.
- [[system/agent-instructions/ingestion-verification]]: ingest-time claim verification, existing-workspace checks, external checks, and second review.
- [[sources/maps/source-systems]]: high-level source-system map.
- [[sources/maps/verification-sources]]: expandable external verification source registry.
- [[system/templates/wiki-note]]: wiki page template.
- [[system/templates/source-record]]: source record template.
- [[system/templates/ingestion-record]]: ingestion record template.
- [[system/templates/capture-note]]: capture note template.
- [[system/log]]: append-only operation log.

Read order for structural work:

1. `system/agent-instructions/source-philosophy.md`
2. root `AGENTS.md`
3. `system/operating-model.md`
4. relevant source maps, records, schema, and templates

## Capture

`capture/` is the default entry point for new unprocessed intake.

- `capture/quick-notes/`
- `capture/daily/`
- `capture/meetings/`
- `capture/imports/`
- `capture/clippings/`
- `capture/attachments/`

Capture is temporary. Triage useful material into `sources/library/`, `wiki/`, `sources/records/`, `assets/`, or `system/migration/`.

## Wiki

`wiki/` starts empty.

Use it for synthesized understanding, not raw source storage.

Recommended lanes:

- `wiki/indexes/`
- `wiki/topics/`
- `wiki/people/`
- `wiki/organizations/`
- `wiki/projects/`
- `wiki/decisions/`
- `wiki/guides/`

Register durable entry pages here when they become important.

## Sources

`sources/` starts without source materials.

- `sources/library/`: selected local source material only when useful.
- `sources/maps/`: maps of source systems and external verification sources.
- `sources/records/source-records/`: one record per important external source.
- `sources/records/ingestion-records/`: records of processed ingest batches.
- `sources/records/review-records/`: model/human review records.

Do not ingest external systems wholesale. Use pointer-only, summary-only, or selective-extract unless there is a clear reason to copy.

## Assets

`assets/` is for supporting media that is not itself source evidence.

If a media file is evidence, treat it as a source artifact instead.

