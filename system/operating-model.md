---
type: system-rule
status: active
created: 2026-06-17
last_reviewed: 2026-06-17
owner: GB friends
---

# Operating Model

This page maps the source philosophy to this `gbwiki` implementation.

## Rule Hierarchy

1. `system/agent-instructions/source-philosophy.md`
2. root `AGENTS.md`
3. this operating model
4. `system/index.md`
5. source maps, records, schema, templates, and logs

## Current Implementation

| Conceptual role | Current path | Notes |
| --- | --- | --- |
| Capture space | `capture/` | Fast unprocessed intake. |
| Source library | `sources/library/` | Selected local source material only when useful. |
| Source maps | `sources/maps/` | Maps of source systems and important source locations. |
| Source records | `sources/records/` | Source, ingestion, and review records. |
| Assets | `assets/` | Supporting media that is not source evidence. |
| Wiki / synthesis | `wiki/` | Current understanding, maps, decisions, guides, entities, and projects. |
| System / operating layer | `system/` and root `AGENTS.md` | Rules, index, templates, logs, and maintenance workflows. |

This repository keeps only selected imported source material when it improves durability, offline access, review, or reproducibility.

## Source Truth

Important originals may live outside this workspace.

Default policy:

- Do not ingest external systems wholesale.
- Prefer `pointer-only`, `summary-only`, or `selective-extract` for canonical external originals.
- Use local copies only when they improve synthesis, offline access, reproducibility, or durability.
- Preserve source location, canonicality, owner, ingestion mode, and staleness risk.

Use `sources/maps/source-systems.md` for source-system records.

## Ingest Contract

When asked to ingest:

1. Identify the source system and source artifact.
2. Decide whether the original is canonical elsewhere.
3. Choose ingestion mode.
4. Run `system/agent-instructions/ingestion-verification.md` if claims may enter durable synthesis, affect decisions, be shown externally, or need online credibility checks.
5. Check existing `wiki/`, `sources/records/`, and relevant capture material before writing new synthesis.
6. Use `sources/maps/verification-sources.md` as the expandable external-source registry when online checks are useful.
7. Store selected local source material in `sources/library/` only when useful.
8. Update relevant wiki pages.
9. Update index/source maps when a durable entry point is created.
10. Log meaningful changes in `system/log.md`.

## Query Contract

When answering questions:

1. Read `system/index.md` or a relevant source map.
2. Search `wiki/` first.
3. Search source records and source library only when needed.
4. Distinguish current understanding from source evidence.
5. File durable answers back into `wiki/` when useful.

## Lint Contract

Lint is a report-first workflow. It should identify concrete issues before editing:

- unprocessed capture
- source records without related wiki pages
- wiki pages without sources
- duplicate or overlapping pages
- stale claims
- broken links
- orphan pages
- unclear titles
- missing metadata
- unmanaged migration staging
- high-staleness snapshots
