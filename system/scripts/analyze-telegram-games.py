#!/usr/bin/env python3
"""Analyze game mentions in a Telegram Desktop JSON export."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ASCII_LEFT = r"(?<![A-Za-z0-9_])"
ASCII_RIGHT = r"(?![A-Za-z0-9_])"


GAME_ALIASES = {
    "Dota 2 / Dota": [ASCII_LEFT + r"dota(?:\s*2|2)?" + ASCII_RIGHT],
    "World of Warcraft": [ASCII_LEFT + r"wow" + ASCII_RIGHT, "world of warcraft", "魔兽世界", "魔兽"],
    "Overwatch": ["overwatch", "守望先锋", "守望"],
    "The Legend of Zelda": ["zelda", "塞尔达"],
    "Pokemon": [ASCII_LEFT + r"pok[eé]mon" + ASCII_RIGHT, "宝可梦", "口袋妖怪"],
    "Diablo": [ASCII_LEFT + r"diablo" + ASCII_RIGHT, "暗黑"],
    "Monster Hunter": ["monster hunter", "怪物猎人", "怪猎"],
    "Hearthstone": ["hearthstone", "炉石"],
    "Civilization": [ASCII_LEFT + r"civilization" + ASCII_RIGHT, "文明"],
    "Honor of Kings": ["王者荣耀"],
    "Genshin Impact": [ASCII_LEFT + r"genshin" + ASCII_RIGHT, "原神"],
    "PUBG": [ASCII_LEFT + r"pubg" + ASCII_RIGHT, "绝地求生"],
    "Elden Ring": ["elden ring", "老头环"],
    "Dark Souls": ["dark souls", "黑魂"],
    "StarCraft": [ASCII_LEFT + r"starcraft" + ASCII_RIGHT, "星际"],
    "Sekiro": [ASCII_LEFT + r"sekiro" + ASCII_RIGHT, "只狼"],
    "Cyberpunk 2077": [ASCII_LEFT + r"cyberpunk" + ASCII_RIGHT, "赛博朋克"],
    "Final Fantasy XIV": [ASCII_LEFT + r"ff14" + ASCII_RIGHT, "最终幻想14"],
    "Minecraft": [ASCII_LEFT + r"minecraft" + ASCII_RIGHT, "我的世界"],
    "Counter-Strike": [ASCII_LEFT + r"csgo" + ASCII_RIGHT, ASCII_LEFT + r"cs2" + ASCII_RIGHT, "counter-strike"],
    "Valorant": [ASCII_LEFT + r"valorant" + ASCII_RIGHT, "瓦罗兰特"],
    "Apex Legends": [ASCII_LEFT + r"apex" + ASCII_RIGHT],
}

PLATFORM_OR_NOISE_ALIASES = {
    "Nintendo Switch": [ASCII_LEFT + r"switch" + ASCII_RIGHT, ASCII_LEFT + r"ns" + ASCII_RIGHT],
    "Steam": [ASCII_LEFT + r"steam" + ASCII_RIGHT],
    "PlayStation": [ASCII_LEFT + r"ps[345]" + ASCII_RIGHT, "playstation"],
    "Xbox": [ASCII_LEFT + r"xbox" + ASCII_RIGHT],
    "generic_lol_laugh": [ASCII_LEFT + r"lol" + ASCII_RIGHT],
}

PLAY_CONTEXT = [
    "玩", "开黑", "排位", "匹配", "天梯", "副本", "raid", "boss", "dps",
    "roll", "装备", "卡组", "战队", "赛季", "手柄", "主机", "版本", "更新",
]


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


def compile_aliases(alias_map: dict[str, list[str]]) -> dict[str, list[re.Pattern[str]]]:
    return {
        name: [re.compile(alias, re.IGNORECASE) for alias in aliases]
        for name, aliases in alias_map.items()
    }


def alias_hits(patterns: list[re.Pattern[str]], text: str) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        hits.extend(match.group(0) for match in pattern.finditer(text))
    return hits


def has_play_context(text: str) -> bool:
    lower = text.lower()
    return any(keyword.lower() in lower for keyword in PLAY_CONTEXT)


def parse_year(message: dict) -> str:
    if message.get("date"):
        return message["date"][:4]
    return str(datetime.fromtimestamp(int(message["date_unixtime"])).year)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("outdir", type=Path)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    data = read_json(args.input)
    game_patterns = compile_aliases(GAME_ALIASES)
    platform_patterns = compile_aliases(PLATFORM_OR_NOISE_ALIASES)

    games: dict[str, dict] = defaultdict(lambda: {
        "mention_occurrences": 0,
        "message_ids": set(),
        "years": Counter(),
        "senders": Counter(),
        "aliases": Counter(),
        "play_context_messages": 0,
    })
    rejected = defaultdict(lambda: {
        "mention_occurrences": 0,
        "message_ids": set(),
        "aliases": Counter(),
    })

    total_messages = 0
    text_messages = 0
    first_date = None
    last_date = None

    for message in data["messages"]:
        if message.get("type") != "message":
            continue
        total_messages += 1
        text = text_to_plain(message.get("text"))
        if text:
            text_messages += 1
        date = message.get("date") or ""
        if date:
            first_date = min(first_date, date) if first_date else date
            last_date = max(last_date, date) if last_date else date

        year = parse_year(message)
        sender = str(message.get("from_id", "unknown"))
        message_id = int(message["id"])
        contextual = has_play_context(text)

        for game, patterns in game_patterns.items():
            hits = alias_hits(patterns, text)
            if not hits:
                continue
            stats = games[game]
            stats["mention_occurrences"] += len(hits)
            stats["message_ids"].add(message_id)
            stats["years"][year] += 1
            stats["senders"][sender] += 1
            stats["aliases"].update(hit.lower() for hit in hits)
            stats["play_context_messages"] += int(contextual)

        for item, patterns in platform_patterns.items():
            hits = alias_hits(patterns, text)
            if not hits:
                continue
            stats = rejected[item]
            stats["mention_occurrences"] += len(hits)
            stats["message_ids"].add(message_id)
            stats["aliases"].update(hit.lower() for hit in hits)

    rows = []
    for game, stats in games.items():
        message_count = len(stats["message_ids"])
        participant_count = len(stats["senders"])
        active_year_count = len(stats["years"])
        play_context_messages = stats["play_context_messages"]
        evidence_score = (
            message_count
            + participant_count * 5
            + active_year_count * 20
            + play_context_messages * 0.25
        )
        rows.append({
            "game": game,
            "evidence_score": round(evidence_score, 2),
            "message_count": message_count,
            "mention_occurrences": stats["mention_occurrences"],
            "participant_count": participant_count,
            "active_year_count": active_year_count,
            "play_context_messages": play_context_messages,
            "top_years": stats["years"].most_common(5),
            "top_aliases": stats["aliases"].most_common(8),
            "top_senders": stats["senders"].most_common(5),
        })

    rows.sort(key=lambda row: (row["evidence_score"], row["message_count"]), reverse=True)

    rejected_rows = []
    for item, stats in rejected.items():
        rejected_rows.append({
            "item": item,
            "reason": "platform/noise term; not ranked as a game",
            "message_count": len(stats["message_ids"]),
            "mention_occurrences": stats["mention_occurrences"],
            "top_aliases": stats["aliases"].most_common(8),
        })
    rejected_rows.sort(key=lambda row: row["mention_occurrences"], reverse=True)

    metadata = {
        "chat_name": data.get("name"),
        "input": str(args.input),
        "total_message_count": total_messages,
        "text_message_count": text_messages,
        "first_date": first_date,
        "last_date": last_date,
        "ranking_method": "evidence_score = message_count + participant_count*5 + active_year_count*20 + play_context_messages*0.25",
        "data_quality_notes": [
            "English aliases use ASCII boundaries so names adjacent to Chinese text or punctuation are still counted.",
            "Platform/channel/noise terms are tracked separately and excluded from game ranking.",
            "Ranking measures chat evidence strength, not a private mental-state claim about preference.",
        ],
    }

    (args.outdir / "game-rankings.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.outdir / "game-ranking-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.outdir / "game-rejected-platform-noise.json").write_text(
        json.dumps(rejected_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.outdir / "game-aliases.json").write_text(
        json.dumps({
            "games": GAME_ALIASES,
            "platform_or_noise": PLATFORM_OR_NOISE_ALIASES,
            "play_context": PLAY_CONTEXT,
        }, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with (args.outdir / "game-rankings.csv").open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "game", "evidence_score", "message_count", "mention_occurrences",
            "participant_count", "active_year_count", "play_context_messages",
            "top_years", "top_aliases",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: json.dumps(row[key], ensure_ascii=False) if isinstance(row[key], list) else row[key]
                for key in fieldnames
            })


if __name__ == "__main__":
    main()
