---
type: ingestion-record
status: completed
created: 2026-06-17
source: redacted local Telegram Desktop export path; archived in snapshot
ingestion_mode: snapshot
related_source_records:
  - sources/records/source-records/telegram-gaibang-officials-channel.md
related_wiki:
  - wiki/topics/telegram-gaibang-mainline.md
  - wiki/topics/telegram-gaibang-games-top5.md
verification_status: integrity-checked; no durable content claims promoted
---

# Telegram Group Chat Snapshot 2026-06-17

## Source

- Source system: Telegram
- Source artifact: Telegram Desktop export directory
- Original local path: redacted local Telegram Desktop export path; archived in snapshot
- Exported chat name: `丐帮官员频道`
- Exported chat type: `private_supergroup`
- Telegram chat id in export: `1077197275`

## What Was Ingested

- Copied the full export directory, compressed it into `original-export.tar.zst`, verified the archive by extraction and `diff -qr`, then removed the expanded `original/` copy to save space.
- Generated lossless derived files:
  - `derived/result.compact.json.zst`
  - `derived/export-metadata.json`
  - `derived/analysis/`
- `derived/result.compact.json` was used as a temporary expanded file and removed after verifying `derived/result.compact.json.zst` could restore it byte-for-byte.
- Generated `checksums.sha256`.

Metadata observed from the export:

| field | value |
| --- | --- |
| message count | `275120` |
| first message date | `2016-04-29T01:21:51` |
| last message date | `2026-06-17T10:26:11` |
| exported message types | `message: 275016`, `service: 104` |
| original export size | about `96M` |
| compressed original archive size | about `7.5M` |
| compressed compact JSON size | about `7.2M` |
| final snapshot size | about `16M` |

## Claim Verification

| claim | existing workspace state | external check | result | action |
| --- | --- | --- | --- | --- |
| This is a Telegram chat export snapshot from the provided local path. | new | skipped; first-party local export | integrity-checked | kept as source evidence |
| The export contains `275120` messages from `2016-04-29T01:21:51` to `2026-06-17T10:26:11`. | new | skipped; derived directly with `jq` from local export metadata | integrity-checked | recorded in source and ingestion records |
| Compact JSON is lossless relative to original JSON semantics. | new | deterministic local check | verified | recorded in snapshot README |
| The compressed original archive can restore the full copied export directory. | new | deterministic local extraction and `diff -qr` | verified | expanded copy removed after verification |

No conversational claims from the chat were promoted into `wiki/`.

## Pages Created

- `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/README.md`
- `sources/records/source-records/telegram-gaibang-officials-channel.md`
- `sources/records/ingestion-records/2026-06-17-telegram-gaibang-officials-channel-snapshot.md`
- `wiki/topics/telegram-gaibang-mainline.md`
- `wiki/topics/telegram-gaibang-games-top5.md`

## Pages Updated

- `sources/maps/source-systems.md`
- `system/index.md`
- `system/log.md`

## Verification Commands

```sh
base="sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot"

zstd -t "$base/original-export.tar.zst"
zstd -t "$base/derived/result.compact.json.zst"
zstd -dc "$base/derived/result.compact.json.zst" | jq -S -c . | shasum -a 256

(cd "$base" && shasum -a 256 -c checksums.sha256)
```

## Follow-Ups

- Consider adding a deterministic importer for future snapshots that creates the same directory shape and checksums.
- Consider generating a privacy-preserving structural index by month, participant id, and message type before any semantic analysis.
- Consider generating a compressed JSONL message stream only if future tooling needs streaming reads.
- First wiki synthesis has been created; future synthesis should refine specific questions, topics, people, or time periods rather than expanding broad claims.
