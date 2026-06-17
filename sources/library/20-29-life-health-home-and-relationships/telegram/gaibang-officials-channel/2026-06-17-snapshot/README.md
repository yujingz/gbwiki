---
type: source-snapshot
status: active
created: 2026-06-17
source_system: Telegram
source_name: 丐帮官员频道
ingestion_mode: snapshot
sensitivity: personal-private
---

# Telegram Snapshot 2026-06-17

This directory preserves a point-in-time Telegram Desktop export.

## Source

- Original export path: `/Users/yujing/Downloads/Telegram Desktop/ChatExport_2026-06-17 (1)`
- Exported chat name: `丐帮官员频道`
- Exported chat type: `private_supergroup`
- Telegram chat id in export: `1077197275`
- Message count in export: `275120`
- Export date range: `2016-04-29T01:21:51` to `2026-06-17T10:26:11`

## Files

- `original-export.tar.zst`: zstd-compressed tar archive of the Telegram Desktop export copy. The expanded `original/` directory is intentionally not retained.
- `derived/result.compact.json.zst`: zstd-compressed compact JSON.
- `derived/analysis/`: aggregate analysis artifacts generated from the compressed compact JSON.
- `derived/analysis/games/`: game mention rankings, alias rules, and excluded platform/noise terms.
- `derived/export-metadata.json`: small metadata summary extracted from the export.
- `checksums.sha256`: SHA-256 checksums for source and derived files, excluding macOS `.DS_Store` metadata.

## Integrity Checks

- Source `result.json` SHA-256 from the imported Telegram export:
  `7f2652531decefbb3c26910ae5eb332220f030b312f4e0bb855fcbd386a48f87`
- Canonical JSON hash for original and compact JSON:
  `ca2a3aa4f2fe8fdff158a19fb5c3b75c66cdd844f377d5f91a6d61f971fefbb0`
- `original-export.tar.zst` was extracted to a temporary directory and verified with `diff -qr` against the expanded `original/` copy before the expanded copy was removed.
- `derived/result.compact.json.zst` passed `zstd -t`.
- Decompressed `derived/result.compact.json.zst` was verified byte-for-byte against `derived/result.compact.json` before the expanded compact JSON was removed.

## Restore

Restore the full Telegram Desktop export copy:

```sh
zstd -dc original-export.tar.zst | tar -xf -
```

Restore compact JSON when direct JSON tooling needs an expanded file:

```sh
zstd -dc derived/result.compact.json.zst > derived/result.compact.json
```

## Notes

- This is source evidence, not synthesized wiki understanding.
- No raw chat messages are quoted in the current wiki synthesis.
- Treat this material as private to YZ and the group context unless YZ explicitly says otherwise.
