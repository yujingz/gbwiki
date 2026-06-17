#!/usr/bin/env python3
"""Generate aggregate, reproducible metrics for a Telegram Desktop JSON export."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


TOPIC_KEYWORDS = {
    "tech_ai_product": [
        "ai", "gpt", "chatgpt", "claude", "openai", "llm", "agent", "api",
        "python", "javascript", "github", "linux", "mac", "app", "代码",
        "编程", "机器人", "模型", "算法", "数据", "系统", "开源", "工具",
        "产品", "软件",
    ],
    "work_startup_business": [
        "工作", "公司", "创业", "融资", "客户", "项目", "需求", "老板",
        "面试", "offer", "工资", "商业", "销售", "市场", "团队", "刻行",
        "coscene", "挣钱", "赚钱",
    ],
    "daily_life_relationships": [
        "吃", "饭", "喝", "家", "房", "车", "结婚", "对象", "女朋友",
        "男朋友", "朋友", "孩子", "睡", "病", "医院", "跑步", "健身",
        "生活", "爸", "妈",
    ],
    "travel_city_mobility": [
        "旅游", "旅行", "日本", "美国", "上海", "北京", "杭州", "深圳",
        "广州", "香港", "纽约", "东京", "机票", "酒店", "签证", "机场",
        "火车", "高铁", "出差", "出去",
    ],
    "games_entertainment": [
        "游戏", "steam", "switch", "ps5", "电影", "音乐", "动漫", "演唱会",
        "直播", "b站", "bilibili", "玩", "剧",
    ],
    "learning_research": [
        "论文", "学习", "书", "研究", "课程", "学校", "大学", "博士",
        "硕士", "考试", "知识", "数学", "物理", "英语",
    ],
    "news_society": [
        "新闻", "政治", "经济", "政策", "疫情", "新冠", "美国", "中国",
        "社会", "国家", "政府", "战争",
    ],
}

COORDINATION_KEYWORDS = [
    "几点", "什么时候", "今天", "明天", "周末", "约", "安排", "计划",
    "会议", "地址", "哪里", "一起", "来不来", "报名", "出发", "到哪",
]

LAUGH_RE = re.compile(r"(哈{2,}|笑|lol|233|草|绷|xswl)", re.IGNORECASE)
QUESTION_RE = re.compile(r"[?？]")
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+#.-]{1,}|[\u4e00-\u9fff]{2,}")


def text_to_plain(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text", "")))
        return "".join(parts)
    return ""


def parse_time(message: dict) -> datetime:
    raw = message.get("date")
    if not raw:
        return datetime.fromtimestamp(int(message["date_unixtime"]))
    return datetime.fromisoformat(raw)


def read_json(path: Path) -> dict:
    if path.name.endswith(".zst"):
        result = subprocess.run(
            ["zstd", "-dc", str(path)],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        return json.loads(result.stdout)
    return json.loads(path.read_text(encoding="utf-8"))


def scale(values: dict[str, float]) -> dict[str, float]:
    if not values:
        return {}
    lo = min(values.values())
    hi = max(values.values())
    if math.isclose(lo, hi):
        return {key: 50.0 for key in values}
    return {key: round((value - lo) * 100.0 / (hi - lo), 1) for key, value in values.items()}


def entropy(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total <= 0:
        return 0.0
    return -sum((count / total) * math.log(count / total, 2) for count in counter.values() if count)


def message_has_any(text: str, keywords: list[str]) -> bool:
    lower = text.lower()
    return any(keyword.lower() in lower for keyword in keywords)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--min-messages", type=int, default=500)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    data = read_json(args.input)
    messages = data["messages"]
    by_id = {message["id"]: message for message in messages}

    participants: dict[str, dict] = defaultdict(lambda: {
        "names": Counter(),
        "messages": 0,
        "chars": 0,
        "long_messages": 0,
        "active_months": set(),
        "active_years": set(),
        "first_date": None,
        "last_date": None,
        "questions": 0,
        "laughs": 0,
        "links": 0,
        "code_entities": 0,
        "bot_commands": 0,
        "media": 0,
        "stickers": 0,
        "files": 0,
        "forwards": 0,
        "edits": 0,
        "replies_sent": 0,
        "replies_received": 0,
        "thread_starts_6h": 0,
        "day_starts": 0,
        "topic_hits": Counter(),
        "coordination_hits": 0,
        "tokens": Counter(),
    })

    yearly = defaultdict(lambda: {
        "messages": 0,
        "active_users": set(),
        "chars": 0,
        "topic_hits": Counter(),
        "tokens": Counter(),
        "links": 0,
        "media": 0,
    })

    sorted_messages = sorted(messages, key=lambda item: int(item.get("date_unixtime", 0)))
    previous_message_time: datetime | None = None
    current_day = None

    for message in sorted_messages:
        if message.get("type") != "message":
            continue
        sender = str(message.get("from_id", "unknown"))
        text = text_to_plain(message.get("text"))
        when = parse_time(message)
        year = str(when.year)
        month = when.strftime("%Y-%m")
        day = when.date().isoformat()

        stats = participants[sender]
        display_name = message.get("from") or "unknown"
        stats["names"][str(display_name)] += 1
        stats["messages"] += 1
        stats["chars"] += len(text)
        stats["long_messages"] += int(len(text) >= 100)
        stats["active_months"].add(month)
        stats["active_years"].add(year)
        stats["first_date"] = min(stats["first_date"], when.isoformat()) if stats["first_date"] else when.isoformat()
        stats["last_date"] = max(stats["last_date"], when.isoformat()) if stats["last_date"] else when.isoformat()
        stats["questions"] += int(bool(QUESTION_RE.search(text)))
        stats["laughs"] += int(bool(LAUGH_RE.search(text)))
        stats["media"] += int(bool(message.get("media_type") or message.get("photo") or message.get("file")))
        stats["stickers"] += int(message.get("media_type") == "sticker")
        stats["files"] += int(bool(message.get("file")))
        stats["forwards"] += int(bool(message.get("forwarded_from") or message.get("forwarded_from_id")))
        stats["edits"] += int(bool(message.get("edited") or message.get("edited_unixtime")))
        stats["replies_sent"] += int("reply_to_message_id" in message)

        if previous_message_time is None or (when - previous_message_time).total_seconds() >= 6 * 3600:
            stats["thread_starts_6h"] += 1
        if current_day != day:
            stats["day_starts"] += 1
            current_day = day
        previous_message_time = when

        reply_to = message.get("reply_to_message_id")
        if reply_to in by_id:
            target_sender = str(by_id[reply_to].get("from_id", "unknown"))
            participants[target_sender]["replies_received"] += 1

        message_links = 0
        for entity in message.get("text_entities", []):
            entity_type = entity.get("type")
            if entity_type in {"link", "text_link"}:
                stats["links"] += 1
                message_links += 1
            elif entity_type in {"code", "pre"}:
                stats["code_entities"] += 1
            elif entity_type == "bot_command":
                stats["bot_commands"] += 1

        for topic, keywords in TOPIC_KEYWORDS.items():
            if message_has_any(text, keywords):
                stats["topic_hits"][topic] += 1
                yearly[year]["topic_hits"][topic] += 1
        if message_has_any(text, COORDINATION_KEYWORDS):
            stats["coordination_hits"] += 1

        for token in TOKEN_RE.findall(text.lower()):
            if len(token) >= 2 and not token.isdigit():
                stats["tokens"][token] += 1
                yearly[year]["tokens"][token] += 1

        yearly[year]["messages"] += 1
        yearly[year]["active_users"].add(sender)
        yearly[year]["chars"] += len(text)
        yearly[year]["links"] += message_links
        yearly[year]["media"] += int(bool(message.get("media_type") or message.get("photo") or message.get("file")))

    active_ids = [
        sender for sender, stats in participants.items()
        if stats["messages"] >= args.min_messages and not sender.startswith("channel")
    ]

    raw_metrics = {}
    for sender in active_ids:
        stats = participants[sender]
        msg_count = stats["messages"]
        topic_entropy = entropy(stats["topic_hits"])
        raw_metrics[sender] = {
            "log_messages": math.log1p(msg_count),
            "active_months": len(stats["active_months"]),
            "thread_starts_6h": math.log1p(stats["thread_starts_6h"]),
            "avg_chars": stats["chars"] / msg_count,
            "long_ratio": stats["long_messages"] / msg_count,
            "question_ratio": stats["questions"] / msg_count,
            "link_ratio": stats["links"] / msg_count,
            "topic_entropy": topic_entropy,
            "tech_ratio": stats["topic_hits"]["tech_ai_product"] / msg_count,
            "code_tool_ratio": (stats["code_entities"] + stats["bot_commands"]) / msg_count,
            "coordination_ratio": stats["coordination_hits"] / msg_count,
            "work_ratio": stats["topic_hits"]["work_startup_business"] / msg_count,
            "social_signal_ratio": (stats["laughs"] + stats["stickers"]) / msg_count,
            "reply_ratio": stats["replies_sent"] / msg_count,
        }

    scaled = {metric: scale({sender: values[metric] for sender, values in raw_metrics.items()}) for metric in next(iter(raw_metrics.values())).keys()}

    rows = []
    for sender in active_ids:
        stats = participants[sender]
        msg_count = stats["messages"]
        top_topics = [topic for topic, _ in stats["topic_hits"].most_common(3)]
        scores = {
            "参与度": scaled["log_messages"][sender],
            "持续性": scaled["active_months"][sender],
            "发起性": scaled["thread_starts_6h"][sender],
            "信息密度": round((scaled["avg_chars"][sender] + scaled["long_ratio"][sender]) / 2, 1),
            "探索性": round((scaled["question_ratio"][sender] + scaled["link_ratio"][sender] + scaled["topic_entropy"][sender]) / 3, 1),
            "技术工具倾向": round((scaled["tech_ratio"][sender] + scaled["code_tool_ratio"][sender]) / 2, 1),
            "组织推进倾向": round((scaled["coordination_ratio"][sender] + scaled["work_ratio"][sender]) / 2, 1),
            "社交调节倾向": scaled["social_signal_ratio"][sender],
            "响应协作倾向": scaled["reply_ratio"][sender],
        }
        rows.append({
            "from_id": sender,
            "name": stats["names"].most_common(1)[0][0],
            "messages": msg_count,
            "first_date": stats["first_date"][:10],
            "last_date": stats["last_date"][:10],
            "active_months": len(stats["active_months"]),
            "avg_chars": round(stats["chars"] / msg_count, 1),
            "questions": stats["questions"],
            "links": stats["links"],
            "media": stats["media"],
            "thread_starts_6h": stats["thread_starts_6h"],
            "replies_sent": stats["replies_sent"],
            "replies_received": stats["replies_received"],
            "top_topics": ";".join(top_topics),
            "scores": scores,
            "topic_hits": dict(stats["topic_hits"]),
        })

    rows.sort(key=lambda row: row["messages"], reverse=True)

    yearly_rows = []
    for year in sorted(yearly):
        data = yearly[year]
        yearly_rows.append({
            "year": year,
            "messages": data["messages"],
            "active_users": len(data["active_users"]),
            "chars": data["chars"],
            "top_topics": data["topic_hits"].most_common(5),
            "top_tokens": data["tokens"].most_common(30),
        })

    (args.outdir / "participant-metrics.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.outdir / "yearly-topics.json").write_text(
        json.dumps(yearly_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.outdir / "topic-keywords.json").write_text(
        json.dumps(TOPIC_KEYWORDS, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with (args.outdir / "participant-scores.csv").open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "from_id", "name", "messages", "active_months", "avg_chars",
            "top_topics", "参与度", "持续性", "发起性", "信息密度", "探索性",
            "技术工具倾向", "组织推进倾向", "社交调节倾向", "响应协作倾向",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                **{key: row[key] for key in fieldnames if key in row},
                **row["scores"],
            })

    summary = {
        "chat_name": data.get("name"),
        "message_count": len([m for m in messages if m.get("type") == "message"]),
        "service_count": len([m for m in messages if m.get("type") == "service"]),
        "active_participant_count_min_messages": len(active_ids),
        "min_messages": args.min_messages,
        "first_date": sorted_messages[0].get("date"),
        "last_date": sorted_messages[-1].get("date"),
        "topics": TOPIC_KEYWORDS,
    }
    (args.outdir / "analysis-metadata.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
