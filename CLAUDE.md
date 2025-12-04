# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **content repository** containing Flutter developer interview questions and answers. It is **not a code project** - there are no build commands, tests, or linting to run. The repository serves as educational documentation for Flutter interview preparation.

## Content Structure

**Markdown content (primary):**
```
Category/
  Topic/
    questions.md  - Numbered list of interview questions
    answers.md    - Corresponding detailed answers with matching numbers
```

**Categories:**
- `Flutter/` - 20 topics (Basics, Dart, Widgets, StateManagement, Architecture, Animations, etc.)
- `OOP/` - 6 topics (Abstraction, Encapsulation, Inheritance, Polymorphism, SOLID_Principles, Design_Patterns)
- `DSA/`, `Git/`, `Flutter/CICD/`, `Flutter/Firebase/` - Planned topics (in progress)

**JSON data format:** `json_data/flutter/` contains structured versions with metadata:
```json
{
  "topic": "Topic Name",
  "description": "Topic description",
  "questions": [
    {
      "id": "topic_001",
      "question": "question text",
      "answer": "detailed answer",
      "difficulty": "beginner|intermediate|advanced",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

## Content Guidelines

**Markdown files:**
- Questions: Numbered list format (1. Question text)
- Answers: Number + bold question header + answer paragraph
- Match question numbers between files

**JSON files:**
- ID format: `{topic}_{number}` (e.g., `state_001`, `widgets_015`)
- Difficulty: single value - `beginner`, `intermediate`, or `advanced`
- Tags: lowercase, hyphenated (e.g., `state-management`, `bloc`)
- Update `json_data/quiz_structure.json` when adding new topics

## Known Issues

Two folders have typo in filename (`anwers.md` instead of `answers.md`):
- `Flutter/Basics/anwers.md`
- `Flutter/Dart/anwers.md`

## Planning Requirement

Before implementing any feature, create a detailed plan in a `.md` file explaining the feature, implementation approach, and workflow context.
