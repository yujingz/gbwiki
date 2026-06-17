---
type: log
status: active
created: 2026-06-17
last_reviewed: 2026-06-17
---

# Log

Append meaningful operations here.

## 2026-06-17 | setup | Initial gbwiki skeleton

- Created minimal source-aware knowledge workspace structure.
- No raw data or source materials were imported.
- Added operating rules, source-system map, verification-source registry, and note templates.

## 2026-06-17 | ingest | Telegram group chat snapshot

- Ingested a redacted local Telegram Desktop export path as a date-stamped source snapshot.
- Initially copied original export files into the snapshot; later compressed them into `original-export.tar.zst` and removed the expanded copy.
- Generated lossless compact and zstd-compressed JSON derivatives under `derived/`.
- Added source and ingestion records; no chat content was promoted into `wiki/`.

## 2026-06-17 | synthesize | Telegram group chat mainline

- Added `system/scripts/analyze-telegram-snapshot.py` for reproducible aggregate metrics.
- Generated aggregate analysis artifacts under the Telegram snapshot `derived/analysis/` directory.
- Created `wiki/topics/telegram-gaibang-mainline.md` with a first-pass long-term mainline and numeric behavior portraits.

## 2026-06-17 | storage | Compress Telegram snapshot

- Created `original-export.tar.zst` for the Telegram snapshot and verified it by extraction plus `diff -qr`.
- Removed the expanded `original/` copy from the gbwiki snapshot.
- Removed temporary `derived/result.compact.json`; retained `derived/result.compact.json.zst` and updated the analysis script to read `.zst` directly.

## 2026-06-17 | synthesize | Telegram group chat game Top5

- Added `system/scripts/analyze-telegram-games.py` for reproducible game mention ranking from compressed Telegram JSON.
- Fixed English game alias matching to use ASCII boundaries so names adjacent to Chinese text or punctuation are counted.
- Excluded platform/noise terms such as `switch`, `steam`, `ps4/ps5`, `xbox`, `ns`, and `lol` from game ranking while preserving them in a separate artifact.
- Created `wiki/topics/telegram-gaibang-games-top5.md` with source paths, method, Top5 ranking, and data-usability notes.

## 2026-06-17 | maintenance | Shared wiki depersonalization

- Removed single-maintainer naming from system instructions, source maps, and Telegram records.
- Replaced local machine import paths with redacted import-path wording while preserving restorable archive references.
- Left source-derived chat tokens unchanged because they are evidence artifacts, not system ownership metadata.

## 2026-06-17 | synthesize | Telegram group chat social topology

- Added `system/scripts/analyze-telegram-topology.py` to generate reproducible participant-node, pair-edge, and membership-event metrics.
- Generated topology artifacts under the Telegram snapshot `derived/analysis/topology/` directory.
- Created `wiki/topics/telegram-gaibang-social-topology.md` with a source-backed relationship topology synthesis and explicit evidence-strength caveats.
