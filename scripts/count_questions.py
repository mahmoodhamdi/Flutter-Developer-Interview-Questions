#!/usr/bin/env python3
"""
Count questions in the repository.
Generates statistics for all topics.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict


def count_questions_in_markdown(file_path: str) -> int:
    """Count numbered questions in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match lines starting with number followed by period
        pattern = r'^\d+\.\s+'
        matches = re.findall(pattern, content, re.MULTILINE)
        return len(matches)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def count_questions_in_json(file_path: str) -> int:
    """Count questions in a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "questions" in data:
            return len(data["questions"])
        return 0
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def get_difficulty_stats(file_path: str) -> dict:
    """Get question count by difficulty from JSON file."""
    stats = {"beginner": 0, "intermediate": 0, "advanced": 0}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for q in data.get("questions", []):
            difficulty = q.get("difficulty", "").lower()
            if difficulty in stats:
                stats[difficulty] += 1
    except Exception:
        pass
    return stats


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print("=" * 60)
    print("Flutter Interview Questions - Statistics")
    print("=" * 60)
    print()

    categories = defaultdict(list)
    total_questions = 0

    # Scan Flutter directory
    flutter_dir = repo_root / "Flutter"
    if flutter_dir.exists():
        for topic_dir in sorted(flutter_dir.iterdir()):
            if topic_dir.is_dir():
                questions_file = topic_dir / "questions.md"
                if questions_file.exists():
                    count = count_questions_in_markdown(str(questions_file))
                    categories["Flutter"].append((topic_dir.name, count))
                    total_questions += count

    # Scan OOP directory
    oop_dir = repo_root / "OOP"
    if oop_dir.exists():
        for topic_dir in sorted(oop_dir.iterdir()):
            if topic_dir.is_dir():
                questions_file = topic_dir / "questions.md"
                if questions_file.exists():
                    count = count_questions_in_markdown(str(questions_file))
                    categories["OOP"].append((topic_dir.name, count))
                    total_questions += count

    # Scan DSA
    dsa_file = repo_root / "DSA" / "questions.md"
    if dsa_file.exists():
        count = count_questions_in_markdown(str(dsa_file))
        categories["DSA"].append(("Data Structures & Algorithms", count))
        total_questions += count

    # Scan Git
    git_file = repo_root / "Git" / "questions.md"
    if git_file.exists():
        count = count_questions_in_markdown(str(git_file))
        categories["Git"].append(("Version Control", count))
        total_questions += count

    # Print results
    for category, topics in categories.items():
        category_total = sum(count for _, count in topics)
        print(f"\n{category} ({category_total} questions)")
        print("-" * 40)
        for topic, count in topics:
            print(f"  {topic:<30} {count:>5}")

    print()
    print("=" * 60)
    print(f"TOTAL QUESTIONS: {total_questions}")
    print("=" * 60)

    # JSON statistics
    json_dir = repo_root / "json_data" / "flutter"
    if json_dir.exists():
        print("\n\nJSON Data Statistics")
        print("-" * 40)

        json_total = 0
        difficulty_totals = {"beginner": 0, "intermediate": 0, "advanced": 0}

        for json_file in sorted(json_dir.glob("*.json")):
            if json_file.name == "quiz_structure.json":
                continue

            count = count_questions_in_json(str(json_file))
            json_total += count

            stats = get_difficulty_stats(str(json_file))
            for level, c in stats.items():
                difficulty_totals[level] += c

            print(f"  {json_file.stem:<25} {count:>5}")

        print("-" * 40)
        print(f"  {'Total in JSON':<25} {json_total:>5}")
        print()
        print("By Difficulty:")
        for level, count in difficulty_totals.items():
            print(f"  {level.capitalize():<25} {count:>5}")

    # Generate markdown report
    report_path = repo_root / "STATISTICS.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Repository Statistics\n\n")
        f.write(f"**Total Questions: {total_questions}**\n\n")

        f.write("## By Category\n\n")
        f.write("| Category | Topic | Questions |\n")
        f.write("|----------|-------|----------:|\n")

        for category, topics in categories.items():
            for topic, count in topics:
                f.write(f"| {category} | {topic} | {count} |\n")

        f.write(f"\n## Summary\n\n")
        for category, topics in categories.items():
            category_total = sum(count for _, count in topics)
            f.write(f"- **{category}**: {category_total} questions\n")

    print(f"\n\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
