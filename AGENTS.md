# Knowledge System Agent Instructions

Prefer Chinese when possible. Address collaborators by their preferred names when known.

## Highest Priority

This workspace is governed by `system/agent-instructions/source-philosophy.md`.

Read and follow that file before making structural, ingestion, migration, or wiki-synthesis decisions. Do not edit the source philosophy unless repository maintainers explicitly ask for a source-philosophy update.

If this file, older notes, or folder names conflict with the source philosophy, follow the source philosophy and surface the conflict.

Read order for structural work:

1. `system/agent-instructions/source-philosophy.md`
2. root `AGENTS.md`
3. `system/operating-model.md`
4. `system/index.md`
5. relevant source maps, records, schema, and templates

## Core Model

This is not a raw-data warehouse. It is a source-aware, tool-independent, LLM-maintained thinking system.

Core distinctions:

- Sources are evidence.
- Capture is intake.
- `wiki/` is synthesized understanding.
- `system/` is the operating method.
- Tools are replaceable.
- Sync is plumbing.

Main workflow:

```text
capture -> triage -> ingest -> synthesize -> index/log -> lint
```

Main classification rule:

```text
Classify by future retrieval intent, not by file type, source app, capture method, or sync location.
```

## Current Implementation

- `capture/` is the ingestion entry point for unprocessed intake.
- `sources/library/` is for selected local source material only when useful.
- `sources/maps/` records source systems and source-location maps.
- `sources/records/` records source records, ingestion records, and review records.
- `assets/` is for reusable or supporting media that is not source evidence.
- `wiki/` is the synthesis layer.
- `system/` is the operating layer.

Do not copy or import raw data from other vaults or source systems unless repository maintainers explicitly ask.

## Operating Principles

- KISS. Use the simplest structure that solves the retrieval and synthesis problem.
- Preserve provenance. Never silently convert source material into synthesis without traceable source paths.
- Do not overwrite source truth.
- Do not copy everything into this workspace.
- Keep capture low-friction.
- Keep wiki pages synthesized.
- Prefer updating existing durable pages over creating duplicates.
- Mark uncertainty, staleness, and contradictions explicitly.
- Log meaningful ingest, query-synthesis, lint, and rule changes in `system/log.md`.
- Avoid large restructures unless repository maintainers explicitly approve the batch and success criteria.

## Query Workflow

When answering collaborators' questions:

1. Read `system/index.md` or the relevant source map first.
2. Search `wiki/` before searching source artifacts.
3. Search `sources/records/`, `sources/library/`, or external source systems only when wiki synthesis is insufficient.
4. Distinguish synthesis from source evidence in the answer.
5. Cite concrete paths or source locations when useful.
6. If the answer creates durable understanding, update or propose a wiki page and log the change.

## Ingest Workflow

When ingesting source material:

1. Identify the source system and source artifact.
2. Decide whether the original is canonical elsewhere.
3. Choose an ingestion mode: `pointer-only`, `summary-only`, `selective-extract`, `snapshot`, `local-copy`, `mirror`, `fork`, or `ignore`.
4. Run `system/agent-instructions/ingestion-verification.md` when claims may enter durable synthesis, affect decisions, be shown externally, or need online credibility checks.
5. Create or update a source record when the original lives outside the workspace.
6. Put selected local source material in `sources/library/` only when useful.
7. Update relevant `wiki/` pages when the source changes understanding.
8. Add backlinks and source references.
9. Update `system/index.md` when a new durable entry point is created.
10. Append a concise `system/log.md` entry.

## Wiki Workflow

Use `wiki/` for current understanding:

- topic pages
- person pages
- organization pages
- project pages
- decision records
- guides
- maps and indexes

A source note answers:

```text
What did the source say?
Where did this come from?
What evidence exists?
```

A wiki page answers:

```text
What do we currently understand?
What should future agents read first?
How do the pieces connect?
What conclusion or operating knowledge should survive this chat?
```

## Lint Workflow

Periodically check for:

- unprocessed `capture/` items
- source records without related wiki pages
- wiki pages without sources
- duplicate or overlapping wiki pages
- stale claims
- broken links
- orphan pages
- unclear titles
- missing metadata on important notes
- unmanaged migration staging
- snapshots with high staleness risk

Lint should produce concrete fixes, not abstract criticism.

## Editing Rules

- Read before writing.
- Touch only what the task requires.
- Do not delete, move, or destructively rewrite files without explicit confirmation from repository maintainers.
- Do not refactor adjacent structure just because it looks messy.
- If a deterministic script can answer routing, counting, or validation, use code instead of judgment.
- Use `uv` for Python work where an environment is needed.
- Use `pnpm` for JS/TS work where a package manager is needed.
- Keep changes easy for humans and future agents to review.

Use the correct names when they appear:

- Company: coScene
- CLI product: coCLI or `cocli`
