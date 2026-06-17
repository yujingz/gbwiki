#!/usr/bin/env python3
"""Generate participant topology metrics for a Telegram Desktop JSON export."""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path


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


def parse_time(message: dict) -> datetime:
    raw = message.get("date")
    if raw:
        return datetime.fromisoformat(raw)
    return datetime.fromtimestamp(int(message["date_unixtime"]))


def canonical_pair(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def scale(value: float, maximum: float) -> float:
    if maximum <= 0:
        return 0.0
    return value / maximum


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--min-messages", type=int, default=500)
    parser.add_argument("--turn-gap-minutes", type=int, default=10)
    parser.add_argument("--session-gap-minutes", type=int, default=360)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    data = read_json(args.input)
    messages = sorted(data["messages"], key=lambda item: int(item.get("date_unixtime", 0)))
    by_id = {message["id"]: message for message in messages}

    participants: dict[str, dict] = defaultdict(lambda: {
        "names": Counter(),
        "messages": 0,
        "chars": 0,
        "active_months": set(),
        "first_date": None,
        "last_date": None,
        "replies_sent": 0,
        "replies_received": 0,
        "turns_after_others": 0,
        "turns_before_others": 0,
        "co_sessions": 0,
    })

    for message in messages:
        if message.get("type") != "message":
            continue
        sender = str(message.get("from_id", "unknown"))
        if sender.startswith("channel"):
            continue
        when = parse_time(message)
        stats = participants[sender]
        stats["names"][str(message.get("from") or "unknown")] += 1
        stats["messages"] += 1
        stats["chars"] += len(text_to_plain(message.get("text")))
        stats["active_months"].add(when.strftime("%Y-%m"))
        iso_date = when.date().isoformat()
        stats["first_date"] = min(stats["first_date"], iso_date) if stats["first_date"] else iso_date
        stats["last_date"] = max(stats["last_date"], iso_date) if stats["last_date"] else iso_date

    active_ids = {
        sender
        for sender, stats in participants.items()
        if stats["messages"] >= args.min_messages
    }

    names = {
        sender: participants[sender]["names"].most_common(1)[0][0]
        for sender in active_ids
    }
    ids_by_name: dict[str, list[str]] = defaultdict(list)
    for sender, name in names.items():
        ids_by_name[name].append(sender)

    reply_edges: Counter[tuple[str, str]] = Counter()
    turn_edges: Counter[tuple[str, str]] = Counter()
    co_session_edges: Counter[tuple[str, str]] = Counter()

    previous_message: dict | None = None
    previous_time: datetime | None = None
    current_session: Counter[str] = Counter()
    session_count = 0
    multi_participant_session_count = 0
    turn_gap_seconds = args.turn_gap_minutes * 60
    session_gap_seconds = args.session_gap_minutes * 60

    def flush_session() -> None:
        nonlocal multi_participant_session_count
        members = [sender for sender, count in current_session.items() if sender in active_ids and count > 0]
        if len(members) < 2:
            return
        multi_participant_session_count += 1
        for left, right in combinations(sorted(members), 2):
            co_session_edges[(left, right)] += 1
            participants[left]["co_sessions"] += 1
            participants[right]["co_sessions"] += 1

    for message in messages:
        if message.get("type") != "message":
            continue
        sender = str(message.get("from_id", "unknown"))
        when = parse_time(message)

        if previous_time is None or (when - previous_time).total_seconds() >= session_gap_seconds:
            if current_session:
                flush_session()
            current_session = Counter()
            session_count += 1

        if sender in active_ids:
            current_session[sender] += 1

        reply_to = message.get("reply_to_message_id")
        target = by_id.get(reply_to)
        if target and target.get("type") == "message":
            target_sender = str(target.get("from_id", "unknown"))
            if sender in active_ids and target_sender in active_ids and sender != target_sender:
                reply_edges[(sender, target_sender)] += 1
                participants[sender]["replies_sent"] += 1
                participants[target_sender]["replies_received"] += 1

        if previous_message is not None and previous_time is not None:
            previous_sender = str(previous_message.get("from_id", "unknown"))
            gap = (when - previous_time).total_seconds()
            if (
                gap <= turn_gap_seconds
                and previous_sender in active_ids
                and sender in active_ids
                and previous_sender != sender
            ):
                turn_edges[(previous_sender, sender)] += 1
                participants[previous_sender]["turns_before_others"] += 1
                participants[sender]["turns_after_others"] += 1

        previous_message = message
        previous_time = when

    if current_session:
        flush_session()

    membership_events = []
    for message in messages:
        if message.get("type") != "service":
            continue
        action = message.get("action")
        actor_id = str(message.get("actor_id", "unknown"))
        actor_name = str(message.get("actor") or "unknown")
        if action == "create_group":
            for member_name in message.get("members", []):
                member_ids = ids_by_name.get(str(member_name), [])
                membership_events.append({
                    "date": message.get("date", ""),
                    "action": "create_group_member",
                    "actor_id": actor_id,
                    "actor_name": actor_name,
                    "member_id": member_ids[0] if len(member_ids) == 1 else "",
                    "member_name": str(member_name),
                    "mapped": len(member_ids) == 1,
                })
        elif action in {"invite_members", "invite_to_group_call"}:
            for member_name in message.get("members", []):
                if member_name is None:
                    continue
                member_ids = ids_by_name.get(str(member_name), [])
                membership_events.append({
                    "date": message.get("date", ""),
                    "action": str(action),
                    "actor_id": actor_id,
                    "actor_name": actor_name,
                    "member_id": member_ids[0] if len(member_ids) == 1 else "",
                    "member_name": str(member_name),
                    "mapped": len(member_ids) == 1,
                })
        elif action == "join_group_by_link":
            membership_events.append({
                "date": message.get("date", ""),
                "action": "join_group_by_link",
                "actor_id": actor_id,
                "actor_name": actor_name,
                "member_id": actor_id if actor_id in active_ids else "",
                "member_name": actor_name,
                "mapped": actor_id in active_ids,
            })

    pair_stats: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: {
        "reply_count": 0,
        "turn_count": 0,
        "co_session_count": 0,
        "left_to_right_replies": 0,
        "right_to_left_replies": 0,
        "left_to_right_turns": 0,
        "right_to_left_turns": 0,
    })

    for (sender, target), count in reply_edges.items():
        left, right = canonical_pair(sender, target)
        stats = pair_stats[(left, right)]
        stats["reply_count"] += count
        if sender == left:
            stats["left_to_right_replies"] += count
        else:
            stats["right_to_left_replies"] += count

    for (sender, target), count in turn_edges.items():
        left, right = canonical_pair(sender, target)
        stats = pair_stats[(left, right)]
        stats["turn_count"] += count
        if sender == left:
            stats["left_to_right_turns"] += count
        else:
            stats["right_to_left_turns"] += count

    for pair, count in co_session_edges.items():
        pair_stats[pair]["co_session_count"] += count

    max_reply = max((stats["reply_count"] for stats in pair_stats.values()), default=0)
    max_turn = max((stats["turn_count"] for stats in pair_stats.values()), default=0)
    max_co_session = max((stats["co_session_count"] for stats in pair_stats.values()), default=0)

    edge_rows = []
    node_strength: Counter[str] = Counter()
    for (left, right), stats in pair_stats.items():
        relationship_score = round(100 * (
            0.55 * scale(stats["reply_count"], max_reply)
            + 0.35 * scale(stats["turn_count"], max_turn)
            + 0.10 * scale(stats["co_session_count"], max_co_session)
        ), 1)
        reply_total = stats["left_to_right_replies"] + stats["right_to_left_replies"]
        reply_reciprocity = 0.0
        if reply_total > 0:
            reply_reciprocity = round(
                2 * min(stats["left_to_right_replies"], stats["right_to_left_replies"]) / reply_total,
                3,
            )
        row = {
            "left_id": left,
            "left_name": names[left],
            "right_id": right,
            "right_name": names[right],
            "relationship_score": relationship_score,
            "reply_count": int(stats["reply_count"]),
            "turn_count": int(stats["turn_count"]),
            "co_session_count": int(stats["co_session_count"]),
            "reply_reciprocity": reply_reciprocity,
            "left_to_right_replies": int(stats["left_to_right_replies"]),
            "right_to_left_replies": int(stats["right_to_left_replies"]),
            "left_to_right_turns": int(stats["left_to_right_turns"]),
            "right_to_left_turns": int(stats["right_to_left_turns"]),
        }
        edge_rows.append(row)
        node_strength[left] += relationship_score
        node_strength[right] += relationship_score

    edge_rows.sort(key=lambda item: (-item["relationship_score"], -item["reply_count"], item["left_name"], item["right_name"]))

    node_rows = []
    for sender in sorted(active_ids, key=lambda item: (-participants[item]["messages"], names[item])):
        stats = participants[sender]
        strongest_ties = [
            (row["right_name"] if row["left_id"] == sender else row["left_name"])
            for row in edge_rows
            if row["left_id"] == sender or row["right_id"] == sender
        ][:5]
        node_rows.append({
            "from_id": sender,
            "name": names[sender],
            "messages": stats["messages"],
            "active_months": len(stats["active_months"]),
            "first_date": stats["first_date"],
            "last_date": stats["last_date"],
            "avg_chars": round(stats["chars"] / stats["messages"], 1),
            "replies_sent": stats["replies_sent"],
            "replies_received": stats["replies_received"],
            "turns_after_others": stats["turns_after_others"],
            "turns_before_others": stats["turns_before_others"],
            "co_sessions": stats["co_sessions"],
            "relationship_strength": round(node_strength[sender], 1),
            "strongest_ties": ";".join(strongest_ties),
        })

    topology = {
        "metadata": {
            "chat_name": data.get("name"),
            "message_count": sum(1 for message in messages if message.get("type") == "message"),
            "active_participant_min_messages": args.min_messages,
            "active_participant_count": len(active_ids),
            "turn_gap_minutes": args.turn_gap_minutes,
            "session_gap_minutes": args.session_gap_minutes,
            "session_count": session_count,
            "multi_participant_session_count": multi_participant_session_count,
            "relationship_score_formula": "100 * (0.55 * reply/max_reply + 0.35 * turn/max_turn + 0.10 * co_session/max_co_session)",
            "relationship_score_note": "Reply is strongest evidence; short-turn adjacency is medium evidence; same-session co-presence is weak evidence.",
        },
        "nodes": node_rows,
        "top_edges": edge_rows[:40],
        "membership_events": membership_events,
    }

    (args.outdir / "topology-summary.json").write_text(
        json.dumps(topology, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(
        args.outdir / "topology-nodes.csv",
        node_rows,
        [
            "from_id", "name", "messages", "active_months", "first_date", "last_date",
            "avg_chars", "replies_sent", "replies_received", "turns_after_others",
            "turns_before_others", "co_sessions", "relationship_strength", "strongest_ties",
        ],
    )
    write_csv(
        args.outdir / "topology-edges.csv",
        edge_rows,
        [
            "left_id", "left_name", "right_id", "right_name", "relationship_score",
            "reply_count", "turn_count", "co_session_count", "reply_reciprocity",
            "left_to_right_replies", "right_to_left_replies",
            "left_to_right_turns", "right_to_left_turns",
        ],
    )
    write_csv(
        args.outdir / "topology-membership-events.csv",
        membership_events,
        ["date", "action", "actor_id", "actor_name", "member_id", "member_name", "mapped"],
    )


if __name__ == "__main__":
    main()
