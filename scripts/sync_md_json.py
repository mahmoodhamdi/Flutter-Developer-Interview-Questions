#!/usr/bin/env python3
"""
Sync between markdown and JSON for every topic in the repo.

Workflow:
  1. Parse questions.md and answers.md for each topic.
  2. Build a JSON object that matches schema/question_schema.json.
  3. If the JSON file already exists, merge — keep manual tags/difficulty/code_example values.
  4. Validate the result against the schema. Exit non-zero on any validation error.

Markdown formats supported:
  Format A (most topics):
      questions.md:  '1. Question text?'
      answers.md:    '1. **Question text?**\n    Answer paragraph.'

  Format B (AdvancedTopics, Animations, Architecture, UI_UX):
      questions.md:  '1. Question text?'
      answers.md:    '## 1. Question text?\n\n**Answer:** Answer paragraph.'

  Format C (Firebase):
      questions.md:  '1. Question text?'
      answers.md:    '## Section Header\n\n**1. Question text?**\n\nAnswer paragraph.'

Usage:
  python3 scripts/sync_md_json.py            # dry-run + report drift
  python3 scripts/sync_md_json.py --write    # write updated JSON
  python3 scripts/sync_md_json.py --topic Flutter/Basics
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.stderr.write("jsonschema is required. pip install jsonschema\n")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "question_schema.json"
JSON_DIR = ROOT / "json_data"

# File-slug (JSON file name) overrides where the JSON file's name on disk
# differs from a naive lowercase of the directory.  ID slugs come from
# ID_SLUG_OVERRIDES, since IDs must match ^[a-z][a-z0-9_]*_\d{3}$.
SLUG_OVERRIDES = {
    "AdvancedTopics": "advanced_topics",
    "Async_Programming": "async_programming",
    "BestPractices": "best_practices",
    "CICD": "cicd",
    "CleanArchitecture": "clean_architecture",
    "Database_And_Storage": "database_and_storage",
    "FlutterInternals": "flutter_internals",
    "FlutterWebAndDesktop": "flutter_web_and_desktop",
    "PackagesAndPlugins": "packages_and_plugins",
    "StateManagement": "state-management",
    "UI_UX": "ui_ux",
}

# ID slug overrides (no hyphens allowed in IDs).
ID_SLUG_OVERRIDES = {
    "StateManagement": "state_management",
}


@dataclass
class Question:
    number: int
    question: str
    answer: str = ""
    difficulty: str = "intermediate"
    tags: list[str] = field(default_factory=list)
    code_example: Optional[str] = None
    references: list[str] = field(default_factory=list)


def slug_for(topic_dir: Path) -> str:
    """File-name slug, may include hyphens for legacy files like state-management.json."""
    name = topic_dir.name
    return SLUG_OVERRIDES.get(name, name.lower())


def id_slug_for(topic_dir: Path) -> str:
    """ID slug used inside JSON IDs. Must match ^[a-z][a-z0-9_]*_\\d{3}$ (no hyphens)."""
    name = topic_dir.name
    if name in ID_SLUG_OVERRIDES:
        return ID_SLUG_OVERRIDES[name]
    return slug_for(topic_dir).replace("-", "_")


def parse_questions_md(path: Path) -> dict[int, str]:
    """Return {number: question_text} from a questions.md file."""
    text = path.read_text(encoding="utf-8")
    out: dict[int, str] = {}
    pattern = re.compile(r"^(\d+)\.\s+(.+?)$", re.MULTILINE)
    for m in pattern.finditer(text):
        n = int(m.group(1))
        q = m.group(2).strip()
        # Skip lines that look like list continuations inside answers (shouldn't be here, but defensive).
        if 1 <= n <= 999:
            out[n] = q
    return out


def parse_answers_md(path: Path, question_numbers: set[int]) -> dict[int, str]:
    """Return {number: answer_text}. Handles Format A and Format B."""
    text = path.read_text(encoding="utf-8")
    out: dict[int, str] = {}

    # Format A: '\n1. **Q?**\n   Answer text...\n'
    fmt_a = re.compile(
        r"(?:^|\n)(\d+)\.\s+\*\*[^*]+\*\*\s*\n+([\s\S]*?)(?=(?:\n\d+\.\s+\*\*)|\Z)",
        re.MULTILINE,
    )
    # Format B: '\n## 1. Q?\n\n**Answer:** Answer text...\n'
    fmt_b = re.compile(
        r"(?:^|\n)##\s+(\d+)\.\s+[^\n]+\n+\*\*Answer:?\*\*\s*([\s\S]*?)(?=(?:\n##\s+\d+\.)|(?:\n##\s+\d+\.\s+\*\*)|\Z)",
        re.MULTILINE,
    )
    # Format C (Firebase): '\n**1. Q?**\n\nAnswer text...\n'
    fmt_c = re.compile(
        r"(?:^|\n)\*\*(\d+)\.\s+[^*]+\*\*\s*\n+([\s\S]*?)(?=(?:\n\*\*\d+\.)|(?:\n##\s+))",
        re.MULTILINE,
    )

    for pat in (fmt_a, fmt_b, fmt_c):
        for m in pat.finditer(text):
            n = int(m.group(1))
            if n not in question_numbers:
                continue
            answer = m.group(2).strip()
            # If a later format also matched, prefer the longer/richer answer.
            if n not in out or len(answer) > len(out[n]):
                out[n] = answer
    return out


def extract_code_example(answer: str) -> Optional[str]:
    m = re.search(r"```(?:dart|yaml|bash|xml)?\n([\s\S]*?)```", answer)
    return m.group(1).strip() if m else None


def existing_json(topic_dir: Path) -> Optional[dict]:
    """Return the existing JSON content for this topic if any."""
    slug = slug_for(topic_dir)
    # Flutter topics live under json_data/flutter/.
    if topic_dir.parent.name == "Flutter":
        candidate = JSON_DIR / "flutter" / f"{slug}.json"
    elif topic_dir.parent.name == "OOP":
        candidate = JSON_DIR / "oop" / f"{slug.lower()}.json"
    else:
        candidate = JSON_DIR / f"{slug}.json"
    if candidate.exists():
        try:
            return json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
    return None


def merge_existing_metadata(
    parsed: list[Question],
    prior: Optional[dict],
) -> list[Question]:
    """Keep difficulty/tags/code_example from prior JSON when answer text matches strongly."""
    if not prior or "questions" not in prior:
        return parsed
    by_question = {q["question"]: q for q in prior["questions"]}
    for q in parsed:
        match = by_question.get(q.question)
        if match:
            q.difficulty = match.get("difficulty", q.difficulty)
            q.tags = match.get("tags", q.tags) or q.tags
            q.code_example = match.get("code_example", q.code_example)
            q.references = match.get("references", q.references) or q.references
    return parsed


def build_topic_json(topic_dir: Path) -> Optional[dict]:
    qfile = topic_dir / "questions.md"
    afile = topic_dir / "answers.md"
    if not (qfile.exists() and afile.exists()):
        return None
    questions = parse_questions_md(qfile)
    answers = parse_answers_md(afile, set(questions.keys()))
    if not questions:
        return None

    file_slug = slug_for(topic_dir)
    id_slug = id_slug_for(topic_dir)
    parsed: list[Question] = []
    for n in sorted(questions.keys()):
        q_text = questions[n]
        a_text = answers.get(n, "(answer pending — see answers.md)")
        item = Question(
            number=n,
            question=q_text,
            answer=a_text,
            tags=[file_slug.replace("_", "-")],
        )
        item.code_example = extract_code_example(a_text)
        parsed.append(item)

    prior = existing_json(topic_dir)
    parsed = merge_existing_metadata(parsed, prior)

    return {
        "topic": (prior or {}).get("topic") or topic_dir.name.replace("_", " "),
        "description": (prior or {}).get("description")
            or f"Interview questions and answers for {topic_dir.name.replace('_', ' ')}.",
        "version": "2.0.0",
        "last_updated": date.today().isoformat(),
        "flutter_version_target": "3.27",
        "questions": [
            {
                "id": f"{id_slug}_{q.number:03d}",
                "question": q.question,
                "answer": q.answer,
                "difficulty": q.difficulty,
                "tags": q.tags or [file_slug.replace("_", "-")],
                **({"code_example": q.code_example} if q.code_example else {}),
                **({"references": q.references} if q.references else {}),
            }
            for q in parsed
        ],
    }


def topic_dirs() -> list[Path]:
    out: list[Path] = []
    for parent in ("Flutter", "OOP"):
        p = ROOT / parent
        if p.exists():
            for d in sorted(p.iterdir()):
                if d.is_dir():
                    out.append(d)
    for top in ("DSA", "Git"):
        d = ROOT / top
        if d.exists():
            out.append(d)
    return out


def target_path(topic_dir: Path) -> Path:
    slug = slug_for(topic_dir)
    if topic_dir.parent.name == "Flutter":
        return JSON_DIR / "flutter" / f"{slug}.json"
    if topic_dir.parent.name == "OOP":
        return JSON_DIR / "oop" / f"{slug.lower()}.json"
    return JSON_DIR / f"{slug.lower()}.json"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write updated JSON files.")
    parser.add_argument("--topic", help="Limit to one topic (e.g. Flutter/Basics).")
    parser.add_argument("--no-validate", action="store_true", help="Skip schema validation.")
    args = parser.parse_args(argv)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema)

    dirs = topic_dirs()
    if args.topic:
        dirs = [d for d in dirs if str(d.relative_to(ROOT)).replace("\\", "/") == args.topic]
        if not dirs:
            sys.stderr.write(f"no topic matched {args.topic}\n")
            return 2

    failures = 0
    written = 0
    for d in dirs:
        rel = d.relative_to(ROOT)
        data = build_topic_json(d)
        if data is None:
            print(f"-- {rel}: skipped (missing questions.md or answers.md)")
            continue

        if not args.no_validate:
            errors = list(validator.iter_errors(data))
            if errors:
                failures += 1
                print(f"✗  {rel}: {len(errors)} schema error(s)")
                for e in errors[:5]:
                    print(f"   {' / '.join(map(str, e.absolute_path))}: {e.message}")
                continue

        tgt = target_path(d)
        if args.write:
            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            written += 1
            print(f"✓  {rel} → {tgt.relative_to(ROOT)} ({len(data['questions'])} questions)")
        else:
            print(f"✓  {rel} → would write {tgt.relative_to(ROOT)} ({len(data['questions'])} questions)")

    print()
    print(f"Topics processed: {len(dirs)}, errors: {failures}, written: {written}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
