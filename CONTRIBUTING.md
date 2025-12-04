# Contributing to Flutter Developer Interview Questions

Thank you for your interest in contributing! This guide will help you get started.

## How to Contribute

### Adding New Questions

1. **Fork** the repository
2. **Create a branch** for your changes
3. **Add questions** following the format below
4. **Submit a Pull Request**

### Question Format

**In `questions.md`:**
```markdown
1. Your question here?
2. Another question?
```

**In `answers.md`:**
```markdown
**1. Your question here?**
Your detailed answer with code examples if applicable.

---

**2. Another question?**
Another detailed answer.
```

### JSON Format

```json
{
  "id": "topic_001",
  "question": "Your question here?",
  "answer": "Detailed answer...",
  "difficulty": "beginner",
  "tags": ["tag1", "tag2"]
}
```

**Difficulty levels:** `beginner`, `intermediate`, `advanced`

---

## Content Guidelines

### Questions Should Be

- Clear and unambiguous
- Relevant to Flutter/Dart development
- Practical for real interviews
- Not duplicates of existing questions

### Answers Should Include

- Clear explanation
- Code examples (when applicable)
- Best practices
- Common mistakes to avoid (when relevant)

### Code Examples

- Use proper Dart syntax
- Include comments for complex logic
- Follow Dart style guide
- Test code before submitting

---

## Directory Structure

```
Flutter/
  TopicName/
    questions.md
    answers.md

OOP/
  TopicName/
    questions.md
    answers.md

json_data/
  flutter/
    topic-name.json
```

### Adding a New Topic

1. Create a new directory under the appropriate category
2. Add `questions.md` and `answers.md`
3. Update `json_data/quiz_structure.json`
4. Optionally add JSON version in `json_data/`

---

## Pull Request Process

### Before Submitting

- [ ] Questions are numbered correctly
- [ ] Answers match question numbers
- [ ] Code examples are tested
- [ ] Spelling and grammar checked
- [ ] No duplicate questions
- [ ] JSON files are valid (if modified)

### PR Title Format

```
feat: Add questions about [topic]
fix: Correct answer for [topic] question #X
docs: Update [topic] explanation
```

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Added X questions about [topic]
- Fixed typo in [file]
- Updated explanation for [topic]

## Checklist
- [ ] Questions follow format guidelines
- [ ] Answers include code examples
- [ ] No duplicate questions
- [ ] Tested any code examples
```

---

## Code of Conduct

### Be Respectful

- Welcome newcomers
- Be patient with questions
- Provide constructive feedback

### Be Professional

- Focus on content quality
- No spam or self-promotion
- Credit sources when applicable

---

## Getting Help

- **Questions?** Open an issue with the `question` label
- **Found a bug?** Open an issue with the `bug` label
- **Feature idea?** Open an issue with the `enhancement` label

---

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Future acknowledgments section

Thank you for helping make this resource better!
