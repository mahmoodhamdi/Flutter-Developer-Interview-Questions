#!/usr/bin/env python3
"""
Validate JSON files in the repository.
Checks for valid JSON syntax and required structure.
"""

import json
import os
import sys
from pathlib import Path


def validate_json_syntax(file_path: str) -> tuple[bool, str]:
    """Check if file contains valid JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, ""
    except json.JSONDecodeError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def validate_question_structure(data: dict, file_path: str) -> list[str]:
    """Validate the structure of a question JSON file."""
    errors = []

    # Check top-level fields
    if "topic" not in data:
        errors.append("Missing 'topic' field")

    if "questions" not in data:
        errors.append("Missing 'questions' field")
        return errors

    # Check each question
    required_fields = ["id", "question", "answer", "difficulty", "tags"]
    valid_difficulties = ["beginner", "intermediate", "advanced"]

    for i, question in enumerate(data["questions"], 1):
        for field in required_fields:
            if field not in question:
                errors.append(f"Question {i}: Missing '{field}'")

        if "difficulty" in question:
            if question["difficulty"] not in valid_difficulties:
                errors.append(
                    f"Question {i}: Invalid difficulty '{question['difficulty']}'. "
                    f"Must be one of: {valid_difficulties}"
                )

        if "tags" in question:
            if not isinstance(question["tags"], list):
                errors.append(f"Question {i}: 'tags' must be an array")

        if "id" in question:
            # Check ID format (should be topic_number)
            if not question["id"] or "_" not in question["id"]:
                errors.append(
                    f"Question {i}: ID '{question.get('id')}' should follow "
                    "format 'topic_number' (e.g., 'basics_001')"
                )

    return errors


def main():
    """Main entry point."""
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    json_data_dir = repo_root / "json_data"

    if not json_data_dir.exists():
        print(f"Error: json_data directory not found at {json_data_dir}")
        sys.exit(1)

    print("Validating JSON files...\n")

    total_files = 0
    valid_files = 0
    errors_found = []

    # Find all JSON files
    for json_file in json_data_dir.rglob("*.json"):
        total_files += 1
        relative_path = json_file.relative_to(repo_root)

        # Check syntax
        is_valid, error_msg = validate_json_syntax(str(json_file))
        if not is_valid:
            errors_found.append((relative_path, [f"Invalid JSON: {error_msg}"]))
            print(f"❌ {relative_path}: Invalid JSON syntax")
            continue

        # Skip quiz_structure.json (different format)
        if json_file.name == "quiz_structure.json":
            print(f"✅ {relative_path}: Valid (structure file)")
            valid_files += 1
            continue

        # Check structure for question files
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        structure_errors = validate_question_structure(data, str(json_file))
        if structure_errors:
            errors_found.append((relative_path, structure_errors))
            print(f"❌ {relative_path}: Structure errors")
            for error in structure_errors:
                print(f"   - {error}")
        else:
            print(f"✅ {relative_path}: Valid ({len(data.get('questions', []))} questions)")
            valid_files += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Total files: {total_files}")
    print(f"Valid files: {valid_files}")
    print(f"Files with errors: {len(errors_found)}")

    if errors_found:
        print("\nFiles with errors:")
        for file_path, errors in errors_found:
            print(f"\n{file_path}:")
            for error in errors:
                print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✅ All JSON files are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
