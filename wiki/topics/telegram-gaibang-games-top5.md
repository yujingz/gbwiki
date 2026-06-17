---
type: wiki-page
status: active
topics:
  - telegram
  - games
  - long-running-chat-analysis
entities:
  - 丐帮官员频道
sources:
  - sources/records/source-records/telegram-gaibang-officials-channel.md
  - sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/games/
  - system/scripts/analyze-telegram-games.py
last_updated: 2026-06-17
last_reviewed: 2026-06-17
confidence: medium
---

# 丐帮官员频道：游戏 Top5 和数据可用性验证

## Current Understanding

按聊天证据强度看，丐帮这些年最常被讨论、最像“大家实际在玩/关注”的游戏 Top5 是：

1. `Dota 2 / Dota`
2. `World of Warcraft`
3. `Overwatch`
4. `The Legend of Zelda`
5. `Pokemon`

这里的“最喜欢玩”不能被严格理解成每个人的真实偏好投票。聊天记录能验证的是：这些游戏在多年里被多人反复提到，并且常和游戏上下文词一起出现。第 5 名 `Pokemon` 和第 6 名 `Diablo` 非常接近；如果未来把“玩/开黑/副本/装备”等上下文权重加大，`Diablo` 可能会超过 `Pokemon`。

## Data Usability Verification

这次分析直接读取压缩 JSON，不需要恢复 90M 的展开原始目录。

| check | result |
| --- | --- |
| compressed JSON readable | `derived/result.compact.json.zst` 可直接被 `system/scripts/analyze-telegram-games.py` 读取 |
| message records scanned | `275016` |
| text-bearing messages | `259919` |
| date range scanned | `2016-04-29T01:21:57` to `2026-06-17T10:26:11` |
| original archive state | `original-export.tar.zst` 保留，可无损恢复 Telegram Desktop export copy |
| raw quotes in wiki | none |

发现并修复的问题：

- 英文游戏名的词边界一开始过严，会漏掉紧挨中文或标点的 `dota` 等 alias；已改成 ASCII 边界。
- `switch`、`steam`、`ps4/ps5`、`xbox`、`ns` 是平台/渠道词，不应该进入游戏 Top5；现在单独输出到 `game-rejected-platform-noise.json`。
- `lol` 在这个聊天里更像笑声/语气词，未当作《League of Legends》证据。

## Ranking Method

脚本使用 alias map 做确定性匹配，然后计算：

```text
evidence_score = message_count
  + participant_count * 5
  + active_year_count * 20
  + play_context_messages * 0.25
```

这个分数偏向长期、多成员、反复出现的游戏。它衡量“聊天证据强度”，不是心理偏好、游戏时长或真实消费金额。

## Top5 Evidence

| rank | game | score | game messages | mentions | participants | active years | play-context messages | strongest years | main aliases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | `Dota 2 / Dota` | `1077.5` | `780` | `810` | `15` | `10` | `90` | `2017`, `2016`, `2018` | `dota`, `dota2`, `dota 2` |
| 2 | `World of Warcraft` | `1024.25` | `689` | `758` | `16` | `11` | `141` | `2016`, `2017`, `2018` | `wow`, `魔兽`, `魔兽世界` |
| 3 | `Overwatch` | `356.5` | `92` | `120` | `12` | `10` | `18` | `2016`, `2017`, `2018` | `守望`, `overwatch`, `守望先锋` |
| 4 | `The Legend of Zelda` | `348.75` | `88` | `89` | `11` | `10` | `23` | `2018`, `2017`, `2023` | `塞尔达`, `zelda` |
| 5 | `Pokemon` | `289.0` | `76` | `83` | `10` | `8` | `12` | `2018`, `2016`, `2019` | `pokemon`, `pokémon`, `宝可梦`, `口袋妖怪` |

Near miss:

| rank | game | score | game messages | mentions | participants | active years | play-context messages | note |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 6 | `Diablo` | `288.5` | `69` | `73` | `11` | `8` | `18` | 与 `Pokemon` 只差 `0.5` 分，且游戏上下文更多。 |
| 7 | `Monster Hunter` | `241.75` | `64` | `65` | `7` | `7` | `11` | Switch/主机语境里可能还有未归并信号。 |

## Excluded Non-Game Signals

这些词有检索价值，但不作为游戏排名：

| item | matched messages | mentions | reason |
| --- | ---: | ---: | --- |
| `lol` | `638` | `638` | 在本聊天中主要作为笑声/语气词处理。 |
| `Nintendo Switch` | `299` | `303` | 平台，不是游戏；后续可用于检索与 `Zelda`、`Monster Hunter`、`Pokemon` 相关上下文。 |
| `PlayStation` | `233` | `250` | 平台，不是游戏。 |
| `Steam` | `171` | `174` | 平台/商店，不是游戏。 |
| `Xbox` | `67` | `75` | 平台，不是游戏。 |

## Source Evidence

- Script: `system/scripts/analyze-telegram-games.py`
- Ranking: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/games/game-rankings.json`
- Ranking CSV: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/games/game-rankings.csv`
- Metadata: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/games/game-ranking-metadata.json`
- Alias rules: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/games/game-aliases.json`
- Excluded platform/noise terms: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/games/game-rejected-platform-noise.json`

## Retrieval Notes

- 后续查资料时，优先从 `game-rankings.json` 的 `top_aliases` 建搜索 query。
- 如果要做“确实一起玩过”的版本，应加大 `play_context_messages` 权重，或抽取含 `玩/开黑/副本/排位/roll/boss/dps` 的消息做人工复核包。
- 如果要做年份专题，先看 `top_years`：`Dota` 和 `WoW` 的高峰在 2016-2018；`Diablo` 更偏 2021 后；`Zelda` 的峰值在 2018。

## Related

- `wiki/topics/telegram-gaibang-mainline.md`
- `sources/records/source-records/telegram-gaibang-officials-channel.md`
