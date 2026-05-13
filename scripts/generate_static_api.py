#!/usr/bin/env python3
"""
Generate a static REST-ish JSON API from json_data/, deployable to GitHub Pages.

Output layout under docs/api/v1/:
  topics                     → list of topics + counts (index)
  topics/<slug>              → single topic file (all questions)
  questions/<id>             → single question lookup
  questions/by-difficulty/<difficulty>  → flat list of questions at that difficulty
  questions/by-tag/<tag>     → flat list of questions matching the tag
  random                     → randomly sampled question (5 picks rotated by hour)

Consumers fetch the static JSON over HTTPS — no server runtime needed.

Usage:
  python3 scripts/generate_static_api.py             # generate
  python3 scripts/generate_static_api.py --out custom/path/
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
JSON_DIR = ROOT / "json_data"
DEFAULT_OUT = ROOT / "docs" / "api" / "v1"


def load_topics() -> list[tuple[str, str, dict[str, Any]]]:
    """Return list of (category, slug, data)."""
    out: list[tuple[str, str, dict[str, Any]]] = []
    for cat in ("flutter", "oop"):
        sub = JSON_DIR / cat
        if not sub.exists():
            continue
        for f in sorted(sub.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            out.append((cat, f.stem, data))
    for stem in ("dsa", "git"):
        f = JSON_DIR / f"{stem}.json"
        if f.exists():
            data = json.loads(f.read_text(encoding="utf-8"))
            out.append(("misc", stem, data))
    return out


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)

    out = args.out
    if out.exists():
        # Clean previous run to avoid stale files.
        for p in out.rglob("*"):
            if p.is_file():
                p.unlink()

    topics = load_topics()
    if not topics:
        sys.stderr.write("no topics found under json_data/. Run scripts/sync_md_json.py --write first.\n")
        return 2

    # --- topics index ---
    by_difficulty: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_tag: dict[str, list[dict[str, Any]]] = defaultdict(list)
    all_questions: list[dict[str, Any]] = []

    topic_index: list[dict[str, Any]] = []
    for cat, slug, data in topics:
        questions = data.get("questions", [])
        diff_counts: dict[str, int] = defaultdict(int)
        for q in questions:
            diff_counts[q.get("difficulty", "unknown")] += 1
            by_difficulty[q.get("difficulty", "unknown")].append({**q, "topic_slug": slug, "category": cat})
            for tag in q.get("tags", []):
                by_tag[tag].append({**q, "topic_slug": slug, "category": cat})
            all_questions.append({**q, "topic_slug": slug, "category": cat})
            write_json(out / "questions" / f"{q['id']}.json", {**q, "topic_slug": slug, "category": cat})

        topic_index.append({
            "slug": slug,
            "category": cat,
            "topic": data.get("topic"),
            "description": data.get("description"),
            "question_count": len(questions),
            "by_difficulty": dict(diff_counts),
            "last_updated": data.get("last_updated"),
            "flutter_version_target": data.get("flutter_version_target"),
            "href": f"topics/{slug}.json",
        })
        write_json(out / "topics" / f"{slug}.json", data)

    write_json(out / "topics.json", {
        "version": "v1",
        "count": len(topic_index),
        "topics": sorted(topic_index, key=lambda t: (t["category"], t["slug"])),
    })

    # --- by difficulty / by tag ---
    for diff, qs in by_difficulty.items():
        write_json(out / "questions" / "by-difficulty" / f"{diff}.json", {
            "difficulty": diff,
            "count": len(qs),
            "questions": [{"id": q["id"], "topic_slug": q["topic_slug"], "question": q["question"]} for q in qs],
        })
    for tag, qs in by_tag.items():
        write_json(out / "questions" / "by-tag" / f"{tag}.json", {
            "tag": tag,
            "count": len(qs),
            "questions": [{"id": q["id"], "topic_slug": q["topic_slug"], "question": q["question"]} for q in qs],
        })

    # --- random samples (5 deterministic rotations) ---
    rng = random.Random(42)
    rotations = []
    for i in range(5):
        rng2 = random.Random(rng.random())
        rotations.append(rng2.choice(all_questions))
    write_json(out / "random.json", {"rotations": rotations})

    # --- stats ---
    write_json(out / "stats.json", {
        "total_questions": len(all_questions),
        "by_difficulty": {k: len(v) for k, v in by_difficulty.items()},
        "topic_count": len(topic_index),
        "tag_count": len(by_tag),
    })

    print(f"wrote {len(topic_index)} topics, {len(all_questions)} questions to {out.relative_to(ROOT)}")
    print(f"  by-difficulty buckets: {sorted(by_difficulty.keys())}")
    print(f"  by-tag buckets: {len(by_tag)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
