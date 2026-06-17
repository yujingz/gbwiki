---
type: wiki-page
status: active
topics:
  - telegram
  - friendship
  - social-topology
  - long-running-chat-analysis
entities:
  - 丐帮官员频道
sources:
  - sources/records/source-records/telegram-gaibang-officials-channel.md
  - sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/topology/
  - system/scripts/analyze-telegram-topology.py
last_updated: 2026-06-17
last_reviewed: 2026-06-17
confidence: medium
---

# 丐帮官员频道：群友关系拓扑

## Current Understanding

按 2016-04-29 到 2026-06-17 的 Telegram 快照看，这个群不是一个单中心星型网络，而是一个“五人高密度核心 + 一层稳定内圈 + 若干阶段性节点”的长期朋友网络。

最稳的结构判断是：

1. `fry.xzb`、`Xiaotian Li`、`Yifan Cai`、`Zhe Cheng`、`Yunxing Dai` 构成长期对话核心。前 11 条最强关系边里有 10 条覆盖这个五人核心内部的完整网状连接。
2. `Xiaotian Li` 是当前图里的最高连接节点：关系强度总分最高，且与 `fry.xzb`、`Yunxing Dai`、`Yifan Cai`、`Zhe Cheng` 都有高强度边。
3. `fry.xzb` 是创群和长期发动节点：创群、早期拉入核心成员，并在消息量、持续性和沉寂后重启聊天上都是最高或接近最高。
4. `Yunxing Dai` 是最明显的高互惠桥接节点之一：和 `Xiaotian Li` 的显式 reply 边是全图最高，且 reply 互惠度接近对称。
5. `Shenwei Zhang` 是稳定内圈，不是最高频核心，但 reply/接话强度明显高于纯消息量暗示的存在感。
6. `Yutong Pei` 是后进入的高信息量节点，最强边连向 `Yunxing Dai`、`Xiaotian Li`、`Yifan Cai`，更像阶段性桥接而不是十年连续核心。
7. `Tong Chen`、`Jiaxin Hu` 和几个 `unknown` id 更像阶段性或低频外围节点；其中 `unknown` id 需要先做身份映射，不能强行人格化解读。

这里的“关系强”只表示聊天拓扑里的互动强度，不等于线下亲密度、价值判断或现实关系排序。

## Evidence Strength

这页把证据分三层使用：

| evidence | strength | interpretation |
| --- | --- | --- |
| Telegram service events | high | 创群、邀请、通过链接加入等结构事实。 |
| explicit replies | high | 某人明确回复另一个人的消息，是最强的互动边。 |
| short-turn adjacency | medium | 10 分钟内相邻接话，表示对话流动，但不保证一对一回应。 |
| same-session co-presence | weak | 6 小时内同一段多人会话共现，只能说明同时参与同一段讨论。 |

关系分数公式：

```text
100 * (0.55 * reply/max_reply + 0.35 * turn/max_turn + 0.10 * co_session/max_co_session)
```

这个权重有意偏向显式 reply，避免把“刚好一起水群”过度解释成强关系。

## Membership Topology

| date | structural event | interpretation |
| --- | --- | --- |
| 2016-04-29 | `fry.xzb` 创建群，初始成员包括 `fry.xzb`、`Xiaotian Li`、`Yifan Cai` | 初始三角。 |
| 2016-04-29 | `fry.xzb` 邀请 `Zhe Cheng` | 四人早期核心成型。 |
| 2016-05-25 | `fry.xzb` 邀请 `Yunxing Dai` | 五人长期核心基本成型。 |
| 2017-03-30 | `Xiaotian Li` 多次邀请 `Shenwei Zhang` | 稳定内圈进入。 |
| 2020-08-07 | `fry.xzb` 邀请 `Jiaxin Hu` | 低频长跨度外围节点进入。 |
| 2020-11-20 | `Yutong Pei` 通过链接加入 | 后期高信息量节点进入。 |

中间有 bot、重复邀请、被移除或无法映射姓名的事件；它们暂不作为人际拓扑结论。

## Strongest Edges

| rank | pair | score | reply count | turn count | co-sessions | interpretation |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `fry.xzb` - `Xiaotian Li` | `96.0` | `849` | `18045` | `2188` | 全图最强总边，长期核心轴。 |
| 2 | `Xiaotian Li` - `Yunxing Dai` | `77.7` | `915` | `6941` | `2022` | 全图最强显式 reply 边，互惠度很高。 |
| 3 | `Yifan Cai` - `Xiaotian Li` | `63.0` | `534` | `10756` | `2189` | founding/core 技术和日常线上的强边。 |
| 4 | `Zhe Cheng` - `Xiaotian Li` | `57.8` | `429` | `12375` | `1756` | 高接话流动边。 |
| 5 | `Yifan Cai` - `fry.xzb` | `55.3` | `384` | `11522` | `2159` | founding/core 长期共振边。 |
| 6 | `Zhe Cheng` - `fry.xzb` | `50.5` | `303` | `12394` | `1811` | 高频轻互动核心边。 |
| 7 | `fry.xzb` - `Yunxing Dai` | `48.1` | `479` | `5134` | `2045` | 创群发动节点和桥接节点之间的强边。 |
| 8 | `Yifan Cai` - `Yunxing Dai` | `44.5` | `428` | `4877` | `2033` | 高信息/技术/推进线上的强边。 |
| 9 | `Zhe Cheng` - `Yifan Cai` | `43.8` | `269` | `10042` | `1791` | 核心内高流动边。 |
| 10 | `Shenwei Zhang` - `fry.xzb` | `35.3` | `416` | `2542` | `1172` | 内圈和发动节点的强 reply 边。 |
| 11 | `Zhe Cheng` - `Yunxing Dai` | `28.4` | `201` | `4570` | `1629` | 核心内互惠度很高的中强边。 |
| 12 | `Shenwei Zhang` - `Yunxing Dai` | `25.3` | `290` | `1397` | `1140` | 内圈和桥接节点的强 reply 边。 |
| 13 | `Shenwei Zhang` - `Zhe Cheng` | `25.1` | `266` | `2316` | `1017` | 内圈接话/调节边。 |
| 14 | `Shenwei Zhang` - `Yifan Cai` | `23.3` | `227` | `2140` | `1209` | 内圈和 founding/core 的回复边。 |
| 15 | `Yunxing Dai` - `Yutong Pei` | `22.4` | `279` | `1780` | `473` | 后期高信息量桥接边。 |

