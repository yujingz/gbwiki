---
type: source-map
status: active
created: 2026-06-17
last_reviewed: 2026-06-17
owner: YZ
---

# Verification Sources

This is the expandable source registry for external checks during ingest.

It starts with source patterns, not a fixed trusted-source list. Add concrete sources only when a real ingest needs them.

## Source Patterns

| id | source pattern | use for | caveats |
| --- | --- | --- | --- |
| official-primary-source | Official agency, company, product, standards, repository, or API source. | Exact facts, specs, policy text, release dates, ownership, official wording. | Can be self-interested, stale, incomplete, or jurisdiction-specific. |
| original-data-or-filing | Dataset, registry, filing, audit report, changelog, source code, or primary record. | Numbers, historical records, compliance, releases, financial/company facts. | Requires context and may not explain implications. |
| domain-expert-secondary | Reputable domain publication, analyst note, technical article, or textbook-level reference. | Interpretation, background, triangulation, and claim framing. | Secondary evidence. Prefer upstream sources for hard claims. |
| reputable-news-or-fact-check | Independent news orgs and fact-checkers with transparent sourcing and corrections. | Public-event triangulation and dispute checks. | Not a replacement for primary records. Confirm current status and methodology. |

## Entry Template

```yaml
source_system:
source_location:
owner:
trusted_for:
not_trusted_for:
access_method:
staleness_risk:
last_reviewed:
related_domains:
notes:
```

## Maintenance

Append new trusted sources when a real ingest needs them.

Remove or downgrade sources when they become inaccessible, stale, misleading, or too broad to be useful.

