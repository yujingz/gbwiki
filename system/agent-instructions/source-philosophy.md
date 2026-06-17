---
type: system-rule
status: canonical
created: 2026-06-17
last_reviewed: 2026-06-17
owner: YZ
---

# Source Philosophy

Do not edit this philosophy unless YZ explicitly requests a source-philosophy update.

## Core Idea

This system is a methodology for using LLM agents to maintain a living knowledge base.

```text
Sources are evidence.
Capture is intake.
The wiki is synthesized understanding.
The system layer is the operating method.
Tools are replaceable.
Sync is plumbing.
```

The goal is not to ingest everything. The goal is to know:

```text
what exists
where it lives
which source is canonical
what has been captured
what has been summarized
what has been synthesized
what is stale
what needs review
what the current understanding is
```

## Separate Role From Location

A file's physical location does not define its conceptual role.

Classify by role:

```text
Is this source evidence?
Is this temporary capture?
Is this synthesized understanding?
Is this an operating rule?
Is this an index/source map?
Is this merely an asset?
Is this just sync or viewing infrastructure?
```

Do not classify by accidental implementation details:

```text
It is in Dropbox.
It is in Google Drive.
It is inside the workspace.
It is a PDF.
It came from a web clipper.
It was created by an agent.
```

## Conceptual Roles

The system has six conceptual roles:

1. Source systems
2. Source artifacts
3. Capture space
4. Source library
5. Wiki / synthesis layer
6. System / operating layer

## Recommended Structure

```text
knowledge-workspace/
  capture/
  sources/
  wiki/
  system/
  assets/
```

For this Markdown implementation:

```text
capture/
  quick-notes/
  daily/
  meetings/
  imports/
  clippings/
  attachments/

sources/
  library/
  maps/
  records/
    source-records/
    ingestion-records/
    review-records/

wiki/
  indexes/
  topics/
  people/
  organizations/
  projects/
  decisions/
  guides/

system/
  agent-instructions/
  templates/
  schema/
  scripts/
  migration/
  index.md
  log.md
  operating-model.md

assets/
```

## Source Library Domains

Use these stable source-library domains when local source material is actually useful:

```text
10-19-identity-legal-finance-and-paperwork/
20-29-life-health-home-and-relationships/
30-39-learning-research-and-knowledge/
40-49-career-work-and-ventures/
50-59-business-gtm-finance-and-operations/
60-69-product-data-technology-and-ai/
```

Do not create new top-level domains for a single company, project, source app, or temporary workflow.

## Ingestion Modes

Ingestion does not mean copying everything.

Use one mode:

```text
pointer-only
summary-only
selective-extract
snapshot
local-copy
mirror
fork
ignore
```

Default to `pointer-only`, `summary-only`, or `selective-extract` for external canonical systems. Use `snapshot` for time-sensitive public pages, dashboards, or API results. Use `local-copy` only when it improves durability, offline access, review, or reproducibility.

## Wiki Vs Source

A source note answers:

```text
What did the source say?
Where did this come from?
What evidence exists?
```

A wiki page answers:

```text
What do we currently understand?
What is the synthesized view?
What should future agents read first?
How do the pieces connect?
```

Never silently convert a source into synthesis without preserving provenance.

## Metadata

Important wiki pages should use:

```yaml
---
type: wiki-page
status: active
topics:
entities:
sources:
last_updated:
last_reviewed:
confidence:
---
```

Important source records should use:

```yaml
---
type: source-record
status: active
source_system:
source_name:
source_location:
canonical:
relationship:
ingestion_mode:
owner:
access_method:
trust_level:
sensitivity:
update_pattern:
staleness_risk:
last_reviewed:
related_wiki:
related_local_sources:
---
```

## Workflows

Capture:

```text
Create a note in capture, keep it low-friction, classify later.
```

Ingest:

```text
Identify source -> determine canonicality -> choose ingestion mode -> create/update source record -> extract key claims -> update wiki -> update index -> log.
```

Query:

```text
Read index/maps -> search wiki -> search records/sources if needed -> answer with provenance -> file durable insight back into wiki when useful.
```

Lint:

```text
Find contradictions, stale claims, orphan pages, missing source links, unprocessed capture, duplicate pages, missing metadata, and broken links.
```

## Final Rule

Do not build a warehouse. Build a thinking layer.

