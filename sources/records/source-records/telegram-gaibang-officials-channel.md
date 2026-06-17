---
type: source-record
status: active
source_system: Telegram
source_name: 丐帮官员频道
source_location: Telegram chat export snapshots; initial local export at /Users/yujing/Downloads/Telegram Desktop/ChatExport_2026-06-17 (1)
canonical: external-system-primary
relationship: first-party-member-export
ingestion_mode: snapshot
owner: YZ for local export; group participants for conversation content
access_method: Telegram Desktop export archived into gbwiki source library
trust_level: first-party-export
sensitivity: personal-private
update_pattern: periodic snapshot exports
staleness_risk: high for messages after each export timestamp
last_reviewed: 2026-06-17
related_wiki:
  - wiki/topics/telegram-gaibang-mainline.md
  - wiki/topics/telegram-gaibang-games-top5.md
related_local_sources:
  - sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/
verification_status: integrity-checked; content claims not promoted
---

# Telegram Group Chat: 丐帮官员频道

## What This Source Is

- Telegram Desktop export snapshots for a long-running group chat used by YZ and close friends.
- The first ingested snapshot covers `2016-04-29T01:21:51` through `2026-06-17T10:26:11`.
- The first snapshot contains `275120` exported messages plus small sticker/video attachment folders.

## Canonicality

- Telegram is the continuing canonical source for future messages.
- Each local export is a point-in-time snapshot and should not be treated as current after its export timestamp.
- The gbwiki copy is preserved for durability, offline access, reproducibility, and future machine processing.

## Access

- Current local snapshot:
  `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/`
- Original imported path:
  `/Users/yujing/Downloads/Telegram Desktop/ChatExport_2026-06-17 (1)`

## Ingestion Notes

- Preserve the original export copy as `original-export.tar.zst`; the expanded `original/` directory is intentionally not retained.
- Use `derived/result.compact.json.zst` for space-efficient JSON processing and transfer.
- `system/scripts/analyze-telegram-snapshot.py` can read `.zst` input directly.
- Future periodic exports should be added as new date-stamped snapshot directories instead of overwriting this batch.

## Related

- Wiki synthesis: `wiki/topics/telegram-gaibang-mainline.md`
- Wiki synthesis: `wiki/topics/telegram-gaibang-games-top5.md`
- Ingestion record: `sources/records/ingestion-records/2026-06-17-telegram-gaibang-officials-channel-snapshot.md`
