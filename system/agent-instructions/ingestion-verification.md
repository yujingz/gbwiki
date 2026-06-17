---
type: system-rule
status: active
created: 2026-06-17
last_reviewed: 2026-06-17
owner: YZ
---

# Ingestion Verification

Use this when an ingest contains factual claims that may enter `wiki/`, affect decisions, be shown externally, or become future planning evidence.

Do not make every ingest heavy. For private first-party notes, preserve provenance and mark them as first-party evidence. Verify only the external or decision-relevant claims.

## Success Criteria

An ingest is better when future agents can see:

- what the source claimed
- what the workspace already knew
- what was checked externally
- what remains uncertain or contradicted
- whether a second model or human review was attempted
- which claims were allowed into wiki synthesis as current understanding

## Verification Pass

### 1. Agent Knowledge Check

Use model judgment only to triage and flag risk.

Ask:

- What are the main factual claims, dates, entities, numbers, causal claims, and decisions?
- Which claims are likely stale, surprising, ambiguous, high impact, or easy to get wrong?
- Which statements are first-party observations rather than externally verifiable facts?
- Which items should stay as "source says" instead of becoming wiki fact?

Do not treat model memory as source truth.

### 2. Existing Workspace Check

Minimum path:

1. Read `system/index.md` or the relevant source map.
2. Search `wiki/`.
3. Search `sources/records/`.
4. Search `sources/library/` or `capture/` only when wiki and records are insufficient.

Classify the source against the current workspace:

- `new`
- `duplicate`
- `updates-existing`
- `contradicts-existing`
- `pipeline`

Prefer updating existing durable pages over creating duplicates.

### 3. External Verification Check

Use online checking when the claim is public, time-sensitive, third-party, high impact, customer-facing, legal, medical, financial, procurement-related, or likely to be reused.

Default method:

1. Scope the exact claim.
2. Prefer upstream or primary sources.
3. Use lateral reading to evaluate the source and find better coverage.
4. Trace quotes, statistics, product specs, policy claims, and legal claims back to original context.
5. Record checked URLs, access date, and whether each source is primary, secondary, or commentary.

Use `sources/maps/verification-sources.md` as the expandable source registry. The registry is a starting point, not a whitelist.

### 4. Second Review

Use another model, such as Claude, when an ingest is complex, ambiguous, high impact, or creates durable synthesis that YZ may rely on.

Good review prompts provide a compact evidence pack, not raw unbounded files.

Ask the reviewer to check:

- Does the source support the synthesis?
- Is this already in the workspace or pipeline?
- Are there contradictions with existing wiki/source records?
- Are any claims under-sourced, stale, or overstated?
- What should stay uncertain?

Record the result in `sources/records/review-records/`. If second review fails or is unavailable, record that too.

## Recording Format

Add a compact verification section to important ingestion records.

```markdown
## Claim Verification

| claim | existing workspace state | external check | result | action |
| --- | --- | --- | --- | --- |
| <source claim> | new / duplicate / updates-existing / contradicts-existing / pipeline | URL or skipped reason | verified / partially-verified / contradicted / unresolved / not-checked | promoted to wiki / kept as source claim / flagged / deferred |
```

For source records, add fields only when useful:

```yaml
trust_level:
verification_status:
verification_notes:
external_checks:
review_record:
```

For wiki pages:

- use `confidence: high|medium|low`
- cite source paths or source records
- mark contradictions and stale claims inline
- avoid stating unverified source claims as current understanding