## Node Roles

| person | role synthesis | strongest ties |
| --- | --- | --- |
| `Xiaotian Li` | 最高关系中心；高 reply、高接话、高共现，像全图路由节点。 | `fry.xzb`; `Yunxing Dai`; `Yifan Cai`; `Zhe Cheng`; `Shenwei Zhang` |
| `fry.xzb` | 创群者、长期发动机、最高消息量节点；强在启动和维持主干对话。 | `Xiaotian Li`; `Yifan Cai`; `Zhe Cheng`; `Yunxing Dai`; `Shenwei Zhang` |
| `Yifan Cai` | founding core；技术/新东西和日常主线都在核心内扩散。 | `Xiaotian Li`; `fry.xzb`; `Yunxing Dai`; `Zhe Cheng`; `Shenwei Zhang` |
| `Yunxing Dai` | 高互惠桥接节点；reply 和信息密度都强，能把核心与后期节点接起来。 | `Xiaotian Li`; `fry.xzb`; `Yifan Cai`; `Zhe Cheng`; `Shenwei Zhang` |
| `Zhe Cheng` | 核心气氛和接话节点；turn adjacency 很高，显式 reply 中等但互惠性好。 | `Xiaotian Li`; `fry.xzb`; `Yifan Cai`; `Yunxing Dai`; `Shenwei Zhang` |
| `Shenwei Zhang` | 稳定内圈；消息量低于五人核心，但显式 reply 边强，像补位、接话、缓冲节点。 | `fry.xzb`; `Yunxing Dai`; `Zhe Cheng`; `Yifan Cai`; `Xiaotian Li` |
| `Yutong Pei` | 后期高信息量桥；和 `Yunxing Dai`、`Xiaotian Li` 的边最明显。 | `Yunxing Dai`; `Xiaotian Li`; `Yifan Cai`; `Zhe Cheng`; `fry.xzb` |
| `Tong Chen` | 阶段性内圈/外围之间的节点；主要连接五人核心。 | `fry.xzb`; `Xiaotian Li`; `Yifan Cai`; `Zhe Cheng`; `Yunxing Dai` |
| `Jiaxin Hu` | 低频长跨度外围节点；目前证据不足，不做强关系推断。 | `Xiaotian Li`; `Zhe Cheng`; `fry.xzb`; `Yifan Cai`; `Yunxing Dai` |

## Topology Model

用图结构表达，可以把群理解成三层：

```text
founding / dense core:
  fry.xzb
  Xiaotian Li
  Yifan Cai
  Zhe Cheng
  Yunxing Dai

stable inner ring:
  Shenwei Zhang
  Yutong Pei
  Tong Chen

episodic / low-confidence periphery:
  Jiaxin Hu
  user234328816
  user427973593
  user257147853
  user277407287
```

更细一点：

- `fry.xzb` - `Xiaotian Li` 是总互动强度主轴。
- `Xiaotian Li` - `Yunxing Dai` 是显式 reply 主轴。
- `fry.xzb`、`Xiaotian Li`、`Yifan Cai`、`Zhe Cheng` 更像早期高频语言风格的骨架。
- `Yunxing Dai` 把高频核心和高信息量/推进型互动接起来。
- `Shenwei Zhang` 不在最核心五人里，但与核心多点相连，是稳定内圈。
- `Yutong Pei` 的位置不像创群核心，更像 2020 后进入的高信息量桥点。

## Limits

- Telegram export 的 reply 数据只覆盖显式回复；大量早期聊天是自然接话，不能还原真实指向。
- 10 分钟 adjacency 和 6 小时 session 是可复核的工程阈值，不是社会科学定律。
- `unknown` 用户需要身份映射后才能进入 durable person pages。
- 这页不引用原始聊天内容；如果未来需要解释某条边为什么强，应生成人工复核包，而不是把原始私聊内容直接贴进 wiki。

## Source Evidence

- Script: `system/scripts/analyze-telegram-topology.py`
- Topology summary: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/topology/topology-summary.json`
- Node CSV: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/topology/topology-nodes.csv`
- Edge CSV: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/topology/topology-edges.csv`
- Membership event CSV: `sources/library/20-29-life-health-home-and-relationships/telegram/gaibang-officials-channel/2026-06-17-snapshot/derived/analysis/topology/topology-membership-events.csv`
- Source record: `sources/records/source-records/telegram-gaibang-officials-channel.md`

## Related

- `wiki/topics/telegram-gaibang-mainline.md`
- `wiki/topics/telegram-gaibang-games-top5.md`
- `sources/records/source-records/telegram-gaibang-officials-channel.md`
